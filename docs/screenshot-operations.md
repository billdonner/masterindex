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
| workin On | iPhone project; staged demo data; critique; ASC publication | 93, Aug 2 | Current; verify rather than rebuild |
| Screenker | Six-slot Mac project; repeated critique; ASC publication | 86, Aug 10 | Current; above the general gate, below the commercial target |

No Screenker provenance was found for the current SentiPods, Oenora, Zerver Monitor,
SharedSpaceLab, PickleFamilia, KinFlash, Flasherz Kids, Cardz Studio, or MastPex sets.
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
| workin On 1.0 | 0 | 4 | 0 | Current at 93 |
| 100 Burfords 1.1 | 0 | 7 | 6 | Current at 88/90 |
| Zerver Monitor 1.0 | 0 | 0 | 0 | Missing |
| DoubleQross 1.0 | 0 | 9 | 3 | Published but stale |
| Flasherz Kids 1.0 | 0 | 2 (6.5-inch) | 0 | Minimal legacy set; lifecycle decision first |
| PickleFamilia 1.0 | 0 | 0 | 0 | Defer pending product decision |
| Mallinbook 1.0 | 6 | 4 | 2 | Complete, but iOS sets are unscored |
| KinFlash 1.0 | 0 | 0 | 0 | Lifecycle and release decision first |
| PickledBalls 1.0 | 0 | 10 | 10 | Published; re-critique current composition |
| 123 Words 1.12 | 0 | 7 | 6 | Published but stale |
| Cardz Studio 1.0 | 0 | 0 | 0 | Lifecycle decision first |

Apple's current upload procedure and device rules remain external requirements:
[upload screenshots](https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots/)
and [screenshot specifications](https://developer.apple.com/help/app-store-connect/reference/screenshot-specifications/).

## Cleanup Schedule

This order favors release-ready apps with known stale galleries, then fills verified gaps. A
day is a work slot, not a promise to publish an app whose product or release decision is open.

| Date | Work | Exit condition |
|---|---|---|
| Aug 15 | DoubleQross and 123 Words: freeze the intended release UI; regenerate iPhone/iPad raw captures from current builds | Capture manifests identify build, device, locale, scenario, and data source |
| Aug 16 | Compose and critique DoubleQross and 123 Words; re-shoot only failed or misleading slots | Every hard gate passes; each gallery is at least 85, or 90 if assigned commercial |
| Aug 17 | amenbeats and PickledBalls: capture/relink the post-change product; include an iPad decision for universal amenbeats | New critiques apply to the exact projects intended for ASC |
| Aug 18 | Pfoliolio: import the current four iPhone captures into Screenker; capture the matching Mac build and critique both | iPhone and Mac share current naming, data, positioning, and approved scores |
| Aug 19 | Mallinbook: critique iPhone and iPad; review the Mac 89 against its product-line threshold | Three platform galleries have current reports; improve Mac if the target is 90 |
| Aug 20 | SentiPods: import the three existing device sets, run truth/privacy review, then critique; re-capture only failures | Existing ASC coverage gains reproducible Screenker projects and reports |
| Aug 21 | Screenker: improve the current 86 gallery to 90 if it is confirmed for 1041soft.com | Approved six-slot project and matching ASC set |
| Aug 22 | Oenora: after Founders Beta UI freeze, compose/critique the six local iPhone captures and publish; do not populate the unused ASC Mac record | iOS ASC set matches the beta product; native Developer ID Mac remains a separate channel |
| Aug 23 | Verify-only pass for workin On and 100 Burfords; compare Screenker export hashes/order with ASC | No rebuild unless parity or visible-product drift fails |
| Aug 24 | Zerver Monitor: decide whether build 5 is a real release candidate; if yes, create capture brief, capture, critique, and publish | Either an approved current set exists or release work is explicitly deferred |

SharedSpaceLab, PickleFamilia, KinFlash, Flasherz Kids, Cardz Studio, and both MastPex records
stay out of the production queue until each has a real release target and product-line decision.
LtWatcher and grubber-ios are retired/obsolete; Famster is concept-only; Nagz is legacy. Do not
spend screenshot time on those records.

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
