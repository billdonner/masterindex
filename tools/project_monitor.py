#!/usr/bin/env python3
"""Terminal monitor for MasterIndex entities with a separate owner ledger of comments and focus."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import agent_sessions

ROOT = Path(__file__).resolve().parents[1]
HIDDEN_BY_DEFAULT = {"retired", "legacy", "legacy-reference", "reference-only", "stopped", "concept-only"}
# Owner's attention, separate from recorded status. Value is the sort rank; unset sorts after "now".
FOCUS_RANK = {"now": 0, "": 1, "maint": 2, "parked": 3}
NOW_LIMIT = 6


def now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def comments_path(root: Path) -> Path:
    return root / "current" / "project-comments.json"


def load_comments(root: Path) -> dict[str, Any]:
    path = comments_path(root)
    if not path.exists():
        return {"generatedAt": now(), "schemaVersion": "1.0", "comments": {}}
    return read_json(path)


def comment_text(comment_data: dict[str, Any], entity_id: str) -> str:
    entry = comment_data.get("comments", {}).get(entity_id, {})
    return entry.get("text", "") if isinstance(entry, dict) else ""


def focus_of(comment_data: dict[str, Any], entity_id: str) -> str:
    entry = comment_data.get("comments", {}).get(entity_id, {})
    return entry.get("focus", "") if isinstance(entry, dict) else ""


def update_entry(root: Path, entity_id: str, field: str, value: str) -> None:
    """Set or clear one owner field; an entry with neither comment nor focus is removed."""
    data = load_comments(root)
    comments = data.setdefault("comments", {})
    entry = dict(comments.get(entity_id) or {})
    if value:
        entry[field] = value
    else:
        entry.pop(field, None)
    if entry.get("text") or entry.get("focus") or entry.get("pin"):
        comments[entity_id] = {**entry, "updatedAt": now()}
    else:
        comments.pop(entity_id, None)
    data["generatedAt"] = now()
    write_json(comments_path(root), data)


def set_comment(root: Path, entity_id: str, text: str) -> None:
    update_entry(root, entity_id, "text", " ".join(text.split()))


def set_focus(root: Path, entity_id: str, focus: str) -> None:
    focus = "" if focus in {"none", "-"} else focus
    if focus not in FOCUS_RANK:
        raise ValueError(f"focus must be one of: now, maint, parked, none (got {focus!r})")
    update_entry(root, entity_id, "focus", focus)


def is_pinned(comment_data: dict[str, Any], entity_id: str) -> bool:
    entry = comment_data.get("comments", {}).get(entity_id, {})
    return bool(entry.get("pin")) if isinstance(entry, dict) else False


def toggle_pin(root: Path, entity_id: str) -> bool:
    """Pin a project to the top of its focus tier, or unpin it. Returns the new state."""
    pinned = not is_pinned(load_comments(root), entity_id)
    update_entry(root, entity_id, "pin", "1" if pinned else "")
    return pinned


def sessions_by_repo(sessions: list[dict[str, Any]]) -> dict[str, str]:
    """Map each open agent session's directory to the agents running there, e.g. 'claude+codex'."""
    agents: dict[str, set[str]] = {}
    for session in sessions:
        agents.setdefault(session["cwd"].lower(), set()).add(session["agent"])
    return {cwd: "+".join(sorted(names)) for cwd, names in agents.items()}


def open_session(recorded_repo: Any, open_sessions: dict[str, str]) -> str:
    if not isinstance(recorded_repo, str) or not recorded_repo.startswith("~/"):
        return ""
    return open_sessions.get(str(Path.home() / recorded_repo[2:]).lower(), "")


