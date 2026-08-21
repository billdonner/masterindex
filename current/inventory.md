# MasterIndex Inventory

As of Friday, August 21, 2026.

## Scope

- Reconciled App Store Connect, active GitHub sources, local repositories, Fly deployments, and public product URLs.
- Applied no handoff directives because `current/handoffs/index.json` has none.
- Performed the requested retirements, operational fixes, website publications, and feedback-workflow replacement; observed facts and remaining product gaps are kept distinct below.
- Added explicit `masterIndexStatus` classifications to every entity and tracked repository, and removed the temporary `mixed-citizen` holding tier so every current record is now either `good-citizen` or `not-good-citizen`.
- **August 21 non-app evaluation pass.** Every entity with `kind != "app"` was verified live against `flyctl`, HTTP health probes, GitHub repository state, and local checkouts. The pass corrected four wrong records, rebuilt the stale `flyOperations` block, and gave entity records to nineteen non-app repositories that previously existed only in `repos[]` and were therefore outside `entityCoveragePolicy`.

## Executive Summary

- ASC contains 20 app records: 19 map in the primary ASC inventory and GigStand is the intentionally retained retired record. The two MastPex records and Flasherz Kids were deleted from ASC by the owner on 2026-08-19; no further deletions are pending.
- LtWatcher is retired. `billdonner/clubwatch` is archived read-only and its ASC record is retained.
- Clubsync is deferred until PickledBalls v2. Its application tier is not deployed; `bd-clubsync-db` remains deployed to preserve data.
- Card Server is retired after consumer and replacement checks. `billdonner/card-server` is archived, its Fly descriptor is removed, and Card Engine remains the sole verified source for `bd-cardzerver.fly.dev`.
- Server Monitor is deployed and its own probes work, but its production config still targets the deliberately suspended Nagzerver and has logged 7,755 consecutive failures there, so the dashboard sits in a permanent error state that no longer signals anything.
- **Nagzerver is suspended.** The shutdown the owner announced on 2026-08-18 is complete: `flyctl` reports the app suspended and `/healthz` times out. Three dependents were never updated — Server Monitor, `workinon-mcp` widget push, and `nagz-web` — and the Fly secrets still need rotation.
- **Collective Engine is deployed.** `bd-collective-engine` has been running on Fly since 2026-08-19 with its own `bd-collective-db` Postgres 18.1 cluster, contradicting the previous record that claimed no runtime existed. Its entity kind moved from `architecture-proposal` to `backend`. The architecture freeze the proposal defines is still unapproved.
- The registry tracks 57 repositories and 57 entities, 34 of which are non-app.
- Canonical-main records for local-model-lab, adspill, and the Oenora Recognition API are preserved. The local-model-lab checkout path was corrected — it is not on this machine.
- The `billdonner.com/apps` catalog is **stale on IONOS**: the live page still advertises 19 active apps and still lists Flasherz Kids, whose ASC record was deleted 2026-08-19. Regenerating from the current index yields 18 entries and omits it.
- App Feedback replaces the repeating TestFlight email loop with a local 41-item triage inbox across 21 active ASC apps. The working data stays on this Mac; client-encrypted recovery snapshots are versioned in iCloud Drive.
- The portfolio now has two explicit product lines: BillDonner.com apps are permanently free, while 1041soft.com products carry the commercial-grade release and support commitment.
- Nagz, Famster, and SharedSpaceLab are now recorded as one household-communications lineage rather than three independent products: SharedSpaceLab is the active successor prototype, Nagz is the working legacy reference, and Famster is a concept-only shell.
- Nagzerver was mixed production infrastructure for Nagz, PickledBalls, PickleFamilia, and workin On until its 2026-08-21-verified suspension. Its exact deployed source remains preserved on private branch `recovery/deployed-2026-06-30` because Git `main` could not reproduce production at the time.
- `grubber-ios` is obsolete by owner decision; SentiPods is the current grubber client.
- `doubleqross.com` is live at IONOS. Apex and `www` resolve, present the included Sectigo certificate through February 10, 2027, and redirect over HTTPS to the maintained `1041soft.com/qross/` page. The stale private-repo Pages link was removed.
- DoubleQross 1.0 (392) now has refreshed Garland-era iPhone and iPad captures, updated Screenker projects, and exact approval exports scored provisionally at 94 and 93. ASC is unchanged pending human approval.
- The screenshot program now distinguishes Screenker provenance, critique score, freshness, publication, and live ASC parity. Nine apps have verified Screenker history; the immediate correction schedule and future release rubric are in `docs/screenshot-operations.md`.
- KinFlash is assigned to billdonner.com for near-term public release as a kids app on the free line, superseding the 2026-08-14 assignment to 1041soft.com and reconfirmed by the owner on 2026-08-20. Flasherz Kids is obsolete and its ASC record was deleted on 2026-08-19. Cardz Studio and workin On are internal-use apps expected to remain on TestFlight rather than proceed to public App Store release. MastPex was retired outright and its ASC records were deleted on 2026-08-19.

