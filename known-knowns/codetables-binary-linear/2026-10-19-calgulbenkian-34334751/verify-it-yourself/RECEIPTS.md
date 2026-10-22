# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`. The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (343347514df7b4c3233d7f6878fcd82ce8ad4c82f0f12016789bc8fb98ecbf9a)
== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 72) and neighbour propagation
q=2 n=161 k=17 D=72 degree=5
f(0) = 1958438116783835926849340/17007312212901346441  (approx 115152.711508) ; q^k = 131072
max over integers w in D..n of f(w) = -4499877050070118905087143/8999827347913296037063001795 (approx -4.999959e-04)
object field P_at_0_rational = 1958438116783835926849340/17007312212901346441 (agrees: True)
{"q": 2, "n": 161, "k": 17, "D": 72, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}
PASS certificate excludes d >= D = live upper bound 72; new upper bound 71; best upper bound implied by the four live neighbours = 72 (>= D: True, so not implied)
== negative control: first multiplier made negative (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
