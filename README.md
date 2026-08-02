# IndexMaker Hub

GitHub-first package for sharing the current cross-app index with other agents and machines.

## Purpose

This bundle is meant to become the canonical machine-readable index until a non-GitHub distribution path is needed.

Use GitHub for:

- shared storage
- version history
- machine-to-machine access
- raw JSON fetches by agents
- static site hosting via GitHub Pages if desired

## Recommended repository shape

```text
indexmaker-hub/
  README.md
  AGENTS.md
  GITHUB_PUBLISHING.md
  WORKINON_BOARD_SCHEMA.md
  WEB_INFORMATION_ARCHITECTURE.md
  TASK_LIFECYCLE.md
  current/
    index.json
    inventory.md
  tasks/
    index.json
    templates/
      entry-task.template.json
  site/
    index.html
    app.js
    styles.css
  snapshots/
    2026-08-01/
      index.json
      inventory.md
```

## What agents should use

Primary machine-readable source:

- `current/index.json`

Human-readable source:

- `current/inventory.md`

Task-routing source:

- `tasks/index.json`

Browsable source:

- `site/index.html`

Operational design references:

- `WORKINON_BOARD_SCHEMA.md`
- `WEB_INFORMATION_ARCHITECTURE.md`
- `TASK_LIFECYCLE.md`

## Publishing model

Recommended near-term flow:

1. Keep this folder in a dedicated GitHub repo.
2. Commit updates every refresh cycle.
3. Let other agents read the repo directly or consume the raw JSON URL.
4. Optionally publish `site/` with GitHub Pages.

See `GITHUB_PUBLISHING.md` for the exact raw URL contract to standardize across machines.

## Six-hour refresh plan

Target cadence:

- every 6 hours

Refresh responsibilities:

- re-scan current app and repo state
- refresh `current/index.json`
- refresh `current/inventory.md`
- preserve `tasks/index.json` unless task definitions intentionally change
- refresh `snapshots/YYYY-MM-DD/` if you want dated freezes
- keep `site/` rendering against `current/index.json`

## Notes

- This bundle is intentionally static and dependency-free.
- The site is data-driven and does not require a build step.
- App Store Connect access was available for the initial August 1, 2026 inventory, but future refresh runs should always report when ASC access is unavailable.
- The task registry is intentionally separate from `current/index.json` so housekeeping agents can evolve without destabilizing the core inventory schema.
- Verified external public links should be captured whenever available, including websites, service URLs, and public App Store pages.
