# REPRODUCE skeptic: rsv-hub-retrospective-beat-ensemble-wis, route (a), HopkinsIDD 2024-25

context: subagent (Claude Code Agent tool, subagent_type reproduce, fresh context)

Scope: claim/CLAIM.md, REPRODUCE.md, target.md, PREREG.md and the amendments PREREG.v2-v4, plus DISCLOSURES.md
(including item 8, added after the panel started). I wrote the scorer, the truth construction, the bootstrap and the
as-of and look-ahead checks myself before reading the author's scoring code. My scripts and logs are in
panel/work_reproduce/. My copy of the package was deleted after use. All paths below are relative to claim/ unless
they start with panel/.

## Definitions I applied (quoted)

- Kit instruction: "Before reading the author's code, write your own checker from the definition (quote it). Verify
  every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a
  sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."
- WIS (scoringutils/hubverse, weigh = TRUE, median counted once), with K = 11 central intervals on the hub's 23 levels:
  WIS = 1/(K + 1/2) * ( 1/2 * |y - m| + sum_k (alpha_k / 2) * IS_alpha_k ), where
  IS_alpha = (u - l) + (2/alpha)(l - y)1{y < l} + (2/alpha)(y - u)1{y > u}.
  This equals the mean over the 23 levels tau of 2 * rho_tau(y, q_tau), with rho_tau = (1{y < q} - tau)(q - y). I
  implemented both forms independently (panel/work_reproduce/my_score.py).
- Truth (PREREG R4): data/hopkins/hub/target-data/2026-06-05_rsvnet_hospitalization.csv, target "inc hosp", date =
  origin_date + 7*horizon - 1. The derived groups are 0-0.99 = 0-0.49 + 0.5-0.99, 1-4 = 1-1.99 + 2-4 and
  5-64 = 5-17 + 18-49 + 50-64, each scored only when every component is present. 0-130 is taken directly. 65-130 has no
  truth. Tasks without truth are unscored.
- Task set (R6): every (origin_date, location, age_group, horizon) in the 2024-25 hub-ensemble files that has truth.
  The season average is the arithmetic mean over scored tasks.
- Bootstrap (R7): stationary bootstrap (Politis-Romano) over the reference dates in chronological order, mean block
  length 3 (p = 1/3, wrap-around), B = 10000. Each resampled date brings all its tasks. The statistic is
  r = mean(ours) / mean(ensemble) - 1, and the 90% interval is the 5th to 95th percentile. The criterion is met when
  r <= -0.03 AND the 95th percentile is below 0.

## 1. Claimed value, recomputed with my own scorer and truth (panel/work_reproduce/my_score_main.log)

- 2024-25 ensemble files: 15 (2024-10-27 .. 2025-04-06). 2024-12-01-hub-ensemble.parquet is empty. In every ensemble
  row, target_end_date == origin + 7h - 1.
- Ensemble tasks: 3760 over 14 origin dates. By age group: 0-0.99 695, 0-130 980, 1-4 695, 5-64 695, 65-130 695.
- Tasks with truth: 3065 (0-0.99 695, 0-130 980, 1-4 695, 5-64 695; none for 65-130). Our forecasts cover all 3760
  ensemble tasks, so none of the 3065 scored tasks is missing on our side.
- Pinball form vs interval form: max difference 1.819e-12 (ensemble) and 1.364e-12 (ours). Neither side has a
  decreasing quantile or a negative value.
- **MAIN: tasks 3065, dates 14, ours 72.2386, ensemble 99.7021, rel -0.2755.** This matches the claim exactly.
- Per age group (ours / ensemble mean WIS): 0-0.99 37.7803 / 47.9053; 0-130 126.8202 / 179.7678;
  1-4 58.4946 / 81.4796; 5-64 43.4772 / 56.8230.
- **My bootstrap (my implementation, seed 777, B 10000, mean block 3): 90% [-0.3601, -0.1998].**
  - The author's draws happen in the same order as mine, so I also ran my code with the author's seed 20261113. It
    gives [-0.3578, -0.1984], identical to the claimed interval.
  - Seeds 1-5 give [-0.3609, -0.1986], [-0.3612, -0.1975], [-0.3585, -0.1979], [-0.3610, -0.1991] and
    [-0.3584, -0.1977].
  - So r = -0.2755 <= -0.03 and the 95th percentile (about -0.20) is below 0: the R7 rule is met under every seed I ran.
