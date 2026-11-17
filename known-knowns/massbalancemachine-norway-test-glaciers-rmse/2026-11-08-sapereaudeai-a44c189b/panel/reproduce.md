# REPRODUCE skeptic report: massbalancemachine-norway-test-glaciers-rmse, partial win p3

context: subagent (Claude Code Agent tool, fresh context)

## Definition I checked against (quoted)

Criterion (bank partial win p3, quoted in CLAIM.md and PREREG.md): "Reproduce MBM's three test RMSEs within 0.01 m w.e.
from the shipped CSVs with an independent re-implementation (validates the split and scorer)."

Pass rule (PREREG.md): "for each of Ba, Bw, Bs: |RMSE_ours - published| <= 0.01, where published is the printed value
above (1.00, 0.59, 0.70), AND the record counts equal 1065 / 999 / 1028 exactly. All three must pass."

Published values, which I read myself from data/3.1.1_ML_model_performance_test.ipynb (loaded as JSON), cell 36 output:
"Mass Balance Machine - Ba: RMSE=1.00, MSE=0.99, MAE=0.77, Bias=-0.01, R²=0.64, Count=1065",
"Mass Balance Machine - Bw: RMSE=0.59, MSE=0.35, MAE=0.46, Bias=-0.01, R²=0.66, Count=999",
"Mass Balance Machine - Bs: RMSE=0.70, MSE=0.49, MAE=0.54, Bias=0.04, R²=0.72, Count=1028".
The cell computes them as `root_mean_squared_error(observed, modeled)` over the per-record rows of each Type. Cell 29
filters to years 1960-2021 and cell 30 drops NaN rows. Each record's prediction is the sum of its monthly predictions
(cells 15-17 and 22-27).

The pieces of the definition I took from the notebooks myself, not from the author's code:
- Split (2.1.1 cell 4): "test_glaciers = [54, 703, 941, 1135, 1280, 2085, 2320, 2478, 2768, 2769, 3133, 3137, 3138, 3141]".
- Test cleaning rule (2.1.1 cell 5): "df_test_winter = df_test_winter[df_test_winter['balance_winter'] != 9.99]".
- Months (2.1.1 cell 9): summer may-sep, winter oct-apr, annual oct-sep.
- Features (2.1.1 cells 15 and 21): altitude_diff, aspect, slope, skyview_factor, t2m, sshf, slhf, ssrd, fal, str, tp,
  with altitude_diff = altitude_climate - altitude (it matches the printed -129.77 for the first record).
