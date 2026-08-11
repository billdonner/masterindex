# Generic Repository-Standardization Bootstrap

This is the reusable specification for standardizing one target repository
in the portfolio. It is deliberately generic: the target may be an
application, server/service, library, infrastructure repo, CLI tool, data
system, documentation/knowledge repo, experimental repo, monorepo, or
coordination repo (like Master Index itself). Do not assume the target is
an application.

Run this against **one repository at a time**. Do not modify repositories
outside the current target.

## 1. Repository classification

Before anything else, classify the target:

- Type: application | service | library | infrastructure | CLI tool |
  data system | documentation/knowledge repo | experimental | monorepo |
  coordination repo | other (name it)
- Lifecycle: active | maintained | dormant | archived | unknown
- Does it have: a build step? a test suite? CI? a deployed runtime?
  multiple consumers?

Record this in `agent-ops/portfolio.yaml` (in Master Index) and in the
run record under `agent-ops/runs/`.

## 2. Baseline inspection (read-only)

Inspect, in this priority order (matches Master Index's own
Source-of-Truth Priority):

1. Executable behavior and actual source code
2. Tests and build configuration
3. CI/deployment configuration
4. Existing production-facing schemas/interfaces
5. Authoritative specifications and ADRs, if present
6. Existing `AGENTS.md`
7. Existing `CLAUDE.md`
8. README / general documentation
9. Handoff/session documents
10. Prior reviewer assertions, if any exist

Do not infer critical behavior only from README files if executable code
or configuration can verify it. Note what is verified fact vs. inference.

## 3. Creation/normalization of `AGENTS.md`

- If the target repository already has an `AGENTS.md`, preserve its
  useful existing instructions — extend, do not replace.
- If it does not, create one that describes the repository **as it
  actually exists**, based on step 2's findings — not an aspirational
  redesign.
- Keep it durable: repository purpose, map, architectural boundaries, how
  to inspect/validate it, existing update mechanisms, backward-
  compatibility requirements, what must not be changed casually, security
  rules, documentation pointers, completion criteria. Do not put volatile
  session state into it. Do not turn it into an encyclopedia.

## 4. Claude compatibility

- Preserve or create a root `CLAUDE.md` whose only job is to ensure
  Claude Code receives the canonical `AGENTS.md` instructions plus any
  genuinely Claude-specific operational rules.
- It must not become a second, competing source of repository truth.
- Reference/import `AGENTS.md` where the installed Claude Code version
  supports it.

## 5. Independent same-system code review

- A **fresh-context** subagent (same underlying coding system that did
  the normalization work) reviews the result independently.
- It must be read-only.
- The same agent that performed the normalization must not review its
  own work.
- It checks: does `AGENTS.md` accurately describe the repo, is
  `CLAUDE.md` appropriately scoped, were any schemas/paths/interfaces
  changed, is anything dangerous or broken, is documentation now
  inconsistent with code.
- Findings go in the target repository (its own
  `docs/agent-bootstrap/review-same-system.md`, or that repo's
  established equivalent) — not duplicated into Master Index unless the
  target repo has nowhere sensible to put it.

## 6. Independent other-system code review

- The repository must also be reviewed by the other primary coding-agent
  system (Claude Code ↔ Codex).
- Fresh context, read-only.
- If the other system cannot be invoked automatically from the current
  environment, produce a complete, paste-ready handoff document (a
  `CROSS-REVIEW-REQUEST.md`) instead of pretending the review happened.
  Do not claim cross-system review occurred until it actually has.

## 7. Adjudication / comparison

- A fresh-context agent compares both reviews once both exist.
- It independently verifies disputed claims against repository evidence
  — repository evidence outranks reviewer opinion.
- Classify each substantive finding: AGREED / ACCEPT / REJECT / CONFLICT
  / DUPLICATE.
- Do not apply corrections during adjudication — that's a separate step.

## 8. Corrections

- A fresh implementation context applies only the accepted corrections
  from adjudication.
- No unrelated cleanup, no scope creep.

## 9. Final independent verification

- A final fresh, read-only context verifies: accepted corrections were
  applied, the repository still operates as before, `AGENTS.md` is
  accurate, `CLAUDE.md` is appropriately scoped, no unrelated changes
  were introduced.

## 10. Master Index status update

- Update the entry in `agent-ops/portfolio.yaml` (`standardization`,
  `last_reviewed`, `authoritative_project_instructions` pointer, notes).
- Do not touch `current/index.json` as part of this step unless a
  deliberate, separately-justified decision is made to reflect the same
  fact there too (see ownership boundary in `agent-ops/README.md`).

## Isolation requirement

Bootstrap, review, adjudication, correction, and verification steps
should each run in an isolated agent context (fresh subagent / fresh
session) where the tooling supports it, so a review is never contaminated
by the memory of the work it's reviewing.
