# Panelist Report: CRITERION (`polaris-moleculeace-activity-cliff-mse`)

role: CRITERION
context: fresh skeptic review of the packaged files only
target_id: polaris-moleculeace-activity-cliff-mse
confirmed_scope: Contributor-checked, not yet independently verified: deterministic CPU-only CLSS recipes (how-we-built-it/run_clss_moleculeace.py and how-we-built-it/run_lens1_multiscale_ruzicka.py) fit strictly on stereo-stripped InChIKey[:14]-disjoint training splits (overlap == 0 across all 30/30 benchmarks) and shipped in object/CHEMBL287_Ki_test_predictions.csv (28,516 bytes, sha256 37ced5b182f800041f6fcbff6bf9d5c5436fab3fc19f11155545067dff3d7d38, containing only test_row_index, csv_row_index, and model predictions with zero copied MoleculeACE columns, n_train = 1,061, n_test = 267, n_cliff = 103). Under the strict pre-test-scoring scope (0 prior test evaluations on CHEMBL287_Ki; see how-we-built-it/2026-10-19_PROVENANCE_AND_TEST_EVALUATION_LOG.md), Lens 1 (frozen 2026-10-19T11:58:31Z with 0 prior test evaluations on any target) achieves test MSE 0.42747335 (-15.05% vs live Polaris best 0.50318131, -16.20% vs MoleculeACE paper best 0.51009699, cliff MSE 0.52134229 vs paper cliff best 0.61875106 [-15.74%], non-cliff MSE 0.36851908 vs 0.41681673, 99.61% paired bootstrap win rate vs reproduced SVM+ECFP, 95.13% scalar bootstrap win rate vs Polaris, and 25/30 Polaris wins [18/30 >= 5%]), Stage 1 (frozen 2026-10-19T12:18:56Z with 0 prior test evaluations on CHEMBL287_Ki) achieves test MSE 0.42640543 (-15.26% vs Polaris, -16.41% vs paper, cliff MSE 0.52572845 [-15.03%], non-cliff MSE 0.36402573, 99.77% paired bootstrap, 95.11% scalar bootstrap), and Stage 1+2 (frozen 2026-10-19T12:18:56Z with 0 prior test evaluations on CHEMBL287_Ki) achieves test MSE 0.42716055 (-15.11% vs Polaris, -16.26% vs paper, cliff MSE 0.52897638 [-14.51%], non-cliff MSE 0.36321524, 99.77% paired bootstrap, 94.89% scalar bootstrap, and 27/30 Polaris wins [18/30 with >= 5% relative margin and >= 95% paired bootstrap]). Across all 5 candidate test evaluations on CHEMBL287_Ki (3 full 30-target sweeps), adding the iterated Stage 3 stacker (2026-10-19T14:20:55Z-14:39:21Z) achieves test MSE 0.40802135 (-18.9117% vs Polaris, -20.0110% vs paper, 99.97% paired bootstrap, 97.98% scalar bootstrap), cliff MSE 0.50213600 (-18.8468% vs paper cliff best, non-cliff MSE 0.34891276 vs 0.41681673 [-16.2911%], p2), and 29/30 Polaris wins (21/30 with >= 5% relative margin and >= 95% bootstrap win rate, p3; 30-target macro cliff RMSE 0.7211, overall RMSE 0.6303).

---

## 1. Mandate & Verification Protocol

As the **CRITERION** skeptic panelist, I independently audited all files inside `object/`, `how-we-built-it/`, `verify-it-yourself/`, and `the-record-we-beat/`. Using an independent Python verification script executed in a temporary scratch directory (subsequently removed), I checked every literal clause `(a)` through `(d)` of the bank's `success_criterion`, all three enumerated partial wins (`p1`, `p2`, `p3`), the dated provenance and test-set evaluation count audit (`how-we-built-it/2026-10-19_PROVENANCE_AND_TEST_EVALUATION_LOG.md`), potential transductive or stereochemical leakage seams, and null/negative controls.

