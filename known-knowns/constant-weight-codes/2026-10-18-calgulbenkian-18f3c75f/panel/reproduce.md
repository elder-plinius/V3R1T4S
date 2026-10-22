# reproduce report: ub-29-6-11-164749

context: Claude Code subagent, fresh context [claude-sonnet-5-5]

Cell: ub-29-6-11-164749. Role: reproduce (exact rational re-check of a Delsarte LP upper-bound certificate). Scope: this report checks only that the saved certificate proves the stated bound; whether the table value is current or the result is new is for the other skeptics.

## Integrity
All files in the package folder matched the contributor's hash list (shasum -a 256 -c, zero non-OK lines). The folder was copied to a private workspace and all work was done there; no network. Certificate file: object/cert_A29_6_11.json, sha256 18f3c75f26d7a11dc8d9c94a4f4ce39d2a6024c31bd24b8b5f970ac434276cec.

## Definition used (written before opening verify-it-yourself/)
Independent exact Delsarte-bound checker for the Johnson scheme J(n,w).
Definition (Delsarte 1973): a constant-weight code C of length n, weight w, min Hamming distance d
has inner distribution a_i = (1/|C|) #{(x,y) in C^2 : |x\\y| = i}, i=0..w (Johnson distance i = Hamming/2),
a_0=1, a_i=0 for 0<i<d/2, a_i>=0, and for every eigenspace k=0..K (K=min(w,n-w)):
   sum_i a_i Q_k(i) >= 0,   Q_k(i) = m_k * E_i(k) / v_i,
 v_i = C(w,i)C(n-w,i), m_k = C(n,k)-C(n,k-1), E_i(k) = eigenvalue of distance-i graph (Eberlein)
 E_i(k) = sum_j (-1)^j C(k,j) C(w-k,i-j) C(n-w-k,i-j).
|C| = sum_i a_i. LP dual: y_k>=0 (k=1..K) with sum_k y_k (-Q_k(i)) >= 1 for every i in [d/2,w],
then |C| <= 1 + sum_k y_k m_k.   (k=0 row is the trivial |C|>=0 and is not used.)

Weak duality proof (re-derived): for a code with inner distribution a, 1 + sum_i a_i <= 1 + sum_i a_i sum_k y_k (-Q_k(i)) = 1 - sum_k y_k (sum_i a_i Q_k(i)) <= 1 + sum_k y_k m_k, using a_i >= 0, the dual constraint (each coefficient >= 1 for every allowed i = d/2..w), y_k >= 0, and sum_i a_i Q_k(i) >= -m_k (Delsarte inequality, Q_k(0) = m_k). Since |C| is an integer, |C| <= floor(objective). Only the dual vector y of the certificate is used; its other fields are ignored.

## Properties checked
1. Eberlein eigenvalues and Q matrix built from the definition; exact orthogonality relation sum_i E_i(k)E_i(l)/v_i = delta_kl C(n,w)/m_k verified for all k,l (self-test in the output).
2. All y_k are nonnegative and indexed within 1..min(w,n-w).
3. For every Johnson distance i from d/2 to w, sum_k y_k(-Q_k(i)) >= 1 exactly (Fraction arithmetic); the minimum is printed.
4. Objective 1 + sum_k y_k m_k computed exactly; its floor must equal the claimed U.
5. As a cross-check, my own exact simplex (Bland rule, Fractions) solves the primal LP for this cell; by LP duality its optimum must equal the dual objective if the certificate is optimal.

## Checker validation on cells with known answers (run before the cell checks)
Command: (own checker, run on the known-answer cells; not shipped in this package)
A(6,4,3) literature value 4; my exact LP optimum 4 (~4.0000), floor 4
A(7,4,3) literature value 7; my exact LP optimum 7 (~7.0000), floor 7
A(8,4,4) literature value 14; my exact LP optimum 14 (~14.0000), floor 14
A(10,4,5) literature value 36; my exact LP optimum 36 (~36.0000), floor 36
A(12,6,6) literature value 22; my exact LP optimum 22 (~22.0000), floor 22
A(9,4,3) literature value 12; my exact LP optimum 12 (~12.0000), floor 12
A(13,4,3) literature value 26; my exact LP optimum 26 (~26.0000), floor 26
A(12,4,6) literature value 132; my exact LP optimum 132 (~132.0000), floor 132
A(11,6,5) literature value 11; my exact LP optimum 11 (~11.0000), floor 11
A(10,6,5) literature value 6; my exact LP optimum 6 (~6.0000), floor 6
Fano inner distribution ['1', '0', '6', '0'] Q-transform ['7', '0', '0', '28']
neg control y=0 on A(8,4,4): (False, ['dual constraint i=2 violated: 0.0', 'dual constraint i=3 violated: 0.0', 'dual constraint i=4 violated: 0.0'])
neg control negative y: (False, ['negative y', 'dual constraint i=2 violated: 0.0', 'dual constraint i=3 violated: -3.5', 'dual constraint i=4 violated: -7.0'])


## My checker on this cell
Command: (own checker, run on object/cert_A29_6_11.json)
Full output:
```
orthogonality self-test J(29,11): ok
cell A(29,6,11); claimed U=164749; y indices [1, 2, 3, 4, 5, 6, 7, 8, 11]
dual feasible: True [] min over i of sum_k y_k(-Q_k(i)): 1 (>=1 required)
objective 1+sum y_k m_k = 164749 = 164749.0 floor 164749
my exact LP optimum: 164749 = 164749.0 floor 164749
author's lp_optimum field: 164749
RESULT: PASS A(29,6,11) <= 164749 (claimed 164749)
```
Second run output was identical to the first (determinism).

## Author's run_checks.sh (run only after my checker finished)
Command (from a private copy of the package): sh verify-it-yourself/run_checks.sh ; exit code 0. Output tail:
```
PASS: A(31,12,10) <= 197
== check_delsarte.py on object/cert_A29_6_11.json (exact dual feasibility, objective, floor)
A(29,6,11): exact dual objective 164749 = 164749.000000; floor 164749; claimed U 164749
certificate states lp_optimum 164749 match
primal point in certificate feasible: True  its objective: 164749
PASS: A(29,6,11) <= 164749
checker verdict: PASS
== negative control 1: the same certificate checked against a claim one smaller must FAIL
negative control 1 rejected as expected
== negative control 2: a copy with every dual value multiplied by 99/100 must FAIL (dual infeasible)
negative control 2 rejected as expected
== negative control 3: a copy with one dual value set negative must FAIL
negative control 3 rejected as expected
ALL CHECKS PASS
```
Comparison: author's checker and mine agree (same cell, same objective floor, both accept). The author's negative controls (claim one smaller, y scaled by 99/100, one negative y) were rejected as expected.

## Mismatches
None found in the certificate. Minor observation, not affecting this check: the certificate's bookkeeping field table_upper_bound need not equal the table-implied bound in README.md; that is a matter for the novelty and criterion skeptics. Also, the bound obtained is a pure Delsarte LP bound: the exact LP optimum of this cell equals the certificate objective, so no better integer bound can come from this LP.

Conclusion: the certificate is dual feasible and its exact objective has floor equal to the claimed value, so A(n,d,w) <= claimed U is reproduced from the shipped files, deterministically.

pass: true
