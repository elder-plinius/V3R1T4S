# Skeptic Panel Report: REPRODUCE

role: REPRODUCE
target_id: polaris-moleculeace-activity-cliff-mse
context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
date: 2026-10-19

## 1. Quoted Verbatim Definition & Success Criterion (Before Reading Author Code)

Before inspecting `claim/author_checker_moleculeace.py` or `claim/run_clss_moleculeace.py`, I read `claim/CLAIM.md`, `claim/REPRODUCE.md`, and `claim/CHEMBL287_Ki_manifest.json` and wrote my own standalone verification script directly from the verbatim definition in `claim/CLAIM.md`:

- **Full `success_criterion` (quoted verbatim from `claim/CLAIM.md`):**
  "Pick one named MoleculeACE benchmark (full Polaris slug). Success means a saved prediction file (one predicted y per test molecule, in the official test order, with the benchmark slug, the sha256 of the MoleculeACE CSV used, and the exact test-row indices) such that (a) the test set is EXACTLY the rows with split=='test' in the public MoleculeACE CSV for that target and the label column is the same 'y' column (log10-transformed nM) the Polaris benchmark uses, with the Polaris train/test counts from https://polarishub.io/api/v1/benchmark/molecularml/[slug] matching, (b) the skeptic's own sklearn.metrics.mean_squared_error on that file is strictly LOWER (direction: min) than EVERY mean_squared_error listed in the leaderboard table at https://polarishub.io/benchmarks/molecularml/[slug], re-fetched live immediately before claiming, (c) the margin is at least 5% relative to the current best AND a paired bootstrap over test molecules (10,000 resamples, same resamples for both prediction sets where the attacker's and a reproduced baseline's predictions are available; otherwise 10,000 resamples of the attacker's squared errors) puts the attacker's MSE below the listed best in at least 95% of resamples, and (d) no test molecule, nor any molecule with the same InChIKey (ignoring stereo) as a test molecule, appeared in training, and no label for a test molecule was looked up from ChEMBL or any other source. The model must be fit on the official train split only; multi-target transfer is allowed only from OTHER MoleculeACE targets' train splits and must be declared, with the union checked for test-molecule leakage."
- **Enumerated `partial_wins` (quoted verbatim from `claim/CLAIM.md`):**
  - `p1`: "The same strict improvement (live-refetched, at least 5% relative, bootstrap-confirmed) on any ONE of the 28 single-entry benchmarks."
  - `p2`: "A cliff-subset result: on one target, lower MSE than a faithfully reproduced MoleculeACE paper baseline (the repo's own best descriptor+model for that target, run by the attacker and reported with its code) restricted to the test molecules with cliff_mol==1, with at least 40 such molecules, while not being worse on the non-cliff subset."
  - `p3`: "A sweep result: a single fixed model/featurisation recipe (no per-target tuning on test) that beats the listed best MSE on at least 10 of the 30 benchmarks simultaneously, each verified against its own live leaderboard table."

---

## 2. Independent Checker Verification of Saved Artifacts (`30 / 30` Targets)

My standalone checker (`indep_moleculeace_check.py`, executed in `15.32s` on CPU before reading any author code) independently verified every file checksum, split count, row index, label transformation, RDKit `InChIKey[:14]` disjointness, MSE value, bootstrap win rate, and negative control across all 30 MoleculeACE targets:

1. **File Integrity & SHA-256 Checksums:**
   - `claim/CHEMBL287_Ki_test_predictions.csv`: `29,346` bytes, `sha256: 05d8ae3a3797f666ed320364280c2ba0c099417174d42a0a4736f0366726623c` (byte-identical to `claim/predictions/CHEMBL287_Ki_test_predictions.csv`).
   - `claim/CHEMBL287_Ki_manifest.json`: `4,210` bytes, `sha256: 5d7e9e04e787fb7c746f422bc530aad8d3d00561244f4d7c94562640f1be90b4`.
   - `claim/moleculeace_30_sweep_manifest.json`: `51,087` bytes, `sha256: 42c12361b8406c2530934bbed45a1acf701e4e03b50514a44f1dd056c17405e8`.
   - `claim/MoleculeACE_results.csv`: `36,991` bytes, `sha256: 6aa88c897f16bbb328793a2917289e3972b3fc8b50cc56be840f6714ea9baae5`, and `claim/polaris_moleculeace_30_audit.json`: `20,801` bytes, `sha256: 03312341e4e754cbef17b0d61c0eff93d7255cc8879ec1acb0245705925d5d35` (all 30 benchmark CSV hashes in `claim/benchmark_data/CHEMBL*.csv` and all 30 prediction CSV sizes and hashes in `claim/predictions/CHEMBL*_test_predictions.csv` match `claim/moleculeace_30_sweep_manifest.json` 100%).
   - `claim/benchmark_data/CHEMBL287_Ki.csv`: `121,021` bytes, `sha256: e857875848bb64dc6e327e6c42fe9fd36526bbee1b976de4521b55c4c6629894`.

