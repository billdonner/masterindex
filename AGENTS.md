# Agent Contract

If you are an agent consuming or updating this index:

## Read order

1. Read `current/index.json`
2. Read `tasks/index.json` if you need to discover periodic work assigned to entries
3. Read `current/handoffs/index.json` before running a periodic or operational task; apply active directives addressed to the target entity or `all-entities`
4. Use `current/inventory.md` only for narrative context
5. Treat `site/` as presentation, not source of truth

## Write rules

- Update `current/index.json` first
- Then update `current/inventory.md`
- Do not silently rewrite `tasks/index.json` while refreshing inventory data
- Keep the site compatible with the JSON schema
- Preserve prior facts unless replaced by newer observed facts
- Distinguish observed facts from gaps or ambiguities
- If App Store Connect access is unavailable, record that explicitly
- If an entry has any verified external public link, include it in the entry data

## Required top-level sections in `current/index.json`

- `generatedAt`
- `scope`
- `summary`
- `ascApps`
- `clusters`
- `entities`
- `services`
- `repos`
- `gaps`

## Required file for periodic task routing

- `tasks/index.json`

## Required file for targeted next-cycle behavior

- `current/handoffs/index.json`

## Stability expectations

- `entities[].id` should remain stable once introduced
- `clusters[].name` should remain stable unless there is a deliberate rename
- `repo` paths should stay in `~/...` form when possible for readability
- Store verified public links under each entity's `links` object when available
- Default display order should normally be most recently modified first

## Intended use

This file set is designed so housekeeping agents on other machines can:

- locate active repos
- understand cross-app dependencies
- detect gaps
- choose the right repo or service before starting work
- discover which recurring tasks belong to which entity ids
