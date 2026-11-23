# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`. The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (8b17a05d526aa1c9c9a60a151ddcbddf0c59d09fd98333cc798c1ed6b23bd8e2)
== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 111) and neighbour propagation
q=4 n=153 k=7 D=111 degree=3
f(0) = 4553875121138905/347381819532  (approx 13109.134863) ; q^k = 16384
max over integers w in D..n of f(w) = -228728499114701/457457044068924372 (approx -4.999999e-04)
object field P_at_0_rational = 4553875121138905/347381819532 (agrees: True)
{"q": 4, "n": 153, "k": 7, "D": 111, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}
PASS certificate excludes d >= D = live upper bound 111; new upper bound 110; best upper bound implied by the four live neighbours = 111 (>= D: True, so not implied)
== negative control: first multiplier made negative (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
