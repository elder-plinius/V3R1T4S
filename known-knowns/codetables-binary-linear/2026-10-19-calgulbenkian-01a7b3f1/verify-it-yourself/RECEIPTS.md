# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`. The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (01a7b3f11d0b35810510fb80338c6a7f25f4d7e44606ec85fdd7c670f5e89662)
== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 40) and neighbour propagation
q=7 n=55 k=10 D=40 degree=7
f(0) = 7145717180865253961732487977/30501068176025076000  (approx 234277604.299840) ; q^k = 282475249
max over integers w in D..n of f(w) = -13207755302871499166543/26415511095982869119952000 (approx -5.000000e-04)
object field P_at_0_rational = 7145717180865253961732487977/30501068176025076000 (agrees: True)
{"q": 7, "n": 55, "k": 10, "D": 40, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}
PASS certificate excludes d >= D = live upper bound 40; new upper bound 39; best upper bound implied by the four live neighbours = 40 (>= D: True, so not implied)
== negative control: first multiplier made negative (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
