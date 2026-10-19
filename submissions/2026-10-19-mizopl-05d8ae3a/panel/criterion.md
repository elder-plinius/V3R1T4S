# Panelist Report: CRITERION (`polaris-moleculeace-activity-cliff-mse`)

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: polaris-moleculeace-activity-cliff-mse
confirmed_scope: A single fixed, deterministic, CPU-only CLSS recipe (claim/run_clss_moleculeace.py) fit strictly on stereo-stripped InChIKey[:14]-disjoint training splits (overlap == 0 across all 30/30 benchmarks) achieves test MSE 0.40802135 on moleculeace-chembl287-ki (claim/CHEMBL287_Ki_test_predictions.csv, sha256 05d8ae3a3797f666ed320364280c2ba0c099417174d42a0a4736f0366726623c, n_train = 1,061, n_test = 267, n_cliff = 103) vs live Polaris best 0.50318131 (-18.9117% relative) and MoleculeACE paper best 0.51009699 (-20.0110% relative) with 99.97% paired bootstrap win rate vs reproduced SVM+ECFP and 97.98% scalar bootstrap win rate vs Polaris best across 10,000 resamples (seed=0), while lowering cliff_mol==1 MSE (n = 103, at least 40) to 0.50213600 vs paper best 0.61875106 (-18.8468%) and non-cliff MSE to 0.34891276 vs 0.41681673 (-16.2911%, p2), and beating live Polaris best MSE on 29/30 MoleculeACE benchmarks (21/30 with at least 5% relative margin and at least 95% bootstrap win rate, p3) with 30-target macro-average cliff RMSE 0.7211 (overall RMSE 0.6303).

---

## 1. Mandate & Verification Protocol

As the fresh-context **CRITERION** skeptic panelist, I independently audited all files inside `claim/` without reading any external workspace files. Using an independent Python verification script executed in a temporary scratch directory (subsequently removed), I checked every literal clause `(a)` through `(d)` of the bank's `success_criterion`, all three enumerated partial wins (`p1`, `p2`, `p3`), hidden quantifiers, potential transductive or stereochemical leakage seams, and three distinct families of null/negative controls.

### Verified Artifact Checksums & Sizes

| Relative File Path | Size (Bytes) | Verified `sha256` Checksum |
|---|---:|---|
| `claim/CHEMBL287_Ki_test_predictions.csv` | `29,346` | `05d8ae3a3797f666ed320364280c2ba0c099417174d42a0a4736f0366726623c` |
| `claim/CHEMBL287_Ki_manifest.json` | `4,210` | `5d7e9e04e787fb7c746f422bc530aad8d3d00561244f4d7c94562640f1be90b4` |
| `claim/moleculeace_30_sweep_manifest.json` | `51,087` | `42c12361b8406c2530934bbed45a1acf701e4e03b50514a44f1dd056c17405e8` |
| `claim/benchmark_data/CHEMBL287_Ki.csv` | `121,021` | `e857875848bb64dc6e327e6c42fe9fd36526bbee1b976de4521b55c4c6629894` |
| `claim/MoleculeACE_results.csv` | `36,991` | `6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5` |
| `claim/polaris_moleculeace_30_audit.json` | `20,801` | `03312341e4e754cbef17b0d61c0eff93d7255cc8879ec1acb0245705925d5d35` |
| `claim/author_checker_moleculeace.py` | `12,528` | `2dbf427afd15922fd2720bf1babea60728e4be582e97ff62d9412ad245d21c92` |
| `claim/run_clss_moleculeace.py` | `25,441` | `8319686efb9cfe66b2298f27b946ddd8d9efbc46ee61623339747701a342f5e5` |

---

## 2. Literal Clause-by-Clause Audit of Full `success_criterion`