## MasterIndex Citizenship

The canonical JSON now makes this explicit instead of leaving it inferred.

- Entities: 35 `good-citizen`, 22 `not-good-citizen`, across 57 records.
- Repositories: 40 `good-citizen`, 17 `not-good-citizen`.
- Every `not-good-citizen` entity and repository now carries a machine-readable `masterIndexStatusReason` in `current/index.json`.
- The August 21 pass moved three previously good entities to `not-good-citizen` on verified evidence: `card-engine-backend` (local checkout diverged from the deployed source), `nagzerver-backend` (suspended with unrotated secrets and stale dependents), and `local-model-lab` (recorded checkout path does not exist here). `portfolio-app-directory` joined them because the live catalog lists a deleted product.

### Good citizens

These have a clear lifecycle, a mapped source of truth, and no material open trust gap in the inventory.

- Apps and services: DoubleQross, PickledBalls, Pfoliolio, 100 Burfords, Screenker, grubber, card-engine, server-monitor, pfolio, Oenora Recognition API.
- Portfolio surfaces and tooling: 1041soft.com, Bill Donner Apps, App Feedback.
- Repositories: `~/qross`, `~/pickledballs`, `~/pfolio-app`, `github:billdonner/pfolio`, `~/100Burfords`, `github:billdonner/screenker`, `~/grubber`, `~/card-engine`, `~/server-monitor`, `~/app-feedback`, `~/Flyz`, `~/masterindex`, `~/collective-engine` (Collective Engine architecture proposal and normative Codex handoff; private `github:billdonner/collective-engine`; `~/familia` is a legacy symlink to it, not a separate repository).

### Not good citizens

These are intentionally retained, but they are retired, obsolete, placeholder, missing, or otherwise weak records rather than clean active portfolio assets.

- Apps and services: Mallinbook, KinFlash, PickleFamilia, Nagz, Flasherz Kids, Cardz Studio, Famster, LtWatcher, picklefortunes, grubber-ios, clubsync, card-server.
- Repositories: `github:billdonner/zkraper`, `github:billdonner/asc-feedback`, `~/peerlink`, `~/card-server`, `~/cardz-studio-ios`, `~/clubsync`, `~/clubwatch`, `~/famster-ios`, `~/grubber-ios`, `~/nagz-ios`, `~/obo`, `~/obo-ios`, `~/picklefortunes`, `github:billdonner/picklefamilia-ios` (archived), and `~/Documents/Codex/2026-08-02/masterindex-explorer`.

### Review of Non-Good Records

