# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 1 seconds on a laptop):

```text
sha256 matches INDEX.csv (e25137a39f9a642d3a93ae58337d80703f5e45c2efc48e96207d7e61aeb101e5)
== check_fmm_fast.py: exact Brent equations over Z, rank 889, coefficient class Z
coefficient class: Z (max |coefficient| = 2; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 10 bits, slot width 12 bits, 15246 blocks of 126 slots compared
PASS format=9x11x14 rank=889
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=9x11x14 rank=889: 25 of 15246 (a, b) blocks differ; first at A[3][6] x B[0][0]
negative control rejected as expected
ALL CHECKS PASS
```
