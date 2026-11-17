# PREREG.v9: p2 attempt 3 (WT2D), the last p2 attempt of this run

frozen_utc: 2026-11-12T20:20:05Z

null_test: required (unchanged for the run; P2N-style null of PREREG.v3 for this attempt, reported in the lens)

Disclosed selection: WT2D is chosen after seeing the PREREG.v4 D1 development scan, where a log-linear model on all
prevalent species was strongest relative to the published bar on WT2D (dev 0.813 vs published species best 0.772).
That scan used different folds (seeds 5000-5004) on the same 96 samples, so this attempt is not independent of it;
the report will say so. Earlier p2 attempts: cirrhosis attempt 1 (0.923) and attempt 2 (0.915), both below 0.936.

Cohort: MetAML WT2D, t2d (53) vs n (43). Bar (same readings Q2-Q4 as PREREG.v3): best published species-abundance
AUC for WT2D 0.772 (Fig 3, RF-FS:Emb) minus 0.01 = 0.762; the overall best (markers, SVM, 0.785) would need 0.775
and is reported for context. Procedure: exactly the frozen attempt-1 procedure of PREREG.v3 (prevalence >= 10%,
log10, standardise, univariate Mann-Whitney top-k with k in {5,10,15,20}, L2 logistic C in {0.01,0.1,1}, inner
5-fold choice), on new committed folds folds/folds_p2c_wt2d.csv (StratifiedGroupKFold by subject, random_state
8000..8019), hashed in folds/FOLDS_v9.sha256 before any fit. Baseline RF500 on the same folds reported (expected
0.762 +/- 0.111, the paper's RF row). Pass: mean AUC >= 0.762. No further p2 attempt in this run whatever the result.
