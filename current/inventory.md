# MasterIndex Inventory

As of Thursday, August 13, 2026.

## Scope

- Reviewed all local git repositories with 2026 commit activity under `/Users/billdonner/*` plus current 2026 experiment repos under `Documents/Codex/Experiments`.
- Treated all repositories as read-only.
- Queried App Store Connect live on August 13, 2026 through the ASC API (key `MN6H2P6385`). This replaces the retained August 2 snapshot; every `ascApps` entry now reflects the live query, including per-platform version states.
- Ignored older inactive repos unless directly tied to a 2026-active app, service, or shared package.
- Operations policy: every entity receives a verification pass every six hours and a full refresh daily through `tasks/index.json`. Agents must read `current/handoffs/index.json` before a cycle so a targeted instruction can change the next cycle's behavior without changing the inventory schema.

## Executive Summary

- App Store Connect shows 23 apps as of the 2026-08-13 live query, up from 19 on 2026-08-03. (PickleBrains, picklefortunes, Alities, Quackman, and the stray screenkr2 listings were removed from ASC in the 2026-08 cleanup and remain absent.)
- 20 ASC apps map to a local or GitHub repository. 3 do not: `MastPex IOS` and `MastPex Mac` (owner describes both as placeholders) and `GigStand` (app ID 428849240, a long-lived record at 1.020 READY_FOR_SALE).
- Three apps previously listed as unmatched were resolved on 2026-08-13 by reading `PRODUCT_BUNDLE_IDENTIFIER` out of each `project.yml`: `Zerver Monitor` → `~/server-monitor-ios`, `Oenora` → `~/oenora`, `SharedSpaceLab` → `~/SharedSpaceLab`. `SharedSpaceLab` is therefore no longer local-only; it does have an ASC record.
- 8 ASC records carry a macOS version, but only 4 correspond to a project that declares a macOS target: **Mallinbook, Pfoliolio, Screenker, SentiPods**. `Oenora` and `SharedSpaceLab` are `platform: iOS` only — their macOS records are phantoms that can never receive a build. `MastPex Mac` is a placeholder and `PickleFamilia` is on hold.
- Every macOS record sits at 1.0 `PREPARE_FOR_SUBMISSION`; none has been submitted. Primary category is unset on 7 of 8 and age rating on 7 of 8 — both hard submission gates.
- Mac-specific App Store collateral was written on 2026-08-13 for the four real Mac apps, kept deliberately distinct from their iPhone listings (`AppStore/mac/APP-STORE-MAC.md` in each repo; Pfoliolio via PR #15, since its CLAUDE.md forbids commits to `main`).
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
- MasterIndex reboot-readiness audit (2026-08-11): the canonical JSON files parse cleanly, every `entities[].id` has a key in `tasks/index.json`, and `current/handoffs/index.json` has no active directives.
- Local path availability audit (2026-08-11): `~/123words`, `~/bookmaker`, and `~/mallinbook` are retained from prior observed scans but did not resolve as local directories on this machine, so they are recorded as gaps rather than removed.
- MasterIndex instruction coverage audit (2026-08-05): 14 of 38 tracked repositories already have `AGENTS.md`; 24 require the standard injection.

## Current ASC Apps

### ASC apps mapped to active local repos

| ASC app | Bundle ID | ASC app ID | Repo | Local version/build | ASC state |
|---|---|---:|---|---|---|
| PickledBalls | `com.pickledballs.app` | `6762310890` | `~/pickledballs` | `1.0 (354)` on TestFlight | `IOS 1.0 PREPARE_FOR_SUBMISSION` (metadata complete; only App Privacy questionnaire remains) |
| Qross | `com.qross.app` | `6759799988` | `~/qross` | `0.2 (313)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| 100 Burfords | `com.billdonner.burfords` | `6766107636` | `~/100Burfords` | `1.1 (9)` | `IOS 1.0 READY_FOR_SALE` |
| Flasherz Kids | `com.billdonner.obo` | `6759509933` | `~/obo-ios` | `1.1 (47)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| Nagz | `com.nagz.app` | `6759530926` | `~/nagz-ios` | `1.4.0 (359)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| Cardz Studio | `com.billdonner.cardz-studio` | `6759624116` | `~/cardz-studio-ios` | `1.0 (10)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| KinFlash | `com.billdonner.kinflash` | `6762008872` | `~/kinflash` | `1.0.0 (62)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| workin On | `com.workinon.app` | `6762529338` | `~/workinon` | `0.9.1 (67)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` (TestFlight build 67 uploaded and processing 2026-08-09) |
| Famster | `com.famster.app` | `6763581385` | `~/famster-ios` | `1.0.0 (3)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| LtWatcher | `com.ltwatch.app` | `6764622141` | `~/clubwatch` | `0.1.0 (4)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` |
| 123 Words | `com.123words.app` | `6766975041` | `~/123words` | `1.11 (40)` | `IOS 1.11 READY_FOR_SALE; 1.12 draft` |
| SentiPods | `com.sentipods.app` | not surfaced in local scan | `~/sentipods` | `1.0 (15)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` (TestFlight build 14 uploaded) |
| Mallinbook | `com.mallinbook.app` | `6785245339` | `~/mallinbook` | `1.0 (14)` | `IOS + MAC_OS 1.0 PREPARE_FOR_SUBMISSION` (TestFlight build 13 on both platforms) |

### Confirmed gaps

- 3 ASC apps do not map to any repository (2026-08-13 live query): `MastPex IOS`, `MastPex Mac`, `GigStand`. The MastPex pair are placeholders per the owner; `GigStand` (app ID 428849240) predates this index and is at 1.020 READY_FOR_SALE.
- **Phantom macOS records.** `Oenora` and `SharedSpaceLab` each hold a `MAC_OS 1.0` record in ASC, but their `project.yml` files declare `platform: iOS` and nothing else. No build can be uploaded to either record. Add a Mac target or delete the macOS version record — until then any Mac store copy for them describes an app that cannot exist.
- **macOS submission gates.** Primary category is unset on 7 of the 8 macOS records (only Pfoliolio has Finance) and age rating on 7 of 8 (only Screenker is 4+). Mallinbook has no build attached to its macOS record. These are ASC web-UI fields; no written collateral clears them.
- `SentiPods` `README.md` claims the Mac bundle is `com.sentipods.mac`, but `project.yml` sets the `SentipodsMac` target to `com.sentipods.app` — one universal-purchase record, not two apps. The README is stale.
- `SentiPods` desktop screenshots existed locally (`AppStoreScreenshots/mac/`) but had never been uploaded to ASC, which is why the record showed zero. Committed 2026-08-13.
- `grubber-ios` is active locally but did not match a current ASC app.
- Retained repo paths `~/123words`, `~/bookmaker`, and `~/mallinbook` did not resolve locally during the August 11 reboot-readiness audit; keep their prior facts, but verify or restore the directories before doing local work against them. `~/mallinbook` was cloned to a scratch path on 2026-08-13 for the collateral pass and is still absent from the home directory.
- `picklefortunes` repo remains active locally but its ASC listing was deleted (2026-08 cleanup).

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
- `~/grubber` completed M4 and its fast live-update lane: APNs device registration/dispatch, `/api/v1/updates/recent`, `/api/v1/topics/{topic_id}/compare`, and the public live producer view at `https://bd-grubber.fly.dev/progress` are deployed. The fast and full analysis lanes serialize SQLite writes with a shared lock.
- Several existing repositories received MasterIndex agent-entry-point documentation updates. These confirm their ongoing connection to the shared index, but do not by themselves establish a product release or deployment change.
- `~/workinon` is now at local version `0.9.1 (67)`. TestFlight build `67` was uploaded on 2026-08-09 and entered App Store Connect processing. The build includes the bundled MasterIndex operational board, inline detail reveal in both the MasterIndex and Focus tabs, and shorter recent-change titles.
- `~/masterindex` regenerated the `workin On` feed so recent-change cards keep concise titles such as `Qross changed` while the body records the latest git commit subject when available, falling back to the last-modified date when the repo is unavailable.

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
- App Store Connect was not re-queried during this refresh; the inventory remains from the August 2 live query. SentiPods is mapped to `~/sentipods`, but its ASC app ID remains unsurfaced in the local scan.
- The server-side cause of the observed `grubber /status` hang is not yet confirmed.
