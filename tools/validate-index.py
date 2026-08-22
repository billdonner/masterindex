#!/usr/bin/env python3
"""Structural validation for current/index.json and tasks/index.json.

Written after the 2026-08-22 fork merge. A textual merge of current/index.json
resolved exactly one line by itself and produced structurally invalid JSON while
silently emitting a duplicate entity id, recording one system as two entities
under different ids, and resurrecting deleted records. None of that surfaced as
a conflict, so it has to be caught here instead.

Exit 0 clean, 1 on any error. Warnings never fail the run.
"""
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Repositories that legitimately host more than one entity.
SHARED_REPOS = {"~/oenora"}

errors: list[str] = []
warnings: list[str] = []


def main() -> int:
    try:
        index = json.loads((ROOT / "current/index.json").read_text())
    except json.JSONDecodeError as exc:
        print(f"ERROR current/index.json does not parse: {exc}")
        return 1

    entities = index.get("entities", [])
    ids = [e.get("id") for e in entities]

    if not all(ids):
        errors.append("every entity needs an id")
    for dup, count in Counter(ids).items():
        if count > 1:
            errors.append(f"duplicate entity id {dup!r} appears {count} times")

    # Every entityId reference must resolve. This is what caught the dangling
    # famster-ios-app reference that a conflict-free merge left behind.
    known = set(ids)
    dangling: list[str] = []

    def walk(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "entityId" and isinstance(value, str) and value not in known:
                    dangling.append(value)
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    walk(index)
    for ref in sorted(set(dangling)):
        errors.append(f"entityId {ref!r} does not resolve to any entity")

    # One system recorded as two entities is the shape the fork took, and a
    # dangling-reference check alone will not see it.
    repos = Counter(
        e["repo"] for e in entities if isinstance(e.get("repo"), str) and e["repo"].strip()
    )
    for repo, count in repos.items():
        if count > 1 and repo not in SHARED_REPOS:
            owners = [e["id"] for e in entities if e.get("repo") == repo]
            warnings.append(f"repo {repo!r} is claimed by {count} entities: {owners}")

    try:
        tasks = json.loads((ROOT / "tasks/index.json").read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"tasks/index.json does not parse: {exc}")
    else:
        coverage = set(tasks.get("entryTasks", {}))
        for missing in sorted(known - coverage):
            errors.append(f"entity {missing!r} has no tasks/index.json entryTasks coverage")
        for orphan in sorted(coverage - known):
            errors.append(f"entryTasks covers {orphan!r}, which is not an entity")

    for warning in warnings:
        print(f"WARN  {warning}")
    for error in errors:
        print(f"ERROR {error}")
    print(f"{len(entities)} entities checked: {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
