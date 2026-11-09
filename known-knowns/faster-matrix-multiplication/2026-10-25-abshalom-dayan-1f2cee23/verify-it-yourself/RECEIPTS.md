# Receipts: real output of the checks, <26x27x27>

Produced by running `sh verify-it-yourself/run_checks.sh` from claim/ (as `nice /usr/bin/time -l sh verify-it-yourself/run_checks.sh`) on a MacBook with an Apple M4 Pro, 24 GB, macOS 26.6.1, Python 3.14.7, numpy 2.5.3 (the system python3 of that machine, run with -I), at 2026-10-24T22:58:11Z to 2026-10-24T22:59:28Z UTC, exit code 0. The laptop was shared with another job (a background build of other cells) at the time, so the wall times are upper bounds.

- Whole script: 77 s wall, maximum resident set size 1.32 GB (the largest process: one of the two checkers).
- Check 1 (check_brent_stdlib.py, standard library only): 73 s. Check 2 (check_exact_np.py, numpy): 4 s.
- The two comment lines at the top of run_checks.sh that state time and memory (`About ... on a laptop; peak memory about ...`) and the same sentence in README.md were filled in with these numbers after the run; no code line of run_checks.sh was changed.

## Output of run_checks.sh (complete, unedited)

```
1f2cee23872a890e45415b641ac56808453a6e71f7c448a7309dc2c19b659382 u.txt (matches)
9b2bbcffa370db4c8db54419f391a9c66369c4245686743f5e84dd81222ca033 v.txt (matches)
e1df758b5c8bd838cc3320988c76c5108490caae7f49638942079d916af3b8ff w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <26,27,27> (A 26x27, B 27x27), 8828 terms, terms with a zero factor: 0
nonzeros u 528101, v 211796, w 192935; denominators occurring [2, 4, 11, 20, 22, 41, 44, 82, 220, 820, 1640, 16400]
least common denominator of each factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 359254116 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 8731360000
random exact evaluation 1 (seed 20261024): 0 of 702 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 702 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 702 entries of C differ from AB
rank-8828 scheme for <26,27,27> over Q: all Brent equations hold exactly
PASS
check 1 took 73 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <26,27,27> (A 26x27, B 27x27), 8828 terms, terms with a zero factor: 0
nonzeros u 528101, v 211796, w 192935; LCD per factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/702, wrong so far 0, 1s
  slab 100/702, wrong so far 0, 1s
  slab 200/702, wrong so far 0, 1s
  slab 300/702, wrong so far 0, 1s
  slab 400/702, wrong so far 0, 1s
  slab 500/702, wrong so far 0, 2s
  slab 600/702, wrong so far 0, 2s
  slab 700/702, wrong so far 0, 2s
Brent equations: 359254116 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 8731360000; max slab bound 14059428076936000 (< 2^54)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 702 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 702 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 702 entries of C differ from AB
rank-8828 scheme for <26,27,27> over Q: all Brent equations hold exactly
PASS
check 2 took 4 s
PASS
```

## Negative controls (the checkers must reject altered objects)

Made by `verify-it-yourself/make_negative_controls.py` from the joined object: `neg_delete` is the object with term 1000 removed from all three factor files and the rank header lowered by one; `neg_coef` has one coefficient of u (first entry of term 7) increased by 1. Each was run through both checkers with `python3 -I <checker> <folder> --trials 3 --seed 20261024`; all four must exit nonzero and print FAIL.

| control | checker | exit code | verdict | wall | max RSS |
|---|---|---|---|---|---|
| neg_delete | check_brent_stdlib.py | 1 | FAIL | 82 s | 1.37 GB |
| neg_delete | check_exact_np.py | 1 | FAIL | 5 s | 0.51 GB |
| neg_coef | check_brent_stdlib.py | 1 | FAIL | 77 s | 1.38 GB |
| neg_coef | check_exact_np.py | 1 | FAIL | 6 s | 0.54 GB |

Real output of the four runs (progress lines removed; the order of lines is as printed by the checkers):

```
--- neg_delete, check_brent_stdlib (started 2026-10-24T23:13:32Z; exit code 1; 82 s wall, max RSS 1.37 GB)
format <26,27,27> (A 26x27, B 27x27), 8827 terms, terms with a zero factor: 0
nonzeros u 527975, v 211739, w 192857; denominators occurring [2, 4, 11, 20, 22, 41, 44, 82, 220, 820, 1640, 16400]
least common denominator of each factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 359254116 checked (all index triples), 560196 wrong; scaling Du*Dv*Dw = 8731360000
problem: 560196 Brent equations fail
FAIL
--- neg_delete, check_exact_np (started 2026-10-24T23:14:54Z; exit code 1; 5 s wall, max RSS 0.51 GB)
format <26,27,27> (A 26x27, B 27x27), 8827 terms, terms with a zero factor: 0
nonzeros u 527975, v 211739, w 192857; LCD per factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 359254116 checked (all index triples), 560196 wrong; D = Du*Dv*Dw = 8731360000; max slab bound 14057493719896000 (< 2^54)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 78 of 702 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 78 of 702 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 78 of 702 entries of C differ from AB
problem: 560196 Brent equations fail, 234 random-evaluation entries differ
FAIL
--- neg_coef, check_brent_stdlib (started 2026-10-24T23:14:59Z; exit code 1; 77 s wall, max RSS 1.38 GB)
format <26,27,27> (A 26x27, B 27x27), 8828 terms, terms with a zero factor: 0
nonzeros u 528101, v 211796, w 192935; denominators occurring [2, 4, 11, 20, 22, 41, 44, 82, 220, 820, 1640, 16400]
least common denominator of each factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 359254116 checked (all index triples), 32 wrong; scaling Du*Dv*Dw = 8731360000
problem: 32 Brent equations fail
FAIL
--- neg_coef, check_exact_np (started 2026-10-24T23:16:16Z; exit code 1; 6 s wall, max RSS 0.54 GB)
format <26,27,27> (A 26x27, B 27x27), 8828 terms, terms with a zero factor: 0
nonzeros u 528101, v 211796, w 192935; LCD per factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 359254116 checked (all index triples), 32 wrong; D = Du*Dv*Dw = 8731360000; max slab bound 14059428076936000 (< 2^54)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 702 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 702 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 702 entries of C differ from AB
problem: 32 Brent equations fail, 12 random-evaluation entries differ
FAIL
```

## Chunked-path test of check 2 (after the main run)

Check 2 (check_exact_np.py) has an exactness argument with a chunked int64 path for slabs whose bound reaches 2^53 (see its docstring). On this cell it runs naturally: in a run of check_exact_np.py with --json, 2 slabs of the 702 needed the chunked path, 0 wrong equations, verdict below. (A forced test with the testing hook CHECK_LIM53_TEST at 2^46 to 2^48 was tried and aborts on this cell because single terms exceed the lowered limit; the natural run is the test.)

```
format <26,27,27> (A 26x27, B 27x27), 8828 terms, terms with a zero factor: 0
nonzeros u 528101, v 211796, w 192935; LCD per factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 359254116 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 8731360000; max slab bound 14059428076936000 (< 2^54)
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 702 entries of C differ from AB
rank-8828 scheme for <26,27,27> over Q: all Brent equations hold exactly
PASS
```
