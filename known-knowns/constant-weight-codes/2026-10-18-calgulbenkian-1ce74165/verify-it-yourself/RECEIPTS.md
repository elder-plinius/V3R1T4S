# Receipts

Output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (macOS, system python3 3.9, standard library only; numpy was not installed, so the optional second checker was skipped):

```
sha256 matches INDEX.csv (1ce741658d4881c2b38b5d8b026e9181729916857f62b9427bedf8ca23351565)
== check_cw_std.py (standard library): count, distinct, weight, no two words share 8 ones
A27_8_11_2422.txt: M=2422 n=27 w=11 distinct, weight w, no two words share 8 ones, so min distance >= 8 PASS
checker verdict: PASS
== check_cw.py skipped (numpy is not installed; it is optional)
== negative control 1: a copy whose last word is replaced by a copy of the first word must FAIL
negative control 1 rejected as expected
== negative control 2: the same object checked against a claim of one more word must FAIL
negative control 2 rejected as expected
== negative control 3: a copy with the last word moved to a word sharing 8 ones with the first must FAIL
negative control 3 rejected as expected
ALL CHECKS PASS
```
