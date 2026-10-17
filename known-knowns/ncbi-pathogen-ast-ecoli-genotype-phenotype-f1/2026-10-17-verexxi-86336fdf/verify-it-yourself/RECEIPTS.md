# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` (2026-10-16, build machine; export files pre-cached by hard link, same sha256)

```
object files: sha256 OK
recomputed TEST rows: 1715 comparisons, 1257 clusters; rule predictions and clusters identical
model F1 98.80 acc 98.78 TP/FP/TN/FN (867, 8, 827, 13) | rule F1 94.40 acc 94.52 TP/FP/TN/FN (792, 6, 829, 88)
cluster bootstrap (2000 reps, stdlib RNG): model F1 2.5% 98.23; paired diff 2.5% 3.08
ok   F1 98.80 >= published 93.9 + 3
ok   F1 98.80 >= recomputed rule 94.40 + 3
ok   bootstrap 2.5% 98.23 > max(published, rule)
ok   paired-difference 2.5% > 0
ok   accuracy 98.78 >= published 94.5
ok   matches claimed F1/accuracy
PASS
```
