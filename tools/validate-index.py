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

    # Dependencies are the graph, and until 2026-08-23 they were prose: 59
    # references resolved to no entity at all, including collective-comms still
    # naming the retired `collective-engine`. An index whose edges cannot be
    # walked can list what exists and not say how any of it connects, which is
    # most of what it is for.
    declared = set((index.get("externalDependencies") or {}).get("names", {}))
    for entity in entities:
        for dep in entity.get("dependencies") or []:
            if dep not in known:
                errors.append(
                    f"{entity['id']!r} depends on {dep!r}, which is not an entity id."
                    " Resolve it, or declare it under externalDependencies"
                )
        for dep in entity.get("externalDependencies") or []:
            if dep in known:
                errors.append(
                    f"{entity['id']!r} lists {dep!r} as external, but it is an entity"
                )
            elif dep not in declared:
                errors.append(
                    f"{entity['id']!r} lists {dep!r} as external and it is undeclared"
                )

    # A contract is the only thing that says two entities are one pipeline.
    for contract in index.get("contracts") or []:
        for role in ("producer", "consumer", "ownedBy"):
            ref = contract.get(role)
            if ref is not None and ref not in known:
                errors.append(
                    f"contract {contract.get('id')!r} names {ref!r} as {role},"
                    " which is not an entity"
                )

    # A cluster an entity claims membership of has to exist, and a cluster that
    # highlights something has to highlight it by id: 'collective-engine' sat in
    # the Pickleball Collective highlights while the entity itself was filed
    # under PickledBalls, so the cluster and the entity disagreed in silence.
    cluster_names = {c.get("name") for c in index.get("clusters") or []}
    for entity in entities:
        if entity.get("cluster") and entity["cluster"] not in cluster_names:
            errors.append(
                f"{entity['id']!r} is in cluster {entity['cluster']!r}, which is"
                " not defined in clusters[]"
            )
    # highlights[] is deliberately not checked against entity ids. It is prose --
    # "TestFlight builds uploaded", "iPhone bottle photography" -- and checking it
    # produced 41 warnings on its first run, almost all of them correct prose. A
    # check that noisy is one people learn to skip, which costs more than it finds.

    # Where a thing runs, for the entities that cannot simply run elsewhere.
    machines = {m.get("id") for m in (index.get("hosts") or {}).get("machines", [])}
    for entity in entities:
        if entity.get("host") and entity["host"] not in machines:
            errors.append(
                f"{entity['id']!r} names host {entity['host']!r}, which is not"
                " a machine in hosts"
            )
    for machine in (index.get("hosts") or {}).get("machines", []):
        for ran in machine.get("runs") or []:
            if ran not in known:
                errors.append(
                    f"host {machine.get('id')!r} runs {ran!r}, which is not an entity"
                )

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
