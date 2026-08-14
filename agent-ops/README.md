# agent-ops

This is an **additive orchestration sidecar**. It coordinates the process
of standardizing *other* repositories in the portfolio (adding/normalizing
their own `AGENTS.md`, running independent review, and tracking
standardization status). It is not part of Master Index's core inventory
system.

## What this is

- A workflow definition (`PROCESS.md`) for taking a repository through
  inspection → normalization → independent review → cross-agent-system
  review → adjudication → corrections → final verification.
- A generic bootstrap specification (`AGENT-BOOTSTRAP.md`) that any coding
  agent (Claude Code, Codex, or otherwise) can follow to standardize one
  target repository.
- An orchestration ledger (`portfolio.yaml`) tracking which repositories
  have gone through this process and what state they're in.
- `runs/` — per-repository orchestration run records (created as runs
  happen; empty until then).
- `reviews/` — cross-repository review/adjudication artifacts, for cases
  where a review doesn't belong inside the target repository itself
  (created as reviews happen; empty until then).

## What this is not

- **Not** a replacement for `current/index.json`, `tasks/index.json`, or
  `current/handoffs/index.json`. Those remain the canonical Master Index
  data files, described in `../AGENTS.md`.
- **Not** authoritative about any repository's own architecture or
  operating instructions. Per the ownership boundary this bootstrap
  establishes: each repository owns truth about itself (source, tests,
  its own `AGENTS.md`/`CLAUDE.md`); Master Index only records
  portfolio-level facts (identity, type, lifecycle, relationships,
  standardization state, pointers to that repository's own docs).
- **Not** a trigger for existing Master Index applications. Nothing in
  `site/`, `tools/`, or `workinon/` reads from or depends on `agent-ops/`.
  It is safe to ignore this directory entirely and Master Index continues
  to work exactly as before.
- **Not** a second inventory. `portfolio.yaml` here is an orchestration
  ledger only — it must never silently replace or mutate
  `current/index.json`. If a future change wants to merge these, that is
  a deliberate, separate decision, not an automatic side effect of using
  this sidecar.

## How to use it

1. Read `AGENT-BOOTSTRAP.md` for the generic per-repository
   standardization spec.
2. Read `PROCESS.md` for the state machine that governs a run.
3. Check `portfolio.yaml` for the target repository's current
   `standardization` state before starting or resuming work.
4. Record the run under `runs/<repo>-<date>/` as it progresses.
5. Update `portfolio.yaml`'s `standardization` field and `last_reviewed`
   when a run reaches a terminal or checkpoint state.
6. Do not touch any repository outside the one being standardized in a
   given run.

This sidecar assumes a human or orchestrating session drives it — it is
not itself an automated job.
