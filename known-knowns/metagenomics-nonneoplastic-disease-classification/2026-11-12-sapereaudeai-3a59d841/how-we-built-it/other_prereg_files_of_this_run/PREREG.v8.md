# PREREG.v8: confound context for the p1 result (not a gate; p1's pass rule in PREREG.v7 is unchanged)

frozen_utc: 2026-11-12T20:02:24Z

Seen before writing: the p1 held-out AUC (0.7096), its by-country split, null and within-B context number.
Not yet computed: anything below. Reported next to p1; no number here changes the p1 verdict.

null_test: required (unchanged for the run)

C1. Covariate-only transfer: logistic regression (C = 1) on age, BMI and sex (training-standardised; sex one-hot;
    missing values -> training median plus missing indicator), trained on cMD QinJ_2012 + KarlssonFH_2013 (T2D vs
    control) and applied once to MetaCardis T2D vs healthy (cMD sampleMetadata age, BMI, gender). AUC with 2,000
    stratified bootstrap 95% interval.
C2. The frozen p1 model's MetaCardis scores restricted to (case, control) pairs matched on BMI (|difference| <= 1.0)
    and, separately, on age (|difference| <= 3 years): pair-restricted AUC, plus raw BMI / age AUC on the same pairs.
C3. Spearman correlation of the p1 score with BMI and with age in MetaCardis, within cases and within controls.
