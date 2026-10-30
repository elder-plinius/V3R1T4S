# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` from this package folder (with the date, platform, compiler and
Python version printed before it and the timing after it):

```
2026-10-24T19:27:13Z
Darwin arm64
Apple clang version 21.0.0 (clang-2100.1.1.101)
Python 3.14.7
n=33 s=40 c=15 k=8 dim_isotropic=10 dim_dual=26
{"n": 33, "s": 40, "c": 15, "k": 8, "dim_perp": 26, "dim_isotropic": 10, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
n=33 s=40 c=15 k=8 dim_N=26 dim_I=10 N_closed_under_w=True
kappa=13 (2*kappa == dim_N: True)
wrote verify-it-yourself/tmp_work/G9.txt
kappa=13 n=33 m=18 part=0/3 subsets=620845293 deficient=0 (expected subsets in all parts C(n,m)=1037158320)
kappa=13 n=33 m=18 part=1/3 subsets=287764785 deficient=0 (expected subsets in all parts C(n,m)=1037158320)
kappa=13 n=33 m=18 part=2/3 subsets=128548242 deficient=0 (expected subsets in all parts C(n,m)=1037158320)
T=[9, 10, 11, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31]
v_x=0 0 0 0 0 0 0 0 0 2 1 2 0 0 0 1 0 0 0 0 0 1 1 2 1 0 0 2 0 1 0 0 0
v_z=0 0 0 0 0 0 0 0 0 2 1 2 0 0 0 2 1 2 0 0 0 1 1 0 2 2 2 0 0 1 1 1 0
symplectic_weight=16 orthogonal_to_all_rows_of_S=True in_span_S=False support=[9, 10, 11, 15, 16, 17, 21, 22, 23, 24, 25, 26, 27, 29, 30, 31]
ok:   parameters computed from S
ok:   computed n=33 s=40 c=15 k=8; claimed n=33 k=8 c=15
ok:   GF(9) description consistent with S
ok:   span(S)^perp is closed under w (GF(9)-linear, dimension 2 kappa)
ok:   the two parameter computations agree
ok:   all parts of the m=18 information-set test present
ok:   test run on the code recovered from S (kappa=13)
ok:   examined 1037158320 of C(33,18) = 1037158320 coordinate subsets
ok:   every 18 coordinates hold an information set (deficient subsets: 0), so d >= 16
ok:   witness of symplectic weight 16 outside span(S), claimed d=16
computed d=16; claimed d=16
PASS
real 4.58
user 7.64
sys 0.11
```
