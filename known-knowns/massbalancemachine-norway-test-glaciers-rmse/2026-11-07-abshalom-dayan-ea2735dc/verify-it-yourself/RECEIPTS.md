# Receipts

`sh verify-it-yourself/run_checks.sh`, run 2026-11-07 (exit 0), real output:

```
ok   test CSV sha256 is the pinned d1d34e0821a9...
ok   object/LW1_test_point_predictions.csv sha256 9bec8deb75b2...
ok   object/frozen_LW1.json sha256 ea2735dcad5f...
ok   every id has one n_months, one balance and n_months monthly rows (0 bad)
ok   point counts Ba 1065, Bw 999, Bs 1028 (expected 1065 / 999 / 1028)
ok   predictions cover exactly the 999 points of seasons Bw (999 given)
ok   frozen model: 3 coefficients (at most 20)
ok   predictions recomputed from the frozen coefficients agree (max diff 1.78e-15)
ok   Bw RMSE 0.5239 over 999 points (claimed 0.5239)
ok   p2: Bw RMSE 0.5239 is at most 0.59 with at most 20 fitted parameters
PASS
```
