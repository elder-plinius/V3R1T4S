# Skeptic 3: Target Criterion & Zero-Leakage Audit

context: independent rule and protocol audit started from target definition and solver code only

## Audit Summary

1. Inspected `how-we-built-it/fb_htr_ssvep.py` and verified that `FBHTRSSVEPClassifier` is a single fixed sklearn-compatible estimator with fixed hyperparameters (`n_harmonics=4, c_joint=0.1, c_cca=0.2, c_ts=0.1, w_joint=0.45, w_cca=0.40, w_ts=0.15`) evaluated via `WithinSessionEvaluation(paradigm=SSVEP(), random_state=42)`.
2. Verified that all supervised spatial filters (leave-one-out debiased class-template spatial filters and Harmonic SSD generalized eigenvalue filters), feature scalers (`StandardScaler`), Representer-Theorem Gram bases, and `LogisticRegression` classifiers are fitted strictly on `X_train, y_train` inside each 5-fold CV split, and that `_TRIAL_CACHE` caches only stateless single-trial spectral/covariance transforms keyed by single-trial byte content.
3. Confirmed via `verify-it-yourself/check_moabb_ssvep.py` that all 160 CV folds across all 32 subject-sessions have zero train/test index overlap, exact 5-fold test partitioning, and class-stratified training splits.

pass: true
