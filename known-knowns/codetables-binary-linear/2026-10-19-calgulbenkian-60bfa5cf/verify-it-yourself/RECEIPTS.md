# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only; a C compiler was present, so the C cross-check ran). Wall time 7 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`. The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (60bfa5cf703ab1750aabbe57c1bd8f9793fed9008adcfefde99cc1a6836f8474)
== mindist_gf4.py (exact minimum distance by full enumeration of all 4^11 messages; rank; comparison with the live bounds)
{"n": 160, "k": 11, "messages_nonzero": 4194303, "expected": 4194303, "rank_k": true, "min_distance": 102, "A_d": 2958, "claimed_d": 102}
PASS rank k: True; exact d=102; live lower=101 (d > lower: True); live upper=111 (d <= upper: True); A_d=2958
== second implementation in C (only if a C compiler is available)
n=160 k=11 messages=4194303 rank_deficient=no min_distance=102 A_d=2958
C implementation agrees
== negative control: generator row 2 replaced by a copy of row 1 (rank deficient) (must be rejected)
PASS (negative control rejected)
PASS
```
