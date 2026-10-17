# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` (2026-10-16, build machine; export files pre-cached by hard link, same sha256)

```
object files: sha256 OK
recomputed TEST rows: 1531 comparisons, 1114 clusters; rule predictions and clusters identical
model F1 97.66 acc 98.76 TP/FP/TN/FN (396, 10, 1116, 9) | rule F1 94.51 acc 97.19 TP/FP/TN/FN (370, 8, 1118, 35)
cluster bootstrap (2000 reps, stdlib RNG): model F1 2.5% 96.30; paired diff 2.5% 1.23
ok   F1 97.66 >= published 94.6 + 3
ok   F1 97.66 >= recomputed rule 94.51 + 3
ok   bootstrap 2.5% 96.30 > max(published, rule)
ok   paired-difference 2.5% > 0
ok   accuracy 98.76 >= published 97.9
ok   matches claimed F1/accuracy
PASS
```