- True lifecycle decisions: Nagz, Flasherz Kids, Cardz Studio, Famster, LtWatcher, picklefortunes, grubber-ios, clubsync, card-server, zkraper, and asc-feedback are non-good because the owner has already decided they are legacy, obsolete, internal-only, deferred, retired, or placeholder assets.
- Active but blocked by real product debt: KinFlash and Mallinbook are non-good because each still has an unresolved public-release, metadata, or platform-posture problem rather than merely stale wording in the index. KinFlash is now narrowed to owner-side hosting, ASC, and release-decision work rather than repo execution debt; Mallinbook is now narrowed to the live privacy-page placeholder and follow-on ASC actions rather than repo execution debt.
- Local-environment or routing problems: `~/peerlink` is missing locally and blocks reproducible PickledBalls builds here; `~/obo` remains a historical docs hub around an obsolete line; `github:billdonner/picklefamilia-ios` is archived, remote-only, and outside the current active workstream.
- The highest-value repairs outside MasterIndex are now choosing KinFlash public hosting plus release-channel and ASC submission answers, and replacing Mallinbook's live privacy-page placeholder before completing its ASC follow-through.

### KinFlash Follow-up

`~/kinflash` is no longer non-good. On Saturday, August 15, 2026, the repo-side release work was verified: iOS Debug and Release builds succeeded, 249 unit tests passed with 31 legitimate skips, privacy manifests were confirmed in the built app, and the screenshot rig was proven end-to-end for all 7 iPhone and 7 iPad slots at brief-conformant geometry.

KinFlash the app remains non-good because the remaining blockers are owner-facing rather than repo-facing:

- No publicly reachable hosting exists yet for support and privacy URLs because the private repo has Pages disabled and `homepageUrl` is empty.
- The Mac release channel remains undecided.
- Local build 66 has not been uploaded; ASC build 65 is VALID but is not the intended release candidate.
- ASC App Privacy answers, final screenshot selection/captions, and final slot-1 composition remain open.

### Nagzerver Follow-up

`~/nagzerver` is no longer non-good. On Saturday, August 15, 2026, the source-of-truth problem was resolved: `recovery/deployed-2026-06-30` was confirmed as a strict fast-forward superset of `main`, merged cleanly, and local `main` was verified against the live 163-path API surface with zero API drift. Two security fixes landed in Git: the SPA catch-all no longer allows arbitrary file reads, and production test-helper endpoints are now fail-closed behind `NAGZ_ENABLE_TEST_HELPERS=1`.

Production still needs operational follow-through:

- Fly release v100 has not yet been redeployed with those fixes.
- Secrets should be rotated because `/proc/self/environ` was reachable before the code fix.
- `fly.toml` still has no `release_command`, so migrations remain a manual post-deploy step.

### Oenora Follow-up

`~/oenora` is no longer non-good. On Saturday, August 15, 2026, the Mac distribution posture was resolved and documented: Oenora for Mac is a notarized Developer ID direct download under `com.billdonner.oenora.mac`, governed by `docs/decisions/ADR-007-mac-distribution-channel.md`, with a reproducible release path in `scripts/notarize-mac.sh`. The iOS side is aligned: `project.yml` build 7 matches ASC build 7, and the public Founders Beta TestFlight link is enabled.

The remaining Oenora gaps are now explicit external follow-through, not repo ambiguity:

- The empty ASC `MAC_OS` version under `com.billdonner.oenora` is a leftover app-creation artifact and should be deleted by owner action.
- The Developer ID Application private key is missing from the current build machine keychain, so no new notarized Mac build can be produced there until the key is restored.
- `1041soft.com/oenora/` support and privacy pages still do not exist.
- No public download host has been chosen yet for the notarized Mac artifact.
- The iOS age rating remains unset.

## Product Lines

### BillDonner.com — always free

Personal utilities, experiments, and children-oriented apps. Users are never charged; a Mac
version and MCP surface are optional. Assignment is decided by audience, not capability.
KinFlash belongs here and is planned for near-term public release from billdonner.com: it is a
kids app, so it sits on the free line even though it ships a capable Mac sibling and an MCP
surface. amenbeats is also assigned here. `workin On` remains in this product family but is
internal-use/TestFlight-only rather than a public release.

### 1041soft.com — commercial

Products intended for sale or another explicit revenue model. These carry a higher quality,
testing, documentation, privacy, and support bar; they should normally have a real Mac version
and an MCP or automation surface when that fits the product. No new app has been assigned here
since the 2026-08-18 audience-based split; KinFlash was briefly assigned on 2026-08-14 and moved
to the free line.

