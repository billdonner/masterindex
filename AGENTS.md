# Agent Contract

If you are an agent consuming or updating this index:

## Read order

1. Read `current/index.json`
2. Read `tasks/index.json` if you need to discover periodic work assigned to entries
3. Read `current/handoffs/index.json` before periodic or operational work; apply active directives for the entity or `all-entities`
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

## Session routing

- For a modification inside an indexed repository, first prefer an already-open
  agent session whose working directory is that repository.
- Use the MasterIndex session for inventory updates, cross-repository planning,
  routing, and work that has no active repository session.
- Do not duplicate implementation in MasterIndex when a repository-root
  session is known to be active; give that session the bounded handoff instead.
- If no such session is known or available, say so and proceed from the
  repository's working directory only after checking its agent instructions and
  working-tree status.

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

## Repository classification

Master Index is a coordination/data-registry repository: a canonical
inventory + task registry + static browser, not an application, service,
or library. It has no build step, no deployed runtime of its own, and no
automated test suite. Validate it with `tools/masterindex-drift-check.sh
--strict`, which is read-only (see that script and
`bootstrap/MASTERINDEX_DRIFT_LAUNCHAGENT.md`).

## Architectural boundaries — do not change casually

- The schema of `current/index.json`, `tasks/index.json`, and
  `current/handoffs/index.json` (required top-level keys are enforced by
  `tools/masterindex-drift-check.sh`).
- The relative path layout between `site/`, `current/`, and `tasks/` —
  `site/app.js` fetches `../current/index.json`.
- The read/write order and stability rules already defined above in this
  file — they are relied on by other repositories' agent instructions
  (e.g. `~/qross/CLAUDE.md` injects the delimited block from
  `bootstrap/MASTERINDEX_MANAGED_BLOCK.md`; `~/drumbeats/CLAUDE.md` has
  compatible manual MasterIndex guidance, not the managed block).
- `bootstrap/` — the existing mechanism for injecting *Master Index
  awareness* into other repositories. Keep this distinct from
  `agent-ops/`, which is a separate, additive layer for standardizing
  *other repositories' own* agent instructions and review process (see
  `agent-ops/README.md`). Neither replaces the other.

## Full system reference

For a verified, detailed map of this repository's architecture, readers,
writers, generated vs. authoritative files, and open unknowns, see
`docs/agent-bootstrap/master-index-current-system.md`.

## Agent-orchestration sidecar

`agent-ops/` holds an additive, opt-in workflow for standardizing *other*
repositories in this portfolio (AGENTS.md normalization, independent
review, cross-agent-system review, adjudication). It does not change how
Master Index itself is read or written. See `agent-ops/README.md` before
using it.
