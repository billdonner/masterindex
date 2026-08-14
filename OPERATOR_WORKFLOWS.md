# Portable Operator Workflows

This document standardizes the *shape* of common developer workflows across
the labs and apps tracked by MasterIndex.

## Important boundary

Codex command approvals are managed by the host and may be scoped to a
machine, workspace, or session. They cannot be made universal by committing a
repository file. Do not represent this document as a bypass for managed safety
controls.

## Portable pattern

Keep repeatable operations as short, reviewed repository scripts. Each script
should have one bounded purpose, a clear name, and a non-destructive default.
Suggested names:

- `scripts/check-local.sh` — run the local verification lane.
- `scripts/build-device.sh` — build a signed Debug app for a selected device.
- `scripts/install-connected-devices.sh` — install a previously built app on
  explicitly connected test devices.
- `scripts/sync-github.sh` — report status and push the current branch only
  after tests pass.

When Codex offers to remember approval, approve the script prefix rather than
an unrestricted interpreter or a broad command family. That creates a
repeatable low-friction path while retaining clear boundaries around deletion,
credentials, releases, and unfamiliar operations.

## Required behavior for agent handoffs

Agents should:

1. Prefer an existing repository workflow script over constructing a new
   ad-hoc command.
2. State whether a workflow is local-only, modifies a physical test device,
   or publishes externally.
3. Keep GitHub pushes and App Store/TestFlight release steps separate.
4. Record newly established workflow scripts in the relevant entity notes and
   keep this guidance accurate as tooling changes.
