# Skeptic 3: Target Criterion & Zero-Leakage Audit

context: independent rule and protocol audit started from target definition and solver code only

## Audit Summary

1. Inspected `how-we-built-it/verify_srbench_win.py` and confirmed that `train_test_split(..., train_size=0.75, test_size=0.25, random_state=seed)` uses the exact 30 official SRBench `random_state` seeds per dataset.
2. Confirmed that all basis selection, 5-fold cross-validation (`KFold(n_splits=5)`), 3-decimal coefficient rounding (`round_floats`), and `sympy.collect` factoring (`fast_collect_sympy`) occur strictly inside `(X_train, y_train)` with zero access to `X_test` or `y_test`.
3. Confirmed that complexity is measured via `symbolic_utils.complexity(round_floats(parse_expr(...)))` exactly as specified in `known-unknowns/machine-learning/srbench-2025-blackbox-dominate-leader.md`.

pass: true
