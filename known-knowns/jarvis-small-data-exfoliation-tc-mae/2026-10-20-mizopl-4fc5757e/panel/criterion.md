# Panelist Review — CRITERION (`jarvis-small-data-exfoliation-tc-mae`)

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: jarvis-small-data-exfoliation-tc-mae

## 1. Clause-by-Clause Audit of `success_criterion`, `partial_wins` (`p1`, `p2`), and `verification_method`

### Clause (1) — Required Artifacts: Trained Model, Training Script, and `jarvis_leaderboard` Prediction CSVs
- **Trained Model Archive**: `claim/trained_models_jarvis_clss.npz` exists (`55,014` bytes, `sha256: 4fc5757ef96c86ab1361ac488a5ee376e5aeea57b29c03afa5befa1b54b21489`), storing all dual kernel weights (`alpha_p`, `alpha_base`, `alpha_r`, `alpha`), LOO-selected physics gates (`c_hom = 0.75`, `w_r = 0.80`), out-of-fold predictions, and official test predictions.
- **Training & Feature Engineering Scripts**: `claim/train_and_predict_jarvis_clss.py` (`30,043` bytes, `sha256: 907e5b94119f5983d6a89f17f4c3fe5827e5260145bc4f11c5e9b292ebdb9450`), `claim/featurize_physics_clss.py` (`37,185` bytes, `sha256: 67b7872f5c6470446659e356ac9e1e955b642cb849968a64517758f8a5e266d5`), and `claim/author_checker_jarvis_clss.py` (`13,955` bytes, `sha256: f8ba2764f0c05db80791c25e1e48d2b6c22f4d14a9923f81bdbf0e0e74db2f75`).
- **Official `jarvis_leaderboard` Prediction CSVs & `.csv.zip` Submission Archives**:
  - `claim/AI-SinglePropertyPrediction-Tc_supercon-dft_3d-test-mae.csv` (`1,076` bytes, `sha256: 6fa908bbd746495ee5dc1808fa483cd83106c932b5a0a2097fdf35b38df98ae2`, `30` test rows with columns `id,target,prediction`) and `.csv.zip` (`628` bytes, `sha256: ac07d1423cb6ea587cb037b7555a8ce42c874b148b0af086f118bc4d576fdd32`).
  - `claim/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv` (`3,012` bytes, `sha256: 79189386af5ae8c30bc79fb1f7bbc3839536a53616c1b5cb110471dd905a1c19`, `81` test rows with columns `id,target,prediction`) and `.csv.zip` (`1,395` bytes, `sha256: ae3e9da2a4346116d9ea43fffead59bf67bb53bb948a5094fc23381e1432f6ac`).
  - `claim/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv` (`1,159` bytes, `sha256: 1328eea4abc72755830ac8d1c848a0e01564aa16ccc0b603941b26d94c4fa570`, `32` test rows with columns `id,target,prediction`) and `.csv.zip` (`662` bytes, `sha256: 8ffcfb46f7bd52a11428b8f6c8239e0eac367d7956e217701316169a09f17a67`).
- **Status**: **SATISFIED**.

### Clause (2) — Strict Zero-Leakage Split Hygiene & Structure-Only Input Audit
- Direct comparison of the official `jarvis_leaderboard` benchmark split archives (`claim/data/dft_3d_Tc_supercon.json.zip`, `sha256: e34fe109057b9dd7b4ae50b18fdec70cc156b6a994a02ec6f57f5c365f8a06dc`; `claim/data/dft_3d_exfoliation_energy.json.zip`, `sha256: d7a3127002098c3da40292bee8d78de0e45ca42bef81adc73a07bc47e900a9a4`; `claim/data/tinnet_N_ead.json.zip`, `sha256: 14da9466b46ccd69aea116c6d6ef456da2c2cfe955b45b89105bb9f21acdfc49`) against `claim/data/clean_structures/*_structures.json.gz` confirms exact split identity and zero overlap:
  - `dft_3d_Tc_supercon`: `n_train = 556`, `n_val = 30` (`n_train_val = 586`), `n_test = 30`, `(set(train) | set(val)) & set(test) == set()` (`0` overlap).
  - `dft_3d_exfoliation_energy`: `n_train = 650`, `n_val = 81` (`n_train_val = 731`), `n_test = 81`, `(set(train) | set(val)) & set(test) == set()` (`0` overlap).
  - `tinnet_N_ead`: `n_train = 263`, `n_val = 32` (`n_train_val = 295`), `n_test = 32`, `(set(train) | set(val)) & set(test) == set()` (`0` overlap).
