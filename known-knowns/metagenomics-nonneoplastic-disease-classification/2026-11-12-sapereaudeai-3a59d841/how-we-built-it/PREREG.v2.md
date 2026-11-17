# PREREG.v2: added sensitivity analyses for the p3 audit (run 2026-11-12-1824)

frozen_utc: 2026-11-12T18:46:30Z

Why a v2: the human lifted the time limit at about 18:45Z, so analyses that PREREG.md left out for time are added.
Nothing in PREREG.md changes: same readings R1-R5, disease (T2D), data, folds, models, statistics, baseline
tolerances, null design (N1 primary, N2 reported) and escape hatches. Results seen before this file was written:
the W2 audit (attempts/within-cohort-audit/out/W2_audit.json) and null N1 (attempts/pooled-audit/out/null_n1.json).
The analyses below are reported as sensitivity checks; none of them is a gate, and none replaces a primary number.

null_test: required (unchanged; N1 of PREREG.md)

S1. Fold scheme: setting P2 rerun with plain StratifiedKFold(10, shuffle=True, random_state=r), r = 0..19, ignoring
    subject groups (the paper's literal scheme), for the species RF (500 trees) and the study-only LR. New fold file
    folds/folds_P2_ungrouped.csv, hashed in folds/FOLDS_v2.sha256 before fitting.
S2. Study recognition: in P2, how identifiable each study is from species alone: species RF (500 trees, sqrt,
    repeat-0 grouped folds), one-vs-rest AUC for each study label, from out-of-fold class probabilities.
S3. Learner robustness of R3: in P2 and W1, the within-study permutation repeated with a linear species model
    (log10(abundance + 1e-5) per species, standardised inside the training fold, LogisticRegression C=1.0 L2), on the
    repeat-0 folds; 400 permutations each; real-label value computed the same way.
S4. Complete-case depth: in P2, the depth-alone LR on the 818 samples with a matched read count (no imputation, no
    missing indicator), on the same grouped folds restricted to those samples (20 repeats). This removes the
    hmpii-missingness channel from the depth-alone number.
S5. Within each T2D study of P1 (Qin 2012 and WT2D), the pooled-model (P1 species RF out-of-fold) scores' AUC
    restricted to that study's own samples, mean over repeats (already computable from saved OOF; reported).