- Hyperparameters (2.1.1 cell 52 output): max_depth=5, learning_rate=0.05, n_estimators=300, gamma=0, min_child_weight=0.
- Base score: base_score 0.5, from the shipped booster JSON (written by xgboost 2.0.3, 11 features, 300 trees).
- Aggregated objective: loss 0.5*(sum of a record's monthly predictions - record balance)^2. The gradient is the
  record residual, broadcast to each of the record's months, and the hessian is 1.

## What I did

I wrote my own checker, claim/skeptic_reproduce/check.py, from the definitions above before opening
code/reimpl_p3.py. It builds the records from the shipped wide CSV, makes the BREID split, applies the 9.99 rule,
implements the objective, trains with xgboost.train, and scores with its own scorer. I ran everything with nthread 2
(tree_method hist, seed 0). My scripts share only the xgboost library and these hyperparameters with the author's code.
My monthly rows are ordered differently (record-major against the author's month-major) and I pass float64 input, so
the code paths are not the same.

1. sha256sum -c SHA256SUMS.txt: all 20 listed files OK, and no unlisted file is in the package.
2. My records:
   - wide CSV has 4171 rows: 18 train glaciers and 14 test glaciers, with 0 RGIIDs shared between train and test.
   - train records: annual 2845, winter 2752, summer 2901 (67909 monthly rows).
   - test records: annual 1065, winter 999, summer 1028 (24913 monthly rows); the 9.99 rule removes 1 test winter record.
   - test years run from 1965 to 2021, so the 1960-2021 filter removes nothing, and the inputs contain no NaN.
   - These counts equal the notebook 2.1.1 cell 4 output (2845/1065, 2752/1000 before the rule, 2901/1028).
3. My records against the shipped monthly test CSV:
   - targets agree element by element in id order;
   - the 24913 x 11 feature matrix equals mine (max |diff| 2.8e-14);
   - each record has its full set of months.
4. The shipped booster (data/custom_loss_best_model.json) on my records, scored by my scorer, gives Ba/Bw/Bs RMSE
   0.9962/0.5881/0.7001. The other published metrics match too: MSE 0.9925/0.3459/0.4901, MAE 0.7705/0.4635/0.5384,
   bias -0.0123/-0.0122/0.0361, R² 0.6351/0.6633/0.7193; each rounds to the cell-36 value. Fourteen per-record mb_ML
   values printed in notebook 3.1.1 also match to 6 decimals:
   - cell 23, winter first 5 (1.444547 ... 1.843004) and last 5 (2.120444 ... 1.541409);
   - cell 32, annual first 5 (-3.853414 ... -2.444545) and summer ids 1023-1026 (-3.808799, -4.611671, -3.424848,
     -5.268450). My value for the last one is -5.268451, a 1e-6 float32 rounding difference.
5. My own retrain:
   - My scorer gives annual 0.9962 (n=1065), winter 0.5881 (n=999), summer 0.7001 (n=1028). To ten decimals that is
     0.9962432215 / 0.5881431127 / 0.7000514446.
   - The per-record max |diff| against the shipped MBM booster is 1.8e-6.
6. The author's saved result/test_record_predictions_primary.csv (3092 rows, every test record, not a sample):
   - My scorer gives annual 0.9962 (n=1065), winter 0.5881 (n=999), summer 0.7001 (n=1028).
   - Its y equals my targets in order, and its yhat is within 1.9e-6 of my retrain's yhat.
7. Determinism:
   - My checker fit twice gives bit-identical predictions.
   - At nthread 1 my checker's output, record predictions and model JSON are identical to the nthread 2 run.
8. The author's command from REPRODUCE.md (`python -I -B code/reimpl_p3.py data <out>`), run twice:
   - I ran it with `--nthread 2` instead of the default 4, to stay within this machine's thread limit.
   - Both reruns give model_primary.json and test_record_predictions_primary.csv byte-identical to the saved result/
     files (same sha256).
   - result_primary.json is identical except for the nthread field.
   - Against result/primary_output.txt, the only line that differs (diff --strip-trailing-cr) is the config line,
     'nthread': 2 against 4. The output prints P3_PASS: yes, and its built-in checks (a)-(f) all report as in the saved
     output.
9. Deleted-input run in my own code (claim/skeptic_reproduce/deleted_input.py):
   - I removed every test-glacier row by BREID and by RGIID: 4171 rows became 3064.
   - Retraining on that input gives test predictions identical to my primary retrain (max |diff| 0.0) and RMSE
     0.9962/0.5881/0.7001.
10. Negative controls through my scorer:
    - a zero prediction gives 1.8804/2.3378/3.3397;
    - predictions shuffled within each season give 2.2508/1.4268/1.7497;
    - both fail the rule, so my scorer can reject a wrong answer.

## Numbers (copied from claim/skeptic_reproduce/check_output.txt)

| season | published | my retrain, my scorer | shipped booster, my scorer | author's saved predictions, my scorer | n (mine) | required n |
|---|---|---|---|---|---|---|
| Ba | 1.00 | 0.9962 | 0.9962 | 0.9962 | 1065 | 1065 |
| Bw | 0.59 | 0.5881 | 0.5881 | 0.5881 | 999 | 999 |
| Bs | 0.70 | 0.7001 | 0.7001 | 0.7001 | 1028 | 1028 |

The |RMSE - published| differences are 0.0038, 0.0019 and 0.0001, all within 0.01, and the counts are exact.

## Mismatches

None in content. Two notes on procedure:
- **Thread count:** I did not run the author's command at its default nthread 4, because this machine allows 2
  threads. The nthread 2 rerun reproduced the saved model and predictions byte for byte.
- **Literal diff:** the `diff` exactly as written in REPRODUCE.md reports differences on this Windows machine. After
  stripping carriage returns, the only remaining difference is the nthread value in the config line, which I changed
  myself.

Out of scope for this role, not checked: whether the 0.01 tolerance singles out MBM's configuration. lens2_output.txt
shows other grid points scoring nearby.

My files: claim/skeptic_reproduce/check.py, check_output.txt, check_output_nthread1.txt, deleted_input.py,
deleted_input_output.txt, rerun_output.txt, rerun2_output.txt, and the out1/, out_nt1/, rerun/ and rerun2/ folders.

pass: true
