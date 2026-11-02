# Receipts: real output of the checks, <20x20x21>

Produced by running `sh verify-it-yourself/run_checks.sh` from claim/ (as `nice /usr/bin/time -l sh verify-it-yourself/run_checks.sh`) on a MacBook with an Apple M4 Pro, 24 GB, macOS 26.6.1, Python 3.14.7, numpy 2.5.3 (the system python3 of that machine, run with -I), at 2026-10-24T22:51:57Z to 2026-10-24T22:52:24Z UTC, exit code 0. The laptop was shared with another job (a background build of other cells) at the time, so the wall times are upper bounds.

- Whole script: 27 s wall, maximum resident set size 0.90 GB (the largest process: one of the two checkers).
- Check 1 (check_brent_stdlib.py, standard library only): 25 s. Check 2 (check_exact_np.py, numpy): 2 s.
- The two comment lines at the top of run_checks.sh that state time and memory (`About ... on a laptop; peak memory about ...`) and the same sentence in README.md were filled in with these numbers after the run; no code line of run_checks.sh was changed.

## Output of run_checks.sh (complete, unedited)

```
b97796005813233f1938c3de171c7e6782b6d2da05830bfe1ef5c4c54685645e u.txt (matches)
1d1d3f4fd9584afea8aed3c75ed028ecf03bc425f9f17f9ef0d6efc98b16e746 v.txt (matches)
b9b611abc1fd0048903f376452f96b2d09a6539329f6273588a4364e6ea4f330 w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <20,20,21> (A 20x20, B 20x21), 4230 terms, terms with a zero factor: 0
nonzeros u 145605, v 208778, w 87630; denominators occurring [2, 4, 7, 8, 14, 16, 29, 56, 112, 203, 1421]
least common denominator of each factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 70560000 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 285200384
random exact evaluation 1 (seed 20261024): 0 of 420 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 420 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 420 entries of C differ from AB
rank-4230 scheme for <20,20,21> over Q: all Brent equations hold exactly
PASS
check 1 took 25 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <20,20,21> (A 20x20, B 20x21), 4230 terms, terms with a zero factor: 0
nonzeros u 145605, v 208778, w 87630; LCD per factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/400, wrong so far 0, 0s
  slab 100/400, wrong so far 0, 0s
  slab 200/400, wrong so far 0, 0s
  slab 300/400, wrong so far 0, 0s
Brent equations: 70560000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 285200384; max slab bound 343591054054752 (< 2^49)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 420 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 420 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 420 entries of C differ from AB
rank-4230 scheme for <20,20,21> over Q: all Brent equations hold exactly
PASS
check 2 took 2 s
PASS
```

## Negative controls (the checkers must reject altered objects)

Made by `verify-it-yourself/make_negative_controls.py` from the joined object: `neg_delete` is the object with term 1000 removed from all three factor files and the rank header lowered by one; `neg_coef` has one coefficient of u (first entry of term 7) increased by 1. Each was run through both checkers with `python3 -I <checker> <folder> --trials 3 --seed 20261024`; all four must exit nonzero and print FAIL.

| control | checker | exit code | verdict | wall | max RSS |
|---|---|---|---|---|---|
| neg_delete | check_brent_stdlib.py | 1 | FAIL | 24 s | 0.88 GB |
| neg_delete | check_exact_np.py | 1 | FAIL | 2 s | 0.19 GB |
| neg_coef | check_brent_stdlib.py | 1 | FAIL | 24 s | 0.90 GB |
| neg_coef | check_exact_np.py | 1 | FAIL | 2 s | 0.18 GB |

Real output of the four runs (progress lines removed; the order of lines is as printed by the checkers):

```
--- neg_delete, check_brent_stdlib (started 2026-10-24T22:59:31Z; exit code 1; 24 s wall, max RSS 0.88 GB)
format <20,20,21> (A 20x20, B 20x21), 4229 terms, terms with a zero factor: 0
nonzeros u 145580, v 208735, w 87622; denominators occurring [2, 4, 7, 8, 14, 16, 29, 56, 112, 203, 1421]
least common denominator of each factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 70560000 checked (all index triples), 8600 wrong; scaling Du*Dv*Dw = 285200384
problem: 8600 Brent equations fail
FAIL
--- neg_delete, check_exact_np (started 2026-10-24T22:59:55Z; exit code 1; 2 s wall, max RSS 0.19 GB)
format <20,20,21> (A 20x20, B 20x21), 4229 terms, terms with a zero factor: 0
nonzeros u 145580, v 208735, w 87622; LCD per factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 70560000 checked (all index triples), 8600 wrong; D = Du*Dv*Dw = 285200384; max slab bound 343572801230176 (< 2^49)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 8 of 420 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 8 of 420 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 8 of 420 entries of C differ from AB
problem: 8600 Brent equations fail, 24 random-evaluation entries differ
FAIL
--- neg_coef, check_brent_stdlib (started 2026-10-24T22:59:57Z; exit code 1; 24 s wall, max RSS 0.90 GB)
format <20,20,21> (A 20x20, B 20x21), 4230 terms, terms with a zero factor: 0
nonzeros u 145605, v 208778, w 87630; denominators occurring [2, 4, 7, 8, 14, 16, 29, 56, 112, 203, 1421]
least common denominator of each factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 70560000 checked (all index triples), 168 wrong; scaling Du*Dv*Dw = 285200384
problem: 168 Brent equations fail
FAIL
--- neg_coef, check_exact_np (started 2026-10-24T23:00:21Z; exit code 1; 2 s wall, max RSS 0.18 GB)
format <20,20,21> (A 20x20, B 20x21), 4230 terms, terms with a zero factor: 0
nonzeros u 145605, v 208778, w 87630; LCD per factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 70560000 checked (all index triples), 168 wrong; D = Du*Dv*Dw = 285200384; max slab bound 343591054054752 (< 2^49)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 420 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 420 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 420 entries of C differ from AB
problem: 168 Brent equations fail, 12 random-evaluation entries differ
FAIL
```

## Chunked-path test of check 2 (after the main run)

Check 2 (check_exact_np.py) has an exactness argument with a chunked int64 path for slabs whose bound reaches 2^53 (see its docstring). On this cell no slab reaches 2^53, so the chunked path did not run in run_checks.sh. To exercise it anyway, it was run once with the environment override CHECK_LIM53_TEST=2^46 (a testing hook in the checker that lowers the limit): 19 slabs went through the chunked path, 0 wrong equations, verdict below.

```
format <20,20,21> (A 20x20, B 20x21), 4230 terms, terms with a zero factor: 0
nonzeros u 145605, v 208778, w 87630; LCD per factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 70560000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 285200384; max slab bound 343591054054752 (< 2^49)
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 420 entries of C differ from AB
rank-4230 scheme for <20,20,21> over Q: all Brent equations hold exactly
PASS
```
