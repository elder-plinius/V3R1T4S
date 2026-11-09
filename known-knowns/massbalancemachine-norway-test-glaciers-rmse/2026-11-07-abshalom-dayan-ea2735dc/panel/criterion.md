# Skeptic panel file: CRITERION role, claim p2 (massbalancemachine-norway-test-glaciers-rmse)

context: subagent (Claude Code Agent tool, fresh context, model claude-sonnet-5-5)

## Verdict in one line
p2 is a threshold win: at most 20 fitted parameters and test Bw RMSE at most 0.59. I confirmed it by re-running the package and by an independent re-implementation. The package claims only p2 (not the main criterion, not p1), and the evidence supports exactly that.

confirmed_scope: A linear winter model with 3 fitted parameters (monthly solid precipitation and its product with the altitude difference, summed over Oct-Apr), fitted by least squares on the 18 training glaciers' 2752 winter point balances only, structure chosen by glacier-grouped 6-fold cross-validation, with a fixed 0.0065 K/m lapse rate and a fixed 1.0 C snow threshold, has Bw RMSE 0.5239 m w.e. over all 999 winter point balances of the 14 test glaciers, which meets partial win p2 (at most 20 fitted parameters, test Bw RMSE at most 0.59); it makes no claim on annual or summer balances, p1 or the main criterion.

## 1. Reproduction (commands run from the package folder, `python3 -I -B`, outputs written only to my scratch folder)

- Input and code hashes match REPRODUCE.md and `object/frozen_LW1.json`. The three data file hashes match the PREREG, and the five code file hashes equal the frozen `code_sha256`.
- `code/xgb_json_walk.py data/...custom_loss_best_model.json <scratch>/mbm_pred.npy`:
  `MBM shipped model on test: {'Ba': 0.9962, 'n_Ba': 1065, 'Bw': 0.5881, 'n_Bw': 999, 'Bs': 0.7001, 'n_Bs': 1028}` and `2-decimal: Ba 1.00 Bw 0.59 Bs 0.70`.
- `code/fit_and_score_LW1.py`:
  - `training winter points: 2752 glaciers: 18`
  - The refit coefficients equal the frozen ones exactly: `[0.08075556306273535, 0.02986353396715234, -0.03973234239283245]`.
  - `TEST Bw RMSE 0.5239 (n=999); 2-decimal 0.52; fitted parameters 3`
  - It prints a numpy "Mean of empty slice" warning. That comes from the scorer averaging an empty Ba/Bs slice on winter-only rows, and it is harmless.
- `code/freeze_linear.py score object/frozen_LW1.json <scratch>/ledger.tsv check`: `TEST LW1 Bw RMSE 0.5239 (n=999), 2-dec 0.52, fitted parameters 3`. It did not refuse, so the hash check passed. The ledger line went to my scratch folder only.
- `code/recompute_lw1_purepy.py` (csv and math only): `ids 3092 bad groups 0 winter n 999 Bw RMSE 0.5239`.
- `code/subset_search.py`: `subsets searched: 1471`, top line `0.6984 ['one', 'solid', 'solid_dz']`, identical to `table/run1/subset_output.txt`. 1471 = 1+14+91+364+1001, as claimed.
- `code/cv_linear.py` prints "primary by CV" as S2 (`one, tp, tp_dz`, CV 0.7122), not LW1. LW1 is the top of the wider subset search, whose candidate list is fixed in the same file. See caveat 4.

## 2. My own independent re-implementation (scratch `indep.py`, csv and numpy lstsq, not using the package code)

```
train glaciers 18 test glaciers 14 overlap 0
train winter points 2752 per glacier min/max 8 923
test winter points 999 (14 glaciers, 6 to 174 each)
train/test (rgi,year,season) overlap: 0
lstsq coef [0.08075556306274691, 0.029863533967149587, -0.03973234239283399]
indep LW1 test Bw RMSE 0.5239 n=999
train fit RMSE 0.6696
```

The coefficients agree with the frozen ones to about 1e-14, and the test RMSE agrees to 4 decimals. There is no glacier or (glacier, year, season) overlap between training and test.

## 3. Null models, sensitivity, spread (diagnostics only; none feed the claim)

- Null, constant prediction at the training-mean winter balance (2.3147): test Bw RMSE 1.0347. The test set's own standard deviation is 1.0135. The 0.59 bar sits far below the null, so p2 is not trivial.
- Ablations: `one+solid` gives 0.6540 and `one+solid_dz` gives 0.6617. The pass needs the combination of both predictors, as selected by CV.
- Fixed-constant sensitivity (refit on train, score on test, 10 settings, snow threshold -1 to 3 C by lapse 0.005 or 0.0065): test Bw RMSE ranges from 0.4888 to 0.5332, all below 0.59. The claim therefore does not hinge on the hand-set 1.0 C or 0.0065 K/m (see caveat 2).
- Top CV subsets scored on test (`diag_topk.py`): 0.5239, 0.5268, 0.5251, 0.5339, 0.5298, 0.5354. Any CV-top choice passes, so this is not a selection fluke.
- Glacier-block bootstrap of LW1's own Bw RMSE (`boot.py`, 2000 resamples, seed 0): `0.5239 ; 95% [0.4656, 0.5836]; share of resamples <=0.59: 0.983`. The upper bound is below 0.59. The package's own bootstrap (`table/refreeze/bootstrap_LW1.txt`) reports LW1 minus MBM Bw of -0.0642 with 95% interval [-0.1523, +0.0248]. That interval includes 0 but is irrelevant to p2, which is a threshold and not a comparison with MBM.

