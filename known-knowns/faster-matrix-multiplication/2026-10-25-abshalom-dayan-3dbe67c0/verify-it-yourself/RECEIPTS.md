# Receipts: real output of the checks, <20x21x21>

Produced by running `sh verify-it-yourself/run_checks.sh` from claim/ (as `nice /usr/bin/time -l sh verify-it-yourself/run_checks.sh`) on a MacBook with an Apple M4 Pro, 24 GB, macOS 26.6.1, Python 3.14.7, numpy 2.5.3 (the system python3 of that machine, run with -I), at 2026-10-24T22:52:24Z to 2026-10-24T22:52:44Z UTC, exit code 0. The laptop was shared with another job (a background build of other cells) at the time, so the wall times are upper bounds.

- Whole script: 20 s wall, maximum resident set size 0.55 GB (the largest process: one of the two checkers).
- Check 1 (check_brent_stdlib.py, standard library only): 18 s. Check 2 (check_exact_np.py, numpy): 2 s.
- The two comment lines at the top of run_checks.sh that state time and memory (`About ... on a laptop; peak memory about ...`) and the same sentence in README.md were filled in with these numbers after the run; no code line of run_checks.sh was changed.

## Output of run_checks.sh (complete, unedited)

```
3dbe67c0fd5688bd563efe6b78a457f6f91111868199e5e3307a3dbc3d6b8604 u.txt (matches)
75acbc4537f71d57179eb8f296fc13016f3f9cc2d58aefdc63d6026c3aa9463b v.txt (matches)
d9fdcfe51666bc6023b62f4bcb158d34ad74b1710a15e6f0e2f3e69b8c87df95 w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <20,21,21> (A 20x21, B 21x21), 4471 terms, terms with a zero factor: 0
nonzeros u 211890, v 98908, w 89223; denominators occurring [2, 4, 7, 8, 14, 16, 29, 56, 112, 203, 1421]
least common denominator of each factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 77792400 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 285200384
random exact evaluation 1 (seed 20261024): 0 of 420 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 420 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 420 entries of C differ from AB
rank-4471 scheme for <20,21,21> over Q: all Brent equations hold exactly
PASS
check 1 took 18 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <20,21,21> (A 20x21, B 21x21), 4471 terms, terms with a zero factor: 0
nonzeros u 211890, v 98908, w 89223; LCD per factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/420, wrong so far 0, 0s
  slab 100/420, wrong so far 0, 0s
  slab 200/420, wrong so far 0, 0s
  slab 300/420, wrong so far 0, 1s
  slab 400/420, wrong so far 0, 1s
Brent equations: 77792400 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 285200384; max slab bound 124678617281232 (< 2^47)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 420 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 420 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 420 entries of C differ from AB
rank-4471 scheme for <20,21,21> over Q: all Brent equations hold exactly
PASS
check 2 took 2 s
PASS
```

## Negative controls (the checkers must reject altered objects)

Made by `verify-it-yourself/make_negative_controls.py` from the joined object: `neg_delete` is the object with term 1000 removed from all three factor files and the rank header lowered by one; `neg_coef` has one coefficient of u (first entry of term 7) increased by 1. Each was run through both checkers with `python3 -I <checker> <folder> --trials 3 --seed 20261024`; all four must exit nonzero and print FAIL.

| control | checker | exit code | verdict | wall | max RSS |
|---|---|---|---|---|---|
| neg_delete | check_brent_stdlib.py | 1 | FAIL | 16 s | 0.55 GB |
| neg_delete | check_exact_np.py | 1 | FAIL | 2 s | 0.20 GB |
| neg_coef | check_brent_stdlib.py | 1 | FAIL | 16 s | 0.55 GB |
| neg_coef | check_exact_np.py | 1 | FAIL | 2 s | 0.19 GB |

Real output of the four runs (progress lines removed; the order of lines is as printed by the checkers):

```
--- neg_delete, check_brent_stdlib (started 2026-10-24T23:00:23Z; exit code 1; 16 s wall, max RSS 0.55 GB)
format <20,21,21> (A 20x21, B 21x21), 4470 terms, terms with a zero factor: 0
nonzeros u 211846, v 98900, w 89215; denominators occurring [2, 4, 7, 8, 14, 16, 29, 56, 112, 203, 1421]
least common denominator of each factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 77792400 checked (all index triples), 2816 wrong; scaling Du*Dv*Dw = 285200384
problem: 2816 Brent equations fail
FAIL
--- neg_delete, check_exact_np (started 2026-10-24T23:00:39Z; exit code 1; 2 s wall, max RSS 0.20 GB)
format <20,21,21> (A 20x21, B 21x21), 4470 terms, terms with a zero factor: 0
nonzeros u 211846, v 98900, w 89215; LCD per factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 77792400 checked (all index triples), 2816 wrong; D = Du*Dv*Dw = 285200384; max slab bound 124676335678160 (< 2^47)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 8 of 420 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 8 of 420 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 8 of 420 entries of C differ from AB
problem: 2816 Brent equations fail, 24 random-evaluation entries differ
FAIL
--- neg_coef, check_brent_stdlib (started 2026-10-24T23:00:40Z; exit code 1; 16 s wall, max RSS 0.55 GB)
format <20,21,21> (A 20x21, B 21x21), 4471 terms, terms with a zero factor: 0
nonzeros u 211890, v 98908, w 89223; denominators occurring [2, 4, 7, 8, 14, 16, 29, 56, 112, 203, 1421]
least common denominator of each factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 77792400 checked (all index triples), 32 wrong; scaling Du*Dv*Dw = 285200384
problem: 32 Brent equations fail
FAIL
--- neg_coef, check_exact_np (started 2026-10-24T23:00:56Z; exit code 1; 2 s wall, max RSS 0.19 GB)
format <20,21,21> (A 20x21, B 21x21), 4471 terms, terms with a zero factor: 0
nonzeros u 211890, v 98908, w 89223; LCD per factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 77792400 checked (all index triples), 32 wrong; D = Du*Dv*Dw = 285200384; max slab bound 124678617281232 (< 2^47)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 420 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 420 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 420 entries of C differ from AB
problem: 32 Brent equations fail, 12 random-evaluation entries differ
FAIL
```

## Chunked-path test of check 2 (after the main run)

Check 2 (check_exact_np.py) has an exactness argument with a chunked int64 path for slabs whose bound reaches 2^53 (see its docstring). On this cell no slab reaches 2^53, so the chunked path did not run in run_checks.sh. To exercise it anyway, it was run once with the environment override CHECK_LIM53_TEST=2^46 (a testing hook in the checker that lowers the limit): 20 slabs went through the chunked path, 0 wrong equations, verdict below.

```
format <20,21,21> (A 20x21, B 21x21), 4471 terms, terms with a zero factor: 0
nonzeros u 211890, v 98908, w 89223; LCD per factor matrix: U 22736, V 112, W 112
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 77792400 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 285200384; max slab bound 124678617281232 (< 2^47)
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 420 entries of C differ from AB
rank-4471 scheme for <20,21,21> over Q: all Brent equations hold exactly
PASS
```
