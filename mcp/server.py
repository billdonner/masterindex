#!/usr/bin/env python3
"""A dependency-free MCP server for MasterIndex portfolio queries and intake.

The server deliberately reads the three canonical JSON files for every tool
call.  That makes a long-running client see a completed refresh immediately,
without a restart or an in-memory cache becoming another source of truth.

It speaks the MCP stdio JSON-lines transport.  Keep stdout protocol-only;
diagnostics belong on stderr.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from project_intake import IntakeError, ProjectIntakeStore

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "current" / "index.json"
TASKS_PATH = ROOT / "tasks" / "index.json"
HANDOFFS_PATH = ROOT / "current" / "handoffs" / "index.json"
PROTOCOL_VERSION = "2025-06-18"
PROJECT_INTAKE = ProjectIntakeStore(ROOT)


def read_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def load_data() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    return read_json(INDEX_PATH), read_json(TASKS_PATH), read_json(HANDOFFS_PATH)


def normalize(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())


def iso_date(value: Any) -> date | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return date.fromisoformat(value[:10])
        except ValueError:
            return None


def age_days(value: Any) -> int | None:
    observed = iso_date(value)
    return (date.today() - observed).days if observed else None


def active_tasks(tasks: dict[str, Any], entity_id: str) -> list[dict[str, Any]]:
    return [task for task in tasks.get("entryTasks", {}).get(entity_id, []) if task.get("status") == "active"]


def target_matches(entity: dict[str, Any], target: Any) -> bool:
    candidate = normalize(target)
    if not candidate:
        return False
    values = [normalize(entity.get("id")), normalize(entity.get("name"))]
    return any(candidate == value or candidate in value or value in candidate for value in values if value)


def active_handoffs(handoffs: dict[str, Any], entity: dict[str, Any]) -> list[dict[str, Any]]:
    matched = []
    for directive in handoffs.get("directives", []):
        if directive.get("status") != "active":
            continue
        targets = directive.get("targets", [])
        if "all-entities" in targets or any(target_matches(entity, target) for target in targets):
            matched.append(directive)
    return matched


def compact_entity(entity: dict[str, Any], tasks: dict[str, Any]) -> dict[str, Any]:
    return {
        key: entity.get(key)
        for key in ("id", "name", "kind", "status", "cluster", "repo", "bundleId", "lastModified", "description")
    } | {"activeTaskCount": len(active_tasks(tasks, entity["id"]))}


def entity_matches_query(entity: dict[str, Any], query: str) -> tuple[bool, list[str]]:
    needle = query.lower().strip()
    if not needle:
        return True, []
    fields = {
        "id": entity.get("id"),
        "name": entity.get("name"),
        "kind": entity.get("kind"),
        "status": entity.get("status"),
        "cluster": entity.get("cluster"),
        "repo": entity.get("repo"),
        "description": entity.get("description"),
        "dependencies": " ".join(entity.get("dependencies", [])),
        "notes": " ".join(entity.get("notes", [])),
        "links": " ".join(str(value) for value in entity.get("links", {}).values() if value),
    }
    matched = [field for field, value in fields.items() if needle in str(value or "").lower()]
    return bool(matched), matched


def resolve_related(entity: dict[str, Any], index: dict[str, Any]) -> dict[str, Any]:
    entities = index.get("entities", [])
    direct_dependencies = entity.get("dependencies", [])
    entity_keys = {normalize(entity.get("id")), normalize(entity.get("name"))}
    related = []
    consumers = []
    for candidate in entities:
        if candidate.get("id") == entity.get("id"):
            continue
        candidate_keys = {normalize(candidate.get("id")), normalize(candidate.get("name"))}
        if any(
            dep and any(dep == key or dep in key or key in dep for key in candidate_keys)
            for dep in map(normalize, direct_dependencies)
        ):
            related.append({"relationship": "depends-on", "entity": compact_entity(candidate, {"entryTasks": {}})})
        if any(
            dep and any(dep == key or dep in key or key in dep for key in entity_keys)
            for dep in map(normalize, candidate.get("dependencies", []))
        ):
            consumers.append({"relationship": "depended-on-by", "entity": compact_entity(candidate, {"entryTasks": {}})})
    services = []
    for service in index.get("services", []):
        service_text = " ".join([str(service.get("name", "")), *map(str, service.get("consumers", [])), str(service.get("repo", ""))])
        if any(key and key in normalize(service_text) for key in entity_keys):
            services.append(service)
    return {
        "declaredDependencyNames": direct_dependencies,
        "resolvedEntities": related,
        "consumerEntities": consumers,
        "relatedServices": services,
        "sameCluster": [compact_entity(item, {"entryTasks": {}}) for item in entities if item.get("cluster") == entity.get("cluster") and item.get("id") != entity.get("id")],
    }


def tool_search(arguments: dict[str, Any]) -> dict[str, Any]:
    index, tasks, handoffs = load_data()
    query = str(arguments.get("query", "")).strip()
    kinds = set(arguments.get("kinds") or [])
    statuses = set(arguments.get("statuses") or [])
    cluster = arguments.get("cluster")
    limit = min(max(int(arguments.get("limit", 12)), 1), 50)
    results = []
    for entity in index.get("entities", []):
        matches, fields = entity_matches_query(entity, query)
        if not matches or (kinds and entity.get("kind") not in kinds) or (statuses and entity.get("status") not in statuses):
            continue
        if cluster and entity.get("cluster", "").casefold() != str(cluster).casefold():
            continue
        result = compact_entity(entity, tasks) | {"matchedFields": fields}
        if arguments.get("includeLinks"):
            result["links"] = entity.get("links", {})
        if arguments.get("includeHandoffs"):
            result["activeHandoffCount"] = len(active_handoffs(handoffs, entity))
        results.append(result)
    results.sort(key=lambda item: (item.get("lastModified") or "", item.get("name") or ""), reverse=True)
    return {"query": query, "resultCount": len(results), "returnedCount": min(len(results), limit), "results": results[:limit]}


def tool_get_entity(arguments: dict[str, Any]) -> dict[str, Any]:
    entity_id = str(arguments.get("id", "")).strip()
    index, tasks, handoffs = load_data()
    entity = next((item for item in index.get("entities", []) if item.get("id") == entity_id), None)
    if not entity:
        raise ValueError(f"Unknown entity id: {entity_id}. Use search_portfolio to find ids.")
    result = dict(entity)
    result["activeTasks"] = active_tasks(tasks, entity_id)
    result["activeHandoffs"] = active_handoffs(handoffs, entity)
    result["relationships"] = resolve_related(entity, index)
    result["freshness"] = {"lastModified": entity.get("lastModified"), "ageDays": age_days(entity.get("lastModified"))}
    return result


def tool_freshness(arguments: dict[str, Any]) -> dict[str, Any]:
    index, tasks, handoffs = load_data()
    threshold = min(max(int(arguments.get("staleAfterDays", 7)), 1), 365)
    sources = {
        "inventory": {"path": "current/index.json", "generatedAt": index.get("generatedAt")},
        "tasks": {"path": "tasks/index.json", "generatedAt": tasks.get("generatedAt")},
        "handoffs": {"path": "current/handoffs/index.json", "generatedAt": handoffs.get("generatedAt")},
    }
    for source in sources.values():
        source["ageDays"] = age_days(source["generatedAt"])
        source["stale"] = source["ageDays"] is None or source["ageDays"] > threshold
    stale_entities = [
        compact_entity(entity, tasks) | {"ageDays": age_days(entity.get("lastModified"))}
        for entity in index.get("entities", [])
        if age_days(entity.get("lastModified")) is None or age_days(entity.get("lastModified")) > threshold
    ]
    stale_entities.sort(key=lambda item: item.get("ageDays") or 10**9, reverse=True)
    return {
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "staleAfterDays": threshold,
        "sources": sources,
        "entityCount": len(index.get("entities", [])),
        "staleEntityCount": len(stale_entities),
        "staleEntities": stale_entities[:50],
        "interpretation": "Freshness is a signal, not proof of truth. It measures the recorded observation dates; unavailable sources must remain explicit gaps.",
        "notChecked": "This tool reads recorded dates only. Run check_local_sources for current local Git evidence on MasterIndex or selected entities, and verify_public_links only when public HTTP availability matters.",
    }


def run_source_command(arguments: list[str], directory: Path) -> tuple[bool, str]:
    """Run a bounded, read-only Git command without exposing credentials."""
    completed = subprocess.run(arguments, cwd=directory, text=True, capture_output=True, timeout=8, check=False)
    if completed.returncode:
        return False, (completed.stderr or completed.stdout).strip()
    return True, completed.stdout.strip()


def local_git_source(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"status": "unavailable", "reason": "Recorded local path does not exist on this Mac."}
    if not path.is_dir():
        return {"status": "unavailable", "reason": "Recorded path is not a directory."}
    ok, head = run_source_command(["git", "rev-parse", "--is-inside-work-tree"], path)
    if not ok or head != "true":
        return {"status": "unavailable", "reason": "Recorded directory is not a readable Git working tree."}
    _, branch = run_source_command(["git", "branch", "--show-current"], path)
    _, revision = run_source_command(["git", "rev-parse", "--short", "HEAD"], path)
    _, last_commit = run_source_command(["git", "log", "-1", "--format=%cI"], path)
    _, status = run_source_command(["git", "status", "--porcelain"], path)
    _, origin = run_source_command(["git", "remote", "get-url", "origin"], path)
    return {
        "status": "observed-local", "branch": branch or None, "head": revision or None,
        "lastCommitAt": last_commit or None, "dirty": bool(status), "originConfigured": bool(origin),
        "remoteSync": "not checked; local Git status does not establish whether origin is current."
    }


def expand_recorded_repo(recorded_path: Any) -> Path | None:
    if not isinstance(recorded_path, str) or not recorded_path:
        return None
    if recorded_path == "~":
        return Path.home()
    if recorded_path.startswith("~/"):
        return Path.home() / recorded_path[2:]
    return None


def tool_local_sources(arguments: dict[str, Any]) -> dict[str, Any]:
    """Verify present local files/repositories without contacting a remote."""
    index, _, _ = load_data()
    requested_ids = list(dict.fromkeys(arguments.get("entityIds") or []))
    if len(requested_ids) > 30:
        raise ValueError("Check no more than 30 entity ids at a time.")
    entities_by_id = {entity.get("id"): entity for entity in index.get("entities", [])}
    unknown = [entity_id for entity_id in requested_ids if entity_id not in entities_by_id]
    if unknown:
        raise ValueError(f"Unknown entity ids: {', '.join(unknown)}")
    checks = []
    for entity_id in requested_ids:
        entity = entities_by_id[entity_id]
        recorded_path = entity.get("repo")
        local_path = expand_recorded_repo(recorded_path)
        check = {"entityId": entity_id, "name": entity.get("name"), "recordedRepo": recorded_path}
        if local_path is None:
            check["source"] = {"status": "not-checkable", "reason": "No safe local ~/ repository path is recorded for this entity."}
        else:
            check["source"] = local_git_source(local_path)
        checks.append(check)
    return {
        "checkedAt": datetime.now(timezone.utc).isoformat(),
        "scope": "local filesystem and Git metadata only; no fetch, pull, push, remote sync, deployment, App Store, or network check was performed.",
        "masterIndex": local_git_source(ROOT),
        "entityChecks": checks,
        "next": "Use verify_public_links for explicit public HTTP checks. A separate authenticated source is required for App Store Connect, deployment, or GitHub remote truth."
    }


def tool_public_links(arguments: dict[str, Any]) -> dict[str, Any]:
    """Explicitly check public URLs; availability is not a release-state claim."""
    index, _, _ = load_data()
    requested_ids = list(dict.fromkeys(arguments.get("entityIds") or []))
    if not requested_ids:
        raise ValueError("entityIds is required so public HTTP checks stay deliberate and bounded.")
    if len(requested_ids) > 15:
        raise ValueError("Check no more than 15 entities at a time.")
    timeout = min(max(int(arguments.get("timeoutSeconds", 6)), 2), 20)
    entities_by_id = {entity.get("id"): entity for entity in index.get("entities", [])}
    unknown = [entity_id for entity_id in requested_ids if entity_id not in entities_by_id]
    if unknown:
        raise ValueError(f"Unknown entity ids: {', '.join(unknown)}")
    checks = []
    for entity_id in requested_ids:
        entity = entities_by_id[entity_id]
        for label, url in entity.get("links", {}).items():
            if not isinstance(url, str) or not url.startswith(("https://", "http://")):
                continue
            try:
                request = Request(url, method="HEAD", headers={"User-Agent": "MasterIndex-MCP/0.3"})
                with urlopen(request, timeout=timeout) as response:
                    checks.append({"entityId": entity_id, "link": label, "url": url, "status": "reachable", "httpStatus": response.status, "finalUrl": response.url})
            except HTTPError as error:
                checks.append({"entityId": entity_id, "link": label, "url": url, "status": "http-error", "httpStatus": error.code})
            except (URLError, TimeoutError, OSError) as error:
                checks.append({"entityId": entity_id, "link": label, "url": url, "status": "unreachable", "reason": str(error)})
    return {
        "checkedAt": datetime.now(timezone.utc).isoformat(), "scope": "Public HTTP availability only; this does not authenticate, inspect private content, or establish product/release state.",
        "entityIds": requested_ids, "checks": checks
    }


def tool_brief(arguments: dict[str, Any]) -> dict[str, Any]:
    index, tasks, handoffs = load_data()
    focus = arguments.get("focus", "attention")
    entities = index.get("entities", [])
    active_directives = [item for item in handoffs.get("directives", []) if item.get("status") == "active"]
    active_entry_tasks = [
        {"entityId": entity_id, **task}
        for entity_id, task_list in tasks.get("entryTasks", {}).items()
        for task in task_list if task.get("status") == "active"
    ]
    payload: dict[str, Any] = {
        "focus": focus,
        "inventoryGeneratedAt": index.get("generatedAt"),
        "verificationState": "Recorded inventory view only. portfolio_brief does not itself inspect local repositories, remotes, services, public links, or App Store Connect.",
        "counts": {"entities": len(entities), "repos": len(index.get("repos", [])), "services": len(index.get("services", [])), "gaps": len(index.get("gaps", [])), "activeHandoffs": len(active_directives), "activeEntryTasks": len(active_entry_tasks)},
    }
    if focus in ("attention", "all"):
        payload["gaps"] = index.get("gaps", [])[:20]
        payload["activeHandoffs"] = [{key: item.get(key) for key in ("id", "targets", "summary", "createdAt", "spec")} for item in active_directives]
        payload["freshness"] = tool_freshness({"staleAfterDays": arguments.get("staleAfterDays", 14)})
    if focus in ("release", "all"):
        payload["releaseCandidates"] = [compact_entity(entity, tasks) for entity in entities if entity.get("status") in {"ready-for-sale", "ready-for-distribution", "asc-mapped", "testflight-internal"}]
    if focus in ("operations", "all"):
        payload["services"] = index.get("services", [])
        payload["scheduledWork"] = active_entry_tasks[:50]
    return payload


def tool_worklist(_: dict[str, Any]) -> dict[str, Any]:
    index, tasks, handoffs = load_data()
    active_directives = [item for item in handoffs.get("directives", []) if item.get("status") == "active"]
    active_global = [item for item in tasks.get("globalTasks", []) if item.get("status") == "active"]
    active_entry = [
        {"entityId": entity_id, "entityName": next((entity.get("name") for entity in index.get("entities", []) if entity.get("id") == entity_id), None), **task}
        for entity_id, task_list in tasks.get("entryTasks", {}).items()
        for task in task_list if task.get("status") == "active"
    ]
    return {
        "activeGlobalTasks": active_global,
        "activeEntryTasks": active_entry,
        "activeHandoffs": active_directives,
        "note": "The registry defines cadence, not execution history. Do not claim a task is complete or overdue without an observed run record.",
    }


def tool_capture_project_idea(arguments: dict[str, Any]) -> dict[str, Any]:
    project = PROJECT_INTAKE.capture(
        name=arguments.get("name", ""), purpose=arguments.get("purpose", ""),
        slug=arguments.get("slug") or None, kind=arguments.get("kind", "project"),
    )
    return {
        "project": project,
        "next": "Review the proposal and call provision_project only when you explicitly want its folder, private GitHub repository, and MasterIndex registration created.",
        "provisioningPlan": PROJECT_INTAKE.provisioning_plan(project["id"]),
    }


def tool_provision_project(arguments: dict[str, Any]) -> dict[str, Any]:
    return PROJECT_INTAKE.provision(
        project_id=arguments.get("id", ""), confirmation=arguments.get("confirmation", ""),
        create_github=arguments.get("createGithub", True),
    )


TOOLS = [
    {"name": "search_portfolio", "description": "Search software assets by name, capability, dependency, repository, URL, status, cluster, or free text. Start here for general portfolio questions.", "inputSchema": {"type": "object", "properties": {"query": {"type": "string", "description": "Words or phrase to find; empty returns assets matching filters."}, "kinds": {"type": "array", "items": {"type": "string"}}, "statuses": {"type": "array", "items": {"type": "string"}}, "cluster": {"type": "string"}, "limit": {"type": "integer", "default": 12, "minimum": 1, "maximum": 50}, "includeLinks": {"type": "boolean", "default": False}, "includeHandoffs": {"type": "boolean", "default": False}}}},
    {"name": "get_entity", "description": "Return the full record for one stable entity id, with its active tasks, active handoffs, related assets, consumers, services, and freshness signal.", "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}}, "required": ["id"]}},
    {"name": "portfolio_brief", "description": "Give a grounded cross-portfolio brief. Use attention for gaps and staleness, release for App Store/release posture, operations for services and scheduled work, or all.", "inputSchema": {"type": "object", "properties": {"focus": {"type": "string", "enum": ["attention", "release", "operations", "all"], "default": "attention"}, "staleAfterDays": {"type": "integer", "default": 14, "minimum": 1, "maximum": 365}}}},
    {"name": "get_freshness", "description": "Report age of the canonical inventory, task, and handoff registries plus assets whose recorded observations are older than a chosen threshold.", "inputSchema": {"type": "object", "properties": {"staleAfterDays": {"type": "integer", "default": 7, "minimum": 1, "maximum": 365}}}},
    {"name": "check_local_sources", "description": "Read current local Git state for MasterIndex and selected indexed repositories. It never fetches, pulls, pushes, contacts a remote, or changes files. Use it to distinguish recorded facts from locally observed source state.", "inputSchema": {"type": "object", "properties": {"entityIds": {"type": "array", "items": {"type": "string"}, "maxItems": 30, "description": "Stable entity ids to inspect. Omit to inspect only MasterIndex itself."}}}},
    {"name": "verify_public_links", "description": "Explicitly make bounded public HTTP HEAD requests for recorded links on selected entities. Availability does not prove a release, service health, ownership, or current App Store state.", "inputSchema": {"type": "object", "properties": {"entityIds": {"type": "array", "items": {"type": "string"}, "minItems": 1, "maxItems": 15}, "timeoutSeconds": {"type": "integer", "default": 6, "minimum": 2, "maximum": 20}}, "required": ["entityIds"]}},
    {"name": "get_maintenance_worklist", "description": "Return active periodic tasks and targeted handoffs. This is routing data, not a claim that any task ran.", "inputSchema": {"type": "object", "properties": {}}},
    {"name": "capture_project_idea", "description": "Create a reviewable project-intake proposal from a name and purpose. This writes only intake/index.json; it does not make folders, GitHub repositories, deployments, domains, or App Store records.", "inputSchema": {"type": "object", "properties": {"name": {"type": "string"}, "purpose": {"type": "string"}, "slug": {"type": "string", "description": "Optional lowercase GitHub/local-folder slug."}, "kind": {"type": "string", "enum": ["project", "app", "backend", "service", "package", "website"], "default": "project"}}, "required": ["name", "purpose"]}},
    {"name": "provision_project", "description": "Provision one captured idea only after the user has explicitly approved it. It creates a local Git repo, private GitHub repo (unless disabled), scaffold, canonical MasterIndex entity, and initial weekly review task. The confirmation must exactly equal the project name.", "inputSchema": {"type": "object", "properties": {"id": {"type": "string"}, "confirmation": {"type": "string", "description": "Exact project name; this is a deliberate confirmation."}, "createGithub": {"type": "boolean", "default": True, "description": "Create and push the default private GitHub repository."}}, "required": ["id", "confirmation"]}},
]
for _tool in TOOLS:
    _tool["annotations"] = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}
for _tool in TOOLS:
    if _tool["name"] in {"capture_project_idea", "provision_project"}:
        _tool["annotations"] = {"readOnlyHint": False, "destructiveHint": False, "idempotentHint": False, "openWorldHint": _tool["name"] == "provision_project"}
    if _tool["name"] == "verify_public_links":
        _tool["annotations"] = {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": True}


def resource_list() -> list[dict[str, Any]]:
    return [
        {"uri": "masterindex://inventory/current", "name": "Current inventory", "description": "Authoritative current/index.json", "mimeType": "application/json"},
        {"uri": "masterindex://inventory/narrative", "name": "Inventory narrative", "description": "Human narrative context; current/index.json remains authoritative for facts", "mimeType": "text/markdown"},
        {"uri": "masterindex://tasks/current", "name": "Task registry", "description": "Recurring operational tasks", "mimeType": "application/json"},
        {"uri": "masterindex://handoffs/current", "name": "Handoff registry", "description": "Active and historical targeted directives", "mimeType": "application/json"},
    ]


def handle(method: str, params: dict[str, Any]) -> Any:
    if method == "initialize":
        return {"protocolVersion": PROTOCOL_VERSION, "capabilities": {"tools": {}, "resources": {}}, "serverInfo": {"name": "masterindex", "version": "0.3.0"}, "instructions": "Portfolio knowledge server. Treat dates as recorded observations. For current local source evidence, use check_local_sources after get_freshness; it never contacts a remote. Use verify_public_links only when public HTTP availability is relevant. capture_project_idea only saves a reviewable proposal. provision_project changes local files, GitHub, and MasterIndex only after exact-name confirmation."}
    if method == "ping":
        return {}
    if method == "notifications/initialized":
        return None
    if method == "tools/list":
        return {"tools": TOOLS}
    if method == "tools/call":
        name = params.get("name")
        functions = {"search_portfolio": tool_search, "get_entity": tool_get_entity, "portfolio_brief": tool_brief, "get_freshness": tool_freshness, "check_local_sources": tool_local_sources, "verify_public_links": tool_public_links, "get_maintenance_worklist": tool_worklist, "capture_project_idea": tool_capture_project_idea, "provision_project": tool_provision_project}
        if name not in functions:
            raise ValueError(f"Unknown tool: {name}")
        result = functions[name](params.get("arguments") or {})
        return {"content": [{"type": "text", "text": json.dumps(result, indent=2, ensure_ascii=False)}], "structuredContent": result}
    if method == "resources/list":
        return {"resources": resource_list()}
    if method == "resources/read":
        paths = {"masterindex://inventory/current": INDEX_PATH, "masterindex://inventory/narrative": ROOT / "current" / "inventory.md", "masterindex://tasks/current": TASKS_PATH, "masterindex://handoffs/current": HANDOFFS_PATH}
        uri = params.get("uri")
        if uri not in paths:
            raise ValueError(f"Unknown resource: {uri}")
        mime_type = "text/markdown" if uri == "masterindex://inventory/narrative" else "application/json"
        return {"contents": [{"uri": uri, "mimeType": mime_type, "text": paths[uri].read_text(encoding="utf-8")}]} 
    raise ValueError(f"Method not found: {method}")


def emit(message: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(message, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main() -> None:
    for raw in sys.stdin:
        request: dict[str, Any] | None = None
        try:
            request = json.loads(raw)
            if not isinstance(request, dict):
                raise ValueError("Request must be a JSON object")
            request_id = request.get("id")
            method = request.get("method")
            if not method:
                raise ValueError("Request missing method")
            result = handle(method, request.get("params") or {})
            if request_id is not None:
                emit({"jsonrpc": "2.0", "id": request_id, "result": result})
        except Exception as exc:  # Protocol errors must remain machine-readable.
            if request is not None and request.get("id") is not None:
                emit({"jsonrpc": "2.0", "id": request["id"], "error": {"code": -32602, "message": str(exc)}})
            else:
                print(f"masterindex MCP error: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
