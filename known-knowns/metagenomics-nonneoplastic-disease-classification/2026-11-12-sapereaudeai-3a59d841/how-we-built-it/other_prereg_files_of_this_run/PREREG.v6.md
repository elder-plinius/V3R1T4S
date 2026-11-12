# PREREG.v6: p2 attempt 2 (cirrhosis), after attempt 1 (PREREG.v3) scored 0.923 < 0.936

frozen_utc: 2026-11-12T19:47:48Z

Attempt 1 (PREREG.v3, frozen procedure: univariate top-k + L2 logistic, species only) gave mean AUC 0.9231 on
folds_p2_cirrhosis.csv, below the 0.936 bar: p2 attempt 1 failed and stays reported as failed. This is the second and
last p2 attempt on this cohort in this run; the report will state both attempts and their results.

Unchanged from PREREG.v3: cohort (cirrhosis, 118/114), readings Q2-Q4 (bar 0.936 = best published species-abundance
AUC 0.946 - 0.01; the overall marker best 0.963 reported for context), protocol (10-fold x 20, mean per-fold AUC),
<= 20 taxa in every fitted model, linear learner, selection inside training folds, released full-data model.

null_test: required (unchanged for the run; P2N-style null for this attempt: 400 label permutations of the full nested
procedure on the repeat-0 folds of the new fold file, reported in the lens)

## Changes (the whole new procedure, fixed now)

1. Features: log10(relative abundance / 100 + 1e-5) of every MetaPhlAn2 taxon at genus, family, order, class and
   phylum rank plus species (rows ending in g__, f__, o__, c__, p__ or s__; no strain t__ rows and no kingdom rows),
   i.e. named taxa of the same MetaPhlAn2 abundance profile. Prevalence filter inside the training fold: present
   (> 0) in >= 10% of training samples. Standardised inside the training fold.
2. Learner: L1-penalised logistic regression (liblinear) for selection, then an L2 logistic refit (C = 1) on the
   selected taxa ("relaxed lasso"). The L1 strength C is chosen inside each training fold by inner 5-fold
   StratifiedKFold (random_state = 1000*r + k) over the grid C in {0.01, 0.02, 0.05, 0.1, 0.2, 0.5}, keeping only
   values whose inner fits select between 1 and 20 taxa in every inner fold, by mean inner AUC (ties: smaller C).
   The outer fit uses the chosen C; if it selects more than 20 taxa, C steps down the grid until <= 20; if it selects
   none, C steps up.
3. New final folds, committed before any fit of this procedure: folds/folds_p2b_cirrhosis.csv
   (StratifiedGroupKFold by subject, random_state 7000..7019), hashed in folds/FOLDS_v6.sha256.
4. Pass: mean AUC >= 0.936. Baseline RF re-run on the new folds is reported next to it (expected 0.945 +/- 0.036).
