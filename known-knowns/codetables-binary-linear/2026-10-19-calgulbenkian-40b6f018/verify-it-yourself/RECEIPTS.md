# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only; a C compiler was present, so the C cross-check ran). Wall time 4 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`. The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (40b6f0180e9248f1b86c69053b8c5e200f01156b917179cc619c63f659469d81)
== mindist_gf4.py (exact minimum distance by full enumeration of all 4^10 messages; rank; comparison with the live bounds)
{"n": 157, "k": 10, "messages_nonzero": 1048575, "expected": 1048575, "rank_k": true, "min_distance": 102, "A_d": 5304, "claimed_d": 102}
PASS rank k: True; exact d=102; live lower=101 (d > lower: True); live upper=110 (d <= upper: True); A_d=5304
== second implementation in C (only if a C compiler is available)
n=157 k=10 messages=1048575 rank_deficient=no min_distance=102 A_d=5304
C implementation agrees
== negative control: generator row 2 replaced by a copy of row 1 (rank deficient) (must be rejected)
PASS (negative control rejected)
PASS
```
