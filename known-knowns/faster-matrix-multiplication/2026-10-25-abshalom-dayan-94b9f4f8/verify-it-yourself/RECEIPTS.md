# Receipts: real output of the checks, <28x29x29>

Produced by running `sh verify-it-yourself/run_checks.sh` from claim/ (as `nice /usr/bin/time -l sh verify-it-yourself/run_checks.sh`) on a MacBook with an Apple M4 Pro, 24 GB, macOS 26.6.1, Python 3.14.7, numpy 2.5.3 (the system python3 of that machine, run with -I), at 2026-10-25T07:37:33Z to 2026-10-25T07:39:08Z UTC, exit code 0. The four cells of this batch were run one at a time. The laptop was also running other jobs of the same owner at the time (load average at the start of this run: 11.83 9.92 10.03), so the wall times are upper bounds.

- Whole script: 95 s wall, maximum resident set size 1.82 GB (the largest process: one of the two checkers).
- Check 1 (check_brent_stdlib.py, standard library only): 89 s. Check 2 (check_exact_np.py, numpy): 6 s.
- The two comment lines at the top of run_checks.sh that state time and memory (`About ... on a laptop; peak memory about ...`) and the same sentence in README.md were filled in with these numbers after the run; no code line of run_checks.sh was changed.

## Output of run_checks.sh (complete, unedited)

```
94b9f4f822d17940b90b4aa712839b7cacdf0b6012636b885fb4f0ab509a188f u.txt (matches)
dbb972f623641fe34062aa8472a5001a0f9a8979f7e2c5aea9007368edf27a79 v.txt (matches)
831e7d2ebf430b9523457ca0832a5b4d0229ab8832af1846d6208def9e11da04 w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py, standard library only)
format <28,29,29> (A 28x29, B 29x29), 10739 terms, terms with a zero factor: 0
nonzeros u 686486, v 262924, w 240063; denominators occurring [2, 3, 4, 5, 6, 8, 11, 12, 15, 24, 44, 55, 66, 165, 264, 605, 1815]
least common denominator of each factor matrix: U 14520, V 264, W 264
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 554508304 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 1011985920
random exact evaluation 1 (seed 20261024): 0 of 812 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 812 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 812 entries of C differ from AB
rank-10739 scheme for <28,29,29> over Q: all Brent equations hold exactly
PASS
check 1 took 89 s
== check 2: second exact Brent-equation checker (check_exact_np.py, needs numpy)
format <28,29,29> (A 28x29, B 29x29), 10739 terms, terms with a zero factor: 0
nonzeros u 686486, v 262924, w 240063; LCD per factor matrix: U 14520, V 264, W 264
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
  slab 0/812, wrong so far 0, 1s
  slab 100/812, wrong so far 0, 1s
  slab 200/812, wrong so far 0, 1s
  slab 300/812, wrong so far 0, 2s
  slab 400/812, wrong so far 0, 2s
  slab 500/812, wrong so far 0, 2s
  slab 600/812, wrong so far 0, 3s
  slab 700/812, wrong so far 0, 3s
  slab 800/812, wrong so far 0, 3s
Brent equations: 554508304 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 1011985920; max slab bound 2323226025918072 (< 2^52)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 812 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 812 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 0 of 812 entries of C differ from AB
rank-10739 scheme for <28,29,29> over Q: all Brent equations hold exactly
PASS
check 2 took 6 s
PASS
```

## Negative controls (the checkers must reject altered objects)

Made by `verify-it-yourself/make_negative_controls.py` from the joined object: `neg_delete` is the object with term 1000 removed from all three factor files and the rank header lowered by one; `neg_coef` has one coefficient of u (first entry of term 7) increased by 1. Each was run through both checkers with `python3 -I <checker> <folder> --trials 3 --seed 20261024`; all four must exit nonzero and print FAIL.

| control | checker | exit code | verdict | wall | max RSS |
|---|---|---|---|---|---|
| neg_delete | check_brent_stdlib.py | 1 | FAIL | 92 s | 1.82 GB |
| neg_delete | check_exact_np.py | 1 | FAIL | 7 s | 0.71 GB |
| neg_coef | check_brent_stdlib.py | 1 | FAIL | 91 s | 1.82 GB |
| neg_coef | check_exact_np.py | 1 | FAIL | 7 s | 0.71 GB |

Real output of the four runs (progress lines removed; the order of lines is as printed by the checkers):

