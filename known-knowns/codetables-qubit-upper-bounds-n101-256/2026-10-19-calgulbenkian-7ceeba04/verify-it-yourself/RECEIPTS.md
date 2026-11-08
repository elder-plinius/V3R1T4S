# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`, and INDEX.csv has the seven standard columns (the panel copy had one more, the closure value, now in the-record-we-beat/closure_of_others.txt). The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (7ceeba0422a356f681c95ebbfa42905b949d248d2e1501f991d14bf8e3440d03)
== qubit_cert_check.py (exact integers, excluded distance D = live upper bound 35) and propagation neighbours
PASS [[104,2]] no code with d >= 35 (shadow=True): value has 569 digits; 34 Q, 2 G, 33 H multipliers; all 105 columns <= 0
{"n": 104, "k": 2, "d": 35, "VALID": true}
PASS certificate excludes d >= 35 = live upper bound; new upper bound 34; one-step bound implied by live neighbours and merged/open PR values = 35 (>= 35: True); triage closure of everything else (all rules iterated, live table + 56 merged/open PR values + other cells of the batch) = 35
== negative control: all shadow multipliers removed (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