2. **Split Alignment, Label Verification, and RDKit `InChIKey[:14]` Disjointness (`30 / 30` Targets):**
   - For all 30 datasets, the raw `split == 'train'` and `split == 'test'` counts in `claim/benchmark_data/{ds}.csv` match `n_train` and `n_test` in `claim/polaris_moleculeace_30_audit.json` (`1,061` train and `267` test on `CHEMBL287_Ki`, with `103` `cliff_mol == 1` and `164` `cliff_mol == 0`).
   - Across all 30 datasets, `test_row_index`, `csv_row_index`, `smiles`, `cliff_mol`, and `y_true` in `claim/predictions/{ds}_test_predictions.csv` match the exact `split == 'test'` rows of `claim/benchmark_data/{ds}.csv` to machine precision (`0.0` discrepancy), and every `y` value satisfies `abs(y - (-log10(exp_mean [nM]))) <= 1e-6`.
   - Using RDKit (`Chem.MolToInchiKey(mol)[:14]` and `Chem.MolToSmiles(mol, canonical=True)`), my checker independently confirmed that after removing the `1` raw training molecule in `CHEMBL1871_Ki` (`525` raw train to `524` used) and `2` raw training molecules in `CHEMBL204_Ki` (`2,201` raw train to `2,199` used) whose `InChIKey[:14]` appeared in test, all `30 / 30` targets have **`0` stereo-stripped 14-character `InChIKey[:14]` overlap**, **`0` full InChIKey overlap**, and **`0` canonical SMILES overlap** between the training set used and the test set.

