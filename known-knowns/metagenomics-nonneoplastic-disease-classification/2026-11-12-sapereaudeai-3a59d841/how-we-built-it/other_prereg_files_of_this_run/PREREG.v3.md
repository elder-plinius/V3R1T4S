# PREREG.v3: partial win p2 attempt (run 2026-11-12-1824)

frozen_utc: 2026-11-12T18:53:30Z

Written after the human lifted the time limit (about 18:45Z) and before any model has been fitted on the cohort
named below. Nothing in PREREG.md or PREREG.v2.md changes (they govern the p3 audit). This file adds a p2 attempt.

null_test: required (unchanged for the run; for p2 the null is P2N below and is reported in the p2 lens and, if p2 is
claimed, in that claim's own null_test.md)

## Criterion (verbatim, bank partial win p2)

"Match the best published within-cohort AUC for one disease to within 0.01 using a model with <= 20 named taxa and no
nonlinear learner, releasing the taxa and coefficients - an interpretability/parsimony result."

## Readings (most favourable fair reading, chosen before any result)

Q1. Cohort, by a rule fixed now: the MetAML disease cohort with the highest published species-abundance AUC, i.e.
    liver cirrhosis (Qin et al. 2014; MetAML dataset Quin_gut_liver_cirrhosis; 118 cirrhosis vs 114 controls).
Q2. "best published within-cohort AUC": the best MetAML (status source) cross-validated AUC for that cohort with the
    same feature type as a taxa model, species abundance: Fig 3, RF-FS:Emb 0.946 (margin 0.035), fetched as
    data/figs/pcbi.1004977.g003.png (sha256 f9b5cb06...b6). Reason: the bank's protocol-mismatch pitfall says that
    comparing against another feature type is a fake win. The overall best for the cohort (marker presence, SVM,
    0.963) is reported next to it for context, and the report will say plainly whether that stricter bar is met.
Q3. "to within 0.01": mean AUC >= 0.946 - 0.01 = 0.936 (exceeding the published value also counts as matching).
Q4. "a model with <= 20 named taxa and no nonlinear learner": every fitted model (each training fold, and the final
    full-data model) uses at most 20 species, and the learner is a logistic regression (linear in the log-abundance
    features). Taxa are selected inside training folds only. The released model is the full-data fit of the same
    frozen procedure, with its taxa names and coefficients.
Q5. Protocol: the paper's (10-fold stratified CV x 20 repeats, mean of per-fold AUCs), on new fold files
    folds/folds_p2_cirrhosis.csv (StratifiedGroupKFold by subject, random_state 3000..3019), written and hashed in
    folds/FOLDS_v3.sha256 before any fit. Pass: mean AUC >= 0.936. The 95% MetAML-style margin and the repetition
    range are reported; the bank sets no interval requirement for p2, so none is added.

## The frozen procedure (no development loop: model choice is nested inside each training fold)

- Features: x = log10(relative abundance / 100 + 1e-5) for every species row (|s__, no |t__).
- Inside each training fold: drop species present (> 0) in fewer than 10% of training samples; standardise; rank
  species by |Mann-Whitney AUC - 0.5| on the training fold; keep the top k; fit LogisticRegression(L2, C).
- (k, C) chosen inside each training fold by an inner 5-fold StratifiedKFold (random_state = 1000*r + k_outer) over
  the grid k in {5, 10, 15, 20} x C in {0.01, 0.1, 1}, by mean inner AUC (ties: smaller k, then smaller C).
- The released model: the same procedure on all 232 samples (inner 5-fold, random_state 0).

## Baseline (kit/RUN.md step 3c)

RF on species abundance (500 trees, sqrt, gini) on the same final folds. Expected 0.945 (MetAML Fig 3, RF row,
margin 0.036); tolerance: inside 0.945 +/- 0.036. Reported next to the p2 number.

## Null (P2N)

The full nested procedure with labels permuted (one 10-fold repetition, repeat-0 final folds), 400 permutations
(seeds 0..399); the real repeat-0 value must beat every control.

## Escape hatches

H1. If the nested run cannot finish, report what finished; no claim from a partial run.
H2. If the RF baseline misses its tolerance, the comparison is unresolved and no p2 claim is made from it.
H3. Nothing is retuned after the final folds are scored; a different procedure needs a PREREG.v4 and fresh folds,
    and the report will count every attempt.