- Ours is worse than the ensemble on 2 of the 14 dates (2025-01-12 and 2025-04-06).
- p2, for the record (not this claim): 1390 tasks, ours 48.1374 vs 64.6925, rel -0.2559. 90% [-0.3302, -0.1758] with
  seed 777 and [-0.3310, -0.1752] with seed 20261113.
- The author's own pipeline (REPRODUCE steps 1-2, run in my copy) gives the same result. wis.py prints
  "SELFTEST PASS". score_test.py prints "MAIN criterion (R7: rel <= -0.03 and rel_hi < 0): MET (rel -0.2755,
  90% [-0.3578, -0.1984])", and its summary is byte-identical to attempts/evaluator/test/score_test_2024-25.log.

## 2. Regeneration with the frozen pipeline (REPRODUCE step 3)

- Hashes of the frozen files match the freeze records. The current code/model_rsv.py (7ace5548...) and
  code/asof_rsv.py (29340a54...) match freeze_hashes_v4.txt. run_season.py, FROZEN_PARAMS.json and the four evaluator
  scripts are unchanged since METHOD_FREEZE.md.
- I ran `run_season.py FROZEN_PARAMS.json out 2024-25` in my copy with a fresh, empty RSV_CACHE inside my work folder.
  It produced 31 files plus read_log.csv.
- **All 31 regenerated files are byte-identical** to attempts/forecaster/result/forecasts/ and to
  attempts/forecaster/forecasts_sha256.txt (31 of 31 identical, 0 differ). read_log.csv is identical too. Scoring the
  regenerated files gives the same 72.2386 / 99.7021 / -0.2755. Hashes are in panel/work_reproduce/regen_fc_sha256.txt.
- The forecasts sha list checks OK, and all 31 entries of submission_sha256.txt check OK.

## 3. As-of discipline and look-ahead

- **Independent check of the vintage choice** (panel/work_reproduce/my_asof_check.py). For each archive file I took the
  maximum date over all non-missing rows of any target and any age group, which is stricter than the pipeline's own
  metadata. I then applied the PREREG.v2 rule (label <= O and last date <= O - 8 days; latest data week wins) and the
  PREREG.v4 per-location rule.
  - All 31 origins match read_log.csv: 0 mismatches.
  - Every vintage read has label <= O and last date read <= O - 8 days.
  - Only origin 2024-11-24 uses the v4 per-location rule: 12 states and NC come from the 2024-11-15 vintage, and US
    from the 2024-11-22 vintage. This matches PREREG.v4.
  - The mislabelled 2023-12-08 vintage (content to 2023-12-30) is correctly never the data vintage.
- **My own look-ahead check** (panel/work_reproduce/my_lookahead.py). For each origin I built a minimal run tree holding
  only the 4 pipeline scripts, FROZEN_PARAMS.json and the archive vintages dated <= O, copied unchanged. The tree had no
  final target file, no model-output and no later vintage. Each run used a fresh process, a fresh cache and no RSV_ARCH.
  All four tested origins are byte-identical to the claimed files:
  - 2024-10-27 (36 vintages): identical True
  - 2024-11-24 (40 vintages, the v4 swap origin): identical True
  - 2025-02-09 (58 vintages, the parallel file families): identical True
  - 2025-04-06 (74 vintages): identical True
- **The author's audit** (REPRODUCE step 4, attempts/contrarian/code/lookahead_audit.py, run in my copy) on two other
  origins: "2025-01-12 vintages_kept 49 truncated 0 identical True" and "2024-12-15 vintages_kept 44 truncated 0
  identical True".
- Code reading confirms that the only data input is the archive folder, through asof_rsv. The meta() step opens every
  archive file to find its last date, but usable() filters on label <= O first, and the minimal-tree runs show the extra
  files have no effect.

## 4. Comparator is live and current; hub format

- I made one live request: a GitHub API GET of HopkinsIDD/rsv-forecast-hub git/trees/main?recursive=1 at
  2026-11-13T02:09:39Z, HTTP 200, with a User-Agent naming V3R1T4S.
  - Live main is still the pinned commit 6bf251ac3fc798e55ed95d0b7269f5f5781c0207, and the tree is not truncated.
  - All 391 local files under data/hopkins/hub/ are blob-identical to live main. These include all 15 2024-25
    hub-ensemble files, the truth file, and all 163 live 2024-25 model-output files.
  - No path in the live tree contains "score", "eval" or "wis", so there is no hub scores file and the recomputed bar
    stands.
