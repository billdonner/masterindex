# MasterIndex Inventory

As of Wednesday, August 6, 2026.

## Scope

- Reviewed all local git repositories with 2026 commit activity under `/Users/billdonner/*` plus current 2026 experiment repos under `Documents/Codex/Experiments`.
- Treated all repositories as read-only.
- Refreshed the full 20-app App Store Connect inventory from the live ASC API on August 6, 2026.
- Ignored older inactive repos unless directly tied to a 2026-active app, service, or shared package.

## Executive Summary

- App Store Connect currently shows 20 apps from the August 6 live API pull. PickleBrains, picklefortunes, Alities, Quackman, and the stray screenkr2 listings remain removed from ASC.
- 18 ASC apps map cleanly to currently active local repositories.
- 2 ASC apps are visible in ASC but do not have a clearly corresponding 2026-active local repository in this scan.
- Mallinbook was resolved on 2026-08-02: its repo is `~/mallinbook` (renamed 2026-08-01 from `bookmaker-app`, which hid it from the original scan). Multiplatform macOS + iOS; the `~/bookmaker` Python engine remains as read-only reference.
- AmenBeats was resolved on 2026-08-04: its repo is `~/drumbeats` (App Store name ≠ repo name hid it from earlier scans). A Bill + Jim SwiftUI drum-machine app; Jim (`@jrforster`) added as full admin, now a shared build.
- MastPex was resolved on 2026-08-07: its iOS and macOS ASC records map to `~/Documents/Codex/2026-08-02/masterindex-explorer`, the native read-only explorer for compatible MasterIndex files.
- Default browsing order should normally be most recently modified first.
- Strongest active clusters:
  - `PickledBalls` + `nagzerver` + `clubsync` + `CourtScheduler` (SharedAI unlinked from v1.0, returns with the Instructor tier; server-monitor moved to the Infrastructure cluster)
  - `Qross` + `card-server` + `qross-data` + `card-studio`
  - `Nagz` + `nagzerver` + `nagz-web` + `nagz-ai` + `workinon` + `workinon-mcp`
  - `Flasherz Kids` + `card-server`
  - `LtWatcher` + `clubsync` + `nagzerver`
- Current Codex experiments are local-only:
  - `ConversationLab`
  - `CoordinationLab`
  - `SharedSpaceLab`
- `adspill` (new cluster): a Bill + Jim (`@jrforster`) private research collaboration on selling excess advertising capacity, split into Project 1 (auction/exchange modeling sandbox, Bill's track) and Project 2 (self-serve create-and-sell for long-tail local video ads, Jim's track). Lab/scoping stage.
- `local-model-lab` (standalone, added 2026-08-04): MLX local-model evaluation lab at `~/mlxsrv/local-model-lab`, benchmarking on-device quantized models (and OpenAI GPT-5 for comparison) against an exported 177k-question Qross corpus snapshot. No dependency on the Qross app/repos — the corpus is just benchmark data.
- `Oenora` is an active local iOS technical spike at `~/oenora`: camera/photo-library capture, on-device OCR, local restart-safe persistence, candidate review/correction, and cellar history all work without data leaving the device. Its August 8 commits contain the Xcode project, Swift package, tests, decision records, product specification, app icon, launch copy, and local ASC tooling. No ASC record, deployment, or public product link has been observed; the name remains provisional pending clearance.

## Current ASC Apps

### ASC apps mapped to active local repos

