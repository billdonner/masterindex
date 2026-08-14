# MasterIndex Inventory

As of Friday, August 14, 2026.

## Scope

- Reconciled App Store Connect, active GitHub sources, local repositories, Fly deployments, and public product URLs.
- Applied no handoff directives because `current/handoffs/index.json` has none.
- Performed the requested retirements, operational fixes, and website publications; observed facts and remaining product gaps are kept distinct below.

## Executive Summary

- ASC contains 23 app records: 20 map to repositories, two MastPex records are placeholders, and GigStand is the intentionally retained retired record.
- LtWatcher is retired. `billdonner/clubwatch` is archived read-only and its ASC record is retained.
- Clubsync is deferred until PickledBalls v2. Its application tier is not deployed; `bd-clubsync-db` remains deployed to preserve data.
- Card Server is retired after consumer and replacement checks. `billdonner/card-server` is archived, its Fly descriptor is removed, and Card Engine remains the sole verified source for `bd-cardzerver.fly.dev`.
- Server Monitor is repaired and deployed. Its seven production targets omit Clubsync and its direct Nagzerver and Card Engine HTTP probes return 200.
- The registry tracks 53 repositories, of which 51 remain active after the two retirements.
- Canonical-main records for local-model-lab, adspill, and the Oenora Recognition API are preserved.
- The generated 19-entry `billdonner.com/apps` catalog is live on IONOS, with Pfoliolio corrected, Oliopfolio redirected, and LtWatcher archived outside the public apps tree.

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
| Oenora iOS | 1.0 (6) | 6 VALID, external beta approved | Aligned; native Mac uses a separate notarized Developer ID bundle |

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
- The generated files were published to IONOS on 2026-08-14 and match the live HTTPS responses by SHA-1.
- The previous catalog and LtWatcher directory were retained under `/_archive`; the public LtWatcher route now returns 404.

### Company Website — `1041soft.com` (live 2026-08-14)

Canonical app-website home. Public repo `billdonner/1041soft-site`, served by GitHub
Pages, Let's Encrypt certificate covering apex and `www`, valid to 2026-11-12, HTTPS
enforced with HTTP 301ing to it. DNS at Namecheap: apex A records to
`185.199.108–111.153`, `www` CNAME to `billdonner.github.io.`

Paths: `/qross/`, `/nagz/`, `/workinon/`, `/flasherz/`, `/zervermonitor/`,
`/screenker/`, `/mallinbook/`, `/sentipods/`, `/pfolio/` — each with support and
privacy pages. All 24 routes verified 200 over HTTPS.

**Rule: never enable GitHub Pages on a private repo.** Pages publishes `docs/` to the
open web regardless of repo visibility, and bills Actions minutes on private repos.
Add a subpath here instead.

This site coexists with the now-live `billdonner.com/apps` portfolio catalog. Qross
and workinOn keep their existing `billdonner.com/apps/...` support URLs, which
resolve and were deliberately left unchanged.

## Preserved Main-Only Facts

- `local-model-lab` is parked, with its historical MLX/Qross corpus benchmark results retained.
- `adspill` remains a two-person advertising-capacity research sandbox.
- The Oenora Recognition API is live at `bd-oenora-recognition.fly.dev` and remains an Oenora dependency.
- Oenora's public TestFlight invite, externally approved iOS build 6, three-device CloudKit soak, repaired recognition configuration, and notarized native Mac delivery are retained.

## Remaining Gaps

- Mallinbook's ASC privacy URL still points to a removed GitHub Pages route and returns 404. A working replacement now exists at `https://1041soft.com/mallinbook/privacy`; the ASC field still needs setting.
- SentiPods still has no ASC privacyPolicyUrl. A working page exists at `https://1041soft.com/sentipods/privacy`; the ASC field still needs setting.
- **Closed 2026-08-14 — unintended public exposure.** Seven private repos (qross, nagz, nagz-ios, workinon, obo-ios, server-monitor-ios, mallinbook) were publishing `docs/` to the open web through GitHub Pages. Verified world-readable at the time: qross business plans, risk register, `architecture/cardzerver-operational-roadmap.md`, `decisions/ADR-009-secret-management.md`, `carol-claude-code-instructions.md`; and nagz `DEPLOYMENT_PLAN.md`, `CODE_REVIEW_FINDINGS.md`, `CONTRIBUTOR_GUIDE.md`. Scanned for live credential patterns and found none. Pages disabled on all seven; every path re-verified 404.
- `nagz/docs/.well-known/apple-app-site-association` never actually served — Jekyll ignores dot-directories — so universal links have never worked from that domain. Not a regression from the migration.
- Age ratings remain unset for Oenora, SharedSpaceLab, and SentiPods pending owner decisions.
- `~/peerlink` is missing and no matching GitHub repository was found, so PickledBalls project generation remains blocked on this machine.
- ~~`1041soft.com` still points at Namecheap forwarding/parking; HTTPS is unusable.~~ **Resolved 2026-08-14** — see Company Website below. Apex now serves from GitHub Pages over enforced HTTPS.
- Oenora's existing ASC macOS 1.0 record has no builds after the project deliberately replaced Catalyst with a native Developer ID target using `com.billdonner.oenora.mac`.

## Operational Rule

Use `current/index.json` as source of truth, `tasks/index.json` for recurring routing, and `current/handoffs/index.json` for next-cycle directives. Public websites and `site/` are presentation surfaces and must be checked against JSON, ASC, repository settings, and live deployments.
