# Receipts: real output of the checks, <30x31x31>

Produced by running `sh verify-it-yourself/run_checks.sh` from claim/ (as `nice /usr/bin/time -l sh verify-it-yourself/run_checks.sh`) on a MacBook with an Apple M4 Pro, 24 GB, macOS 26.6.1, Python 3.14.7, numpy 2.5.3 (the system python3 of that machine, run with -I), at 2026-10-25T07:41:28Z to 2026-10-25T07:44:06Z UTC, exit code 0. The four cells of this batch were run one at a time. The laptop was also running other jobs of the same owner at the time (load average at the start of this run: 10.14 10.10 10.08), so the wall times are upper bounds.

- Whole script: 158 s wall, maximum resident set size 2.36 GB (the largest process: one of the two checkers).
- Check 1 (check_brent_stdlib.py, standard library only): 148 s. Check 2 (check_exact_np.py, numpy): 10 s.
- The two comment lines at the top of run_checks.sh that state time and memory (`About ... on a laptop; peak memory about ...`) and the same sentence in README.md were filled in with these numbers after the run; no code line of run_checks.sh was changed.

## Output of run_checks.sh (complete, unedited)

```
1570401161925e32961aa2ad3cb58ac6c66b38b3e804fac3e9d7a195405da245 u.txt (matches)
ccae23a2fc6350bf299bfbf6b5df8ebab898741535a56a983e2285f681efcb3d v.txt (matches)
cfb52c03a37acf0d7c85b66db919ec6dcd32ef47203ac183c59a577426eabb42 w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <30,31,31> (A 30x31, B 31x31), 12906 terms, terms with a zero factor: 0
nonzeros u 877795, v 321688, w 294303; denominators occurring [2, 4, 7, 13, 14, 24, 26, 49, 52, 98, 312, 1176, 2352, 28224]
least common denominator of each factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 831168900 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 35716681728
random exact evaluation 1 (seed 20261024): 0 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 930 entries of C differ from AB
rank-12906 scheme for <30,31,31> over Q: all Brent equations hold exactly
PASS
check 1 took 148 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <30,31,31> (A 30x31, B 31x31), 12906 terms, terms with a zero factor: 0
nonzeros u 877795, v 321688, w 294303; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/930, wrong so far 0, 1s
  slab 100/930, wrong so far 0, 1s
  slab 200/930, wrong so far 0, 2s
  slab 300/930, wrong so far 0, 2s
  slab 400/930, wrong so far 0, 2s
  slab 500/930, wrong so far 0, 3s
  slab 600/930, wrong so far 0, 4s
  slab 700/930, wrong so far 0, 4s
  slab 800/930, wrong so far 0, 5s
  slab 900/930, wrong so far 0, 5s
Brent equations: 831168900 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 113569216608466944 (< 2^57)
exact Python-integer path used for 178 term-slab pairs (single contribution >= 2^53) in 30 of 930 slabs
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
rank-12906 scheme for <30,31,31> over Q: all Brent equations hold exactly
PASS
check 2 took 10 s
PASS
```

## Negative controls (the checkers must reject altered objects)

Made by `verify-it-yourself/make_negative_controls.py` from the joined object: `neg_delete` is the object with term 1000 removed from all three factor files and the rank header lowered by one; `neg_coef` has one coefficient of u (first entry of term 7) increased by 1. Each was run through both checkers with `python3 -I <checker> <folder> --trials 3 --seed 20261024`; all four must exit nonzero and print FAIL.

| control | checker | exit code | verdict | wall | max RSS |
|---|---|---|---|---|---|
| neg_delete | check_brent_stdlib.py | 1 | FAIL | 141 s | 2.36 GB |
| neg_delete | check_exact_np.py | 1 | FAIL | 11 s | 0.94 GB |
| neg_coef | check_brent_stdlib.py | 1 | FAIL | 160 s | 2.37 GB |
| neg_coef | check_exact_np.py | 1 | FAIL | 10 s | 0.94 GB |

Real output of the four runs (progress lines removed; the order of lines is as printed by the checkers):

