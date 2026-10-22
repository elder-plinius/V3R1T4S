# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder on 2026-10-19 (python3, standard library only). Wall time 1 s on the packager's machine.

Differences from the copy of this folder that the panel ran: the table files are read from `the-record-we-beat/` (the panel folder called it `table-record/`), the last output line is `PASS` instead of `ALL CHECKS PASS`. The checkers themselves are unchanged.

```
sha256 of object matches INDEX.csv (15d4c77a8595afddc79a2c9a96a7d24d7e9152fbb10258401b7def9dd6abfebb)
== lp_delsarte_check.py (exact Fractions, excluded distance D = live upper bound 56) and neighbour propagation
q=8 n=67 k=5 D=56 degree=3
f(0) = 2599266943397044/90226601905  (approx 28808.210533) ; q^k = 32768
max over integers w in D..n of f(w) = -444764489315164/889530443964507345 (approx -4.999992e-04)
object field P_at_0_rational = 2599266943397044/90226601905 (agrees: True)
{"q": 8, "n": 67, "k": 5, "D": 56, "f0_lt_qk": true, "max_f_le_0": true, "VALID": true}
PASS certificate excludes d >= D = live upper bound 56; new upper bound 55; best upper bound implied by the four live neighbours = 56 (>= D: True, so not implied)
== negative control: first multiplier made negative (must be rejected) (must be rejected)
PASS (negative control rejected)
PASS
```
