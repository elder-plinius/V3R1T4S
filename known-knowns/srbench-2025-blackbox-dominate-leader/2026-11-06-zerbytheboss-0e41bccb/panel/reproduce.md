# Skeptic 1: Reproducibility & Independent Computation Audit

context: independent clean-room verification process started from package directory only

## Audit Summary

1. Executed `sh verify-it-yourself/run_checks.sh` from a clean temporary copy of the package.
2. Verified that `check_srbench2025.py` independently parses all 120 closed-form symbolic models in `object/srbench2025_verified_splits.csv` across the 30 official SRBench seeds per dataset, recomputes each expression's exact SymPy preorder traversal AST node count (`model_size`), and evaluates each expression on the held-out 25% test splits of `579_fri_c0_250_5.tsv.gz`, `1028_SWD.tsv.gz`, and `650_fri_c0_500_50.tsv.gz`.
3. Confirmed exact agreement between recomputed test $R^2$ values (`max diff < 1e-12`), recomputed AST node counts (`0` mismatches across all 120 rows), and `r2_test_sympy` / `model_size`, and verified that mutating a single digit in `object/srbench2025_verified_splits.csv` causes `run_checks.sh` to exit with code 1 and output `FAIL`.

pass: true
