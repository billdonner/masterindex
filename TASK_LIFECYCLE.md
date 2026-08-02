# Task Lifecycle

As of Sunday, August 2, 2026.

## Goal

Define how recurring tasks move from definition to action to update, so the web page and `workin On` can stay consistent.

## Core principle

Inventory data and task data should stay separate but synchronized.

- `current/index.json` = what exists
- `tasks/index.json` = what should be checked or done

## Task states

Use a simple explicit lifecycle.

### `active`

Task should continue running on its cadence.

Examples:

- release checks
- link verification
- health checks

### `paused`

Task is intentionally suspended but still meaningful.

Examples:

- app is dormant for now
- check is temporarily noisy

### `blocked`

Task cannot make meaningful progress without a dependency or access path.

Examples:

- ASC unavailable
- endpoint unreachable for reasons outside task scope
- target repo missing

### `retired`

Task no longer belongs in the system.

Examples:

- entity removed
- replaced by a better task
- merged into a cluster-level task

## Execution cycle

### 1. Discover target

Locate the entry by stable `entityId`.

Never route by display name if the id is available.

### 2. Read current context

Read:

- `current/index.json`
- `tasks/index.json`
- optional narrative companion when needed

### 3. Perform the check

Examples:

- verify public link still resolves
- verify backend still exists
- verify release status changed
- verify metadata is stale or current

### 4. Classify outcome

Possible outcomes:

- no change
- changed
- warning
- blocked
- failed

### 5. Update canonical artifacts

If facts changed:

- update `current/index.json`
- update `current/inventory.md` only if the narrative should change

If only task posture changed:

- update `tasks/index.json`

### 6. Emit operational surface

If relevant, create or refresh a board item for `workin On`.

## Recommended outcome model

Add this conceptually even if not yet implemented:

```json
{
  "lastRunAt": "2026-08-02T08:00:00-05:00",
  "lastOutcome": "changed",
  "lastOutcomeSummary": "Verified website is still live; App Store page still missing.",
  "nextExpectedRunAt": "2026-08-03T08:00:00-05:00"
}
```

This can later be added per task in `tasks/index.json`.

## Relationship to workin On

Tasks should only surface there when they produce one of these:

- attention needed
- due soon
- recently changed
- blocked or failed

Routine healthy runs should not spam the board.

## Relationship to the web page

The web page should show:

- active tasks for an entity
- paused tasks
- blocked tasks
- last known task outcome later

The web page is the system of context.
`workin On` is the system of urgency.

## Task granularity rules

Prefer entry-level tasks when:

- one app has unique release behavior
- one backend needs its own health check
- one entity has missing links or stale metadata

Prefer cluster-level tasks when:

- multiple entries share the same dependency risk
- one report should summarize a whole product area

Prefer global tasks when:

- the whole index must refresh
- schema or publishing health must be checked

## Suggested next schema extension

Eventually extend each task object with:

- `targetEntityId`
- `lastRunAt`
- `lastOutcome`
- `lastOutcomeSummary`
- `nextExpectedRunAt`
- `boardVisibility`

Where `boardVisibility` can be:

- `always`
- `only_on_warning`
- `only_on_change`
- `hidden`

## Retirement rules

Retire a task when:

- the entity is removed
- the task is permanently replaced
- the task no longer has useful operational value

Pause a task instead when:

- the entity is still real
- the check is temporarily not worth running

That keeps historical intent visible.
