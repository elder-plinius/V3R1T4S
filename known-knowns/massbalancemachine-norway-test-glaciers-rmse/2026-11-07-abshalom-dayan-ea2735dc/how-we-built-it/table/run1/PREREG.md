# PREREG: massbalancemachine-norway-test-glaciers-rmse

Written 2026-11-07T14:37:53Z (from `date -u`), before any test-glacier prediction was scored by this run.
Counts 1065 / 999 / 1028 were checked on the test CSV (row structure only, no prediction made) before this file.

## Criterion (verbatim, repo/bank/targets.json)

A saved, runnable model (code, fixed seeds) trained only on rows from the 18 training glaciers in the shipped CSVs
(hyperparameters chosen by cross-validation within those glaciers only). Inputs are only the shipped features or
other public static data (DEM, RGI outlines), never any mass-balance, geodetic or glacier-wide observation of a test
glacier. It predicts every test-glacier point balance, and its RMSE against the observed values over the same 1065
annual, 999 winter and 1028 summer measurements must be strictly lower (direction: min), at 2-decimal rounding, than
MBM's for all three: Ba <= 0.99, Bw <= 0.58 and Bs <= 0.69 m w.e. The RMSE is computed by an independent script and
checked against MBM's numbers reproduced from the repository notebook. The result must also beat any RMSE on these
same full test sets, by a model that uses no observation of a test glacier, in a paper from the last 24 months found
by a fresh search. Numbers from models calibrated on test-glacier geodetic data (e.g. the paper's GloGEM 0.91 and
OGGM 0.93 annual RMSE for 1980-2019) and numbers on sub-periods do not set the bar.

Partial wins counted this weekend (NEXT_RUN.md): p1 and p2 (verbatim in target.md). p3 is the baseline gate below.

## Inputs (frozen)

- Training: `src/Data/2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_svf_monthly.csv`
  sha256 19e10b018db4e291f4e9e99dcc908ca08a82ef25817b633a3b809b3b30200e94 (67909 monthly rows, 18 glaciers, 8498 point balances).
- Test: `src/Data/2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_test_svf.csv`
  sha256 d1d34e0821a9147a3a166b6dc4ee8cee8abed8a288e2ab89cdd107273f100f1c (24913 monthly rows, 14 glaciers).
- Both fetched 2026-11-07T14:35Z from raw.githubusercontent.com/khsjursen/ML_MB_Norway/main (MIT licence; stake data
  NVE, doi:10.58059/sjse-6w92).
- Model inputs allowed: the shipped feature columns altitude_diff, aspect, slope, skyview_factor, t2m, sshf, slhf,
  ssrd, fal, str, tp, plus the shipped structure columns month and n_months, and functions of these. Not used as
  inputs: balance (target only), id, BREID, RGIID, year, altitude, altitude_climate, and no other file. No NVE
  glacier-wide, geodetic or Hugonnet file is read by any model.

## Statistic (frozen)

For each season s in {Ba: n_months 12, Bw: 7, Bs: 5}: each test point balance is one unique `id` in the test CSV
with that n_months; prediction = sum of the model's monthly predictions over that id's rows (exactly MBM's
`get_ytrue_y_pred_agg_season`); observed = the id's `balance` (constant within id, mean taken). RMSE_s =
sqrt(mean((pred - obs)^2)) over all ids of that season. Counts must be 1065 / 999 / 1028 or the score is void.
Scorer: `lib/score.py` (written by this run from the definition, not MBM's code).

Thresholds:
- Main: round(RMSE_Ba,2) <= 0.99 and round(RMSE_Bw,2) <= 0.58 and round(RMSE_Bs,2) <= 0.69, AND the same holds
  against MBM's numbers as reproduced below (if the reproduction gives different 2-decimal values, the bar is the
  lower of published and reproduced for each season).
- p1: at 2-decimal rounding, one season strictly below MBM's (1.00 / 0.59 / 0.70) and the other two <= MBM's.
- p2: a model with at most 20 fitted parameters (every coefficient, scale and threshold fitted to data counts; fixed
  constants such as 273.15 K do not) and raw (unrounded) RMSE_Bw <= 0.5900. The rounded value is reported too.

## Baseline (step 3c, frozen)

- Baseline: MBM's shipped trained model `src/Training_cluster/2024-10-24_10-30-28/custom_loss_best_model.json`
  sha256 a7ddf96b2f11a51dd8415fbe6190f95671c23123526e200533fb09aae74e1d0d (XGBoost JSON, 300 trees, 11 features,
  base_score 0.5), evaluated by this run's own numpy tree walker (float32 features, go left when x < split value,
  default direction on missing).
- Source: notebook `src/3.1.1_ML_model_performance_test.ipynb` (sha256 b6226ca7...599ad) cell 36 output:
  "Ba: RMSE=1.00 ... Count=1065; Bw: RMSE=0.59 ... Count=999; Bs: RMSE=0.70 ... Count=1028" (period 1960-2021 = all test rows).
- Caveat recorded before running: the notebook loads the pickled GridSearchCV best estimator
  (`custom_loss_cv_grid.pkl`, not fetched, 4.3 MB); the JSON is assumed to be the same booster. If it is not, the
  reproduction misses.
- Expected: 1.00 / 0.59 / 0.70 at 2 decimals; tolerance 0.01 per season (p3 wording). Counts must match exactly.
- A miss makes the comparison unresolved: no improvement is claimed against it.

## Model selection and test discipline (frozen)

- Hyperparameters and model choices are chosen only by glacier-grouped cross-validation on the 18 training glaciers:
  6 folds, glaciers assigned to folds by a fixed greedy balance of point counts (largest first, seed-free), every
  glacier wholly in one fold. CV score = mean over the three seasons of the pooled out-of-fold RMSE.
- Every model is frozen (config + code sha256 written to `attempts/{lens}/frozen_*.json`) before its test score is
  computed. Every test scoring is appended to `test_ledger.tsv` (time, model, sha, Ba, Bw, Bs). All scored models
  are reported, not only the best. At most 8 test scorings in this run.
- A claim may only come from a model that its lens named as primary (by CV) before its test scoring. A model chosen
  because of its test score is not a claim.
- Seeds fixed; the claimed model must reproduce its test RMSE to 4 decimals from a fresh shell.

## Null test

null_test: not needed because the claim is an explicit frozen model scored once by a deterministic RMSE scorer against fixed table values set by the bank criterion; no search is run on test data. Supplementary (not gating): a glacier-block bootstrap (2000 resamples of the 14 test glaciers, seed 0) of RMSE(model) - RMSE(MBM) per season is reported for any claimed model, so its spread is visible.
