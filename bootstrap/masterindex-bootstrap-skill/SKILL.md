---
name: masterindex-bootstrap
description: Use when work spans multiple apps, repositories, services, or machines and the agent should consult the shared MasterIndex inventory and task registry before acting. This skill helps agents fetch the canonical MasterIndex files, target entries by stable entity ids, preserve verified public links, and prefer most-recently-modified items first for portfolio-wide work.
---

# MasterIndex Bootstrap

Use this skill when a task involves more than one project, or when portfolio context matters.

## Read order

1. Read `current/index.json`
2. Read `tasks/index.json` if recurring or operational work is involved
3. Use `current/inventory.md` only for narrative context

## Operating rules

- Use `entities[].id` as canonical target keys
- Preserve verified external public links in each entry's `links` object
- Default to most recently modified entries first unless a more specific sort is required
- Treat the web page as presentation, not source of truth

## When updating MasterIndex

- Update `current/index.json` first
- Update `current/inventory.md` second when the narrative should change
- Do not silently rewrite `tasks/index.json` during a normal inventory refresh

## Expected file contract

- `current/index.json`
- `current/inventory.md`
- `tasks/index.json`

## Good triggers

- "review all my active apps"
- "which backend does this app use"
- "what changed most recently"
- "which entries still need public links"
- "run the periodic checks for these apps"
