# Preregistration: Lens 1 (c-evaluator-optimizer)

frozen_utc: 2026-10-14T03:25:55Z
target: fmm-additive-complexity-records
lens: c-evaluator-optimizer
null_test: not needed because every candidate straight-line program is an explicit algebraic object verified deterministically and symbolically over Z by verify_slp.py against exact integer matrix multiplication and compared directly against published integer addition counts in the live status tables.

## Objective & Scope
Build and run a native C (`clang -O3 -pthread`) Common-Subexpression Elimination (CSE) + Exact Meet-in-the-Middle Subexpression Re-Covering + Dead/Single-Use Fresh-Variable Pruning + Lookahead Beam/LNS Optimizer (`cse_opt.c`) across `(3, 3, 3):23` (`cr=58`) and at least 12 formats with `max(n, m, p) <= 8` where the ternary `ZT` rank equals the best rank in `fmm_sota.json`.

## Evaluation Rule
1. Every output `_reduced.json` file must pass `python3 verify_slp.py` with 0 symbolic bilinear errors over `Z`.
2. A format is a verified record if its recounted `cr` is strictly less than:
   - the minimum `cr` across all files for that format and rank in `dronperminov/FastMatrixMultiplication/schemes/results/addition_reduced_ZT`,
   - `schemes/reduced_known.json`, `README.md`, and `CHANGELOG.md`,
   - `matmulcatalog`'s `COVERAGE.md` `adds` column, and
   - any cited complexity bound on `fmm.univ-lille.fr` for that format and rank.
