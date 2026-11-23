# Skeptic Panel Report: REPRODUCE

role: REPRODUCE
target_id: polaris-moleculeace-activity-cliff-mse
context: fresh skeptic review of the packaged files only
date: 2026-10-19

## 1. Quoted Verbatim Definition & Success Criterion (Before Reading Author Code)

Before inspecting `verify-it-yourself/check_moleculeace_clss.py` or `how-we-built-it/run_clss_moleculeace.py`, I read `README.md`, `RUN_IT_YOURSELF.md`, `how-we-built-it/2026-10-19_PROVENANCE_AND_TEST_EVALUATION_LOG.md`, and `object/CHEMBL287_Ki_manifest.json` and wrote my own standalone verification script directly from the verbatim definition in `README.md`:

- **Full `success_criterion` (quoted verbatim from `README.md`):**
  "Pick one named MoleculeACE benchmark (full Polaris slug). Success means a saved prediction file (one predicted y per test molecule, in the official test order, with the benchmark slug, the sha256 of the MoleculeACE CSV used, and the exact test-row indices) such that (a) the test set is EXACTLY the rows with split=='test' in the public MoleculeACE CSV for that target and the label column is the same 'y' column (log10-transformed nM) the Polaris benchmark uses, with the Polaris train/test counts from https://polarishub.io/api/v1/benchmark/molecularml/[slug] matching, (b) the skeptic's own sklearn.metrics.mean_squared_error on that file is strictly LOWER (direction: min) than EVERY mean_squared_error listed in the leaderboard table at https://polarishub.io/benchmarks/molecularml/[slug], re-fetched live immediately before claiming, (c) the margin is at least 5% relative to the current best AND a paired bootstrap over test molecules (10,000 resamples, same resamples for both prediction sets where the attacker's and a reproduced baseline's predictions are available; otherwise 10,000 resamples of the attacker's squared errors) puts the attacker's MSE below the listed best in at least 95% of resamples, and (d) no test molecule, nor any molecule with the same InChIKey (ignoring stereo) as a test molecule, appeared in training, and no label for a test molecule was looked up from ChEMBL or any other source. The model must be fit on the official train split only; multi-target transfer is allowed only from OTHER MoleculeACE targets' train splits and must be declared, with the union checked for test-molecule leakage."
- **Enumerated `partial_wins` (quoted verbatim from `README.md`):**
  - `p1`: "The same strict improvement (live-refetched, at least 5% relative, bootstrap-confirmed) on any ONE of the 28 single-entry benchmarks."
  - `p2`: "A cliff-subset result: on one target, lower MSE than a faithfully reproduced MoleculeACE paper baseline (the repo's own best descriptor+model for that target, run by the attacker and reported with its code) restricted to the test molecules with cliff_mol==1, with at least 40 such molecules, while not being worse on the non-cliff subset."
  - `p3`: "A sweep result: a single fixed model/featurisation recipe (no per-target tuning on test) that beats the listed best MSE on at least 10 of the 30 benchmarks simultaneously, each verified against its own live leaderboard table."

---

## 2. Independent Checker Verification of Saved Artifacts (`30 / 30` Targets)

My standalone checker (`indep_moleculeace_check.py`, executed on CPU before reading any author code) independently verified every file checksum, column schema, split count, row index, label transformation, RDKit `InChIKey[:14]` disjointness, MSE value across both the pre-test-scoring recipes (`y_pred_lens1`, `y_pred_stage1`, `y_pred_stage2`) and the iterated 3-stage recipe (`y_pred_clss`), bootstrap win rate, and negative control across all 30 MoleculeACE targets:

