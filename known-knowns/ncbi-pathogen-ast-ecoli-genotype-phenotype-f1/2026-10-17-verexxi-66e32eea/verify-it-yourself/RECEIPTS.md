# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` (2026-10-16, build machine; export files pre-cached by hard link, same sha256)

```
object files: sha256 OK
recomputed TEST rows: 1693 comparisons, 1246 clusters; rule predictions and clusters identical
model F1 96.13 acc 98.35 TP/FP/TN/FN (348, 12, 1317, 16) | rule F1 80.36 acc 89.72 TP/FP/TN/FN (356, 166, 1163, 8)
cluster bootstrap (2000 reps, stdlib RNG): model F1 2.5% 93.51; paired diff 2.5% 10.92
ok   F1 96.13 >= published 77.2 + 3
ok   F1 96.13 >= recomputed rule 80.36 + 3
ok   bootstrap 2.5% 93.51 > max(published, rule)
ok   paired-difference 2.5% > 0
ok   accuracy 98.35 >= published 89.9
ok   matches claimed F1/accuracy
PASS
```