- Every crystal structure dictionary across all `616 + 812 + 327 = 1,755` entries contains strictly the 4 geometric/chemical keys `['cartesian', 'coords', 'elements', 'lattice_mat']`, with zero DFT electronic, elastic, or target metadata.
- Inside `fit_predict_tc_supercon`, `fit_predict_exfoliation`, and `fit_predict_tinnet`, `QuantileTransformer` and kernel matrices are fitted strictly on `X_tr`, and blending weights (`c_hom = 0.75` on `dft_3d_Tc_supercon`, `w_r = 0.80` on `dft_3d_exfoliation_energy`) are selected automatically by minimizing analytical leave-one-out (`LOO`) MAE strictly on `(X_tr, y_tr)` prior to reading `X_ev`. Pointwise inductive evaluation (`X_te[:1]`) matches batch test evaluation within `4.4e-15` (`dft_3d_Tc_supercon`), `4.3e-14` (`dft_3d_exfoliation_energy`), and `3.6e-15` (`tinnet_N_ead`), and re-running training from scratch reproduces `claim/trained_models_jarvis_clss.npz` with `max |retrain - npz| == 0.0`.
- **Status**: **SATISFIED**.

### Clause (3) — Primary Benchmarks: Relative Margin (at least 5%) and 1,000-Sample Bootstrap 90% CI Half-Width Gate
Although the verbatim `success_criterion` requires solving `dft_3d_exfoliation_energy` **or** `dft_3d_Tc_supercon`, the claimed submission solves **both** primary tasks simultaneously:

1. **`dft_3d_Tc_supercon` (`AI-SinglePropertyPrediction-Tc_supercon-dft_3d-test-mae`, `n_test = 30`)**:
   - **Live Leaderboard Best**: `atomgpt_model` = `1.51870 K` (verified from `claim/data/leaderboard_baselines/tc_atomgpt.csv.zip`: `1.518733 K`); second-best `cfid` = `1.99890 K` (target description reference).
   - **Claimed Test MAE (`sklearn.metrics.mean_absolute_error`)**: **`0.902806 K`**.
   - **Relative MAE Reduction**: **`-40.5540%`** below `atomgpt_model` (`-54.8349%` below `cfid = 1.9989 K`), far exceeding the `5.0%` threshold.
   - **Absolute MAE Reduction vs 1,000-Sample Bootstrap 90% CI Half-Width**:
     - Absolute gain: `+0.615894 K`.
     - 1,000-sample bootstrap 90% CI (`seed=0`): `[0.548054, 1.283978] K`, half-width `h90 = 0.367962 K` (maximum across seeds `0..9` is `0.367962 K`).
     - Gate verification: `0.615894 K` strictly exceeds `0.367962 K` (`MAE + h90 = 1.270768 K`, strictly below `1.51870 K`).

2. **`dft_3d_exfoliation_energy` (`AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae`, `n_test = 81`)**:
   - **Live Leaderboard Best**: `matminer_xgboost` = `40.88700 meV/atom` (verified from `claim/data/leaderboard_baselines/exf_matminer_xgb.csv.zip`: `40.887046 meV/atom`); second-best `matminer_rf` = `42.75540 meV/atom`.
   - **Claimed Test MAE (`sklearn.metrics.mean_absolute_error`)**: **`28.195924 meV/atom`**.
   - **Relative MAE Reduction**: **`-31.0394%`** below `matminer_xgboost` (`-34.0530%` below `matminer_rf`), far exceeding the `5.0%` threshold.
   - **Absolute MAE Reduction vs 1,000-Sample Bootstrap 90% CI Half-Width**:
     - Absolute gain: `+12.691076 meV/atom`.
     - 1,000-sample bootstrap 90% CI (`seed=0`): `[18.510812, 40.775969] meV/atom`, half-width `h90 = 11.132579 meV/atom` (maximum across seeds `0..9` is `11.449430 meV/atom`, which also strictly satisfies `12.691076` exceeding `11.449430`).
     - Gate verification: `12.691076 meV/atom` strictly exceeds `11.132579 meV/atom` (`MAE + h90 = 39.328502 meV/atom`, strictly below `40.88700 meV/atom`).
