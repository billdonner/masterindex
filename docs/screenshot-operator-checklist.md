# Screenshot Operator Checklist

Use this when running one screenshot cycle for one app. The canonical policy lives in
`docs/screenshot-operations.md`; this file is the short execution handoff.

## Where To Work

Use three places:

1. Target app repo
   Use the app repository to freeze the candidate build, set up demo data, and capture source
   screenshots.
2. Screenker
   Use Screenker to compose, critique, iterate, and export the gallery.
3. MasterIndex
   Use `~/masterindex` to read the queue and record the lane, board state, blockers, and parity.

## Your Role

You should not try to do every mechanical step yourself. Your job is only:

1. Pick the next app from `current/index.json` `screenshotOperations.board`.
2. Confirm the candidate build is the one you want judged.
3. Approve or reject the exact final export.
4. Approve or reject ASC publication.

Everything else can be done by an agent in the app repo, Screenker, or MasterIndex.

## Agent Role

The agent should:

1. Read the app's `screenshotOperations.board` row in `current/index.json`.
2. Freeze the candidate version/build/platform scope.
3. Write the capture brief.
4. Generate deterministic source screenshots.
5. Build or update the Screenker project.
6. Make a sandbox copy for critique.
7. Run hard gates and scoring.
8. Iterate until the gallery passes or clearly needs re-capture.
9. Prepare the exact export for your approval.
10. If approved, publish to ASC and verify parity.
11. Update MasterIndex board state and archive the evidence.

## One-Cycle Flow

Run this sequence for one app:

1. Open `~/masterindex`.
2. Find the next app in `current/index.json` `screenshotOperations.board`.
3. Move to the target app repo.
4. Freeze:
   version, build, locale, device family, visible flows, product claim.
5. Create a capture brief:
   what each slot is supposed to prove, which demo data is used, and what privacy constraints
   apply.
6. Capture deterministic source screenshots in the app repo.
7. Save a manifest:
   commit, build number, OS, simulator/device, locale, date, scenario.
8. Open Screenker.
9. Import the source screenshots into the canonical project or a new project.
10. Create a sandbox copy before critique.
11. Run hard gates:
   truth, privacy, freshness, technical export, coverage, accessibility/localization.
12. Score the set:
   hook 30, thumbnail legibility 20, narrative 20, consistency 20, finish 10.
13. Apply one high-impact change.
14. Re-render and re-score.
15. If the problem is in the product rather than the composition, go back to the app repo and
    re-capture.
16. Stop when the score is high enough or the loop is no longer paying off:
   85+ for general release, 90+ for confirmed 1041soft.com commercial release.
17. Present the exact export for your approval.
18. If approved and the app is `publish-now`, upload to ASC.
19. Read ASC back and verify slot count, order, locale, display type, and completion state.
20. Update `current/index.json` board state in MasterIndex.
21. Archive the `.screenker` project, source captures, export, manifest, critique report, and
    parity result.

## Stop Conditions

Stop and ask for a decision if any of these are true:

1. The build is still changing materially.
2. The app has no truthful demo data.
3. A real product blocker prevents honest screenshots.
4. The app needs owner decisions before publication.
5. The critique reveals that the app UI itself must change before screenshots can be good.

## User Decision Gates

These are the only points where you must step in:

1. Choose the candidate build if there is more than one.
2. Approve the final export.
3. Approve ASC publication.
4. Decide whether to defer the app if the product is not ready.

## First Apps To Run

Current queue head from MasterIndex:

1. 123 Words
2. PickledBalls
3. amenbeats
4. Pfoliolio
5. Mallinbook
6. SentiPods
7. KinFlash
8. Oenora

Deferred by owner for now:

- DoubleQross

## Minimal Handoff Prompt

Use this when handing one app to another agent:

```text
Run the screenshot cycle for <APP> using MasterIndex as source of truth.
Read ~/masterindex/current/index.json screenshotOperations.board and
~/masterindex/docs/screenshot-operations.md first.
Work in the target app repo for build freeze and deterministic capture, then in Screenker for
composition and critique, then back to MasterIndex to update board state.
Do not publish without explicit human approval.
Return with:
1. capture manifest
2. critique result and score
3. exact approval export location
4. ASC parity result or publication blocker
5. recommended next board state
```
