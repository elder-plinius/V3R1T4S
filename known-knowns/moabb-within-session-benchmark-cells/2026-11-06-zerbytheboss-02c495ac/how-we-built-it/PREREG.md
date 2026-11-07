# Pre-Registration & Protocol Lock

- **Frozen UTC**: `2026-11-07T00:36:49Z`
- **Target ID**: `moabb-within-session-benchmark-cells` (`neuroscience`)
- **Paradigm Table**: `SSVEP (All classes)` on `https://moabb.neurotechx.com/docs/paper_results.html` (`Kalunga2016`, `Nakanishi2015`, `MAMEM3`)
- **Evaluation Protocol**: MOABB `WithinSessionEvaluation(paradigm=SSVEP(), datasets=[Kalunga2016(), Nakanishi2015(), MAMEM3()], random_state=42)` (5-fold `StratifiedKFold(n_splits=5, shuffle=True, random_state=42)` within each subject-session, scored by multi-class accuracy).
- **Single Fixed Pipeline Invariant**: Exactly one `sklearn.pipeline.Pipeline` (`make_fb_htr_ssvep_pipeline()`) with one fixed set of hyperparameters (`n_harmonics=4, c_joint=0.1, c_cca=0.2, c_ts=0.1, w_joint=0.45, w_cca=0.40, w_ts=0.15`) is evaluated across all three datasets without dataset-specific tuning.
- **Zero Test-Fold Leakage Invariant**: All supervised spatial filters (class-template spatial filters with leave-one-out training debiasing and Harmonic SSD generalized eigenvalue filters), `StandardScaler` statistics, Representer-Theorem Gram bases, and `LogisticRegression` weights are fitted strictly on `X_train, y_train` inside each CV fold.
- **Win Thresholds**: Beat the best pipeline on the live results page by `>= +1.0` percentage point on all 3 datasets (`Kalunga2016 > 71.89`, `Nakanishi2015 > 88.22`, `MAMEM3 > 43.10`) and reproduce at least one listed baseline pipeline on at least one claimed dataset.
- null_test: not needed because this is an empirical benchmark evaluated deterministically on fixed 5-fold cross-validation splits against published MOABB benchmark table values (`kit/RUN.md` Step 3b/3c).
