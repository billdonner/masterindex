# MasterIndex Inventory

As of Sunday, August 2, 2026.

## Scope

- Reviewed all local git repositories with 2026 commit activity under `/Users/billdonner/*` plus current 2026 experiment repos under `Documents/Codex/Experiments`.
- Treated all repositories as read-only.
- Queried App Store Connect live, using the existing local API key, to inventory current apps visible in ASC on August 2, 2026.
- Ignored older inactive repos unless directly tied to a 2026-active app, service, or shared package.

## Executive Summary

- App Store Connect currently shows 23 apps.
- 11 ASC apps map cleanly to currently active local repositories.
- 12 ASC apps are visible in ASC but do not have a clearly corresponding 2026-active local repository in this scan.
- Default browsing order should normally be most recently modified first.
- Strongest active clusters:
  - `PickledBalls` + `nagzerver` + `clubsync` + `CourtScheduler` + `server-monitor` (SharedAI unlinked from v1.0, returns with the Instructor tier)
  - `Qross` + `card-server` + `qross-data` + `card-studio`
  - `Nagz` + `nagzerver` + `nagz-web` + `nagz-ai` + `workinon` + `workinon-mcp`
  - `Flasherz Kids` + `card-server`
  - `LtWatcher` + `clubsync` + `nagzerver`
- Current Codex experiments are local-only:
  - `ConversationLab`
  - `CoordinationLab`
  - `SharedSpaceLab`

## Current ASC Apps

### ASC apps mapped to active local repos

| ASC app | Bundle ID | ASC app ID | Repo | Local version/build | ASC state |
|---|---|---:|---|---|---|
| PickledBalls | `com.pickledballs.app` | `6762310890` | `~/PickledBalls` | `1.0 (354)` on TestFlight | `IOS 1.0 PREPARE_FOR_SUBMISSION` (metadata complete; support-page deploy + App Privacy remain) |
| Qross | `com.qross.app` | `6759799988` | `~/qross` | `0.2 (313)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| 100 Burfords | `com.billdonner.burfords` | `6766107636` | `~/100Burfords` | `1.0 (7)` | `IOS 1.0 READY_FOR_SALE` |
| Flasherz Kids | `com.billdonner.obo` | `6759509933` | `~/obo-ios` | `1.1 (47)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| Nagz | `com.nagz.app` | `6759530926` | `~/nagz-ios` | `1.4.0 (359)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| Cardz Studio | `com.billdonner.cardz-studio` | `6759624116` | `~/cardz-studio-ios` | `1.0 (10)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| KinFlash | `com.billdonner.kinflash` | `6762008872` | `~/kinflash` | `1.0.0 (62)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| workin On | `com.workinon.app` | `6762529338` | `~/workinon` | `0.9.1 (52)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| Famster | `com.famster.app` | `6763581385` | `~/famster-ios` | `1.0.0 (3)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| LtWatcher | `com.ltwatch.app` | `6764622141` | `~/clubwatch` | `0.1.0 (4)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| picklefortunes | `com.picklefortunes.app` | `6775271321` | `~/picklefortunes` | `1.0.0 (10)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |

### Confirmed gaps

- 12 ASC apps did not map cleanly to an active local repository in this scan.
- `grubber-ios` is active locally but did not match a current ASC app.
- `Zerver Monitor` exists in ASC but only the backend/service repo was present in the local scan.
- `SharedSpaceLab` is local-only and not in ASC.

## Shared Services

- `bd-nagzerver.fly.dev` from `~/nagzerver`
- `bd-clubsync.fly.dev` from `~/clubsync`
- `bd-cardzerver.fly.dev` from `~/card-server`
- `bd-grubber.fly.dev` from `~/grubber`
- `bd-server-monitor.fly.dev` from `~/server-monitor`
- `api.famster.app` as a confirmed backend domain without a corresponding repo found in this scan

## Public Links

- PickledBalls website from local docs: `https://pickledballs.billdonner.com`
- Famster backend domain from local docs: `https://api.famster.app`
- grubber service: `https://bd-grubber.fly.dev`
- nagzerver: `https://bd-nagzerver.fly.dev`
- clubsync: `https://bd-clubsync.fly.dev`
- card-server: `https://bd-cardzerver.fly.dev`
- server-monitor: `https://bd-server-monitor.fly.dev`
- Verified App Store page found during the August 2, 2026 link pass:
  - 100 Burfords: `https://apps.apple.com/ca/app/100-burfords/id6766107636`

For the other mapped ASC apps, no clearly public App Store page was verified in the web pass. That is consistent with most of them still being in `PREPARE_FOR_SUBMISSION`.

Rule going forward: if any entity has a verified external public link, it should be included in the shared index.

## Main Ambiguities

- `card-engine` and `card-server` overlap conceptually.
- `PickledBalls` is still the live ASC name even though docs describe a rebrand path toward PickleNagz.
- `Flasherz Kids` docs and `project.yml` disagree on some build text; `project.yml` was treated as more current.
