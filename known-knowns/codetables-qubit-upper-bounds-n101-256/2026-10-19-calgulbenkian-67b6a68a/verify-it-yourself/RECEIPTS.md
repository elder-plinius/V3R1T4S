# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`, and INDEX.csv has the seven standard columns (the panel copy had one more, the closure value, now in the-record-we-beat/closure_of_others.txt). The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (67b6a68a5b0b71bf4b18453b38e0119dd4be72c9e789897bbc14d7da5095c071)
== qubit_cert_check.py (exact integers, excluded distance D = live upper bound 39) and propagation neighbours
PASS [[119,5]] no code with d >= 39 (shadow=True): value has 713 digits; 38 Q, 2 G, 36 H multipliers; all 120 columns <= 0
{"n": 119, "k": 5, "d": 39, "VALID": true}
PASS certificate excludes d >= 39 = live upper bound; new upper bound 38; one-step bound implied by live neighbours and merged/open PR values = 39 (>= 39: True); triage closure of everything else (all rules iterated, live table + 56 merged/open PR values + other cells of the batch) = 39
== negative control: all shadow multipliers removed (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
