# Panelist Review — CRITERION (`jarvis-small-data-exfoliation-tc-mae`)

role: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: jarvis-small-data-exfoliation-tc-mae

## 1. Clause-by-Clause Audit of `success_criterion`, `partial_wins` (`p2`), and `verification_method`

### Clause (1) — Required Artifacts: Standard-Operator ONNX Models, Per-Material Feature CSVs, Complete Training Script, and `jarvis_leaderboard` Prediction CSVs (`id,prediction`)
- **Standard-Operator ONNX Models**:
  - `object/model_dft_3d_exfoliation_energy.onnx` (`14,286` bytes, `sha256: bc24f70e097f87e392982c46a2621ada98312a9798a41cd30b83a3e30cb6f67f`, ONNX opset 18, IR version 8, named inputs `X_eval` and `X_support`, named output `prediction`).
  - `object/model_tinnet_N_ead.onnx` (`3,612` bytes, `sha256: ef9e306148bc05e9ca6b992ba2ebe31752fb6193a7d4f09847c0b3a1b6f5d8ef`, ONNX opset 18, IR version 8, named inputs `X_eval` and `X_support`, named output `prediction`).
- **Per-Material Feature CSV Shards**: `object/features_dft_3d_exfoliation_energy_part1.csv`..`part28.csv` (`812` rows: `650` train, `81` val, `81` test) and `object/features_tinnet_N_ead_part1.csv`..`part11.csv` (`327` rows: `263` train, `32` val, `32` test), indexed with SHA-256 digests in `object/jarvis_clss_results_manifest.json` (`18,229` bytes, `sha256: cfaa8987d6f3c03197247f4b2695f24100ec166623b09ca71fc7c7238a194eed`).
- **Complete Training & Feature Engineering Scripts**: `how-we-built-it/featurize_physics_clss.py` (`34,242` bytes, `sha256: 3675beadd412c1ef37ca162519c30364e4d3b25990cd53ebf3719f5f1382798a`), `how-we-built-it/train_and_predict_jarvis_clss.py` (`35,367` bytes, `sha256: 7c456ccf602ac5ac8efe9faa8276d1bd26cb41f6f4e108ad740d7d287eb4b806`), and `how-we-built-it/author_checker_jarvis_clss.py` (`722` bytes, `sha256: 4e6ab5f8dfdb3796fdc48c83438d59edee836974e537066918547fe70814609c`).
- **Official `jarvis_leaderboard` Prediction CSVs (`id,prediction` only, no `.csv.zip` copies)**:
  - `object/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv` (`1,934` bytes, `sha256: 10169820be31c96ecdb8f2a08877dcdb1296ba62afabb43afaec59e259a44f82`, `81` test rows with exact columns `id,prediction`).
  - `object/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv` (`735` bytes, `sha256: 707e335f234b093a52fbebda8c649bea30adb40d569753f340a0254a6dd75b6b`, `32` test rows with exact columns `id,prediction`, uncredited supplementary).
- **Status**: **SATISFIED**.

### Clause (2) — Disjoint Split Hygiene & Zero-Contributor-Code Verification
- `verify-it-yourself/check_jarvis_clss_package.py` (`13,726` bytes, `sha256: 0183cfe775ca0cc9d8a0f2fbfcc6c18944d31bff0d9e293f469b4ed189afadd3`) imports zero contributor code, verifies disjoint `train`, `val`, and `test` IDs across the feature CSV shards (`0` overlap) and against the official upstream benchmark archives (`dft_3d_exfoliation_energy.json.zip`, `sha256: d7a3127002098c3da40292bee8d78de0e45ca42bef81adc73a07bc47e900a9a4`; `tinnet_N_ead.json.zip`, `sha256: 14da9466b46ccd69aea116c6d6ef456da2c2cfe955b45b89105bb9f21acdfc49`), and evaluates `object/model_dft_3d_exfoliation_energy.onnx` and `object/model_tinnet_N_ead.onnx` directly via `onnxruntime.InferenceSession` on inputs `{"X_eval": X_te, "X_support": X_tv}` -> `["prediction"]`, matching the submitted `id,prediction` CSVs within `4.87e-09` and `4.83e-09`.
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

