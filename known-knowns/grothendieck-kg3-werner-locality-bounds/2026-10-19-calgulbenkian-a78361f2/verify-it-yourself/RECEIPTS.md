# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from the package folder by the packager on 2026-10-19 (python3 3.9.6, Darwin). Wall time about 7 seconds. Exit status 0.

```
sha256 of object/d8_n1_120x120.mat matches INDEX.csv (a78361f200b669741a4a0636bb4e1027a1e6cdfeca174c84ef67269a17bbeaac)
== e8_check.py: identification with the E8 roots, Q, lower bound, 18454 dual certificates (about 5 s)
== Phase A: matrix from the MATLAB file
matrix found (byte offset 0, element 322): 120 x 120, symmetric, diagonal all -7, entries [-7, -3, 0, 3]
per row: number of entries +-3 = [56], number of zeros = [63]
== Phase B: identification with the positive roots of E8
base of simple roots found among the lines (Bourbaki labelling), lines [0, 9, 1, 5, 37, 56, 20, 27]
Gram entries not reproduced by root coordinates: 0 of 14400
120 distinct positive roots with all coordinates >= 0 and norm 2; |2 rho|^2 = 2480 (so |rho|^2 = 620)
A = D (3 G' - 13 I) D with D = diag(signs) and G' the Gram matrix of the 120 positive roots; L and Q are unchanged by D.
identity (A b)_i = 3 ip(r_i, w) - 13 b_i on 40 pseudo-random sign vectors: 0 violations
== Phase C: Q
A.A = 66360, trace A = -840, Q = (A.A + 13 trace A)/6 = 9240
== Phase D: lower bound L >= 6104
witness b has 96 entries +1 and 24 entries -1; a = sign(A b); a^T A b = 6104 ; ||A b||_1 = 6104
== Phase E: upper bound L <= 6104
dominant w = 2v with v = sum c_k omega_k, |v|^2 <= 620: 18454 vectors
certificate lines read: 18454
dominant vectors without a certificate: 0; certificates with dual value above 6104: 0; with dual value exactly 6104: 2
largest certified dual value: 6104 at c = (0, 0, 0, 0, 5, 0, 1, 0)
elapsed 3.2 s
RESULT PASS: L = 6104, Q = 9240, Q/L = 165/109 = 1.5137614678899083
== negative control 1: one symmetric pair of matrix entries changed; the check must FAIL
negative control 1 rejected as expected: RESULT FAIL
== negative control 2: the certificate of the first tight vector is replaced by zeros; the check must FAIL
negative control 2 rejected as expected: dominant vectors without a certificate: 0; certificates with dual value above 6104: 1; with dual value exactly 6104: 1
ALL CHECKS PASS
```
