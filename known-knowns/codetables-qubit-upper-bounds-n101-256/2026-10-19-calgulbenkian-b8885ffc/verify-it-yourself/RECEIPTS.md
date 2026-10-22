# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`, and INDEX.csv has the seven standard columns (the panel copy had one more, the closure value, now in the-record-we-beat/closure_of_others.txt). The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (b8885ffcf45b3445a6e86ae60146ee6879e8c83b01f98456a533642db635be84)
== qubit_cert_check.py (exact integers, excluded distance D = live upper bound 37) and propagation neighbours
PASS [[112,4]] no code with d >= 37 (shadow=True): value has 651 digits; 36 Q, 2 G, 34 H multipliers; all 113 columns <= 0
{"n": 112, "k": 4, "d": 37, "VALID": true}
PASS certificate excludes d >= 37 = live upper bound; new upper bound 36; one-step bound implied by live neighbours and merged/open PR values = 37 (>= 37: True); triage closure of everything else (all rules iterated, live table + 56 merged/open PR values + other cells of the batch) = 37
== negative control: all shadow multipliers removed (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
