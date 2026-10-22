# Receipts

Output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (macOS, system python3 3.9, standard library only; numpy was not installed, so the optional second checker was skipped):

```
sha256 matches INDEX.csv (765069602e766f6ce6bc285ce449f5ee7f8ae8bac63b099cb9560ec9e850b93d)
== check_cw_std.py (standard library): count, distinct, weight, no two words share 4 ones
A54_8_7_4205.txt: M=4205 n=54 w=7 distinct, weight w, no two words share 4 ones, so min distance >= 8 PASS
checker verdict: PASS
== check_cw.py skipped (numpy is not installed; it is optional)
== negative control 1: a copy whose last word is replaced by a copy of the first word must FAIL
negative control 1 rejected as expected
== negative control 2: the same object checked against a claim of one more word must FAIL
negative control 2 rejected as expected
== negative control 3: a copy with the last word moved to a word sharing 4 ones with the first must FAIL
negative control 3 rejected as expected
ALL CHECKS PASS
```
