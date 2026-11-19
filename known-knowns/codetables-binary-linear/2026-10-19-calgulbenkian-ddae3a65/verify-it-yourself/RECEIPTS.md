# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`. The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (ddae3a6527a7b51d1eb559e5642b5e981a3ceae5ec12ed98b83faf3f5932e0be)
== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 72) and neighbour propagation
q=2 n=163 k=18 D=72 degree=5
f(0) = 138327920185042536516573/621000958767257068  (approx 222749.930144) ; q^k = 262144
max over integers w in D..n of f(w) = -731566217158668677/1463134713488272857396 (approx -4.999992e-04)
object field P_at_0_rational = 138327920185042536516573/621000958767257068 (agrees: True)
{"q": 2, "n": 163, "k": 18, "D": 72, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}
PASS certificate excludes d >= D = live upper bound 72; new upper bound 71; best upper bound implied by the four live neighbours = 72 (>= D: True, so not implied)
== negative control: first multiplier made negative (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
