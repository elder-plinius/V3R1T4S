# Reproduce (Python 3 with numpy only; run from this folder; `-B` stops __pycache__; no command writes into this folder)

Set `S` to an empty scratch folder outside this package first, e.g. `S=$(mktemp -d)`.

```sh
shasum -a 256 data/*.csv data/*.json
# 19e10b018db4e291f4e9e99dcc908ca08a82ef25817b633a3b809b3b30200e94  ..._climate_svf_monthly.csv  (training, 18 glaciers)
# d1d34e0821a9147a3a166b6dc4ee8cee8abed8a288e2ab89cdd107273f100f1c  ..._climate_test_svf.csv     (test, 14 glaciers)
# a7ddf96b2f11a51dd8415fbe6190f95671c23123526e200533fb09aae74e1d0d  ..._custom_loss_best_model.json (MBM)

# 0. The frozen object's code hashes equal the shipped code
shasum -a 256 code/mbdata.py code/score.py code/feats.py code/cv_linear.py code/freeze_linear.py
python3 -I -c "import json; print(json.dumps(json.load(open('object/frozen_LW1.json'))['code_sha256'], indent=1))"

# 1. Baseline: MBM's shipped model on the test set (seconds)
python3 -I -B code/xgb_json_walk.py data/src_Training_cluster_2024-10-24_10-30-28_custom_loss_best_model.json $S/mbm_pred.npy
# expected: Ba 0.9962 (n 1065), Bw 0.5881 (n 999), Bs 0.7001 (n 1028); 2-decimal 1.00 / 0.59 / 0.70

# 2. The claim: refit LW1 on training winter points, check coefficients equal the frozen ones, score the test set
python3 -I -B code/fit_and_score_LW1.py
# expected: TEST Bw RMSE 0.5239 (n=999); 2-decimal 0.52; fitted parameters 3

# 3. The same through the hash-checked freeze/score program (refuses if any code file differs from the frozen hashes)
python3 -I -B code/freeze_linear.py score object/frozen_LW1.json $S/ledger.tsv "check"

# 4. Independent pure-Python scorer (csv + math only)
python3 -I code/recompute_lw1_purepy.py data/src_Data_2023-08-28_stake_mb_norway_cleaned_ids_latlon_wattributes_climate_test_svf.csv object/frozen_LW1.json
# expected: ids 3092 bad groups 0 winter n 999 Bw RMSE 0.5239

# 5. How the predictors were chosen (training data only, about 5 s)
python3 -I -B code/subset_search.py
# expected: subsets searched: 1471; top line 0.6984 ['one', 'solid', 'solid_dz'] (as table/run1/subset_output.txt)
```

Data sources (fetched 2026-11-07T14:35:43Z, HTTP 200): https://raw.githubusercontent.com/khsjursen/ML_MB_Norway/main/src/Data/<file>
and .../src/Training_cluster/2024-10-24_10-30-28/custom_loss_best_model.json (MIT license; stake data NVE, doi:10.58059/sjse-6w92).
The `src_` file-name prefix is ours (the repository path with "/" replaced by "_").
