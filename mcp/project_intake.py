"""Shared, local-only project-intake operations for MCP and the browser UI."""

from __future__ import annotations

import json
import re
import shutil
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any


class IntakeError(ValueError):
    """A safe, user-actionable intake or provisioning error."""


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def write_json(path: Path, data: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,62}", slug):
        raise IntakeError("Use a project name that becomes a 2–63 character lowercase slug.")
    return slug


def normalized(value: Any) -> str:
    return re.sub(r"[^a-z0-9]+", "", str(value or "").lower())


class ProjectIntakeStore:
    """Owns the reviewable intake registry and intentional provisioning flow."""

    def __init__(self, root: Path, project_parent: Path | None = None):
        self.root = root.resolve()
        self.path = self.root / "intake" / "index.json"
        self.index_path = self.root / "current" / "index.json"
        self.tasks_path = self.root / "tasks" / "index.json"
        self.narrative_path = self.root / "current" / "inventory.md"
        self.project_parent = (project_parent or Path.home()).resolve()

    def registry(self) -> dict[str, Any]:
        return load_json(self.path)

    def process_inbox(self) -> list[dict[str, Any]]:
        """Turn ideas sent from elsewhere (the iOS app appends to `inbox`) into captured ideas.

        Each goes through `capture`, so the same checks apply as for an idea
        typed here. One that fails stays in the inbox with the reason, so its
        sender can see why; nothing is dropped silently.
        """
        captured = []
        for idea in [item for item in self.registry().get("inbox", []) if not item.get("rejected")]:
            try:
                captured.append(self.capture(name=idea.get("name", ""), purpose=idea.get("purpose", ""), kind=idea.get("kind") or "project"))
                rejected = None
            except IntakeError as error:
                rejected = str(error)
            registry = self.registry()                      # capture() rewrote it
            for item in registry.get("inbox", []):
                if item is not None and item.get("name") == idea.get("name") and item.get("submittedAt") == idea.get("submittedAt"):
                    if rejected:
                        item["rejected"] = rejected
                    else:
                        registry["inbox"].remove(item)
                    break
            write_json(self.path, registry)
        return captured

    def list_projects(self) -> list[dict[str, Any]]:
        self.process_inbox()
        return sorted(self.registry().get("projects", []), key=lambda project: project.get("createdAt", ""), reverse=True)

    def _existing_names(self) -> list[dict[str, str]]:
        index = load_json(self.index_path)
        entries = [{"name": item.get("name", ""), "id": item.get("id", ""), "source": "MasterIndex entity"} for item in index.get("entities", [])]
        entries += [{"name": item.get("repo", ""), "id": item.get("repo", ""), "source": "MasterIndex repository"} for item in index.get("repos", [])]
        entries += [{"name": item.get("name", ""), "id": item.get("id", ""), "source": "project intake"} for item in self.registry().get("projects", [])]
        return entries

    def _collisions(self, name: str, slug: str) -> list[dict[str, str]]:
        requested = {normalized(name), normalized(slug), normalized(f"{slug}-project")}
        matches = []
        for entry in self._existing_names():
            candidate = normalized(entry["name"])
            if candidate and (candidate in requested or candidate == normalized(slug)):
                matches.append(entry)
        return matches

    def capture(self, *, name: str, purpose: str, slug: str | None = None, kind: str = "project") -> dict[str, Any]:
        name = " ".join(str(name).split())
        purpose = str(purpose).strip()
        if not 2 <= len(name) <= 100:
            raise IntakeError("Project name must be 2–100 characters.")
        if not 8 <= len(purpose) <= 2_000:
            raise IntakeError("Purpose must be 8–2,000 characters.")
        if kind not in {"project", "app", "backend", "service", "package", "website"}:
            raise IntakeError("Kind must be project, app, backend, service, package, or website.")
        slug = slugify(slug or name)
        registry = self.registry()
        exact = [project for project in registry.get("projects", []) if project.get("slug") == slug]
        if exact:
            raise IntakeError(f"An intake already uses the slug '{slug}'.")
        collisions = self._collisions(name, slug)
        if collisions:
            sources = ", ".join(f"{item['source']}: {item['name']}" for item in collisions)
            raise IntakeError(f"Name or slug conflicts with {sources}. Choose a distinct name or slug.")
        defaults = registry["defaults"]
        captured_at = now()
        project = {
            "id": f"{slug}-project",
            "name": name,
            "slug": slug,
            "purpose": purpose,
            "kind": kind,
            "state": "captured",
            "createdAt": captured_at,
            "lastModified": captured_at,
            "proposed": {
                "directory": f"~/{slug}",
                "github": {"owner": defaults["githubOwner"], "name": slug, "visibility": defaults["visibility"]},
                "cluster": "Incubator",
                "entityStatus": defaults["entityStatus"]
            },
            "openDecisions": [
                "Choose the initial user/platform and product-line posture.",
                "Confirm the project kind before its first implementation milestone.",
                "Keep the GitHub repository private unless its release plan explicitly changes."
            ],
            "provenance": {"observedAt": captured_at, "source": {"kind": "owner-intake", "authority": "owner-report"}, "confidence": "reported"}
        }
        registry["projects"].append(project)
        registry["generatedAt"] = captured_at
        write_json(self.path, registry)
        return project

    def _project(self, project_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
        registry = self.registry()
        project = next((item for item in registry.get("projects", []) if item.get("id") == project_id), None)
        if not project:
            raise IntakeError(f"Unknown intake id '{project_id}'.")
        return registry, project

    def provisioning_plan(self, project_id: str) -> dict[str, Any]:
        _, project = self._project(project_id)
        return {
            "projectId": project["id"],
            "confirmationRequired": project["name"],
            "creates": [
                f"local Git repository {project['proposed']['directory']}",
                f"private GitHub repository {project['proposed']['github']['owner']}/{project['proposed']['github']['name']}",
                "README.md, AGENTS.md, CLAUDE.md, and .gitignore scaffold",
                "canonical MasterIndex entity, repository record, and weekly intent-review task"
            ],
            "doesNotCreate": ["App Store Connect records", "domains", "deployments", "billing", "public websites"],
            "note": "Provisioning is irreversible enough to require the exact project name. A failure after local or GitHub creation is reported; nothing is silently deleted."
        }

    def _run(self, arguments: list[str], *, cwd: Path | None = None) -> str:
        completed = subprocess.run(arguments, cwd=cwd, text=True, capture_output=True, check=False)
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip()
            raise IntakeError(f"Command failed ({' '.join(arguments[:3])}): {detail or 'no detail returned'}")
        return completed.stdout.strip()

    def _write_scaffold(self, project: dict[str, Any], destination: Path) -> None:
        destination.mkdir(parents=False, exist_ok=False)
        (destination / "README.md").write_text(
            f"# {project['name']}\n\n{project['purpose']}\n\nCreated through MasterIndex Project Intake on {project['createdAt']}.\n",
            encoding="utf-8",
        )
        (destination / "AGENTS.md").write_text(
            "# Project instructions\n\n"
            "This project was created through MasterIndex. Before portfolio-wide planning, read "
            "`~/masterindex/current/index.json`; use its entity ids and record verified cross-project facts there through the normal MasterIndex workflow.\n\n"
            "Keep product decisions and project-specific implementation guidance in this repository. Do not treat an idea-stage record as a release commitment.\n",
            encoding="utf-8",
        )
        # Claude Code loads CLAUDE.md, not AGENTS.md; this keeps one set of instructions for every agent.
        (destination / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
        (destination / ".gitignore").write_text(".DS_Store\n.env\n.env.*\n!.env.example\n", encoding="utf-8")

    def _register_in_masterindex(self, project: dict[str, Any], github_url: str | None) -> None:
        index = load_json(self.index_path)
        if any(entity.get("id") == project["id"] for entity in index.get("entities", [])):
            raise IntakeError(f"MasterIndex already has entity id '{project['id']}'.")
        observed_at = now()
        if not any(cluster.get("name") == "Incubator" for cluster in index.get("clusters", [])):
            index["clusters"].append({
                "name": "Incubator",
                "maturity": "captured ideas and newly scaffolded projects",
                "summary": "Projects enter here through the MasterIndex intake before they have a committed product or release posture.",
                "highlights": [],
                "watchpoints": ["Confirm platform, product line, and scope before advancing an incubating project."]
            })
            if isinstance(index.get("summary", {}).get("clusters"), int):
                index["summary"]["clusters"] += 1
        links = {"github": github_url} if github_url else {}
        index["entities"].append({
            "id": project["id"], "name": project["name"], "kind": project["kind"], "status": "incubating",
            "cluster": "Incubator", "repo": project["proposed"]["directory"], "bundleId": None,
            "description": project["purpose"], "dependencies": [], "links": links,
            "release": "Idea captured and repository scaffolded; no release posture selected.", "lastModified": observed_at[:10],
            "notes": ["Created through MasterIndex Project Intake.", *project["openDecisions"]],
            "provenance": {"observedAt": observed_at, "source": {"kind": "MasterIndex project intake", "authority": "owner-report"}, "confidence": "reported"}
        })
        index["repos"].append({
            "repo": project["proposed"]["directory"], "branch": "main", "last2026Commit": observed_at[:10],
            "kind": f"{project['kind']}/incubator", "role": project["purpose"]
        })
        index["generatedAt"] = observed_at
        write_json(self.index_path, index)

        narrative = self.narrative_path.read_text(encoding="utf-8")
        entry = f"\n## Project Intake — {observed_at[:10]}\n\n- **{project['name']}** (`{project['id']}`) entered the Incubator through the owner intake. Purpose: {project['purpose']} Repository: `{project['proposed']['directory']}`. It is an idea-stage scaffold, not a release commitment.\n"
        self.narrative_path.write_text(entry + narrative, encoding="utf-8")

        tasks = load_json(self.tasks_path)
        tasks.setdefault("entryTasks", {})[project["id"]] = [{
            "taskId": f"{project['id']}-intent-review", "name": f"{project['name']} intent review", "status": "active",
            "cadence": {"kind": "rrule", "value": "FREQ=WEEKLY;INTERVAL=1"},
            "purpose": "Review the project purpose, platform, product line, and next evidence before committing implementation scope.",
            "expectedInputs": ["intake/index.json", project["proposed"]["directory"]],
            "expectedOutputs": ["Updated MasterIndex entity facts or an explicit decision/gap"]
        }]
        tasks["generatedAt"] = observed_at
        write_json(self.tasks_path, tasks)

    def _set_owner_focus(self, project_id: str, focus: str | None, note: str | None) -> None:
        """Record the owner's focus tier and note through the project monitor, the ledger's one writer here."""
        monitor = [sys.executable, str(self.root / "tools" / "project_monitor.py"), "--root", str(self.root), "--no-publish"]
        if focus:
            self._run([*monitor, "--focus", project_id, focus])
        if note:
            self._run([*monitor, "--comment", project_id, note])

    def provision(self, *, project_id: str, confirmation: str, create_github: bool = True,
                  focus: str | None = None, note: str | None = None) -> dict[str, Any]:
        registry, project = self._project(project_id)
        if project.get("state") != "captured":
            raise IntakeError(f"Only a captured project can be provisioned (current state: {project.get('state')}).")
        if confirmation != project["name"]:
            raise IntakeError("Confirmation must exactly match the project name.")
        destination = (self.project_parent / project["slug"]).resolve()
        if destination.parent != self.project_parent or destination.exists():
            raise IntakeError(f"Refusing to provision outside the configured empty project location: {destination}")
        if not shutil.which("git"):
            raise IntakeError("git is required to provision a project.")
        if create_github and not shutil.which("gh"):
            raise IntakeError("GitHub CLI (gh) is required for private remote repository creation.")

        local_created = False
        github_url = None
        try:
            self._write_scaffold(project, destination)
            local_created = True
            self._run(["git", "init", "-b", "main"], cwd=destination)
            self._run(["git", "add", "README.md", "AGENTS.md", "CLAUDE.md", ".gitignore"], cwd=destination)
            self._run(["git", "commit", "-m", "Initial project scaffold"], cwd=destination)
            if create_github:
                github = project["proposed"]["github"]
                github_url = f"https://github.com/{github['owner']}/{github['name']}"
                self._run(["gh", "repo", "create", f"{github['owner']}/{github['name']}", "--private", "--source", str(destination), "--remote", "origin", "--push"], cwd=destination)
            self._register_in_masterindex(project, github_url)
            self._set_owner_focus(project["id"], focus, note)
        except Exception as exc:
            project["state"] = "provisioning-needs-attention"
            project["lastModified"] = now()
            project["provisionError"] = str(exc)
            project["partialProvision"] = {"localDirectory": str(destination) if local_created else None, "githubUrl": github_url}
            registry["generatedAt"] = project["lastModified"]
            write_json(self.path, registry)
            raise IntakeError(f"Provisioning stopped. No automatic cleanup was attempted. {exc}") from exc

        project["state"] = "provisioned"
        project["lastModified"] = now()
        project["provisionedAt"] = project["lastModified"]
        project["provision"] = {"directory": str(destination), "githubUrl": github_url, "masterIndexRegistered": True}
        registry["generatedAt"] = project["lastModified"]
        write_json(self.path, registry)
        return {"project": project, "message": "Project provisioned and registered in MasterIndex. Commit these registry changes after reviewing them."}
