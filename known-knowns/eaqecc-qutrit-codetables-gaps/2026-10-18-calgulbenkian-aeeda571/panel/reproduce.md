# Reproduce report: qutrit-33-3-23-24

context: Claude Code subagent, fresh context
role: reproduce

Step 1: shasum -a 256 -c on the contributor's hash list run inside the package folder: every listed file reported OK (0 failures). All work was then done on a private copy of the package folder; no network was used.

## Definition (quoted from the target's success criterion)
"with s independent generators on Alice's n qutrits, c = rank(S J S^T)/2 (half the rank of the symplectic commutation matrix) and k = n - s + c; the minimum distance d, computed exactly as the minimum weight of vectors in the symplectic dual of span(S) that are not in the isotropic part span(S) ∩ span(S)^perp (the EAQECC definition used by Grassl), is STRICTLY GREATER (direction: max) than the table's d_lower for that (n,k,c), and d <= d_upper. Results for c = 0 are excluded."

## My checker (written before reading verify-it-yourself/)
My own checker (Python, GF(3) row reduction written from scratch) and a C enumeration program, neither shipped in this package. Steps: s = rank(S); G = S J S^T with J = [[0,I],[-I,0]]; c = rank(G)/2; k = n - s + c; the symplectic dual is the GF(3) null space of S J (dimension 2n - s); the isotropic part span(S) ∩ dual is obtained as {S^T y : G y = 0}; a basis of the dual is built with the isotropic part first, then a complement. The C program visits every coefficient vector of the dual basis (3^dim vectors) whose complement coefficients are not all zero, i.e. every dual vector outside the isotropic part, and takes the minimum symplectic weight (number of positions i with (x_i, z_i) not (0,0)). The count of vectors visited is printed so it can be compared with 3^dim - 3^isotropic_dim.

Calibration (hand-derived, three tiny cases run first): (A) n=3, S = {Z1 Z2^-1, Z2 Z3^-1}: Z1 alone is in the dual and outside span(S), so d=1 (program: s=2, c=0, k=1, d=1). (B) n=3, S = {XXX, ZZZ}: weight 1 is impossible (sum of x-parts = 0 and sum of z-parts = 0), X1 X2^-1 is in the dual and outside span(S), so d=2 (program: d=2). (C) n=2, S = {X1, Z1}: s=2, c=1, k=1, dual = span{X2, Z2}, d=1 (program: s=2, c=1, k=1, d=1). All three matched.

## Command and real output
Own checker, run on the calibration cases and then on the object file under object/ (the output is shown below):

```
calibA expect s=2 c=0 k=1 d=1: n=3 s=2 rank(SJS^T)=0 c=0 k=1 dual_dim=4 radical_dim=2 | min_weight=1 count_at_min=6 vectors_tested=72
calibB expect s=2 c=0 k=1 d=2: n=3 s=2 rank(SJS^T)=0 c=0 k=1 dual_dim=4 radical_dim=2 | min_weight=2 count_at_min=24 vectors_tested=72
calibC expect s=2 c=1 k=1 d=1: n=2 s=2 rank(SJS^T)=2 c=1 k=1 dual_dim=2 radical_dim=0 | min_weight=1 count_at_min=8 vectors_tested=8
eaqecc_33_3_23_24.json: n=33 s=54 rank(SJS^T)=48 c=24 k=3 dual_dim=12 radical_dim=6 | min_weight=23 count_at_min=1176 vectors_tested=530712
claimed n,k,c,d: 33 3 24 23
time: 0.29s user 0.03s system 96% cpu 0.338 total
independent numpy membership-by-rref method: total dual 531441 in span(S) 729 min wt outside span 23 min wt nonzero in span 25
```

## Clause-by-clause
- S is an integer matrix over GF(3) with 2n = 66 columns: yes (shape assertion in my checker).
- Independent generators: s equals the number of rows (see output above).
- c = rank(S J S^T)/2 = 24 >= 1 and k = n - s + c = 3: reproduced above, equal to the claimed values.
- Exact minimum distance by exhaustive enumeration: d = 23 (claimed 23). I visited 530712 = 3^12 - 3^6 vectors (all dual vectors outside the 6-dimensional isotropic part); the minimum weight is 23 (1176 vectors attain it). Second method (a small numpy script of mine, not shipped) takes all 3^12 = 531441 dual vectors, tests membership in span(S) by row reduction, and gives minimum weight outside span(S) = 23 (729 = 3^6 vectors are inside span(S); their own minimum nonzero weight is 25); it agrees.
- Table comparison, as stated in README.md for the cell [[33,3,22-30;24]]_3: d_lower = 22 < 23 <= d_upper = 30. I did not fetch the live table (not part of this role).

## Author's own run (after my checker)
PY set to the venv python, bash verify-it-yourself/run_checks.sh from my private copy (output shown below); a first run with the system python only failed on a numpy import, which I corrected by setting PY.

```
sha256 matches INDEX.csv (aeeda5718cc3d1662ff3fdba77996671c36d732aea511eb157b4667a3168a8a6)
== calibration on hand-derived cases
EA n=2 {X1X2, Z1Z2} s,c,k,d = (2, 1, 1, 2) expected (2, 1, 1, 2) OK
EA n=2 {X1, Z1} s,c,k,d = (2, 1, 1, 1) expected (2, 1, 1, 1) OK
cyclic [[5,1,3]]_3 s,c,k,d = (4, 0, 1, 3) expected (4, 0, 1, 3) OK
CALIBRATION PASS
== check_eaqecc.py on object/eaqecc_33_3_23_24.json (table cell dlower-dupper = 22-30)
file eaqecc_33_3_23_24.json n 33 s 54 c 24 k 3 dual_dim 12 isotropic_dim 6
exact minimum distance d = 23 (0.1 s)
  c>=1 True
  d==d_claimed True
  d>table_d_lower(22) True
  d<=table_d_upper(30) True
[[33,3,23;24]]_3 PASS
== negative control: a copy with one matrix entry changed must FAIL
negative control rejected as expected: FAIL
ALL CHECKS PASS
```

## Result
No mismatch. My independent checker and the author's checker agree on s, c, k and d. Both of my methods give d = 23.

pass: true
