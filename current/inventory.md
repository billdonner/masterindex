# MasterIndex Inventory

As of Monday, August 3, 2026.

## Scope

- Reviewed all local git repositories with 2026 commit activity under `/Users/billdonner/*` plus current 2026 experiment repos under `Documents/Codex/Experiments`.
- Treated all repositories as read-only.
- Retained the recorded 20-app App Store Connect inventory; no live ASC credentials were available for this audit, so ASC was not re-queried.
- Ignored older inactive repos unless directly tied to a 2026-active app, service, or shared package.

## Executive Summary

- App Store Connect currently shows 20 apps (2026-08-04 inventory; PickleBrains, picklefortunes, Alities, Quackman, and the stray screenkr2 listings were removed from ASC in the 2026-08 cleanup).
- 15 ASC apps map cleanly to currently active local repositories.
- 5 ASC apps are visible in ASC but do not have a clearly corresponding 2026-active local repository in this scan.
- Mallinbook was resolved on 2026-08-02: its repo is `~/mallinbook` (renamed 2026-08-01 from `bookmaker-app`, which hid it from the original scan). Multiplatform macOS + iOS; the `~/bookmaker` Python engine remains as read-only reference.
- AmenBeats was resolved on 2026-08-04: its repo is `~/drumbeats` (App Store name ≠ repo name hid it from earlier scans). A Bill + Jim SwiftUI drum-machine app; Jim (`@jrforster`) added as full admin, now a shared build.
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

## Current ASC Apps

### ASC apps mapped to active local repos

| ASC app | Bundle ID | ASC app ID | Repo | Local version/build | ASC state | Public link |
|---|---|---:|---|---|---|---|
| PickledBalls | `com.pickledballs.app` | `6762310890` | `~/PickledBalls` | `1.0 (354)` on TestFlight | `IOS 1.0 PREPARE_FOR_SUBMISSION` (metadata complete; only App Privacy questionnaire remains) | `https://pickledballs.billdonner.com` |
| Qross | `com.qross.app` | `6759799988` | `~/qross` | `0.2 (313)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` | No verified public link |
| 100 Burfords | `com.billdonner.burfords` | `6766107636` | `~/100Burfords` | `1.1 (9)` | `IOS 1.0 READY_FOR_SALE` | Verified website and App Store link in `index.json` |
| Flasherz Kids | `com.billdonner.obo` | `6759509933` | `~/obo-ios` | `1.1 (47)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` | No verified public link |
| Nagz | `com.nagz.app` | `6759530926` | `~/nagz-ios` | `1.4.0 (359)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` | No verified public link |
| Cardz Studio | `com.billdonner.cardz-studio` | `6759624116` | `~/cardz-studio-ios` | `1.0 (10)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` | No verified public link |
| KinFlash | `com.billdonner.kinflash` | `6762008872` | `~/kinflash` | `1.0.0 (65)` uploaded; TestFlight processing | `IOS 1.0 PREPARE_FOR_SUBMISSION` | No verified public link |
| workin On | `com.workinon.app` | `6762529338` | `~/workinon` | `0.9.1 (52)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` | No verified public link |
| Famster | `com.famster.app` | `6763581385` | `~/famster-ios` | `1.0.0 (3)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` | `https://api.famster.app` |
| LtWatcher | `com.ltwatch.app` | `6764622141` | `~/clubwatch` | `0.1.0 (4)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` | No verified public link |
| 123 Words | `com.123words.app` | `6766975041` | `~/123words` | `1.11 (40)` | `IOS 1.11 READY_FOR_SALE; 1.12 draft` | No verified public link |
| AmenBeats | `com.billdonner.drumbeats` | `6778510642` | `~/drumbeats` | TestFlight build `5+` | `IOS 1.0 DRAFT` | No verified public link |
| SentiPods | `com.sentipods.app` | not surfaced in local scan | `~/sentipods` | `1.0 (15)` | `IOS 1.0 PREPARE_FOR_SUBMISSION` (TestFlight build 14 uploaded) | `https://bd-grubber.fly.dev` |
| Mallinbook | `com.mallinbook.app` | `6785245339` | `~/mallinbook` | `1.0 (14)` | `IOS + MAC_OS 1.0 PREPARE_FOR_SUBMISSION` (TestFlight build 13 on both platforms) | No verified public link |
| Oliopfolio | `com.pfolio.app` | `6797993806` | `~/pfolio-app` | `1.0.0 (7)`; build 6 uploaded both platforms 2026-08-04 | `IOS + MAC_OS 1.0 PREPARE_FOR_SUBMISSION` (record created 2026-08-04; Mac is the primary platform) | No verified public link |

### Confirmed gaps

- The five ASC-only records are now browseable MasterIndex entities: MastPex IOS, MastPex Mac, PickleFamilia, Screenker, and Zerver Monitor. No corresponding active local repository was verified in the 2026-08-04 scan. (`AmenBeats` resolved to `~/drumbeats` on 2026-08-04.)
- Screenker is now wired to Qross, 123 Words, and 100 Burfords as their observed shared App Store screenshot-composition workflow. Its standalone app source, bundle ID, and public product page remain unverified.
- MasterIndex policy: every ASC app has an entity. A verified public website or App Store page is stored in `links`; when neither is verified, the entity's `release` field explicitly records its known release or development status.
- `grubber-ios` is active locally but did not match a current ASC app.
- `SentiPods` is mapped to `~/sentipods` (`com.sentipods.app`), based on the local project's alignment to its ASC 1.0 record. Its ASC app ID was not surfaced in the local scan.
- `picklefortunes` is retired: its ASC listing was deleted in the 2026-08 cleanup, its repository is archived, and its reusable kit is retained in PickledBalls.
- `Zerver Monitor` exists in ASC but only the backend/service repo was present in the local scan.
- `SharedSpaceLab` is local-only and not in ASC.

## Shared Services

- `bd-nagzerver.fly.dev` from `~/nagzerver`
- `bd-clubsync.fly.dev` from `~/clubsync`
- `bd-cardzerver.fly.dev` from `~/card-server`
- `bd-grubber.fly.dev` from `~/grubber`
- `bd-server-monitor.fly.dev` from `~/server-monitor`
- `bd-pfolio.fly.dev` from `~/pfolio` (portfolio tracker API; shares bd-postgres)
- `api.famster.app` as a confirmed backend domain without a corresponding repo found in this scan

## Collaborators

Unified watch over the people Bill co-works with, refreshed every 6h by the
`collaborator-activity-watch` task (`tasks/index.json`). Canonical data lives in
`current/index.json` under `collaborators[]`; this table is presentation only.

| Collaborator | Role | Repo | Last activity | Awaiting Bill |
|---|---|---|---|---|
| Jim Forster (`@jrforster`) | dev collaborator | `billdonner/adspill`, `billdonner/drumbeats` | adspill: ball in Jim's court (issue #2). drumbeats (AmenBeats): joined as admin 2026-08-04, feature work starting | No |
| Carol (`@cuchif`) | dev collaborator | `billdonner/qross` | 3 open PRs from Carol (#172/#173/#174, 07-25/26) | **Yes — 3 PRs need review** |
| Steve Gould | pfolio end-user / stakeholder | `billdonner/pfolio`, `billdonner/pfolio-app` | 4 open PRs on his product from `@rachelelise` (pfolio #3/#4, pfolio-app #1/#2) | **Yes — 4 PRs need review** |

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
