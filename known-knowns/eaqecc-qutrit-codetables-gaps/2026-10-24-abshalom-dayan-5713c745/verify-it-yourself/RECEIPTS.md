# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` from this package folder (with the date, platform, compiler and
Python version printed before it and the timing after it):

```
2026-10-24T22:07:20Z
Darwin arm64
Apple clang version 21.0.0 (clang-2100.1.1.101)
Python 3.14.7
n=33 s=38 c=12 k=7 dim_isotropic=14 dim_dual=28
{"n": 33, "s": 38, "c": 12, "k": 7, "dim_perp": 28, "dim_isotropic": 14, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
n=33 s=38 c=12 k=7 dim_N=28 dim_I=14 N_closed_under_w=True
kappa=14 (2*kappa == dim_N: True)
wrote verify-it-yourself/tmp_work/G9.txt
kappa=14 n=33 m=19 part=0/3 subsets=507629004 deficient=0 (expected subsets in all parts C(n,m)=818809200)
kappa=14 n=33 m=19 part=1/3 subsets=219864219 deficient=0 (expected subsets in all parts C(n,m)=818809200)
kappa=14 n=33 m=19 part=2/3 subsets=91315977 deficient=0 (expected subsets in all parts C(n,m)=818809200)
T=[0, 11, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
v_x=2 0 0 0 0 0 0 0 0 0 0 1 0 0 1 0 0 0 1 2 0 0 2 2 1 2 1 0 0 0 0 0 0
v_z=1 0 0 0 0 0 0 0 0 0 0 1 0 0 2 2 0 1 0 0 2 1 0 1 1 2 2 2 0 0 0 0 0
symplectic_weight=15 orthogonal_to_all_rows_of_S=True in_span_S=False support=[0, 11, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
GF(729) modulus u^3 + 2 u^2 + 0 u + 1 over GF(9); i = 4; 27 affine points; 288 degree-3 places
L1: rank S = 38, dim phi(C) = 28, 2n - rank S = 28, phi(C) orthogonal to S: True -> span(S)^perp = phi(C): True
L2: 16 columns unscaled by w^-1 (pattern +-+---+-+-++---+-+++----+-+-+++++)
L3: K = 14, rank(head) = 14 (injective: True), dim zero-tail subcode = 11, rank(tail) = 3
L4: place #182 (point x0 = 69, y0 = 114 in this GF(729) coding): head code = C_L(D_28, 4Q + 4P_inf) (dim 14), zero-tail code = C_L(D_28, 3Q + 4P_inf) (dim 11): True
L4: 1 of 288 places identify both codes
L5: Goppa bounds d(head code) >= 28 - 16 = 12, d(zero-tail code) >= 28 - 13 = 15
L6: tail code dimension 3, all 10 maximal minors nonzero: True -> d(tail) = 3
L7: d(C) >= min(15, 12 + 3) = 15, so d_EA >= 15
L8: witness weight 15, in C: True, phi(witness) orthogonal to S: True, outside span(S): True
RESULT: d_EA = 15 exactly (theorem-based; no distance search): True
ok:   parameters computed from S
ok:   computed n=33 s=38 c=12 k=7; claimed n=33 k=7 c=12
ok:   GF(9) description consistent with S
ok:   span(S)^perp is closed under w (GF(9)-linear, dimension 2 kappa)
ok:   the two parameter computations agree
ok:   all parts of the m=19 information-set test present
ok:   test run on the code recovered from S (kappa=14)
ok:   examined 818809200 of C(33,19) = 818809200 coordinate subsets
ok:   every 19 coordinates hold an information set (deficient subsets: 0), so d >= 15
ok:   witness of symplectic weight 15 outside span(S), claimed d=15
computed d=15; claimed d=15
PASS
real 6.89
user 9.84
sys 0.34
```
