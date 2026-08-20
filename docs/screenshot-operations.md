# Screenshot Operations

Observed Friday, August 14, 2026. `current/index.json` remains the source of truth;
this runbook explains how to act on its `screenshotOperations` facts.

## What Screenker Has Actually Done

Screenker is now a portfolio workflow, not only an image compositor. Its history includes
capture briefs, source relinking, deterministic exports, App Store Connect import/diff/publish,
device and web previews, sandboxed agent critique, and built-in Claude/OpenAI gallery critique.

| App | Verified Screenker history | Last recorded critique | Current conclusion |
|---|---|---:|---|
| DoubleQross | iPhone and iPad projects; capture handback; re-shoot; ASC gallery | iPhone 90, Jul 28 | Stale after project-original, palette, and visible UI changes |
| PickledBalls | iPhone and iPad projects; capture brief; device re-shoots; repeated ASC publication | iPhone 88, iPad 86, Jul 29 | Galleries were changed and republished later; scores are stale |
| 100 Burfords | iPhone and landscape-iPad projects; UITest capture rig; ASC publication | iPhone 88, iPad 90, Aug 1 | Current; published to the 1.1 draft Aug 6 |
| 123 Words | iPhone and iPad gallery; second critique pass; ASC publication | 90, Aug 1 | Stale after major child-UX, phonics, hub, and layout work |
| Pfoliolio | iPhone and Mac projects; capture hooks; ASC publication | Mac 93, Aug 5 | Current iPhone set bypassed Screenker; matching Mac recapture is pending |
| amenbeats | iPhone project; scripted capture; critique; corrected re-shoot and republish | 93, Aug 5 | Stale after Kid/Pro and real Kid mode landed |
| Mallinbook | iPhone, iPad, and two Mac projects; capture briefs; ASC publication | Mac 89, Aug 2 | Mac is scored; iPhone and iPad have no recorded critique |
| workin On | iPhone project; staged demo data; critique; ASC publication | 93, Aug 2 | Current historical/internal set; no public release work planned |
| Screenker | Six-slot Mac project; repeated critique; ASC publication | 86, Aug 10 | Current; above the general gate, below the commercial target |

No Screenker provenance was found for the current SentiPods, Oenora, Zerver Monitor,
SharedSpaceLab, PickleFamilia, KinFlash, or Cardz Studio sets.
Nagz has an ASC gallery but is a legacy reference and should not receive new gallery work.

## Live ASC Baseline

The August 14 read-only ASC audit found these current en-US sets:

| App/version | Mac | iPhone | iPad | Operational state |
|---|---:|---:|---:|---|
| Pfoliolio 1.0 | 6 | 4 | 0 | Published, mixed provenance, current iPhone set uncritiqued |
| amenbeats 1.0 | 0 | 5 | 0 | Published but stale; universal app has no iPad set |
| Oenora 1.0 | 0 | 0 | 0 | Six local iPhone captures exist but nothing is in ASC |
| SharedSpaceLab 1.0 | 0 | 0 | 0 | Defer until a release candidate exists |
| SentiPods 1.0 | 3 | 3 | 3 | Device coverage complete; no critique provenance |
| Screenker 1.0 | 6 | 0 | 0 | Current at 86 |
| workin On 1.0 | 0 | 4 | 0 | Internal/TestFlight-only; current at 93, no public marketing work |
| 100 Burfords 1.1 | 0 | 7 | 6 | Current at 88/90 |
| Zerver Monitor 1.0 | 0 | 0 | 0 | Missing |
| DoubleQross 1.0 | 0 | 9 | 3 | Published but stale |
| PickleFamilia 1.0 | 0 | 0 | 0 | Defer pending product decision |
| Mallinbook 1.0 | 6 | 4 | 2 | Complete, but iOS sets are unscored |
| KinFlash 1.0 | 0 | 0 | 0 | Near-term billdonner.com release; gallery is highest-priority missing work at the 85-point gate |
| PickledBalls 1.0 | 0 | 10 | 10 | Published; re-critique current composition |
| 123 Words 1.12 | 0 | 7 | 6 | Published but stale |
| Cardz Studio 1.0 | 0 | 0 | 0 | Internal/TestFlight-only; no public marketing gallery |

Apple's current upload procedure and device rules remain external requirements:
[upload screenshots](https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots/)
and [screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/screenshot-specifications/).

## Execution Model

