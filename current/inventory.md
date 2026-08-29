# MasterIndex Inventory

As of Friday, August 28, 2026.

## Scope

- Reconciled App Store Connect, active GitHub sources, local repositories, Fly deployments, and public product URLs.
- Applied no handoff directives because `current/handoffs/index.json` has none.
- Performed the requested retirements, operational fixes, website publications, and feedback-workflow replacement; observed facts and remaining product gaps are kept distinct below.

## Executive Summary

- ASC contains 23 app records: 20 map in the primary ASC inventory, two MastPex records are internal-use/TestFlight apps, and GigStand is the intentionally retained retired record.
- LtWatcher is retired. `billdonner/clubwatch` is archived read-only and its ASC record is retained.
- Clubsync is deferred until PickledBalls v2. Its application tier is not deployed; `bd-clubsync-db` remains deployed to preserve data.
- Card Server is retired after consumer and replacement checks. `billdonner/card-server` is archived, its Fly descriptor is removed, and Card Engine remains the sole verified source for `bd-cardzerver.fly.dev`.
- Server Monitor is repaired and deployed. Its seven production targets omit Clubsync and its direct Nagzerver and Card Engine HTTP probes return 200.
- The registry tracks 57 repositories, of which 52 remain active after the feedback replacement, prior retirements, and the `grubber-ios` obsolete decision.
- Canonical-main records for local-model-lab, adspill, and the Oenora Recognition API are preserved.
- The generated `billdonner.com/apps` catalog is live on IONOS with six active entries: AmenBeats, 123 Words, 100 Burfords, PickledBalls, workin On, and SentiPods. PickledBalls is independently listed from PickleFamilia. LT Watch and Flasherz Kids are nonviable and removed from the public apps tree; Screenker, Mallinbook, Pfoliolio, and PickleFamilia belong to the 1041Soft release track.
- App Feedback replaces the repeating TestFlight email loop with a local 41-item triage inbox across 21 active ASC apps. The working data stays on this Mac; client-encrypted recovery snapshots are versioned in iCloud Drive.
- The portfolio now has two explicit product lines: BillDonner.com apps are permanently free, while 1041soft.com products carry the commercial-grade release and support commitment. Owner confirmed on 2026-08-23 that amenbeats belongs on BillDonner.com.
- Nagz, Famster, and SharedSpaceLab are now recorded as one household-communications lineage rather than three independent products: SharedSpaceLab is the active successor prototype, Nagz is the working legacy reference, and Famster is a concept-only shell.
- Nagzerver remains mixed production infrastructure for Nagz, PickledBalls, PickleFamilia, and workin On. Its exact deployed source was recovered to private branch `recovery/deployed-2026-06-30` because Git `main` could not reproduce production.
- `grubber-ios` is obsolete by owner decision; SentiPods is the current grubber client.
- Grubber is the service, corpus, and intended product name for the podcast/news analysis system; SentiPods is the current ASC client label until a rename is executed. It is multi-client, not true multi-tenant. Grubber also owns the paid tech newsletter digest plan, the Fly-side global brand-universe supplement, and an aggregate artifact monitor at `https://bd-grubber.fly.dev/monitor`. Newsletter/Gmail-derived content is personal-only; brand metadata, derived brand mentions, and aggregate artifact snapshots live in Fly Postgres for server-side advertising-trend analysis, not in the public `/db` export or raw brand API routes. As of 2026-08-28, the live monitor reports 69 shows, 1,352 episodes, 1,374 public news articles, 162 active topics, 6,745 active brands, 3,795 derived brand mention rows, 16 daily digests, and one private brand report; `/monitor` is aggregate-only and excluded from OpenAPI. Public `/db` currently fails closed while the large validated SQLite transport is repaired.
- `doubleqross.com` is live at IONOS and now serves the DoubleQross product site directly (apex and `www`, Sectigo certificate through February 10, 2027): the domain is connected to the webspace `/qross` directory, which also hosts the app's catalog downloads. Pages are sourced from the qross repo's `docs/` and deployed by SFTP; `1041soft.com/qross/` is legacy and `billdonner.github.io/qross` mirrors the same content.
- The screenshot program now distinguishes Screenker provenance, critique score, freshness, publication, and live ASC parity. Nine apps have verified Screenker history; the immediate correction schedule and future release rubric are in `docs/screenshot-operations.md`.
- KinFlash is now **two products**, decided 2026-08-23. The Mac app authors family trees, flashcards, and games; its price is undecided. The iOS app is free and only plays what the Mac produced. They shared one bundle id — one App Store record, one price — so the ids were split before submission: `com.billdonner.kinflash` (Mac) and `com.billdonner.kinflashplay` (iOS, shown as "KinFlash Play"). This supersedes the 2026-08-19 decision that all three platforms would ship as one universal app at one price; Mac App Store distribution and TestFlight for both still hold. Public page: `billdonner.com/apps/kinflash/`. Two risks stand: `billdonner.com` expires 2026-12-14 and will host the Support and Privacy URLs, and the live page still advertises "optional cloud sync backup" for an app that has no sync of any kind. Ten game designs are proposed in the repo (`GAMES_DESIGN.md`), and the first — "How Are We Related?" — is built end to end as of 2026-08-24 (build 71). Two decisions were settled: living relatives may appear **per game**, chosen at generation and recorded in the file, with a game that excludes them naming none of them anywhere, not even as a wrong answer; and a game is its own small exportable document (`.kinflashgame`) rather than something inside the tree package, so it arrives in Messages, opens with one tap, and gives the recipient the game rather than the family database. Nine games remain unbuilt.
- Pickleball Collective now has two active local sources: Collective Engine is the deployed multi-tenant scheduler, and Collective Comms is the approval-gated dedicated-Mac messaging utility. Neither is an App Store product.
- Collective Engine now emits file-based, RFC 8785-canonical handoff payloads with verification tooling. Collective Comms now defaults one-to-one delivery to SMS, supports explicit overrides, and surfaces invalid Messages targets rather than silently dropping sends.
- Operational evidence on August 21 confirmed that an iMessage send reached 16 iPhone players but silently missed 3 Android players; SMS resend delivered to all three. The scheduler also records its handoff-only Tuesday court split as non-authoritative.
- Collective Engine now exposes court-seat capacity and attendance limit separately, preventing a rotational opening from being shown to a player as a full day.
- Collective Engine now labels rotations clearly for bookers. Collective Comms can append an iMessage-only weekly calendar attachment after the text send; SMS is intentionally excluded and attachment failure cannot affect the text-delivery record.
- Collective Engine's Fly deployment has a healthy `/health` endpoint, but its intended `collective.1041soft.com` host is still NXDOMAIN; publish that DNS record and the corresponding exact-match Auth0 URLs before calling it publicly reachable. Collective Comms now verifies the producer's canonical handoff digest and blocks publication on a mismatch.
- Review Authority is an active local, read-only review controller. Its Milestone 1 vertical slice can inspect a registered build source, redact and content-address evidence, request a bounded cloud critique, and retain an audit record; it has no public release, UI, correction loop, or configured Git remote.
- XpenseXpunger is a new 1041soft-commercial project at `~/xpensexpunger`. It is a separate Mac-first, local-first expense evidence scanner for Gmail receipts, local files, screenshots, PDFs, CSVs, and later Plaid Transactions. It must not be merged into `pfolio`, and `~/1041soft` is output-only for compatible `finance/scan-results/*.json` exports.
- 1041Soft LLC's Apple Developer Program conversion request was submitted on 2026-08-24 to move the existing Individual membership to an Organization membership after D-U-N-S issuance. Apple support case ID: `20000146677819`. Approval and seller-name/account conversion are still pending.

