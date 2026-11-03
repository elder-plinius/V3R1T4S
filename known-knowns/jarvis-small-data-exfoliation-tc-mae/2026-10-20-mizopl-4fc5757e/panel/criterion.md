# Panelist Review — CRITERION (`jarvis-small-data-exfoliation-tc-mae`)

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: jarvis-small-data-exfoliation-tc-mae

## 1. Clause-by-Clause Audit of `success_criterion`, `partial_wins` (`p1`, `p2`), and `verification_method`

### Clause (1) — Required Artifacts: Standard-Operator ONNX Models, Per-Material Feature CSVs, Training Script, and `jarvis_leaderboard` Prediction CSVs
- **Standard-Operator ONNX Models**:
  - `object/model_dft_3d_exfoliation_energy.onnx` (`14,286` bytes, `sha256: bc24f70e097f87e392982c46a2621ada98312a9798a41cd30b83a3e30cb6f67f`, ONNX opset 18, IR version 8).
  - `object/model_tinnet_N_ead.onnx` (`3,612` bytes, `sha256: ef9e306148bc05e9ca6b992ba2ebe31752fb6193a7d4f09847c0b3a1b6f5d8ef`, ONNX opset 18, IR version 8).
- **Per-Material Feature CSV Shards**: `object/features_dft_3d_exfoliation_energy_part1.csv`..`part28.csv` (`812` rows: `650` train, `81` val, `81` test) and `object/features_tinnet_N_ead_part1.csv`..`part11.csv` (`327` rows: `263` train, `32` val, `32` test), indexed with SHA-256 digests in `object/jarvis_clss_results_manifest.json` (`17,731` bytes, `sha256: dc4ce33b887b2d5cae714e324875968b229ea99fb33e8622a2d299ff24778f83`).
- **Training & Feature Engineering Scripts**: `how-we-built-it/featurize_physics_clss.py` (`34,242` bytes, `sha256: 3675beadd412c1ef37ca162519c30364e4d3b25990cd53ebf3719f5f1382798a`), `how-we-built-it/train_and_predict_jarvis_clss.py` (`8,456` bytes, `sha256: f2d2ea4a28ae67c27ee035f46cfa9c2f26cec1690b46c2b3aae257ce5343bb26`), and `how-we-built-it/author_checker_jarvis_clss.py` (`692` bytes, `sha256: 9bb3af40cf1c0398c1a5b9ff7b586574b50b88ebac472fafa8fcbb36c69ef179`).
- **Official `jarvis_leaderboard` Prediction CSVs & `.csv.zip` Submission Archives**:
  - `object/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv` (`3,012` bytes, `sha256: 79189386af5ae8c30bc79fb1f7bbc3839536a53616c1b5cb110471dd905a1c19`, `81` test rows with columns `id,target,prediction`) and `.csv.zip` (`1,395` bytes, `sha256: ae3e9da2a4346116d9ea43fffead59bf67bb53bb948a5094fc23381e1432f6ac`).
  - `object/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv` (`1,159` bytes, `sha256: 1328eea4abc72755830ac8d1c848a0e01564aa16ccc0b603941b26d94c4fa570`, `32` test rows with columns `id,target,prediction`) and `.csv.zip` (`662` bytes, `sha256: 8ffcfb46f7bd52a11428b8f6c8239e0eac367d7956e217701316169a09f17a67`).
- **Status**: **SATISFIED**.

### Clause (2) — Strict Zero-Leakage Split Hygiene & Zero-Contributor-Code Verification
- `verify-it-yourself/check_jarvis_clss_package.py` (`11,611` bytes, `sha256: b619aba27a43c9bf291f64a9b6c1c41752a6bfd022dab6845bd1c415dd54d875`) imports zero contributor code, verifies disjoint `train`, `val`, and `test` IDs across the feature CSV shards (`0` overlap), and evaluates `object/model_dft_3d_exfoliation_energy.onnx` and `object/model_tinnet_N_ead.onnx` directly via `onnxruntime.InferenceSession`, matching the submitted prediction CSVs within `4.87e-09` and `4.83e-09`.
- **Status**: **SATISFIED**.

