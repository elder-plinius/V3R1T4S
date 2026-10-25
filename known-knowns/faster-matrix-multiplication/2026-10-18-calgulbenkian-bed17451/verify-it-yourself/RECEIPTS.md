# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 1 seconds on a laptop):

```text
sha256 matches INDEX.csv (bed17451925a1e9a484a2848faae3aca36011203fbd9e3277c73d673a8a57daa)
== check_fmm_fast.py: exact Brent equations over Z, rank 1039, coefficient class Z
coefficient class: Z (max |coefficient| = 2; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 21294 blocks of 126 slots compared
PASS format=9x13x14 rank=1039
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=9x13x14 rank=1039: 44 of 21294 (a, b) blocks differ; first at A[0][1] x B[7][0]
negative control rejected as expected
ALL CHECKS PASS
```
