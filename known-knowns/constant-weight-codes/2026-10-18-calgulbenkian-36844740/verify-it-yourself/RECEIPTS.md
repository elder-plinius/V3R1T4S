# Receipts

Output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (macOS, system python3 3.9, standard library only; numpy was not installed, so the optional second checker was skipped):

```
sha256 matches INDEX.csv (3684474037a4c99801649121c6515c307e50684c4652135eaba3767b5a1c1df5)
== check_cw_std.py (standard library): count, distinct, weight, no two words share 4 ones
A51_6_6_11187.txt: M=11187 n=51 w=6 distinct, weight w, no two words share 4 ones, so min distance >= 6 PASS
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
