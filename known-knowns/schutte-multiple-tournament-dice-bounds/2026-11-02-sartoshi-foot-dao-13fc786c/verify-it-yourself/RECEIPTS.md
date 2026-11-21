# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from a fresh copy of this package on 2026-11-02 (UTC) on an Apple M-series laptop, with no tools preinstalled (python-sat installed into a temporary venv; drat-trim and cake_lpr built at the pinned commits). The last summary line was reworded afterwards (its logic was stated backwards); the checks are unchanged.

```
== 0. object files match SHA256SUMS
object/certificate_m3k6n12.tsv ok
object/witness_m3k6n13.json ok
== 1. upper bound: object/witness_m3k6n13.json is an S_6 set of three tournaments on 13 vertices (Definition 2.1)
m=3 n=13 k=6 subsets=1716 undominated=0
PASS
== 2. python with python-sat 1.9.dev17
python-sat 1.9.dev17
== 3. job list = cover tree, and rebuilt CNFs match the object
1. encoder files: sha256 as recorded (cube.py, cube3.py, checker.py)
2. job list = cover tree of (3,6,12): 2871 jobs (62 cover, 126 leaf L1, 114 leaf L2, 2569 leaf L3)
3. CNFs rebuilt and matched (sha256, variables, clauses): 40 of 2871 jobs (seed 20261101)
PASS
== 4. drat-trim and cake_lpr at pinned commits
== 5. re-prove jobs: CaDiCaL 1.9.5 writes a DRAT proof, drat-trim turns it into LRAT, cake_lpr checks it
m3k6n12/COVER1: s VERIFIED UNSAT
m3k6n12/8_1_1_0-0-0-0_L3_3_1_1: s VERIFIED UNSAT
m3k6n12/10_0_1_0-0-0-0_L3_8_6_1: s VERIFIED UNSAT
m3k6n12/9_0_1_0-0-1-0_L3_4_3_4: s VERIFIED UNSAT
m3k6n12/10_0_1_0-0-0-0_L3_6_5_0: s VERIFIED UNSAT
m3k6n12/8_1_2_1-0-0-0_L3_6_6_0: s VERIFIED UNSAT
6 of 6 jobs re-proved and verified by cake_lpr (of 2,871 in the certificate)
no S_6 set of three tournaments on 12 vertices (all 2,871 cubes of the cover are UNSAT, as listed in the object);
an S_6 triple on fewer vertices would extend to 12 (add vertices that lose to all), so none exists: f(3,6) >= 13; with step 1, f(3,6) = 13
PASS
env -u CHECK_PYTHON -u DRAT_TRIM -u CAKE_LPR nice -n 19 sh   109.04s user 2.98s system 97% cpu 1:55.06 total
```
