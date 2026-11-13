# Disclosures (facts the checks should weigh; computed by the author's code, rerunnable)

1. Amendments before scoring: PREREG.v2 (a mislabelled vintage, 2023-12-08, holds data to 2023-12-30; a parallel
   Saturday/Monday file family from 2025-01-27), PREREG.v3 (the frozen code crashed on 2024-10-13 on 65-130 rows that
   stop in 2016; one-line fix), PREREG.v4 (the 2024-11-22 vintage lacks NC and stops at 2024-09-28 for 12 states; a
   location is taken from the usable vintage where its own data are latest). Only 2024-11-24 changed under v4; the other
   30 files were byte-identical before and after (checked before scoring).
2. Development (2023-24 only, 40 configurations) used a development-only revision reference (the 2024-10-25 vintage as
   the "near final" view of the 2023-24 vintages) because no vintage before 2023-10-16 exists; the frozen rule
   (26-week gap, October-April pulls) gives factors within 0.035 (log) of that preview at the first test origin.
   Dev truth was the final target file for 2023-24.
3. The hub README asked teams to project raw RSV-NET data ("There should be no adjustment for reporting"). The pipeline
   corrects the latest weeks for reporting delays using only past vintages (lag 0 factor about exp(0.45)). Scoring uses
   the hub's current target data, as the bank's verification method says.
4. Descriptive sensitivity (attempts/contrarian/out/sensitivity.txt, computed after the scoring):
   - block length 1/2/3/4/6: rel -0.2755, every 90% interval below 0 (widest [-0.3746, -0.1579] at L = 1);
   - truth = first report of each week: ours WORSE, rel +0.2627 [+0.0283, +0.4938]; truth = the view 4 weeks later:
     rel -0.2630 [-0.3497, -0.1811]; truth = season-end view (2025-05-16 vintage): rel -0.2538 [-0.3413, -0.1661];
   - US tasks only rel -0.4463; states only rel +0.1817 [+0.0827, +0.2634] (ours worse on states); every horizon 0-4 and
     every age group below 0; leave-one-date-out rel from -0.3225 to -0.2400; ours lower on 12 of 14 dates.
5. Scorer: a Python implementation of the scoringutils/hubverse quantile WIS (weigh = TRUE, median once); R and
   hubEvals are not installed on this machine (no installs allowed). Pinball and interval forms agree to 3e-12.
6. Not part of this claim: p1 is NOT met (CEPH-Rtrend_rsv on its own tasks: ours 108.0979 vs 106.0856, rel +0.0190);
   p2's reading is met by the same scoring (rel -0.2559 [-0.3310, -0.1752]) but is a separate object.
7. Long-term revisions: the final file is 3-10% above the late-2024 view for 2023-24 season totals; 2024-25 values in
   the final file may still be revised.
8. Added 2026-11-13T02:09:50Z (after the panel started): the frozen pipeline (same code, same FROZEN_PARAMS.json) run on the DEV season
   2023-24 with the as-of rule. In 2023-24 no vintage older than 2023-10-16 exists, so the frozen 26-week-gap revision
   rule finds almost no earlier vintages and the backfill correction is mostly absent. Result (in-sample season,
   descriptive only, attempts/evaluator/test/score_2023-24_descriptive.log): MAIN rel +0.1861 (ours WORSE than the
   2023-24 hub-ensemble), 90% [-0.0507, +0.3181]; pediatric rel -0.0125. So the 2024-25 result is not replicated on
   2023-24 by the frozen as-of pipeline; its gain needs a previous season of archive vintages.
9. (Required by the CRITERION skeptic.) 65-130 placeholders: 370 of the 695 hub-ensemble 65-130 tasks carry all-zero
   forecasts (every quantile 0, all 14 locations, every horizon) for the six origins 2024-12-08 .. 2025-01-26. Cause: the
   Friday vintages from 2024-12-06 carry 65-130 only as rows ending in 2016; the PREREG.v3 stale-series rule marks them
   absent and the frozen fallback (0-130 x the US share over 52 weeks) gets a zero share. These tasks have no truth in the
   hub's target file and are unscored for both models (PREREG R4, written before any forecast existed).
10. If 65-130 were scored anyway, the margin disappears: with 65+ truth from the hub's archive vintages (latest vintage
   carrying 65-130; 3,746 tasks) ours 100.81 vs 101.89, rel -0.0106, 90% [-0.247, +0.161] (CRITERION skeptic); with the
   complement 0-130 - (0-4 + 5-17 + 18-49 + 50-64) from the final file (3,760 tasks) rel -0.0151, 90% about
   [-0.24, +0.16] (REPRODUCE and CRITERION skeptics). On 65-130 alone ours is about twice the ensemble's WIS. The
   complement is not an identity in these data (98 of 938 derived 2024-25 values are negative).
11. Asymmetry: the pipeline's input code (asof_rsv.py) derives 65-130 as 0-130 minus the other groups when a vintage
   lacks a 65-130 column, while PREREG R4 treats 65-130 as having no truth.
12. State-level splits (CRITERION skeptic, own bootstrap): all states +18.2% [+8.0%, +26.2%]; state 0-130 +9.4%
   [+1.8%, +16.8%]; state pediatric +35.2% [+18.4%, +52.8%]. The whole gain comes from the 265 US tasks.
13. The development record (all 40 configurations plus three re-checks of the chosen one) is
   how-we-built-it/forecaster/dev_results_2023-24.jsonl. The freeze is evidenced by self-recorded date -u stamps and
   sha256 hashes (METHOD_FREEZE.md, freeze_hashes*.txt), not by a git commit or a third-party timestamp.
14. The claim's hub-format files are object/forecasts/ (the run's attempts/forecaster/result/submission/); the scored
   files (result/forecasts/) also carry horizon -1 rows, which hub-config does not allow; the horizon 0-4 rows used for
   scoring are identical in both.