Run every app through one of four lanes. Do not give dead, internal-only, and public-release
apps the same workflow.

| Lane | Meaning | Required output |
|---|---|---|
| Publish-now | Active public or near-public release candidate | Approved Screenker export plus ASC parity verification |
| Verify-only | Already current or nearly current; reopen only on visible drift | Read-only parity report, or a documented reason to re-enter critique |
| Internal-evidence | Internal/TestFlight-only app still worth evaluating | Approved local archive and critique report; no ASC marketing publication required |
| Archive/no-work | Historical, obsolete, or intentionally parked line | Explicit note that no new screenshot work should be done |

### Current lane assignment

| Lane | Apps |
|---|---|
| Publish-now | DoubleQross, PickledBalls, 123 Words, amenbeats, Pfoliolio, Mallinbook, KinFlash, SentiPods, Oenora, Zerver Monitor, Screenker |
| Verify-only | 100 Burfords |
| Internal-evidence | workin On, Cardz Studio |
| Archive/no-work | PickleFamilia, LtWatcher, grubber-ios, Famster, Nagz |

SharedSpaceLab is intentionally outside the production screenshot queue until it has a real
release candidate and product-line decision.

## Execution Board

Track each app version and platform through these states:

| State | Meaning |
|---|---|
| no-project | No Screenker project, manifest, or approved source set exists yet |
| capture-needed | Product scope is frozen enough to capture, but source screenshots are missing or stale |
| captured | Deterministic source captures and manifest exist |
| in-critique | Screenker sandbox iteration is underway |
| re-capture-needed | Critique found a product-truth, state, data, or layout issue that decoration cannot solve |
| approved-local | The exact export is approved locally; not yet published to ASC |
| published-asc | Upload completed; ASC now has the intended assets |
| verified-parity | Live ASC slot count, order, locale, and display type match the approved export |
| deferred | Work paused because product, release, or owner decisions are unresolved |
| archived-no-work | Historical line; preserve evidence only |

Use the `unitOfWork` already defined in `current/index.json`: app version + platform + locale +
display type.

## Pipeline Steps

Execute the same sequence for every `publish-now` unit of work:

1. Freeze the candidate.
   Lock version, build, locale, device families, positioning, and the exact flows the gallery
   must prove. If these are still moving, do not start capture.
2. Write the capture brief.
   Record the product claim, target device/display types, source of demo data, privacy/truth
   constraints, and the expected slot narrative.
3. Capture deterministically.
   Generate or collect raw screenshots from the candidate build. Record commit, build number,
   OS, simulator/device, locale, date, and scenario in a manifest.
4. Compose in a Screenker sandbox copy.
   Never mutate the approved project directly during critique loops.
5. Run hard gates first.
   Truth, privacy, freshness, technical export, coverage, accessibility/localization, ASC parity,
   and human-approval readiness all pass or fail before any score matters.
6. Score and prioritize.
   Record the weighted Screenker score and a short fix list ordered by impact.
7. Iterate narrowly.
   Apply one high-impact change per loop. Re-capture whenever the weakness is in-product rather
   than compositional.
8. Stop intentionally.
   Stop after six loops, after two gains below three points, or once the required threshold is
   met: 85 general, 90 confirmed 1041soft.com commercial.
9. Approve the exact export.
   Move approved changes back to the canonical project, export, and require explicit human
   approval before publication.
10. Publish and verify.
   Upload to ASC, read ASC back, and compare live slot count, order, locale, display type, and
   asset completion against the approved export.
11. Archive evidence.
   Preserve the canonical `.screenker` project, source captures, export files, manifest, critique
   report, approval date, and ASC parity result.

For `verify-only`, run steps 1, 5, 10, and 11 only unless a freshness trigger reopens capture.

For `internal-evidence`, run steps 1 through 9 and 11, but skip ASC publication. The goal is a
truthful, reproducible local gallery record, not public storefront polish.

For `archive/no-work`, do not create a new project. Preserve any existing evidence and add an
explicit note that the line is historical.

## Work Queue

Use this execution order unless an app's release reality changes:

1. DoubleQross: finish the already-captured iPhone and iPad candidate by getting human approval,
   then publish and verify parity.
2. 123 Words and PickledBalls: both are published but stale, so re-capture and re-critique the
   current product rather than polishing old compositions.
3. amenbeats and Pfoliolio: bring them back onto exact current product state, including the iPad
   decision for amenbeats and matched iPhone/Mac provenance for Pfoliolio.
