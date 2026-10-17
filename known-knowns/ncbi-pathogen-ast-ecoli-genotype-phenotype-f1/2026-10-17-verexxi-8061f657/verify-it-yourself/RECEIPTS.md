# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` (2026-10-16, build machine; export files pre-cached by hard link, same sha256)

```
object files: sha256 OK
recomputed TEST rows: 1422 comparisons, 1045 clusters; rule predictions and clusters identical
model F1 91.97 acc 97.68 TP/FP/TN/FN (189, 7, 1200, 26) | rule F1 44.78 acc 69.48 TP/FP/TN/FN (176, 395, 812, 39)
cluster bootstrap (2000 reps, stdlib RNG): model F1 2.5% 86.73; paired diff 2.5% 39.50
ok   F1 91.97 >= published 44.5 + 3
ok   F1 91.97 >= recomputed rule 44.78 + 3
ok   bootstrap 2.5% 86.73 > max(published, rule)
ok   paired-difference 2.5% > 0
ok   accuracy 97.68 >= published 73.6
ok   matches claimed F1/accuracy
PASS
```
