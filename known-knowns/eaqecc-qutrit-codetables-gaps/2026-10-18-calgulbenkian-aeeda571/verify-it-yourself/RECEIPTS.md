# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` (run from the claim folder).

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


## Run in this package folder, 2026-10-18 (packager)

Command: `PY=python-with-numpy-and-pulp sh verify-it-yourself/run_checks.sh` (exit 0)

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