## Product Lines

### BillDonner.com — always free

Personal utilities, experiments, and children-oriented apps. Users are never charged; a Mac
version and MCP surface are optional. `SharedSpaceLab`, `Nagz`, `workin On`, `AmenBeats`,
`SentiPods`, `Flasherz Kids`, and `Zerver Monitor` belong to this product family. `workin On`
and `Flasherz Kids` are internal-use/obsolete rather than public releases; `MastPex IOS` and
`MastPex Mac` remain internal-use/TestFlight-only.

### 1041soft.com — commercial

Products intended for sale or another explicit revenue model. These carry a higher quality,
testing, documentation, privacy, and support bar; they should normally have a real Mac version
and an MCP or automation surface when that fits the product. KinFlash is the newest confirmed
assignment and is planned for near-term release.

The 1041Soft release-track page now lists DoubleQross, Oenora, Screenker, Mallinbook,
Pfoliolio, PickleFamilia, and other current release-track entries; none is currently approved for App Store release. The BillDonner.com assignments above are excluded from that page. The 1041Soft homepage now foregrounds MCP control from Claude and ChatGPT, including voice workflows; Oenora is the next planned MCP-enabled app. KinFlash's public page was decided on
2026-08-19: it lives at `billdonner.com/apps/kinflash/`, not on 1041soft.com and
not on GitHub Pages, following the existing one-page-per-app pattern under
`/apps/<name>/`.