The remaining apps are not yet classified. Presentation drift remains open until that is done:
the BillDonner.com generator currently includes every active app, and 1041soft.com still serves
`/workinon/` even though workin On is internal-only. KinFlash is settled on billdonner.com and needs no move.
Flasherz Kids is resolved: its ASC record was deleted on
2026-08-19, so it left `ascApps.mapped` and the regenerated catalog no longer lists it.

Regenerating the catalog also surfaced a filter hazard worth remembering.
`tools/generate_billdonner_apps.py` drops any entity whose status is `archived` or `retired`,
and Mallinbook and PickledBalls were both miscoded `archived` while still being live products.
Both were corrected to `asc-mapped` on 2026-08-19 before the catalog was regenerated. The
generator now takes its "reconciled on" date from the index `generatedAt` instead of a
hardcoded string.

## Screenshot Program

The canonical screenshot program now lives in `current/index.json` under
`screenshotOperations`, with machine-readable lane and board-state tracking. The August 14
read-only App Store Connect audit established the baseline by inspecting every mapped version,
locale, and screenshot display type, then correlating those live sets with repository history
and Screenker projects. A gallery is not called current merely because it is present in ASC or
once received a high score.

| State | Apps |
|---|---|
| Current, scored, and published | 100 Burfords (iPhone 88/iPad 90) |
| Current internal/TestFlight evidence; no public gallery work | workin On (93) |
| Current and published, below the commercial target | Screenker (86) |
| Current local candidate awaiting human approval; ASC unchanged | DoubleQross (provisional iPhone 94/iPad 93) |
| Published but score or captures are stale | PickledBalls, 123 Words, amenbeats, Pfoliolio |
| Screenker projects exist but critique coverage is incomplete | Mallinbook (Mac 89; iPhone/iPad unscored) |
| ASC device coverage exists without Screenker critique | SentiPods |
| Local captures exist but ASC is empty | Oenora iOS |
| Active ASC release record is empty | Zerver Monitor |
| Highest-priority missing gallery | KinFlash, near-term billdonner.com release, 85-point gate |
| Defer until lifecycle or release decision | SharedSpaceLab, PickleFamilia |
| Internal functional evidence only | Cardz Studio, workin On |
| No new screenshot work | LtWatcher, grubber-ios, Famster, Nagz |

The current board priority is: 123 Words first; then PickledBalls; then amenbeats and
Pfoliolio; then Mallinbook and SentiPods; then KinFlash, Oenora, Zerver Monitor, Screenker,
and a verify-only pass for 100 Burfords. DoubleQross is approved-local but deferred by owner for
now, so it is held out of the active queue. Internal-only and archived lines are tracked
separately so they do not pollute the public-release queue. The detailed lane model and per-app
execution steps are in `docs/screenshot-operations.md`.

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
- **Superseded 2026-08-21.** The Nagzerver HTTP target now fails permanently because the service was intentionally suspended — 7,755 consecutive failures at last check — so the dashboard reports a standing 1-errored-of-7 state. Remove or explicitly retire that target; the Nagzerver Redis and Postgres targets still probe successfully and can stay.

### Version and build drift

| App | Source | App Store Connect | Result |
|---|---:|---:|---|
| Pfoliolio | 35 | iOS + macOS 35 VALID | Aligned |
| amenbeats | 8 | 8 VALID | Aligned in GitHub commit `aea6725` |
| 100 Burfords | 1.1 (9) | 1.1 (9) draft | Aligned in GitHub commit `48192f3` |
| DoubleQross | 392 | 392 VALID | Aligned; bundle id remains com.qross.app |
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
| PickleFamilia | com.picklefamilia.app | archived github:billdonner/picklefamilia-ios | Archived historical line; ASC iOS + macOS 1.0 PREPARE_FOR_SUBMISSION retained |
| KinFlash | com.billdonner.kinflash | ~/kinflash | Near-term billdonner.com release; iOS 1.0 PREPARE_FOR_SUBMISSION |
| PickledBalls | com.pickledballs.app | ~/pickledballs | iOS 1.0 PREPARE_FOR_SUBMISSION |
| 123 Words | com.123words.app | github:billdonner/123words | 1.11 READY_FOR_SALE; 1.12 draft |
| Cardz Studio | com.billdonner.cardz-studio | ~/cardz-studio-ios | Internal/TestFlight-only; iOS 1.0 retained |

