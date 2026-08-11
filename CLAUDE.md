# Claude Code Instructions for Master Index

The canonical, vendor-neutral instruction file for this repository is
[`AGENTS.md`](./AGENTS.md). Read it first — it defines the agent contract
(read order, write rules, session routing, schema stability, architectural
boundaries) that applies regardless of which coding agent is operating
here.

This file exists only to:

1. Point Claude Code at `AGENTS.md` as the source of truth, and
2. Record genuinely Claude-specific operational notes, if any accumulate.

It is deliberately thin. Do not duplicate `AGENTS.md` content here — if
something belongs to the repository's contract, it belongs in `AGENTS.md`
so every agent system sees the same rules.

## Claude-specific notes

- None yet. Add entries here only when a rule is specific to how Claude
  Code (as opposed to any other agent) should behave in this repository.

## See also

- `AGENTS.md` — canonical agent contract
- `docs/agent-bootstrap/master-index-current-system.md` — verified system
  map (architecture, readers/writers, authoritative vs. generated files)
- `agent-ops/README.md` — additive orchestration sidecar for
  standardizing other repositories in the portfolio
