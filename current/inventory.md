# MasterIndex Inventory

As of Friday, August 14, 2026.

## Scope

- Reconciled App Store Connect, active GitHub sources, local repositories, Fly deployments, and public product URLs.
- Applied no handoff directives because `current/handoffs/index.json` has none.
- Performed the requested retirements and operational fixes; observed facts and unresolved publication access are kept distinct below.

## Executive Summary

- ASC contains 23 app records: 20 map to repositories, two MastPex records are placeholders, and GigStand is the intentionally retained retired record.
- LtWatcher is retired. `billdonner/clubwatch` is archived read-only and its ASC record is retained.
- Clubsync is deferred until PickledBalls v2. Its application tier is not deployed; `bd-clubsync-db` remains deployed to preserve data.
- Card Server is retired after consumer and replacement checks. `billdonner/card-server` is archived, its Fly descriptor is removed, and Card Engine remains the sole verified source for `bd-cardzerver.fly.dev`.
- Server Monitor is repaired and deployed. Its seven production targets omit Clubsync and its direct Nagzerver and Card Engine HTTP probes return 200.
- The registry tracks 53 repositories, of which 51 remain active after the two retirements.
- Canonical-main records for local-model-lab, adspill, and the Oenora Recognition API are preserved.
- A canonical `billdonner.com/apps` publication bundle is now generated from `current/index.json`; the live IONOS site cannot be updated until its SFTP password is supplied.

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
| Qross | 392 | 392 VALID | Aligned; clean worktree used without touching the active feature branch |
| 123 Words | 1.12 (59) | 59 VALID | Aligned to the open 1.12 train in commit `3f89587` |
| SentiPods | iOS 20, macOS 21 | macOS 21 VALID | Aligned |

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
| SharedSpaceLab | com.1041soft.experiments.sharedspacelab | ~/Documents/Codex/Experiments/SharedSpaceLab | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| Screenker | com.screenker.app | github:billdonner/screenker | macOS 1.0 PREPARE_FOR_SUBMISSION |
| SentiPods | com.sentipods.app | ~/sentipods | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| Mallinbook | com.mallinbook.app | github:billdonner/mallinbook | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| workin On | com.workinon.app | ~/workinon | iOS 1.0 PREPARE_FOR_SUBMISSION |
| 100 Burfords | com.billdonner.burfords | ~/100Burfords | 1.0 READY_FOR_SALE; 1.1 draft |
| Zerver Monitor | com.billdonner.ZerverMonitor | ~/server-monitor-ios | iOS 1.0 PREPARE_FOR_SUBMISSION |
| Famster | com.famster.app | ~/famster-ios | iOS 1.0 PREPARE_FOR_SUBMISSION |
| Nagz | com.nagz.app | ~/nagz-ios | iOS 1.0 PREPARE_FOR_SUBMISSION |
| Qross | com.qross.app | ~/qross | iOS 1.0 PREPARE_FOR_SUBMISSION |
| LtWatcher | com.ltwatch.app | archived github:billdonner/clubwatch | Retired; ASC record retained |
| Flasherz Kids | com.billdonner.obo | ~/obo-ios | iOS 1.0 PREPARE_FOR_SUBMISSION |
| PickleFamilia | com.picklefamilia.app | github:billdonner/picklefamilia-ios | iOS + macOS 1.0 PREPARE_FOR_SUBMISSION |
| KinFlash | com.billdonner.kinflash | ~/kinflash | iOS 1.0 PREPARE_FOR_SUBMISSION |
| PickledBalls | com.pickledballs.app | ~/pickledballs | iOS 1.0 PREPARE_FOR_SUBMISSION |
| 123 Words | com.123words.app | github:billdonner/123words | 1.11 READY_FOR_SALE; 1.12 draft |
| Cardz Studio | com.billdonner.cardz-studio | ~/cardz-studio-ios | iOS 1.0 PREPARE_FOR_SUBMISSION |

Unmatched or intentionally retained:

- MastPex IOS and MastPex Mac are placeholders with no app repository.
- GigStand is retired, removed from all 175 territories, and permanently retained by ASC because it was previously sold.

## Services

| Service | Source | State | Consumers |
|---|---|---|---|
| bd-nagzerver.fly.dev | ~/nagzerver | live | Nagz, workin On, PickledBalls |
| bd-cardzerver.fly.dev | ~/card-engine | live | Qross, Flasherz Kids, Cardz Studio, card-studio |
| bd-grubber.fly.dev | ~/grubber | live | SentiPods, grubber clients |
| bd-server-monitor.fly.dev | ~/server-monitor | live | operations, Zerver Monitor |
| bd-pfolio.fly.dev | github:billdonner/pfolio | live | Pfoliolio |
| api.famster.app | unidentified | live | Famster |
| bd-oenora-recognition.fly.dev | ~/oenora | live | Oenora |
| bd-clubsync.fly.dev | ~/clubsync | deferred | PickledBalls v2 only |

Fly also contains live infrastructure apps `bd-postgres` and `bd-clubsync-db`, plus suspended `bd-arca` and `bd-podcast-brands`.

## Website Publication

- `tools/generate_billdonner_apps.py` generates the active catalog from canonical JSON.
- `publish/billdonner.com/apps/index.html` lists 19 active ASC-mapped apps and omits retired LtWatcher.
- `publish/billdonner.com/apps/pfoliolio/index.html` supplies the marketing and support route expected by ASC.
- `publish/billdonner.com/apps/oliopfolio/index.html` redirects the obsolete name to Pfoliolio.
- The live IONOS site remains unchanged because no usable SFTP credential exists in the keychain, repository configuration, or available browser session.

## Preserved Main-Only Facts

- `local-model-lab` is parked, with its historical MLX/Qross corpus benchmark results retained.
- `adspill` remains a two-person advertising-capacity research sandbox.
- The Oenora Recognition API is live at `bd-oenora-recognition.fly.dev` and remains an Oenora dependency.
- Oenora's public TestFlight invite and external-beta history are retained alongside the newer build 3 ASC observation.

## Remaining Gaps

- The IONOS SFTP password is required to publish the prepared `billdonner.com` fix.
- Mallinbook's ASC privacy URL still points to a removed GitHub Pages route and returns 404.
- SentiPods still has no ASC privacyPolicyUrl.
- Age ratings remain unset for Oenora, SharedSpaceLab, and SentiPods pending owner decisions.
- `~/peerlink` is missing and no matching GitHub repository was found, so PickledBalls project generation remains blocked on this machine.
- `1041soft.com` still points at Namecheap forwarding/parking rather than its GitHub Pages source; HTTPS is unusable.

## Operational Rule

Use `current/index.json` as source of truth, `tasks/index.json` for recurring routing, and `current/handoffs/index.json` for next-cycle directives. Public websites and `site/` are presentation surfaces and must be checked against JSON, ASC, repository settings, and live deployments.
