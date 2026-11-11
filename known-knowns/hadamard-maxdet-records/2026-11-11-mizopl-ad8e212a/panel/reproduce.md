# Skeptic 1 — Reproducibility Audit (`reproduce.md`)

- `context`: `fresh independent skeptic review initialized from clean package directory`
- `target_id`: `hadamard-maxdet-records`
- `command_checked`: `sh verify-it-yourself/run_checks.sh`
- `corrupt_checked`: `python3 verify-it-yourself/verify.py --corrupt`

## Audit Findings

1. **Zero-Dependency Standard-Library Execution + SymPy Cross-Check:** `sh verify-it-yourself/run_checks.sh` runs `verify-it-yourself/verify.py` using only Python 3 standard library modules (plus `sympy.Matrix.det(method="bareiss")` automatically when `sympy` is installed) and completes in under 1.5 seconds on CPU, printing `PASS` on its final line with exit code `0`.
2. **Triple-Engine Exact Determinant Agreement:** Across all 8 matrices `object/M081.txt` .. `object/M117.txt` and `object/hadamard_maxdet_8_records.json` (`sha256: ad8e212ac8397998c64702e7a9837dd048bf833df109520d01d713111b13b190`), fraction-free Bareiss elimination on Python `int`, 14-prime 61-bit modular Gaussian elimination via CRT, and SymPy Bareiss elimination agree digit-for-digit on `|det(X)|` and `D_norm = |det(X)| / 2^(n-1)`.
3. **Algebraic Core & Reconstruction Check:** `verify.py` and `how-we-built-it/reconstruct_all_8_records.py` rebuild every matrix bit-for-bit from `generator_params` (`gs_os1`, `hadamard_core_os1`, `hadamard_core_os2`) and confirm exact Hadamard orthogonality `H H^T = (n - 1) I_(n-1)` on all 8 cores.
4. **Adversarial Corruption Rejection:** Running `python3 verify-it-yourself/verify.py --corrupt` as well as single-digit and sign-flip perturbations to `object/hadamard_maxdet_8_records.json` and `object/M081.txt` .. `object/M117.txt` exits with status `1` and final line `FAIL`.

pass: true
