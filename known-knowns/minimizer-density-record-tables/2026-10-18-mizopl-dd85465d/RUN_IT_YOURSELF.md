# Run It Yourself (`2026-10-18-mizopl-dd85465d`)

## 1. Quick Verification (~0.4 seconds, Python 3 + NumPy)

From the root of this package directory:

```bash
sh verify-it-yourself/run_checks.sh
```

`verify-it-yourself/run_checks.sh` fetches `k_extension_k16_w12.csv` (`sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa`) and `w12_k3.gm` (`sha256: c592519b57ad8104860b7e1559b28c2d37ef329db82298b151a65e056ce27f1d`) from `OrensteinLab/10-minimizers` at pinned commit `916daebd399d15d061e2fd437326aee5cf0e7292`, stops on any SHA-256 mismatch, and runs `verify-it-yourself/author_checker_minimizer_check.py` on `object/w12_k3_improved.gm`.

## 2. Upstream Reference Code (Pinned Commits)

- `OrensteinLab/GreedyMini` exact C++ DNA density evaluator (`prob_gc_dna` / `density_expected_dna`):
  `https://github.com/OrensteinLab/GreedyMini/blob/a67eb90dc278ea78111a76d5813cf2ac7662b0ae/code/density_and_gc.cpp`
- `OrensteinLab/10-minimizers` empirical DNA density notebook:
  `https://github.com/OrensteinLab/10-minimizers/blob/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/greedymini_density.ipynb`
