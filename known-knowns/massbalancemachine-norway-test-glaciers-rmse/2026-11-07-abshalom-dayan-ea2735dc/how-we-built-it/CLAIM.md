# Claim

**One sentence:** A 3-parameter linear winter model (monthly solid precipitation and its product with the
climate-cell-minus-stake altitude difference, summed over October-April), fitted by least squares on the 18 training
glaciers' winter point balances only, predicts all 999 winter point balances of the 14 withheld test glaciers with
RMSE 0.5239 m w.e. (2-decimal 0.52).

- Target id: `massbalancemachine-norway-test-glaciers-rmse`
- Claimed: partial win **p2** only. Not claimed: the main criterion and p1 (this model predicts winter balances only).
- Status source: https://github.com/khsjursen/ML_MB_Norway (record in `table/record.md`).

## Partial win p2 (verbatim, repo/bank/targets.json)

"A model of at most 20 fitted parameters (e.g. a calibrated temperature-index or linear model) with test Bw RMSE at
most 0.59 m w.e."

## Main success criterion (verbatim, for context)

"A saved, runnable model (code, fixed seeds) trained only on rows from the 18 training glaciers in the shipped CSVs
(hyperparameters chosen by cross-validation within those glaciers only). Inputs are only the shipped features or other
public static data (DEM, RGI outlines), never any mass-balance, geodetic or glacier-wide observation of a test glacier.
It predicts every test-glacier point balance, and its RMSE against the observed values over the same 1065 annual, 999
winter and 1028 summer measurements must be strictly lower (direction: min), at 2-decimal rounding, than MBM's for all
three: Ba <= 0.99, Bw <= 0.58 and Bs <= 0.69 m w.e. The RMSE is computed by an independent script and checked against
MBM's numbers reproduced from the repository notebook. The result must also beat any RMSE on these same full test sets,
by a model that uses no observation of a test glacier, in a paper from the last 24 months found by a fresh search.
Numbers from models calibrated on test-glacier geodetic data (e.g. the paper's GloGEM 0.91 and OGGM 0.93 annual RMSE
for 1980-2019) and numbers on sub-periods do not set the bar."

## The object

`object/frozen_LW1.json`: phis ["one", "solid", "solid_dz"], coefficients
[0.08075556306273535, 0.02986353396715234, -0.03973234239283245], 3 fitted parameters.

Model per monthly row: f = b0 + b1*solid + b2*solid*dz/1000, with dz = altitude_diff (m), t = t2m - 273.15 +
0.0065*dz (deg C), tp_mm = tp*1000, solid = tp_mm if t < 1.0 else 0. A point's winter prediction is the sum of f over
its 7 monthly rows (Oct-Apr). The lapse rate 0.0065 K/m and the 1.0 deg C threshold are fixed constants, not fitted.
How the 3 predictors were chosen: by glacier-grouped 6-fold cross-validation on the training glaciers only, the lowest
CV RMSE among 1471 subsets ("one" plus up to 4 of 14 candidate predictors), code `code/subset_search.py`. The
frozen file records the sha256 of the five code files the model uses; they are shipped in `code/` byte for byte, and
`code/freeze_linear.py score` refuses to run if any differs.

## Provenance (two work sessions on 2026-11-07, both on the same machine)
- First session (14:34-15:27Z): PREREG (`table/run1/PREREG.md`, written 14:37:53Z), the CV, the freeze and the one
  test scoring of LW1 (14:42:47Z). Its frozen file `table/run1/frozen_LW1_run1.json` recorded hashes of that session's
  code, which lived in other folders.
- Second session (from 17:39Z): the same programs were moved into one flat `code/` folder. Only import-path lines,
  output-path arguments and write targets changed; the full diff is `table/refreeze/code_diff.txt`. A new PREREG
  (`table/PREREG.md`, sealed 17:46:19Z; its sha256 is the first line of `table/test_ledger.tsv`) fixed the repair's
  pass conditions before anything was rerun. LW1 was re-frozen with the shipped code's hashes: its coefficients equal
  the first frozen file's exactly, and its 999 winter predictions are bitwise equal (`table/refreeze/compare_first_run.txt`).

## Order of events for LW1 (file modification times, machine clock, UTC; corroborative only, no external timestamp)
- 14:38:21Z first PREREG; 14:42:00Z `cv_linear.py` (predictors, fixed lapse rate and threshold); 14:42:23Z output of
  the subset search (`table/run1/subset_output.txt`; its top line is LW1's set, CV 0.6984); 14:42:40Z
  `frozen_LW1.json`; 14:42:47Z LW1 test score; 14:43:55Z LIN1 test score. All of the first session's linear-lens file
  times are in `table/run1/provenance_mtimes_linear.txt`.
- The lens NOTES.md (14:46:47Z), BRIEF.md and scout.md (14:45:46Z) were written after LW1 was scored.

## Disclosures
- **PREREG deviation.** The first PREREG named "mean over the three seasons of the pooled OOF RMSE" as the CV score.
  LW1's predictor set was chosen by winter-only pooled CV RMSE. A winter-only model has no annual or summer score, so
  the mean is undefined for it; no PREREG.v2 was written at the time.
- **Selection by CV, not by test.** LW1 was the first linear model scored on test; the only other linear model scored
  (LIN1, 14:43:55Z) has LW1 as its winter part, so the winter number 0.5239 was seen once.
- **Test scorings.** Six models were scored on test in the first session (all listed in `table/run1/test_ledger_run1.tsv`);
  this session re-scored LW1 (same model) and scored one new all-season model (BL2, 0.9073 / 0.5146 / 0.6728, whose
  winter part is not LW1) before this package was built; at most one more may follow (`table/test_ledger.tsv`).
- **Spread.** Glacier-block bootstrap (`code/bootstrap.py`, `table/refreeze/bootstrap_LW1.txt`): LW1 minus MBM Bw
  -0.0642 (95% -0.152 to +0.025). p2 is a threshold criterion (Bw at most 0.59), not a comparison with MBM.

## Files
- `code/`: the flat program folder (byte-identical to the work folder's): mbdata.py (loader, input sha256 checks,
  asserts no test glacier in the training file), score.py (scorer), cv_linear.py (predictors and design), feats.py
  (imported helper), subset_search.py (CV selection), freeze_linear.py (freeze and score), fit_and_score_LW1.py (refit
  and test score), recompute_lw1_purepy.py (independent pure-Python test scorer), bootstrap.py, xgb_json_walk.py
  (MBM baseline), and the scripts of the all-season models (not used by LW1).
- `data/`: the two shipped CSVs, exactly as fetched, and MBM's shipped model JSON (for the baseline).
- `object/frozen_LW1.json`; `baseline/`: MBM reproduction command and output.
- `table/`: status page and record, PREREGs, ledgers, provenance records.
- `REPRODUCE.md`: commands.