- **Status**: **SATISFIED ON BOTH PRIMARY BENCHMARKS**.

### Clause (4) — Enumerated Partial Win `p1` (`tinnet_N_ead`)
- **Task Eligibility**: `tinnet_N_ead` (`AI-SinglePropertyPrediction-ead-tinnet_N-test-mae`) was named before the run started, contains `327` total materials (`295` in `train U val` and `32` in `test`, strictly fewer than `2,000` materials), and has `6` entries on the live leaderboard (at least `3` required), led by `alignn = 0.08710 eV` (verified from `claim/data/leaderboard_baselines/tinnet_N_alignn.csv.zip`: `0.087055 eV`) and `matminer_xgboost = 0.17120 eV`.
- **Claimed Test MAE**: **`0.068908 eV`**.
- **Relative MAE Reduction**: **`-20.8865%`** below `alignn = 0.08710 eV` (`-59.7501%` below `matminer_xgboost = 0.17120 eV`), exceeding the `5.0%` threshold.
- **Absolute MAE Reduction vs 1,000-Sample Bootstrap 90% CI Half-Width**:
  - Absolute gain: `+0.018192 eV`.
  - 1,000-sample bootstrap 90% CI (`seed=0`): `[0.052454, 0.086948] eV`, half-width `h90 = 0.017247 eV` (maximum across seeds `0..9` is `0.017247 eV`).
  - Gate verification: `0.018192 eV` strictly exceeds `0.017247 eV` (`MAE + h90 = 0.086155 eV`, strictly below `0.08710 eV`).
- **Status**: **SATISFIED (`p1`)**.

### Clause (5) — Enumerated Partial Win `p2` (5-Fold CV Paired Study on `train U val` vs Reproduced `matminer_xgboost`)
- Out-of-fold 5-fold cross-validation (`KFold(n_splits=5, shuffle=True, random_state=42)`) and analytical LOO predictions on `train U val` are published in `claim/cv5_oof_dft_3d_Tc_supercon.csv`, `claim/cv5_oof_dft_3d_exfoliation_energy.csv`, and `claim/cv5_oof_tinnet_N_ead.csv`:
  - `dft_3d_Tc_supercon` (`n = 586`): CLSS 5-fold OOF MAE = `1.984094 K` (analytical LOO MAE = `1.885324 K`) vs reproduced `matminer_xgboost` OOF MAE = `2.368224 K` (`-16.22%` 5-fold reduction, `-20.39%` LOO reduction; 1-sided paired Wilcoxon `p = 5.9901e-09`, paired t-test `p = 4.5807e-05`, 10,000-bootstrap win rate = `99.99%`).
  - `dft_3d_exfoliation_energy` (`n = 731`): CLSS 5-fold OOF MAE = `32.672745 meV/atom` (analytical LOO MAE = `31.805270 meV/atom`) vs reproduced `matminer_xgboost` OOF MAE = `45.004627 meV/atom` (`-27.40%` 5-fold reduction, `-29.33%` LOO reduction; 1-sided paired Wilcoxon `p = 1.6160e-18`, paired t-test `p = 1.8647e-14`, 10,000-bootstrap win rate = `100.00%`).
  - `tinnet_N_ead` (`n = 295`): CLSS 5-fold OOF MAE = `0.095629 eV` (analytical LOO MAE = `0.085702 eV`) vs reproduced `matminer_xgboost` OOF MAE = `0.165561 eV` (`-42.24%` 5-fold reduction, `-48.24%` LOO reduction; 1-sided paired Wilcoxon `p = 5.8606e-15`, paired t-test `p = 2.9225e-15`, 10,000-bootstrap win rate = `100.00%`).
- **Status**: **SATISFIED (`p2`)**.

## 2. Null Models & Physics-Module Ablation Controls

