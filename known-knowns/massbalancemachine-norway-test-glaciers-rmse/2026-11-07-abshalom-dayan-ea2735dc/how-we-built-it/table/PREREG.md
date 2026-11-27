# PREREG: massbalancemachine-norway-test-glaciers-rmse (run 2026-11-07-1740)

Written 2026-11-07T17:46:19Z (from `date -u`), before this run scored anything on the test glaciers. Its sha256 and this time are
the first line of this run's `test_ledger.tsv`, written right after this file; the file is then made read-only.
This run continues runs/2026-11-07-1434 (its PREREG.md, written 2026-11-07T14:37:53Z, stays in force for that run's
six scorings). This file adds rules; it loosens nothing from the first one.

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
Criterion and partial-win text unchanged from runs/2026-11-07-1434/PREREG.md (same bank entry at repo_commit 06b61ea).

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
Scorer: `code/score.py` (byte-identical to runs/2026-11-07-1434/lib/score.py, written from the definition, not MBM's code).

Thresholds:
- Main: round(RMSE_Ba,2) <= 0.99 and round(RMSE_Bw,2) <= 0.58 and round(RMSE_Bs,2) <= 0.69, AND the same holds
  against MBM's numbers as reproduced below (if the reproduction gives different 2-decimal values, the bar is the
  lower of published and reproduced for each season).
- p1: at 2-decimal rounding, one season strictly below MBM's (1.00 / 0.59 / 0.70) and the other two <= MBM's.
  (Bars are the same as in runs/2026-11-07-1434/PREREG.md; nothing is loosened.)
- p2: a model with at most 20 fitted parameters (every coefficient, scale and threshold fitted to data counts; fixed
  constants such as 273.15 K do not) and raw (unrounded) RMSE_Bw <= 0.5900. The rounded value is reported too.

## Baseline (step 3c, frozen)

- Baseline: MBM's shipped trained model `src/Training_cluster/2024-10-24_10-30-28/custom_loss_best_model.json`
  sha256 a7ddf96b2f11a51dd8415fbe6190f95671c23123526e200533fb09aae74e1d0d (XGBoost JSON, 300 trees, 11 features,
  base_score 0.5), evaluated by the numpy tree walker `code/xgb_json_walk.py` (runs/2026-11-07-1434/baseline/xgb_json_walk.py with only its import-path line and output-path argument changed) (float32 features, go left when x < split value,
  default direction on missing).
- Source: notebook `src/3.1.1_ML_model_performance_test.ipynb` (sha256 b6226ca7...599ad) cell 36 output:
  "Ba: RMSE=1.00 ... Count=1065; Bw: RMSE=0.59 ... Count=999; Bs: RMSE=0.70 ... Count=1028" (period 1960-2021 = all test rows).
- Caveat recorded before running: the notebook loads the pickled GridSearchCV best estimator
  (`custom_loss_cv_grid.pkl`, not fetched, 4.3 MB); the JSON is assumed to be the same booster. If it is not, the
  reproduction misses.
- Expected: 1.00 / 0.59 / 0.70 at 2 decimals; tolerance 0.01 per season (p3 wording). Counts must match exactly.
  The first run reproduced 0.9962 / 0.5881 / 0.7001; this run must give the same four decimals.
- A miss makes the comparison unresolved: no improvement is claimed against it.

## Part A. Provenance repair of the two PROMISING claims (frozen)

- `code/` holds every program, flat, all reading data from `../data/` (the three shipped files above, sha256-checked
  on load). The programs are the first run's, with only import-path lines, output-path arguments and write targets
  changed (the full diff is saved in attempts/refreeze/code_diff.txt). Every program writes only to paths named on
  its command line. The claim packages ship byte-identical copies of `code/` and `data/`.
- BL1 is re-frozen with `code/freeze_score.py freeze` using exactly the first run's config (kind blend, cfg
  {"lr": 0.05, "colsample": 1, "n_max": 500, "seed": 0, "fs": "F2", "depth": 3, "lam": 20, "min_child": 0,
  "subsample": 1}, n_trees 200, w_gbm Ba 0.25 / Bw 0.30 / Bs 0.20). LW1 is re-frozen with `code/freeze_linear.py
  freeze` using phis one, solid, solid_dz. The frozen files record sha256 of exactly the shipped code files.