### Clause (a): Official Test Split Alignment, `y` Column (`log10(nM)`), SHA-256, and Polaris Counts — **PASS**
- **Primary Headline Target (`moleculeace-chembl287-ki` / `CHEMBL287_Ki`):**
  - `claim/CHEMBL287_Ki_test_predictions.csv` (`29,346` bytes, `sha256: 05d8ae3a3797f666ed320364280c2ba0c099417174d42a0a4736f0366726623c`) is byte-for-byte identical to `claim/predictions/CHEMBL287_Ki_test_predictions.csv` and contains exactly `267` rows (`test_row_index` `0..266`).
  - `claim/CHEMBL287_Ki_manifest.json` (`sha256: 5d7e9e04e787fb7c746f422bc530aad8d3d00561244f4d7c94562640f1be90b4`) records the benchmark slug `moleculeace-chembl287-ki`, the exact `sha256` (`e857875848bb64dc6e327e6c42fe9fd36526bbee1b976de4521b55c4c6629894`) of `claim/benchmark_data/CHEMBL287_Ki.csv`, and the exact `267` test-row indices (`test_csv_row_indices`: `[2, 6, 19, ..., 1325, 1327]`).
  - Independent verification confirms:
    1. `csv_row_index` in `claim/CHEMBL287_Ki_test_predictions.csv` equals `df_raw.index[df_raw['split'] == 'test']` with zero difference across all `267` test rows.
    2. `smiles`, `cliff_mol` (`103` cliff molecules with `cliff_mol == 1` and `164` non-cliff molecules with `cliff_mol == 0`), and `y_true` (`max_abs_diff = 0.0` against column `y`, `log10(nM)`) match `claim/benchmark_data/CHEMBL287_Ki.csv` (`split == 'test'`) in exact test order.
    3. The official train and test counts `n_train = 1,061` (`split == 'train'`) and `n_test = 267` (`split == 'test'`) match the Polaris API `nTrainDatapoints = 1,061` and `nTestDatapoints = 267`.
- **All 30 Benchmarks (`claim/predictions/CHEMBL*_test_predictions.csv`):**
  - Across all `30 / 30` benchmarks listed in `claim/moleculeace_30_sweep_manifest.json`, every `csv_sha256`, `pred_csv_sha256`, `pred_csv_bytes`, `n_train`, `n_test`, `csv_row_index`, `smiles`, `cliff_mol`, and `y_true` (`max_abs_diff = 0.0`) matches `claim/benchmark_data/CHEMBL*.csv` and `claim/polaris_moleculeace_30_audit.json`.

### Clause (b): Independent `sklearn.metrics.mean_squared_error` Strictly Lower Than Live Polaris Leaderboard & Paper Best — **PASS**
- **Primary Headline Target (`moleculeace-chembl287-ki` / `CHEMBL287_Ki`):**
  - Independent `sklearn.metrics.mean_squared_error(y_true, y_pred_clss)` = **`0.40802135`** (`0.40802135239783544`, `RMSE = 0.63876549`).
  - Live Polaris Leaderboard Best MSE (`autosota-moleculeace-chembl287-ki`): **`0.50318131`** (`0.5031813063290076`, `RMSE = 0.70935274`). CLSS is strictly lower by **`0.09515995` MSE units (`-18.9117%` relative)**.
  - MoleculeACE Paper Best MSE across all 24 baseline methods in `claim/MoleculeACE_results.csv` (`SVM+ECFP`, `rmse = 0.71421075`): **`0.51009699`** (`0.5100969897018766`). CLSS is strictly lower by **`0.10207564` MSE units (`-20.0110%` relative)**.
  - Faithfully Reproduced `SVM+ECFP` Baseline MSE: **`0.51008387`** (`0.5100838672816728`).
- **30-Benchmark Sweep:**
  - CLSS achieves strictly lower MSE than EVERY listed entry on the live Polaris leaderboard on **`29 / 30`** benchmarks, including **both 3-entry leaderboards**:
    - `moleculeace-chembl234-ki` (`CHEMBL234_Ki`, 3 live entries, best `0.37022063`, paper best `0.38646355`): CLSS MSE = **`0.36037801`** (`-2.6586%` vs Polaris, `-6.7498%` vs Paper).
    - `moleculeace-chembl236-ki` (`CHEMBL236_Ki`, 3 live entries, best `0.44968493`, paper best `0.48471536`): CLSS MSE = **`0.44350711`** (`-1.3738%` vs Polaris, `-8.5015%` vs Paper).
  - CLSS also achieves strictly lower MSE than the MoleculeACE paper best across all 24 algorithms on **`28 / 30`** benchmarks.