## Expense Evidence / XpenseXpunger

XpenseXpunger is the active implementation track for bookkeeping evidence scanning. It exists in
`~/xpensexpunger`, not under `~/1041soft`, and targets the 1041soft commercial product line. The
first build is a SwiftPM CLI/Mac-first core with local SQLite storage, safe metadata-only raw
document tracking, vendor matching, schema-v1 JSON export, and compatibility verification through
`~/1041soft/finance/scripts/aggregate_bookkeeping.py`.

Security boundary: raw bank logs, Gmail/Plaid tokens, card or account identifiers, SSNs, OAuth
secrets, Plaid access tokens, and session cookies must never be written to repo files. Raw evidence
stays where the user selected it; the app stores references and redacted extracted fields.

Release status: initial SwiftPM CLI MVP is committed in `~/xpensexpunger`, and a private product
site is deployed at `https://xpensexpunger.poobah52.chatgpt.site` with support and privacy sections
for ASC draft metadata. No App Store Connect record, bundle id, signed archive, TestFlight build,
or storefront screenshots have been verified yet.

Maintenance utility direction: as of 2026-08-26, XpenseXpunger should be the local monthly utility
for maintaining 1041soft.com expense evidence. The committed plan is
`~/xpensexpunger/docs/1041SOFT_EXPENSE_MAINTENANCE_PLAN.md`: import private local evidence outside
git, normalize into SQLite, export schema-v1 JSON into `~/1041soft/finance/scan-results/`, and run
the existing 1041soft aggregator after export.

Bookkeeping baseline: `~/1041soft/finance/scan-results/` now contains normalized schema-v1
results from Gmail receipt scans, Apple subscription screenshots, and Apple Card CSV transaction
history. The aggregate output is `~/1041soft/finance/bookkeeping-aggregate-2026-08-23.md`, generated
by the existing `aggregate_bookkeeping.py` workflow. Raw Gmail/card/Plaid exports stay out of git;
Apple hardware was explicitly checked in the Apple Card CSV and no clear Apple Store hardware
purchase was found.

Open accounting work: business, personal, mixed-use, deductible classification, and
product-specific Apple purchase-history attribution for Apple-billed subscriptions still require
owner/accountant decisions.

## Screenshot Program

The August 14 read-only App Store Connect audit inspected every mapped version, locale, and
screenshot display type, then correlated those live sets with repository history and Screenker
projects. A gallery is not called current merely because it is present in ASC or once received a
high score.

| State | Apps |
|---|---|
| Current, scored, and published | 100 Burfords (iPhone 88/iPad 90) |
| Current internal/TestFlight evidence; no public gallery work | workin On (93) |
| Current and published, below the commercial target | Screenker (86) |
| Published but score or captures are stale | DoubleQross, PickledBalls, 123 Words, amenbeats, Pfoliolio |
| Screenker projects exist but critique coverage is incomplete | Mallinbook (Mac 89; iPhone/iPad unscored) |
| ASC device coverage exists without Screenker critique | SentiPods |
| Local captures exist but ASC is empty | Oenora iOS |
| Active ASC release record is empty | Zerver Monitor |
| Highest-priority missing commercial gallery | KinFlash — now two galleries (paid-TBD Mac authoring app, free iOS player); ASC empty for every slot |
| Defer until lifecycle or release decision | SharedSpaceLab, PickleFamilia |
| Internal functional evidence only | Cardz Studio, workin On, MastPex iOS, MastPex Mac |
| No new screenshot work | Flasherz Kids, LtWatcher, grubber-ios, Famster, Nagz |

The cleanup queue runs August 15-26: DoubleQross and 123 Words first; amenbeats and
PickledBalls next; then Pfoliolio and Mallinbook. KinFlash now takes the next two slots for
commercial capture and critique, followed by SentiPods, Screenker, Oenora, a verification-only
check for 100 Burfords, and Zerver Monitor if its build remains a release candidate. The
detailed daily exit conditions are in `docs/screenshot-operations.md`.

