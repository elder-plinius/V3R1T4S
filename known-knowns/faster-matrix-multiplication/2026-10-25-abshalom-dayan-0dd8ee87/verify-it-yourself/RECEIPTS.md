# Receipts: real output of the checks, <24x25x25>

Produced by running `sh verify-it-yourself/run_checks.sh` from claim/ (as `nice /usr/bin/time -l sh verify-it-yourself/run_checks.sh`) on a MacBook with an Apple M4 Pro, 24 GB, macOS 26.6.1, Python 3.14.7, numpy 2.5.3 (the system python3 of that machine, run with -I), at 2026-10-24T22:55:21Z to 2026-10-24T22:56:11Z UTC, exit code 0. The laptop was shared with another job (a background build of other cells) at the time, so the wall times are upper bounds.

- Whole script: 50 s wall, maximum resident set size 1.05 GB (the largest process: one of the two checkers).
- Check 1 (check_brent_stdlib.py, standard library only): 47 s. Check 2 (check_exact_np.py, numpy): 3 s.
- The two comment lines at the top of run_checks.sh that state time and memory (`About ... on a laptop; peak memory about ...`) and the same sentence in README.md were filled in with these numbers after the run; no code line of run_checks.sh was changed.

## Output of run_checks.sh (complete, unedited)

```
0dd8ee872815374dbea1c5ad46d2fa3d66b5513d5daf7e3deb924a7d11e146dc u.txt (matches)
2fa3c110aee729212f67c643abcb3ea16e7ace02aa005b5ea9078c9ebc8455dd v.txt (matches)
23207f290da58bb771cd3a713cf030e3916bb262c1fbd5db863eb04af2b7f42c w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <24,25,25> (A 24x25, B 25x25), 7157 terms, terms with a zero factor: 0
nonzeros u 398652, v 167772, w 152419; denominators occurring [2, 4, 5, 9, 10, 18, 20, 37, 45, 180, 333, 666, 2997, 5994]
least common denominator of each factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 225000000 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 1942056000
random exact evaluation 1 (seed 20261024): 0 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 600 entries of C differ from AB
rank-7157 scheme for <24,25,25> over Q: all Brent equations hold exactly
PASS
check 1 took 47 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <24,25,25> (A 24x25, B 25x25), 7157 terms, terms with a zero factor: 0
nonzeros u 398652, v 167772, w 152419; LCD per factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/600, wrong so far 0, 0s
  slab 100/600, wrong so far 0, 1s
  slab 200/600, wrong so far 0, 1s
  slab 300/600, wrong so far 0, 1s
  slab 400/600, wrong so far 0, 1s
  slab 500/600, wrong so far 0, 1s
Brent equations: 225000000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 1942056000; max slab bound 2118902173790580 (< 2^51)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
rank-7157 scheme for <24,25,25> over Q: all Brent equations hold exactly
PASS
check 2 took 3 s
PASS
```

## Negative controls (the checkers must reject altered objects)

Made by `verify-it-yourself/make_negative_controls.py` from the joined object: `neg_delete` is the object with term 1000 removed from all three factor files and the rank header lowered by one; `neg_coef` has one coefficient of u (first entry of term 7) increased by 1. Each was run through both checkers with `python3 -I <checker> <folder> --trials 3 --seed 20261024`; all four must exit nonzero and print FAIL.

| control | checker | exit code | verdict | wall | max RSS |
|---|---|---|---|---|---|
| neg_delete | check_brent_stdlib.py | 1 | FAIL | 53 s | 1.02 GB |
| neg_delete | check_exact_np.py | 1 | FAIL | 4 s | 0.35 GB |
| neg_coef | check_brent_stdlib.py | 1 | FAIL | 55 s | 1.05 GB |
| neg_coef | check_exact_np.py | 1 | FAIL | 5 s | 0.38 GB |

Real output of the four runs (progress lines removed; the order of lines is as printed by the checkers):

```
--- neg_delete, check_brent_stdlib (started 2026-10-24T23:06:33Z; exit code 1; 53 s wall, max RSS 1.02 GB)
format <24,25,25> (A 24x25, B 25x25), 7156 terms, terms with a zero factor: 0
nonzeros u 398536, v 167719, w 152347; denominators occurring [2, 4, 5, 9, 10, 18, 20, 37, 45, 180, 333, 666, 2997, 5994]
least common denominator of each factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 225000000 checked (all index triples), 442656 wrong; scaling Du*Dv*Dw = 1942056000
problem: 442656 Brent equations fail
FAIL
--- neg_delete, check_exact_np (started 2026-10-24T23:07:26Z; exit code 1; 4 s wall, max RSS 0.35 GB)
format <24,25,25> (A 24x25, B 25x25), 7156 terms, terms with a zero factor: 0
nonzeros u 398536, v 167719, w 152347; LCD per factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 225000000 checked (all index triples), 442656 wrong; D = Du*Dv*Dw = 1942056000; max slab bound 2118549603234060 (< 2^51)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 72 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 72 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 72 of 600 entries of C differ from AB
problem: 442656 Brent equations fail, 216 random-evaluation entries differ
FAIL
--- neg_coef, check_brent_stdlib (started 2026-10-24T23:07:30Z; exit code 1; 55 s wall, max RSS 1.05 GB)
format <24,25,25> (A 24x25, B 25x25), 7157 terms, terms with a zero factor: 0
nonzeros u 398652, v 167772, w 152419; denominators occurring [2, 4, 5, 9, 10, 18, 20, 37, 45, 180, 333, 666, 2997, 5994]
least common denominator of each factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 225000000 checked (all index triples), 32 wrong; scaling Du*Dv*Dw = 1942056000
problem: 32 Brent equations fail
FAIL
--- neg_coef, check_exact_np (started 2026-10-24T23:08:25Z; exit code 1; 5 s wall, max RSS 0.38 GB)
format <24,25,25> (A 24x25, B 25x25), 7157 terms, terms with a zero factor: 0
nonzeros u 398652, v 167772, w 152419; LCD per factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 225000000 checked (all index triples), 32 wrong; D = Du*Dv*Dw = 1942056000; max slab bound 2118902173790580 (< 2^51)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 600 entries of C differ from AB
problem: 32 Brent equations fail, 12 random-evaluation entries differ
FAIL
```

## Chunked-path test of check 2 (after the main run)

Check 2 (check_exact_np.py) has an exactness argument with a chunked int64 path for slabs whose bound reaches 2^53 (see its docstring). On this cell no slab reaches 2^53, so the chunked path did not run in run_checks.sh. To exercise it anyway, it was run once with the environment override CHECK_LIM53_TEST=2^48 (a testing hook in the checker that lowers the limit): 24 slabs went through the chunked path, 0 wrong equations, verdict below.

```
format <24,25,25> (A 24x25, B 25x25), 7157 terms, terms with a zero factor: 0
nonzeros u 398652, v 167772, w 152419; LCD per factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 225000000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 1942056000; max slab bound 2118902173790580 (< 2^51)
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
rank-7157 scheme for <24,25,25> over Q: all Brent equations hold exactly
PASS
```
