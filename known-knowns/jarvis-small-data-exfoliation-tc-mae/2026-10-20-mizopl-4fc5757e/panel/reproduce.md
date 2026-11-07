# Skeptic Panel Report — Role: REPRODUCE

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target_id: jarvis-small-data-exfoliation-tc-mae

## 1. Quoted Definition & Success Criterion

- **`success_criterion`:**
  "Trained model, training script and predictions file (`jarvis_leaderboard` CSV format) for `dft_3d_exfoliation_energy` or `dft_3d_Tc_supercon` such that test MAE on the official `test` IDs is strictly lower than the best MAE on the live leaderboard page (`1.9989 K` or `40.887 meV/atom`, or whatever is best at verification time) by at least 5% relative and by more than the half-width of a 1,000-sample bootstrap 90% confidence interval of the claimed model's MAE, trained on the official `train`+`val` IDs, and deterministically reproducible by re-running the saved model."
- **Enumerated `partial_wins`:**
  - **`p1` (Dropped):** Requires a task named before the run starts; because `how-we-built-it/PREREG.md` was written retrospectively on `2026-11-03` and has been removed, `p1` credit on `tinnet_N_ead` is dropped (`tinnet_N_ead` is retained in `object/` as an uncredited supplementary evaluation).
  - **`p2` (Claimed):** "5-fold CV study on `train`+`val` showing the claimed model's advantage over a reproduced `matminer_xgboost` baseline with a paired test, published with the predictions"

---

## 2. Independent Zero-Contributor-Code Verification (`verify-it-yourself/check_jarvis_clss_package.py`)

`verify-it-yourself/check_jarvis_clss_package.py` (`13,726` bytes, `sha256: 0183cfe775ca0cc9d8a0f2fbfcc6c18944d31bff0d9e293f469b4ed189afadd3`) imports zero contributor code and verifies:

### 2.1 Saved Artifact Integrity (Byte Sizes and SHA-256 Digests)

| Relative File Path | Verified Size (Bytes) | Verified SHA-256 Digest |
| :--- | ---: | :--- |
| `object/jarvis_clss_results_manifest.json` | `18,229` | `cfaa8987d6f3c03197247f4b2695f24100ec166623b09ca71fc7c7238a194eed` |
| `object/model_dft_3d_exfoliation_energy.onnx` | `14,286` | `bc24f70e097f87e392982c46a2621ada98312a9798a41cd30b83a3e30cb6f67f` |
| `object/model_tinnet_N_ead.onnx` | `3,612` | `ef9e306148bc05e9ca6b992ba2ebe31752fb6193a7d4f09847c0b3a1b6f5d8ef` |
| `object/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv` | `1,934` | `10169820be31c96ecdb8f2a08877dcdb1296ba62afabb43afaec59e259a44f82` |
| `object/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv` | `735` | `707e335f234b093a52fbebda8c649bea30adb40d569753f340a0254a6dd75b6b` |
| `object/cv5_oof_dft_3d_exfoliation_energy.csv` | `45,178` | `d3a94e8543c3c3443424dd75d2b2dca17aa43b4bd15320695925ecbb833e2f64` |
| `object/cv5_oof_tinnet_N_ead.csv` | `17,669` | `104b07f6c20bf883001ba4567df85bc232de8d30c17077f7bac26a362d8c8b63` |
| `how-we-built-it/featurize_physics_clss.py` | `34,242` | `3675beadd412c1ef37ca162519c30364e4d3b25990cd53ebf3719f5f1382798a` |
| `how-we-built-it/train_and_predict_jarvis_clss.py` | `35,367` | `7c456ccf602ac5ac8efe9faa8276d1bd26cb41f6f4e108ad740d7d287eb4b806` |
| `how-we-built-it/author_checker_jarvis_clss.py` | `722` | `4e6ab5f8dfdb3796fdc48c83438d59edee836974e537066918547fe70814609c` |

### 2.2 Independent Split Hygiene & Standard-Operator ONNX Evaluation
- **`dft_3d_exfoliation_energy` (Claimed Primary)**: `650` train + `81` val = `731` `train U val` IDs (`X_support` shape `[731, 1807]`), `81` `test` IDs (`X_eval` shape `[81, 1807]`, `812` total across `object/features_dft_3d_exfoliation_energy_part1.csv`..`part28.csv`). Overlap between `train U val` and `test` IDs = `0`. Evaluating `object/model_dft_3d_exfoliation_energy.onnx` via `onnxruntime.InferenceSession` (`sess.run(["prediction"], {"X_eval": X_te, "X_support": X_tv})`) reproduces `object/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv` (`id,prediction`) with `max |diff| = 4.87e-09`.
- **`tinnet_N_ead` (Uncredited Supplementary)**: `263` train + `32` val = `295` `train U val` IDs (`X_support` shape `[295, 2186]`), `32` `test` IDs (`X_eval` shape `[32, 2186]`, `327` total across `object/features_tinnet_N_ead_part1.csv`..`part11.csv`). Overlap between `train U val` and `test` IDs = `0`. Evaluating `object/model_tinnet_N_ead.onnx` via `onnxruntime.InferenceSession` reproduces `object/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv` (`id,prediction`) with `max |diff| = 4.83e-09`.

### 2.3 Independent Test MAE & 1,000-Sample 90% Bootstrap CI Verification

| Task | Live Best MAE | Verified Test MAE | Relative Reduction ($\ge 5\%$ req.) | Absolute Gain $\Delta\text{MAE}$ | Bootstrap $h_{90\%}$ (`seed=0`) | Max $h_{90\%}$ (`seeds 0..9`) | Upper Bound $\text{MAE} + h_{90\%}$ vs Live Best | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `dft_3d_exfoliation_energy` | `40.88700 meV/atom` (`matminer_xgboost`) | **`28.195924 meV/atom`** | **`-31.0394%`** | **`+12.691076 meV/atom`** | **`11.132579 meV/atom`** | `11.449430 meV/atom` | `39.328502` vs `40.88700 meV/atom` | **PASS (Claimed Primary + `p2`)** |
| `tinnet_N_ead` | `0.08710 eV` (`alignn_model`) | **`0.068908 eV`** | **`-20.8865%`** | **`+0.018192 eV`** | **`0.017247 eV`** | `0.017247 eV` | `0.086155 eV` vs `0.08710 eV` | **Supplementary (`p1` Dropped)** |

pass: true