Future releases use a T-7 capture brief, T-5 deterministic capture, T-4 critique, T-3 re-shoot,
T-2 human approval and ASC publication, T-1 drift check, and T+1 storefront verification.
Hard gates cover truth, privacy, provenance, technical export, device coverage, accessibility,
localization, ASC parity, and human approval. Screenker's weighted score remains hook 30,
thumbnail legibility 20, narrative 20, consistency 20, and finish 10. The general release gate
is 85; a confirmed 1041soft.com product targets 90.

## Household Communications Lineage

| Component | Honest role | Current direction |
|---|---|---|
| SharedSpaceLab | Active successor prototype | Continue the friendly, local-first shared household surface on iPhone and wall-mounted iPad; Mac Catalyst, local MCP, and nearby peer communication already exist |
| ConversationLab | Reusable conversation kernel candidate | Preserve and harden behind SharedSpaceLab use cases |
| CoordinationLab | Reusable coordination kernel candidate | Preserve and harden behind SharedSpaceLab use cases |
| Nagz | Working legacy reference | Mine its implemented family, connection, reminder, remote messaging, and APNs behavior; do not add product features by default |
| Famster | Concept-only shell | Stop treating it as an independent product; its visible feature areas are placeholders and 1041Kit initialization is commented out |
| 1041Kit | Capable generic package, currently unwired in Famster | Reuse only if the successor later needs its auth, API, GRDB, sync, or WebSocket layers |
| Nagzerver | Shared production infrastructure | Keep operating independently of the product-line decision; separate or retire routes consumer by consumer |

SharedSpaceLab intentionally has no Nagz, Famster, account, or remote-backend runtime dependency
today. That is the correct experimental boundary, not evidence that the projects are unrelated.
Prove the local household interaction model first. Then migrate only the Nagz server capabilities
that the product demonstrates it needs, such as remote identity, off-LAN communication, or APNs.
The eventual public name, BillDonner.com versus 1041soft.com assignment, business model, and
native-Mac requirement remain open.

## Feedback Recovery

The App Feedback working store remains under `~/Library/Application Support/AppFeedback` and
is served only on `127.0.0.1`. After every successful two-hour collection, it is compressed and
AES-256 encrypted before being written to `iCloud Drive/AppFeedback Backups`. The job retains
14 days of recent snapshots, 90 daily snapshots, and 24 monthly snapshots.

The encryption key is in the login Keychain under
`com.billdonner.app-feedback.backup`. The first encrypted snapshot was independently restored
on 2026-08-14; its 41-item JSON state and all screenshot files matched the live store byte for
byte. Source, restore commands, and recovery-key instructions are in `~/app-feedback`.

## Completed Reconciliation

### Product lifecycle

- LtWatcher was retired because its Clubsync dependency is absent and that capability has no useful path before PickledBalls v2.
- Clubsync was removed from current PickledBalls dependencies and from recurring health checks. The source and database remain available for the v2 decision.
- Card Server was checked against current consumers and the live service before retirement. All observed current consumers use Card Engine.
- Card Server's historical Qross App Store ID was corrected before archival, and its deployment descriptor was removed to prevent accidental replacement of Card Engine.

### Server Monitor

- Production uses public `/healthz` and `/health` endpoints for Nagzerver and Card Engine.
- Cardzerver records now use canonical entity id `card-engine-backend`.
- Clubsync is no longer a monitored production target.
- Live `/api/status` reported seven configured targets and successful HTTP 200 probes for Nagzerver and Cardzerver.
- Remaining yellow/red display values are database thresholds such as cache rate and historical failed deliveries, not failed endpoint checks.

### Version and build drift

| App | Source | App Store Connect | Result |
|---|---:|---:|---|
| Pfoliolio | 35 | iOS + macOS 35 VALID | Aligned |
| amenbeats | 8 | 8 VALID | Aligned in GitHub commit `aea6725` |
| 100 Burfords | 1.1 (9) | 1.1 (9) draft | Aligned in GitHub commit `48192f3` |
| DoubleQross | 394 | 394 VALID | Aligned; bundle id remains com.qross.app; store name DoubleQross; 12+ |
| 123 Words | 1.12 (59) | 59 VALID | Aligned to the open 1.12 train in commit `3f89587` |
| SentiPods | iOS 20, macOS 21 | macOS 21 VALID | Aligned |
| Oenora iOS | 1.0 (7) | 7 VALID, external beta submitted; 6 remains approved | Aligned; native Mac uses a separate notarized Developer ID bundle |

