# MasterIndex Inventory

As of Monday, September 14, 2026 (targeted website update; retained app observations have their own dates).

## Scope

- Reconciled App Store Connect, active GitHub sources, local repositories, Fly deployments, and public product URLs.
- Applied no handoff directives because `current/handoffs/index.json` has none.
- Performed the requested retirements, operational fixes, website publications, and feedback-workflow replacement; observed facts and remaining product gaps are kept distinct below.

## 1041Soft company email and daily check — 2026-09-20

- Company email is complete: one Private Email mailbox (`bill@1041soft.com`, renewed to 2027-09) with free aliases `support@`, `info@` and `finance@1041soft.com`; everything forwards to billdonner@gmail.com, Gmail filters label it under `1041Soft/Support|Info|Apple|Finance`, and Gmail sends as all four addresses via `mail.privateemail.com:465`. Private Email clients need an app password, and the SMTP username is always `bill@1041soft.com`.
- A daily 8:30 AM Chicago "morning check" (tasks/index.json `1041soft-morning-check`, owner-initiated by saying "check" in a Claude Code session; any session timer is only a convenience) sweeps the Apple support case and entity state, App Review queues, the four Gmail labels and Twilio's balance, and logs Apple events to `~/1041soft/formation/`.

## AmenBeats submitted — 2026-09-16

- Owner approved the TestFlight beta and authorized submission. AmenBeats 1.0 build 17 was submitted at 21:07 UTC (4:07 PM Central). Both the app version and submission `b57551af-97b8-455b-a0be-0283ceefb642` are **WAITING_FOR_REVIEW**, verified by ASC API. Automatic release after approval remains selected.
- The earlier TestFlight-only instructions below are historical and superseded by this approval.

## AmenBeats TestFlight update — 2026-09-16

- Build 16 was rejected September 15 for undiscoverable parental controls and an unresponsive Kid-mode exit.
- Build 17 is VALID and IN_BETA_TESTING for the existing internal TestFlight group. Xcode Cloud run 17 succeeded from `02aecfa`; parent PIN/recovery, compact lock help, and fitted Kid layouts are included.
- App Store 1.0 is PREPARE_FOR_SUBMISSION with build 17 selected. Corrected description and reviewer steps are saved. **Not submitted**, per owner request; test the beta first.
- External/public-link distribution of build 17 has not been requested; its external beta state is READY_FOR_BETA_SUBMISSION.

## AmenBeats and Apple migration update — 2026-09-14