Unmatched or intentionally retained:

- GigStand is retired, removed from all 175 territories, and permanently retained by ASC because it was previously sold.

## Services

All states below were verified live on 2026-08-21.

| Service | Source | State | Consumers |
|---|---|---|---|
| bd-cardzerver.fly.dev | ~/card-engine | live | Qross, Cardz Studio, card-studio |
| bd-grubber.fly.dev | ~/grubber | live | SentiPods, grubber clients |
| bd-server-monitor.fly.dev | ~/server-monitor | live | operations, Zerver Monitor |
| bd-pfolio.fly.dev | github:billdonner/pfolio | live | Pfoliolio |
| bd-oenora-recognition.fly.dev | ~/oenora | live | Oenora |
| bd-collective-engine.fly.dev | ~/collective-engine | live | none yet — deployed prototype, not a production dependency |
| bd-nagzerver.fly.dev | ~/nagzerver | **suspended** | shutdown complete; former consumers now stranded |
| api.famster.app | ~/nagzerver | **down** | alias to the suspended Nagzerver deployment |
| bd-clubsync.fly.dev | ~/clubsync | deferred | PickledBalls v2 only |

Health endpoints differ per service and are not interchangeable: Grubber and Nagzerver use `/healthz`; Card Engine, pfolio, Oenora Recognition, and Collective Engine use `/health`. On Grubber, `/`, `/status`, and `/shows` all return 404 — earlier notes citing them were wrong.

Fly also contains deployed infrastructure apps `bd-postgres`, `bd-clubsync-db`, and `bd-collective-db`, plus suspended `bd-arca` and `bd-podcast-brands`. `bd-arca` and `bd-podcast-brands` have no entity, no repository, and no recorded owner decision — only this narrative mention. `bd-clubsync-db` is on `flyio/postgres-flex` 17.2 with 17.7 available, so the deferred database carries patch debt as well as cost.

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
- `com.billdonner.app-feedback-collect` runs at login and every two hours; `com.billdonner.app-feedback-server` keeps the dashboard available.
- The retired `zkraper` and `asc-feedback` private repositories contain replacement notices and are archived. Their email, manual watermark, and Qross-only flows must not be scheduled.

## Website Publication

- `tools/generate_billdonner_apps.py` generates the active catalog from canonical JSON.
- `publish/billdonner.com/apps/index.html` lists 19 active ASC-mapped apps and omits retired LtWatcher.
- `publish/billdonner.com/apps/pfoliolio/index.html` supplies the marketing and support route expected by ASC.
- `publish/billdonner.com/apps/oliopfolio/index.html` redirects the obsolete name to Pfoliolio.
- The generated files were published to IONOS on 2026-08-14 and match the live HTTPS responses by SHA-1.
- The previous catalog and LtWatcher directory were retained under `/_archive`; the public LtWatcher route now returns 404.

### URL Standardization (2026-08-14)

`1041soft.com` is the canonical support, marketing, and privacy host. ASC URLs for
**12 apps** were standardized onto it and each verified 200: Qross, Nagz, workin On,
Flasherz Kids, Zerver Monitor, Mallinbook, SentiPods, Pfoliolio, Screenker, Oenora,
SharedSpaceLab, PickleFamilia. Flasherz Kids has since dropped out of that set: its ASC
record was deleted on 2026-08-19.

**Do not regenerate ASC support routes back to `billdonner.com/apps/...`.**
`tools/generate_billdonner_apps.py` builds the billdonner.com catalog from this index
and previously supplied the ASC support route for several apps. That catalog remains a
portfolio index; it is no longer the ASC support surface.

Deliberately not standardized: 100 Burfords and 123 Words (public repos, resolve);
PickledBalls (`pickledballs.billdonner.com`, its own domain); Famster, KinFlash,
LtWatcher, amenbeats (billdonner.com routes resolve, but none has a privacy URL);
Cardz Studio (nothing set); GigStand (`gigstand.net` is dead, and
the app is retired).

