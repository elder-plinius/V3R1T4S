# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` (2026-10-16, build machine; export files pre-cached by hard link, same sha256)

```
object files: sha256 OK
recomputed TEST rows: 1623 comparisons, 1192 clusters; rule predictions and clusters identical
model F1 96.28 acc 98.64 TP/FP/TN/FN (285, 9, 1316, 13) | rule F1 92.41 acc 97.17 TP/FP/TN/FN (280, 28, 1297, 18)
cluster bootstrap (2000 reps, stdlib RNG): model F1 2.5% 93.56; paired diff 2.5% 1.81
ok   F1 96.28 >= published 92.4 + 3
ok   F1 96.28 >= recomputed rule 92.41 + 3
ok   bootstrap 2.5% 93.56 > max(published, rule)
ok   paired-difference 2.5% > 0
ok   accuracy 98.64 >= published 97.6
ok   matches claimed F1/accuracy
PASS
```
