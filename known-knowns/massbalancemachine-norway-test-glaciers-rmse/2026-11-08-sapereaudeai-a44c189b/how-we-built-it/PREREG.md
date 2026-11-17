# PREREG (frozen before any re-scoring in this run; time on the frozen_at line, from date -u)

Nothing in this run has been scored yet. Run 2026-11-08-1646 already saw 0.9962 / 0.5881 / 0.7001 from a retrain
with the same configuration; this prereg fixes the definitions and the pass rule for a clean, single-file rebuild.
It is not a blind prediction.

## Criterion (verbatim, bank partial win p3)
"Reproduce MBM's three test RMSEs within 0.01 m w.e. from the shipped CSVs with an independent re-implementation
(validates the split and scorer)."

## Published values (quoted from khsjursen/ML_MB_Norway @ 32d8175, src/3.1.1_ML_model_performance_test.ipynb, cell 36 output)
- "Mass Balance Machine - Ba: RMSE=1.00, MSE=0.99, MAE=0.77, Bias=-0.01, R²=0.64, Count=1065"
- "Mass Balance Machine - Bw: RMSE=0.59, MSE=0.35, MAE=0.46, Bias=-0.01, R²=0.66, Count=999"
- "Mass Balance Machine - Bs: RMSE=0.70, MSE=0.49, MAE=0.54, Bias=0.04, R²=0.72, Count=1028"

## What "independent re-implementation" means here
Own code (written in this workspace, one file claim/code/reimpl_p3.py; it imports nothing from the repository's
scripts/ or notebooks and never loads custom_loss_cv_grid.pkl):
1. Record building from the shipped wide CSV (2023-08-28_..._climate_svf.csv): one monthly row per (stake record,
   month) for annual (Oct-Sep, 12 months, balance_netto), winter (Oct-Apr, 7, balance_winter) and summer (May-Sep, 5,
   balance_summer), each season only where its balance is present; feature altitude_diff = altitude_climate -
   altitude; climate features t2m, sshf, slhf, ssrd, fal, str, tp taken from the matching month's column.
2. The split: test = the 14 BREIDs quoted from notebook 2.1.1 ("test_glaciers = [54, 703, 941, 1135, 1280, 2085,
   2320, 2478, 2768, 2769, 3133, 3137, 3138, 3141]"), train = all other rows (18 glaciers).
3. The one test cleaning rule quoted from notebook 2.1.1 cell 5: "# Remove strange value / df_test_winter =
   df_test_winter[df_test_winter['balance_winter'] != 9.99]".
4. The aggregated objective: loss 0.5 * (sum over a record's months of the monthly predictions - record balance)^2;
   gradient = (record sum - record balance) broadcast to each of its months; hessian = 1.
5. The training call (xgboost.train with that objective).
6. The scorer: sum monthly predictions per record; RMSE per season over that season's records; record counts.

Shared, not re-implemented: the xgboost library (3.2.0) as tree learner; MBM's selected hyperparameters quoted from
notebook 2.1.1 cell 52 output (max_depth=5, learning_rate=0.05, n_estimators=300, gamma=0, min_child_weight=0;
others xgboost defaults) and base_score 0.5 from the shipped booster JSON's learner_model_param ('5E-1'); MBM's 11
feature names in the shipped test CSV's column order; the shipped data. tree_method hist (the xgboost 3.x default),
subsample 1, colsample 1, seed 0, nthread 4.

## Primary statistic and pass rule
- Primary: our model's RMSE per season over our own test records (rebuilt from the wide CSV, after rule 3).
- Pass: for each of Ba, Bw, Bs: |RMSE_ours - published| <= 0.01, where published is the printed value above (1.00,
  0.59, 0.70), AND the record counts equal 1065 / 999 / 1028 exactly. All three must pass. Report 4 decimals.
- One primary run only. If it misses, p3 is not met here; no retuning, no other configuration substituted.

## Secondary checks (reported; they can void the claim if they contradict it, never rescue it)
(a) our test records' targets equal the shipped monthly test CSV's record targets per season (sorted, allclose);
(b) the shipped booster scored by the same scorer on our records gives values within 0.01 (scorer check);
(c) our model scored on the shipped monthly test CSV (aggregated by its id column) gives the same RMSEs as the primary;
(d) rerunning gives bit-identical predictions; (e) known negatives: zero prediction and record-shuffled predictions
must fall outside the tolerance (checker negative test);
(f) a second scorer in pure Python (no numpy/pandas) on the saved record-level predictions agrees to 1e-9.

## Lens 2 (contrarian, exploratory, no claim)
Determinism across seeds 0-2, nthread 1 vs 4, tree_method hist/approx/exact; the 9.99 rule's effect; and
discrimination: the configurations of MBM's notebook-2.1.1 grid (max_depth 3/4/5, learning_rate 0.01/0.1,
n_estimators 100/200/300/400) retrained the same way; report how many land within 0.01 of all three values.
If many do, the report says p3's tolerance does not single out MBM's configuration.

null_test: not needed because this is a deterministic reproduction of three published values checked against a fixed tolerance by a deterministic scorer (no search, no "beats chance" statistic); known-negative controls (e) are run instead.

## Baseline (kit/RUN.md step 3c)
The baseline is MBM itself (Sjursen et al. 2025, TC 19:5801), repository khsjursen/ML_MB_Norway @
32d8175adab27963c6ca2766f2420f24cdb72a6b; data: the shipped wide CSV (sha256 43597e76...a1a61b) and test CSV (sha256
d1d34e08...0f1c); split by the 14 test BREIDs; metric RMSE over point records per season (sum of monthly
predictions per record); expected 1.00 / 0.59 / 0.70 (n 1065/999/1028); tolerance 0.01 (the criterion's own).
frozen_at: Sun Nov  8 17:33:32 UTC 2026
frozen_at_iso: 2026-11-08 17:33:42 UTC (format line added at the same minute as the freeze, before any scoring)