| ASC app | Bundle ID | ASC app ID | Repo | Local version/build | ASC state | Public link |
|---|---|---:|---|---|---|---|
| PickledBalls | `com.pickledballs.app` | `6762310890` | `~/PickledBalls` | `1.0 (354)` on TestFlight | `IOS 1.0 PREPARE_FOR_SUBMISSION` (metadata complete; only App Privacy questionnaire remains) | `https://pickledballs.billdonner.com` |
| Qross | `com.qross.app` | `6759799988` | `~/qross` | build `389` uploaded | `IOS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.github.io/qross/` |
| 100 Burfords | `com.billdonner.burfords` | `6766107636` | `~/100Burfords` | `1.1 (9)` | `IOS 1.0 READY_FOR_SALE` | Verified website and App Store link in `index.json` |
| Flasherz Kids | `com.billdonner.obo` | `6759509933` | `~/obo-ios` | build `47` expired | `IOS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.github.io/obo-ios/` |
| Nagz | `com.nagz.app` | `6759530926` | `~/nagz-ios` | build `359` expired | `IOS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.github.io/nagz/` |
| Cardz Studio | `com.billdonner.cardz-studio` | `6759624116` | `~/cardz-studio-ios` | `1.0 (10)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` | No verified public link |
| KinFlash | `com.billdonner.kinflash` | `6762008872` | `~/kinflash` | build `65` uploaded | `IOS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.com/apps/kinflash/` |
| workin On | `com.workinon.app` | `6762529338` | `~/workinon` | build `65` uploaded | `IOS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.github.io/workinon/` |
| Famster | `com.famster.app` | `6763581385` | `~/famster-ios` | build `3` expired | `IOS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.com/apps/famster/` |
| LtWatcher | `com.ltwatch.app` | `6764622141` | `~/clubwatch` | build `2` expired | `IOS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.com/apps/ltwatcher/` |
| 123 Words | `com.123words.app` | `6766975041` | `~/123words` | build `41` uploaded | versions `1.0`, `1.1`, and `1.11` ready for distribution; `1.12` in preparation | `https://billdonner.github.io/123words/` |
| AmenBeats | `com.billdonner.drumbeats` | `6778510642` | `~/drumbeats` | build `7` uploaded | `IOS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.com/apps/amenbeats/` |
| MastPex IOS | `com.billdonner.mastpex` | `6797321392` | `~/Documents/Codex/2026-08-02/masterindex-explorer` | build `1` uploaded | `IOS 1.0 PREPARE_FOR_SUBMISSION` | No verified public link |
| MastPex Mac | `com.billdonner.mastpex.mac` | `6797321653` | `~/Documents/Codex/2026-08-02/masterindex-explorer` | build `1` uploaded | `MAC_OS 1.0 PREPARE_FOR_SUBMISSION` | No verified public link |
| SentiPods | `com.sentipods.app` | `6797132650` | `~/sentipods` | build `15` uploaded | `IOS + MAC_OS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.com/apps/sentipods/` |
| Zerver Monitor | `com.billdonner.ZerverMonitor` | `6759637400` | `~/server-monitor-ios` | build `4` expired | `IOS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.github.io/server-monitor-ios/` |
| Mallinbook | `com.mallinbook.app` | `6785245339` | `~/mallinbook` | build `18` uploaded | `IOS + MAC_OS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.com/apps/mallinbook/` |
| Oliofolio Portfolio* | `com.pfolio.app` | `6797993806` | `~/pfolio-app` | macOS `28` VALID; iOS `6` | `IOS + MAC_OS 1.0 PREPARE_FOR_SUBMISSION` | `https://billdonner.com/apps/oliopfolio/` |

### Confirmed gaps

- The two ASC records without a matched active local repository remain browseable entities: PickleFamilia and Screenker. The August 6 ASC pull supplied their real bundle IDs, platform status, and build metadata. MastPex was resolved on 2026-08-07 to `~/Documents/Codex/2026-08-02/masterindex-explorer`.
- PickleFamilia has a verified public product page at `https://billdonner.github.io/picklefamilia-ios/`; its source repository is still unverified.
- Screenker is wired to Qross, 123 Words, and 100 Burfords as their observed shared App Store screenshot-composition workflow. It also has a verified public product page at `https://billdonner.github.io/screenker/`, but its standalone local source repository remains unverified.
- Zerver Monitor is now resolved to `~/server-monitor-ios`: its `project.yml` declares the exact ASC bundle ID, and it contains the iOS, watchOS, widget, and web-support sources. Its public GitHub Pages site is `https://billdonner.github.io/server-monitor-ios/`.
- MasterIndex policy: every ASC app has an entity. A verified public website or App Store page is stored in `links`; when neither is verified, the entity's `release` field explicitly records its known release or development status.
- `grubber-ios` is active locally but did not match a current ASC app.
- `SentiPods` is mapped to `~/sentipods` (`com.sentipods.app`), based on the local project's alignment to its ASC 1.0 record. Its ASC app ID was not surfaced in the local scan.
- `picklefortunes` is retired: its ASC listing was deleted in the 2026-08 cleanup, its repository is archived, and its reusable kit is retained in PickledBalls.
- `SharedSpaceLab` is local-only and not in ASC.

## Shared Services

- `bd-nagzerver.fly.dev` from `~/nagzerver`
- `bd-clubsync.fly.dev` from `~/clubsync`
- `bd-cardzerver.fly.dev` from `~/card-server`
- `bd-grubber.fly.dev` from `~/grubber`
- `bd-server-monitor.fly.dev` from `~/server-monitor`
\* The name went Oliopfolio -> Oliofolio (dropping the p, which is what Steve kept
mistyping). **"Oliofolio" turns out to be taken on the App Store by another account,
as is "Olio Folio"** — so the store listing is "Oliofolio Portfolio", the nearest free
variant, pending confirmation. The app itself shows the short "Oliofolio" on device.
Privacy policy is live at https://billdonner.github.io/pfolio-app/privacy.html and
attached to the ASC record.

- `bd-pfolio.fly.dev` from `~/pfolio` (portfolio tracker API; shares bd-postgres)
- `api.famster.app` as a confirmed backend domain without a corresponding repo found in this scan

## Fly.io Operations and Cost Reporting