- **Constant Dummy Predictors**:
  - Train-mean predictor fails on all 3 tasks: `2.74354 K` (exceeding `1.51870 K`), `60.27569 meV/atom` (exceeding `40.88700 meV/atom`), and `0.43263 eV` (exceeding `0.08710 eV`).
  - Train-median predictor upper bound `MAE + h90` fails on all 3 tasks: `2.42035 K`, `68.75949 meV/atom`, and `0.53709 eV`.
- **400-Sample Training-Label Permutation Controls**:
  - `dft_3d_Tc_supercon`: null MAE = `2.0504 +/- 0.2816 K` (`min = 1.4471 K`, `0 / 400` permutations reaching `0.902806 K`, `z = -4.08`, `p = 0.00249`).
  - `dft_3d_exfoliation_energy`: null MAE = `62.3599 +/- 4.0929 meV/atom` (`min = 53.3428 meV/atom`, `0 / 400` permutations reaching `28.195924 meV/atom`, `z = -8.35`, `p = 0.00249`).
  - `tinnet_N_ead`: null MAE = `0.6760 +/- 0.0810 eV` (`min = 0.4541 eV`, `0 / 400` permutations reaching `0.068908 eV`, `z = -7.49`, `p = 0.00249`).
- **Component Ablation Controls**:
  - Ablating the Single-Site Isoelectronic Homolog kernel on `dft_3d_Tc_supercon` (`c_hom = 0`) causes the error on A15 superconductor `JVASP-14960` (`V3Si`, true `Tc = 17.6330 K`) to jump from `4.4608 K` (pure homolog `Nb3Si` error `1.1330 K`) to `14.4473 K`, degrading Test MAE to `1.228082 K` and inflating `h90` to `0.787078 K` (`MAE + h90 = 2.015160 K`, failing the `1.51870 K` bootstrap CI gate).
  - Ablating the Griffith 3D-Covalent Fracture kernel on `dft_3d_exfoliation_energy` (`w_r = 0`) degrades LOO MAE from `31.805270` to `32.724774 meV/atom`, degrades Test MAE to `30.402496 meV/atom`, and inflates `h90` to `13.220252 meV/atom` (`MAE + h90 = 43.622747 meV/atom`, failing the `40.88700 meV/atom` bootstrap CI gate).
  - Ablating the Hammer-Norskov Adsorbate-Centered Canonical Slab descriptor on `tinnet_N_ead` (`S = 0`) degrades LOO MAE from `0.085702` to `0.124532 eV`, degrades Test MAE to `0.083625 eV` (`-3.99%` relative reduction, failing the `5.0%` margin), and inflates `h90` to `0.024248 eV` (`MAE + h90 = 0.107873 eV`, failing the `0.08710 eV` bootstrap CI gate).

confirmed_scope: Structure-only physics-informed CLSS kernel models trained strictly on official train U val IDs with zero label leakage (claim/trained_models_jarvis_clss.npz, sha256 4fc5757ef96c86ab1361ac488a5ee376e5aeea57b29c03afa5befa1b54b21489) achieve official test MAE = 0.902806 K on dft_3d_Tc_supercon (claim/AI-SinglePropertyPrediction-Tc_supercon-dft_3d-test-mae.csv, -40.55% below live best atomgpt_model 1.5187 K and -54.83% below cfid 1.9989 K, gain +0.615894 K exceeding 1,000-sample bootstrap 90% CI half-width h90 = 0.367962 K), test MAE = 28.195924 meV/atom on dft_3d_exfoliation_energy (claim/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv, -31.04% below live best matminer_xgboost 40.887 meV/atom, gain +12.691076 meV/atom exceeding h90 = 11.132579 meV/atom), and test MAE = 0.068908 eV on the preregistered p1 task tinnet_N_ead (N = 327 materials, claim/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv, -20.89% below live best alignn 0.0871 eV, gain +0.018192 eV exceeding h90 = 0.017247 eV), together with 5-fold cross-validation paired superiority over reproduced matminer_xgboost on train U val across all three benchmarks (Wilcoxon p = 5.99e-09, 1.62e-18, and 5.86e-15, p2).
pass: true
