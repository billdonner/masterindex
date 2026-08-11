# Master Index — Current System Map

Status: verified by direct inspection of the repository at commit `1c58765` (2026-08-11, after pulling 4 commits that had landed on `origin/main` ahead of the local checkout this bootstrap started from), unless marked **[inference]**.

## Purpose

Master Index (`billdonner/masterindex`) is the canonical, machine-readable
portfolio index for Bill Donner's cross-project work: a snapshot of every
app, repo, service, and cluster he maintains, plus a task registry for
recurring/periodic housekeeping and a handoff registry for targeted
directives. It exists so agents working in any single repository (or on a
different machine) can look up portfolio-wide facts without re-deriving
them, and so a small number of housekeeping agents can keep those facts
fresh.

It is **not** a build artifact, not a deployed service, and not itself an
application — it is a data + documentation repository consumed by other
agent sessions, by a local static web viewer, and (partially) by the
`workin On` app.

## Repository Classification

Coordination / data-registry repository (per the AGENT-BOOTSTRAP taxonomy:
"coordination repositories"). No build step, no test suite, no CI, no
deployed runtime of its own.

## Current Directory Structure

```
masterindex/
├── AGENTS.md                     — agent contract (pre-existing, canonical)
├── README.md                     — human-facing hub description
├── GITHUB_PUBLISHING.md          — raw-URL / publishing contract
├── TASK_LIFECYCLE.md             — task state model (design doc)
├── WEB_INFORMATION_ARCHITECTURE.md — site/ IA design doc
├── WORKINON_BOARD_SCHEMA.md      — workin On card schema design doc
├── bootstrap/                    — reusable injection snippets for OTHER repos/agents
│   ├── README.md
│   ├── MASTERINDEX_UNIVERSAL_INJECTION.md
│   ├── MASTERINDEX_MANAGED_BLOCK.md
│   ├── AGENTS_SNIPPET.md
│   ├── MASTERINDEX_DRIFT_LAUNCHAGENT.md
│   ├── install-masterindex-drift-launchagent.sh
│   ├── housekeeping-task-template.md
│   └── masterindex-bootstrap-skill/SKILL.md
├── current/
│   ├── index.json                — AUTHORITATIVE core inventory
│   ├── inventory.md               — human narrative companion (generated from index.json)
│   └── handoffs/index.json        — AUTHORITATIVE targeted-directive registry
├── tasks/
│   ├── index.json                 — AUTHORITATIVE recurring-task registry
│   ├── README.md
│   └── templates/entry-task.template.json
├── snapshots/2026-08-01/          — dated freeze of index.json + inventory.md
├── site/                          — static browser (index.html, app.js, styles.css)
├── tools/
│   ├── masterindex-drift-check.sh — read-only validator/drift checker
│   ├── generate_workinon_feed.py  — generator for workinon/board-feed.json
│   └── generate_workinon_feed.mjs
├── workinon/
│   ├── board-feed.json            — GENERATED operational feed for workin On
│   ├── shortcut-manifest.json     — GENERATED workinon:// post URLs
│   └── README.md
├── index.html                     — GENERATED-ish redirect stub to site/ (GitHub Pages entry point)
└── .github/workflows/pages.yml    — CI: deploys index.html + site/ + current/ + tasks/ to GitHub Pages on push to main
```

## Authoritative Files (source of truth)

- `current/index.json` — the core inventory. Top-level keys observed:
  `generatedAt, scope, summary, automation, flyOperations, ascApps,
  clusters, entities, collaborators, services, repos, gaps, taskRegistry`.
  36 entities, 45 repos, 8 services, 16 clusters as of the inspected commit.
  Each entity has `id, name, kind, cluster, status, lastModified, repo,
  bundleId, release, description, dependencies, links, notes`.
- `tasks/index.json` — recurring task registry. Keys:
  `generatedAt, schemaVersion, description, defaultExecutionAssumptions,
  entityCoveragePolicy, globalTasks, entryTasks`. 4 global tasks, 22
  entry-level tasks observed. Tasks target entities by `entities[].id`.
