# Verification Receipts (`three-heap-wythoff-fraenkel-a1-11`)

Command executed from package root:

```sh
sh verify-it-yourself/run_checks.sh
```

Captured output:

```text
[1/4] Cross-checking literal 3D brute-force move rules on 0 <= p1 <= 11, p3 <= 55...
      Brute-force check OK (172 P-positions verified directly).
[2/4] Verifying base case m = 0 and inductive Sun-Zeilberger proofs for m = 1..11...
      m= 1 OK: alpha= -4, N1=  21, N2=  28, N3=  75 (B_N3=  77), n2=  48, n1= 130
      m= 2 OK: alpha=-10, N1=  28, N2=  58, N3= 157 (B_N3= 162), n2=  97, n1= 265
      m= 3 OK: alpha=-16, N1=  48, N2=  73, N3= 206 (B_N3= 216), n2= 127, n1= 350
      m= 4 OK: alpha=-20, N1= 126, N2= 208, N3= 561 (B_N3= 573), n2= 343, n1= 921
      m= 5 OK: alpha=-26, N1=  71, N2= 123, N3= 345 (B_N3= 361), n2= 209, n1= 577
      m= 6 OK: alpha=-32, N1= 113, N2= 232, N3= 637 (B_N3= 657), n2= 388, n1=1051
      m= 7 OK: alpha=-39, N1= 227, N2= 343, N3= 937 (B_N3= 962), n2= 572, n1=1539
      m= 8 OK: alpha=-46, N1= 388, N2= 648, N3=1739 (B_N3=1767), n2=1066, n1=2839
      m= 9 OK: alpha=-52, N1= 645, N2= 645, N3=1070 (B_N3=1102), n2= 651, n1=1760
      m=10 OK: alpha=-56, N1= 656, N2= 656, N3=1766 (B_N3=1801), n2=1080, n1=2887
      m=11 OK: alpha=-61, N1=1214, N2=1214, N3=1381 (B_N3=1420), n2=1216, n1=3249
[3/4] Auditing Sun & Zeilberger Table 1 (m = 0..10)...
      All 11 rows (m = 0..10) of Sun & Zeilberger Table 1 match identically (partial win p1 confirmed).
[4/4] Final summary for open case A_1 = 11:
      T^11 = [1, 7, 11, 13, 17, 21, 23]
      |S^11| = 40, max(S^11) = 1252
      alpha^11 = -61, N1^11 = 1214, N2^11 = 1214, N3^11 = 1381, B^11_{N3^11} = 1420
      Claim 3.4/3.5 witnesses: N = 15, n2 = 1216, n1 = 3249
PASS
```
