# Receipts: real output of the checks, <26x26x27>

Produced by running `sh verify-it-yourself/run_checks.sh` from claim/ (as `nice /usr/bin/time -l sh verify-it-yourself/run_checks.sh`) on a MacBook with an Apple M4 Pro, 24 GB, macOS 26.6.1, Python 3.14.7, numpy 2.5.3 (the system python3 of that machine, run with -I), at 2026-10-24T22:56:11Z to 2026-10-24T22:58:11Z UTC, exit code 0. The laptop was shared with another job (a background build of other cells) at the time, so the wall times are upper bounds.

- Whole script: 120 s wall, maximum resident set size 2.13 GB (the largest process: one of the two checkers).
- Check 1 (check_brent_stdlib.py, standard library only): 115 s. Check 2 (check_exact_np.py, numpy): 5 s.
- The two comment lines at the top of run_checks.sh that state time and memory (`About ... on a laptop; peak memory about ...`) and the same sentence in README.md were filled in with these numbers after the run; no code line of run_checks.sh was changed.

## Output of run_checks.sh (complete, unedited)

```
1d6c9f89e17717b7236f9bbbf46d6903e95f66a3965445cd8194bc23bd065d58 u.txt (matches)
bdcfa626ff98644b132c75ac00deebb2b9cb922116b7b44e00e63d2238f5da5a v.txt (matches)
9192310639d1141ba525574fac6735b5ce0507711ac0c8989a1f049b221aa48e w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <26,26,27> (A 26x26, B 26x27), 8437 terms, terms with a zero factor: 0
nonzeros u 352891, v 522808, w 190241; denominators occurring [2, 4, 11, 20, 22, 41, 44, 82, 220, 820, 1640, 16400]
least common denominator of each factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 333135504 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 8731360000
random exact evaluation 1 (seed 20261024): 0 of 702 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 702 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 702 entries of C differ from AB
rank-8437 scheme for <26,26,27> over Q: all Brent equations hold exactly
PASS
check 1 took 115 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <26,26,27> (A 26x26, B 26x27), 8437 terms, terms with a zero factor: 0
nonzeros u 352891, v 522808, w 190241; LCD per factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/676, wrong so far 0, 1s
  slab 100/676, wrong so far 0, 1s
  slab 200/676, wrong so far 0, 1s
  slab 300/676, wrong so far 0, 1s
  slab 400/676, wrong so far 0, 1s
  slab 500/676, wrong so far 0, 1s
  slab 600/676, wrong so far 0, 2s
Brent equations: 333135504 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 8731360000; max slab bound 49600548524296000 (< 2^56)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 702 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 702 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 702 entries of C differ from AB
rank-8437 scheme for <26,26,27> over Q: all Brent equations hold exactly
PASS
check 2 took 5 s
PASS
```

## Negative controls (the checkers must reject altered objects)

Made by `verify-it-yourself/make_negative_controls.py` from the joined object: `neg_delete` is the object with term 1000 removed from all three factor files and the rank header lowered by one; `neg_coef` has one coefficient of u (first entry of term 7) increased by 1. Each was run through both checkers with `python3 -I <checker> <folder> --trials 3 --seed 20261024`; all four must exit nonzero and print FAIL.

| control | checker | exit code | verdict | wall | max RSS |
|---|---|---|---|---|---|
| neg_delete | check_brent_stdlib.py | 1 | FAIL | 145 s | 2.02 GB |
| neg_delete | check_exact_np.py | 1 | FAIL | 6 s | 0.49 GB |
| neg_coef | check_brent_stdlib.py | 1 | FAIL | 146 s | 2.26 GB |
| neg_coef | check_exact_np.py | 1 | FAIL | 5 s | 0.48 GB |

Real output of the four runs (progress lines removed; the order of lines is as printed by the checkers):

```
--- neg_delete, check_brent_stdlib (started 2026-10-24T23:08:29Z; exit code 1; 145 s wall, max RSS 2.02 GB)
format <26,26,27> (A 26x26, B 26x27), 8436 terms, terms with a zero factor: 0
nonzeros u 352791, v 522682, w 190163; denominators occurring [2, 4, 11, 20, 22, 41, 44, 82, 220, 820, 1640, 16400]
least common denominator of each factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 333135504 checked (all index triples), 982800 wrong; scaling Du*Dv*Dw = 8731360000
problem: 982800 Brent equations fail
FAIL
--- neg_delete, check_exact_np (started 2026-10-24T23:10:55Z; exit code 1; 6 s wall, max RSS 0.49 GB)
format <26,26,27> (A 26x26, B 26x27), 8436 terms, terms with a zero factor: 0
nonzeros u 352791, v 522682, w 190163; LCD per factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 333135504 checked (all index triples), 982800 wrong; D = Du*Dv*Dw = 8731360000; max slab bound 49590324065656000 (< 2^56)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 78 of 702 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 78 of 702 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 78 of 702 entries of C differ from AB
problem: 982800 Brent equations fail, 234 random-evaluation entries differ
FAIL
--- neg_coef, check_brent_stdlib (started 2026-10-24T23:11:01Z; exit code 1; 146 s wall, max RSS 2.26 GB)
format <26,26,27> (A 26x26, B 26x27), 8437 terms, terms with a zero factor: 0
nonzeros u 352891, v 522808, w 190241; denominators occurring [2, 4, 11, 20, 22, 41, 44, 82, 220, 820, 1640, 16400]
least common denominator of each factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 333135504 checked (all index triples), 216 wrong; scaling Du*Dv*Dw = 8731360000
problem: 216 Brent equations fail
FAIL
--- neg_coef, check_exact_np (started 2026-10-24T23:13:27Z; exit code 1; 5 s wall, max RSS 0.48 GB)
format <26,26,27> (A 26x26, B 26x27), 8437 terms, terms with a zero factor: 0
nonzeros u 352891, v 522808, w 190241; LCD per factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 333135504 checked (all index triples), 216 wrong; D = Du*Dv*Dw = 8731360000; max slab bound 49600548524296000 (< 2^56)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 702 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 702 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 702 entries of C differ from AB
problem: 216 Brent equations fail, 12 random-evaluation entries differ
FAIL
```

## Chunked-path test of check 2 (after the main run)

Check 2 (check_exact_np.py) has an exactness argument with a chunked int64 path for slabs whose bound reaches 2^53 (see its docstring). On this cell it runs naturally: in a run of check_exact_np.py with --json, 25 slabs of the 676 needed the chunked path, 0 wrong equations, verdict below. (A forced test with the testing hook CHECK_LIM53_TEST at 2^46 to 2^48 was tried and aborts on this cell because single terms exceed the lowered limit; the natural run is the test.)

```
format <26,26,27> (A 26x26, B 26x27), 8437 terms, terms with a zero factor: 0
nonzeros u 352891, v 522808, w 190241; LCD per factor matrix: U 180400, V 220, W 220
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 333135504 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 8731360000; max slab bound 49600548524296000 (< 2^56)
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 702 entries of C differ from AB
rank-8437 scheme for <26,26,27> over Q: all Brent equations hold exactly
PASS
```
