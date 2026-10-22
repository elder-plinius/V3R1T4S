# Receipts

Output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (Python 3.9.6, standard library only, `-I`):

```
sha256 matches INDEX.csv (6b189cf6925d08bb3dd11e8632ce2a83f5f3782c233794de9734936f74b0373b)
== self-test of the checker on cells with known answers (exact Delsarte LP by vertex enumeration)
selftest A(6,4,3): eigenvalue orthogonality ok; exact Delsarte LP optimum 4 (best known A = 4)
selftest A(7,4,3): eigenvalue orthogonality ok; exact Delsarte LP optimum 7 (best known A = 7)
selftest A(8,4,4): eigenvalue orthogonality ok; exact Delsarte LP optimum 14 (best known A = 14)
selftest A(10,6,5): eigenvalue orthogonality ok; exact Delsarte LP optimum 6 (best known A = 6)
selftest A(9,4,3): eigenvalue orthogonality ok; exact Delsarte LP optimum 12 (best known A = 12)
SELFTEST OK
== known answer: merged certificate for A(31,12,10) must give 197
A(31,12,10): exact dual objective 8091/41 = 197.341463; floor 197; claimed U 197
certificate states lp_optimum 8091/41 match
primal point in certificate feasible: True  its objective: 8091/41
PASS: A(31,12,10) <= 197
== check_delsarte.py on object/cert_A35_12_12.json (exact dual feasibility, objective, floor)
A(35,12,12): exact dual objective 48694800/17531 = 2777.639610; floor 2777; claimed U 2777
certificate states lp_optimum 48694800/17531 match
primal point in certificate feasible: True  its objective: 48694800/17531
PASS: A(35,12,12) <= 2777
checker verdict: PASS
== negative control 1: the same certificate checked against a claim one smaller must FAIL
negative control 1 rejected as expected
== negative control 2: a copy with every dual value multiplied by 99/100 must FAIL (dual infeasible)
negative control 2 rejected as expected
== negative control 3: a copy with one dual value set negative must FAIL
negative control 3 rejected as expected
ALL CHECKS PASS
```