### Clause (c): Relative Margin at Least `5%` AND `10,000`-Resample Bootstrap Win Rate at Least `95%` — **PASS**
- **Relative Margin on `moleculeace-chembl287-ki` (`CHEMBL287_Ki`):**
  - Relative MSE reduction vs live Polaris best (`0.50318131`): **`18.9117%`** (at least `5.0%`, exceeding the threshold by $3.78\times$).
  - Relative MSE reduction vs MoleculeACE paper best (`0.51009699`): **`20.0110%`** (at least `5.0%`).
- **10,000-Resample Bootstrap (`seed=0`) on `moleculeace-chembl287-ki` (`CHEMBL287_Ki`):**
  - **Paired Bootstrap Win Rate** over the `267` test molecules against the reproduced `SVM+ECFP` baseline (`0.51008387`): **`99.97%` (`9,997 / 10,000` resamples, at least `95.0%`)**.
  - **Unpaired Scalar Bootstrap Win Rate** of CLSS squared errors against the scalar live Polaris listed best `0.50318131`: **`97.98%` (`9,798 / 10,000` resamples, at least `95.0%`)**.
  - **Multi-Seed Stability Check (`10,000` resamples each):**
    - `seed=0`: paired `99.97%` (`9,997 / 10,000`), scalar `97.98%` (`9,798 / 10,000`)
    - `seed=1`: paired `99.95%` (`9,995 / 10,000`), scalar `97.92%` (`9,792 / 10,000`)
    - `seed=2`: paired `99.97%` (`9,997 / 10,000`), scalar `98.17%` (`9,817 / 10,000`)
    - `seed=42`: paired `99.97%` (`9,997 / 10,000`), scalar `98.24%` (`9,824 / 10,000`)
    - `seed=100`: paired `99.97%` (`9,997 / 10,000`), scalar `97.91%` (`9,791 / 10,000`)
  - Across all 5 independent RNG seeds, both the paired and unpaired scalar bootstrap win rates remain well above `95%` (`99.95%..99.97%` paired, `97.91%..98.24%` scalar).
- **Simultaneous Satisfaction Across the 30-Target Sweep:**
  - **`21 / 30`** benchmarks simultaneously satisfy all three criteria: relative MSE improvement at least `5.0%` vs live Polaris best, `10,000`-resample paired bootstrap win rate at least `95.0%` vs `SVM+ECFP`, and MSE strictly below the MoleculeACE paper best.

### Clause (d): Anti-Leakage, `InChIKey[:14]` Disjointness, and Code Audit — **PASS**
- **RDKit `InChIKey[:14]` Disjointness Across All 30 Benchmarks:**
  - On `CHEMBL287_Ki`, the raw `split == 'train'` (`1,061` molecules) and `split == 'test'` (`267` molecules) already have **`0` canonical SMILES overlap, `0` full InChIKey overlap, and `0` stereo-stripped 14-character `InChIKey[:14]` overlap** (`n_train = n_train_used = 1,061`).
  - Across all 30 MoleculeACE CSVs, `28 / 30` raw CSVs have `0` train-test `InChIKey[:14]` overlap natively, while `2 / 30` (`CHEMBL1871_Ki`: `1` molecule; `CHEMBL204_Ki`: `2` molecules) contain stereoisomers in raw `split == 'train'` sharing a 14-character connectivity `InChIKey[:14]` with a test molecule. Lines `504–506` of `claim/run_clss_moleculeace.py` explicitly remove those training molecules prior to feature extraction (`n_train_used = 524` on `CHEMBL1871_Ki`, `n_train_used = 2,199` on `CHEMBL204_Ki`), resulting in **`overlap_ik14 == 0` and `overlap_can_smiles == 0` across all `30 / 30` benchmarks**.
