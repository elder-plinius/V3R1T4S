# PREREG: rsv-hub-retrospective-beat-ensemble-wis, run 2026-11-13-0104

Written 2026-11-13T01:20:56Z (date -u), before any forecast of ours exists and before any WIS of any model, ensemble or
of ours has been computed. Structural facts already read (no values, no truth-vs-forecast comparison): hub task sets per
season and model (attempts/evaluator/task_sets.txt), the age groups and missingness pattern of the final target-data file,
and the format of the first three archive vintages.

## Criterion (verbatim; full text with partial wins in target.md)
"Success means, on ONE of two separately declared routes, saved quantile forecasts in that hub's submission format
produced by a released deterministic pipeline that at each reference date reads only data available on that date
(as-of vintages; no final revised series, no other team's forecasts, no parameter tuned on later weeks of the same
season), whose season-average WIS, computed with the public hubverse scoring code (same locations, horizons, reference
dates and, where applicable, age groups; hub exclusion rules applied), is STRICTLY LOWER (direction: min) than the hub
ensemble's season-average WIS recomputed identically from that hub's own ensemble model-output, re-fetched live
immediately before claiming, by at least 3% relative AND outside a stationary-bootstrap 90% interval over reference
dates. Route (a), archive: a completed season (2023-24 or 2024-25) of github.com/HopkinsIDD/rsv-forecast-hub, covering
every reference date, location, age group and horizon of the hub-ensemble (...), with as-of data taken from that hub's
target-data/archive vintages. [...]"
p1: "Strictly lower season-average WIS than every individual submitted model (not necessarily the ensemble) for a
completed season, under the as-of data discipline and the public scorer, with a bootstrap interval excluding zero."
p2: "Route (a) only: beat the ensemble's WIS restricted to the pediatric (0-4 years) age groups of the HopkinsIDD archive
hub, where RSV dynamics are sharpest and the submitted pool is thinnest, across all locations and reference dates of a
completed season (the CDCgov hub has no age groups)."

## Readings frozen now (the most favourable FAIR reading, chosen before any result)
R1. Route (a) only: HopkinsIDD/rsv-forecast-hub pinned at commit 6bf251ac3fc798e55ed95d0b7269f5f5781c0207.
R2. Seasons, by this rule: TEST = 2024-25 and DEV = 2023-24 (plus earlier seasons from vintage history), unless the
    2024-25 hub-ensemble lacks the pediatric groups or some 2024-25 ensemble reference date has no archive vintage dated
    on or before it; then TEST = 2023-24 and DEV = seasons up to 2022-23 only. Checked structurally (task_sets.txt and the
    vintage map in data/hopkins/fetch_list_vintages.tsv): 13 of the 14 non-empty 2024-25 ensemble files carry 0-0.99 and
    1-4, and every 2024-25 origin date has a vintage dated on or before it. So TEST = 2024-25, DEV = 2023-24 and earlier.
    The 2024-25 data are not opened by any development code; 2024-25 forecasts are produced only after METHOD_FREEZE.md.
