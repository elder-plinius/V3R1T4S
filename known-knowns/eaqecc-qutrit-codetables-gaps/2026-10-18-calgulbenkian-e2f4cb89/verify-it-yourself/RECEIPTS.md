# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` (run from the claim folder).

```
sha256 matches INDEX.csv (e2f4cb89b2b3c23d00e39c2126d5a3e094a9613fece4ba104dac17084c0e88c7)
== calibration on hand-derived cases
EA n=2 {X1X2, Z1Z2} s,c,k,d = (2, 1, 1, 2) expected (2, 1, 1, 2) OK
EA n=2 {X1, Z1} s,c,k,d = (2, 1, 1, 1) expected (2, 1, 1, 1) OK
cyclic [[5,1,3]]_3 s,c,k,d = (4, 0, 1, 3) expected (4, 0, 1, 3) OK
CALIBRATION PASS
== check_eaqecc.py on object/eaqecc_16_4_8_4.json (table cell dlower-dupper = 7-9)
file eaqecc_16_4_8_4.json n 16 s 16 c 4 k 4 dual_dim 16 isotropic_dim 8
exact minimum distance d = 8 (2.7 s)
  c>=1 True
  d==d_claimed True
  d>table_d_lower(7) True
  d<=table_d_upper(9) True
[[16,4,8;4]]_3 PASS
== negative control: a copy with one matrix entry changed must FAIL
negative control rejected as expected: FAIL
ALL CHECKS PASS
```


## Run in this package folder, 2026-10-18 (packager)

Command: `PY=python-with-numpy-and-pulp sh verify-it-yourself/run_checks.sh` (exit 0)

```
sha256 matches INDEX.csv (e2f4cb89b2b3c23d00e39c2126d5a3e094a9613fece4ba104dac17084c0e88c7)
== calibration on hand-derived cases
EA n=2 {X1X2, Z1Z2} s,c,k,d = (2, 1, 1, 2) expected (2, 1, 1, 2) OK
EA n=2 {X1, Z1} s,c,k,d = (2, 1, 1, 1) expected (2, 1, 1, 1) OK
cyclic [[5,1,3]]_3 s,c,k,d = (4, 0, 1, 3) expected (4, 0, 1, 3) OK
CALIBRATION PASS
== check_eaqecc.py on object/eaqecc_16_4_8_4.json (table cell dlower-dupper = 7-9)
file eaqecc_16_4_8_4.json n 16 s 16 c 4 k 4 dual_dim 16 isotropic_dim 8
exact minimum distance d = 8 (2.5 s)
  c>=1 True
  d==d_claimed True
  d>table_d_lower(7) True
  d<=table_d_upper(9) True
[[16,4,8;4]]_3 PASS
== negative control: a copy with one matrix entry changed must FAIL
negative control rejected as expected: FAIL
ALL CHECKS PASS
```
