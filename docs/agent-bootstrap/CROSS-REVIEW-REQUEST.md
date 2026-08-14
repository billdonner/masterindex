# Cross-System Review Request — Paste Into Codex

This Master Index bootstrap was performed by **Claude Code**. Per the
bootstrap specification's Phase 9, it must also be independently reviewed
by **Codex**, in a fresh context, read-only. Codex could not be launched
automatically from this environment, so this document is the complete,
paste-ready handoff. Copy everything below the line into a fresh Codex
session with access to `~/masterindex`.

---

You are performing an INDEPENDENT, READ-ONLY review. You have no memory
of any prior work in this repository — treat this document as your only
context.

## Background

`~/masterindex` (git remote: `github.com/billdonner/masterindex`) is a
live, in-production coordination/data-registry repository: a canonical
portfolio index consumed by other repositories' agent instructions (e.g.
`~/qross/CLAUDE.md`, `~/drumbeats/CLAUDE.md` inject a delimited
MasterIndex block), a static web viewer (`site/`, deployed via GitHub
Pages by `.github/workflows/pages.yml`), and a `workin On` app feed
(`workinon/`).

Claude Code performed an "agent-orchestration bootstrap" on this
repository — commit `1fbdfe2` on `main`, "Add additive
agent-orchestration bootstrap layer" (compare against its parent,
`1c58765`, to see the exact diff: `git diff 1c58765..1fbdfe2`). The goal
was to ADD a safe, additive agent-orchestration layer while preserving
100% of existing behavior, schemas, paths, and update mechanisms — never
to redesign or "clean up" Master Index.

Claude Code also ran its own same-system review (a separate fresh
subagent, not the implementer) and wrote it to
`docs/agent-bootstrap/review-same-system.md` — that review found no
PROBLEM-level defects. **Do not trust that review either.** Your job is
to independently re-derive the same conclusions (or find what it missed)
directly from repository evidence, from a completely different coding
system, as a genuine second opinion.

## What was added (for orientation only — verify, don't trust)

- `docs/agent-bootstrap/master-index-current-system.md` — a system map
- `AGENTS.md` — appended to (claimed: not rewritten)
- `CLAUDE.md` — new, claimed to defer to `AGENTS.md`
- `agent-ops/` — new sidecar directory (`README.md`,
  `AGENT-BOOTSTRAP.md`, `PROCESS.md`, `portfolio.yaml`, `runs/`,
  `reviews/`), claimed to be inert/additive and not consumed by any
  existing application code

## Your job

Independently verify, from evidence (source, config, git history — not
from either of the documents mentioned above):

1. Was any existing file renamed, moved, deleted, or substantially
   rewritten? (`git diff --name-status 1c58765..1fbdfe2`,
   `git show --stat 1fbdfe2`)
2. Did any existing schema/API/update format/data contract/path change?
   Specifically check `current/index.json` top-level keys,
   `tasks/index.json`'s `globalTasks`/`entryTasks`, the shape of
   `current/handoffs/index.json`, `site/app.js`'s relative fetch to
   `../current/index.json`, and whether `.github/workflows/pages.yml`
   (the pre-existing Pages deploy CI) was touched.
3. Does `tools/masterindex-drift-check.sh --strict` still pass cleanly?
   (Note: it is a `#!/bin/zsh` script using zsh-only syntax — invoke it
   with `zsh tools/masterindex-drift-check.sh --strict`, not `bash` or
   `sh`, or you'll get a misleading interpreter error.)
4. Is the pre-existing `AGENTS.md` "Agent Contract" (read order, write
   rules, session routing, required keys, stability expectations) still
   present and semantically unchanged — only extended, not replaced?
   (`git diff 1c58765..1fbdfe2 -- AGENTS.md`)
5. Does the new `CLAUDE.md` avoid becoming a second, competing source of
   truth?
6. Is `agent-ops/` genuinely additive — does anything in `site/`,
   `tools/`, or `workinon/` now depend on it? Does
   `agent-ops/portfolio.yaml` claim any authority over
   `current/index.json`?
7. Is `docs/agent-bootstrap/master-index-current-system.md` factually
   accurate? Spot-check at least 5 claims directly against repository
   state.
8. Were any secrets or credentials introduced anywhere in the diff?
9. Would `~/qross/CLAUDE.md` and `~/drumbeats/CLAUDE.md` (read-only — do
   not modify anything outside `~/masterindex`) still function correctly
   given the current state of `~/masterindex`?
10. Anything the Claude Code implementation or its own same-system
    review appears to have misunderstood, missed, or gotten wrong that a
    fresh read of the repository reveals?

## Output

Write your findings to
`~/masterindex/docs/agent-bootstrap/review-cross-system.md` in this
repository. Structure: a short verdict, then a findings list (claim,
evidence, verdict per finding: CONFIRMED OK / PROBLEM / MINOR NIT). Be
skeptical of both the implementation and the prior same-system review —
you are the independent second opinion the bootstrap spec requires. Do
not modify anything else in `~/masterindex`. Do not modify any other
repository.

---

## Status

As of this document's creation, **cross-system review has not yet
occurred** — this file is the request, not the review. Do not treat
Master Index as `STANDARDIZED AND VERIFIED` until
`review-cross-system.md` actually exists and both reviews have gone
through adjudication (`agent-ops/PROCESS.md`, `ADJUDICATION` state).
