# Receipts

Output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (macOS, system python3 3.9, standard library only; numpy was not installed, so the optional second checker was skipped):

```
sha256 matches INDEX.csv (e12d11fa604fd790d622442b7d96815ed8b129256b45507a9f09bff518cf27b1)
== check_cw_std.py (standard library): count, distinct, weight, no two words share 4 ones
A56_8_7_4691.txt: M=4691 n=56 w=7 distinct, weight w, no two words share 4 ones, so min distance >= 8 PASS
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