### Clause (3) — Primary Benchmark (`dft_3d_exfoliation_energy`): Relative Margin (at least 5%) and 1,000-Sample Bootstrap 90% CI Half-Width Gate
- **Live Leaderboard Best**: `matminer_xgboost` = `40.88700 meV/atom` (upstream archive `sha256: e89262451215f98da0eddf327a082787461edfa5f73426baf6c4fd745acacb78`); second-best `matminer_rf` = `42.75540 meV/atom`.
- **Claimed Test MAE (`sklearn.metrics.mean_absolute_error`)**: **`28.195924 meV/atom`**.
- **Relative MAE Reduction**: **`-31.0394%`** below `matminer_xgboost`, exceeding the `5.0%` threshold.
- **Absolute MAE Reduction vs 1,000-Sample Bootstrap 90% CI Half-Width**:
  - Absolute gain: `+12.691076 meV/atom`.
  - 1,000-sample bootstrap 90% CI (`seed=0`): `[18.510812, 40.775969] meV/atom`, half-width `h90 = 11.132579 meV/atom` (maximum across seeds `0..9` is `11.449430 meV/atom`).
  - Gate verification: `12.691076 meV/atom` strictly exceeds `11.132579 meV/atom` (`MAE + h90 = 39.328502 meV/atom < 40.88700 meV/atom`).
- **Status**: **SATISFIED**.

### Clause (4) — Enumerated Partial Win `p1` (`tinnet_N_ead`)
- **Task Eligibility**: Named in `how-we-built-it/PREREG.md`, contains `327` total materials (`295` in `train U val` and `32` in `test`, `< 2,000` materials), and has `13` entries on the live leaderboard ($\ge 3$ required), led by `alignn_model = 0.08710 eV` (upstream archive `sha256: 5bc9f63e3016343afc3a5719611ec9335442305a5d752fd5c44fb66ff857ac59`).
- **Claimed Test MAE**: **`0.068908 eV`** (`-20.8865%` below `0.08710 eV`).
- **Absolute MAE Reduction vs 1,000-Sample Bootstrap 90% CI Half-Width**:
  - Absolute gain: `+0.018192 eV` > `h90 = 0.017247 eV` (`MAE + h90 = 0.086155 eV < 0.08710 eV`).
- **Status**: **SATISFIED (`p1`)**.

### Clause (5) — Enumerated Partial Win `p2` (5-Fold CV Paired Study on `train U val` vs Reproduced `matminer_xgboost`)
- Published in `object/cv5_oof_dft_3d_exfoliation_energy.csv` (`sha256: d3a94e8543c3c3443424dd75d2b2dca17aa43b4bd15320695925ecbb833e2f64`) and `object/cv5_oof_tinnet_N_ead.csv` (`sha256: 104b07f6c20bf883001ba4567df85bc232de8d30c17077f7bac26a362d8c8b63`):
  - `dft_3d_exfoliation_energy` (`n = 731`): CLSS 5-fold OOF MAE = `32.672745 meV/atom` (LOO = `31.805270 meV/atom`) vs reproduced `matminer_xgboost` OOF MAE = `45.004627 meV/atom` (`-27.40%`, Wilcoxon `p = 1.6160e-18`, paired t-test `p = 1.8647e-14`).
  - `tinnet_N_ead` (`n = 295`): CLSS 5-fold OOF MAE = `0.095629 eV` (LOO = `0.085702 eV`) vs reproduced `matminer_xgboost` OOF MAE = `0.165561 eV` (`-42.24%`, Wilcoxon `p = 5.8606e-15`, paired t-test `p = 2.9225e-15`).
- **Status**: **SATISFIED (`p2`)**.

confirmed_scope: Structure-only physics-informed CLSS kernel models trained strictly on official train U val IDs with zero label leakage and exported as standard-operator ONNX graphs (object/model_dft_3d_exfoliation_energy.onnx, sha256 bc24f70e097f87e392982c46a2621ada98312a9798a41cd30b83a3e30cb6f67f; object/model_tinnet_N_ead.onnx, sha256 ef9e306148bc05e9ca6b992ba2ebe31752fb6193a7d4f09847c0b3a1b6f5d8ef) evaluated directly by onnxruntime on shipped per-material feature CSV shards (object/jarvis_clss_results_manifest.json, sha256 dc4ce33b887b2d5cae714e324875968b229ea99fb33e8622a2d299ff24778f83) achieve official test MAE = 28.195924 meV/atom on dft_3d_exfoliation_energy (object/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv, sha256 79189386af5ae8c30bc79fb1f7bbc3839536a53616c1b5cb110471dd905a1c19, -31.04% below live best matminer_xgboost 40.887 meV/atom, gain +12.691076 meV/atom exceeding 1,000-sample bootstrap 90% CI half-width h90 = 11.132579 meV/atom) and test MAE = 0.068908 eV on the preregistered p1 task tinnet_N_ead (N = 327 materials, object/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv, sha256 1328eea4abc72755830ac8d1c848a0e01564aa16ccc0b603941b26d94c4fa570, -20.89% below live best alignn_model 0.0871 eV, gain +0.018192 eV exceeding h90 = 0.017247 eV), together with 5-fold cross-validation paired superiority over reproduced matminer_xgboost on train U val across both benchmarks (Wilcoxon p = 1.62e-18 and 5.86e-15, p2).
pass: true
