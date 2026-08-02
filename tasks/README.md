# Task Registry

This folder is for recurring or agentic work assigned to specific inventory entries.

## Purpose

Use `tasks/index.json` to declare periodic work without polluting the core inventory data.

Examples:

- health checks for live services
- release-status checks for specific apps
- dependency drift checks for selected repos
- metadata cleanup tasks
- reporting or summarization tasks tied to one cluster
- public-link discovery and verification tasks

## Rules

- Target entries by `entities[].id` from `current/index.json`
- Keep task definitions stable and explicit
- Prefer appending new tasks over mutating old tasks without reason
- Mark inactive tasks as paused instead of deleting them unless they are obsolete

## Main file

- `index.json` contains all current task assignments

## Template

- `templates/entry-task.template.json` is the reusable schema example for one task
