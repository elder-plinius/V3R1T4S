# Receipts

Output of `sh verify-it-yourself/run_checks.sh`, run by the claim-folder builder on 2026-10-19:

```
sha256 matches INDEX.csv (c83bdf57b2cd3dbf6be677cd10c11c2ac26521c670fc925a71af39df802ebef7)
== check_dna.py on object/gc_13_10_6_24.txt (n=13, d=10, w=6, mode gc)
c_length: PASS
c_alphabet: PASS
c_distinct: PASS
c_gc: PASS
c_hamming: PASS
c_rc: PASS
{"VALID": true, "c_alphabet": true, "c_distinct": true, "c_gc": true, "c_hamming": true, "c_length": true, "c_rc": true, "d": 10, "min_hamming": 10, "mode": "gc", "n": 13, "size": 24, "w": 6}
checker verdict: PASS (VALID=True, size=24, w=6)
== negative control 1: the last word replaced by a copy of the first word must FAIL
negative control 1 rejected as expected (VALID false)
== negative control 2: one letter of the first word changed so that its GC count is wrong must FAIL
negative control 2 rejected as expected (VALID false)
ALL CHECKS PASS
```