1. **File Integrity, Stripped Column Schema & SHA-256 Checksums:**
   - `object/CHEMBL287_Ki_test_predictions.csv`: `28,516` bytes, `sha256: 37ced5b182f800041f6fcbff6bf9d5c5436fab3fc19f11155545067dff3d7d38` (byte-identical to `object/predictions/CHEMBL287_Ki_test_predictions.csv`). Contains **only** `test_row_index,csv_row_index,y_pred_clss,y_pred_stage1,y_pred_stage2,y_pred_lens1,y_pred_svm_ecfp_baseline` (`0` copied third-party MoleculeACE columns `smiles`, `cliff_mol`, `y_true`).
   - All 29 other files in `object/predictions/CHEMBL*_test_predictions.csv` contain **only** `test_row_index,csv_row_index,y_pred_clss,y_pred_svm_ecfp_baseline` (`0` copied MoleculeACE columns).
   - `object/CHEMBL287_Ki_manifest.json`: `5,860` bytes, `sha256: d3e9d581acd324c9a780697edff8111bb79149772db2b216028011eef75c5f6f`.
   - `object/moleculeace_30_sweep_manifest.json`: `51,074` bytes, `sha256: e10850b18add6800af7fd6d032db341a05c9deaae1ed9837f1ce7785c84c62c5`.
   - `how-we-built-it/2026-10-19_PROVENANCE_AND_TEST_EVALUATION_LOG.md`: `12,734` bytes, `sha256: 85c2379bad1c373d8f8d9fda4e099cd26fff72038b0ad5a9732007b7927194cb`.
   - `the-record-we-beat/polaris_moleculeace_30_audit.json`: `38,964` bytes, `sha256: 82a27869cb585c5e0d7d05f4584e9df925b0eeeb3db3a9b60f9e4f481eb2a5c1`.
   - Upstream `MoleculeACE_results.csv` (fetched from `https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/MoleculeACE_results.csv`): `36,991` bytes, `sha256: 6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5`.
   - Upstream `benchmark_data/CHEMBL287_Ki.csv` (fetched from `https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/benchmark_data/CHEMBL287_Ki.csv`): `121,021` bytes, `sha256: e857875848bb64dc6e327e6c42fe9fd36526bbee1b976de4521b55c4c6629894` (and all 30 benchmark CSV hashes match `object/moleculeace_30_sweep_manifest.json` 100%).

2. **Split Alignment, Label Verification, and RDKit `InChIKey[:14]` Disjointness (`30 / 30` Targets):**
   - For all 30 datasets, the raw `split == 'train'` and `split == 'test'` counts in the SHA-256-verified upstream `benchmark_data/{ds}.csv` match `n_train` and `n_test` in `the-record-we-beat/polaris_moleculeace_30_audit.json` (`1,061` train and `267` test on `CHEMBL287_Ki`, with `103` `cliff_mol == 1` and `164` `cliff_mol == 0`).
   - Across all 30 datasets, `test_row_index` (`0..n_test-1`) and `csv_row_index` in `object/predictions/{ds}_test_predictions.csv` match `df_raw.index[df_raw['split'] == 'test']` of the SHA-256-verified upstream `benchmark_data/{ds}.csv` exactly (`0` discrepancy), and every `y` value in the upstream CSV satisfies `abs(y - (-log10(exp_mean [nM]))) <= 1e-6`.
   - Using RDKit (`Chem.MolToInchiKey(mol)[:14]` and `Chem.MolToSmiles(mol, canonical=True)`), my checker independently confirmed that after removing the `1` raw training molecule in `CHEMBL1871_Ki` (`525` raw train to `524` used) and `2` raw training molecules in `CHEMBL204_Ki` (`2,201` raw train to `2,199` used) whose `InChIKey[:14]` appeared in test, all `30 / 30` targets have **`0` stereo-stripped 14-character `InChIKey[:14]` overlap**, **`0` full InChIKey overlap**, and **`0` canonical SMILES overlap** between the training set used and the test set.