R3. As-of rule: for origin_date O (a Sunday), the pipeline reads only target-data/archive/<D>_rsvnet_hospitalization.csv
    files with D <= O (D from the file name; the 2023-24 hub README sets this convention: origin 2023-10-22 uses "data
    pulled on 10-20-2023"). The latest such file is the data; earlier such files may be used to estimate revisions.
    Never target-data/2026-06-05_rsvnet_hospitalization.csv, never model-output/, never a later vintage.
R4. Truth: target-data/2026-06-05_rsvnet_hospitalization.csv at the pinned commit (the hub's current target data, the
    hubverse oracle), target "inc hosp", keyed by location, age_group, date = target_end_date = origin_date + 7*horizon - 1
    (as in the hub's scripts/ensemble.R). The submission age groups that the target file does not carry are its exact
    sums: 0-0.99 = 0-0.49 + 0.5-0.99; 1-4 = 1-1.99 + 2-4; 5-64 = 5-17 + 18-49 + 50-64 (a task is scored only when every
    component is non-missing). 0-130 is direct. The final target file has no 65-130 rows for 2023-24 or 2024-25, so
    65-130 tasks have no truth and are unscored for every model (we still submit them). Tasks with missing truth are
    unscored for every model. This is the hub exclusion applied: the hub publishes no other scoring exclusions.
R5. WIS: the hubverse/scoringutils quantile WIS (weigh = TRUE, median counted once) on the hub's 23 levels, computed by
    attempts/evaluator/code/wis.py (pinball form; checked against the interval form). Season-average WIS = arithmetic mean
    over scored tasks (one task = origin_date x location x age_group x horizon), as scoringutils summarise_scores by model.
R6. Main criterion task set: every (origin_date, location, age_group, horizon) in the 2024-25 hub-ensemble files
    (model-output/hub-ensemble, 14 non-empty files; 2024-12-01-hub-ensemble.parquet has 0 rows and adds no task), restricted
    to scored tasks (R4). Our forecasts must cover all of them (the pipeline produces every location x {0-130, 0-0.99, 1-4,
    5-64, 65-130} x horizon -1..5 for every 2024-25 round origin date).
R7. Bootstrap: stationary bootstrap (Politis-Romano) over the reference dates of the compared task set in chronological
    order, mean block length 3, B = 10000, seed 20261113; each resampled date brings all its tasks; statistic r =
    (mean WIS ours / mean WIS comparator) - 1 on the resample; the 90% interval is the 5th..95th percentile.
    Main criterion met iff point r <= -0.03 AND the 95th percentile of r < 0.
R8. p1: "every individual submitted model" = every model-output directory other than hub-ensemble with at least one
    quantile forecast for an origin date in 2024-10-01..2025-07-31: CEPH-Rtrend_rsv, CU-RSV_SVIRS, JHU_CSSE-RSV,
    Metaculus-cp, UGA_flucast-INFLAenza, UM-DeepOutbreak, and also hub-baseline (included although it is the hub's
    baseline, not a team submission). Each model is compared with us on ITS OWN scored tasks of the season (all its
    origin dates, locations, age groups, horizons), our forecast for the same task; files with 0 rows add nothing.
    p1 met iff for every one of these models: point r < 0 AND the 95th percentile of r < 0 (R7 bootstrap over that
    model's reference dates).
R9. p2: tasks of the 2024-25 hub-ensemble with age_group in {0-0.99, 1-4} (the hub's 0-4-year submission groups), all
    locations and reference dates, scored per R4. p2 met iff point r < 0 AND the 95th percentile of r < 0 (R7). No 3%
    margin (p2 states none); the interval follows the bank's thin-pool pitfall.
R10. Re-fetch: before any claim the hub-ensemble files of the test season are re-fetched (or their git blob SHAs
    re-listed) and the score recomputed if anything changed.

## Statistic, thresholds and decision
As R5-R9. One frozen forecaster, one test season, scored once. No variant is scored on 2024-25 for selection.

## Development protocol (before the freeze)
- DEV data: as-of forecasts for the 2023-24 origin dates of the hub-ensemble files (R3 rule), scored with R4/R5 against
  the same final truth file restricted to 2023-24 target dates; pseudo-forecasts on earlier seasons from early vintages
  allowed. Selection statistic: ratio of our mean WIS to the hub-ensemble's mean WIS on the 2023-24 ensemble tasks
  (real-time file where both a RETRO and a real-time file exist), with the p2 ratio and the per-model p1 ratios reported.
- At most 40 configurations. The chosen one is frozen in attempts/forecaster/METHOD_FREEZE.md (time from date -u,
  sha256 of code and parameters) before any 2024-25 forecast is produced.

## Null design
null_test: not needed because the claims compare one frozen forecaster with named comparators on a held-out season using the bank's own stationary-bootstrap interval (no search over models, seasons or targets on the scored season); a reference-date sign-flip permutation of the paired differences is reported descriptively only.

## Escape hatches (declared now)
E1. If wis.py's two forms disagree on hub files (> 1e-9) the scorer is not used and nothing is claimed.
E2. A hub file that cannot be parsed is excluded for its model and reported (no such file found so far; one ensemble file
    is empty and adds nothing).
E3. If the frozen pipeline crashes on a 2024-25 origin, only a crash fix that leaves every already-produced output
    byte-identical is allowed, recorded in PREREG.v2.md; otherwise that origin uses the pipeline's frozen fallback.
E4. Main criterion, p1 and p2 are judged separately; each passing one is its own claim (one claim per object).
E5. 2023-24 scores of the frozen model are in-sample (dev) and are reported as descriptive only, never as a claim.
E6. If the hub's target data changes before claiming, both truths are reported and the claim uses the file present at
    claim time (re-fetched).

## Baseline (kit step 3c)
No published score exists for either hub (scout.md: no scores file; the hub dashboard's Evaluation tab is empty). So no
published baseline can be reproduced. The baseline record (baseline/) is the recomputation of every 2023-24 model's and
the hub-ensemble's season WIS by our scorer (dev season), with the interval form agreeing, and an independent check that
the hub-ensemble files equal the mean of their members' quantiles (sanity only; the file itself is the comparator).
Expected score: none published; tolerance: two scorer forms within 1e-9.
