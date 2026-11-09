# Skeptic 1: Reproducibility & Independent Computation Audit

context: independent clean-room verification process started from package directory only

## Audit Summary

1. Executed `sh verify-it-yourself/run_checks.sh` from a clean temporary copy of the package.
2. Verified that `check_moabb_ssvep.py` independently validates all 32 subject-session rows (160 CV folds, 3,955 trials across `Kalunga2016`, `Nakanishi2015`, and `MAMEM3`) in `object/moabb_ssvep_within_session_cells.csv` against `verify-it-yourself/data/moabb_ssvep_fold_witness.json.gz`, recomputing every multi-class logit and softmax probability from the orthonormal QR linear projections (`U_te @ R_W + b`), ensemble probability combination (`0.45 * p_joint + 0.40 * p_cca + 0.15 * p_ts`), fold accuracy, session accuracy, and dataset mean/std (`ddof=0`).
3. Confirmed that mutating a single digit in `object/moabb_ssvep_within_session_cells.csv` causes `run_checks.sh` to exit with code 1 and output `FAIL`.

pass: true