Pfoliolio export used App Store-managed numbering, so Apple accepted both platforms as build 35. Source was aligned and pushed in commit `2d73c97`.

## Card Server Compatibility Finding

The retirement check exposed two response-contract differences when the legacy Card Server suite was pointed at production Card Engine:

- Bulk deletion of a nonexistent item returns 422; the legacy suite expected 200.
- An invalid daily-score date returns 404; the legacy suite expected 400.

No current consumer was found to require Card Server, so these do not block retirement. They remain recorded for any Card Studio or legacy-client migration work.

## Current ASC Apps

| App | Bundle ID | Repository | State |
|---|---|---|---|
| Pfoliolio | com.pfolio.app | ~/pfolio-app | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| amenbeats | com.billdonner.drumbeats | github:billdonner/drumbeats | iOS 1.0 PREPARE_FOR_SUBMISSION |
| Oenora | com.billdonner.oenora | ~/oenora | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| SharedSpaceLab | com.1041soft.experiments.sharedspacelab | ~/Documents/Codex/Experiments/SharedSpaceLab | Active successor prototype; iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| Screenker | com.screenker.app | github:billdonner/screenker | macOS 1.0 PREPARE_FOR_SUBMISSION |
| SentiPods | com.sentipods.app | ~/sentipods | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| Mallinbook | com.mallinbook.app | github:billdonner/mallinbook | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| workin On | com.workinon.app | ~/workinon | Internal/TestFlight-only; iOS 1.0 retained |
| 100 Burfords | com.billdonner.burfords | ~/100Burfords | 1.0 READY_FOR_SALE; 1.1 draft |
| Zerver Monitor | com.billdonner.ZerverMonitor | ~/server-monitor-ios | iOS 1.0 PREPARE_FOR_SUBMISSION |
| Famster | com.famster.app | ~/famster-ios | Concept-only shell; iOS 1.0 PREPARE_FOR_SUBMISSION retained |
| Nagz | com.nagz.app | ~/nagz-ios | Working legacy reference; iOS 1.0 PREPARE_FOR_SUBMISSION retained |
| DoubleQross | com.qross.app | ~/qross | iOS 1.0 PREPARE_FOR_SUBMISSION |
| LtWatcher | com.ltwatch.app | archived github:billdonner/clubwatch | Retired; ASC record retained |
| Flasherz Kids | com.billdonner.obo | ~/obo-ios | Obsolete; ASC record retained |
| PickleFamilia | com.picklefamilia.app | github:billdonner/picklefamilia-ios | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| KinFlash (Mac, authoring) | com.billdonner.kinflash | ~/kinflash | Price TBD; no macOS platform version in ASC yet |
| KinFlash Play (iOS, player) | com.billdonner.kinflashplay | ~/kinflash | Free; ASC record 6762008872 still carries the OLD bundle id and needs reconciling |
| PickledBalls | com.pickledballs.app | ~/pickledballs | iOS 1.0 PREPARE_FOR_SUBMISSION |
| 123 Words | com.123words.app | github:billdonner/123words | 1.11 READY_FOR_SALE; 1.12 draft |
| Cardz Studio | com.billdonner.cardz-studio | ~/cardz-studio-ios | Internal/TestFlight-only; iOS 1.0 retained |

Unmatched or intentionally retained:

- MastPex IOS and MastPex Mac are internal/TestFlight-only apps in the shared MasterIndex Explorer repository; they are not public-release placeholders.
- GigStand is retired, removed from all 175 territories, and permanently retained by ASC because it was previously sold.

## Services

