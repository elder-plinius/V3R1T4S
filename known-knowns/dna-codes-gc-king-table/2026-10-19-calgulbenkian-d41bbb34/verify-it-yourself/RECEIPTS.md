# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run by the claim-folder builder on 2026-10-19:

```
sha256 matches INDEX.csv (d41bbb3417f3d8da02bb9440e86e05c86a24e2d1829ebe115440a902b62e531e)
== check_dna.py on object/gc_13_9_6.txt (n=13, d=9, w=6, mode gc)
c_length: PASS
c_alphabet: PASS
c_distinct: PASS
c_gc: PASS
c_hamming: PASS
c_rc: PASS
{"VALID": true, "c_alphabet": true, "c_distinct": true, "c_gc": true, "c_hamming": true, "c_length": true, "c_rc": true, "d": 9, "min_hamming": 9, "mode": "gc", "n": 13, "size": 52, "w": 6}
checker verdict: PASS (VALID=True, size=52, w=6)
== negative control 1: the last word replaced by a copy of the first word must FAIL
negative control 1 rejected as expected (VALID false)
== negative control 2: one letter of the first word changed so that its GC count is wrong must FAIL
negative control 2 rejected as expected (VALID false)
ALL CHECKS PASS
```
