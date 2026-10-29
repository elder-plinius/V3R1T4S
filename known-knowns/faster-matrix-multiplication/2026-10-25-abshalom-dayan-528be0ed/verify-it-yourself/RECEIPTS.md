# Receipts: real output of the checks, <30x30x31>

Produced by running `sh verify-it-yourself/run_checks.sh` from claim/ (as `nice /usr/bin/time -l sh verify-it-yourself/run_checks.sh`) on a MacBook with an Apple M4 Pro, 24 GB, macOS 26.6.1, Python 3.14.7, numpy 2.5.3 (the system python3 of that machine, run with -I), at 2026-10-25T07:44:06Z to 2026-10-25T07:47:55Z UTC, exit code 0. The four cells of this batch were run one at a time. The laptop was also running other jobs of the same owner at the time (load average at the start of this run: 11.12 10.41 10.20), so the wall times are upper bounds.

- Whole script: 230 s wall, maximum resident set size 3.79 GB (the largest process: one of the two checkers).
- Check 1 (check_brent_stdlib.py, standard library only): 219 s. Check 2 (check_exact_np.py, numpy): 10 s.
- The two comment lines at the top of run_checks.sh that state time and memory (`About ... on a laptop; peak memory about ...`) and the same sentence in README.md were filled in with these numbers after the run; no code line of run_checks.sh was changed.

## Output of run_checks.sh (complete, unedited)

```
528be0ed8aa1904d71bc1f59da284b0e3d9f66f4a2e01f01940bcb1ce1c0fb8c u.txt (matches)
da65b90d20b3a1589689d228a71b57910e80d6996174e64f39a848411b020bae v.txt (matches)
c53a02a35df88172c1cb9333c6763d2af9b016609d484d075b6e56bbc54c78aa w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <30,30,31> (A 30x30, B 30x31), 12395 terms, terms with a zero factor: 0
nonzeros u 576535, v 870728, w 290715; denominators occurring [2, 4, 7, 13, 24, 26, 49, 52, 98, 312, 1176, 2352, 28224]
least common denominator of each factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 778410000 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 35716681728
random exact evaluation 1 (seed 20261024): 0 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 930 entries of C differ from AB
rank-12395 scheme for <30,30,31> over Q: all Brent equations hold exactly
PASS
check 1 took 219 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <30,30,31> (A 30x30, B 30x31), 12395 terms, terms with a zero factor: 0
nonzeros u 576535, v 870728, w 290715; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/900, wrong so far 0, 1s
  slab 100/900, wrong so far 0, 1s
  slab 200/900, wrong so far 0, 2s
  slab 300/900, wrong so far 0, 2s
  slab 400/900, wrong so far 0, 3s
  slab 500/900, wrong so far 0, 4s
  slab 600/900, wrong so far 0, 4s
  slab 700/900, wrong so far 0, 5s
  slab 800/900, wrong so far 0, 5s
Brent equations: 778410000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 459266248437295104 (< 2^59)
exact Python-integer path used for 174 term-slab pairs (single contribution >= 2^53) in 29 of 900 slabs
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
rank-12395 scheme for <30,30,31> over Q: all Brent equations hold exactly
PASS
check 2 took 10 s
PASS
```

## Negative controls (the checkers must reject altered objects)

Made by `verify-it-yourself/make_negative_controls.py` from the joined object: `neg_delete` is the object with term 1000 removed from all three factor files and the rank header lowered by one; `neg_coef` has one coefficient of u (first entry of term 7) increased by 1. Each was run through both checkers with `python3 -I <checker> <folder> --trials 3 --seed 20261024`; all four must exit nonzero and print FAIL.

| control | checker | exit code | verdict | wall | max RSS |
|---|---|---|---|---|---|
| neg_delete | check_brent_stdlib.py | 1 | FAIL | 244 s | 3.80 GB |
| neg_delete | check_exact_np.py | 1 | FAIL | 10 s | 0.72 GB |
| neg_coef | check_brent_stdlib.py | 1 | FAIL | 222 s | 4.29 GB |
| neg_coef | check_exact_np.py | 1 | FAIL | 10 s | 0.72 GB |

Real output of the four runs (progress lines removed; the order of lines is as printed by the checkers):