| Service | Source | State | Consumers |
|---|---|---|---|
| bd-nagzerver.fly.dev | ~/nagzerver | live | Nagz, workin On, PickledBalls, legacy PickleFamilia |
| bd-cardzerver.fly.dev | ~/card-engine | live | Qross, Flasherz Kids, Cardz Studio, card-studio |
| bd-grubber.fly.dev | ~/grubber | live | SentiPods, grubber clients |
| bd-server-monitor.fly.dev | ~/server-monitor | live | operations, Zerver Monitor |
| bd-pfolio.fly.dev | github:billdonner/pfolio | live | Pfoliolio |
| api.famster.app | ~/nagzerver | alias | Famster concept shell; same deployment and API as Nagzerver |
| bd-oenora-recognition.fly.dev | ~/oenora | live | Oenora |
| bd-clubsync.fly.dev | ~/clubsync | deferred | PickledBalls v2 only |

Fly also contains live infrastructure apps `bd-postgres` and `bd-clubsync-db`, plus suspended `bd-arca` and `bd-podcast-brands`.

### Nagzerver source recovery

The live Fly release exposes 37 current `/api/v1/pb/*` PickledBalls routes, 14 legacy
`/api/v1/pickle/*` routes, seven workin On routes, four residual clubwatch routes, and the Nagz
family API. The PickledBalls and PickleFamilia implementation was absent from every inspected
Git `main` ref. The exact non-secret source from Fly release v100 was preserved at commit
`a57211b` on private branch `recovery/deployed-2026-06-30` without changing production or main.

That recovered tree generates all 163 live API paths. Its full suite passes 1,113 of 1,114 tests.
The remaining failure, `tests/test_pickleball_sessions.py::test_player_schedule`, shows a confirmed
occurrence omitted from `/api/v1/pb/schedule`. Review and repair that branch before any merge or
redeployment; until then, main is not a reproducible source for production.

## Feedback Triage

- `~/app-feedback` is the active source and local installation; its private GitHub mirror contains code only.
- The dashboard is live at `http://127.0.0.1:4317` and binds only to localhost.
- The initial collection scanned 21 active ASC apps and retained 41 items: 36 screenshot submissions, five crash reports, and 36 downloaded screenshots, with zero API errors.
- A second launchd collection recognized all 41 source ids, queued nothing, produced no duplicates, and exited 0.
- New, Triaged, and Done states, priority, notes, screenshots, search, and app/type/status filters are stored under `~/Library/Application Support/AppFeedback` and are never uploaded.
- `com.billdonner.app-feedback-collect` runs at login and every two hours; `com.billdonner.app-feedback-server` keeps the dashboard available. Since 2026-08-22, unchanged collections skip duplicate snapshot publication by digest while a seven-day maximum age preserves recovery freshness.
- The retired `zkraper` and `asc-feedback` private repositories contain replacement notices and are archived. Their email, manual watermark, and Qross-only flows must not be scheduled.

## Website Publication

- `tools/generate_billdonner_apps.py` generates the active catalog from canonical JSON.
- `publish/billdonner.com/apps/index.html` is the historical MasterIndex publication path; the current six-entry catalog is maintained in `~/website` and includes PickledBalls independently from PickleFamilia.
- `publish/billdonner.com/apps/pfoliolio/index.html` supplies the marketing and support route expected by ASC.
- `publish/billdonner.com/apps/oliopfolio/index.html` redirects the obsolete name to Pfoliolio.
- The current generated files were published to IONOS on 2026-08-28; live verification passed for the homepage, `/apps/`, `/apps/pickledballs/`, and retained support routes.
- The previous catalog and LtWatcher directory were retained under `/_archive`; the public LtWatcher route now returns 404.

### Company Website — `1041soft.com` (live 2026-08-28)

Canonical app-website home. Public repo `billdonner/1041soft-site`, served by GitHub
Pages, Let's Encrypt certificate covering apex and `www`, valid to 2026-11-12, HTTPS
enforced with HTTP 301ing to it. DNS at Namecheap: apex A records to
`185.199.108–111.153`, `www` CNAME to `billdonner.github.io.`

Observed paths: `/qross/`, `/nagz/`, `/workinon/`, `/flasherz/`, `/zervermonitor/`,
`/screenker/`, `/mallinbook/`, `/sentipods/`, `/pfolio/` — each with support and
privacy pages. All 24 routes verified 200 over HTTPS.

`doubleqross.com` was registered and activated at IONOS on 2026-08-14. Apex and `www` resolve
through IONOS, present the included Sectigo certificate covering both names through 2027-02-10,
and return HTTP/2 302 over HTTPS to `https://1041soft.com/qross/`, which returns 200. The branded
domain is ready to use as DoubleQross's marketing URL in App Store Connect.
ASC iOS 1.0 `en-US` now uses `https://doubleqross.com/` as its marketing URL; its support URL
remains `https://1041soft.com/qross/support.html` so the maintained support content is not duplicated.

