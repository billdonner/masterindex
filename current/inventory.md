# MasterIndex Inventory

As of Monday, August 3, 2026.

## Scope

- Reviewed all local git repositories with 2026 commit activity under `/Users/billdonner/*` plus current 2026 experiment repos under `Documents/Codex/Experiments`.
- Treated all repositories as read-only.
- Retained the App Store Connect inventory from the live query on August 2, 2026; ASC was not re-queried during this refresh.
- Ignored older inactive repos unless directly tied to a 2026-active app, service, or shared package.

## Executive Summary

- App Store Connect currently shows 19 apps (2026-08-03 refresh; PickleBrains, picklefortunes, Alities, Quackman, and the stray screenkr2 listings were removed from ASC in the 2026-08 cleanup).
- 13 ASC apps map cleanly to currently active local repositories.
- 6 ASC apps are visible in ASC but do not have a clearly corresponding 2026-active local repository in this scan.
- Mallinbook was resolved on 2026-08-02: its repo is `~/mallinbook` (renamed 2026-08-01 from `bookmaker-app`, which hid it from the original scan). Multiplatform macOS + iOS; the `~/bookmaker` Python engine remains as read-only reference.
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
| PickledBalls | `com.pickledballs.app` | `6762310890` | `~/PickledBalls` | `1.0 (354)` on TestFlight | `IOS 1.0 PREPARE_FOR_SUBMISSION` (metadata complete; only App Privacy questionnaire remains) |
| Qross | `com.qross.app` | `6759799988` | `~/qross` | `0.2 (313)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| 100 Burfords | `com.billdonner.burfords` | `6766107636` | `~/100Burfords` | `1.1 (9)` | `IOS 1.0 READY_FOR_SALE` |
| Flasherz Kids | `com.billdonner.obo` | `6759509933` | `~/obo-ios` | `1.1 (47)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| Nagz | `com.nagz.app` | `6759530926` | `~/nagz-ios` | `1.4.0 (359)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| Cardz Studio | `com.billdonner.cardz-studio` | `6759624116` | `~/cardz-studio-ios` | `1.0 (10)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| KinFlash | `com.billdonner.kinflash` | `6762008872` | `~/kinflash` | `1.0.0 (62)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| workin On | `com.workinon.app` | `6762529338` | `~/workinon` | `0.9.1 (52)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| Famster | `com.famster.app` | `6763581385` | `~/famster-ios` | `1.0.0 (3)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| LtWatcher | `com.ltwatch.app` | `6764622141` | `~/clubwatch` | `0.1.0 (4)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| 123 Words | `com.123words.app` | `6766975041` | `~/123words` | `1.11 (40)` | `IOS 1.11 READY_FOR_SALE; 1.12 draft` |
| SentiPods | `com.sentipods.app` | not surfaced in local scan | `~/sentipods` | `1.0 (15)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` (TestFlight build 14 uploaded) |
| Mallinbook | `com.mallinbook.app` | `6785245339` | `~/mallinbook` | `1.0 (14)` | `IOS + MAC_OS 1.0 PREPARE_FOR_SUBMISSION` (TestFlight build 13 on both platforms) |

### Confirmed gaps

- 6 ASC apps did not map cleanly to an active local repository (2026-08-03 refresh): MastPex IOS, MastPex Mac, PickleFamilia, Screenker, Zerver Monitor, amenbeats.
- `grubber-ios` is active locally but did not match a current ASC app.
- `SentiPods` is mapped to `~/sentipods` (`com.sentipods.app`), based on the local project's alignment to its ASC 1.0 record. Its ASC app ID was not surfaced in the local scan. `MastPex IOS` / `MastPex Mac` are also new in ASC with no local repo identified yet.
- `picklefortunes` repo remains active locally but its ASC listing was deleted (2026-08 cleanup).
- `Zerver Monitor` exists in ASC but only the backend/service repo was present in the local scan.
- `SharedSpaceLab` is local-only and not in ASC.

## Shared Services

- `bd-nagzerver.fly.dev` from `~/nagzerver`
- `bd-clubsync.fly.dev` from `~/clubsync`
- `bd-cardzerver.fly.dev` from `~/card-server`
- `bd-grubber.fly.dev` from `~/grubber`
- `bd-server-monitor.fly.dev` from `~/server-monitor`
- `api.famster.app` as a confirmed backend domain without a corresponding repo found in this scan

## Changes Observed In This Refresh

- `~/qross` is actively developed on branch `palette-tournament`; its latest observed commit updates tournament palettes and the Coastal Dusk brand color.
- `~/sentipods` is a new Grubber-cluster client that connects to `https://bd-grubber.fly.dev/api/v1` and provides podcast, episode, transcript, and search surfaces.
- `~/sentipods` completed a live smoke test and is now at local version `0.1.0 (8)`; its ASC mapping remains unverified in this refresh.
- `~/sentipods` received a UI and resilience pass and is now at local version `0.1.0 (12)` following its TestFlight upload. During its live smoke test, `grubber`'s `/shows` endpoint responded while `/status` hung; the client safely loads the former first and treats status metadata as best effort.
- `~/sentipods` is now at local version `1.0 (15)`, aligned with its ASC 1.0 PREPARE_FOR_SUBMISSION record. TestFlight build `14`, including its new icon, is uploaded.
- `~/grubber` completed M2 of its pods-versus-news analysis pipeline: idempotent embeddings, topic clustering, daily rollups, and two new read endpoints for trending topics and topic detail.
- `~/grubber` completed M3: LLM topic labeling, podcast-versus-news claim comparison, and daily digest generation. The producer-side LLM work has a `$5` soft and `$10` hard spending cap per UTC day; digest reads are available as markdown or JSON.
- Several existing repositories received MasterIndex agent-entry-point documentation updates. These confirm their ongoing connection to the shared index, but do not by themselves establish a product release or deployment change.

## Public Links

- PickledBalls website from local docs: `https://pickledballs.billdonner.com`
- Famster backend domain from local docs: `https://api.famster.app`
- grubber service: `https://bd-grubber.fly.dev`
- nagzerver: `https://bd-nagzerver.fly.dev`
- clubsync: `https://bd-clubsync.fly.dev`
- card-server: `https://bd-cardzerver.fly.dev`
- server-monitor: `https://bd-server-monitor.fly.dev`
- Mallinbook repo (public GitHub): `https://github.com/billdonner/mallinbook`
- Verified App Store page found during the August 2, 2026 link pass:
  - 100 Burfords: `https://apps.apple.com/ca/app/100-burfords/id6766107636`
  - 100 Burfords site (GitHub Pages, privacy policy): `https://billdonner.github.io/100Burfords/`

For the other mapped ASC apps, no clearly public App Store page was verified in the web pass. That is consistent with most of them still being in `PREPARE_FOR_SUBMISSION`.

Rule going forward: if any entity has a verified external public link, it should be included in the shared index.

## Main Ambiguities

- `card-engine` and `card-server` overlap conceptually.
- `PickledBalls` is still the live ASC name even though docs describe a rebrand path toward PickleNagz.
- `Flasherz Kids` docs and `project.yml` disagree on some build text; `project.yml` was treated as more current.
- App Store Connect was not re-queried during this refresh; the inventory remains from the August 2 live query, so Sentipods remains an unverified ASC mapping gap.
- The server-side cause of the observed `grubber /status` hang is not yet confirmed.
