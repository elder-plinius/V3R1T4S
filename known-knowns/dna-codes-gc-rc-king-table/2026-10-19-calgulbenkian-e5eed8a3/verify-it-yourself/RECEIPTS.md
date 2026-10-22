# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run by the claim-folder builder on 2026-10-19:

```
sha256 matches INDEX.csv (e5eed8a3ba787f959f144f130a6fe81dde0a14f60d6b7ed7d79a1f17df2fd852)
== check_dna.py on object/gc_rc_18_13_9.txt (n=18, d=13, w=9, mode gcrc)
c_length: PASS
c_alphabet: PASS
c_distinct: PASS
c_gc: PASS
c_hamming: PASS
c_rc: PASS
{"VALID": true, "c_alphabet": true, "c_distinct": true, "c_gc": true, "c_hamming": true, "c_length": true, "c_rc": true, "d": 13, "min_hamming": 13, "min_rc_distance": 13, "mode": "gcrc", "n": 18, "size": 36, "w": 9}
checker verdict: PASS (VALID=True, size=36, w=9)
== negative control 1: the last word replaced by a copy of the first word must FAIL
negative control 1 rejected as expected (VALID false)
== negative control 2: one letter of the first word changed so that its GC count is wrong must FAIL
negative control 2 rejected as expected (VALID false)
ALL CHECKS PASS
```