Owner reported purchasing `picklefamilia.com` and `picklefamilia.app` through IONOS on 2026-08-29.
DNS, SSL, redirects, canonical-domain choice, auto-renewal, and renewal pricing are not yet verified.
The same IONOS dashboard showed 88.92 GB of webspace used, 12,963 files, 7 SFTP users, 2 standard
databases, PHP Extended Support active, a Site Scan warning for vulnerable websites, and Performance
Level 2; no payment or credential data is recorded here.

**Rule: never enable GitHub Pages on a private repo.** Pages publishes `docs/` to the
open web regardless of repo visibility, and bills Actions minutes on private repos.
Add a subpath here instead.

This site coexists with the now-live `billdonner.com/apps` portfolio catalog. The owner has now
assigned workin On and amenbeats exclusively to the permanently free BillDonner.com line, making
any 1041soft.com homepage promotion for those apps a presentation drift rather than a canonical
product home.

## Preserved Main-Only Facts

- `local-model-lab` is parked, with its historical MLX/Qross corpus benchmark results retained.
- `adspill` remains a two-person advertising-capacity research sandbox.
- The Oenora Recognition API is live at `bd-oenora-recognition.fly.dev` and remains an Oenora dependency.
- Oenora's public TestFlight invite, approved build 6, submitted build 7 with sealed-case tracking, three-device CloudKit soak, repaired recognition configuration, and notarized native Mac delivery are retained.

## Remaining Gaps

- Mallinbook's ASC privacy URL still points to a removed GitHub Pages route and returns 404. A working replacement now exists at `https://1041soft.com/mallinbook/privacy`; the ASC field still needs setting.
- SentiPods still has no ASC privacyPolicyUrl. A working page exists at `https://1041soft.com/sentipods/privacy`; the ASC field still needs setting.
- **Closed 2026-08-14 — unintended public exposure.** Seven private repos (qross, nagz, nagz-ios, workinon, obo-ios, server-monitor-ios, mallinbook) were publishing `docs/` to the open web through GitHub Pages. Verified world-readable at the time: qross business plans, risk register, `architecture/cardzerver-operational-roadmap.md`, `decisions/ADR-009-secret-management.md`, `carol-claude-code-instructions.md`; and nagz `DEPLOYMENT_PLAN.md`, `CODE_REVIEW_FINDINGS.md`, `CONTRIBUTOR_GUIDE.md`. Scanned for live credential patterns and found none. Pages disabled on all seven; every path re-verified 404.
- `nagz/docs/.well-known/apple-app-site-association` never actually served — Jekyll ignores dot-directories — so universal links have never worked from that domain. Not a regression from the migration.
- Age ratings remain unset for Oenora, SharedSpaceLab, and SentiPods pending owner decisions.
- `~/peerlink` is missing and no matching GitHub repository was found, so PickledBalls project generation remains blocked on this machine.
- ~~`1041soft.com` still points at Namecheap forwarding/parking; HTTPS is unusable.~~ **Resolved 2026-08-14** — see Company Website below. Apex now serves from GitHub Pages over enforced HTTPS.
- Oenora's existing ASC macOS 1.0 record has no builds after the project deliberately replaced Catalyst with a native Developer ID target using `com.billdonner.oenora.mac`.
- Nagzerver Git `main` does not reproduce the deployed PickledBalls and PickleFamilia API. The exact deployed source is preserved on `recovery/deployed-2026-06-30`, but its one failing schedule test must be resolved before review and merge.
- SharedSpaceLab's public product name, product-line assignment, business model, and eventual server boundary remain undecided. Famster must not be expanded as a parallel implementation while those decisions are open.
- 1041Soft LLC's Apple Developer organization conversion is pending Apple review under case ID `20000146677819`. No approval, seller-name change, or converted organization membership has been verified yet.

## Operational Rule

Use `current/index.json` as source of truth, `tasks/index.json` for recurring routing, and `current/handoffs/index.json` for next-cycle directives. Public websites and `site/` are presentation surfaces and must be checked against JSON, ASC, repository settings, and live deployments.
