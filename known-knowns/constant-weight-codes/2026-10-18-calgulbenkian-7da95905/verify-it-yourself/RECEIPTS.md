# Receipts

Output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (macOS, system python3 3.9, standard library only; numpy was not installed, so the optional second checker was skipped):

```
sha256 matches INDEX.csv (7da959051e830cb64dbc8466a3ed10b049e7f648249222311b652cd3d261c8da)
== check_cw_std.py (standard library): count, distinct, weight, no two words share 4 ones
A45_8_7_1913.txt: M=1913 n=45 w=7 distinct, weight w, no two words share 4 ones, so min distance >= 8 PASS
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
