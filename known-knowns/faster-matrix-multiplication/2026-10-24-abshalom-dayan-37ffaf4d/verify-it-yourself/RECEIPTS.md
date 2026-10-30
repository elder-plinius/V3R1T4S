# RECEIPTS: real output of sh verify-it-yourself/run_checks.sh

Run from this folder, 2026-10-24T19:15:13Z to 19:16:28Z (UTC), 74 s wall clock (Apple M4 Pro laptop, Python 3.14, under nice).

```
37ffaf4dc24686ccb944605fd965f8b981088a74cf5246a54d6bcf5a2b665eca u.txt (matches)
5d15717baf763e44e9fb2808ff92335e66ec76f0940c0f75839a79a33ea4c5be v.txt (matches)
0f0a3d5cffe4ba63b5aa9a464c87abe0c17a501028c2d7f0d02cc128ea4fd93a w.txt (matches)
== check 1: all Brent equations exactly, plus 3 random exact evaluations (check_brent_stdlib.py)
format <18,18,19> (A 18x18, B 18x19), 3225 terms, terms with a zero factor: 0
nonzeros u 102579, v 145368, w 64253; denominators occurring [2, 4, 5, 7, 10, 12, 14, 25, 28, 50, 84, 300, 600, 1200]
least common denominator of each factor matrix: U 8400, V 84, W 84
pairs of terms sharing two proportional factors (mergeable): 0
Brent equations: 37896336 checked (all index triples), 0 wrong; scaling Du*Dv*Dw = 59270400
random exact evaluation 1 (seed 20261024): 0 of 342 entries of C differ from AB
random exact evaluation 2 (seed 20261024): 0 of 342 entries of C differ from AB
random exact evaluation 3 (seed 20261024): 0 of 342 entries of C differ from AB
rank-3225 scheme for <18,18,19> over Q: all Brent equations hold exactly
PASS
== check 2: second exact Brent-equation checker (check_scheme_second.py)
format <18,18,19>, 3225 terms, every term with three nonzero factors, common denominator 352800, 37896336 Brent equations checked, 0 wrong
rank 3225 scheme for <18,18,19> over Q verified exactly
PASS
PASS
```

Negative controls (the same two checkers on altered copies, 2026-10-24, run in the build folder): neg_delete is the
object with term 1000 removed from all three files (rank header 3224); neg_coef is the object with the first u
coefficient of term 7 changed from 1 to 2. Both are rejected:

```
== neg_delete (check_scheme.py, second checker)
format <18,18,19>, 3224 terms, every term with three nonzero factors, common denominator 352800, 37896336 Brent equations checked, 203202 wrong
FAIL
exit status 1
== neg_delete (check_brent_stdlib.py)
problem: 203202 Brent equations fail
FAIL
== neg_coef (check_scheme.py, second checker)
format <18,18,19>, 3225 terms, every term with three nonzero factors, common denominator 352800, 37896336 Brent equations checked, 152 wrong
FAIL
exit status 1
== neg_coef (check_brent_stdlib.py)
problem: 152 Brent equations fail
FAIL
```

"common denominator 352800" in the second checker's output is its scaling factor; the least common denominators are
U 8400, V 84 and W 84. check_scheme.py is the run-folder name of check_scheme_second.py.

Corrupted copy of this folder (one coefficient in object/w.txt changed): run_checks.sh prints the w.txt sha256
MISMATCH, both checkers report 1100 wrong Brent equations, and the last line is FAIL (exit status 1).