3. **Independent `sklearn.metrics.mean_squared_error` & 10,000-Resample Bootstrap Verification (`seed=0`):**
   - **Primary Headline Target — `moleculeace-chembl287-ki` (`CHEMBL287_Ki`):**
     * **Overall Test MSE (`n = 267`):** `0.40802135` (`RMSE = 0.63876549`) vs Live Polaris Best MSE `0.50318131` (**`-18.9117%` relative MSE reduction**, exceeding the 5% margin requirement by `3.78x`) and vs MoleculeACE Paper Best MSE `0.51009699` (`SVM+ECFP`, **`-20.0110%` relative MSE reduction**) and reproduced `SVM+ECFP` baseline `0.51008387`.
     * **10,000-Resample Paired Bootstrap Win Rate vs `SVM+ECFP` (`seed=0`):** **`99.97%` (`9,997 / 10,000` resamples)** (exceeding the 95% threshold).
     * **10,000-Resample Scalar Bootstrap Win Rate vs Live Polaris Best `0.50318131` (`seed=0`):** **`97.98%` (`9,798 / 10,000` resamples)** (exceeding the 95% threshold).
     * **Activity-Cliff Subset (`cliff_mol == 1`, `n = 103`, Partial Win `p2`):** CLSS Cliff MSE = **`0.50213600`** (`RMSE = 0.70861555`) vs MoleculeACE Paper Best Cliff MSE `0.61875106` (`MLP+ECFP`, **`-18.8468%` relative reduction**) and vs reproduced `SVM+ECFP` Cliff MSE `0.65858689` (**`-23.7555%` relative reduction**, **`99.90%` paired bootstrap win rate** on cliff molecules).
     * **Non-Cliff Subset (`cliff_mol == 0`, `n = 164`):** CLSS Non-Cliff MSE = **`0.34891276`** (`RMSE = 0.59068838`) vs reproduced `SVM+ECFP` Non-Cliff MSE `0.41681673` (**`-16.2911%` relative reduction**).
   - **30-Benchmark Universal Sweep (`claim/moleculeace_30_sweep_manifest.json`, Partial Win `p3`):**
     * **Strict Wins vs Live Polaris Leaderboard Best MSE:** **`29 / 30`** benchmarks.
     * **Simultaneous Wins with at least 5% Relative Margin vs Polaris + at least 95% Paired Bootstrap + Strictly Below Paper Best MSE:** **`21 / 30`** benchmarks (more than double `p3`'s 10/30 requirement).
     * **Strict Wins vs MoleculeACE Paper Best Overall MSE (re-derived across all 24 methods in `claim/MoleculeACE_results.csv`):** **`28 / 30`** benchmarks.
     * **Strict Wins vs MoleculeACE Paper Best Cliff MSE (`cliff_mol == 1`):** **`21 / 30`** benchmarks.
     * **Macro-Average RMSE across all 30 targets:** **`0.6303`** overall (`Macro MSE = 0.4020`), **`0.7211`** activity-cliff (`Macro Cliff MSE = 0.5298`), and **`0.5797`** non-cliff.

4. **Negative Controls:**
   - Predicting the constant training mean on `CHEMBL287_Ki` yields Test MSE = `1.098933` (and test mean yields `1.0980`), which is strictly worse than Polaris best `0.50318131` and is rejected by the checker.
   - Across `400` random permutations of `y_pred_clss` on `CHEMBL287_Ki` (`seed=42`), the minimum permuted MSE is `1.493204` (`mean = 1.759092`), with `0 / 400` permutations beating Polaris best (`z = -13.61`).

---

## 3. Code Audit & Double End-to-End Retraining Determinism Check

After completing my independent checker, I inspected `claim/author_checker_moleculeace.py` and `claim/run_clss_moleculeace.py`:

1. **Zero Test-Label Leakage & Strict Train-Only Fitting:**
   - In `claim/run_clss_moleculeace.py` (`run_single_dataset`, lines 500-514), `df` is split into `tr_df` (`split == 'train'`) and `te_df` (`split == 'test'`), any training molecule whose `InChIKey[:14]` appears in `te_ik14` is removed (`tr_clean_df`), and `fit_predict_clss_universal(views_tr, y_tr, views_te)` is invoked without `y_te` or `cliff_te` even being passed as arguments.
   - Inside `extract_fast_views(smiles_list)` (lines 62-183), every molecule is featurized independently row-by-row with zero cross-molecule statistics.
   - Inside `fit_predict_clss_universal` (lines 312-495), `StandardScaler` on `physchem` (lines 232 and 331), closed-form LOO KRR eigendecompositions `np.linalg.eigh(K_tr)` (line 200), 5-fold Stratified OOF (`StratifiedKFold(n_splits=5, shuffle=True, random_state=42)`) for precomputed `SVR`, `LGBMRegressor`, and `ExtraTreesRegressor` (lines 392-451), the Stage 2 MMP directional difference ridge operator `beta_diff` on training pairs (lines 246-275), the Stage 3 `QuantileTransformer` on `desc215` (line 479), and all three `SLSQP` simplex stacking weight vectors (`w_stage1`, `w_stage2`, `w_stage3`) are fit strictly on `views_tr` and `y_tr`.

2. **Double End-to-End CPU Retraining Verification on `CHEMBL287_Ki`:**
   - I executed `claim/author_checker_moleculeace.py --retrain CHEMBL287_Ki` twice from scratch on CPU:
     * **Run 1 (`52.2s` retrain):** `CHEMBL287_Ki | Pol=0.5032 Pap=0.5101 to CLSS=0.408021 | Cliff: Pap=0.6188 to 0.502136`, with `max |y_retrained - y_saved| = 4.441e-16` (at IEEE-754 float64 machine epsilon, well below `1e-10`).
     * **Run 2 (`43.6s` retrain):** `CHEMBL287_Ki | Pol=0.5032 Pap=0.5101 to CLSS=0.408021 | Cliff: Pap=0.6188 to 0.502136`, with `max |y_retrained - y_saved| = 4.441e-16` (`0.0` drift between Run 1 and Run 2).

All scratch files (`panel/reproduce_work`) and Python cache directories were removed after verification.

pass: true
