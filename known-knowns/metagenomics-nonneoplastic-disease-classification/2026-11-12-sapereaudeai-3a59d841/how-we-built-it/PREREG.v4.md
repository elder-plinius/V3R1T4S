# PREREG.v4: one more p3 sensitivity check, and a development-only scan for the main criterion

frozen_utc: 2026-11-12T19:08:13Z

Nothing in PREREG.md, PREREG.v2.md or PREREG.v3.md changes.

null_test: required (unchanged for the run)

## S6 (p3 sensitivity; written after the P2 covariate-only LR numbers were seen, before S6 is computed)

In P2 the age and BMI columns are missing for the HMP samples, so PREREG.md's median-imputation-with-indicator lets
the "age alone" and "BMI alone" models see a missingness flag that marks HMP membership. S6 repeats age-alone,
BMI-alone and age+BMI LR in P2 on the complete cases only (samples with both age and BMI), no imputation, no
indicator, on the P2 grouped folds restricted to those samples (20 repeats). Reported next to the primary numbers;
no primary number is replaced.

## D1 (main success criterion: development scan only, no claim can come from it)

Purpose: decide whether any cohort/learner pair is worth a frozen final attempt at the main criterion (mean AUC >
best published species AUC + 0.03, outside the 95% repetition interval, and > our RF re-run + 0.03 on the same
folds). Development folds: StratifiedKFold(10, shuffle=True, random_state 5000..5004) (5 repeats), on each
non-cancer MetAML cohort: cirrhosis, IBD (metahit, ibd vs n), obesity (Chatelier, obesity vs leaness), T2D, WT2D.
Learners (all fitting inside folds): RF500 (reference), ExtraTrees(1000, sqrt), L2 logistic on standardised
log10(abundance/100 + 1e-5) with prevalence >= 10% (C = 0.1), and RF500 on the same log features plus Shannon
diversity and richness. Rule for going further: a learner whose dev mean beats both the dev RF and the best
published species AUC by >= 0.04 on some cohort; then a PREREG.v5 freezes it with fresh final folds (seeds
6000..6019), committed before any final fit. Every dev number is reported, whatever it shows. The p2 cohort
(cirrhosis) is included in D1 only after the p2 final run of PREREG.v3 has been scored.