```
--- neg_delete, check_brent_stdlib (started 2026-10-25T08:04:58Z; exit code 1; 244 s wall, max RSS 3.80 GB)
format <30,30,31> (A 30x30, B 30x31), 12394 terms, terms with a zero factor: 0
nonzeros u 576475, v 870636, w 290709; denominators occurring [2, 4, 7, 13, 24, 26, 49, 52, 98, 312, 1176, 2352, 28224]
least common denominator of each factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 778410000 checked (all index triples), 33120 wrong; scaling Du*Dv*Dw = 35716681728
problem: 33120 Brent equations fail
FAIL
--- neg_delete, check_exact_np (started 2026-10-25T08:09:02Z; exit code 1; 10 s wall, max RSS 0.72 GB)
format <30,30,31> (A 30x30, B 30x31), 12394 terms, terms with a zero factor: 0
nonzeros u 576475, v 870636, w 290709; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 778410000 checked (all index triples), 33120 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 459260212318083072 (< 2^59)
exact Python-integer path used for 174 term-slab pairs (single contribution >= 2^53) in 29 of 900 slabs
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 6 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 6 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 6 of 930 entries of C differ from AB
problem: 33120 Brent equations fail, 18 random-evaluation entries differ
FAIL
--- neg_coef, check_brent_stdlib (started 2026-10-25T08:09:12Z; exit code 1; 222 s wall, max RSS 4.29 GB)
format <30,30,31> (A 30x30, B 30x31), 12395 terms, terms with a zero factor: 0
nonzeros u 576535, v 870728, w 290715; denominators occurring [2, 4, 7, 13, 24, 26, 49, 52, 98, 312, 1176, 2352, 28224]
least common denominator of each factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 778410000 checked (all index triples), 248 wrong; scaling Du*Dv*Dw = 35716681728
problem: 248 Brent equations fail
FAIL
--- neg_coef, check_exact_np (started 2026-10-25T08:12:53Z; exit code 1; 10 s wall, max RSS 0.72 GB)
format <30,30,31> (A 30x30, B 30x31), 12395 terms, terms with a zero factor: 0
nonzeros u 576535, v 870728, w 290715; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 778410000 checked (all index triples), 248 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 459266248437295104 (< 2^59)
exact Python-integer path used for 174 term-slab pairs (single contribution >= 2^53) in 29 of 900 slabs
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 930 entries of C differ from AB
problem: 248 Brent equations fail, 12 random-evaluation entries differ
FAIL
```

## Tests of the large-number paths of check 2 (after the main run)

check_exact_np.py has three arithmetic paths (docstring, item 2): one float64 product per slab when the slab bound is below 2^53; chunks of terms (each chunk bound below 2^53) added as int64; and, for a term whose single contribution reaches 2^53, exact Python integers. Natural run of the shipped checker on this cell (`--trials 1 --seed 1`, 6 s wall, max RSS 0.69 GB): max slab bound 2^59, 57 of 900 slabs went through the chunked float path, 174 term-slab pairs (in 29 slabs) through the exact Python-integer path; 0 wrong equations; PASS. (The exact-integer path is needed natively on this cell: the numpy checker of the earlier batch would have stopped here.) Forced run with the testing hook CHECK_LIM53_TEST=2^40 (lowers the 2^53 limit so that all three paths run on this cell): max slab bound 2^59, 900 of 900 slabs went through the chunked float path, 131047 term-slab pairs (in 900 slabs) through the exact Python-integer path; 0 wrong equations; PASS.

Natural run:

```
format <30,30,31> (A 30x30, B 30x31), 12395 terms, terms with a zero factor: 0
nonzeros u 576535, v 870728, w 290715; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 778410000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 459266248437295104 (< 2^59)
exact Python-integer path used for 174 term-slab pairs (single contribution >= 2^53) in 29 of 900 slabs
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
rank-12395 scheme for <30,30,31> over Q: all Brent equations hold exactly
PASS
```

Forced run (CHECK_LIM53_TEST=2^40):

```
format <30,30,31> (A 30x30, B 30x31), 12395 terms, terms with a zero factor: 0
nonzeros u 576535, v 870728, w 290715; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 778410000 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 459266248437295104 (< 2^59)
exact Python-integer path used for 131047 term-slab pairs (single contribution >= 2^53) in 900 of 900 slabs
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
rank-12395 scheme for <30,30,31> over Q: all Brent equations hold exactly
PASS
```

## Calibration of the exact-integer path of check 2 (shared by the four cells of this batch)

The numpy checker of the earlier 8-cell batch stops with an assertion when a single term's contribution to a slab can reach 2^53 (its float64 matrix product would no longer be exact), and it did so on <30,31,31> in the overnight run (its log is in attempts/rebuild/out/band_30x31x31_check.log). This claim ships a version of check_exact_np.py that handles such terms with exact Python integers (see its docstring, item 2). To check that the change does not make the checker accept wrong objects, it was run on the <18,18,19> object of PR #714's package and on that package's two negative controls (`neg_delete`: term 1000 removed and the rank header lowered; `neg_coef`: one coefficient of u increased by 1; both made by make_negative_controls.py), natively and with the testing hook CHECK_LIM53_TEST lowering the limit to 2^30, so that every slab and thousands of terms go through the chunked and the exact-integer paths. Verdicts and counts of wrong equations must be identical in both modes, and the object must pass:

| input | limit of the float path | exit code | verdict | equations found wrong | term-slab pairs on the exact-integer path |
|---|---|---|---|---|---|
| 18x18x19_object | 2^53 (native) | 0 | PASS | 0 | 0 |
| 18x18x19_neg_coef | 2^53 (native) | 1 | FAIL | 152 | 0 |
| 18x18x19_neg_delete | 2^53 (native) | 1 | FAIL | 203202 | 0 |
| 18x18x19_object | 2^30 (CHECK_LIM53_TEST=1073741824) | 0 | PASS | 0 | 30076 |
| 18x18x19_neg_coef | 2^30 (CHECK_LIM53_TEST=1073741824) | 1 | FAIL | 152 | 30076 |
| 18x18x19_neg_delete | 2^30 (CHECK_LIM53_TEST=1073741824) | 1 | FAIL | 203202 | 30040 |

Real output (all six runs, `--trials 1 --seed 1`):

```
### 18x18x19_object limit=native
format <18,18,19> (A 18x18, B 18x19), 3225 terms, terms with a zero factor: 0
nonzeros u 102579, v 145368, w 64253; LCD per factor matrix: U 8400, V 84, W 84
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 37896336 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 59270400; max slab bound 37372720109760 (< 2^46)
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 342 entries of C differ from AB
rank-3225 scheme for <18,18,19> over Q: all Brent equations hold exactly
PASS
### exit code 0
### 18x18x19_neg_coef limit=native
format <18,18,19> (A 18x18, B 18x19), 3225 terms, terms with a zero factor: 0
nonzeros u 102579, v 145368, w 64253; LCD per factor matrix: U 8400, V 84, W 84
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 37896336 checked (all index triples), 152 wrong; D = Du*Dv*Dw = 59270400; max slab bound 37372720109760 (< 2^46)
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 4 of 342 entries of C differ from AB
problem: 152 Brent equations fail, 4 random-evaluation entries differ
FAIL
### exit code 1
### 18x18x19_neg_delete limit=native
format <18,18,19> (A 18x18, B 18x19), 3224 terms, terms with a zero factor: 0
nonzeros u 102526, v 145297, w 64199; LCD per factor matrix: U 8400, V 84, W 84
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 37896336 checked (all index triples), 203202 wrong; D = Du*Dv*Dw = 59270400; max slab bound 37357311317760 (< 2^46)
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 54 of 342 entries of C differ from AB
problem: 203202 Brent equations fail, 54 random-evaluation entries differ
FAIL
### exit code 1
### 18x18x19_object limit=1073741824
format <18,18,19> (A 18x18, B 18x19), 3225 terms, terms with a zero factor: 0
nonzeros u 102579, v 145368, w 64253; LCD per factor matrix: U 8400, V 84, W 84
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 37896336 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 59270400; max slab bound 37372720109760 (< 2^46)
exact Python-integer path used for 30076 term-slab pairs (single contribution >= 2^53) in 324 of 324 slabs
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 342 entries of C differ from AB
rank-3225 scheme for <18,18,19> over Q: all Brent equations hold exactly
PASS
### exit code 0
### 18x18x19_neg_coef limit=1073741824
format <18,18,19> (A 18x18, B 18x19), 3225 terms, terms with a zero factor: 0
nonzeros u 102579, v 145368, w 64253; LCD per factor matrix: U 8400, V 84, W 84
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 37896336 checked (all index triples), 152 wrong; D = Du*Dv*Dw = 59270400; max slab bound 37372720109760 (< 2^46)
exact Python-integer path used for 30076 term-slab pairs (single contribution >= 2^53) in 324 of 324 slabs
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 4 of 342 entries of C differ from AB
problem: 152 Brent equations fail, 4 random-evaluation entries differ
FAIL
### exit code 1
### 18x18x19_neg_delete limit=1073741824
format <18,18,19> (A 18x18, B 18x19), 3224 terms, terms with a zero factor: 0
nonzeros u 102526, v 145297, w 64199; LCD per factor matrix: U 8400, V 84, W 84
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 37896336 checked (all index triples), 203202 wrong; D = Du*Dv*Dw = 59270400; max slab bound 37357311317760 (< 2^46)
exact Python-integer path used for 30040 term-slab pairs (single contribution >= 2^53) in 324 of 324 slabs
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 54 of 342 entries of C differ from AB
problem: 203202 Brent equations fail, 54 random-evaluation entries differ
FAIL
### exit code 1
```
