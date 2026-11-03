# Skeptic Panel Report — Role: REPRODUCE

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target_id: jarvis-small-data-exfoliation-tc-mae

## 1. Quoted Definition & Success Criterion

- **`success_criterion`:**
  "Trained model, training script and predictions file (`jarvis_leaderboard` CSV format) for `dft_3d_exfoliation_energy` or `dft_3d_Tc_supercon` such that test MAE on the official `test` IDs is strictly lower than the best MAE on the live leaderboard page (`1.9989 K` or `40.887 meV/atom`, or whatever is best at verification time) by at least 5% relative and by more than the half-width of a 1,000-sample bootstrap 90% confidence interval of the claimed model's MAE, trained strictly on the official `train`+`val` IDs with no label leakage, and deterministically reproducible by re-running the training script."
- **Enumerated `partial_wins`:**
  - **`p1`:** "Same rules on one further small JARVIS AI single-property task (fewer than 2,000 materials, at least 3 entries on the leaderboard) named before the run starts" — `tinnet_N_ead` (`AI-SinglePropertyPrediction-ead-tinnet_N-test-mae`, $N = 327$, 13 entries on the live leaderboard, live best `alignn_model = 0.0871 eV`).
  - **`p2`:** "5-fold CV study on `train`+`val` showing the claimed model's advantage over a reproduced `matminer_xgboost` baseline with a paired test, published with the predictions"

---

## 2. Independent Zero-Contributor-Code Verification (`verify-it-yourself/check_jarvis_clss_package.py`)

`verify-it-yourself/check_jarvis_clss_package.py` (`11,611` bytes, `sha256: b619aba27a43c9bf291f64a9b6c1c41752a6bfd022dab6845bd1c415dd54d875`) imports zero contributor code and verifies:

### 2.1 Saved Artifact Integrity (Byte Sizes and SHA-256 Digests)

| Relative File Path | Verified Size (Bytes) | Verified SHA-256 Digest |
| :--- | ---: | :--- |
| `object/jarvis_clss_results_manifest.json` | `17,731` | `dc4ce33b887b2d5cae714e324875968b229ea99fb33e8622a2d299ff24778f83` |
| `object/model_dft_3d_exfoliation_energy.onnx` | `14,286` | `bc24f70e097f87e392982c46a2621ada98312a9798a41cd30b83a3e30cb6f67f` |
| `object/model_tinnet_N_ead.onnx` | `3,612` | `ef9e306148bc05e9ca6b992ba2ebe31752fb6193a7d4f09847c0b3a1b6f5d8ef` |
| `object/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv` | `3,012` | `79189386af5ae8c30bc79fb1f7bbc3839536a53616c1b5cb110471dd905a1c19` |
| `object/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv.zip` | `1,395` | `ae3e9da2a4346116d9ea43fffead59bf67bb53bb948a5094fc23381e1432f6ac` |
| `object/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv` | `1,159` | `1328eea4abc72755830ac8d1c848a0e01564aa16ccc0b603941b26d94c4fa570` |
| `object/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv.zip` | `662` | `8ffcfb46f7bd52a11428b8f6c8239e0eac367d7956e217701316169a09f17a67` |
| `object/cv5_oof_dft_3d_exfoliation_energy.csv` | `45,178` | `d3a94e8543c3c3443424dd75d2b2dca17aa43b4bd15320695925ecbb833e2f64` |
| `object/cv5_oof_tinnet_N_ead.csv` | `17,669` | `104b07f6c20bf883001ba4567df85bc232de8d30c17077f7bac26a362d8c8b63` |
| `how-we-built-it/featurize_physics_clss.py` | `34,242` | `3675beadd412c1ef37ca162519c30364e4d3b25990cd53ebf3719f5f1382798a` |
| `how-we-built-it/train_and_predict_jarvis_clss.py` | `8,456` | `f2d2ea4a28ae67c27ee035f46cfa9c2f26cec1690b46c2b3aae257ce5343bb26` |
| `how-we-built-it/author_checker_jarvis_clss.py` | `692` | `9bb3af40cf1c0398c1a5b9ff7b586574b50b88ebac472fafa8fcbb36c69ef179` |

### 2.2 Independent Split Hygiene & Standard-Operator ONNX Evaluation
- **`dft_3d_exfoliation_energy`**: `650` train + `81` val = `731` `train U val` IDs, `81` `test` IDs (`812` total across `object/features_dft_3d_exfoliation_energy_part1.csv`..`part28.csv`). Overlap between `train U val` and `test` IDs = `0`. Evaluating `object/model_dft_3d_exfoliation_energy.onnx` via `onnxruntime.InferenceSession` reproduces `object/AI-SinglePropertyPrediction-exfoliation_energy-dft_3d-test-mae.csv` with `max |diff| = 4.87e-09`.
- **`tinnet_N_ead` (`p1`)**: `263` train + `32` val = `295` `train U val` IDs, `32` `test` IDs (`327 < 2,000` total across `object/features_tinnet_N_ead_part1.csv`..`part11.csv`). Overlap between `train U val` and `test` IDs = `0`. Evaluating `object/model_tinnet_N_ead.onnx` via `onnxruntime.InferenceSession` reproduces `object/AI-SinglePropertyPrediction-ead-tinnet_N-test-mae.csv` with `max |diff| = 4.83e-09`.

### 2.3 Independent Test MAE & 1,000-Sample 90% Bootstrap CI Verification

| Task | Live Best MAE | Verified Test MAE | Relative Reduction ($\ge 5\%$ req.) | Absolute Gain $\Delta\text{MAE}$ | Bootstrap $h_{90\%}$ (`seed=0`) | Max $h_{90\%}$ (`seeds 0..9`) | Upper Bound $\text{MAE} + h_{90\%}$ vs Live Best | Criterion Check |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `dft_3d_exfoliation_energy` | `40.88700 meV/atom` (`matminer_xgboost`) | **`28.195924 meV/atom`** | **`-31.0394%`** | **`+12.691076 meV/atom`** | **`11.132579 meV/atom`** | `11.449430 meV/atom` | `39.328502` vs `40.88700 meV/atom` | **PASS** |
| `tinnet_N_ead` (`p1`) | `0.08710 eV` (`alignn_model`) | **`0.068908 eV`** | **`-20.8865%`** | **`+0.018192 eV`** | **`0.017247 eV`** | `0.017247 eV` | `0.086155 eV` vs `0.08710 eV` | **PASS (`p1`)** |

pass: true
