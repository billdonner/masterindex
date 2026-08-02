# workin On Board Schema

As of Sunday, August 2, 2026.

## Goal

Show `MasterIndex` in `workin On` as an operational dashboard, not as a full browsing experience.

The web page remains the deep-dive surface.

`workin On` should answer:

- what needs attention now
- what changed recently
- what tasks are due soon
- what public links or release signals are still missing

## Source inputs

- `current/index.json`
- `tasks/index.json`

Optional later inputs:

- failure logs from task runs
- per-entry stale-age calculations
- service health snapshots

## Board model

Use a small number of predictable card types.

### 1. Attention cards

One card per entry that needs action.

Examples:

- missing public link
- release state changed
- backend health check failed
- ambiguity unresolved
- stale entry needing refresh

Suggested fields:

```json
{
  "id": "attention-pickledballs-app-missing-public-appstore-link",
  "type": "attention",
  "entityId": "pickledballs-app",
  "title": "PickledBalls missing public App Store page",
  "body": "Website exists, but no verified public App Store page is recorded yet.",
  "priority": "medium",
  "tags": ["links", "app-store", "pickledballs"],
  "deepLink": "site/index.html#pickledballs-app"
}
```

### 2. Due-soon task cards

One card per task that is due in the next execution window.

Examples:

- daily release check due soon
- weekly link verification due tomorrow
- six-hour backend check due now

Suggested fields:

```json
{
  "id": "due-nagzerver-health-check",
  "type": "due-task",
  "entityId": "nagzerver-backend",
  "taskId": "nagzerver-health-check",
  "title": "nagzerver health check due",
  "body": "Shared backend health check is due in this six-hour cycle.",
  "priority": "high",
  "tags": ["backend", "health", "due"],
  "deepLink": "site/index.html#nagzerver-backend"
}
```

### 3. Recent-change cards

One card per entry changed recently.

Examples:

- `KinFlash` changed July 31, 2026
- `grubber` changed July 31, 2026

Suggested fields:

```json
{
  "id": "recent-grubber-service",
  "type": "recent-change",
  "entityId": "grubber-service",
  "title": "grubber changed recently",
  "body": "Last modified July 31, 2026.",
  "priority": "low",
  "tags": ["recent", "grubber"],
  "deepLink": "site/index.html#grubber-service"
}
```

### 4. Summary cards

Low-cardinality overview items pinned near the top.

Examples:

- 12 unmatched ASC apps
- 5 live services
- 4 entries missing public links

Suggested fields:

```json
{
  "id": "summary-public-link-gaps",
  "type": "summary",
  "title": "Public link gaps",
  "body": "Several entries still lack a verified website or App Store page.",
  "priority": "low",
  "tags": ["summary", "links"]
}
```

## Recommended lanes

If `workin On` supports grouping, use these lanes:

1. `Needs Attention`
2. `Due Soon`
3. `Recently Changed`
4. `Summaries`

If not, interleave by priority with this sort order:

1. high priority attention
2. due-soon tasks
3. medium priority attention
4. recent changes
5. summaries

## Priority rules

### High

- backend unreachable
- release state changed unexpectedly
- required public link disappeared
- task failure repeated

### Medium

- missing public link
- unresolved ambiguity on a high-value entry
- stale metadata on active app or backend

### Low

- recent change notice
- summary counts
- low-risk cleanup suggestions

## Deep link pattern

Every board item should point back to the web browser view for detail.

Preferred logical target:

- `site/index.html#<entityId>`

If the future web page uses query parameters instead:

- `site/index.html?entity=<entityId>`

## Minimum viable feed

Start with only:

- missing public links
- due tasks
- recent changes in the last 7 days
- backend failures

That is enough to make `workin On` genuinely useful without overwhelming it.

## What should not go into workin On

- the full repository table
- all cluster notes
- all gaps at once
- long narrative descriptions
- every entity regardless of urgency

That belongs on the web page.
