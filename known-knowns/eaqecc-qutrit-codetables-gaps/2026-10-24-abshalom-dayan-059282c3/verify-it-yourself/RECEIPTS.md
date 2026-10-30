# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` from this package folder (with the date, platform, compiler and
Python version printed before it and the timing after it):

```
2026-10-24T22:42:28Z
Darwin arm64
Apple clang version 21.0.0 (clang-2100.1.1.101)
Python 3.14.7
n=33 s=36 c=12 k=9 dim_isotropic=12 dim_dual=30
{"n": 33, "s": 36, "c": 12, "k": 9, "dim_perp": 30, "dim_isotropic": 12, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
n=33 s=36 c=12 k=9 dim_N=30 dim_I=12 N_closed_under_w=True
kappa=15 (2*kappa == dim_N: True)
wrote verify-it-yourself/tmp_work/G9.txt
kappa=15 n=33 m=20 part=0/3 subsets=368070285 deficient=0 (expected subsets in all parts C(n,m)=573166440)
kappa=15 n=33 m=20 part=1/3 subsets=148206066 deficient=0 (expected subsets in all parts C(n,m)=573166440)
kappa=15 n=33 m=20 part=2/3 subsets=56890089 deficient=0 (expected subsets in all parts C(n,m)=573166440)
T=[0, 1, 3, 4, 5, 6, 9, 12, 13, 14, 16, 30, 31, 32]
v_x=0 2 0 0 1 1 1 0 0 0 0 0 2 0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2
v_z=1 1 0 2 1 0 1 0 0 2 0 0 0 1 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 1 2 1
symplectic_weight=14 orthogonal_to_all_rows_of_S=True in_span_S=False support=[0, 1, 3, 4, 5, 6, 9, 12, 13, 14, 16, 30, 31, 32]
GF(729) modulus u^3 + 2 u^2 + 0 u + 1 over GF(9); i = 4; 27 affine points; 288 degree-3 places
L1: rank S = 36, dim phi(C) = 30, 2n - rank S = 30, phi(C) orthogonal to S: True -> span(S)^perp = phi(C): True
L2: 5 columns unscaled by w^-1 (pattern ++++++++++++++++++++++++++++-----)
L3: K = 15, rank(head) = 15 (injective: True), dim zero-tail subcode = 12, rank(tail) = 3
L4: place #182 (point x0 = 69, y0 = 114 in this GF(729) coding): head code = C_L(D_28, 3Q + 8P_inf) (dim 15), zero-tail code = C_L(D_28, 2Q + 8P_inf) (dim 12): True
L4: 1 of 288 places identify both codes
L5: Goppa bounds d(head code) >= 28 - 17 = 11, d(zero-tail code) >= 28 - 14 = 14
L6: tail code dimension 3, all 10 maximal minors nonzero: True -> d(tail) = 3
L7: d(C) >= min(14, 11 + 3) = 14, so d_EA >= 14
L8: witness weight 14, in C: True, phi(witness) orthogonal to S: True, outside span(S): True
RESULT: d_EA = 14 exactly (theorem-based; no distance search): True
ok:   parameters computed from S
ok:   computed n=33 s=36 c=12 k=9; claimed n=33 k=9 c=12
ok:   GF(9) description consistent with S
ok:   span(S)^perp is closed under w (GF(9)-linear, dimension 2 kappa)
ok:   the two parameter computations agree
ok:   all parts of the m=20 information-set test present
ok:   test run on the code recovered from S (kappa=15)
ok:   examined 573166440 of C(33,20) = 573166440 coordinate subsets
ok:   every 20 coordinates hold an information set (deficient subsets: 0), so d >= 14
ok:   witness of symplectic weight 14 outside span(S), claimed d=14
computed d=14; claimed d=14
PASS
real 8.69
user 11.62
sys 0.38
```
