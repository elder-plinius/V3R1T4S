# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 5 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`, and INDEX.csv has the seven standard columns (the panel copy had one more, the closure value, now in the-record-we-beat/closure_of_others.txt). The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (e5e68b962a2b56f0495d9446a99a9041aa8fa0846a9da8de8ba6989e42c055fa)
== qubit_cert_check.py (exact integers, excluded distance D = live upper bound 36) and propagation neighbours
PASS [[108,3]] no code with d >= 36 (shadow=True): value has 601 digits; 35 Q, 2 G, 33 H multipliers; all 109 columns <= 0
{"n": 108, "k": 3, "d": 36, "VALID": true}
PASS certificate excludes d >= 36 = live upper bound; new upper bound 35; one-step bound implied by live neighbours and merged/open PR values = 36 (>= 36: True); triage closure of everything else (all rules iterated, live table + 56 merged/open PR values + other cells of the batch) = 36
== negative control: all shadow multipliers removed (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