```
--- neg_delete, check_brent_stdlib (started 2026-10-25T07:59:36Z; exit code 1; 141 s wall, max RSS 2.36 GB)
format <30,31,31> (A 30x31, B 31x31), 12905 terms, terms with a zero factor: 0
nonzeros u 877733, v 321678, w 294297; denominators occurring [2, 4, 7, 13, 14, 24, 26, 49, 52, 98, 312, 1176, 2352, 28224]
least common denominator of each factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 831168900 checked (all index triples), 3720 wrong; scaling Du*Dv*Dw = 35716681728
problem: 3720 Brent equations fail
FAIL
--- neg_delete, check_exact_np (started 2026-10-25T08:01:57Z; exit code 1; 11 s wall, max RSS 0.94 GB)
format <30,31,31> (A 30x31, B 31x31), 12905 terms, terms with a zero factor: 0
nonzeros u 877733, v 321678, w 294297; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 831168900 checked (all index triples), 3720 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 113568752291604480 (< 2^57)
exact Python-integer path used for 178 term-slab pairs (single contribution >= 2^53) in 30 of 930 slabs
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 6 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 6 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 6 of 930 entries of C differ from AB
problem: 3720 Brent equations fail, 18 random-evaluation entries differ
FAIL
--- neg_coef, check_brent_stdlib (started 2026-10-25T08:02:08Z; exit code 1; 160 s wall, max RSS 2.37 GB)
format <30,31,31> (A 30x31, B 31x31), 12906 terms, terms with a zero factor: 0
nonzeros u 877795, v 321688, w 294303; denominators occurring [2, 4, 7, 13, 14, 24, 26, 49, 52, 98, 312, 1176, 2352, 28224]
least common denominator of each factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 831168900 checked (all index triples), 32 wrong; scaling Du*Dv*Dw = 35716681728
problem: 32 Brent equations fail
FAIL
--- neg_coef, check_exact_np (started 2026-10-25T08:04:48Z; exit code 1; 10 s wall, max RSS 0.94 GB)
format <30,31,31> (A 30x31, B 31x31), 12906 terms, terms with a zero factor: 0
nonzeros u 877795, v 321688, w 294303; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 831168900 checked (all index triples), 32 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 113569216608466944 (< 2^57)
exact Python-integer path used for 178 term-slab pairs (single contribution >= 2^53) in 30 of 930 slabs
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 930 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 930 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 930 entries of C differ from AB
problem: 32 Brent equations fail, 12 random-evaluation entries differ
FAIL
```

## Tests of the large-number paths of check 2 (after the main run)

check_exact_np.py has three arithmetic paths (docstring, item 2): one float64 product per slab when the slab bound is below 2^53; chunks of terms (each chunk bound below 2^53) added as int64; and, for a term whose single contribution reaches 2^53, exact Python integers. Natural run of the shipped checker on this cell (`--trials 1 --seed 1`, 7 s wall, max RSS 0.94 GB): max slab bound 2^57, 2 of 930 slabs went through the chunked float path, 178 term-slab pairs (in 30 slabs) through the exact Python-integer path; 0 wrong equations; PASS. (The exact-integer path is needed natively on this cell: the numpy checker of the earlier batch would have stopped here.) Forced run with the testing hook CHECK_LIM53_TEST=2^40 (lowers the 2^53 limit so that all three paths run on this cell): max slab bound 2^57, 930 of 930 slabs went through the chunked float path, 24294 term-slab pairs (in 930 slabs) through the exact Python-integer path; 0 wrong equations; PASS.

Natural run:

```
format <30,31,31> (A 30x31, B 31x31), 12906 terms, terms with a zero factor: 0
nonzeros u 877795, v 321688, w 294303; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 831168900 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 113569216608466944 (< 2^57)
exact Python-integer path used for 178 term-slab pairs (single contribution >= 2^53) in 30 of 930 slabs
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
rank-12906 scheme for <30,31,31> over Q: all Brent equations hold exactly
PASS
```

Forced run (CHECK_LIM53_TEST=2^40):

```
format <30,31,31> (A 30x31, B 31x31), 12906 terms, terms with a zero factor: 0
nonzeros u 877795, v 321688, w 294303; LCD per factor matrix: U 366912, V 312, W 312
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 831168900 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 35716681728; max slab bound 113569216608466944 (< 2^57)
exact Python-integer path used for 24294 term-slab pairs (single contribution >= 2^53) in 930 of 930 slabs
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 930 entries of C differ from AB
rank-12906 scheme for <30,31,31> over Q: all Brent equations hold exactly
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
