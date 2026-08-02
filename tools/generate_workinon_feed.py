from __future__ import annotations

import json
import math
import sys
from datetime import datetime
from pathlib import Path
from urllib.parse import urlencode


def read_json(path: Path):
    return json.loads(path.read_text())


def parse_date_value(value: str | None) -> float:
    if not value or value == "no commits yet":
        return float("-inf")
    try:
        return datetime.fromisoformat(value).timestamp()
    except ValueError:
        return float("-inf")


def days_since(value: str | None, now_dt: datetime) -> int | None:
    ts = parse_date_value(value)
    if not math.isfinite(ts):
        return None
    return int((now_dt.timestamp() - ts) // 86400)


def encode_workinon_url(key: str, text: str) -> str:
    return f"workinon://post?{urlencode({'key': key, 'text': text})}"


def board_key(kind: str, suffix: str) -> str:
    return f"masterindex.{kind}.{suffix}"


def deep_link(entity_id: str) -> str:
    return f"site/index.html#{entity_id}"


def build_attention_items(index_data: dict) -> list[dict]:
    items = []
    for entity in index_data["entities"]:
        has_website = bool(entity.get("links", {}).get("website"))
        has_app_store = bool(entity.get("links", {}).get("appStore"))
        is_app = entity["kind"] == "app"

        if not has_website and not has_app_store:
            items.append(
                {
                    "id": f"attention-{entity['id']}-no-public-links",
                    "type": "attention",
                    "entityId": entity["id"],
                    "title": f"{entity['name']} missing public links",
                    "body": "No verified website or public App Store page is recorded yet.",
                    "priority": "medium" if is_app else "low",
                    "tags": ["links", "public", entity["cluster"].lower()],
                    "deepLink": deep_link(entity["id"]),
                    "statusKey": board_key("attention", f"{entity['id']}.no-public-links"),
                }
            )
            continue

        if is_app and not has_app_store:
            body = (
                "A website is recorded, but no verified public App Store page is in the index yet."
                if has_website
                else "No verified public App Store page is in the index yet."
            )
            items.append(
                {
                    "id": f"attention-{entity['id']}-missing-appstore-link",
                    "type": "attention",
                    "entityId": entity["id"],
                    "title": f"{entity['name']} missing public App Store page",
                    "body": body,
                    "priority": "medium",
                    "tags": ["links", "app-store", entity["cluster"].lower()],
                    "deepLink": deep_link(entity["id"]),
                    "statusKey": board_key("attention", f"{entity['id']}.missing-appstore"),
                }
            )
    return items


def cadence_summary(cadence: dict | None) -> str:
    value = (cadence or {}).get("value", "")
    if "INTERVAL=6" in value:
        return "Task is due in this six-hour cycle."
    if "FREQ=DAILY" in value:
        return "Task is due in the daily cycle."
    if "FREQ=WEEKLY" in value:
        return "Task is part of the weekly cycle."
    return f"Task cadence: {value}." if value else "Task is due soon."


def build_due_task_items(index_data: dict, task_data: dict) -> list[dict]:
    entities_by_id = {entity["id"]: entity for entity in index_data["entities"]}
    items = []

    for entity_id, tasks in task_data.get("entryTasks", {}).items():
        entity = entities_by_id.get(entity_id)
        if not entity:
            continue
        for task in tasks:
            if task.get("status") != "active":
                continue
            cadence_value = task.get("cadence", {}).get("value", "")
            items.append(
                {
                    "id": f"due-{task['taskId']}",
                    "type": "due-task",
                    "entityId": entity_id,
                    "taskId": task["taskId"],
                    "title": f"{task['name']} due",
                    "body": cadence_summary(task.get("cadence")),
                    "priority": "high" if "INTERVAL=6" in cadence_value else "medium",
                    "tags": ["task", entity["kind"], entity["cluster"].lower()],
                    "deepLink": deep_link(entity_id),
                    "statusKey": board_key("due", task["taskId"]),
                }
            )
    return items


def build_recent_change_items(index_data: dict, now_dt: datetime) -> list[dict]:
    items = []
    for entity in index_data["entities"]:
        age_days = days_since(entity.get("lastModified"), now_dt)
        if age_days is None or age_days > 7:
            continue
        items.append(
            {
                "id": f"recent-{entity['id']}",
                "type": "recent-change",
                "entityId": entity["id"],
                "title": f"{entity['name']} changed recently",
                "body": f"Last modified {entity['lastModified']}.",
                "priority": "medium" if age_days <= 2 else "low",
                "tags": ["recent", entity["kind"], entity["cluster"].lower()],
                "deepLink": deep_link(entity["id"]),
                "statusKey": board_key("recent", entity["id"]),
            }
        )
    return items


def build_summary_items(index_data: dict, feed_items: list[dict]) -> list[dict]:
    missing_links_count = sum(1 for item in feed_items if item["type"] == "attention")
    due_task_count = sum(1 for item in feed_items if item["type"] == "due-task")
    recent_count = sum(1 for item in feed_items if item["type"] == "recent-change")
    return [
        {
            "id": "summary-public-link-gaps",
            "type": "summary",
            "title": "Public link gaps",
            "body": f"{missing_links_count} entries still need verified public links or App Store pages.",
            "priority": "low",
            "tags": ["summary", "links"],
            "statusKey": board_key("summary", "public-link-gaps"),
        },
        {
            "id": "summary-due-tasks",
            "type": "summary",
            "title": "Tasks due soon",
            "body": f"{due_task_count} recurring entry tasks are currently in the operational queue.",
            "priority": "low",
            "tags": ["summary", "tasks"],
            "statusKey": board_key("summary", "due-tasks"),
        },
        {
            "id": "summary-recent-changes",
            "type": "summary",
            "title": "Recent changes",
            "body": f"{recent_count} entries were modified in the last 7 days.",
            "priority": "low",
            "tags": ["summary", "recent"],
            "statusKey": board_key("summary", "recent-changes"),
        },
        {
            "id": "summary-asc-gaps",
            "type": "summary",
            "title": "ASC coverage gaps",
            "body": f"{index_data['summary']['unmatchedAscApps']} App Store Connect apps still do not map cleanly to an active local repository.",
            "priority": "low",
            "tags": ["summary", "asc"],
            "statusKey": board_key("summary", "asc-gaps"),
        },
    ]


def priority_score(priority: str) -> int:
    return {"high": 0, "medium": 1}.get(priority, 2)


def type_score(item_type: str) -> int:
    return {"attention": 0, "due-task": 1, "recent-change": 2}.get(item_type, 3)


def sort_items(items: list[dict]) -> list[dict]:
    return sorted(
        items,
        key=lambda item: (priority_score(item["priority"]), type_score(item["type"]), item["title"]),
    )


def materialize_shortcut_manifest(items: list[dict]) -> list[dict]:
    manifest = []
    for item in items:
      text = f"{item['title']} - {item['body']}"
      manifest.append(
          {
              "id": item["id"],
              "title": item["title"],
              "statusKey": item["statusKey"],
              "url": encode_workinon_url(item["statusKey"], text),
              "entityId": item.get("entityId"),
              "taskId": item.get("taskId"),
              "type": item["type"],
              "priority": item["priority"],
          }
      )
    return manifest


def build_readme(feed: dict) -> str:
    items = feed["items"]
    return f"""# workin On Feed

Generated for MasterIndex on {feed["generatedAt"]}.

## Purpose

This folder contains the first working operational feed for the `workin On` app.

## Files

- `board-feed.json` — canonical generated board items
- `shortcut-manifest.json` — ready-to-post `workinon://post` URLs for keyed status items

## Feed summary

- Total cards: {len(items)}
- Attention cards: {sum(1 for item in items if item["type"] == "attention")}
- Due task cards: {sum(1 for item in items if item["type"] == "due-task")}
- Recent change cards: {sum(1 for item in items if item["type"] == "recent-change")}
- Summary cards: {sum(1 for item in items if item["type"] == "summary")}

## Notes

- Keys are namespaced as `masterindex.*` for safe upserts in workin On.
- The web page remains the deep-dive surface.
- workin On should surface these as operational status items, not as the full browser.
"""


def main():
    hub_root = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    current_index_path = hub_root / "current" / "index.json"
    tasks_path = hub_root / "tasks" / "index.json"
    output_dir = hub_root / "workinon"
    board_feed_path = output_dir / "board-feed.json"
    shortcut_manifest_path = output_dir / "shortcut-manifest.json"
    summary_path = output_dir / "README.md"

    index_data = read_json(current_index_path)
    task_data = read_json(tasks_path)
    now_dt = datetime.now().astimezone()

    attention = build_attention_items(index_data)
    due_soon = build_due_task_items(index_data, task_data)
    recent = build_recent_change_items(index_data, now_dt)
    summaries = build_summary_items(index_data, [*attention, *due_soon, *recent])
    items = sort_items([*attention, *due_soon, *recent, *summaries])

    board_feed = {
        "generatedAt": now_dt.isoformat(timespec="seconds"),
        "sourceFiles": {
            "inventory": "current/index.json",
            "tasks": "tasks/index.json",
        },
        "intendedSurface": "workin On",
        "defaultLanes": [
            "Needs Attention",
            "Due Soon",
            "Recently Changed",
            "Summaries",
        ],
        "itemCount": len(items),
        "items": items,
    }

    shortcut_manifest = {
        "generatedAt": board_feed["generatedAt"],
        "namespace": "masterindex",
        "items": materialize_shortcut_manifest(items),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    board_feed_path.write_text(json.dumps(board_feed, indent=2) + "\n")
    shortcut_manifest_path.write_text(json.dumps(shortcut_manifest, indent=2) + "\n")
    summary_path.write_text(build_readme(board_feed))
    print(f"Generated {board_feed['itemCount']} workin On board items in {output_dir}")


if __name__ == "__main__":
    main()