```
--- neg_delete, check_brent_stdlib (started 2026-10-25T07:47:58Z; exit code 1; 92 s wall, max RSS 1.82 GB)
format <28,29,29> (A 28x29, B 29x29), 10738 terms, terms with a zero factor: 0
nonzeros u 686350, v 262863, w 239979; denominators occurring [2, 3, 4, 5, 6, 8, 11, 12, 15, 24, 44, 55, 66, 165, 264, 605, 1815]
least common denominator of each factor matrix: U 14520, V 264, W 264
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 554508304 checked (all index triples), 696864 wrong; scaling Du*Dv*Dw = 1011985920
problem: 696864 Brent equations fail
FAIL
--- neg_delete, check_exact_np (started 2026-10-25T07:49:31Z; exit code 1; 7 s wall, max RSS 0.71 GB)
format <28,29,29> (A 28x29, B 29x29), 10738 terms, terms with a zero factor: 0
nonzeros u 686350, v 262863, w 239979; LCD per factor matrix: U 14520, V 264, W 264
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 554508304 checked (all index triples), 696864 wrong; D = Du*Dv*Dw = 1011985920; max slab bound 2322957305004072 (< 2^52)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 84 of 812 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 84 of 812 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 84 of 812 entries of C differ from AB
problem: 696864 Brent equations fail, 252 random-evaluation entries differ
FAIL
--- neg_coef, check_brent_stdlib (started 2026-10-25T07:49:38Z; exit code 1; 91 s wall, max RSS 1.82 GB)
format <28,29,29> (A 28x29, B 29x29), 10739 terms, terms with a zero factor: 0
nonzeros u 686486, v 262924, w 240063; denominators occurring [2, 3, 4, 5, 6, 8, 11, 12, 15, 24, 44, 55, 66, 165, 264, 605, 1815]
least common denominator of each factor matrix: U 14520, V 264, W 264
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 554508304 checked (all index triples), 32 wrong; scaling Du*Dv*Dw = 1011985920
problem: 32 Brent equations fail
FAIL
--- neg_coef, check_exact_np (started 2026-10-25T07:51:09Z; exit code 1; 7 s wall, max RSS 0.71 GB)
format <28,29,29> (A 28x29, B 29x29), 10739 terms, terms with a zero factor: 0
nonzeros u 686486, v 262924, w 240063; LCD per factor matrix: U 14520, V 264, W 264
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 554508304 checked (all index triples), 32 wrong; D = Du*Dv*Dw = 1011985920; max slab bound 2323226025918072 (< 2^52)
random exact evaluation 1 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 812 entries of C differ from AB
random exact evaluation 2 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 812 entries of C differ from AB
random exact evaluation 3 (seed 20261024, rational entries p/q, |p|<=20, q<=12): 4 of 812 entries of C differ from AB
problem: 32 Brent equations fail, 12 random-evaluation entries differ
FAIL
```

## Tests of the large-number paths of check 2 (after the main run)

check_exact_np.py has three arithmetic paths (docstring, item 2): one float64 product per slab when the slab bound is below 2^53; chunks of terms (each chunk bound below 2^53) added as int64; and, for a term whose single contribution reaches 2^53, exact Python integers. Natural run of the shipped checker on this cell (`--trials 1 --seed 1`, 5 s wall, max RSS 0.72 GB): max slab bound 2^52, 0 of 812 slabs went through the chunked float path, 0 term-slab pairs (in 0 slabs) through the exact Python-integer path; 0 wrong equations; PASS. (On this cell the exact-integer path is not needed natively.) Forced run with the testing hook CHECK_LIM53_TEST=2^40 (lowers the 2^53 limit so that all three paths run on this cell): max slab bound 2^52, 109 of 812 slabs went through the chunked float path, 2080 term-slab pairs (in 83 slabs) through the exact Python-integer path; 0 wrong equations; PASS.

Natural run:

```
format <28,29,29> (A 28x29, B 29x29), 10739 terms, terms with a zero factor: 0
nonzeros u 686486, v 262924, w 240063; LCD per factor matrix: U 14520, V 264, W 264
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 554508304 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 1011985920; max slab bound 2323226025918072 (< 2^52)
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 812 entries of C differ from AB
rank-10739 scheme for <28,29,29> over Q: all Brent equations hold exactly
PASS
```

Forced run (CHECK_LIM53_TEST=2^40):

```
format <28,29,29> (A 28x29, B 29x29), 10739 terms, terms with a zero factor: 0
nonzeros u 686486, v 262924, w 240063; LCD per factor matrix: U 14520, V 264, W 264
pairs of terms sharing two proportional factors (mergeable): uv 0, uw 0, vw 0
Brent equations: 554508304 checked (all index triples), 0 wrong; D = Du*Dv*Dw = 1011985920; max slab bound 2323226025918072 (< 2^52)
exact Python-integer path used for 2080 term-slab pairs (single contribution >= 2^53) in 83 of 812 slabs
random exact evaluation 1 (seed 1, rational entries p/q, |p|<=20, q<=12): 0 of 812 entries of C differ from AB
rank-10739 scheme for <28,29,29> over Q: all Brent equations hold exactly
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
