# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 1 seconds on a laptop):

```text
sha256 matches INDEX.csv (910a044b4fccb5ea250be0894c8e4a40947f31989b04c39e1cb34d31bbbc9e6a)
== check_fmm_fast.py: exact Brent equations over Z, rank 1065, coefficient class Z
coefficient class: Z (max |coefficient| = 3; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 20736 blocks of 144 slots compared
PASS format=9x12x16 rank=1065
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=9x12x16 rank=1065: 5 of 20736 (a, b) blocks differ; first at A[1][3] x B[0][6]
negative control rejected as expected
ALL CHECKS PASS
```
