# REPRODUCE skeptic report: claim p2 (LW1, 3-parameter linear winter model)

context: subagent (Claude Code Agent tool, fresh context, model claude-sonnet-5-5)

Everything below was run with `python3 -I -B` (Python 3.14.7, numpy 2.5.3). All outputs went to my scratch folder. The package folder was only read, and it still has 44 files with no `__pycache__`.

## 1. Data hashes
`shasum -a 256 data/*.csv data/*.json` gave the three hashes quoted in REPRODUCE.md, exactly:
- training CSV `19e10b01...9e94`
- test CSV `d1d34e08...0f1c`
- MBM JSON `a7ddf96b...1d0d`

## 2. My own checker, written from the CLAIM.md definition before I read any package code
I wrote a plain-csv loader and an aggregator by `id`. Counts per test file, from the `n_months` column:

| Season | Months | Test points |
|---|---|---|
| Annual | 12 | 1065 |
| Winter | 7 | 999 |
| Summer | 5 | 1028 |

In the training file, 2752 ids are winter points. Training has 18 glaciers and test has 14.

I built the model from the stated specification. The model is f = b0 + b1*solid + b2*solid*dz/1000, with t = t2m - 273.15 + 0.0065*dz, tp*1000, and solid = tp_mm if t < 1.0 else 0, summed over the 7 winter rows. I fitted it by `numpy.linalg.lstsq` on the 2752 training winter points. Output (`mine.py`):
```
train winter pts 2752 test winter pts 999
train glaciers 18 test glaciers 14 overlap set()
coef [0.08075556306274691, 0.029863533967149587, -0.03973234239283399] rank 3
frozen coef [0.08075556306273535, 0.02986353396715234, -0.03973234239283245]
max |coef diff| 1.1560197243909442e-14
TEST Bw RMSE 0.5239109960722116 n 999
TEST Bw RMSE with frozen coef 0.5239109960722138
rounded 2dec 0.52
constant-mean baseline 1.0346664438613447
```
My refit matches the frozen coefficients to 1.2e-14. The claimed RMSE 0.5239 (0.52) and n = 999 are reproduced. The package's own scorer, run with the frozen coefficients, gives 0.5239109960722138, the same digits as mine with the frozen coefficients.

## 3. Frozen object code hashes
`shasum -a 256 code/mbdata.py code/score.py code/feats.py code/cv_linear.py code/freeze_linear.py` equals the `code_sha256` block in `object/frozen_LW1.json`, entry by entry:
- `mbdata.py` `d3b98736...40bf`
- `score.py` `5c4a3a61...228a`
- `feats.py` `60696fb2...1634`
- `cv_linear.py` `959367dc...63c`
- `freeze_linear.py` `88407307...b96`

Negative test: I copied `code/` to scratch, appended one line to `feats.py`, and ran `freeze_linear.py score`. It stopped with `AssertionError: code changed since freeze` and wrote no ledger.

## 4. REPRODUCE.md steps
- **Step 1 (baseline):** `Ba 0.9962 (n 1065), Bw 0.5881 (n 999), Bs 0.7001 (n 1028)`, which gives 1.00 / 0.59 / 0.70 at 2 decimals.
- **Baseline cross-check:** my own pure-Python tree walk (`mine_baseline.py`, written separately from `code/xgb_json_walk.py`) gives Ba 0.996243, Bw 0.588143, Bs 0.700051 with n = 1065 / 999 / 1028.
- **Step 2 (refit and score), run twice:** both runs give `refit coef` equal to the `frozen coef`, and `TEST Bw RMSE 0.5239 (n=999); 2-decimal 0.52; fitted parameters 3`. The two output files are byte-identical (`cmp`).
- **Step 3 (`freeze_linear.py score`), run twice:** both give `TEST LW1 Bw RMSE 0.5239 (n=999), 2-dec 0.52, fitted parameters 3`. The ledger sha is `ea2735dc...cff3`, which equals the sha of `object/frozen_LW1.json` and the LW1 row in `table/test_ledger.tsv`.
- **Step 4 (pure-Python scorer):** `ids 3092 bad groups 0 winter n 999 Bw RMSE 0.5239`.
- **Step 5 (subset search), run twice:** `subsets searched: 1471`, top line `0.6984 ['one', 'solid', 'solid_dz']`. The two runs are byte-identical, and the output is identical to `table/run1/subset_output.txt` (`diff` empty).
- **Independent subset search:** I wrote my own search (`mine_search.py`, my own loader, my own predictors and my own fold assignment from the stated greedy rule). It also finds 1471 subsets, and its top 15 lines are identical to the package's top 15 (`diff` empty). The count matches 1+14+91+364+1001 = 1471.
- **Bootstrap:** rerunning `code/bootstrap.py` on the LW1 and MBM predictions gives `diff -0.0642  95% [-0.1523, +0.0248]`. This matches `table/refreeze/bootstrap_LW1.txt`.