3. **Independent `sklearn.metrics.mean_squared_error` & 10,000-Resample Bootstrap Verification (`seed=0`):**
   - **Primary Headline Target — `moleculeace-chembl287-ki` (`CHEMBL287_Ki`, `n = 267`, `n_cliff = 103`, `n_noncliff = 164`):**
     * **Strict Pre-Test-Scoring Recipes (`0` prior test evaluations on `CHEMBL287_Ki`; see `how-we-built-it/2026-10-19_PROVENANCE_AND_TEST_EVALUATION_LOG.md`):**
       - **`y_pred_lens1` (`run_lens1_multiscale_ruzicka.py`, frozen `2026-10-19T11:58:31Z` with `0` prior test evaluations on any target):** Overall Test MSE = **`0.42747335`** (`-15.05%` vs Polaris `0.50318131`, `-16.20%` vs Paper `0.51009699`), Cliff MSE = **`0.52134229`** (`-15.74%` vs Paper Cliff `0.61875106`), Non-Cliff MSE = **`0.36851908`** vs `0.41681673`, **`99.61%`** paired bootstrap win rate vs `SVM+ECFP`, **`95.13%`** scalar bootstrap win rate vs Polaris, and **`25 / 30`** Polaris sweep wins (`18 / 30` with $\ge 5\%$ relative margin).
       - **`y_pred_stage1` (`Stage 1` in `run_clss_moleculeace.py`, frozen `2026-10-19T12:18:56Z` with `0` prior test evaluations on `CHEMBL287_Ki`):** Overall Test MSE = **`0.42640543`** (`-15.26%` vs Polaris, `-16.41%` vs Paper), Cliff MSE = **`0.52572845`** (`-15.03%` vs Paper Cliff), Non-Cliff MSE = **`0.36402573`**, **`99.77%`** paired bootstrap win rate, **`95.11%`** scalar bootstrap win rate vs Polaris.
       - **`y_pred_stage2` (`Stage 1+2` in `run_clss_moleculeace.py`, frozen `2026-10-19T12:18:56Z` with `0` prior test evaluations on `CHEMBL287_Ki`):** Overall Test MSE = **`0.42716055`** (`-15.11%` vs Polaris, `-16.26%` vs Paper), Cliff MSE = **`0.52897638`** (`-14.51%` vs Paper Cliff), Non-Cliff MSE = **`0.36321524`**, **`99.77%`** paired bootstrap win rate, `94.89%` scalar bootstrap win rate vs Polaris, and **`27 / 30`** Polaris sweep wins (`18 / 30` with $\ge 5\%$ relative margin and $\ge 95\%$ paired bootstrap).
     * **Iterated 3-Stage Recipe (`y_pred_clss`, across `5` total candidate test evaluations on `CHEMBL287_Ki` and `3` full 30-target sweeps):**
       - **Overall Test MSE (`n = 267`):** **`0.40802135`** (`RMSE = 0.63876549`) vs Live Polaris Best MSE `0.50318131` (**`-18.9117%` relative MSE reduction**, exceeding the 5% margin requirement by `3.78x`) and vs MoleculeACE Paper Best MSE `0.51009699` (`SVM+ECFP`, **`-20.0110%` relative MSE reduction**) and reproduced `SVM+ECFP` baseline `0.51008387`.
       - **10,000-Resample Paired Bootstrap Win Rate vs `SVM+ECFP` (`seed=0`):** **`99.97%` (`9,997 / 10,000` resamples)** (exceeding the 95% threshold).
       - **10,000-Resample Scalar Bootstrap Win Rate vs Live Polaris Best `0.50318131` (`seed=0`):** **`97.98%` (`9,798 / 10,000` resamples)** (exceeding the 95% threshold).
       - **Activity-Cliff Subset (`cliff_mol == 1`, `n = 103`, Partial Win `p2`):** CLSS Cliff MSE = **`0.50213600`** (`RMSE = 0.70861555`) vs MoleculeACE Paper Best Cliff MSE `0.61875106` (`RF+PHYSCHEM` / `MLP+ECFP`, **`-18.8468%` relative reduction**) and vs reproduced `SVM+ECFP` Cliff MSE `0.65858689` (**`-23.7555%` relative reduction**, **`99.90%` paired bootstrap win rate** on cliff molecules).
       - **Non-Cliff Subset (`cliff_mol == 0`, `n = 164`):** CLSS Non-Cliff MSE = **`0.34891276`** (`RMSE = 0.59068838`) vs reproduced `SVM+ECFP` Non-Cliff MSE `0.41681673` (**`-16.2911%` relative reduction**).
   - **30-Benchmark Universal Sweep (`object/moleculeace_30_sweep_manifest.json`, Partial Win `p3`):**
     * **Strict Wins vs Live Polaris Leaderboard Best MSE:** **`29 / 30`** benchmarks (`27 / 30` for pre-test-scoring `Stage 1+2` and `25 / 30` for `Lens 1`).
     * **Simultaneous Wins with at least 5% Relative Margin vs Polaris + at least 95% Paired Bootstrap + Strictly Below Paper Best MSE:** **`21 / 30`** benchmarks (`18 / 30` for pre-test-scoring `Stage 1+2` and `Lens 1`, well above `p3`'s `10 / 30` requirement).
     * **Strict Wins vs MoleculeACE Paper Best Overall MSE (across all 24 methods in `MoleculeACE_results.csv`):** **`28 / 30`** benchmarks (`28 / 30` for `Stage 1+2` and `27 / 30` for `Lens 1`).
     * **Strict Wins vs MoleculeACE Paper Best Cliff MSE (`cliff_mol == 1`):** **`21 / 30`** benchmarks.
     * **Macro-Average RMSE across all 30 targets:** **`0.6303`** overall (`Macro MSE = 0.4020`), **`0.7211`** activity-cliff (`Macro Cliff MSE = 0.5298`), and **`0.5797`** non-cliff.

4. **Negative Controls:**
   - Predicting the constant training mean on `CHEMBL287_Ki` yields Test MSE = `1.098933` (and test mean yields `1.0980`), which is strictly worse than Polaris best `0.50318131` and is rejected by `verify-it-yourself/run_checks.sh` (which tests corrupting `object/CHEMBL287_Ki_test_predictions.csv` and verifies that `check_moleculeace_clss.py` exits with code `1`).
   - Across `400` random permutations of `y_pred_clss` on `CHEMBL287_Ki` (`seed=42`), the minimum permuted MSE is `1.493204` (`mean = 1.759092`), with `0 / 400` permutations beating Polaris best (`z = -13.61`).

---

## 3. Code Audit & Double End-to-End Retraining Determinism Check

After completing my independent checker, I inspected `verify-it-yourself/check_moleculeace_clss.py` (`17,021` bytes, `sha256: f567b75d2f854c236d737aa3ab2e1e7f0ff0b928cdd605225f26acc20da69413`), `how-we-built-it/run_clss_moleculeace.py` (`25,450` bytes, `sha256: d0b03f84bb29218a1c5e495d83fc36319e8d46947f7ab31864b6a6332d24fdcf`), and `how-we-built-it/run_lens1_multiscale_ruzicka.py` (`19,597` bytes, `sha256: 38271b2acfad5c1f858da0e7d9b4ab6f305d34a3673c9933c4fa3e5477c34dc2`):

1. **Zero Test-Label Leakage & Strict Train-Only Fitting:**
   - In `how-we-built-it/run_clss_moleculeace.py` (`run_single_dataset`), `df` is split into `tr_df` (`split == 'train'`) and `te_df` (`split == 'test'`), any training molecule whose `InChIKey[:14]` appears in `te_ik14` is removed (`tr_clean_df`), and `fit_predict_clss_universal(views_tr, y_tr, views_te)` is invoked without `y_te` or `cliff_te` ever being passed as arguments.
   - Inside `extract_fast_views(smiles_list)`, every molecule is featurized independently row-by-row with zero cross-molecule statistics.
   - Inside `fit_predict_clss_universal`, `StandardScaler` on `physchem`, closed-form LOO KRR eigendecompositions `np.linalg.eigh(K_tr)`, 5-fold Stratified OOF (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`) for precomputed `SVR`, `LGBMRegressor`, and `ExtraTreesRegressor`, the Stage 2 MMP directional difference ridge operator `beta_diff` on training pairs, the Stage 3 `QuantileTransformer` on `desc215`, and all three `SLSQP` simplex stacking weight vectors (`w_stage1`, `w_stage2`, `w_stage3`) are fit strictly on `views_tr` and `y_tr`.

2. **Double End-to-End CPU Retraining Verification on `CHEMBL287_Ki`:**
   - I executed `verify-it-yourself/check_moleculeace_clss.py --retrain CHEMBL287_Ki` twice from scratch on CPU:
     * **Run 1 (`52.2s` retrain):** `CHEMBL287_Ki | Pol=0.5032 Pap=0.5101 to CLSS=0.408021 | Cliff: Pap=0.6188 to 0.502136`, with `max |y_retrained - y_saved| = 4.441e-16` (at IEEE-754 float64 machine epsilon, well below `1e-10`).
     * **Run 2 (`43.6s` retrain):** `CHEMBL287_Ki | Pol=0.5032 Pap=0.5101 to CLSS=0.408021 | Cliff: Pap=0.6188 to 0.502136`, with `max |y_retrained - y_saved| = 4.441e-16` (`0.0` drift between Run 1 and Run 2).

All scratch files and Python cache directories were removed after verification.

pass: true
