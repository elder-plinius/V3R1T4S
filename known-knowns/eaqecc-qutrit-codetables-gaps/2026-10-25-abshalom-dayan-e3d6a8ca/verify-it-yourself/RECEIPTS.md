# Receipts: real output of `sh verify-it-yourself/run_checks.sh`

Run from the package folder on 2026-10-25, start 04:30:48Z, end 04:31:09Z (UTC, `date -u`), Apple M4 Pro (arm64),
one core, on a shared machine with two other CPU-heavy processes running. `/usr/bin/time -p`: real 21.40 s, user
20.90 s, sys 0.12 s. Exit status 0.

```
n=35 s=42 c=14 k=7 dim_isotropic=14 dim_dual=28
{"n": 35, "s": 42, "c": 14, "k": 7, "dim_perp": 28, "dim_isotropic": 14, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
n=35 s=42 c=14 k=7 dim_N=28 dim_I=14 N_closed_under_w=True
kappa=14 (2*kappa == dim_N: True)
wrote verify-it-yourself/tmp_work/G9.txt
kappa=14 n=35 m=20 part=0/3 subsets=2004173586 deficient=0 (expected subsets in all parts C(n,m)=3247943160)
kappa=14 n=35 m=20 part=1/3 subsets=875699289 deficient=0 (expected subsets in all parts C(n,m)=3247943160)
kappa=14 n=35 m=20 part=2/3 subsets=368070285 deficient=0 (expected subsets in all parts C(n,m)=3247943160)
T=[1, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26]
v_x=0 2 0 0 0 0 0 0 0 0 2 2 0 1 0 1 0 2 2 1 0 1 0 2 2 0 2 0 0 0 0 0 0 0 0
v_z=0 1 0 0 0 0 0 0 0 0 0 2 0 2 2 0 2 1 0 0 1 0 0 2 2 1 1 0 0 0 0 0 0 0 0
symplectic_weight=16 orthogonal_to_all_rows_of_S=True in_span_S=False support=[1, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26]
GF(6561) modulus u^4 + 3 u^3 + 0 u^2 + 0 u + 3 over GF(9); i = 4; 27 affine points; 6076 points over GF(6561); 1512 degree-4 places
L1: rank S = 42, dim phi(C) = 28, 2n - rank S = 28, phi(C) orthogonal to S: True -> span(S)^perp = phi(C): True
L2: 20 columns unscaled by w^-1 (pattern +---++---+--+++-+----++-+--+-+--++-)
L3: K = 14, rank(head) = 14 (injective: True), dim zero-tail subcode = 10, rank(tail) = 4, K - dim zero-tail = 4
L4: place #1319 (point x0 = 2329, y0 = 2788 in this GF(6561) coding): head code = C_L(D_28, 2Q + 8P_inf) (dim 14), zero-tail code = C_L(D_28, 1Q + 8P_inf) (dim 10): True
L4: 1 of 1512 places identify both codes
L5: Goppa bounds d(head code) >= 28 - 16 = 12, d(zero-tail code) >= 28 - 12 = 16
L6: tail code dimension 4 (= K - dim zero-tail: True), all 35 maximal minors nonzero: True -> d(tail) = 4
L7: d(C) >= min(16, 12 + 4) = 16, so d_EA >= 16
L8: witness weight 16, in C: True, phi(witness) orthogonal to S: True, outside span(S): True
RESULT: d_EA = 16 exactly (theorem-based; no distance search): True
ok:   parameters computed from S
ok:   computed n=35 s=42 c=14 k=7; claimed n=35 k=7 c=14
ok:   GF(9) description consistent with S
ok:   span(S)^perp is closed under w (GF(9)-linear, dimension 2 kappa)
ok:   the two parameter computations agree
ok:   all parts of the m=20 information-set test present
ok:   test run on the code recovered from S (kappa=14)
ok:   examined 3247943160 of C(35,20) = 3247943160 coordinate subsets
ok:   every 20 coordinates hold an information set (deficient subsets: 0), so d >= 16
ok:   witness of symplectic weight 16 outside span(S), claimed d=16
computed d=16; claimed d=16
PASS
```
