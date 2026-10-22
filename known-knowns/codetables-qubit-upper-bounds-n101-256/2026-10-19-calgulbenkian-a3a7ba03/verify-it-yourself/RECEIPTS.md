# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`, and INDEX.csv has the seven standard columns (the panel copy had one more, the closure value, now in the-record-we-beat/closure_of_others.txt). The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (a3a7ba03a048421c32a1630e2ba1ec4784653e99b640c0cd4731abaa113f6ac4)
== qubit_cert_check.py (exact integers, excluded distance D = live upper bound 39) and propagation neighbours
PASS [[117,3]] no code with d >= 39 (shadow=True): value has 702 digits; 38 Q, 2 G, 38 H multipliers; all 118 columns <= 0
{"n": 117, "k": 3, "d": 39, "VALID": true}
PASS certificate excludes d >= 39 = live upper bound; new upper bound 38; one-step bound implied by live neighbours and merged/open PR values = 39 (>= 39: True); triage closure of everything else (all rules iterated, live table + 56 merged/open PR values + other cells of the batch) = 39
== negative control: all shadow multipliers removed (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
