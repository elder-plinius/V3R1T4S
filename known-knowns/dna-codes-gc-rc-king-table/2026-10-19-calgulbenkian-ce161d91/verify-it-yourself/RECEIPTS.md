# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run by the claim-folder builder on 2026-10-19:

```
sha256 matches INDEX.csv (ce161d919503237b51c6e106f34671091efa38bbb9099376dcefb260b31f302b)
== check_dna.py on object/gc_rc_9_5_4.txt (n=9, d=5, w=4, mode gcrc)
c_length: PASS
c_alphabet: PASS
c_distinct: PASS
c_gc: PASS
c_hamming: PASS
c_rc: PASS
{"VALID": true, "c_alphabet": true, "c_distinct": true, "c_gc": true, "c_hamming": true, "c_length": true, "c_rc": true, "d": 5, "min_hamming": 5, "min_rc_distance": 5, "mode": "gcrc", "n": 9, "size": 72, "w": 4}
checker verdict: PASS (VALID=True, size=72, w=4)
== negative control 1: the last word replaced by a copy of the first word must FAIL
negative control 1 rejected as expected (VALID false)
== negative control 2: one letter of the first word changed so that its GC count is wrong must FAIL
negative control 2 rejected as expected (VALID false)
ALL CHECKS PASS
```
