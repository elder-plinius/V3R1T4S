# Skeptic 3: Target Criterion & Zero-Leakage Audit

context: independent rule and protocol audit started from target definition and solver code only

## Audit Summary

1. Inspected `how-we-built-it/solve_disdat_sdm.py` and verified that model training, categorical level extraction, feature standardization, and suitability score prediction depend exclusively on `{R}train_po.rds`, `{R}train_bg.rds`, and `{R}test_env*.rds`, with zero access to `{R}test_pa*.rds` until final ROC AUC evaluation.
2. Verified that `nsw30` (the 2-presence NSW species excluded in `RYCKEWAERT/deepmaxent` and `hideyuki-doi/tabfm-distribution`) is excluded, leaving the exact 225 valid species and 217 species with `< 1,000` presence-only records.
3. Confirmed that only tabular point covariates from `disdat` are used (zero external rasters, satisfying `p3`).

pass: true