def local_git_state(recorded_repo: Any) -> str:
    if not isinstance(recorded_repo, str) or not recorded_repo.startswith("~/"):
        return "—"
    path = Path.home() / recorded_repo[2:]
    if not path.exists():
        return "missing"
    try:
        output = subprocess.run(
            ["git", "status", "--porcelain", "--branch"], cwd=path, text=True,
            capture_output=True, timeout=5, check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return "unreadable"
    if output.returncode:
        return "not-git"
    lines = output.stdout.splitlines()
    branch = lines[0].removeprefix("## ").split("...")[0] if lines else "detached"
    return f"{branch} {'dirty' if len(lines) > 1 else 'clean'}"


def truncate(value: Any, width: int) -> str:
    text = str(value or "—")
    return text if len(text) <= width else text[: max(width - 1, 0)] + "…"


def handoff_matches(entity: dict[str, Any], targets: set[str]) -> bool:
    values = [re.sub(r"[^a-z0-9]+", "", str(entity.get(key, "")).lower()) for key in ("id", "name")]
    for target in targets:
        candidate = re.sub(r"[^a-z0-9]+", "", str(target).lower())
        if candidate == "allentities" or any(candidate and (candidate == value or candidate in value or value in candidate) for value in values if value):
            return True
    return False


def build_rows(root: Path, *, include_all: bool, inspect_local: bool) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    index = read_json(root / "current" / "index.json")
    tasks = read_json(root / "tasks" / "index.json")
    handoffs = read_json(root / "current" / "handoffs" / "index.json")
    comment_data = load_comments(root)
    open_sessions = sessions_by_repo(agent_sessions.live_sessions()) if inspect_local else {}
    active_handoff_targets = {
        target for directive in handoffs.get("directives", []) if directive.get("status") == "active"
        for target in directive.get("targets", [])
    }
    rows = []
    for entity in index.get("entities", []):
        if not include_all and entity.get("status") in HIDDEN_BY_DEFAULT:
            continue
        entity_id = entity["id"]
        tasks_count = len([task for task in tasks.get("entryTasks", {}).get(entity_id, []) if task.get("status") == "active"])
        handoff = "H" if handoff_matches(entity, active_handoff_targets) else ""
        rows.append({
            "id": entity_id, "name": entity.get("name"), "kind": entity.get("kind"), "status": entity.get("status"),
            "modified": entity.get("lastModified"), "local": local_git_state(entity.get("repo")) if inspect_local else "not checked",
            "work": f"{tasks_count} task{'s' if tasks_count != 1 else ''}{' ' + handoff if handoff else ''}",
            "comment": comment_text(comment_data, entity_id), "focus": focus_of(comment_data, entity_id),
            "pin": is_pinned(comment_data, entity_id),
            "session": open_session(entity.get("repo"), open_sessions),
        })
    rows.sort(key=lambda row: (row.get("modified") or "", row["name"] or ""), reverse=True)
    # Stable sorts: by focus tier, pinned projects first within a tier, then newest first.
    rows.sort(key=lambda row: (FOCUS_RANK[row["focus"]], not row["pin"]))
    return rows, {"indexGeneratedAt": index.get("generatedAt"), "commentsUpdatedAt": comment_data.get("generatedAt")}


# ANSI styles. Colour is used only on a terminal, and never when NO_COLOR is set.
# Fixed 256-colour codes rather than the terminal's 16 theme colours: many themes
# (Ghostty's default included) render "green" as a muted olive.
STYLE = {"bold": "1", "dim": "2", "red": "38;5;196", "green": "38;5;46", "yellow": "38;5;220", "blue": "38;5;39",
         "cyan": "38;5;51", "bold green": "1;38;5;46"}
FOCUS_STYLE = {"now": "bold green", "maint": "blue", "parked": "dim", "": "yellow"}


def use_color() -> bool:
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


def paint(text: str, style: str, enabled: bool) -> str:
    return f"\033[{STYLE[style]}m{text}\033[0m" if enabled and style else text


def local_style(local: str) -> str:
    if local in {"missing", "unreadable", "not-git"}:
        return "red"
    return "yellow" if local.endswith(" dirty") else ""


def render(rows: list[dict[str, Any]], metadata: dict[str, Any], *, clear: bool = False) -> None:
    if clear:
        print("\033[2J\033[H", end="")
    color = use_color()
    width = shutil.get_terminal_size(fallback=(150, 40)).columns
    name_width, status_width, local_width, work_width = 25, 23, 24, 11
    fixed = name_width + status_width + local_width + work_width + 45
    comment_width = max(18, width - fixed)
    print(paint(f"MasterIndex Project Monitor  ·  {len(rows)} shown  ·  recorded inventory {metadata['indexGeneratedAt']}  ·  refreshed {now()}", "bold", color))
    in_focus = sum(row["focus"] == "now" for row in rows)
    over = f" — over your limit of {NOW_LIMIT}, park something" if in_focus > NOW_LIMIT else ""
    print(paint(f"Focus now: {in_focus}{over}", "red" if over else "bold green", color)
          + "  ·  Agent = open terminal sessions  ·  Local = read-only Git status  ·  focus and comments are yours, not verified facts.")
    print(paint(f"{'#':>2}  {'Focus':<6}  {'Agent':<12}  {'Project':<{name_width}}  {'Status':<{status_width}}  {'Local':<{local_width}}  {'Work':<{work_width}}  {'Updated':<10}  Comment", "bold", color))
    print("─" * min(width, fixed + comment_width))
    for number, row in enumerate(rows, start=1):
        status = f"{row['kind']} · {row['status']}"
        focus_style = FOCUS_STYLE[row["focus"]]
        parked = row["focus"] == "parked"
        # Each cell is padded first and painted second, so colour never shifts a column.
        cells = [
            (f"{number:>2}", "dim" if parked else ""),
            (f"{(row['focus'] or '·') + ('*' if row['pin'] else ''):<6}", focus_style),
            (f"{truncate(row['session'], 12):<12}", "dim" if parked else ("cyan" if row["session"] else "")),
            (f"{truncate(row['name'], name_width):<{name_width}}", "bold green" if row["focus"] == "now" else focus_style if parked else ""),
            (f"{truncate(status, status_width):<{status_width}}", "dim" if parked else ""),
            (f"{truncate(row['local'], local_width):<{local_width}}", local_style(row["local"]) or ("dim" if parked else "")),
            (f"{truncate(row['work'], work_width):<{work_width}}", "dim" if parked or row["work"].startswith("0 ") else ""),
            (f"{truncate(row['modified'], 10):<10}", "dim"),
            (truncate(row["comment"], comment_width), "dim" if parked or not row["comment"] else ""),
        ]
        print("  ".join(paint(text, style, color) for text, style in cells))


def resolve_row(rows: list[dict[str, Any]], reference: str) -> dict[str, Any] | None:
    if reference.isdigit() and 1 <= int(reference) <= len(rows):
        return rows[int(reference) - 1]
    return next((row for row in rows if row["id"] == reference), None)


def interactive(root: Path, include_all: bool, inspect_local: bool) -> None:
    while True:
        rows, metadata = build_rows(root, include_all=include_all, inspect_local=inspect_local)
        render(rows, metadata, clear=True)
        print("\nCommands: <number> <comment> | f <number|id> now|maint|parked|none | p <number|id> pin to top | c <number|id> <comment> | e <number|id> | x <number|id> | r refresh | a all/important | q quit")
        try:
            command = input("monitor> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if command in {"q", "quit", "exit"}:
            return
        if command in {"r", "refresh", ""}:
            continue
        if command in {"a", "all"}:
            include_all = not include_all
            continue
        if command.startswith("e "):
            row = resolve_row(rows, command[2:].strip())
            if not row:
                print("Unknown project; press Return to continue."); input(); continue
            replacement = input(f"Comment for {row['name']} (blank clears): ")
            set_comment(root, row["id"], replacement)
            continue
        parts = command.split(maxsplit=2)
        if parts and parts[0] == "p" and len(parts) == 2:
            row = resolve_row(rows, parts[1])
            if row:
                toggle_pin(root, row["id"])
            else:
                print("Unknown project; press Return to continue."); input()
            continue
        if parts and parts[0] == "f" and len(parts) == 3:
            row = resolve_row(rows, parts[1])
            try:
                if not row:
                    raise ValueError("Unknown project")
                set_focus(root, row["id"], parts[2].lower())
            except ValueError as error:
                print(f"{error}; press Return to continue."); input()
            continue
        if parts and parts[0] == "x" and len(parts) == 2:
            row = resolve_row(rows, parts[1])
            if row:
                set_comment(root, row["id"], "")
            else:
                print("Unknown project; press Return to continue."); input()
            continue
        if parts and parts[0] == "c" and len(parts) == 3:
            reference, text = parts[1], parts[2]
        elif len(parts) >= 2:
            reference, text = parts[0], command[len(parts[0]):].strip()
        else:
            print("Use a number plus a comment; press Return to continue."); input(); continue
        row = resolve_row(rows, reference)
        if not row:
            print("Unknown project; press Return to continue."); input(); continue
        set_comment(root, row["id"], text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="Include retired, legacy, reference, stopped, and concept-only records.")
    parser.add_argument("--no-local", action="store_true", help="Skip local Git source checks.")
    parser.add_argument("--interactive", action="store_true", help="Keep the monitor open and accept comment commands.")
    parser.add_argument("--watch", type=int, metavar="SECONDS", help="Refresh the read-only display repeatedly; implies non-interactive mode.")
    parser.add_argument("--comment", nargs=2, metavar=("ENTITY_ID", "TEXT"), help="Set a comment without opening the interactive monitor.")
    parser.add_argument("--pin", metavar="ENTITY_ID", help="Pin a project to the top of its focus tier, or unpin it.")
    parser.add_argument("--focus", nargs=2, metavar=("ENTITY_ID", "TIER"), help="Set your focus on a project: now, maint, parked, or none.")
    arguments = parser.parse_args()
    if arguments.pin:
        index = read_json(ROOT / "current" / "index.json")
        if arguments.pin not in {entity["id"] for entity in index.get("entities", [])}:
            parser.error(f"unknown entity id: {arguments.pin}")
        print(f"{'Pinned' if toggle_pin(ROOT, arguments.pin) else 'Unpinned'} {arguments.pin}.")
        return
    if arguments.comment or arguments.focus:
        entity_id, value = arguments.comment or arguments.focus
        index = read_json(ROOT / "current" / "index.json")
        if entity_id not in {entity["id"] for entity in index.get("entities", [])}:
            parser.error(f"unknown entity id: {entity_id}")
        try:
            set_comment(ROOT, entity_id, value) if arguments.comment else set_focus(ROOT, entity_id, value)
        except ValueError as error:
            parser.error(str(error))
        print(f"Saved {'comment' if arguments.comment else 'focus'} for {entity_id}.")
        return
    if arguments.interactive:
        interactive(ROOT, arguments.all, not arguments.no_local)
        return
    while True:
        rows, metadata = build_rows(ROOT, include_all=arguments.all, inspect_local=not arguments.no_local)
        render(rows, metadata, clear=bool(arguments.watch))
        if not arguments.watch:
            return
        try:
            time.sleep(max(arguments.watch, 1))
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    main()