- Hub format (panel/work_reproduce/my_format_check.py, checked against data/hopkins/hub-config_tasks.json, 2024-25
  round).
  - result/submission/: 31 files with no problems: the 8 columns, "quantile", the 23 levels, and allowed origins,
    locations, age groups and horizons, with no negative values.
  - result/forecasts/, the scored files, also contain horizon -1 rows, which the hub config does not allow. Each
    submission file equals its forecasts file minus the horizon -1 lines, line for line (31 of 31).
  - Scoring uses only ensemble horizons 0-4, whose lines are identical in both folders, so the claimed value is the
    value of the hub-valid submission files.

## Mismatches found

None. Every claimed number (3065 tasks, 14 dates, 72.2386, 99.7021, -0.2755, and the interval under the author's seed)
reproduced exactly from independent code. The forecasts regenerate byte for byte. No look-ahead was detected on 6
origins (4 in my minimal-tree check, 2 with the author's audit). The as-of vintage choice is correct on all 31 origins.

## Observations for the panel (not reproduction failures; descriptive)

1. **65-130.**
   - The hub's truth, in both the final file and the season-end vintage, has 65-130 values only for 2014-10-11 ..
     2016-04-30, so no 2024-25 65-130 task can be scored from hub data. R4 follows the hub's data literally.
   - However, our 65-130 forecasts are largely degenerate: 1576 of 2165 medians at horizons 0-4 are exactly 0. The
     reason is the fallback share computing to 0. METHOD_FREEZE.md describes the fallback but not this outcome.
   - If 65-130 were instead derived as 0-130 minus (0-4 + 5-17 + 18-49 + 50-64) from the final file, the result would
     not meet the criterion: 3760 tasks, ours 98.1307 vs 99.6332, rel -0.0151, 90% [-0.2441, +0.1546]. Ours is +113.7%
     worse on 65-130.
   - That derivation is not an identity in these data. 98 of 938 derived 2024-25 values are negative. Even the
     pediatric sum (0-0.49 + 0.5-0.99 + 1-1.99 + 2-4) differs from the file's own 0-4 by -11% to +10% in 2024-25, so
     counts made from rate x population are not additive.
   - I consider R4 the fair, literal reading, but the criterion skeptic should weigh this.
2. **Choice of truth.**
   - Using only the hub's direct group (0-130 tasks, 980) gives rel -0.2945 (the author's interval [-0.3889, -0.2130]).
   - Truth from the season-end vintage 2025-05-16 gives rel -0.2538, 90% [-0.3426, -0.1687] with my seed 777. This
     matches the author's point value of -0.2538.
   - The author reports, and I did not recompute, that with truth = the first report of each week ours is WORSE: rel
     +0.2627 [+0.0283, +0.4938]. Per DISCLOSURES item 3, the hub README asked teams to forecast raw, unadjusted data,
     while this pipeline adds a backfill nowcast. The result therefore depends on scoring against revised data, which
     is the hub's current target data as the criterion specifies.
3. **Second season.** DISCLOSURES item 8 (attempts/evaluator/test/score_2023-24_descriptive.log, which I read but did
   not recompute) reports that the same frozen pipeline on the 2023-24 dev season is worse than the ensemble: rel
   +0.1861, 90% [-0.0507, +0.3181]. So the 2024-25 result does not replicate on a second season. The criterion needs
   only one season; the bank's pitfall asks for replication "if possible".
4. **Scorer.** The criterion names "the public hubverse scoring code" (R scoringutils/hubEvals). Neither the author nor I
   ran the R code, since no installs were allowed. Two independent Python implementations of the documented formula
   agree with each other and across two forms to about 2e-12.
5. **Archive vintages not downloaded.** The live archive has 153 vintages, of which 80 are in data/hopkins/. The 73
   missing ones are dated 2024-05-24 .. 2024-09-27 and 2025-05-23 .. 2026-05-29, so none falls in the origin window.
   By the frozen rules they could not become a data vintage. The summer ones would be excluded from the revision factors
   by the October-April filter, assuming their last week falls in May-September. I did not download them to confirm.
   Using a subset of the archive cannot leak future data.
6. **Amendment originals not in the package.** The pre-amendment code (the original model_rsv.py and asof_rsv.py) and
   attempts/forecaster/result/forecasts_v3_unscored/ are not in the package, so the claim that "only 2024-11-24 changed
   under v4" cannot be re-run directly. My as-of check shows that 2024-11-24 is the only origin where the v4
   per-location rule changes anything, which supports that claim.

pass: true