4. Mallinbook and SentiPods: close critique-provenance gaps on already-populated ASC sets.
5. KinFlash: run the full cycle to the 85-point free-line target, not the 90-point commercial bar
   (it is a kids app on billdonner.com), and block publication until its hosting, release-channel,
   and ASC-product decisions are resolved.
6. Oenora and Zerver Monitor: create current release-facing galleries only if the current build is
   a real candidate.
7. Screenker: improve its own Mac gallery from 86 toward the 90 commercial bar if its product-line
   assignment remains 1041soft.com.
8. 100 Burfords: verify-only pass; rebuild only if parity or visible drift fails.
9. Internal-only lane: workin On, Cardz Studio.

## Release-Relative Schedule

Use this sequence for every future release train:

| When | Required action |
|---|---|
| T-7 days | Freeze positioning, supported devices, locales, and the flows the gallery must prove; write the Screenker capture brief |
| T-5 days | Capture from the release-candidate build with deterministic demo data; record build, OS, device, locale, and scenario |
| T-4 days | Compose in Screenker and run the first critique on a sandbox copy |
| T-3 days | Apply one high-impact change per loop; re-capture when the problem is in-product rather than decorative |
| T-2 days | Human truth/privacy/accessibility review; approve the exact project and exported files |
| T-2 days | Publish to ASC, then read ASC back and compare slot count, order, display type, and asset completion |
| T-1 day | Final release-candidate drift check; any visible mismatch reopens the gallery |
| T+1 day | Check the public storefront after release and archive the manifest, critique report, and ASC parity result |

Outside a release train, run a read-only portfolio check weekly. Rebuild only on an invalidation
trigger. Run a full rubric and provenance audit monthly and before changing a product-line
assignment.

## Future Rubric

A numeric critique is valid only after all hard gates pass.

### Hard gates

| Gate | Pass condition |
|---|---|
| Truth | Every claim and visible state exists in the candidate build; no debug banners, fake capabilities, beta-only copy, or misleading device treatment |
| Privacy and safety | No real personal, account, child, health, financial, location, or server data; synthetic data is credible and documented |
| Freshness and provenance | Manifest names the build, commit, project, capture source, device, OS, locale, date, and scenario; no material visible change occurred afterward |
| Technical export | Correct Apple display type and dimensions, no alpha, no clipping, no broken panorama seam, and no more than ten slots |
| Coverage | Every promised platform and required device family has an intentional set or a documented exclusion |
| Accessibility and localization | Text remains legible at store thumbnail size, contrast is acceptable, captions do not carry essential inaccessible detail, and the locale matches the UI |
| ASC parity | Uploaded slot count, order, display type, locale, and asset-delivery state match the approved export |
| Human approval | A person approves the exact export after critique; agents never publish from the critic sandbox |

### Screenker score: 100 points

| Dimension | Weight | A 5 means |
|---|---:|---|
| Hook, slide 1 | 30 | Product and benefit are understood in under three seconds at thumbnail size |
| Thumbnail legibility | 20 | Captions are short, readable, and supported by the visible UI |
| Narrative flow | 20 | The sequence progresses from promise to proof without duplication or unexplained jumps |
| Cross-slot consistency | 20 | Identity, typography, framing, spacing, color, device treatment, and data form one deliberate system |
| Premium finish | 10 | The set is specific, polished, restrained, and free of accidental UI or generic filler |

General BillDonner.com release gate: **85**. Confirmed 1041soft.com release target: **90**.
A score is not valid forever: changing a source capture, composition, captured flow, product
positioning, supported-device promise, or locale resets the affected gallery to **stale**.

## Critique Loop

1. Create a deterministic `sandbox_copy`; never mutate the approved project directly.
2. Run hard gates before assigning a score. A failed hard gate cannot be averaged away.
3. Record the weighted score and a short, prioritized wishlist.
4. Apply one high-impact change, render again, and re-score.
5. Stop after six iterations, after two gains below three points, or when the applicable gate is met.
6. Re-capture in the app when the weakness is product truth, content, state, or layout. Screenker decoration cannot repair a weak or misleading source.
7. Move the approved change back to the canonical project, export, obtain human approval, publish, and verify ASC parity.

The archive for each approved gallery should retain the `.screenker` project, source captures,
exported files, capture manifest, critique report, approval date, and ASC verification result.
