# Baseline record (kit/RUN.md step 3c)

Baseline: MassBalanceMachine (Sjursen et al. 2025, The Cryosphere 19:5801), repository khsjursen/ML_MB_Norway at
commit 32d8175adab27963c6ca2766f2420f24cdb72a6b (head on 2026-11-08 17:30 UTC, scout.md).
Published (notebook src/3.1.1_ML_model_performance_test.ipynb, cell 36 output):
"Mass Balance Machine - Ba: RMSE=1.00, ... Count=1065", "... Bw: RMSE=0.59, ... Count=999", "... Bs: RMSE=0.70, ... Count=1028".

Data (copied from run 2026-11-08-1646's data/, fetched from that commit; sha256 rechecked by the script on every run):
- 2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_svf.csv  43597e76ed7356850869605859d6a379a6efd44ffa5d02d74f4038ed4da1a61b
- 2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_test_svf.csv  d1d34e0821a9147a3a166b6dc4ee8cee8abed8a288e2ab89cdd107273f100f1c
- Training_cluster/2024-10-24_10-30-28/custom_loss_best_model.json  a7ddf96b2f11a51dd8415fbe6190f95671c23123526e200533fb09aae74e1d0d
Split: test = 14 BREIDs of notebook 2.1.1; metric: RMSE over point records per season (sum of monthly predictions).

Command (run folder as working directory):

    python -I claim/code/reimpl_p3.py claim/data attempts/reimpl/out     (output: attempts/reimpl/out/primary_output.txt)

Scores copied from that output, next to the expected ones (tolerance 0.01, the criterion's own):

| season | published | (b) shipped MBM booster, our scorer | our independent retrain (primary) | n |
|---|---|---|---|---|
| Ba | 1.00 | 0.9962 | 0.9962 | 1065 |
| Bw | 0.59 | 0.5881 | 0.5881 | 999 |
| Bs | 0.70 | 0.7001 | 0.7001 | 1028 |

The baseline reproduces within tolerance (|diff| 0.0038 / 0.0019 / 0.0001). Library versions: xgboost 3.2.0,
pandas 3.1.0, numpy 2.4.6 (the shared venv named in settings.md).