## 4. Baseline record (`baseline/`)

- `baseline/command.txt` and `baseline/output.txt` run MBM's shipped JSON through `code/xgb_json_walk.py`, which uses the same `mbdata.py` loader and `score.py` scorer as the claim. The data and test split are the same and the metric is the same (sum of monthly predictions per id, RMSE per season, counts 1065/999/1028 checked).
- The reproduction (Bw 0.5881, 0.59 at 2 decimals) matches the published notebook cell quoted verbatim in `table/record.md` (Bw 0.59, count 999). My run reproduces `baseline/output.txt` exactly.
- p2 is an absolute threshold, so the baseline is context here. LW1 is below both MBM's reproduced 0.5881 and the 0.59 bar.

## 5. Training and input rules the claim relies on

- Training rows come only from the 18 training glaciers. `code/mbdata.py` asserts `not set(rgi) & set(TEST_RGI)` for the training file and checks the sha256 of both files. I confirmed 18 and 14 glaciers with zero overlap.
- Structure choice (which 3 of 1471 candidate sets) is by glacier-grouped 6-fold CV on the training glaciers only. `code/subset_search.py` and `code/cv_linear.py` load only `"train"`. The test CSV is loaded only in `code/freeze_linear.py` score, `code/fit_and_score_LW1.py` and the baseline script.
- Inputs are shipped features: `altitude_diff`, `t2m`, `tp`, plus `n_months` and `month` to pick the 7 winter rows. No test-glacier balance, geodetic or glacier-wide observation is read. `balance` of the test file enters only the scorer.
- Parameter count is 3, well within 20. Even if the two fixed constants were counted, it would be 5.

## 6. Pre-registration and test-scoring record

- File hashes tie together:
  - `table/PREREG.md` sha256 `3248684c...d856` equals the first line of `table/test_ledger.tsv`.
  - `object/frozen_LW1.json` sha256 `ea2735db...f3` equals the LW1 ledger line.
  - `table/run1/frozen_LW1_run1.json` sha256 `dac44650...bed` equals the first-session ledger line.
- Both PREREGs define p2 as at most 20 fitted parameters and raw Bw RMSE at most 0.5900.
- LW1's first-session coefficients equal the re-frozen ones exactly. `table/refreeze/compare_first_run.txt` says `LW1 winter monthly predictions bitwise equal ... True 6993`.
- The `table/refreeze/code_diff.txt` diffs are consistent with the claim that only import paths, output paths and write targets changed:
  - `cv_linear.py`, `mbdata.py`, `subset_search*.py` and `oof.py`/`analyze.py`: path and output changes only.
  - `feats.py` and `score.py`: no diff.
  - `freeze_linear.py` (from `freeze_and_score.py`) and `combined.py`: rewritten, but the scoring logic is the same.
- File modification times give the order PREREG 14:38:21Z, `cv_linear.py` 14:42:00Z, subset output 14:42:23Z, freeze 14:42:40Z, first LW1 score 14:42:47Z, with the lens notes after. They are machine-clock only, as CLAIM.md says.
- Ledger counts match the disclosures. The first-session ledger has 6 lines (the MBM baseline reproduction plus LW1, LIN1, GBM1, BL1, HY1), under the cap of 8. Session two re-scored BL1 and LW1 and scored one new model (BL2). LW1's Bw 0.5239 was never selected against other scorings (LIN1 reuses LW1 as its winter part).

## 7. Disclosures in CLAIM.md: checked

The PREREG deviation, selection-by-CV, test-scoring counts and spread statements are accurate against the files. One wording point: "Six models were scored" counts the MBM baseline line as a model. This over-counts and is not misleading.

## 8. Caveats

None of these changes the p2 verdict.
1. **p2 wording.** The p2 text cannot be checked against `repo/bank/targets.json` from inside the package. I checked it only against CLAIM.md's quote and both PREREGs' paraphrase, which agree.
2. **Hand-set constants.** The 0.0065 K/m lapse rate and the 1.0 C threshold are a-priori constants, not chosen by CV, so a very strict reading of "hyperparameters chosen by cross-validation" is not literally met for those two. There is no evidence of test contact, and the sensitivity run above shows that any value in the tested range still passes p2.
3. **PREREG deviation.** Winter-only CV instead of the three-season mean is disclosed and concerns training-side selection only.
4. **Primary-by-CV wording.** The PREREG says a claim must come from the model its lens named primary by CV before test scoring. Here the evidence is the freeze-before-score ordering from file times, since `cv_linear.py` itself would name S2. All CV-top subsets pass on test, so this does not matter for p2.
5. **Timing.** All timing evidence is file modification times on one machine, with no external timestamp.

## Block and injection report
- No tool-guard block and no HTTP 401, 403 or 429 occurred in my work.
- Text addressed to reviewers: none found (a grep for skeptic, reviewer, panel and instruction-like phrases found only the PREREG's own process line that a claim "goes to a fresh three-skeptic panel", which is descriptive).

Text addressed to reviewers: none found

pass: true