- `current/handoffs/index.json` — targeted directive registry. Keys:
  `generatedAt, schemaVersion, description, targeting, directives`.
  Empty `directives: []` at inspection time — mechanism exists, unused.
- `AGENTS.md` — the pre-existing agent contract. This already specifies
  read order, write rules, session-routing rules, required schema keys,
  and stability expectations. It is the closest thing this repo already
  has to the artifact this bootstrap's Phase 3 asks for.

## Generated / Derivative Files (do not hand-edit as primary source)

- `current/inventory.md` — narrative rendering of `index.json`.
- `workinon/board-feed.json`, `workinon/shortcut-manifest.json` — produced
  by `tools/generate_workinon_feed.{py,mjs}` from `index.json` +
  `tasks/index.json`.
- `snapshots/YYYY-MM-DD/` — point-in-time freezes, historical, not written
  during normal refresh cycles.

## Readers

- **Other agent sessions / other machines**: per `AGENTS.md` and the
  `bootstrap/` injection snippets, agents read `current/index.json`,
  `tasks/index.json`, and `current/handoffs/index.json` before portfolio-
  wide or cross-repo work. **Verified in the wild**: `~/qross/CLAUDE.md`
  and `~/drumbeats/CLAUDE.md` both contain the delimited
  `<!-- MASTERINDEX:START -->…<!-- MASTERINDEX:END -->` managed block from
  `bootstrap/MASTERINDEX_MANAGED_BLOCK.md`, confirming this repo is
  actively consumed by at least two other repositories' agent instructions
  today.
- **`site/app.js`** — static browser; does `fetch("../current/index.json")`
  relative to `site/`, i.e. it must be served with `site/` and `current/`
  as siblings. Read-only; presentation layer only (per both `AGENTS.md`
  and the WEB_INFORMATION_ARCHITECTURE design doc).
- **`workin On` app** — [inference, per WORKINON_BOARD_SCHEMA.md and
  workinon/README.md] consumes `workinon/board-feed.json` /
  `shortcut-manifest.json` as an operational dashboard feed, namespaced
  `masterindex.*`. Not verified by inspecting the workin On app itself
  (out of scope — other repos were not touched).

## Writers

- Human/agent-driven refresh cycles update `current/index.json` (first),
  then `current/inventory.md` (only if narrative changes), per the write
  rules in `AGENTS.md`. Git log shows frequent small commits doing exactly
  this ("Refresh X state", "Reconcile Y source mapping").
- `tools/generate_workinon_feed.py` / `.mjs` regenerate the `workinon/`
  feed files from the inventory + task registry.
- `tasks/index.json` is explicitly meant to be edited rarely/deliberately
  — "do not silently rewrite `tasks/index.json` during a normal inventory
  refresh" appears in `AGENTS.md`, `README.md`, and multiple bootstrap
  snippets, consistently.
- No writer touches `current/handoffs/index.json` in the observed history
  (directives array is empty); the mechanism is defined but not yet used.

## Automation / Jobs

- `tools/masterindex-drift-check.sh` — read-only validator, installable as
  a macOS LaunchAgent (`com.billdonner.masterindex.drift`, every 6 hours)
  via `bootstrap/install-masterindex-drift-launchagent.sh`. It validates
  JSON, checks required top-level keys, reports a dirty working tree, and
  compares local HEAD to `origin/main` via `git ls-remote`. It explicitly
  does **not** pull, rebase, commit, push, or edit anything. No evidence
  found that this LaunchAgent is currently installed on this machine
  (install script exists; no check for an installed plist was run, since
  that would require inspecting `~/Library/LaunchAgents`, outside this
  repo — **[unresolved unknown]**).
- **GitHub Actions / CI exists**: `.github/workflows/pages.yml` deploys
  `index.html`, `site/`, `current/`, and `tasks/` to GitHub Pages on every
  push to `main` that touches those paths (or via manual
  `workflow_dispatch`). This is a deploy pipeline, not a test/validation
  gate — it does not run `tools/masterindex-drift-check.sh` or any other
  check before deploying. No automated test suite exists. Validation
  today is `tools/masterindex-drift-check.sh --strict` run manually or
  via the LaunchAgent, independent of the Pages deploy.
