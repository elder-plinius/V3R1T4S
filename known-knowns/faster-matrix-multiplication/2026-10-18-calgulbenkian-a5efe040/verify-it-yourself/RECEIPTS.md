# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 1 seconds on a laptop):

```text
sha256 matches INDEX.csv (a5efe04017632a0da87598ba3b2509ca66bb6fea965bb71a2faebb2aef582ab1)
== check_fmm_fast.py: exact Brent equations over Z, rank 816, coefficient class ZT
coefficient class: ZT (max |coefficient| = 1; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 10 bits, slot width 12 bits, 12600 blocks of 126 slots compared
PASS format=9x10x14 rank=816
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=9x10x14 rank=816: 12 of 12600 (a, b) blocks differ; first at A[8][4] x B[1][1]
negative control rejected as expected
ALL CHECKS PASS
```