MasterIndex now records Fly deployment status under `flyOperations` in `current/index.json`. The August 6 authenticated CLI check observed deployed cardzerver, nagzerver, grubber, server-monitor, and pfolio apps. `bd-clubsync` did not appear in the personal app list (while `bd-clubsync-db` did), so that ownership/app-name mapping remains a recorded gap. No billing or usage amount was available from the observed CLI surface; cost status is explicitly `unavailable` and no projection is fabricated.

## Collaborators

Unified watch over the people Bill co-works with, refreshed every 6h by the
`collaborator-activity-watch` task (`tasks/index.json`). Canonical data lives in
`current/index.json` under `collaborators[]`; this table is presentation only.

| Collaborator | Role | Repo | Last activity | Awaiting Bill |
|---|---|---|---|---|
| Jim Forster (`@jrforster`) | dev collaborator | `billdonner/adspill`, `billdonner/drumbeats` | adspill: ball in Jim's court (issue #2). drumbeats (AmenBeats): joined as admin 2026-08-04, feature work starting | No |
| Carol (`@cuchif`) | dev collaborator | `billdonner/qross` | 3 open PRs from Carol (#172/#173/#174, 07-25/26) | **Yes — 3 PRs need review** |
| Steve Gould | pfolio end-user / stakeholder | `billdonner/pfolio`, `billdonner/pfolio-app` | His UX work is merged (pfolio-app #5, reviewed hands-on and approved 2026-08-07) and all four of his PRs were closed as superseded on 2026-08-08, each with a comment tracing where the work landed. His classification backlog moved to pfolio issue #7. | **No — nothing of his is waiting on Bill** |

- **Reconcile:** Steve is mapped to `pfolio` as its end-user; the repo's code
  collaborator is `@rachelelise`, not a Steve GitHub identity. Decide whether
  Steve should be tracked as a stakeholder only (current) or given his own
  GitHub handle.
- Scope is GitHub only (commits, PRs, issues); no email inbox is scanned.

## Changes Observed In This Refresh

- `~/qross` is actively developed on branch `palette-tournament`; its latest observed commit updates tournament palettes and the Coastal Dusk brand color.
- `~/sentipods` is a new Grubber-cluster client that connects to `https://bd-grubber.fly.dev/api/v1` and provides podcast, episode, transcript, and search surfaces.
- `~/sentipods` completed a live smoke test and is now at local version `0.1.0 (8)`; its ASC mapping remains unverified in this refresh.
- `~/sentipods` received a UI and resilience pass and is now at local version `0.1.0 (12)` following its TestFlight upload. During its live smoke test, `grubber`'s `/shows` endpoint responded while `/status` hung; the client safely loads the former first and treats status metadata as best effort.
- `~/sentipods` is now at local version `1.0 (15)`, aligned with its ASC 1.0 PREPARE_FOR_SUBMISSION record. TestFlight build `14`, including its new icon, is uploaded.
- `~/grubber` completed M2 of its pods-versus-news analysis pipeline: idempotent embeddings, topic clustering, daily rollups, and two new read endpoints for trending topics and topic detail.
- `~/grubber` completed M3: LLM topic labeling, podcast-versus-news claim comparison, and daily digest generation. The producer-side LLM work has a `$5` soft and `$10` hard spending cap per UTC day; digest reads are available as markdown or JSON.
- `~/grubber` completed M4 and its fast live-update lane: APNs device registration/dispatch, `/api/v1/updates/recent`, `/api/v1/topics/{topic_id}/compare`, and the public live producer view at `https://bd-grubber.fly.dev/progress` are deployed. The Mac producer has text, audio, news, fast-analysis, and full-analysis launchd lanes; the analysis lanes serialize SQLite writes with a shared lock.
- `~/kinflash` expanded the native Mac MCP surface for voice testing: capture, transcription, feedback, run logs, settings, and a smoke-test script. This is active local development; no new ASC release was observed.
- `~/kinflash` separated its roster data from a fictional-pedigree fixture and refreshed the rendered export. This is internal development work; no new ASC release was observed.
- `~/oenora` added local App Store Connect app-registration documentation and tooling. It does not establish an ASC record, deployment, or public release; the provisional product name still requires clearance.
- `~/oenora` added an app icon, App Store and website copy, plus local ASC inspection and metadata-update scripts. These are launch-preparation assets, not evidence of an ASC record or public website.
- Several existing repositories received MasterIndex agent-entry-point documentation updates. These confirm their ongoing connection to the shared index, but do not by themselves establish a product release or deployment change.
- `~/adspill` was added to the index: a two-person (Bill + Jim) ad-capacity experiment. Project 1 is a working Python auction sim plus a real-time monitor UI (8 unit tests green, stdlib-only, no store/network yet); Project 2 is framing-stage only. A FloSports/Northwoods diligence memo reframed the effort as a demand + rights + sales-cost problem rather than an exchange build, gated on whether Northwoods League teams retain in-stream ad rights after FloSports' exclusive global deal. Repo is private, so no public link is recorded.

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