### Pages sweep (2026-08-14)

Every private repository was swept for enabled GitHub Pages. Disabled on qross, nagz,
nagz-ios, workinon, obo-ios, server-monitor-ios, mallinbook, pfolio-app, and
picklefamilia-ios (archived historical line).

Three remain enabled **deliberately**:

- `nagzerver` publishes **nagz.online** from `gh-pages`. Built output only — internal
  docs on `main` are not exposed (`ARCHITECTURE.md`, `POLICY_MATRIX.md`,
  `API_SURFACE.md` all verified 404). Do not disable.
- `pickledballs` publishes **pickledballs.billdonner.com** from `gh-pages` and serves
  the live PickledBalls ASC URLs. Do not disable.
- `alities-mobile` publishes `main/docs` and exposes `appstore-copy.md` (verified 200).
  Minor; migrate or disable when convenient.

The rule is narrower than "no Pages on private repos": never publish a private repo's
`docs/` directory, because that is where internal material lives. Publishing built
output from a `gh-pages` branch is safe for exposure, though it still bills Actions
minutes.

### Company Website — `1041soft.com` (live 2026-08-14)

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

**Rule: never enable GitHub Pages on a private repo.** Pages publishes `docs/` to the
open web regardless of repo visibility, and bills Actions minutes on private repos.
Add a subpath here instead.

This site coexists with the now-live `billdonner.com/apps` portfolio catalog. The owner has now
assigned workin On exclusively to the permanently free BillDonner.com line, making the live
1041soft.com `/workinon/` path a presentation drift rather than a canonical product home.

## Preserved Main-Only Facts

- `local-model-lab` is active as a lab and the canonical old-corpus leaderboard has been repaired. **Corrected 2026-08-21:** the checkout is *not* on this machine — neither `~/mlxsrv/local-model-lab` nor `~/mlxsrv` exists here. The repository was pushed 2026-08-20, so the lab runs on the owner's second Mac and must be audited there. The Apple 4+ content-screening run with a 2026-08-17 ETA therefore has no recorded outcome.
- `adspill` remains a two-person advertising-capacity research sandbox, and is now explicitly parked: no pushes since 2026-07-29, Bill in an observer role, and no activity expected until the Northwoods League in-stream ad-rights question is answered.
- The Oenora Recognition API is live at `bd-oenora-recognition.fly.dev` and remains an Oenora dependency.
- Oenora's public TestFlight invite, approved build 6, submitted build 7 with sealed-case tracking, three-device CloudKit soak, repaired recognition configuration, and notarized native Mac delivery are retained.

## Remaining Gaps

- Mallinbook's replacement privacy URL now resolves at `https://1041soft.com/mallinbook/privacy`, but the published page still contains literal placeholder text. The corrected policy text is in the repo, but 1041soft-site must be updated and redeployed before the ASC field can be pointed at a truthful page.
- SentiPods public-link drift is closed. ASC privacy, support, and marketing URLs now resolve to the verified `https://1041soft.com/sentipods/` surfaces; the remaining blockers are ASC-console-only metadata fields and age rating choices.
- **Closed 2026-08-14 — unintended public exposure.** Seven private repos (qross, nagz, nagz-ios, workinon, obo-ios, server-monitor-ios, mallinbook) were publishing `docs/` to the open web through GitHub Pages. Verified world-readable at the time: qross business plans, risk register, `architecture/cardzerver-operational-roadmap.md`, `decisions/ADR-009-secret-management.md`, `carol-claude-code-instructions.md`; and nagz `DEPLOYMENT_PLAN.md`, `CODE_REVIEW_FINDINGS.md`, `CONTRIBUTOR_GUIDE.md`. Scanned for live credential patterns and found none. Pages disabled on all seven; every path re-verified 404.
- `nagz/docs/.well-known/apple-app-site-association` never actually served — Jekyll ignores dot-directories — so universal links have never worked from that domain. Not a regression from the migration.
- Age ratings remain unset for Oenora, SharedSpaceLab, and SentiPods pending owner decisions.
- `~/peerlink` is missing and no matching GitHub repository was found, so PickledBalls project generation remains blocked on this machine.
- ~~`1041soft.com` still points at Namecheap forwarding/parking; HTTPS is unusable.~~ **Resolved 2026-08-14** — see Company Website below. Apex now serves from GitHub Pages over enforced HTTPS.
- Oenora's existing ASC macOS 1.0 record has no builds after the project deliberately replaced Catalyst with a native Developer ID target using `com.billdonner.oenora.mac`.
- Nagzerver Git `main` does not reproduce the deployed PickledBalls and PickleFamilia API. The exact deployed source is preserved on `recovery/deployed-2026-06-30`, but its one failing schedule test must be resolved before review and merge.
- SharedSpaceLab's public product name, product-line assignment, business model, and eventual server boundary remain undecided. Famster must not be expanded as a parallel implementation while those decisions are open.

