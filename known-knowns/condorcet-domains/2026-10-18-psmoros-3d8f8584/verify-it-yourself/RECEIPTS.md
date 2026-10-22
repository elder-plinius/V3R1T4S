# RECEIPTS: real output of `sh verify-it-yourself/run_checks.sh` (main session, 2026-10-18T07:31:58Z)

```
joined xz sha256 3d8f8584cae56439f03859f9a9b22f63f9d7dc8963220769a9c089a0381eab54
n 20 lines 3336208 malformed 0 distinct 3336208 duplicates 0 triples 1140 violations 0
assignment lines 1140 bad_or_missing 0 orders_disobeying 0
size 3336208, required more than 3336207
PASS
assignment: 1140 lines, 1140 distinct triples (C(20,3) = 1140), 0 malformed or repeated
n 20 |D(A)| 3336208 (memoised prefix sets: 1754)
expected 3336208: yes; at least 3155367: yes
PASS
the list has 3336208 distinct orders, all obeying the assignment, and |D(A)| = 3336208: the list is exactly D(A)
3336208 > 3155366 (Table 4 of arXiv:2601.07336v1, n = 20)
PASS
```
