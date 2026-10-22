# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 1 seconds on a laptop):

```text
sha256 matches INDEX.csv (6083d9f3d15c408b83094f0d8d2f48ce60ecb549856051182174e92f00aa5596)
== check_fmm_fast.py: exact Brent equations over Z, rank 533, coefficient class Z
coefficient class: Z (max |coefficient| = 2; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 10 bits, slot width 12 bits, 10140 blocks of 60 slots compared
PASS format=4x13x15 rank=533
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=4x13x15 rank=533: 17 of 10140 (a, b) blocks differ; first at A[3][3] x B[1][8]
negative control rejected as expected
ALL CHECKS PASS
```
