# Repository-Standardization Process (State Machine)

Each repository being standardized via `AGENT-BOOTSTRAP.md` moves through
these states. Track current state in `agent-ops/portfolio.yaml` under
that repository's `standardization` field.

```
UNASSESSED
IN_ASSESSMENT
NORMALIZING
PRIMARY_REVIEW
CROSS_AGENT_REVIEW
ADJUDICATION
CORRECTIONS
FINAL_VERIFICATION
STANDARDIZED
BLOCKED
ARCHIVED_NO_MIGRATION
```

The orchestrator (whatever session is driving this process) is a
**coordinator only** — it does not itself substitute for the isolated
agent contexts required at each step.

---

### UNASSESSED

- **Entry condition**: repository has no orchestration run yet, or is
  newly added to `portfolio.yaml`.
- **Permitted actions**: none beyond recording the repository exists.
- **Required artifacts**: a `portfolio.yaml` entry with `standardization:
  UNASSESSED`.
- **Exit condition**: someone decides to start a run.
- **Who may modify target repo**: no one.
- **Who must stay read-only**: everyone.

### IN_ASSESSMENT

- **Entry condition**: a run starts (`agent-ops/runs/<repo>-<date>/`
  created).
- **Permitted actions**: read-only inspection per `AGENT-BOOTSTRAP.md`
  step 1–2 (classification, baseline inspection).
- **Required artifacts**: classification + inspection notes in the run
  record.
- **Exit condition**: inspection is complete enough to normalize.
- **Who may modify target repo**: no one (read-only phase).
- **Who must stay read-only**: the assessing agent.

### NORMALIZING

- **Entry condition**: assessment complete.
- **Permitted actions**: create/normalize the target's `AGENTS.md` and
  `CLAUDE.md` per `AGENT-BOOTSTRAP.md` steps 3–4. Additive changes only —
  no unrelated refactors, no schema changes.
- **Required artifacts**: the normalized `AGENTS.md`/`CLAUDE.md` in the
  target repo; a summary of what was created/changed in the run record.
- **Exit condition**: normalization is committed (or ready to commit) in
  the target repo.
- **Who may modify target repo**: the implementing agent for this run.
- **Who must stay read-only**: no one yet (this is the one write phase
  before review).

### PRIMARY_REVIEW

- **Entry condition**: normalization exists.
- **Permitted actions**: fresh-context, read-only, same-coding-system
  review per `AGENT-BOOTSTRAP.md` step 5. Must not be performed by the
  agent that did the normalizing.
- **Required artifacts**: `review-same-system.md` (in the target repo's
  `docs/agent-bootstrap/`, or its established equivalent).
- **Exit condition**: review is written.
- **Who may modify target repo**: no one.
- **Who must stay read-only**: the reviewing agent.

### CROSS_AGENT_REVIEW

- **Entry condition**: primary review exists.
- **Permitted actions**: fresh-context, read-only review by the other
  coding-agent system (Claude Code ↔ Codex), per `AGENT-BOOTSTRAP.md`
  step 6. If that system cannot be launched from the current environment,
  produce `CROSS-REVIEW-REQUEST.md` instead and treat the repository as
  **BLOCKED** on cross-system review until it's actually done.
- **Required artifacts**: `review-cross-system.md`, or
  `CROSS-REVIEW-REQUEST.md` if genuinely blocked.
- **Exit condition**: the cross-system review exists (not just requested).
- **Who may modify target repo**: no one.
- **Who must stay read-only**: the reviewing agent.

### ADJUDICATION

- **Entry condition**: both reviews exist.
- **Permitted actions**: fresh-context comparison of both reviews against
  repository evidence per `AGENT-BOOTSTRAP.md` step 7. No corrections
  applied here.
- **Required artifacts**: `review-comparison.md` with each finding
  classified AGREED / ACCEPT / REJECT / CONFLICT / DUPLICATE.
- **Exit condition**: comparison is written.
- **Who may modify target repo**: no one.
- **Who must stay read-only**: the adjudicating agent.

### CORRECTIONS

- **Entry condition**: adjudication exists with at least one ACCEPT or
  AGREED finding requiring a change (if none, skip straight to
  FINAL_VERIFICATION).
- **Permitted actions**: fresh implementation context applies only the
  accepted corrections.
- **Required artifacts**: record of what was changed, tied to the
  adjudicated findings.
- **Exit condition**: accepted corrections are applied.
- **Who may modify target repo**: the correcting agent, for accepted
  findings only.
- **Who must stay read-only**: everyone else.

### FINAL_VERIFICATION

- **Entry condition**: corrections applied (or skipped, if none needed).
- **Permitted actions**: fresh, read-only verification per
  `AGENT-BOOTSTRAP.md` step 9.
- **Required artifacts**: `final-verification.md`.
- **Exit condition**: verification confirms the repo is in a good state.
- **Who may modify target repo**: no one.
- **Who must stay read-only**: the verifying agent.

### STANDARDIZED

- **Entry condition**: final verification passed and both same-system and
  cross-system reviews genuinely occurred (not just requested).
- **Permitted actions**: update `portfolio.yaml` for this repository.
- **Required artifacts**: `portfolio.yaml` entry updated with
  `standardization: STANDARDIZED`, `last_reviewed` set.
- **Exit condition**: terminal state (may re-enter `IN_ASSESSMENT` later
  if the repository changes substantially).
- **Who may modify target repo**: no one (process is complete).

### BLOCKED

- **Entry condition**: any step cannot proceed (missing access, cross-
  system reviewer unavailable, ambiguous ownership, etc).
- **Permitted actions**: document the blocker.
- **Required artifacts**: a note in the run record and in `portfolio.yaml`
  (`notes` field) describing exactly what is blocked and why.
- **Exit condition**: blocker resolved, returning to the state it was
  blocked from.
- **Who may modify target repo**: no one while blocked.

### ARCHIVED_NO_MIGRATION

- **Entry condition**: repository is determined to be dead/archived and
  not worth standardizing.
- **Permitted actions**: document the decision.
- **Required artifacts**: `portfolio.yaml` entry with
  `standardization: ARCHIVED_NO_MIGRATION` and a note explaining why.
- **Exit condition**: terminal (no further action expected).

---

## Notes

- "Fresh-context" means a new agent session/subagent with no memory of
  the work it's reviewing — not the same conversation continuing.
- Every write-capable state (`NORMALIZING`, `CORRECTIONS`) is immediately
  followed by a read-only state before the process can advance further.
- Master Index's own repository, if ever run through this process,
  follows the same state machine — this bootstrap effort itself
  corresponds to `NORMALIZING` having occurred, with
  `PRIMARY_REVIEW`/`CROSS_AGENT_REVIEW`/etc. still to come (see
  `docs/agent-bootstrap/bootstrap-report.md`).
