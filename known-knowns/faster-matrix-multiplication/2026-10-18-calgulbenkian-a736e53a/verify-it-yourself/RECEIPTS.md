# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 1 seconds on a laptop):

```text
sha256 matches INDEX.csv (a736e53a74f68425c0211816e0972faf8c027d4845885509b530644e9f64c52b)
== check_fmm_fast.py: exact Brent equations over Z, rank 569, coefficient class Z
coefficient class: Z (max |coefficient| = 2; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 10 bits, slot width 12 bits, 11760 blocks of 60 slots compared
PASS format=4x14x15 rank=569
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=4x14x15 rank=569: 4 of 11760 (a, b) blocks differ; first at A[0][2] x B[2][10]
negative control rejected as expected
ALL CHECKS PASS
```
