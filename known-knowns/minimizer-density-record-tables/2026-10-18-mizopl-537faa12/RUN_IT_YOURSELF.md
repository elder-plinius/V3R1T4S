# Run It Yourself (`2026-10-18-mizopl-537faa12`)

## 1. Quick Verification (~1.2 seconds, Python 3 + NumPy)

From the root of this package directory:

```bash
sh verify-it-yourself/run_checks.sh
```

`verify-it-yourself/run_checks.sh` fetches `k_extension_k16_w12.csv` (`sha256: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa`) and `w12_k4.gm` (`sha256: 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131`) from `OrensteinLab/10-minimizers` at pinned commit `916daebd399d15d061e2fd437326aee5cf0e7292`, stops on any SHA-256 mismatch, and runs `verify-it-yourself/author_checker_minimizer_check.py` on `object/w12_k4_improved.gm`.

Expected output:
```text
w12_k4_improved.gm sha256  : 537faa127958cbb7f10b0e90c8832449b375b2fad8360bfd4c7e596eee187bc4 (136 bytes)
published_w12_k4.gm sha256 : 7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131 (136 bytes)
k_extension_k16_w12.csv sha: 88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa (1644 bytes)
Improved order (16 uint64s): [15, 6, 7, 12, 10, 4, 11, 3, 0, 1, 8, 9, 14, 2, 13, 5]
Published order (16 uint64s): [6, 1, 16, 16, 16, 16, 16, 0, 16, 2, 4, 3, 16, 16, 5, 16]

--- Exact Expected DNA Density (over all 4^16 = 4,294,967,296 DNA windows) ---
Published w12_k4.gm (bit-plane exact)        : 584312429 / 2^32 = 0.1360458389
Improved  w12_k4_improved.gm (bit-plane)     : 573933439 / 2^32 = 0.1336292920
Improved  w12_k4_improved.gm (4-ary DP)      : 573933439 / 2^32 = 0.1336292920

--- Comparison vs All Listed Methods at (w=12, k=4) ---
  GreedyMini          : 0.136046000  (our order improves by -1.7764%)
  angle-based         : 0.138322748  (our order improves by -3.3931%)
  decycling           : 0.143956000  (our order improves by -7.1735%)
  double decycling    : 0.145236000  (our order improves by -7.9916%)
  miniception         : 0.156164000  (our order improves by -14.4302%)
  mod-minimizer       : 0.156164000  (our order improves by -14.4302%)
  open-close-syncmer  : 0.156164000  (our order improves by -14.4302%)
Smallest listed value   : 0.1360458389 (GreedyMini)
Our exact DNA density   : 0.1336292920
Relative reduction      : -1.776274% (required >= 0.500000%)

VERIFICATION: PASS
PASS
```

## 2. Upstream Reference Code (Pinned Commits)

- `OrensteinLab/GreedyMini` exact C++ DNA density evaluator (`prob_gc_dna` / `density_expected_dna`):
  `https://github.com/OrensteinLab/GreedyMini/blob/a67eb90dc278ea78111a76d5813cf2ac7662b0ae/code/density_and_gc.cpp`
- `OrensteinLab/10-minimizers` empirical DNA density notebook:
  `https://github.com/OrensteinLab/10-minimizers/blob/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/greedymini_density.ipynb`
