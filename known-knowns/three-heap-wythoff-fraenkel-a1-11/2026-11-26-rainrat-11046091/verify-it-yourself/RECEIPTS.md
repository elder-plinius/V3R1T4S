# Verification receipts

Command run from the package root (`UTC 2026-11-25T07:27:27Z`):

```sh
sh verify-it-yourself/run_checks.sh
```

Output:

```text
[1/5] Cross-checking literal 3D brute-force (0 <= p1 <= 12, p3 <= 55) and recomputing through Y <= 5500...
      Brute-force match OK (178 P-positions checked).
[2/5] Verifying m = 0..12 constants, Table 1 (m = 0..10), Claims 3.3-3.5, and Lemma 2.6 direct induction...
      m= 0 OK: alpha=  0, N1=   1, N2=   1, N3=   1 (B_N3=   0), n2=   6, n1=  10
      m= 1 OK: alpha= -4, N1=  21, N2=  28, N3=  75 (B_N3=  77), n2=  52, n1=  91
      m= 2 OK: alpha=-10, N1=  28, N2=  58, N3= 157 (B_N3= 162), n2= 101, n1= 182
      m= 3 OK: alpha=-16, N1=  48, N2=  73, N3= 206 (B_N3= 216), n2= 131, n1= 223
      m= 4 OK: alpha=-20, N1= 126, N2= 208, N3= 561 (B_N3= 573), n2= 347, n1= 575
      m= 5 OK: alpha=-26, N1=  71, N2= 123, N3= 345 (B_N3= 361), n2= 213, n1= 559
      m= 6 OK: alpha=-32, N1= 113, N2= 232, N3= 637 (B_N3= 657), n2= 392, n1= 652
      m= 7 OK: alpha=-39, N1= 227, N2= 343, N3= 937 (B_N3= 962), n2= 576, n1= 953
      m= 8 OK: alpha=-46, N1= 388, N2= 648, N3=1739 (B_N3=1767), n2=1070, n1=1754
      m= 9 OK: alpha=-52, N1= 645, N2= 645, N3=1070 (B_N3=1102), n2=1065, n1=1748
      m=10 OK: alpha=-56, N1= 656, N2= 656, N3=1766 (B_N3=1801), n2=1084, n1=1781
      m=11 OK: alpha=-61, N1=1214, N2=1214, N3=1381 (B_N3=1420), n2=1990, n1=3249
      m=12 OK: alpha=-67, N1=  64, N2= 352, N3= 988 (B_N3=1030), n2= 601, n1=1762
[3/5] Auditing Sun & Zeilberger Table 1 (m = 0..10)...
      All 11 rows of Sun & Zeilberger Table 1 match identically (partial win p1 confirmed).
[4/5] Verifying m = 11 prerequisite and m = 12 target constants...
      m=11: T=[1, 7, 11, 13, 17, 21, 23], |S|=40, alpha=-61, N1=1214, N2=1214, N3=1381, B_N3=1420, n2=1990, n1=3249, B_n1=3288, min_slack=1
      m=12: T=[0, 8, 9, 18, 22, 24], |S|=43, alpha=-67, N1=64, N2=352, N3=988, B_N3=1030, n2=601, n1=1762, B_n1=1804, min_slack=2
[5/5] All certificate integrity, rule-recomputation, Table 1, Claim 3.3-3.5, and Lemma 2.6 checks complete.
PASS
```