- **Code Audit & Empirical Test-Batch Transductive Invariance Check (`claim/run_clss_moleculeace.py`):**
  - Line `514` (`pred_te, oof_pred, _, _ = fit_predict_clss_universal(views_tr, y_tr, views_te)`) does not pass `y_te` or `cliff_te` into `fit_predict_clss_universal`.
  - Every scaler (`StandardScaler` on lines `232` and `331`, `QuantileTransformer` on line `479`), kernel eigendecomposition (`loo_krr_and_predict`), 5-fold Stratified OOF model (`SVR`, `LGBMRegressor`, `ExtraTreesRegressor`), MMP pair difference operator (`clss_mmp_directional_seam_corrector`), and `SLSQP` simplex weight vector (`w_stage1`, `w_stage2`, `w_stage3`) is fit strictly on `views_tr` and `y_tr`.
  - **End-to-End Retraining Verification:** Re-running `claim/run_clss_moleculeace.py` from scratch on `CHEMBL287_Ki` reproduces `claim/CHEMBL287_Ki_test_predictions.csv` with `max_abs_diff = 4.441e-16`.
  - **Empirical Test-Batch Invariance Test:** Calling `fit_predict_clss_universal(views_tr, y_tr, views_te[:5])` on only the first `5` test molecules yields `max_abs_diff = 0.000e+00` on the training OOF predictions (`oof_full`) and `max_abs_diff = 6.916e-08` (`float32` BLAS `SGEMM` rounding) on the `5` test predictions, proving zero transductive coupling across test molecules.

---

## 3. Audit of Enumerated Partial Wins (`p1`, `p2`, `p3`)

All three enumerated partial wins are simultaneously satisfied and subsumed by the full criterion win:
1. **`p1` (Single-Entry Strict Improvement):** Satisfied on **`21 / 28`** single-entry benchmarks, headlined by `moleculeace-chembl287-ki` (`-18.9117%` relative MSE reduction vs Polaris best, `99.97%` paired / `97.98%` scalar bootstrap win rate).
2. **`p2` (Activity-Cliff Subset Result with $n_{\text{cliff}} \ge 40$ and Non-Cliff Non-Degradation):**
   - On `CHEMBL287_Ki` ($n_{\text{cliff}} = 103 \ge 40$, $n_{\text{noncliff}} = 164$):
     - **CLSS Cliff MSE (`cliff_mol == 1`):** **`0.50213600`** (`RMSE = 0.70861555`) vs MoleculeACE paper best cliff MSE **`0.61875106`** (`RF+PHYSCHEM` / `MLP+ECFP` in `claim/MoleculeACE_results.csv`, **`-18.8468%` relative reduction**) and vs reproduced `SVM+ECFP` cliff MSE **`0.65858689`** (**`-23.7555%` relative reduction**, **`99.90%` paired bootstrap win rate** on cliff molecules).
     - **CLSS Non-Cliff MSE (`cliff_mol == 0`):** **`0.34891276`** (`RMSE = 0.59068838`) vs reproduced `SVM+ECFP` non-cliff MSE **`0.41681673`** (**`-16.2911%` relative reduction**, strictly better on non-cliffs as well).
   - Across the 30-target suite, **`20 / 30`** targets have $n_{\text{cliff}} \ge 40$, non-cliff MSE at or below `SVM+ECFP`, and cliff MSE strictly below the best cliff MSE of all 24 methods in the MoleculeACE paper (`22 / 30` against reproduced best classical cliff MSE, and `23 / 30` against `SVM+ECFP` cliff MSE).
3. **`p3` (Universal 30-Target Sweep with Single Fixed Recipe, Threshold at Least `10 / 30`):**
   - The single fixed recipe (`claim/run_clss_moleculeace.py`, zero per-target test tuning) beats the live Polaris listed best MSE on **`29 / 30`** benchmarks and achieves at least `5%` relative improvement + at least `95%` paired bootstrap win rate + beating the MoleculeACE paper best on **`21 / 30`** benchmarks (more than double the `10 / 30` requirement), with 30-target macro-average overall RMSE **`0.6303`** (`MSE = 0.4020`), cliff RMSE **`0.7211`** (`MSE = 0.5298`), and non-cliff RMSE **`0.5797`** (`MSE = 0.3421`).

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

Every clause `(a)`–`(d)` of the full `success_criterion` and all three partial wins (`p1`, `p2`, `p3`) are literally and simultaneously satisfied with zero leakage, deterministic CPU reproduction (`max_abs_diff = 4.441e-16`), and decisive statistical separation from all null and negative controls.

pass: true
