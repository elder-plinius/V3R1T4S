# Receipts: real output of verify-it-yourself/run_checks.sh

Run by the contributor's session (DmitrL-dev, AI-assisted) from this package folder on 2026-10-29T00:08:00Z (UTC), on an
Apple Silicon laptop (macOS, arm64, 8 GB RAM), with CADICAL and CAKE_LPR pointing to local builds of the pinned commits
(CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04, cake_lpr a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, built with the
commands of the script), so the script skipped its own builds. Exit status 0, 97 s wall time.

```
$ sh verify-it-yourself/run_checks.sh
== 1. regenerate the CNF named by object/cnf_spec.json (shipped encoder) and compare sha256 and header
regenerated CNF: 42644 variables, 148931 clauses, sha256 247ca74489c8144e2eca1fa1b7bfdd6c2f7f826e7deac2c46e4b3748c7069626
matches object/cnf_spec.json
== 2. upper bound: object/upper_bound_m2k5n14.json is an S_5 set of two tournaments on 14 vertices
m=2 k=5 n=14: 2002 k-subsets checked, 0 undominated -> PASS
== 3. the base clauses of the CNF are exactly Definition 2.2 for (m,k,n) = (2,5,13) (cnf_audit.py)
f.cnf: 148931 clauses; 1287 domination clauses over 1287 k-sets; 102960 defining clauses; 44684 added clauses
AUDIT OK
== 4. solver and verified checker
CaDiCaL 3.0.1
== 5. CaDiCaL with a text LRAT proof, then cake_lpr on the formula and the proof
s UNSATISFIABLE
s VERIFIED UNSAT
no S_5 set of two tournaments on 13 vertices (so none on fewer, by adding a vertex that loses to all): f(2,5) >= 14;
with the 14-vertex object of step 2: f(2,5) = 14
PASS
```

The same script with its own builds (no CADICAL / CAKE_LPR set) printed the same lines and PASS in 262 s on the same
laptop; the REPRODUCE panelist's run with its own builds of the same commits is in panel/reproduce.md (run A).
