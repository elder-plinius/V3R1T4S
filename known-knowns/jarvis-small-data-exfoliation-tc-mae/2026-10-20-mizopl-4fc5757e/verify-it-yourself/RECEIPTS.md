# Verification Receipts (`2026-10-20-mizopl-4fc5757e`)

## 1. Execution Receipt of `sh verify-it-yourself/run_checks.sh`

- **Command:** `sh verify-it-yourself/run_checks.sh`
- **Exit Code:** `0`
- **Wall-Clock Time:** `0.48s` on CPU (imports zero contributor code; evaluates `object/model_*.onnx` via `onnxruntime` on `object/features_*_part*.csv`)
- **Stdout:**
```text
[OK] dft_3d_exfoliation_energy: ONNX max|diff|=4.87e-09, Test MAE = 28.195924 vs 40.88700 (-31.04%), gain = +12.691076 > h90 = 11.132579, p2 5-fold MAE = 32.67274 vs 45.00463 (Wilcoxon p = 1.62e-18)
[OK] tinnet_N_ead             : ONNX max|diff|=4.83e-09, Test MAE = 0.068908 vs 0.08710 (-20.89%), gain = +0.018192 > h90 = 0.017247, p2 5-fold MAE = 0.09563 vs 0.16556 (Wilcoxon p = 5.86e-15)
PASS
```
