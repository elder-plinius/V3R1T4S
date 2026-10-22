# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run by the claim-folder builder on 2026-10-19:

```
sha256 matches INDEX.csv (32cb5a819ea735c442111cd93ad070114c86172d9a29043a15b09a6d5537943e)
== check_dna.py on object/gc_rc_10_7_5.txt (n=10, d=7, w=5, mode gcrc)
c_length: PASS
c_alphabet: PASS
c_distinct: PASS
c_gc: PASS
c_hamming: PASS
c_rc: PASS
{"VALID": true, "c_alphabet": true, "c_distinct": true, "c_gc": true, "c_hamming": true, "c_length": true, "c_rc": true, "d": 7, "min_hamming": 7, "min_rc_distance": 7, "mode": "gcrc", "n": 10, "size": 20, "w": 5}
checker verdict: PASS (VALID=True, size=20, w=5)
== negative control 1: the last word replaced by a copy of the first word must FAIL
negative control 1 rejected as expected (VALID false)
== negative control 2: one letter of the first word changed so that its GC count is wrong must FAIL
negative control 2 rejected as expected (VALID false)
ALL CHECKS PASS
```