- Pass conditions, all required, else the repair fails and that claim is withdrawn (status NOTHING):
  BL1's train_fit equals the first run's frozen train_fit to 1e-12; LW1's coefficients equal the first run's exactly;
  the re-scored test monthly predictions are bitwise equal to the first run's saved arrays
  (attempts/ensemble/BL1_test_monthly_pred.npy; LW1's 999 winter predictions recomputed from its frozen coefficients);
  the first run's OOF file and weight choice are regenerated by the shipped `code/oof.py` and `code/analyze.py`
  (best plain stage 200, w_gbm 0.25 / 0.30 / 0.20, arrays equal to attempts/ensemble/oof_F2d3.npz).
- The two re-scorings are of models already scored in the first run. They are logged in this run's ledger marked
  "re-score", add no selection, and do not count toward the cap below.

## Part B. Deviations and test-informed choices, stated plainly

1. PREREG deviation (first run): LW1's predictor set (and each season set of LIN1) was chosen by that season's own
   pooled CV RMSE, while the first PREREG named "mean over the three seasons" as the CV score. A winter-only model
   has no annual or summer score, so the mean is undefined for it; no PREREG.v2 was written at the time.
2. Order of events for LW1 (file modification times only, run machine clock, UTC): first PREREG 14:38:21Z;
   subset search output (top line = LW1's set, CV 0.6984) 14:42:23Z; frozen_LW1.json 14:42:40Z; LW1 test score
   14:42:47Z. The lens NOTES.md (14:46:47Z), BRIEF.md and scout.md (14:45:46Z) were written after LW1 was scored.
   There is no external timestamp; these times are corroborative only.
3. Test-informed lens design (first run): the ensemble lens (BL1) was designed after that run had seen the test scores
   of MBM, LW1 and LIN1. Its rules (14:51:36Z) were fixed before its OOF run and before GBM1 was scored; its weights
   come only from CV.
4. Carrier choice (first run): GBM1 and BL1 both meet p1 at 2 decimals; BL1 was named the p1 carrier after both were
   scored, because it is also lower unrounded.
5. Test-informed leads (this run): leads 1 and 2 below were proposed after the first run saw six test scores (it
   noted that pooled CV ranks linear above GBM while test ranks GBM above linear on Ba and Bs). Their rules are fixed
   here before any of their CV or test output exists, but the choice of these two leads is informed by test results.
   Any claim from them carries this disclosure, and the total count of test scorings (first run 6, this run's new
   ones) is reported with it.

## Part C. Live leads (frozen before any of their output exists)

Cap: at most 2 new models scored on test in this run (your human's weekend cap), one per lead. Every scored model is
reported. Each lead's model is that lead's CV primary, named in its folder before its test scoring.

**Lead 1, glacier-balanced blend weights (model BL2).** Components exactly BL1's: the plain GBM OOF stage of 200 trees
and the season-wise linear model, from the regenerated OOF file. Statistic for season s: balanced RMSE =
sqrt(mean over training glaciers g with at least one point of season s of MSE_(g,s)), from the OOF predictions. Per
season, w_gbm in 0, 0.05, ..., 1.00 minimising the balanced RMSE (ties: the smaller w). BL2 = BL1's components with
these weights. If all three weights equal BL1's, BL2 is BL1 and no test scoring is spent.

**Lead 2, monotone-constrained GBM (model MB1).** Feature set F2 (17 features). Constraint vector M1, fixed now on
physical grounds: +1 for tp and solid_tp (more precipitation or snowfall cannot lower balance); -1 for t2m, t_stake,
pdd_stake and abs_sw (warmer or more absorbed shortwave cannot raise balance); 0 for the other 11 features. Grid:
depth 2, 3, 4 x lambda 5, 20; lr 0.05, n_max 500, min_child 0, subsample 1, colsample 1, seed 0 (6 configs).
Selection: the first PREREG's CV score (mean over the three seasons of pooled OOF RMSE), best 50-tree stage; ties: the
first config in this order. Then `code/oof.py` on the chosen config and `code/analyze.py` (BL1's rule: best plain stage
by mean pooled OOF RMSE, per-season w_gbm by pooled OOF RMSE). MB1 = blend of the monotone GBM at that stage and the
season-wise linear model with those weights (the only changes from BL1 are the constraint and its re-tuned config).

Claims: a scored lead model meeting the main criterion (or p1) is a claim only under the rules above; it then goes to a
fresh three-skeptic panel. A lead model that ties or loses is reported with its numbers and the lead gets a verdict.

## Null test

null_test: not needed because each claim is an explicit frozen model scored once by a deterministic RMSE scorer against fixed table values set by the bank criterion; no search is run on test data. Supplementary (not gating): a glacier-block bootstrap (2000 resamples of the 14 test glaciers, seed 0) of RMSE(model) - RMSE(MBM) per season is reported for any claimed model.
