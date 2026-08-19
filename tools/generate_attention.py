#!/usr/bin/env python3
"""Derive the actionable attention board for MasterIndex.

This is the single definition of "something needs a decision or an action".
Both consumer surfaces read the artifact it writes (`current/attention.json`):

- `site/` renders it as the attention strip on the web browser
- `tools/generate_workinon_feed.py` turns it into workin On board cards

Design rules, in priority order:

1. A card exists only if there is an action or decision the owner can take.
2. A card must be clearable. Anything recomputed from static config forever
   is a log entry, not a board item.
3. Conditions that are correct by design are suppressed, and the suppression
   is reported so an empty board is trustworthy rather than mysterious.

The generator is deterministic and reads only committed files, so it can run
in CI as safely as it runs on a laptop.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCHEMA_VERSION = "1.0"
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text())


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")


def parse_moment(value: str | None) -> datetime | None:
    """Parse an ISO date or datetime into an aware datetime, or None."""
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed


def deep_link(entity_id: str | None) -> str:
    return f"site/index.html?entity={entity_id}" if entity_id else "site/index.html"


def card(
    *,
    item_id: str,
    kind: str,
    title: str,
    body: str,
    action: str,
    evidence: str,
    priority: str,
    lane: str,
    entity_id: str | None = None,
    entity_ids: list[str] | None = None,
    sort_date: str | None = None,
    tags: list[str] | None = None,
) -> dict:
    related = entity_ids if entity_ids is not None else ([entity_id] if entity_id else [])
    entity_id = entity_id or (related[0] if related else None)
    return {
        "id": item_id,
        "kind": kind,
        "entityId": entity_id,
        "entityIds": related,
        "title": title,
        "body": body,
        "action": action,
        "evidence": evidence,
        "priority": priority,
        "lane": lane,
        "sortDate": sort_date,
        "tags": tags or [],
        "deepLink": deep_link(entity_id),
        "statusKey": f"masterindex.{kind}.{item_id}",
    }


# --------------------------------------------------------------------------
# Sources of actionable work
# --------------------------------------------------------------------------


def open_gap_items(index: dict, policy: dict) -> tuple[list[dict], list[dict]]:
    """Gaps explicitly dispositioned open. Resolved gaps are history."""
    rules = policy.get("gaps", {})
    actionable = set(rules.get("actionableDispositions", ["open"]))
    items: list[dict] = []
    suppressed: list[dict] = []
    undispositioned: list[str] = []

    for gap in index.get("gaps", []):
        disposition = gap.get("disposition")
        gap_id = gap.get("id") or gap.get("kind")
        if disposition is None:
            undispositioned.append(gap_id)
            continue
        if disposition not in actionable:
            suppressed.append(
                {
                    "rule": f"gap-disposition:{disposition}",
                    "subject": gap_id,
                    "reason": "Recorded as history or as an accepted decision, not as pending work.",
                }
            )
            continue

        summary = gap["summary"]
        headline = gap.get("title") or summary.split(". ")[0].rstrip(".")
        items.append(
            card(
                item_id=f"gap-{gap_id}",
                kind="open-gap",
                title=headline[:110],
                body=summary,
                action=gap.get("nextAction")
                or "Resolve it, then set this gap's disposition to 'resolved' in current/index.json.",
                evidence=f"current/index.json gaps[] id={gap_id} kind={gap['kind']} observedAt={gap['observedAt']}",
                priority=gap.get("priority", "medium"),
                lane="Needs Attention",
                entity_ids=gap.get("entityIds") or [],
                sort_date=gap.get("observedAt"),
                tags=["gap", gap["kind"]],
            )
        )

    if undispositioned and rules.get("triageUndispositioned", True):
        items.append(
            card(
                item_id="gaps-need-disposition",
                kind="triage",
                title=f"{len(undispositioned)} gaps have no disposition recorded",
                body="These gaps cannot be classified as open work, resolved history, or accepted decisions, so they are excluded from the board: "
                + ", ".join(sorted(undispositioned)),
                action="Add a \"disposition\" of open, resolved, or accepted to each gap in current/index.json.",
                evidence="current/index.json gaps[] entries missing the disposition field",
                priority="medium",
                lane="Needs Attention",
                tags=["gap", "triage"],
            )
        )

    return items, suppressed


def link_gap_items(index: dict, policy: dict) -> tuple[list[dict], list[dict]]:
    """Missing public links, but only where a link is genuinely expected."""
    rules = policy.get("publicLinks", {})
    suppressed_statuses = set(rules.get("suppressedStatuses", []))
    suppressed_distributions = set(rules.get("suppressedDistributions", []))
    suppressed_ids = set(rules.get("suppressedEntityIds", []))
    app_store_statuses = set(rules.get("appStorePageExpectedForStatuses", []))
    website_statuses = set(rules.get("websiteExpectedForStatuses", []))
    website_kinds = set(rules.get("websiteExpectedForKinds", []))

    items: list[dict] = []
    suppressed: list[dict] = []

    for entity in index["entities"]:
        entity_id = entity["id"]
        status = entity.get("status")
        distribution = entity.get("distribution")
        links = entity.get("links") or {}

        if entity_id in suppressed_ids:
            suppressed.append({"rule": "entity-exempt", "subject": entity_id, "reason": "Explicitly exempted in current/attention-policy.json."})
            continue
        if distribution in suppressed_distributions:
            suppressed.append({"rule": f"distribution:{distribution}", "subject": entity_id, "reason": "Not intended for public distribution, so a public link is not expected."})
            continue
        if status in suppressed_statuses:
            suppressed.append({"rule": f"status:{status}", "subject": entity_id, "reason": "Status means no public presence is expected."})
            continue

        if status in app_store_statuses and entity["kind"] == "app" and not links.get("appStore"):
            items.append(
                card(
                    item_id=f"link-{entity_id}-appstore",
                    kind="link-gap",
                    title=f"{entity['name']} has shipped but has no App Store link recorded",
                    body=f"Status is '{status}', which means the app is publicly available, but no verified App Store page is stored in its links object.",
                    action="Verify the public App Store URL and store it under this entity's links.appStore.",
                    evidence=f"current/index.json entities[] id={entity_id} status={status} links.appStore=null",
                    priority="medium",
                    lane="Needs Attention",
                    entity_id=entity_id,
                    tags=["links", "app-store"],
                )
            )

        if status in website_statuses and entity["kind"] in website_kinds and not links.get("website"):
            items.append(
                card(
                    item_id=f"link-{entity_id}-website",
                    kind="link-gap",
                    title=f"{entity['name']} has no public website recorded",
                    body=f"Status is '{status}' and kind is '{entity['kind']}', so a public landing or marketing page is expected, but none is stored.",
                    action="Record the public URL under this entity's links.website, or suppress it in current/attention-policy.json if it is deliberately unlisted.",
                    evidence=f"current/index.json entities[] id={entity_id} status={status} links.website=null",
                    priority="low",
                    lane="Needs Attention",
                    entity_id=entity_id,
                    tags=["links", "website"],
                )
            )

    return items, suppressed


def task_items(index: dict, tasks: dict, state: dict, policy: dict, now: datetime) -> list[dict]:
    """Overdue tasks, computed from recorded runs rather than from cadence alone."""
    rules = policy.get("tasks", {})
    grace = timedelta(hours=rules.get("gracePeriodHours", 6))
    runs = state.get("taskRuns", {}) or {}
    entities_by_id = {entity["id"]: entity for entity in index["entities"]}

    active: list[tuple[str, dict]] = []
    for entity_id, entity_tasks in (tasks.get("entryTasks") or {}).items():
        for task in entity_tasks:
            if task.get("status") == "active":
                active.append((entity_id, task))
    for task in tasks.get("globalTasks") or []:
        if task.get("status") == "active":
            active.append((None, task))

    items: list[dict] = []
    uninstrumented: list[str] = []

    for entity_id, task in active:
        task_id = task["taskId"]
        last_run = parse_moment(runs.get(task_id))
        if last_run is None:
            uninstrumented.append(task_id)
            continue
        interval = cadence_interval(task.get("cadence"))
        if interval is None:
            continue
        due_at = last_run + interval
        if now < due_at + grace:
            continue
        overdue_for = now - due_at
        entity = entities_by_id.get(entity_id) if entity_id else None
        items.append(
            card(
                item_id=f"task-{task_id}",
                kind="overdue-task",
                title=f"{task['name']} is overdue",
                body=f"Last recorded run was {last_run.date().isoformat()}; it was due {due_at.date().isoformat()}, {overdue_for.days} day(s) ago.",
                action=task.get("purpose") or "Run the task and record the run in current/attention-state.json taskRuns.",
                evidence=f"tasks/index.json taskId={task_id}; last run from current/attention-state.json",
                priority="high" if overdue_for > interval else "medium",
                lane="Due Soon",
                entity_id=entity_id,
                sort_date=due_at.date().isoformat(),
                tags=["task", "overdue"] + ([entity["kind"]] if entity else []),
            )
        )

    if uninstrumented and rules.get("emitUninstrumentedDigest", True):
        items.append(
            card(
                item_id="tasks-not-instrumented",
                kind="triage",
                title=f"{len(uninstrumented)} active tasks have no recorded run history",
                body="Nothing records when these tasks last ran, so none of them can be evaluated for being overdue. Until runs are recorded, task cadence produces no signal at all.",
                action="Record a completion timestamp per taskId under taskRuns in current/attention-state.json when a task runs; overdue cards then appear on their own.",
                evidence="tasks/index.json active tasks absent from current/attention-state.json taskRuns",
                priority="medium",
                lane="Due Soon",
                tags=["task", "instrumentation"],
            )
        )

    return items


def cadence_interval(cadence: dict | None) -> timedelta | None:
    value = (cadence or {}).get("value", "") or ""
    try:
        interval = int(value.split("INTERVAL=")[1].split(";")[0]) if "INTERVAL=" in value else 1
    except (IndexError, ValueError):
        interval = 1
    if "FREQ=HOURLY" in value:
        return timedelta(hours=interval)
    if "FREQ=DAILY" in value:
        return timedelta(days=interval)
    if "FREQ=WEEKLY" in value:
        return timedelta(weeks=interval)
    if "FREQ=MONTHLY" in value:
        return timedelta(days=30 * interval)
    return None


def change_items(index: dict, state: dict, policy: dict, now: datetime) -> list[dict]:
    """Changes since the operator last reviewed - a diff, not a log."""
    rules = policy.get("recentChange", {})
    watermark = parse_moment(state.get("lastReviewedAt"))
    max_cards = rules.get("maxIndividualCards", 12)

    if watermark is None:
        window = timedelta(days=rules.get("fallbackWindowDays", 7))
        changed = [e for e in index["entities"] if (m := parse_moment(e.get("lastModified"))) and now - m <= window]
        if not changed:
            return []
        return [
            card(
                item_id="changes-no-watermark",
                kind="triage",
                title=f"{len(changed)} entries changed recently, but no review watermark is set",
                body="Without a watermark every refresh re-reports the same changes, so they are collapsed into this single card instead of one card per entry.",
                action="Run: python3 tools/generate_attention.py --mark-reviewed. After that, only entries changed since your last review appear here.",
                evidence=f"current/attention-state.json lastReviewedAt=null; {len(changed)} entities modified within {rules.get('fallbackWindowDays', 7)} days",
                priority="low",
                lane="Recent Activity",
                tags=["recent", "watermark"],
            )
        ]

    changed = sorted(
        [e for e in index["entities"] if (m := parse_moment(e.get("lastModified"))) and m > watermark],
        key=lambda e: e.get("lastModified") or "",
        reverse=True,
    )
    if not changed:
        return []

    items = [
        card(
            item_id=f"changed-{entity['id']}",
            kind="changed-since-review",
            title=f"{entity['name']} changed since your last review",
            body=f"{entity['description'][:200]}" if entity.get("description") else f"Last modified {entity.get('lastModified')}.",
            action="Review the change, then re-run with --mark-reviewed to clear it.",
            evidence=f"current/index.json entities[] id={entity['id']} lastModified={entity.get('lastModified')} > lastReviewedAt={state['lastReviewedAt']}",
            priority="low",
            lane="Recent Activity",
            entity_id=entity["id"],
            sort_date=entity.get("lastModified"),
            tags=["recent", entity["kind"]],
        )
        for entity in changed[:max_cards]
    ]

    if len(changed) > max_cards:
        items.append(
            card(
                item_id="changed-overflow",
                kind="changed-since-review",
                title=f"{len(changed) - max_cards} further entries changed since your last review",
                body="Collapsed to keep the board readable. Open the web browser to see the full list sorted by most recently modified.",
                action="Review them in the browser, then re-run with --mark-reviewed.",
                evidence=f"{len(changed)} entities changed; {max_cards} shown individually",
                priority="low",
                lane="Recent Activity",
                tags=["recent", "overflow"],
            )
        )

    return items


# --------------------------------------------------------------------------


def apply_dismissals(items: list[dict], state: dict, now: datetime) -> tuple[list[dict], list[dict]]:
    dismissed = state.get("dismissed", {}) or {}
    kept: list[dict] = []
    suppressed: list[dict] = []
    for item in items:
        record = dismissed.get(item["id"])
        if record is None:
            kept.append(item)
            continue
        until = parse_moment(record.get("until"))
        if until is not None and now > until:
            kept.append(item)
            continue
        suppressed.append({"rule": "dismissed", "subject": item["id"], "reason": record.get("reason", "Dismissed by the operator.")})
    return kept, suppressed


def sort_items(items: list[dict]) -> list[dict]:
    return sorted(
        items,
        key=lambda item: (
            PRIORITY_ORDER.get(item["priority"], 3),
            {"Needs Attention": 0, "Due Soon": 1, "Recent Activity": 2}.get(item["lane"], 3),
            item["sortDate"] is None,
            str(item["sortDate"] or ""),
            item["title"],
        ),
    )


def build(root: Path, mark_reviewed: bool) -> dict:
    index = read_json(root / "current" / "index.json")
    tasks = read_json(root / "tasks" / "index.json")
    policy = read_json(root / "current" / "attention-policy.json")
    state_path = root / "current" / "attention-state.json"
    state = read_json(state_path)
    now = datetime.now().astimezone()

    if mark_reviewed:
        state["lastReviewedAt"] = now.isoformat(timespec="seconds")
        write_json(state_path, state)

    gap_items, gap_suppressed = open_gap_items(index, policy)
    link_items, link_suppressed = link_gap_items(index, policy)
    items = [*gap_items, *link_items, *task_items(index, tasks, state, policy, now), *change_items(index, state, policy, now)]
    items, dismissed_suppressed = apply_dismissals(items, state, now)
    items = sort_items(items)

    suppressed = [*gap_suppressed, *link_suppressed, *dismissed_suppressed]
    counts = {level: sum(1 for item in items if item["priority"] == level) for level in ("high", "medium", "low")}

    return {
        "generatedAt": now.isoformat(timespec="seconds"),
        "schemaVersion": SCHEMA_VERSION,
        "description": "Derived, actionable attention board. Generated by tools/generate_attention.py; do not hand-edit. Authoritative inputs are current/index.json, tasks/index.json, current/attention-policy.json, and current/attention-state.json.",
        "sourceFiles": {
            "inventory": "current/index.json",
            "tasks": "tasks/index.json",
            "policy": "current/attention-policy.json",
            "state": "current/attention-state.json",
        },
        "watermark": {"lastReviewedAt": state.get("lastReviewedAt")},
        "counts": {**counts, "total": len(items), "suppressed": len(suppressed)},
        "lanes": ["Needs Attention", "Due Soon", "Recent Activity"],
        "items": items,
        "suppressed": sorted(suppressed, key=lambda entry: (entry["rule"], entry["subject"])),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root", nargs="?", default=None, help="MasterIndex checkout root (defaults to this script's repository).")
    parser.add_argument("--mark-reviewed", action="store_true", help="Stamp the review watermark to now, clearing changed-since-review cards.")
    parser.add_argument("--out", default=None, help="Write the board somewhere other than current/attention.json.")
    args = parser.parse_args()

    root = Path(args.root).resolve() if args.root else Path(__file__).resolve().parents[1]
    board = build(root, args.mark_reviewed)
    out_path = Path(args.out).resolve() if args.out else root / "current" / "attention.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    write_json(out_path, board)

    counts = board["counts"]
    print(f"Wrote {out_path} - {counts['total']} actionable items ({counts['high']} high, {counts['medium']} medium, {counts['low']} low), {counts['suppressed']} suppressed")


if __name__ == "__main__":
    main()
