== running check_a089980_ad79.py on object/ files ==
[OK] b089980.txt parsed: n=0..3159 (3160 entries), complete antidiagonals d=0..78
[OK] (A) Brute-force independent-set definition verified on 25/25 small grids (0 <= w,m <= 4)
[OK] Claimed files a089980_antidiag79.txt and .tsv have 80 entries (n=3160..3239), exact symmetry, T(0,79)=1, T(1,78)=F(80)
[OK] (B) Pure-Python exact big-int column transfer reproduced 814 published cells (w=0..10) and confirmed T(w,79-w) for w=0..10
[OK] Exact big-int table antidiag79_indep_bigint.tsv matches claimed T(w,79-w) on all 17 widths w=0..16
[OK] (C) Independent CRT + held-out check prime verified on all 40/40 widths (w=0..39) in both decompositions!
     - hs_mod primes: 37 distinct primes in [2147482819, 2147483647] subset (2^30, 2^31)
     - far primes:    38 distinct primes in [1073740933, 1073741789] subset (0, 2^30)
     - intersection:  0 (disjoint), 80/80 symmetric antidiagonal entries verified
[OK] (D) Live fresh-prime DP sweep (w=16, m=63, p=1000000007) matches claimed T(16,63) mod p = 309266150
PASS
== negative control: a corrupted copy must FAIL ==
negative control rejected as expected (AssertionError)
ALL CHECKS PASS