### Clause (4) — Dropped `p1` Credit (`tinnet_N_ead` Retained as Uncredited Supplementary Artifact)
- Because `how-we-built-it/PREREG.md` was written retrospectively on `2026-11-03` during commit `ed4d4dd` (and has been removed), and no git-committed file dated before the `2026-10-20` run exists to name `tinnet_N_ead` before the run started, `p1` credit is dropped. The `tinnet_N_ead` ONNX model (`3,612` bytes, `sha256: ef9e306148bc05e9ca6b992ba2ebe31752fb6193a7d4f09847c0b3a1b6f5d8ef`) and `id,prediction` CSV (`sha256: 707e335f234b093a52fbebda8c649bea30adb40d569753f340a0254a6dd75b6b`, Test MAE = `0.068908 eV` vs `alignn_model = 0.08710 eV`, $h_{90\%} = 0.017247\text{ eV}$) are retained as an uncredited supplementary evaluation.

### Clause (5) — Enumerated Partial Win `p2` (5-Fold CV Paired Study on `train U val` vs Reproduced `matminer_xgboost`)
- Published in `object/cv5_oof_dft_3d_exfoliation_energy.csv` (`sha256: d3a94e8543c3c3443424dd75d2b2dca17aa43b4bd15320695925ecbb833e2f64`) and `object/cv5_oof_tinnet_N_ead.csv` (`sha256: 104b07f6c20bf883001ba4567df85bc232de8d30c17077f7bac26a362d8c8b63`):
  - `dft_3d_exfoliation_energy` (`n = 731`): CLSS 5-fold OOF MAE = `32.672745 meV/atom` (LOO = `31.805270 meV/atom`) vs reproduced `matminer_xgboost` OOF MAE = `45.004627 meV/atom` (`-27.40%`, Wilcoxon `p = 1.6160e-18`, paired t-test `p = 1.8647e-14`).
  - `tinnet_N_ead` (`n = 295`, supplementary): CLSS 5-fold OOF MAE = `0.095629 eV` (LOO = `0.085702 eV`) vs reproduced `matminer_xgboost` OOF MAE = `0.165561 eV` (`-42.24%`, Wilcoxon `p = 5.8606e-15`, paired t-test `p = 2.9225e-15`).
- **Status**: **SATISFIED (`p2`)**.

confirmed_scope: Structure-only physics-informed CLSS kernel models fitted on official train U val IDs from crystal structure inputs (lattice_mat, coords, elements, cartesian) with disjoint train/val/test ID splits and exported as a standard-operator ONNX graph (object/model_dft_3d_exfoliation_energy.onnx, 14,286 bytes, sha256 bc24f70e097f87e392982c46a2621ada98312a9798a41cd30b83a3e30cb6f67f, graph inputs X_eval and X_support, graph output prediction) evaluated directly by onnxruntime on shipped per-material feature CSV shards (object/jarvis_clss_results_manifest.json, sha256 cfaa8987d6f3c03197247f4b2695f24100ec166623b09ca71fc7c7238a194eed) achieve official test MAE = 28.195924 meV/atom on dft_3d_exfoliation_energy (object/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv, sha256 10169820be31c96ecdb8f2a08877dcdb1296ba62afabb43afaec59e259a44f82, -31.04% below live best matminer_xgboost 40.887 meV/atom, gain +12.691076 meV/atom exceeding 1,000-sample bootstrap 90% CI half-width h90 = 11.132579 meV/atom), together with 5-fold cross-validation paired superiority over reproduced matminer_xgboost on train U val (32.672745 vs 45.004627 meV/atom, Wilcoxon p = 1.62e-18, p2); an uncredited supplementary evaluation on tinnet_N_ead (object/model_tinnet_N_ead.onnx, 3,612 bytes, sha256 ef9e306148bc05e9ca6b992ba2ebe31752fb6193a7d4f09847c0b3a1b6f5d8ef; object/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv, sha256 707e335f234b093a52fbebda8c649bea30adb40d569753f340a0254a6dd75b6b, test MAE = 0.068908 eV vs 0.0871 eV, 5-fold CV Wilcoxon p = 5.86e-15) is included for completeness with p1 credit dropped.
pass: true