The p2 bar is at most 20 fitted parameters and Bw at most 0.59. LW1 has 3 fitted parameters and Bw 0.5239. If the fixed lapse rate and the fixed 1.0 degree threshold were also counted as parameters, the total would be 5, still at most 20.

## 5. No test-glacier observation enters training
- RGIID and BREID overlap between the training and test files is empty (18 vs 14 glaciers). `mbdata.load` also asserts this at load time.
- Point-level overlap on (balance, year, altitude_diff, n_months) is 0, so no stake record is duplicated across the files.
- A grep of `cv_linear.py`, `feats.py` and `subset_search.py` finds no test load. In `fit_and_score_LW1.py` and `freeze_linear.py`, the test file is loaded only after the fit.
- An audit-hook trace of `fit_and_score_LW1.py` shows the order: training CSV opened, `refit coef` printed, then the test CSV opened.
- I ran `fit_and_score_LW1.py` with only a symlink to the training CSV present. It printed the refit coefficients, bit-equal to the frozen ones, and only then failed with `FileNotFoundError` on the missing test file. So the fit does not depend on the test file.

## 6. Provenance statements checked against `table/`
- Verified: the sha256 of `table/PREREG.md` is `3248684c...d856`, equal to the first line of `table/test_ledger.tsv`. The PREREG file is read-only.
- Verified: the sha256 of `table/run1/frozen_LW1_run1.json` (`dac44650...`) equals the run-1 ledger row. Its coefficients are exactly equal to `object/frozen_LW1.json`. Its `score.py` hash is identical to the shipped one, and its `cv_linear.py` and `mbdata.py` hashes differ, as the CLAIM describes.
- Verified: every time quoted under "Order of events" matches `table/run1/provenance_mtimes_linear.txt` (14:38:21Z, 14:42:00Z, 14:42:23Z, 14:42:40Z, 14:42:47Z, 14:43:55Z, 14:45:46Z, 14:46:47Z). The "PREREG written 14:37:53Z" quote is the file's own text. In `table/provenance_mtimes_run2.txt`, the reruns (17:46:33Z onward) come after the seal (17:46:19Z).
- Verified: `table/test_ledger_run1.tsv` has six rows (the MBM baseline plus LW1, LIN1, GBM1, BL1, HY1). LW1 Bw is 0.5239 and LIN1 Bw is also 0.5239, so LW1 is its winter part, as disclosed. `table/test_ledger.tsv` has the PREREG line, BL1 and LW1 re-scores, and BL2 at 0.9073 / 0.5146 / 0.6728, labelled "NEW model 1 of 2 (cap)". That agrees with "at most one more may follow".
- Verified: `table/status_ML_MB_Norway.html` has sha `30dafd86...c8c4`, `commitCount` "403", and the README text pointing to ODINN-SciML/MassBalanceMachine.
- Verified: the notebook RMSEs quoted in `table/record.md` (1.00 / 0.59 / 0.70, counts 1065 / 999 / 1028) agree with my baseline rounded to 2 decimals.

## 7. Findings that do not break the claim
1. **Diff description overstated.** CLAIM.md says "Only import-path lines, output-path arguments and write targets changed". In `table/refreeze/code_diff.txt`, `mbdata.py` (one `RAW` path line), `cv_linear.py` (one `sys.path` line), `subset_search.py` and `score.py` and `feats.py` do match that description. `freeze_linear.py` was restructured: a freeze/score mode interface, a bigger hash set, and a ledger path argument. `combined.py` also lost its freeze/score modes. The LW1 prediction and scoring lines are unchanged in effect, and the coefficients are equal exactly.
2. **Not re-verifiable from the package.** `table/refreeze/compare_first_run.txt` says the first-run and re-frozen winter predictions are bitwise equal, but the first-run arrays are not shipped. Exactly equal coefficients, an identical `score.py` hash and the unchanged diff lines support it. The mtimes are labelled corroborative only, and the literature search in `table/record.md` is not reproducible offline. None of these affect p2, which is a threshold on Bw.
3. **Benign warnings.** `RuntimeWarning: Mean of empty slice` appears in steps 2 and 3. The winter-only call computes empty Ba and Bs groups, which become NaN and are not used.
4. **Bit-exact refit is machine-dependent.** The bit-for-bit refit assertion passed here, but it may be fragile across BLAS builds. My independent `lstsq` agrees to 1.2e-14.
5. **Shared weather cells.** Three test/training glacier pairs share identical ERA5 climate rows. These are weather inputs, not mass-balance observations, and the point-level overlap is 0. This is a property of the shipped data, not of the model.
6. **Wording.** "Six models were scored" counts the MBM baseline row. That is five trained models plus the baseline.
7. **PREREG deviation.** The CV score used was winter-only rather than the mean over seasons. The CLAIM discloses this, and I confirmed it is consistent with the first PREREG text.

I found no mismatch, missing object or non-determinism. No blocks, HTTP errors or tool-guard events occurred.

Text addressed to reviewers: none found

pass: true
