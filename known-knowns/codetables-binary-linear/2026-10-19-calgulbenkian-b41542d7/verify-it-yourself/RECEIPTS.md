# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`. The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (b41542d739724fe3b0e96093fb2aee3bee570bc59b5e80212aa97bbd16fc7584)
== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 45) and neighbour propagation
q=5 n=66 k=11 D=45 degree=7
f(0) = 780563323041959590575285019658599/18052872647294449094322360  (approx 43237624.188245) ; q^k = 48828125
max over integers w in D..n of f(w) = -215005848724218069709240936097/430012301591482311884182722641920 (approx -4.999993e-04)
object field P_at_0_rational = 780563323041959590575285019658599/18052872647294449094322360 (agrees: True)
{"q": 5, "n": 66, "k": 11, "D": 45, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}
PASS certificate excludes d >= D = live upper bound 45; new upper bound 44; best upper bound implied by the four live neighbours = 45 (>= D: True, so not implied)
== negative control: first multiplier made negative (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
