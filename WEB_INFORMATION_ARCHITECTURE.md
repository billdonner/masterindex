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

Add a compact row near the top:

- missing public links
- backend failures
- release-state changes
- tasks due soon

This should be the operational entry point.

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

## Future enhancement order

1. Add active task visibility to entity detail
2. Add top-level attention strip
3. Add missing-links filter
4. Add due-tasks filter
5. Add recent-changes filter
6. Add direct entity URLs

That order gives the best operational payoff.
