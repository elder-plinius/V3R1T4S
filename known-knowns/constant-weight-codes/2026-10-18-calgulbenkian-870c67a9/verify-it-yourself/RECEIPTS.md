# Receipts

Output of `sh verify-it-yourself/run_checks.sh` run from the package folder on 2026-10-18 (Python 3.9.6, standard library only, `-I`):

```
sha256 matches INDEX.csv (870c67a9911cf7f568776eaabced06f0a547d080ca5f5b3f1f8dae8c3ebdac43)
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
== check_delsarte.py on object/cert_A29_6_12.json (exact dual feasibility, objective, floor)
A(29,6,12): exact dual objective 12564279/55 = 228441.436364; floor 228441; claimed U 228441
certificate states lp_optimum 12564279/55 match
primal point in certificate feasible: True  its objective: 12564279/55
PASS: A(29,6,12) <= 228441
checker verdict: PASS
== negative control 1: the same certificate checked against a claim one smaller must FAIL
negative control 1 rejected as expected
== negative control 2: a copy with every dual value multiplied by 99/100 must FAIL (dual infeasible)
negative control 2 rejected as expected
== negative control 3: a copy with one dual value set negative must FAIL
negative control 3 rejected as expected
ALL CHECKS PASS
```
