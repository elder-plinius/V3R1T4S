# Receipts: real output of the checks, <24x24x25>

Produced by running `sh verify-it-yourself/run_checks.sh` from claim/ (as `nice /usr/bin/time -l sh verify-it-yourself/run_checks.sh`) on a MacBook with an Apple M4 Pro, 24 GB, macOS 26.6.1, Python 3.14.7, numpy 2.5.3 (the system python3 of that machine, run with -I), at 2026-10-24T22:54:03Z to 2026-10-24T22:55:21Z UTC, exit code 0. The laptop was shared with another job (a background build of other cells) at the time, so the wall times are upper bounds.

- Whole script: 79 s wall, maximum resident set size 1.62 GB (the largest process: one of the two checkers).
- Check 1 (check_brent_stdlib.py, standard library only): 75 s. Check 2 (check_exact_np.py, numpy): 3 s.
- The two comment lines at the top of run_checks.sh that state time and memory (`About ... on a laptop; peak memory about ...`) and the same sentence in README.md were filled in with these numbers after the run; no code line of run_checks.sh was changed.

## Output of run_checks.sh (complete, unedited)

```
2054584dc35faa7426d99b2406acb3ea68e7798e12579b1b3d729c65c16cf044 u.txt (matches)
0e8f860801dba7fe48e4828b8611d178741433b3f4e13b195c18500face0ac10 v.txt (matches)
fb6a185d56543f959eda3385e43a469d5d698507fef0c8578f6ada96456c080a w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <24,24,25> (A 24x24, B 24x25), 6820 terms, terms with a zero factor: 0
nonzeros u 268829, v 394150, w 150124; denominators occurring [2, 4, 5, 9, 10, 18, 20, 37, 45, 90, 180, 333, 666, 2997, 5994]
least common denominator of each factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 207360000 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 1942056000
random exact evaluation 1 (seed 20261024): 0 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 600 entries of C differ from AB
rank-6820 scheme for <24,24,25> over Q: all Brent equations hold exactly
PASS
check 1 took 75 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <24,24,25> (A 24x24, B 24x25), 6820 terms, terms with a zero factor: 0
nonzeros u 268829, v 394150, w 150124; LCD per factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/576, wrong so far 0, 0s
  slab 100/576, wrong so far 0, 1s
  slab 200/576, wrong so far 0, 1s
  slab 300/576, wrong so far 0, 1s
  slab 400/576, wrong so far 0, 1s
  slab 500/576, wrong so far 0, 1s
Brent equations: 207360000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 1942056000; max slab bound 6929223523914240 (< 2^53)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
rank-6820 scheme for <24,24,25> over Q: all Brent equations hold exactly
PASS
check 2 took 3 s
PASS
```

## Negative controls (the checkers must reject altered objects)

Made by `verify-it-yourself/make_negative_controls.py` from the joined object: `neg_delete` is the object with term 1000 removed from all three factor files and the rank header lowered by one; `neg_coef` has one coefficient of u (first entry of term 7) increased by 1. Each was run through both checkers with `python3 -I <checker> <folder> --trials 3 --seed 20261024`; all four must exit nonzero and print FAIL.

| control | checker | exit code | verdict | wall | max RSS |
|---|---|---|---|---|---|
| neg_delete | check_brent_stdlib.py | 1 | FAIL | 83 s | 1.67 GB |
| neg_delete | check_exact_np.py | 1 | FAIL | 4 s | 0.36 GB |
| neg_coef | check_brent_stdlib.py | 1 | FAIL | 78 s | 1.70 GB |
| neg_coef | check_exact_np.py | 1 | FAIL | 4 s | 0.36 GB |

Real output of the four runs (progress lines removed; the order of lines is as printed by the checkers):

```
--- neg_delete, check_brent_stdlib (started 2026-10-24T23:03:45Z; exit code 1; 83 s wall, max RSS 1.67 GB)
format <24,24,25> (A 24x24, B 24x25), 6819 terms, terms with a zero factor: 0
nonzeros u 268737, v 394034, w 150052; denominators occurring [2, 4, 5, 9, 10, 18, 20, 37, 45, 90, 180, 333, 666, 2997, 5994]
least common denominator of each factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 207360000 checked (all index triples), 768384 wrong; scaling Du*Dv*Dw = 1942056000
problem: 768384 Brent equations fail
FAIL
--- neg_delete, check_exact_np (started 2026-10-24T23:05:08Z; exit code 1; 4 s wall, max RSS 0.36 GB)
format <24,24,25> (A 24x24, B 24x25), 6819 terms, terms with a zero factor: 0
nonzeros u 268737, v 394034, w 150052; LCD per factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 207360000 checked (all index triples), 768384 wrong; D = Du*Dv*Dw = 1942056000; max slab bound 6927534896511960 (< 2^53)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 72 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 72 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 72 of 600 entries of C differ from AB
problem: 768384 Brent equations fail, 216 random-evaluation entries differ
FAIL
--- neg_coef, check_brent_stdlib (started 2026-10-24T23:05:11Z; exit code 1; 78 s wall, max RSS 1.70 GB)
format <24,24,25> (A 24x24, B 24x25), 6820 terms, terms with a zero factor: 0
nonzeros u 268829, v 394150, w 150124; denominators occurring [2, 4, 5, 9, 10, 18, 20, 37, 45, 90, 180, 333, 666, 2997, 5994]
least common denominator of each factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 207360000 checked (all index triples), 200 wrong; scaling Du*Dv*Dw = 1942056000
problem: 200 Brent equations fail
FAIL
--- neg_coef, check_exact_np (started 2026-10-24T23:06:30Z; exit code 1; 4 s wall, max RSS 0.36 GB)
format <24,24,25> (A 24x24, B 24x25), 6820 terms, terms with a zero factor: 0
nonzeros u 268829, v 394150, w 150124; LCD per factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 207360000 checked (all index triples), 200 wrong; D = Du*Dv*Dw = 1942056000; max slab bound 6929223523914240 (< 2^53)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 600 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 600 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 600 entries of C differ from AB
problem: 200 Brent equations fail, 12 random-evaluation entries differ
FAIL
```

## Chunked-path test of check 2 (after the main run)

Check 2 (check_exact_np.py) has an exactness argument with a chunked int64 path for slabs whose bound reaches 2^53 (see its docstring). On this cell no slab reaches 2^53, so the chunked path did not run in run_checks.sh. To exercise it anyway, it was run once with the environment override CHECK_LIM53_TEST=2^48 (a testing hook in the checker that lowers the limit): 45 slabs went through the chunked path, 0 wrong equations, verdict below.

```
format <24,24,25> (A 24x24, B 24x25), 6820 terms, terms with a zero factor: 0
nonzeros u 268829, v 394150, w 150124; LCD per factor matrix: U 59940, V 180, W 180
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 207360000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 1942056000; max slab bound 6929223523914240 (< 2^53)
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 600 entries of C differ from AB
rank-6820 scheme for <24,24,25> over Q: all Brent equations hold exactly
PASS
```
