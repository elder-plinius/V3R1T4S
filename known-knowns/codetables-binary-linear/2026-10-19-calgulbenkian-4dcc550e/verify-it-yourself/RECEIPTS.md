# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`. The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (4dcc550e39a57e8eb177a9765ac46586d28ea8efb9d55ad873425904d3d010fa)
== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 107) and neighbour propagation
q=4 n=148 k=7 D=107 degree=3
f(0) = 258051632794969/16695880740  (approx 15456.005994) ; q^k = 16384
max over integers w in D..n of f(w) = -3314519539249/6629049360174780 (approx -4.999992e-04)
object field P_at_0_rational = 258051632794969/16695880740 (agrees: True)
{"q": 4, "n": 148, "k": 7, "D": 107, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}
PASS certificate excludes d >= D = live upper bound 107; new upper bound 106; best upper bound implied by the four live neighbours = 107 (>= D: True, so not implied)
== negative control: first multiplier made negative (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
