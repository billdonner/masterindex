# Web Information Architecture

As of Sunday, August 2, 2026.

## Goal

The web page is the full exploration and drill-down surface for `MasterIndex`.

It should support:

- browsing
- search
- filtering
- recency-first review
- link validation
- operational context
- agent task visibility

## Primary user modes

### 1. Triage mode

The user wants to know what changed or what needs attention.

Needs:

- recent changes
- missing public links
- backend issues
- due tasks

### 2. Mapping mode

The user wants to understand relationships.

Needs:

- clusters
- dependencies
- shared services
- repo and app relationships

### 3. Entry mode

The user wants one thing in detail.

Needs:

- one entity page or panel
- links
- release state
- task list
- recent modification info

## Recommended page structure

### Top level

1. Summary header
2. Attention strip
3. Main entity browser
4. Cluster browser
5. Shared services section
6. Repo table

## Section design

### Summary header

Current design already fits this fairly well.

Keep:

- total ASC apps
- mapped apps
- unmatched apps
- active repos

Add later:

- entries with public links
- entries missing public links
- tasks due today
- entries changed in last 7 days

### Attention strip

Implemented. The strip renders `current/attention.json` directly — the same
artifact `workin On` consumes — so the two surfaces cannot disagree about what
needs attention. See `ATTENTION_BOARD.md`.

Each card shows priority, lane, a short headline, clamped context, and the
concrete next action. Cards concerning an entity select that entity in the
detail panel and update the URL to `?entity=<id>`.

The strip deliberately shows only open gaps, overdue tasks, and unreviewed
changes. Conditions that are correct by design are suppressed, and the
suppressed count is displayed so an empty strip reads as trustworthy rather
than broken.

### Main entity browser

This is the central list.

Default sort:

- most recently modified first

Filters:

- kind
- status
- cluster
- has website
- has App Store page
- has active tasks
- missing links

Search:

- name
- repo
- bundle id
- links
- dependencies

### Detail panel or entity page

Each entity should expose:

- name
- kind
- status
- last modified
- repo
- bundle id
- release signal
- public links
- dependencies
- notes
- active tasks
- task history later

Recommended future addition:

- `why this matters` field for high-value entries

### Cluster browser

Each cluster should show:

- summary
- maturity
- highlights
- watchpoints
- entries in cluster
- backends in cluster
- public links in cluster

### Shared services section

Each service card should show:

- public URL
- repo
- consumer count
- consumer list
- task status

### Repo table

Should remain sortable and default to most recent first.

Potential extra columns later:

- mapped entity count
- public link present
- active task count

## Recommended navigation model

### Level 1

- Overview
- Entities
- Clusters
- Services
- Tasks
- Repos

### Level 2

For each entity:

- Summary
- Links
- Dependencies
- Tasks
- Change notes

## Recommended URLs

When the browser becomes hosted, support:

- `/`
- `/?entity=pickledballs-app`
- `/?cluster=Nagz`
- `/?filter=missing-links`
- `/?filter=recent`

These will be easier for agents to generate than fragment-only links.

## Agent-facing expectations

Agents should be able to safely link users to:

- one entity
- one cluster
- one filter view

Without reconstructing the whole page.

## Enhancement status

Done:

1. Active task visibility in entity detail
2. Top-level attention strip, driven by the shared attention board
3. Missing-links filter
4. Direct entity URLs (`?entity=<id>`, with cluster and filter parameters)

Still open:

5. Due-tasks filter — blocked until task runs are recorded in
   `current/attention-state.json`; until then no task has a real due state
6. Recent-changes filter — most useful once the review watermark is in routine
   use, so the filter can mean "since I last looked" rather than "last 7 days"
