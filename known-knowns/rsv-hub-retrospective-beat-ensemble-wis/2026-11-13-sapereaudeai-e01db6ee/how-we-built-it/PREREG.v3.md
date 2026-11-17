# PREREG.v3: p3 recomputation object (written 2026-11-13T02:53:41Z by date -u)

Context: the decisive scoring of PREREG.md was done at 2026-11-13T02:48:27Z..02:48:47Z (MAIN not met, p1 not met;
attempts/evaluator/test/score_test_2025-26.log). Nothing in this amendment changes any reading of PREREG.md or
PREREG.v2.md, and no new forecast of ours is scored for any claim. This adds a separate, enumerated partial win:

p3 (verbatim): "An independent recomputation of per-model season WIS for a completed RSV season from the hub's raw
model-output and target data, released as a reproducible script, documenting any discrepancy with the hub's own
published scores (if any) and the exclusion rules needed to reconcile them."

Object: a table of per-model season-average WIS for the 2025-26 season of CDCgov/rsv-forecast-hub (commit e947ca8),
for BOTH targets (wk inc rsv hosp, wk inc rsv prop ed visits), produced by one deterministic script from the hub's raw
model-output files and target-data/oracle-output.parquet at that commit:
- season = files with reference_date 2025-09-01..2026-08-31; every model directory with quantile rows for the target;
- per model: tasks, reference dates, mean WIS over all its scored tasks (wis.py), MAE of the median, 50% and 95%
  interval coverage; mean WIS on the RSVHub-ensemble's tasks it shares; scoringutils-style pairwise relative WIS
  (geometric mean of pairwise ratios over common tasks, scaled to RSVHub-baseline; wis.relative_skill);
- truth = oracle_value, quantile rows only (the oracle repeats each value for output_type quantile and sample);
- documented exclusions/reconciliation: tasks without oracle truth, incomplete quantile sets, files outside the
  ensemble's dates, the ensemble's missing horizon -1 on some dates.
Reconciliation: the hub publishes no scores (scout.md); the only published per-model scores for this season are
arXiv 2605.16238 v2 Supplementary Table 6 (hosp; 52 states, horizons 0-3, reference dates 2026-01-03..2026-05-30);
tolerance as in PREREG.md (|diff| <= 0.05 + 2% of the published mean WIS); the script reproduces that subset too.
p3 is met iff the script runs from the raw files, the table covers every model directory with 2025-26 quantile
forecasts for each target, the published subset reproduces within the tolerance (or the discrepancy is explained by a
stated rule), and pinball and interval forms agree on every row.