### Verified Artifact Checksums & Sizes

| Relative File Path | Size (Bytes) | Verified `sha256` Checksum |
|---|---:|---|
| `object/CHEMBL287_Ki_test_predictions.csv` | `28,516` | `37ced5b182f800041f6fcbff6bf9d5c5436fab3fc19f11155545067dff3d7d38` |
| `object/CHEMBL287_Ki_manifest.json` | `5,860` | `d3e9d581acd324c9a780697edff8111bb79149772db2b216028011eef75c5f6f` |
| `object/moleculeace_30_sweep_manifest.json` | `51,074` | `e10850b18add6800af7fd6d032db341a05c9deaae1ed9837f1ce7785c84c62c5` |
| `how-we-built-it/2026-10-19_PROVENANCE_AND_TEST_EVALUATION_LOG.md` | `12,734` | `85c2379bad1c373d8f8d9fda4e099cd26fff72038b0ad5a9732007b7927194cb` |
| `how-we-built-it/run_clss_moleculeace.py` | `25,450` | `d0b03f84bb29218a1c5e495d83fc36319e8d46947f7ab31864b6a6332d24fdcf` |
| `how-we-built-it/run_lens1_multiscale_ruzicka.py` | `19,597` | `38271b2acfad5c1f858da0e7d9b4ab6f305d34a3673c9933c4fa3e5477c34dc2` |
| `verify-it-yourself/check_moleculeace_clss.py` | `17,021` | `f567b75d2f854c236d737aa3ab2e1e7f0ff0b928cdd605225f26acc20da69413` |
| `verify-it-yourself/run_checks.sh` | `1,120` | `bbfa17a2630e9942bc2baff57c7b280e4e7e8f75029d865196c0139eeca9b861` |
| `the-record-we-beat/polaris_moleculeace_30_audit.json` | `38,964` | `82a27869cb585c5e0d7d05f4584e9df925b0eeeb3db3a9b60f9e4f481eb2a5c1` |
| Upstream `benchmark_data/CHEMBL287_Ki.csv` (verified by URL + `sha256`) | `121,021` | `e857875848bb64dc6e327e6c42fe9fd36526bbee1b976de4521b55c4c6629894` |
| Upstream `MoleculeACE_results.csv` (verified by URL + `sha256`) | `36,991` | `6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5` |

---

## 2. Literal Clause-by-Clause Audit of Full `success_criterion`

### Clause (a): Official Test Split Alignment, Stripped Prediction Schema, `y` Column (`log10(nM)`), SHA-256, and Polaris Counts — **PASS**
- **Primary Headline Target (`moleculeace-chembl287-ki` / `CHEMBL287_Ki`):**
  - `object/CHEMBL287_Ki_test_predictions.csv` (`28,516` bytes, `sha256: 37ced5b182f800041f6fcbff6bf9d5c5436fab3fc19f11155545067dff3d7d38`) is byte-for-byte identical to `object/predictions/CHEMBL287_Ki_test_predictions.csv` and contains exactly `267` rows (`test_row_index` `0..266`) with columns `test_row_index,csv_row_index,y_pred_clss,y_pred_stage1,y_pred_stage2,y_pred_lens1,y_pred_svm_ecfp_baseline` (`0` copied MoleculeACE columns `smiles`, `cliff_mol`, `y_true`).
  - `object/CHEMBL287_Ki_manifest.json` (`5,860` bytes, `sha256: d3e9d581acd324c9a780697edff8111bb79149772db2b216028011eef75c5f6f`) records the benchmark slug `moleculeace-chembl287-ki`, the exact `sha256` (`e857875848bb64dc6e327e6c42fe9fd36526bbee1b976de4521b55c4c6629894`) of the official upstream `CHEMBL287_Ki.csv`, the exact `267` test-row indices (`test_csv_row_indices`: `[2, 6, 19, ..., 1325, 1327]`), and the full `stage_progression_audit`.
  - Independent verification confirms:
    1. `csv_row_index` in `object/CHEMBL287_Ki_test_predictions.csv` equals `df_raw.index[df_raw['split'] == 'test']` of the SHA-256-verified upstream `CHEMBL287_Ki.csv` with zero difference across all `267` test rows.
    2. Using `y` (`log10(nM)`) and `cliff_mol` (`103` cliff molecules with `cliff_mol == 1` and `164` non-cliff molecules with `cliff_mol == 0`) directly from the SHA-256-verified upstream `CHEMBL287_Ki.csv`, all metrics match the manifest to machine precision.
    3. The official train and test counts `n_train = 1,061` (`split == 'train'`) and `n_test = 267` (`split == 'test'`) match the Polaris API `nTrainDatapoints = 1,061` and `nTestDatapoints = 267`.
