# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`, and INDEX.csv has the seven standard columns (the panel copy had one more, the closure value, now in the-record-we-beat/closure_of_others.txt). The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (cc4972633cc4fe40a488858727afbe06e66cb0cc690224972b4b9510411837f4)
== qubit_cert_check.py (exact integers, excluded distance D = live upper bound 38) and propagation neighbours
PASS [[114,3]] no code with d >= 38 (shadow=True): value has 627 digits; 37 Q, 2 G, 35 H multipliers; all 115 columns <= 0
{"n": 114, "k": 3, "d": 38, "VALID": true}
PASS certificate excludes d >= 38 = live upper bound; new upper bound 37; one-step bound implied by live neighbours and merged/open PR values = 38 (>= 38: True); triage closure of everything else (all rules iterated, live table + 56 merged/open PR values + other cells of the batch) = 38
== negative control: all shadow multipliers removed (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
