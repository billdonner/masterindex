# MasterIndex Universal Injection

As of Sunday, August 2, 2026, this is the single preferred file to inject into other sessions, machines, prompts, or agent bootstrap layers.

Use this everywhere except the future `workin On` integration, which should be handled separately.

## Copyable bootstrap text

```text
MasterIndex is the canonical shared portfolio index for cross-project work.

Before doing portfolio-wide, cross-repo, cross-app, or cross-machine work:

1. Read the canonical inventory:
   - current/index.json
2. Read the task registry if recurring or operational work is involved:
   - tasks/index.json
3. Use entities[].id as the canonical target keys.
4. Prefer most recently modified entries first unless the task requires another sort.
5. Treat the web page as presentation only, not source of truth.
6. Preserve verified external public links in each entry's links object.

When updating MasterIndex:

- update current/index.json first
- update current/inventory.md second only if the narrative needs to change
- do not silently rewrite tasks/index.json during a normal inventory refresh
- report gaps, blocked access, and ambiguities explicitly
```

## What this file is for

Use this one file for:

- `AGENTS.md`
- reusable prompt starters
- machine-local startup notes
- other agent systems that need a single bootstrap block
- hand-injected context on other machines

## What this file is not for

Do not use this file as the full `workin On` integration contract.

`workin On` should be handled separately because:

- it is an operational surface, not a full knowledge surface
- it should start fresh rather than preserve old board items
- any app-side behavior should generalize for any user, not just this portfolio

## workin On rule for later

When we do the `workin On` integration:

- start with a fresh `masterindex.*` namespace
- do not assume any old `workin On` board state should be preserved
- design the app-side behavior as a general product feature, not as a one-off MasterIndex hack

## Suggested future fill-ins

When you inject this elsewhere, pair it with your real GitHub URLs for:

- `current/index.json`
- `tasks/index.json`
- optional browser URL

The logic above should stay the same even if the base URL changes.
