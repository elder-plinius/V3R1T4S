# Receipts: real output of the checks, <22x22x23>

Produced by running `sh verify-it-yourself/run_checks.sh` from claim/ (as `nice /usr/bin/time -l sh verify-it-yourself/run_checks.sh`) on a MacBook with an Apple M4 Pro, 24 GB, macOS 26.6.1, Python 3.14.7, numpy 2.5.3 (the system python3 of that machine, run with -I), at 2026-10-24T22:52:44Z to 2026-10-24T22:53:29Z UTC, exit code 0. The laptop was shared with another job (a background build of other cells) at the time, so the wall times are upper bounds.

- Whole script: 46 s wall, maximum resident set size 1.30 GB (the largest process: one of the two checkers).
- Check 1 (check_brent_stdlib.py, standard library only): 43 s. Check 2 (check_exact_np.py, numpy): 2 s.
- The two comment lines at the top of run_checks.sh that state time and memory (`About ... on a laptop; peak memory about ...`) and the same sentence in README.md were filled in with these numbers after the run; no code line of run_checks.sh was changed.

## Output of run_checks.sh (complete, unedited)

```
492ee6aa98869d87672300fc6bad94738cb8e7905650066d316e3903be92c5be u.txt (matches)
3d78b1a87e5450ac44a77c22aa1b9c406a20c833d804b9f27f044291b98864c4 v.txt (matches)
477a6d278146507c1324b04d8dcd299dc3a92d365d669c0a98dc20e1515f3c00 w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <22,22,23> (A 22x22, B 22x23), 5423 terms, terms with a zero factor: 0
nonzeros u 200399, v 290632, w 116087; denominators occurring [2, 3, 4, 6, 9, 11, 12, 16, 18, 22, 36, 48, 144, 176, 352, 2816]
least common denominator of each factor matrix: U 25344, V 144, W 144
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 123921424 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 525533184
random exact evaluation 1 (seed 20261024): 0 of 506 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 506 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 506 entries of C differ from AB
rank-5423 scheme for <22,22,23> over Q: all Brent equations hold exactly
PASS
check 1 took 43 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <22,22,23> (A 22x22, B 22x23), 5423 terms, terms with a zero factor: 0
nonzeros u 200399, v 290632, w 116087; LCD per factor matrix: U 25344, V 144, W 144
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/484, wrong so far 0, 0s
  slab 100/484, wrong so far 0, 1s
  slab 200/484, wrong so far 0, 1s
  slab 300/484, wrong so far 0, 1s
  slab 400/484, wrong so far 0, 1s
Brent equations: 123921424 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 525533184; max slab bound 1122372292091904 (< 2^50)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 506 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 506 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 506 entries of C differ from AB
rank-5423 scheme for <22,22,23> over Q: all Brent equations hold exactly
PASS
check 2 took 2 s
PASS
```

## Negative controls (the checkers must reject altered objects)

Made by `verify-it-yourself/make_negative_controls.py` from the joined object: `neg_delete` is the object with term 1000 removed from all three factor files and the rank header lowered by one; `neg_coef` has one coefficient of u (first entry of term 7) increased by 1. Each was run through both checkers with `python3 -I <checker> <folder> --trials 3 --seed 20261024`; all four must exit nonzero and print FAIL.

| control | checker | exit code | verdict | wall | max RSS |
|---|---|---|---|---|---|
| neg_delete | check_brent_stdlib.py | 1 | FAIL | 41 s | 1.15 GB |
| neg_delete | check_exact_np.py | 1 | FAIL | 2 s | 0.28 GB |
| neg_coef | check_brent_stdlib.py | 1 | FAIL | 48 s | 1.21 GB |
| neg_coef | check_exact_np.py | 1 | FAIL | 3 s | 0.27 GB |

Real output of the four runs (progress lines removed; the order of lines is as printed by the checkers):

```
--- neg_delete, check_brent_stdlib (started 2026-10-24T23:00:58Z; exit code 1; 41 s wall, max RSS 1.15 GB)
format <22,22,23> (A 22x22, B 22x23), 5422 terms, terms with a zero factor: 0
nonzeros u 200372, v 290585, w 116079; denominators occurring [2, 3, 4, 6, 9, 11, 12, 16, 18, 22, 36, 48, 144, 176, 352, 2816]
least common denominator of each factor matrix: U 25344, V 144, W 144
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 123921424 checked (all index triples), 10152 wrong; scaling Du*Dv*Dw = 525533184
problem: 10152 Brent equations fail
FAIL
--- neg_delete, check_exact_np (started 2026-10-24T23:01:39Z; exit code 1; 2 s wall, max RSS 0.28 GB)
format <22,22,23> (A 22x22, B 22x23), 5422 terms, terms with a zero factor: 0
nonzeros u 200372, v 290585, w 116079; LCD per factor matrix: U 25344, V 144, W 144
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 123921424 checked (all index triples), 10152 wrong; D = Du*Dv*Dw = 525533184; max slab bound 1122329723904000 (< 2^50)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 8 of 506 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 8 of 506 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 8 of 506 entries of C differ from AB
problem: 10152 Brent equations fail, 24 random-evaluation entries differ
FAIL
--- neg_coef, check_brent_stdlib (started 2026-10-24T23:01:42Z; exit code 1; 48 s wall, max RSS 1.21 GB)
format <22,22,23> (A 22x22, B 22x23), 5423 terms, terms with a zero factor: 0
nonzeros u 200399, v 290632, w 116087; denominators occurring [2, 3, 4, 6, 9, 11, 12, 16, 18, 22, 36, 48, 144, 176, 352, 2816]
least common denominator of each factor matrix: U 25344, V 144, W 144
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 123921424 checked (all index triples), 184 wrong; scaling Du*Dv*Dw = 525533184
problem: 184 Brent equations fail
FAIL
--- neg_coef, check_exact_np (started 2026-10-24T23:02:30Z; exit code 1; 3 s wall, max RSS 0.27 GB)
format <22,22,23> (A 22x22, B 22x23), 5423 terms, terms with a zero factor: 0
nonzeros u 200399, v 290632, w 116087; LCD per factor matrix: U 25344, V 144, W 144
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 123921424 checked (all index triples), 184 wrong; D = Du*Dv*Dw = 525533184; max slab bound 1122372292091904 (< 2^50)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 506 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 506 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 506 entries of C differ from AB
problem: 184 Brent equations fail, 12 random-evaluation entries differ
FAIL
```

## Chunked-path test of check 2 (after the main run)

Check 2 (check_exact_np.py) has an exactness argument with a chunked int64 path for slabs whose bound reaches 2^53 (see its docstring). On this cell no slab reaches 2^53, so the chunked path did not run in run_checks.sh. To exercise it anyway, it was run once with the environment override CHECK_LIM53_TEST=2^46 (a testing hook in the checker that lowers the limit): 41 slabs went through the chunked path, 0 wrong equations, verdict below.

```
format <22,22,23> (A 22x22, B 22x23), 5423 terms, terms with a zero factor: 0
nonzeros u 200399, v 290632, w 116087; LCD per factor matrix: U 25344, V 144, W 144
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 123921424 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 525533184; max slab bound 1122372292091904 (< 2^50)
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 506 entries of C differ from AB
rank-5423 scheme for <22,22,23> over Q: all Brent equations hold exactly
PASS
```
