# PREREG: rsv-hub-retrospective-beat-ensemble-wis, ROUTE (B), run 2026-11-13-0233

Written 2026-11-13T02:41Z (date -u at 02:40:48Z just before writing), before any 2025-26 forecast of ours exists and
before any model, ensemble or baseline file of the hub has been scored by this run. Nothing scored on 2025-26 so far.
Facts read before writing (data availability only, no scores): hub-config, README, time-series.parquet as_of ranges,
oracle-output date range, file lists (scout.md), and pre-season (as_of <= 2025-09-24) NHSN revision ratios
(attempts/evaluator/out/revisions_preseason.txt: final/reported 1.072 at lag 0, 1.012 at lag 1, <= 1.006 later).

## Criterion (verbatim from bank/targets.json)
Success means, on ONE of two separately declared routes, saved quantile forecasts in that hub's submission format
produced by a released deterministic pipeline that at each reference date reads only data available on that date
(as-of vintages; no final revised series, no other team's forecasts, no parameter tuned on later weeks of the same
season), whose season-average WIS, computed with the public hubverse scoring code (same locations, horizons, reference
dates and, where applicable, age groups; hub exclusion rules applied), is STRICTLY LOWER (direction: min) than the hub
ensemble's season-average WIS recomputed identically from that hub's own ensemble model-output, re-fetched live
immediately before claiming, by at least 3% relative AND outside a stationary-bootstrap 90% interval over reference
dates. [...] Route (b), live hub: the 2025-26 season of github.com/CDCgov/rsv-forecast-hub for wk inc rsv hosp or wk
inc rsv prop ed visits, against RSVHub-ensemble (https://github.com/CDCgov/rsv-forecast-hub/tree/main/model-output/RSVHub-ensemble),
with as-of data taken from that hub's time-series.parquet as_of column or from data.cdc.gov releases available at each
reference date. Neither hub currently publishes its own scores file; if one appears for the claimed season, its
ensemble value becomes the bar instead of the recomputed one.
p1 (verbatim): Strictly lower season-average WIS than every individual submitted model (not necessarily the ensemble)
for a completed season, under the as-of data discipline and the public scorer, with a bootstrap interval excluding zero.
(p2 is route (a) only; p3 is not attempted as a claim in this run.)

## Readings frozen now (most favourable FAIR reading chosen before any result)
R0. Route: (b), CDCgov/rsv-forecast-hub pinned at commit e947ca8fe8d50a581a181e6aefacfe922ba95af5 (ls-remote
    2026-11-13T02:34:34Z). Live re-fetch of the comparator before any claim (R11).
R1. TARGET RULE: the primary target is the one for which the hub's time-series.parquet holds as-of vintages covering a
    complete season BEFORE 2025-26 (needed to freeze the method on pre-season as-of data, as the human asked); if both
    or neither qualify, wk inc rsv hosp (the hub's mandatory target, the one closest to route (a)'s hospitalisation
    counts). Applying it: hosp vintages start 2024-11-27 (whole 2024-25 season), ED vintages start 2025-06-13 (no
    pre-season season) -> PRIMARY TARGET = wk inc rsv hosp. The ED target is not scored in this run (if time allows,
    descriptive only, never a claim).
R2. SEASON / TASK SET: every RSVHub-ensemble file at the pinned commit with reference_date in 2025-09-01..2026-08-31
    (the 2025-26 challenge period: 2025-09-27 and 2025-11-22..2026-05-30, 29 files), target wk inc rsv hosp,
    output_type quantile; one task = (reference_date, location, horizon). Every such task is in the main task set.
    The hub publishes no exclusion rules; the only exclusion is R3's (no truth -> unscored for everyone).
R3. TRUTH (scoring): target-data/oracle-output.parquet at the pinned commit (sha256 bed6c1a1e33cfc03687cc6fc645d00353c82ddf183cd0803189c94a008fd5189),
    rows target == wk inc rsv hosp, matched on (location, target_end_date). A task without an oracle value is unscored
    for every model. Descriptive checks reported next to it (never decisive): (a) FIRST-REPORT truth = the value of
    that week in the earliest time-series vintage containing it; (b) the US vs states split; (c) the 2026-11-12
    time-series vintage as truth (consistency check with the oracle).
R4. WIS: hubverse/scoringutils quantile WIS on the hub's 23 levels (weigh = TRUE, median once), = mean over levels of
    2 x pinball loss, computed by attempts/evaluator/code/wis.py (copied unchanged from run 2026-11-13-0104, where it
    matched the interval form to 3e-12 and reproduced the FluSight hub's published scoringutils table to two decimals
    in run 2026-11-12-1832). The R hubEvals code itself cannot be run here (no installs); say so in any claim.
    Season-average WIS = arithmetic mean over scored tasks pooled over reference dates (summarise_scores by model).
R5. AS-OF RULE: for reference date R the due date is W = R - 3 days (Wednesday). Our pipeline reads ONLY the rows of
    the single time-series.parquet vintage with the largest as_of <= W (string date compare), target wk inc rsv hosp
    (e.g. R = 2025-12-27 -> as_of 2025-12-17, because the hub has no vintage between 12-18 and 12-24), plus vintages
    with smaller as_of for the revision table, plus auxiliary-data/locations.csv (populations). Never
    oracle-output.parquet, never any later vintage, never model-output/. Audited by rerunning on a time-series file
    truncated to as_of <= W (R10).
R6. MAIN criterion: r = (mean WIS ours / mean WIS RSVHub-ensemble) - 1 on the R2 task set restricted to scored tasks,
    our forecast for the same task. Stationary bootstrap (Politis-Romano) over the reference dates of the compared task
    set in chronological order, mean block length 3, B = 10000, seed 20261113; each resampled date brings all its
    tasks; 90% interval = 5th..95th percentile of r. MAIN met iff point r <= -0.03 AND 95th percentile < 0.
R7. p1 reading (ambiguity: "every individual submitted model" vs a model that submitted a handful of files, which has
    no season-average in any meaningful sense): the binding p1 set is every model-output directory other than
    RSVHub-ensemble whose wk inc rsv hosp quantile forecasts cover at least 75% of the R2 scored tasks (the inclusion
    rule of CDC's own FluSight 2025-26 evaluation, "models had to submit at least 75% of forecast targets"),
    INCLUDING RSVHub-baseline if it qualifies. Each eligible model is compared with us on ITS OWN scored tasks of the
    season (its reference dates in R2's window, all its locations and horizons), with R6's bootstrap over its
    reference dates. p1 met iff for every eligible model: point r < 0 AND 95th percentile of r < 0. Reported
    descriptively as well (never decisive): the literal every-directory reading (all models with >= 1 file, each on
    its own tasks).
R8. Coverage: our pipeline produces all 53 locations x horizons -1..3 x 23 quantiles for each of the 29 reference
    dates, so every task of the ensemble and of every model is covered. No placeholders. FALLBACK (pre-declared): if the
    kernel-analog component cannot forecast a location at a reference date (no data, last observation more than 8
    weeks old, NaN or exception), that location's quantiles come from a flat baseline: median = last observed value
    in the vintage; quantiles = last value + weighted empirical quantiles of the location's own s-step differences
    (s = horizon + 1) over the vintage's last 52 weeks, symmetrised (d and -d), clipped at 0, monotone. The number of
    fallback series is reported.
R9. Descriptive (never decisive): US-only and states-only r; first-report truth r; per horizon; the ERA paper's task set
    (52 states, horizons 0-3, reference dates 2026-01-03..2026-05-30).
R10. Look-ahead audit: rerun the frozen pipeline for every test reference date on a copy of time-series.parquet
    truncated to as_of <= W; forecasts must be byte-identical.
R11. Re-fetch: before any claim the 29 RSVHub-ensemble files are re-fetched live (raw.githubusercontent.com, main) and
    compared byte-for-byte; if anything changed, the live version is scored (bank wording) and the change reported.

## Baseline reproduction (kit step 3c)
- No hub-published scores exist. Published third-party baseline: arXiv 2605.16238 v2, Supplementary Table 6
  (RSV): task set 52 jurisdictions excluding US, horizons 0-3, 22 reference dates (due 2025-12-31 .. 2026-05-27, i.e.
  reference dates 2026-01-03 .. 2026-05-30), 4,576 tasks; mean WIS RSVHub-ensemble 16.4, RSVHub-baseline 18.3,
  CEPH-Rtrend_rsv 19.8, Google_SAI-RSVEns 14.7 (one decimal); MAE 25.3 / 27.8 / 28.4 / 21.2.
- Our reproduction: same task set from the pinned model-output files, scored with wis.py against R3's oracle. Truth
  version of the paper is not stated (fetched before v2, 2026-10-14). Tolerance: |ours - published| <= 0.05 + 2% of
  the published value (rounding plus possible later NHSN revisions); also reported with the time-series vintage
  2026-06-03 (closest to the end of the paper's window) as truth. If it misses, the comparison with the paper is
  unresolved and reported as a finding; the bank's bar is the recomputed ensemble in any case.

## Method freeze protocol (before any 2025-26 forecast)
Method family: route (a)'s V3R1T4S-asofKA (runs/2026-11-13-0104/attempts/forecaster/code/model_rsv.py and its frozen
FROZEN_PARAMS.json): kernel analogs on log weekly rates per 100k pooled over series, plus a backfill (revision)
correction learned from earlier vintages. Mechanical adaptation to route (b): series = 53 locations (one "age group"
"all"), population from locations.csv, horizons -1..3 with target_end_date = R + 7h, data last week T = the vintage's
last Saturday, revision table from earlier hub time-series vintages (route (a) rule: vintages whose last week is
<= T - 26 weeks and falls in Oct..Apr; lags 0..10; pooled over locations).
DEV (only pre-2025-26 data): pseudo reference dates R = every Saturday 2024-11-30 .. 2025-05-31 with a vintage
as_of <= R - 3; forecasts from R5's rule; truth = the 2025-09-24 vintage (the last before the first 2025-26 due date);
statistic = mean WIS over all 53 locations x horizons -1..3; reported relative to a flat baseline (R8's fallback model
used for every series). Dev configurations (at most 8, declared now):
  D0 = route (a) frozen parameters, mechanically adapted (PRIMARY);
  D1 = D0 with mult 1.0; D2 = D0 with loc_w 1.0; D3 = D0 with bw (1,1,1,1) and bw_woy 4.0 (route (a) defaults);
  D4 = D0 with gap 8 (revision table from 8-week-old vintages); D5 = D0 with guard 2;
  D6 = D0 with nowcast_mult 1.0; D7 = D0 with the analog library start t0 = 26 instead of 52 weeks.
FREEZE RULE: the frozen configuration is D0 unless another configuration's dev mean WIS is at least 3% below D0's, in
which case it is the configuration with the lowest dev mean WIS. Caveat known in advance: the hub's data start
2023-10-07, so for dev origins the analog library (anchors need 52 weeks of history) is thin; dev is a weak guide and
D0 is preferred by the rule. Frozen in attempts/forecaster/METHOD_FREEZE.md (date -u, sha256 of code and parameters)
before any 2025-26 forecast is produced. 2025-26 forecasts are produced once and scored once.

## Escape hatches (declared now)
E1. A crash of the frozen pipeline on a test reference date may be fixed (code-only, no parameter change) before any
    2025-26 score, in a timestamped PREREG.v2.md; if the fix is not possible, R8's fallback covers the series.
E2. If the comparator files change at the R11 re-fetch, the live version is scored.
E3. If the main criterion fails, p1 is still read from the same single scoring; if both fail, the result is reported
    as a failed replication (status NOTHING or a negative result), never re-tuned on 2025-26.
E4. If a task of the ensemble has no oracle truth, it is unscored for everyone (R3).

## Null design
null_test: not needed because the claim compares one frozen forecaster with named comparators on a held-out season using the bank's own stationary-bootstrap interval (no search over models, seasons or targets on the scored season); a reference-date sign-flip permutation of the paired differences is reported descriptively only.