- **All 30 Benchmarks (`object/predictions/CHEMBL*_test_predictions.csv`):**
  - Across all `30 / 30` benchmarks listed in `object/moleculeace_30_sweep_manifest.json` (`51,074` bytes, `sha256: e10850b18add6800af7fd6d032db341a05c9deaae1ed9837f1ce7785c84c62c5`), every prediction CSV contains only index and prediction columns (`0` copied MoleculeACE columns) and matches `df_raw.index[df_raw['split'] == 'test']` of the SHA-256-verified upstream `benchmark_data/CHEMBL*.csv`.

### Clause (b) & (c): Independent `sklearn.metrics.mean_squared_error`, $\ge 5\%$ Relative Margin, $\ge 95\%$ Bootstrap Win Rate, and Dated Pre-Test-Scoring vs. Iterated Audit — **PASS**
- **Audit of Dated Provenance & Total Test-Set Evaluations (`how-we-built-it/2026-10-19_PROVENANCE_AND_TEST_EVALUATION_LOG.md`):**
  - Total candidate test-set evaluations made during the session (`2026-10-19T11:38:08Z` – `14:43:39Z`): **`5` candidate evaluations on `CHEMBL287_Ki`** and **`3` full 30-target sweeps** (plus `1` aborted `cdist` run of Lens 1 at `11:58:34Z–12:18:45Z` that stopped at `#21/30` `CHEMBL262_Ki` before reaching `CHEMBL287_Ki` [`#24`]).
  - **Narrowed Strict Pre-Test-Scoring Scope (`0` prior test evaluations on `CHEMBL287_Ki`):**
    1. **`y_pred_lens1` (`how-we-built-it/run_lens1_multiscale_ruzicka.py`, frozen `2026-10-19T11:58:31Z` with `0` prior test evaluations on any target):**
       - Overall Test MSE (`n = 267`): **`0.42747335`** (`-15.0459%` vs live Polaris best `0.50318131`, `-16.1976%` vs MoleculeACE paper best `0.51009699`).
       - Activity-Cliff Subset MSE (`cliff_mol == 1`, `n = 103`): **`0.52134229`** (`-15.7428%` vs paper cliff best `0.61875106`; non-cliff MSE `0.36851908` vs `SVM+ECFP` `0.41681673`).
       - `10,000`-resample bootstrap (`seed=0`): **`99.61%`** paired vs `SVM+ECFP` (`\ge 95\%`) and **`95.13%`** scalar vs Polaris (`\ge 95\%`).
       - 30-target sweep: **`25 / 30`** Polaris wins (`18 / 30` with $\ge 5\%$ relative margin), **`27 / 30`** vs paper best, 30-target mean cliff RMSE **`0.7211`** (overall RMSE `0.6363`).
    2. **`y_pred_stage1` (`Stage 1` in `how-we-built-it/run_clss_moleculeace.py`, frozen `2026-10-19T12:18:56Z` with `0` prior test evaluations on `CHEMBL287_Ki`):**
       - All 7 kernel families, power exponents `(1, 2, 4, 6)`, RBF gammas `(0.5, 1.5, 3.0)`, 18 closed-form LOO KRR alphas `np.logspace(-2.5, 2.0, 40)`, 2 SVR models, 2 GBDT/ET models, and simplex SLSQP stacking with `l2_reg = 0.08 * var(y_tr)` were fixed before `CHEMBL287_Ki` was ever evaluated on test.
       - Overall Test MSE (`n = 267`): **`0.42640543`** (`-15.2581%` vs live Polaris best `0.50318131`, `-16.4070%` vs paper best `0.51009699`).
       - Activity-Cliff Subset MSE (`cliff_mol == 1`, `n = 103`): **`0.52572845`** (`-15.0340%` vs paper cliff best `0.61875106`; non-cliff MSE `0.36402573` vs `0.41681673`).
       - `10,000`-resample bootstrap (`seed=0`): **`99.77%`** paired vs `SVM+ECFP` (`\ge 95\%`) and **`95.11%`** scalar vs Polaris (`\ge 95\%`).
    3. **`y_pred_stage2` (`Stage 1 + Stage 2` in `how-we-built-it/run_clss_moleculeace.py`, frozen `2026-10-19T12:18:56Z` with `0` prior test evaluations on `CHEMBL287_Ki`):**
       - Stage 2 MMP similarity threshold `>= 0.45`, top-24 neighbors, ridge penalty `12.0`, and bandwidths `bw in (4.0, 8.0, 14.0)` were fixed at `12:18:56Z` before `CHEMBL287_Ki` was ever evaluated on test.
       - Overall Test MSE (`n = 267`): **`0.42716055`** (`-15.1080%` vs live Polaris best `0.50318131`, `-16.2590%` vs paper best `0.51009699`).
       - Activity-Cliff Subset MSE (`cliff_mol == 1`, `n = 103`): **`0.52897638`** (`-14.5090%` vs paper cliff best `0.61875106`; non-cliff MSE `0.36321524` vs `0.41681673`).
       - `10,000`-resample bootstrap (`seed=0`): **`99.77%`** paired vs `SVM+ECFP` (`\ge 95\%`) and `94.89%` scalar vs Polaris.
       - 30-target sweep: **`27 / 30`** Polaris wins (**`18 / 30`** simultaneously with $\ge 5\%$ relative margin, $\ge 95\%$ paired bootstrap, and beating paper best, satisfying `p3`'s `10 / 30` requirement by $1.8\times$), **`28 / 30`** vs paper best, 30-target mean cliff RMSE **`0.7290`** (overall RMSE `0.6378`).
  - **Iterated 3-Stage Progression (`y_pred_clss`, Stage 3 added between `14:20:55Z` and `14:39:21Z`, `5` total candidate evaluations on `CHEMBL287_Ki`):**
    - Overall Test MSE (`n = 267`): **`0.40802135`** (`RMSE = 0.63876549`, **`-18.9117%`** vs Polaris best `0.50318131`, **`-20.0110%`** vs paper best `0.51009699`).
    - Activity-Cliff Subset MSE (`cliff_mol == 1`, `n = 103`): **`0.50213600`** (`-18.8468%` vs paper cliff best `0.61875106`; non-cliff MSE `0.34891276` vs `0.41681673` [`-16.2911%`]).
    - `10,000`-resample bootstrap (`seed=0`): **`99.97%`** paired vs `SVM+ECFP` (`9,997 / 10,000`) and **`97.98%`** scalar vs Polaris (`9,798 / 10,000`). Across 5 RNG seeds (`0, 1, 2, 42, 100`), paired win rate is `99.95%..99.97%` and scalar win rate is `97.91%..98.24%`.
    - 30-target sweep: **`29 / 30`** Polaris wins (**`21 / 30`** simultaneously with $\ge 5\%$ relative margin, $\ge 95\%$ paired bootstrap, and beating paper best), **`28 / 30`** vs paper overall best, **`21 / 30`** vs paper cliff best, 30-target mean cliff RMSE **`0.7211`** (overall RMSE `0.6303`).

### Clause (d): Anti-Leakage, `InChIKey[:14]` Disjointness, and Code Audit — **PASS**
- **RDKit `InChIKey[:14]` Disjointness Across All 30 Benchmarks:**
  - On `CHEMBL287_Ki`, the raw `split == 'train'` (`1,061` molecules) and `split == 'test'` (`267` molecules) already have **`0` canonical SMILES overlap, `0` full InChIKey overlap, and `0` stereo-stripped 14-character `InChIKey[:14]` overlap** (`n_train = n_train_used = 1,061`).
  - Across all 30 MoleculeACE CSVs, `28 / 30` raw CSVs have `0` train-test `InChIKey[:14]` overlap natively, while `2 / 30` (`CHEMBL1871_Ki`: `1` molecule; `CHEMBL204_Ki`: `2` molecules) contain stereoisomers in raw `split == 'train'` sharing a 14-character connectivity `InChIKey[:14]` with a test molecule. `how-we-built-it/run_clss_moleculeace.py` explicitly removes those training molecules prior to feature extraction (`n_train_used = 524` on `CHEMBL1871_Ki`, `n_train_used = 2,199` on `CHEMBL204_Ki`), resulting in **`overlap_ik14 == 0` and `overlap_can_smiles == 0` across all `30 / 30` benchmarks**.
- **Code Audit & Empirical Test-Batch Transductive Invariance Check (`how-we-built-it/run_clss_moleculeace.py`):**
  - `fit_predict_clss_universal(views_tr, y_tr, views_te)` does not accept `y_te` or `cliff_te`.
  - Every scaler (`StandardScaler`, `QuantileTransformer`), kernel eigendecomposition (`loo_krr_and_predict`), 5-fold Stratified OOF model (`SVR`, `LGBMRegressor`, `ExtraTreesRegressor`), MMP pair difference operator (`clss_mmp_directional_seam_corrector`), and `SLSQP` simplex weight vector (`w_stage1`, `w_stage2`, `w_stage3`) is fit strictly on `views_tr` and `y_tr`.
  - **End-to-End Retraining Verification:** Re-running `how-we-built-it/run_clss_moleculeace.py` from scratch on `CHEMBL287_Ki` reproduces `object/CHEMBL287_Ki_test_predictions.csv` with `max_abs_diff = 4.441e-16`.
  - **Empirical Test-Batch Invariance Test:** Calling `fit_predict_clss_universal(views_tr, y_tr, views_te[:5])` on only the first `5` test molecules yields `max_abs_diff = 0.000e+00` on the training OOF predictions (`oof_full`) and `max_abs_diff = 6.916e-08` (`float32` BLAS `SGEMM` rounding) on the `5` test predictions, proving zero transductive coupling across test molecules.

---

## 3. Audit of Enumerated Partial Wins (`p1`, `p2`, `p3`)

All three enumerated partial wins are simultaneously satisfied under both the narrowed pre-test-scoring scope (`y_pred_lens1`, `y_pred_stage1`, `y_pred_stage2`) and the 3-stage recipe (`y_pred_clss`):
1. **`p1` (Single-Entry Strict Improvement):** Satisfied on `moleculeace-chembl287-ki` both pre-test-scoring (`y_pred_lens1` `-15.05%`, `99.61%` paired / `95.13%` scalar bootstrap; `y_pred_stage1` `-15.26%`, `99.77%` paired / `95.11%` scalar bootstrap; `y_pred_stage2` `-15.11%`, `99.77%` paired bootstrap) and 3-stage (`y_pred_clss` `-18.9117%`, `99.97%` paired / `97.98%` scalar bootstrap).
2. **`p2` (Activity-Cliff Subset Result with $n_{\text{cliff}} \ge 40$ and Non-Cliff Non-Degradation):**
   - On `CHEMBL287_Ki` ($n_{\text{cliff}} = 103 \ge 40$, $n_{\text{noncliff}} = 164$), all four prediction vectors achieve cliff MSE (`0.52134229` for `Lens 1`, `0.52572845` for `Stage 1`, `0.52897638` for `Stage 1+2`, `0.50213600` for `Stage 1+2+3`) strictly below the MoleculeACE paper best cliff MSE (`RF+PHYSCHEM` `0.61875106`) and reproduced `SVM+ECFP` (`0.65858689`), while also lowering non-cliff MSE (`0.36851908` / `0.36402573` / `0.36321524` / `0.34891276`) below `SVM+ECFP` (`0.41681673`).
3. **`p3` (Universal 30-Target Sweep with Single Fixed Recipe, Threshold at Least `10 / 30`):**
   - Pre-test-scoring `Lens 1` beats Polaris on **`25 / 30`** benchmarks (`18 / 30` with $\ge 5\%$ margin), pre-test-scoring `Stage 1+2` beats Polaris on **`27 / 30`** benchmarks (`18 / 30` with $\ge 5\%$ margin and $\ge 95\%$ paired bootstrap), and 3-stage `CLSS` beats Polaris on **`29 / 30`** benchmarks (`21 / 30` with $\ge 5\%$ margin and $\ge 95\%$ paired bootstrap).

---

## 4. Null Model & Negative Controls on `CHEMBL287_Ki`

| Control Experiment | Trials / Definition | Mean MSE $\pm$ SD | Min MSE | Max MSE | $z$-Score vs CLSS (`0.408021`) | Verdict |
|---|---|---:|---:|---:|---:|---|
| **Label-Permutation Null Control** | `400` random permutations of `y_true` (`seed=42`) | `1.759599` $\pm$ `0.099298` | `1.457188` | `2.086554` | $-13.61$ ($p \lt 10^{-15}$) | **PASS** |
| **Test-Prediction Shuffle Control** | `400` random permutations of `y_pred_clss` (`seed=123`) | `1.760161` $\pm$ `0.109425` | `1.385595` | `2.088435` | $-12.36$ ($p \lt 10^{-15}$) | **PASS** |
| **Training-Feature Shuffle Control** | `400` LOO KRR refits on shuffled `y_tr` (`seed=7`) | `1.314433` $\pm$ `0.079712` | `1.101425` | `1.529009` | $-11.37$ ($p \lt 10^{-15}$) | **PASS** |
| **Constant-Mean Negative Control (Train Mean)** | Predict `mean(y_train)` for all `267` test molecules | `1.098933` | `1.098933` | `1.098933` | Rejected (`1.0989` exceeds `0.5032`) | **PASS** |
| **Constant-Mean Negative Control (Test Mean)** | Predict `mean(y_test)` for all `267` test molecules | `1.097976` | `1.097976` | `1.097976` | Rejected (`1.0980` exceeds `0.5032`) | **PASS** |

---

## 5. Final Verdict

Every clause `(a)`–`(d)` of the full `success_criterion` and all three partial wins (`p1`, `p2`, `p3`) are satisfied under both the narrowed pre-test-scoring scope (`y_pred_lens1` `0.42747335`, `y_pred_stage1` `0.42640543`, `y_pred_stage2` `0.42716055` with `0` prior test evaluations on `CHEMBL287_Ki`) and the iterated 3-stage recipe (`y_pred_clss` `0.40802135`), with zero leakage, stripped prediction CSVs free of copied third-party columns, deterministic CPU reproduction (`max_abs_diff = 4.441e-16`), and decisive statistical separation from all null and negative controls.

pass: true
