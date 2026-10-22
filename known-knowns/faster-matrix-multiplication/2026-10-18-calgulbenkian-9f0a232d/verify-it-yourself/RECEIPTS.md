# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 1 seconds on a laptop):

```text
sha256 matches INDEX.csv (9f0a232de00ce5220d75097b9af6986f97d81932fa3e3718e1291d426f4caede)
== check_fmm_fast.py: exact Brent equations over Z, rank 570, coefficient class Z
coefficient class: Z (max |coefficient| = 2; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 10 bits, slot width 12 bits, 6720 blocks of 105 slots compared
PASS format=7x8x15 rank=570
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=7x8x15 rank=570: 16 of 6720 (a, b) blocks differ; first at A[2][0] x B[0][0]
negative control rejected as expected
ALL CHECKS PASS
```
