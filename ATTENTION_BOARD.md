# Attention Board

As of Wednesday, August 19, 2026.

`current/attention.json` is the single definition of "something in this
portfolio needs a decision or an action".

Two surfaces render it, and neither one decides for itself what matters:

- the web browser (`site/`) shows it as the attention strip
- `workin On` shows it as board cards, via `tools/generate_workinon_feed.py`

Because both read the same artifact, they cannot drift apart.

## Why it was rebuilt

The first `workin On` feed produced 65 cards, of which exactly one was high
priority. It was a log, not a board:

- 22 cards said only "X changed. Last modified <date>." — a reformatted `git log`.
- 29 cards repeated one complaint, "missing public link", once per entity —
  including for apps deliberately recorded as internal-use and TestFlight-only,
  and for apps that simply had not shipped yet.
- 10 task cards were derived from declared cadence with no record of when a
  task last ran, so every one of them was permanently due.
- Nothing could ever be cleared, because every card was recomputed from static
  configuration on each run.

The rebuild reduced this to the items that carry a real next step.

## Design rules

1. **An item exists only if there is an action or a decision available.**
   Every item carries an `action` field saying what to actually do.
2. **An item must be clearable.** It disappears when the underlying condition
   changes in an authoritative file — not when someone hides it.
3. **Conditions that are correct by design are suppressed, and the suppression
   is reported.** `suppressed[]` records every rule that fired and why, so an
   empty board is trustworthy rather than mysterious.
4. **Recency is a diff, not a log.** Changes are reported relative to a review
   watermark. Without a watermark they collapse into one card instead of one
   card per changed entry.
5. **Cadence alone never makes a task due.** A task is overdue only when a real
   run has been recorded, because otherwise every task is due forever.

## Inputs

| File | Role |
| --- | --- |
| `current/index.json` | Authoritative. Open gaps and entity link coverage. |
| `tasks/index.json` | Authoritative. Active recurring tasks. |
| `current/attention-policy.json` | Authoritative. Tuning rules — what counts as actionable. |
| `current/attention-state.json` | Authoritative. Operator state: review watermark, recorded task runs, dismissals. |
| `current/attention.json` | **Generated. Never hand-edit.** |

Tune the board by editing `attention-policy.json`, not the generator.

## Item kinds

| Kind | Emitted when |
| --- | --- |
| `open-gap` | A `gaps[]` entry is dispositioned `open`. Uses its `title`, `nextAction`, `priority`, and `entityIds`. |
| `link-gap` | An entity is expected to have a public link and does not. Expectation is set per status and kind in the policy. |
| `overdue-task` | An active task's last recorded run plus its cadence, plus a grace period, is in the past. |
| `changed-since-review` | An entity's `lastModified` is newer than `lastReviewedAt`. Capped, with an overflow card. |
| `triage` | A structural problem that blocks the board itself — undispositioned gaps, or tasks with no run history. |

## Gap fields this depends on

Every `gaps[]` entry carries:

- `id` — stable identifier, used for card ids and `workin On` status keys
- `disposition` — `open`, `resolved`, or `accepted`
- `priority` — `high`, `medium`, or `low`
- `title` — a short actionable headline
- `entityIds` — the entities the gap concerns, so a card can deep-link
- `nextAction` — required on `open` gaps: the concrete next step

`resolved` is history. `accepted` is a recorded decision with no pending work.
Only `open` reaches the board.

## Operating it

```sh
python3 tools/generate_attention.py             # recompute what is actionable
python3 tools/generate_attention.py --mark-reviewed   # stamp the review watermark
python3 tools/generate_workinon_feed.py --refresh     # regenerate both artifacts
```

To clear a change from the board, resolve it in `current/index.json` — flip the
gap's `disposition` to `resolved`, or record the link, or record the task run.
Then regenerate.

To record a task run, add its `taskId` and an ISO timestamp under `taskRuns` in
`current/attention-state.json`. Overdue cards then appear on their own schedule.

To silence an item without resolving it, add its id under `dismissed` in
`attention-state.json` with an optional `until` timestamp and a `reason`.

## Publishing

`.github/workflows/pages.yml` regenerates `current/attention.json` before
assembling the site, so the published web board can never lag behind the
inventory. The generator is deterministic and reads only committed files, so
the CI-built artifact matches the committed one apart from its timestamp.

The `workin On` feed is generated on demand rather than in CI, because
`workin On` consumes the committed `workinon/board-feed.json` directly.

## See also

- `AGENTS.md` — the canonical agent contract
- `WORKINON_BOARD_SCHEMA.md` — how `workin On` should render the cards
- `WEB_INFORMATION_ARCHITECTURE.md` — the web browser's information architecture
