# Verification Receipts (`2026-10-20-mizopl-4fc5757e`)

## 1. Execution Receipt of `sh verify-it-yourself/run_checks.sh`

- **Command:** `sh verify-it-yourself/run_checks.sh`
- **Exit Code:** `0`
- **Wall-Clock Time:** `0.42s` on CPU
- **Stdout:**
```text
[OK] dft_3d_Tc_supercon       : Test MAE = 0.902806 vs 1.51870 (-40.55%), gain = +0.615894 > h90 = 0.367962, p2 5-fold MAE = 1.98409 vs 2.36822 (Wilcoxon p = 5.99e-09)
[OK] dft_3d_exfoliation_energy: Test MAE = 28.195924 vs 40.88700 (-31.04%), gain = +12.691076 > h90 = 11.132579, p2 5-fold MAE = 32.67274 vs 45.00463 (Wilcoxon p = 1.62e-18)
[OK] tinnet_N_ead             : Test MAE = 0.068908 vs 0.08710 (-20.89%), gain = +0.018192 > h90 = 0.017247, p2 5-fold MAE = 0.09563 vs 0.16556 (Wilcoxon p = 5.86e-15)
PASS
```

## 2. Full Structure Re-Training Receipt (`--retrain-from-structures`)

- **Command:** `python3 -B verify-it-yourself/check_jarvis_clss_package.py --retrain-from-structures`
- **Exit Code:** `0`
- **Result:** Recomputes all 1,612-dimensional structure descriptors, homolog signatures, fracture regime vectors, and canonical slab representations from `object/data/clean_structures/*_structures.json.gz`, fits all three CLSS models strictly on `train U val` IDs, and confirms `max |retrain - npz| < 1e-12` (`== 0.0`) across all three benchmarks.