- Root `index.html` is a thin redirect stub (`meta http-equiv="refresh"`
  to `site/`) that exists specifically so GitHub Pages has an entry point
  at the repo root; `site/index.html` remains the real application.

## Update Mechanism / Publishing Model

- Git-based, GitHub-hosted (`github.com/billdonner/masterindex`, public
  remote `origin`, default branch `main`). `GITHUB_PUBLISHING.md` documents
  the intended raw-URL contract for other machines/agents to fetch
  `current/index.json`, `current/inventory.md`, `tasks/index.json`
  directly via `raw.githubusercontent.com`, and an optional GitHub Pages
  deployment of `site/`.
- CLAUDE.md (the user's global `~/CLAUDE.md`, not a repo-local file) also
  independently documents this same read/write contract under "MasterIndex
  (canonical portfolio index)", consistent with `AGENTS.md`.

## Synchronization Assumptions

- Single writer at a time is assumed implicitly (no lockfile, no CI merge
  gate); conflicts are handled by ordinary git merge/rebase.
- Multiple **readers** across machines are explicitly anticipated (that is
  the whole point of the repo) — `AGENTS.md`'s "Session routing" section
  explicitly discusses preferring an already-open per-repository agent
  session over duplicating work in the MasterIndex session.
- The drift checker's role is to detect (not resolve) two kinds of drift:
  local checkout behind/ahead of `origin/main`, and structural drift from
  the required-keys contract.
- `entities[].id` and `clusters[].name` are declared stable identifiers —
  external consumers (other repos' CLAUDE.md injections, `workin On`
  feed keys `masterindex.*`) may depend on `id` stability.

## Backward-Compatibility Requirements (verified from contract docs)

1. `current/index.json` top-level keys `generatedAt, scope, summary,
   ascApps, clusters, entities, services, repos, gaps` must remain present
   (enforced by `masterindex-drift-check.sh`). Additional keys observed but
   not enforced by the checker: `automation, flyOperations, collaborators,
   taskRegistry`.
2. `tasks/index.json` must retain `globalTasks` and `entryTasks` (enforced
   by the checker).
3. `current/handoffs/index.json` must remain valid JSON and exist
   (enforced by the checker; keys not schema-checked by the script).
4. `entities[].id` must remain stable once introduced.
5. Write order (`index.json` before `inventory.md`) and the
   "don't silently rewrite `tasks/index.json`" rule are load-bearing
   conventions repeated across `AGENTS.md`, `README.md`, `TASK_LIFECYCLE.md`,
   and every bootstrap snippet — clearly deliberate, not incidental.
6. `site/app.js`'s relative fetch path (`../current/index.json`) requires
   `site/` and `current/` to remain siblings at their current relative
   depth.

## Areas That Must Not Be Changed Casually

- The schema/shape of `current/index.json`, `tasks/index.json`,
  `current/handoffs/index.json`.
- The relative path layout between `site/`, `current/`, `tasks/`.
- The existing `AGENTS.md` contract — it is already the canonical
  agent-instruction file this bootstrap is asked to "create or normalize."
  It should be extended, not replaced.
- `bootstrap/` — this is the existing "inject Master Index into other
  repos" mechanism, already in production use (confirmed via
  `~/qross/CLAUDE.md`, `~/drumbeats/CLAUDE.md`). This bootstrap's
  `agent-ops/` sidecar is a **different, additive** concern (standardizing
  *other* repos' own AGENTS.md/review process) and must not be conflated
  with or replace `bootstrap/`'s existing role (injecting *Master Index
  awareness* into other repos).

## Unresolved Unknowns

- Whether the drift-check LaunchAgent is actually installed/running on
  this machine right now (not checked — out of this repo's scope to
  verify via `launchctl`, though it could be checked non-destructively;
  deferred to avoid scope creep beyond repository inspection).
- The full current behavior of the `workin On` app's consumption of
  `workinon/board-feed.json` — only documented intent was inspected, not
  the consuming app's code (that app lives in a different repository,
  out of scope for this bootstrap per the constraints).
- Whether any other machines beyond this one currently pull this repo on
  a schedule (design intent is clear; live confirmation would require
  access this session doesn't have).
