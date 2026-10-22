# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run by the claim-folder builder on 2026-10-19:

```
sha256 matches INDEX.csv (d25fd24b3ad2f55fbc4dcc9df2f9bdf8c25bfe6e8ca612db05963f19fe0b7ad1)
== check_dna.py on object/gc_rc_12_8_6.txt (n=12, d=8, w=6, mode gcrc)
c_length: PASS
c_alphabet: PASS
c_distinct: PASS
c_gc: PASS
c_hamming: PASS
c_rc: PASS
{"VALID": true, "c_alphabet": true, "c_distinct": true, "c_gc": true, "c_hamming": true, "c_length": true, "c_rc": true, "d": 8, "min_hamming": 8, "min_rc_distance": 8, "mode": "gcrc", "n": 12, "size": 38, "w": 6}
checker verdict: PASS (VALID=True, size=38, w=6)
== negative control 1: the last word replaced by a copy of the first word must FAIL
negative control 1 rejected as expected (VALID false)
== negative control 2: one letter of the first word changed so that its GC count is wrong must FAIL
negative control 2 rejected as expected (VALID false)
ALL CHECKS PASS
```
