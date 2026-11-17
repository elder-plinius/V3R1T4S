# RECEIPTS (real output of sh verify-it-yourself/run_checks.sh, run from this folder on 2026-11-12T21:04Z, Python 3.11)

```
ok   object sha256 3a59d8419b0ec3f809e9b8f51d0447624da7f34e454d46c6a603ef6b0a57af89
ok   W1 age-only AUC recomputed 0.7345 vs object 0.7345 (fraction of published 0.961)
ok   W1 depth-only AUC recomputed 0.5910 vs object 0.5910 (fraction of published 0.373)
ok   W1 bmi-only AUC recomputed 0.5549 vs object 0.5549 (fraction of published 0.225)
ok   W2 bmi-only AUC recomputed 0.6724 vs object 0.6724 (fraction of published 0.658)
ok   W2 depth-only AUC recomputed 0.6606 vs object 0.6606 (fraction of published 0.613)
ok   P1 age-only AUC recomputed 0.6852 vs object 0.6852 (fraction of published 0.762)
ok   P1 depth-only AUC recomputed 0.5940 vs object 0.5940 (fraction of published 0.387)
ok   P2 study-only AUC (training case-fraction score) 0.8420 vs object 0.8404; fraction of published: 1.015
ok   W1: 400 distinct permutation seeds
ok   W1 within-study permutation mean 0.5000 (fraction of published -0.000), max 0.6127, real 0.7382
ok   W1 real labels beat all 400 within-study permutations
ok   W2: 400 distinct permutation seeds
ok   W2 within-study permutation mean 0.5024 (fraction of published 0.009), max 0.7372, real 0.7759
ok   W2 real labels beat all 400 within-study permutations
ok   P1: 400 distinct permutation seeds
ok   P1 within-study permutation mean 0.4997 (fraction of published -0.001), max 0.5964, real 0.7434
ok   P1 real labels beat all 400 within-study permutations
ok   P2: 400 distinct permutation seeds
ok   P2 within-study permutation mean 0.7595 (fraction of published 0.770), max 0.7970, real 0.8434
ok   P2 real labels beat all 400 within-study permutations
ok   null N1: real 0.8305 vs best of 400 controls 0.5752
ok   W1 covariates only: age: AUC 0.7345, fraction 0.961
ok   W2 covariates only: ALL: AUC 0.6828, fraction 0.698
ok   P1 covariates only: ALL: AUC 0.7112, fraction 0.869
ok   P2 covariates only: study: AUC 0.8404, fraction 1.010
PASS
```