### Opened by the August 21 non-app pass

- **The index has forked — resolve before anything else.** `current/index.json` exists in two actively maintained lineages. This branch (`fix/doubleqross-com`) has the newer `generatedAt` (2026-08-19); `origin/main` has the newer commits (32 of them, through 2026-08-21) and three entities absent here — `oenora-merchant`, `collective-comms`, and `collective-engine` — while still carrying the two MastPex records the owner deleted. The same system is recorded under two different ids: `collective-engine` on main, `collective-engine-backend` here. Consumers read main, so main is the published lineage. Do not merge or force-push either direction without an owner decision.
- **Fly app status is not a liveness signal.** `bd-oenora-recognition` reads `suspended` in `flyctl apps list` because it is scale-to-zero, yet `/health` returns 200 after a ~2s cold start. Nagzerver's shutdown was confirmed the reliable way instead — `flyctl machines list` reports no machines at all, and `/healthz` times out at 30s.
- **Nagzerver shutdown residue.** Server Monitor still probes the dead endpoint, `workinon-mcp` can no longer deliver silent-APNs widget updates, `nagz-web` has no reachable API tier, and the Fly secrets are still unrotated on the assumption they were exposed before the app was turned off.
- **Card Engine local checkout drift.** `~/card-engine` is 27 commits behind and 1 ahead of `origin/main` with a dirty working tree, so the recorded source for the live `bd-cardzerver` deployment is not trustworthy. Reconcile before editing the backend from this machine.
- **Collective Engine governance.** The service is deployed with a production database while the architecture freeze its own proposal defines is still unapproved and no Release 1 build was authorized. The record is now accurate; the decision is the owner's.
- **Unmapped Fly apps.** `bd-arca` and `bd-podcast-brands` have been suspended for over two months with no entity, repository, or decision. Map or destroy them — a suspended app still holds its name and any attached volumes.
- **Public catalog stale.** `billdonner.com/apps` advertises 19 apps and lists deleted Flasherz Kids. The generator now produces 18 and its output is otherwise byte-identical, so republishing is safe; this pass did not publish to IONOS.
- **Clubsync database patch debt.** `bd-clubsync-db` runs healthy on Postgres-flex 17.2 with 17.7 available while its application tier stays undeployed. Either update the image or snapshot and destroy it as an explicit decision.
- **Entity coverage rule.** Nineteen repositories — including `card-studio`, listed as an active project in the owner's global `CLAUDE.md`, and `peerlink`, whose absence blocks local PickledBalls builds — existed only in `repos[]` and so were never touched by `entityCoveragePolicy`, which is keyed on `entities[].id`. They now have entity records and empty `entryTasks` keys. Standing rule: a repository that matters enough to appear in `repos[]` needs an entity id, or nothing recurring will ever check it.

## Operational Rule

Use `current/index.json` as source of truth, `tasks/index.json` for recurring routing, and `current/handoffs/index.json` for next-cycle directives. Public websites and `site/` are presentation surfaces and must be checked against JSON, ASC, repository settings, and live deployments.
