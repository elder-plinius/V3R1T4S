# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`, and INDEX.csv has the seven standard columns (the panel copy had one more, the closure value, now in the-record-we-beat/closure_of_others.txt). The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (44fa84d905d87798ace65c7848fff9c5d5c8edf894e5166e707ce3826564bff3)
== qubit_cert_check.py (exact integers, excluded distance D = live upper bound 41) and propagation neighbours
PASS [[124,3]] no code with d >= 41 (shadow=True): value has 788 digits; 40 Q, 2 G, 39 H multipliers; all 125 columns <= 0
{"n": 124, "k": 3, "d": 41, "VALID": true}
PASS certificate excludes d >= 41 = live upper bound; new upper bound 40; one-step bound implied by live neighbours and merged/open PR values = 41 (>= 41: True); triage closure of everything else (all rules iterated, live table + 56 merged/open PR values + other cells of the batch) = 41
== negative control: all shadow multipliers removed (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