- Owner reports AmenBeats 1.0 build 16 submitted September 6, superseding the September 5 withdrawal. Current App Store Connect state was not independently checked in this update.
- Owner confirmed sending a follow-up to Apple Developer Support in case `20000146677819`, asking whether migration is blocking or delaying the build, what steps remain, and expected timing. Lisa replied the same day (enrollment approved) without addressing the submission. ASC verified by API 2026-09-14: build 16 WAITING_FOR_REVIEW since September 6, most likely held while ASC shows "Developer Information Update In Process"; do not withdraw or resubmit. [Support thread](https://mail.google.com/mail/#all/1a03fa9200586e03).
- Lisa's September 14 reply confirmed enrollment `CX276BJ992` was verified and approved September 13 and said TestFlight builds, tester groups, and feedback should transfer. Owner accepted the Program License Agreement September 14 and the Certificates, Identifiers & Profiles portal came back the same day (verified by API). The developer-information update is still in process in ASC; seller-name change, LLC W-9, and Paid Apps re-acceptance wait on that.

## Owner decisions 2026-09-08

- Nagzerver is reference-only: the Fly app has had no machines since 2026-08-18. It is kept for occasional testing, and every consumer (PickledBalls, workin On, PickleFamilia, Nagz, api.famster.app) is to have its nagzerver dependency removed.
- App Feedback is now the primary feedback inbox and runs on this Mac (repo at `~/app-feedback`, both launchd jobs loaded, dashboard at 127.0.0.1:4317). The backup key still lives only in OldM1's Keychain.
- Removed from the inventory: Flasherz Kids (`obo-ios`), both MastPex placeholders, Card Server, `grubber-ios`, and `adspill`.
- oenora-merchant is paused; its Fly app stays with zero machines (hourly machine destroyed).
- Fly apps `bd-arca` and `bd-podcast-brands` were destroyed. The local pfolio uvicorn and the two stray Oenora dev servers were stopped.

## Executive Summary

- ASC contains 21 app records as of 2026-09-05: 20 map in the primary ASC inventory and GigStand is the intentionally retained retired record. Since the 2026-08-14 scan, Flasherz Kids, both MastPex records, and the original HOABooklet/Mallinbook record (6785245339) were deleted; HOABooklet now lives on new record 6806080022 with no builds yet, and KinFlash Studio gained record 6806833310. SentiPods is now named Grubber Desk and KinFlash is KinFlash Family in ASC.
- LtWatcher is retired. `billdonner/clubwatch` is archived read-only and its ASC record is retained.
- Clubsync is deferred until PickledBalls v2. Its application tier is not deployed; `bd-clubsync-db` remains deployed to preserve data.
- Card Server is retired after consumer and replacement checks. `billdonner/card-server` is archived, its Fly descriptor is removed, and Card Engine remains the sole verified source for `bd-cardzerver.fly.dev`.
- Server Monitor is repaired and deployed. Its seven production targets omit Clubsync and its direct Nagzerver and Card Engine HTTP probes return 200.
- The registry tracks 57 repositories, of which 52 remain active after the feedback replacement, prior retirements, and the `grubber-ios` obsolete decision.
- Canonical-main records for local-model-lab, adspill, and the Oenora Recognition API are preserved.
- The 14-entry `billdonner.com/apps/` personal portfolio is live on IONOS as of September 14. Descriptions remain here; product, support, and privacy actions point to 1041Soft.
- App Feedback replaces the repeating TestFlight email loop with a local 41-item triage inbox across 21 active ASC apps. The working data stays on this Mac; client-encrypted recovery snapshots are versioned in iCloud Drive.
- All apps now share 1041Soft as their company home. Historical always-free and commercial pricing commitments remain distinct; the domain move does not change pricing.
- Nagz, Famster, and SharedSpaceLab are now recorded as one household-communications lineage rather than three independent products: SharedSpaceLab is the active successor prototype, Nagz is the working legacy reference, and Famster is a concept-only shell.
- workin On is TestFlight-only by owner decision (2026-09-04) and now ships through an Xcode Cloud archive lane (push to `release`), the first BillDonner.com app to do so; the MasterIndex board line and the shipping GitHub-tabs line were merged on 2026-09-07, so `main` and `release` are the same commit again.
- Nagzerver remains mixed production infrastructure for Nagz, PickledBalls, PickleFamilia, and workin On. Its exact deployed source was recovered to private branch `recovery/deployed-2026-06-30` because Git `main` could not reproduce production.
- `grubber-ios` is obsolete by owner decision; SentiPods is the current grubber client.
- Grubber is the service, corpus, and intended product name for the podcast/news analysis system; SentiPods is the current ASC client label until a rename is executed. It is multi-client, not true multi-tenant. Grubber also owns the paid tech newsletter digest plan, the Fly-side global brand-universe supplement, and an aggregate artifact monitor at `https://bd-grubber.fly.dev/monitor`. Newsletter/Gmail-derived content is personal-only; brand metadata, derived brand mentions, and aggregate artifact snapshots live in Fly Postgres for server-side advertising-trend analysis, not in the public `/db` export or raw brand API routes. As of 2026-08-28, the live monitor reports 69 shows, 1,352 episodes, 1,374 public news articles, 162 active topics, 6,745 active brands, 3,795 derived brand mention rows, 16 daily digests, and one private brand report; `/monitor` is aggregate-only and excluded from OpenAPI. Public `/db` currently fails closed while the large validated SQLite transport is repaired.
- `doubleqross.com` serves the IONOS `/qross` product site directly; deploy only the explicit public-file allowlist from the qross repo. As of September 12, 2026, legacy `1041soft.com/qross/` and `billdonner.github.io/qross` redirect here. The GitHub mirror no longer publishes internal docs.
- The screenshot program now distinguishes Screenker provenance, critique score, freshness, publication, and live ASC parity. Nine apps have verified Screenker history; the immediate correction schedule and future release rubric are in `docs/screenshot-operations.md`.
- KinFlash is **two products with two App Store records**, re-split 2026-08-30 after a brief period merged under one record. **KinFlash Studio** (macOS, `com.billdonner.kinflashstudio`) authors trees, flashcards and games and is where every purchase happens; **KinFlash Family** (iOS, `com.billdonner.kinflash`) is free, plays what Studio produced, and cannot take payment at all. Note the assignment: Family keeps the ORIGINAL identifier and the existing record 6762008872 — whose iOS 1.0 dates from April — and Studio is the one needing a new record, which the ASC API cannot create; it is a manual click and currently blocks splitting the Xcode Cloud workflows. The earlier plan had these reversed, with the Mac on `com.billdonner.kinflash` and iOS on `com.billdonner.kinflashplay`; neither `kinflashplay` nor the name "KinFlash Play" is used any more. The merge was undone because one record cannot tell TestFlight which of two dissimilar apps a Mac should install, and it demonstrably handed over the iOS player instead of the authoring app; `SUPPORTS_MAC_DESIGNED_FOR_IPHONE_IPAD = NO` does not help, since TestFlight resolves per record. Pricing direction (proposed, not approved) is an annual subscription in Studio gating generation and hosted AI, with everything already produced free forever to the author and her recipients, and bring-your-own-API-key kept as a privacy option at the same price — see `~/kinflash/PRICING.md`. Hosted AI is now load-bearing and unbuilt: granny will not obtain an Anthropic key, and the subscription's justification rests on it. Public company page: `1041soft.com/kinflash/`; the personal portfolio links there. The former BillDonner.com support/privacy hosting assignment is superseded. Website copy still needs reconciliation with the Family/Studio split. Ten game designs are proposed in the repo (`GAMES_DESIGN.md`), and the first — "How Are We Related?" — is built end to end. Two decisions were settled: living relatives may appear **per game**, chosen at generation and recorded in the file, with a game that excludes them naming none of them anywhere, not even as a wrong answer; and a game is its own small exportable document (`.kinflashgame`) rather than something inside the tree package. Nine games remain unbuilt.
- PickleFamilia is the family name (ADR-009 in collective-engine, 2026-09-13) over Collective Engine — the deployed multi-tenant club scheduler, the club's record and channels — and PickleFamilia Companion (repo pickledballs, bundle com.pickledballs.app), the court app that, signed in by a texted code, is also the member's window on the club. Collective Comms is the older approval-gated dedicated-Mac messaging utility. The old picklefamilia-ios organizer app is not revived; its ASC record is legacy. picklefamilia.com and picklefamilia.app are live on the engine since 2026-09-13. The Companion's core is the PickleFamiliaCore package (~/picklefamilia-core), which the iOS app compiles in and the coming Android app (Swift SDK for Android, Kotlin UI, full parity) will link. The engine's main carries the web-service prototype (club types, browser sign-in, admin panel at /admin) awaiting deploy.
- Collective Engine now emits file-based, RFC 8785-canonical handoff payloads with verification tooling. Collective Comms now defaults one-to-one delivery to SMS, supports explicit overrides, and surfaces invalid Messages targets rather than silently dropping sends.
- Operational evidence on August 21 confirmed that an iMessage send reached 16 iPhone players but silently missed 3 Android players; SMS resend delivered to all three. The scheduler also records its handoff-only Tuesday court split as non-authoritative.
- Collective Engine now exposes court-seat capacity and attendance limit separately, preventing a rotational opening from being shown to a player as a full day.
- Collective Engine now labels rotations clearly for bookers. Collective Comms can append an iMessage-only weekly calendar attachment after the text send; SMS is intentionally excluded and attachment failure cannot affect the text-delivery record.
- Collective Engine's Fly deployment has a healthy `/health` endpoint, but its intended `collective.1041soft.com` host is still NXDOMAIN; publish that DNS record and the corresponding exact-match Auth0 URLs before calling it publicly reachable. Collective Comms now verifies the producer's canonical handoff digest and blocks publication on a mismatch.
- Review Authority is an active local, read-only review controller. Its Milestone 1 vertical slice can inspect a registered build source, redact and content-address evidence, request a bounded cloud critique, and retain an audit record; it has no public release, UI, correction loop, or configured Git remote.
- XpenseXpunger is a new 1041soft-commercial project at `~/xpensexpunger`. It is a separate Mac-first, local-first expense evidence scanner for Gmail receipts, local files, screenshots, PDFs, CSVs, and later Plaid Transactions. It must not be merged into `pfolio`, and `~/1041soft` is output-only for compatible `finance/scan-results/*.json` exports.
- 1041Soft LLC's Apple Developer Program conversion (Individual to Organization) is now authorized: Apple support case `20000146677819` replied 2026-08-26 that migration could start on the owner's confirmation, and the go-ahead was sent 2026-09-03. The Mercury business account (ending 8399) was made the sole App Store Connect payout bank the same day. Completed 2026-09-14 17:01 UTC: Apple assigned the Program License Agreement to 1041Soft LLC (Team NEAY582ME4), making the LLC the legal owner of every app on the team in both product lines. Owner finished the ASC Business tasks on 2026-09-19 (LLC W-9 Active, agreements accepted, Mercury processing); Apple's activation of the new entity is pending. Privacy policies on 1041soft.com now name 1041Soft LLC as publisher; the billdonner.com catalog says apps are published by 1041Soft LLC (deployed 2026-09-21). Ownership rule: 1041Soft LLC is the legal owner and App Store seller of every app in both product lines. Detail lives in `~/1041soft/formation/articles-of-organization-checklist.md`.

- MedCommons now has a separate native SwiftUI iPhone/iPad DICOM research viewer in `~/medcommons/ios/DicomResearchViewer`, pushed to `billdonner/medcommonsPhp` at `1336dfa` on 2026-09-02. It is research-only/not for diagnosis, bundles public sample fixtures with a manifest and checksums, passed 9 simulator parser/rendering tests, and compiles for `iphoneos` with signing disabled; physical-device install still needs `DEVELOPMENT_TEAM`.

## MedCommons / DICOM Research Viewer

The legacy `billdonner/medcommonsPhp` archive now includes a separate native iPhone/iPad research prototype at `~/medcommons/ios/DicomResearchViewer`. It is a SwiftUI/XcodeGen app, not a modernization of the old PHP runtime and not a clinical viewer. The UI and README keep the boundary explicit: research only, not for diagnosis.

Current capability: open local `.dcm`/`.dicom` files through the iOS document importer, load four bundled public sample objects offline, parse core metadata, render narrow uncompressed 8/16-bit monochrome and 8-bit RGB pixels, provide window/level sliders and CT presets, and show metadata/source provenance. Compressed or encapsulated transfer syntaxes are detected and left metadata-only.

Verification recorded on 2026-09-02: `xcodebuild` simulator XCTest passed 9 tests covering the bundled CT/MR/RTSTRUCT/OHIF fixtures plus implicit VR, MONOCHROME1 inversion, signed rescale windowing, compressed transfer syntax handling, and malformed input. A generic `iphoneos` build passed with `CODE_SIGNING_ALLOWED=NO`; signed installation on Bill's iPhone/iPad still requires setting an Apple development team in Xcode.

## Product Lines

All apps now share **1041Soft** as their company home (owner instruction, September 14).
BillDonner.com is the personal portfolio, with descriptions and outbound company links.
The old `billdonner-free` and `1041soft-commercial` identifiers are retained for stable
pricing/history references. Previously free apps do not become paid because of this move.
The website work did not query or modify App Store Connect metadata or release states.

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
| Highest-priority missing commercial gallery | KinFlash — two galleries (paid Studio on Mac, free Family on iOS); ASC empty for every slot |
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
| 100 Burfords | 1.1 (16) | 1.1 (14) on TestFlight | Source ahead at `14e561a`; the two review P2s are fixed in 15-16, not yet uploaded |
| DoubleQross | 1.0 (415) | iOS 1.0 Ready for Distribution | Approved and publicly downloadable, free, on the App Store (verified 2026-09-23). Earlier TestFlight 412 remains VALID for internal and external testing. |
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
| AmenBeats | com.billdonner.drumbeats | ~/drumbeats | 1.0 build 17 WAITING_FOR_REVIEW since September 16 (ASC verified 2026-09-21); escalate to Developer Support if still waiting September 23 |
| Oenora | com.billdonner.oenora | ~/oenora | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| SharedSpaceLab | com.1041soft.experiments.sharedspacelab | ~/Documents/Codex/Experiments/SharedSpaceLab | Active successor prototype; iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| Screenker | com.screenker.app | github:billdonner/screenker | macOS 1.0 PREPARE_FOR_SUBMISSION |
| SentiPods | com.sentipods.app | ~/sentipods | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| Mallinbook | com.mallinbook.app | github:billdonner/mallinbook | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| workin On | com.workinon.app | ~/workinon | Internal/TestFlight-only; iOS 1.0 retained |
| 100 Burfords | com.billdonner.burfords | ~/100Burfords | 1.0 READY_FOR_SALE; 1.1 draft |
| MURDL 16 | com.billdonner.murdl27 | ~/Murdl27 | iOS 2.2 READY_FOR_DISTRIBUTION, free and publicly downloadable; macOS 2.1 remains live, while macOS 2.2 is PREPARE_FOR_SUBMISSION with no build (verified 2026-09-23). |
| Zerver Monitor | com.billdonner.ZerverMonitor | ~/server-monitor-ios | iOS 1.0 PREPARE_FOR_SUBMISSION |
| Famster | com.famster.app | ~/famster-ios | Concept-only shell; iOS 1.0 PREPARE_FOR_SUBMISSION retained |
| Nagz | com.nagz.app | ~/nagz-ios | Working legacy reference; iOS 1.0 PREPARE_FOR_SUBMISSION retained |
| DoubleQross | com.qross.app | ~/qross | iOS 1.0 READY_FOR_DISTRIBUTION, free and publicly downloadable (verified 2026-09-23). |
| LtWatcher | com.ltwatch.app | archived github:billdonner/clubwatch | Retired; ASC record retained |
| Flasherz Kids | com.billdonner.obo | ~/obo-ios | Removed from inventory 2026-09-08 (obsolete; ASC record deleted) |
| PickleFamilia (legacy record) | com.picklefamilia.app | github:billdonner/picklefamilia-ios | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION; superseded by PickleFamilia Companion (ADR-009) |
| KinFlash Studio (Mac, authoring) | com.billdonner.kinflashstudio | ~/kinflash | Paid; ASC record 6806833310, macOS 1.0.1 builds 3 and 6 VALID via Xcode Cloud |
| KinFlash Family (iOS, player) | com.billdonner.kinflash | ~/kinflash | Free, no IAP; keeps ASC record 6762008872, which needs renaming from "KinFlash" |
| PickledBalls | com.pickledballs.app | ~/pickledballs | iOS 1.0 PREPARE_FOR_SUBMISSION |
| 123 Words | com.123words.app | github:billdonner/123words | 1.11 READY_FOR_SALE; 1.12 draft |
| Cardz Studio | com.billdonner.cardz-studio | ~/cardz-studio-ios | Internal/TestFlight-only; iOS 1.0 retained |

Unmatched or intentionally retained:

- MastPex IOS and MastPex Mac were internal/TestFlight-only apps in the shared MasterIndex Explorer repository; as of 2026-09-05 neither ASC record exists and the repository path is absent on this machine, so both are treated as retired.
- GigStand is retired, removed from all 175 territories, and permanently retained by ASC because it was previously sold.

## Services

| Service | Source | State | Consumers |
|---|---|---|---|
| bd-nagzerver.fly.dev | ~/nagzerver | live | Nagz, workin On, PickledBalls, legacy PickleFamilia |
| bd-cardzerver.fly.dev | ~/card-engine (absent locally; Scoredux checkout at /private/tmp/scoredux-card-engine) | live; feature/scoredux 909f171 deployed 2026-09-11 | Qross, Flasherz Kids, Cardz Studio, card-studio |

Scoredux latest (2026-09-11): build 405 installed and launched on Titanic as
Release without debugger. Panel fixes preserve questions through Quit, charge only
delivered hints, retain timeout review, clarify costs/advice/retry, and repair early
resume and replay pools. 970 unit tests and six UI checks passed across final runs;
two existing skips, no runtime warnings. Scoring v4 and Daily v3 unchanged; no
backend deployment or ASC upload. Details: `qross/docs/scoredux.md`.

Scoredux build 404 (2026-09-11): installed and launched on Titanic as
Release without debugger. Double Cross again picks a second starting corner;
perfect route is 2n, trails remain separate, and protocol v4 resets prior games.
Design/palette selectors moved to Settings > Appearance. Combined tests: 946
passed, 2 skipped; both Double Cross UI flows passed separately. Backend
test-only `3fb998d` is pushed (180 tests passing); live runtime remains `15290cb`
and Daily v3 is unchanged. No ASC upload. See `qross/docs/scoredux.md`.

Scoredux follow-up (2026-09-11): build 403 is installed on Titanic as Release;
incomplete scores scale by estimated route progress. Backend `15290cb` is pushed
and deployed with `/api/v3/daily-scores`; 164 backend tests passed. This supersedes
the build 402/v2 handoff below. Both repositories remain on `feature/scoredux`.

Earlier Scoredux handoff (2026-09-11): Qross build 402 is on `feature/scoredux`, based on
the vibrant UI, with 296 focused app regression tests passing. This is a local
device release, not an ASC upload; see `qross/docs/scoredux.md` for delivery.
The backend's matching branch is pushed and deployed, with 164 tests passing.
Preserve its versioned daily-score routes and challenge checks before deploying
from main. Legacy scores are intentionally reset on first Scoredux launch.
| bd-grubber.fly.dev | ~/grubber | live | SentiPods, grubber clients |
| bd-server-monitor.fly.dev | ~/server-monitor | live | operations, Zerver Monitor |
| bd-pfolio.fly.dev | github:billdonner/pfolio | live | Pfoliolio |
| api.famster.app | ~/nagzerver | alias | Famster concept shell; same deployment and API as Nagzerver |
| bd-oenora-recognition.fly.dev | ~/oenora | live | Oenora |
| bd-clubsync.fly.dev | ~/clubsync | deferred | PickledBalls v2 only |

Fly also contains live infrastructure apps `bd-postgres` and `bd-clubsync-db`. Suspended `bd-arca` (source ~/sharon) and `bd-podcast-brands` were destroyed 2026-09-08 by owner decision.

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

- **1041soft.com:** unified 14-entry portfolio deployed through GitHub Pages. On September 23, commit `3c3a58d` added direct App Store download links and free-release copy for MURDL 16 and DoubleQross; GitHub Pages propagation follows the push.
- **billdonner.com:** local source `~/website`, commit `8262c66`, published to IONOS September 14. All 24 changed public files uploaded successfully. Homepage, catalog, app descriptions, screenshot/privacy forwarding pages, biography, and music pages were verified live.
- The canonical shared description file is `~/1041soft-site/data/portfolio.json`. Run `python3 build_apps.py --catalog ../1041soft-site/data/portfolio.json` in `~/website` to synchronize the personal portfolio. The personal ASC `--refresh` workflow is retired.
- MasterIndex's `publish/billdonner.com/` tree and `tools/generate_billdonner_apps.py` are historical publication artifacts; do not use them to overwrite the current website.
- Existing app descriptions were retained. Public copy still needs reconciliation with the newer PickleFamilia Companion name and KinFlash Family/Studio split recorded elsewhere in this index.
- Legacy `/murdl/privacy/` on BillDonner.com still returns 404. The current `/apps/murdl/privacy/` forwarding page and `https://1041soft.com/murdl/privacy/` work. Root `/murdl/` redirects correctly; the old root privacy route remains a compatibility follow-up.

### Company Website — `1041soft.com` (updated 2026-09-23)

Canonical company app home at `~/1041soft-site`, public repo `billdonner/1041soft-site`,
served by GitHub Pages over HTTPS. Added homepage entries for AmenBeats, MURDL 16,
123 Words, 100 Burfords, PickledBalls, and workinOn alongside the existing eight.
Support/privacy content and required assets were carried over from their existing sources.

On September 23, MURDL 16 and DoubleQross were recorded as free, publicly downloadable App Store releases, with direct store links added to the company homepage.

`doubleqross.com` directly serves the IONOS `/qross` public site. ASC marketing,
support and privacy URLs all use this domain (verified September 12, 2026).
Legacy 1041soft pages redirect here, commit `0fafed1`. GitHub Pages had again
exposed `main:/docs`; it now publishes only redirects from `public-site-20260912`
(`18672c7`), with two internal URLs verified 404 after rebuilding. Do not restore
whole-docs publishing. The portfolio `/apps/qross/` URL is parked; catalog works.
Release 408 is installed/launched on Titanic without debugger (September 13).
It adds first-question-only Double Cross Jumble rescue: 980 unit tests passed,
two existing skips, five final UI scenarios and a wording rerun passed. Pending
decisions survive relaunch. Review: `qross/docs/reviews/opening-rescue/README.md`.
The preceding 407 second-crossing work also remains included.
Two AI reviewers approved the second-crossing treatment; 975 unit tests passed
with two existing skips, and three final UI playthroughs passed, including large
text. Review: `qross/docs/reviews/second-crossing/README.md`. The September 12
content verification remains the latest public-site check. ASC binary remains 395 selected / 396 newest uploaded;
matching screenshots, privacy questionnaire and accessibility review remain gates.
Details: `qross/docs/content-consistency-2026-09-11.md`.

Owner reported purchasing `picklefamilia.com` and `picklefamilia.app` through IONOS on 2026-08-29. As of 2026-09-13 collective-engine serves the family page on that host (`FAMILY_HOST`); DNS at IONOS and `fly certs add` are the remaining steps.
DNS, SSL, redirects, canonical-domain choice, auto-renewal, and renewal pricing are not yet verified.
The same IONOS dashboard showed 88.92 GB of webspace used, 12,963 files, 7 SFTP users, 2 standard
databases, PHP Extended Support active, a Site Scan warning for vulnerable websites, and Performance
Level 2; no payment or credential data is recorded here.

**Rule: never enable GitHub Pages on a private repo.** Pages publishes `docs/` to the
open web regardless of repo visibility, and bills Actions minutes on private repos.
Add a subpath here instead.

This site is the company home for all apps. The now-live `billdonner.com/apps/` personal portfolio keeps descriptions and links outward; the earlier exclusive domain assignments are superseded.

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
- 1041Soft LLC's enrollment `CX276BJ992` was approved September 13, confirmed by Apple September 14 under case `20000146677819`. Full membership migration completion and seller-name change remain unverified; awaiting Apple's reply on whether migration is affecting AmenBeats 1.0 build 16.

## Operational Rule

Use `current/index.json` as source of truth, `tasks/index.json` for recurring routing, and `current/handoffs/index.json` for next-cycle directives. Public websites and `site/` are presentation surfaces and must be checked against JSON, ASC, repository settings, and live deployments.
