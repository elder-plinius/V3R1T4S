# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` from this package folder (with the date, platform, compiler and
Python version printed before it and the timing after it):

```
2026-10-25T14:07:47Z
Darwin arm64
Apple clang version 21.0.0 (clang-2100.1.1.101)
Python 3.14.7
n=23 s=28 c=9 k=4 dim_isotropic=10 dim_dual=18
{"n": 23, "s": 28, "c": 9, "k": 4, "dim_perp": 18, "dim_isotropic": 10, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
W=11 part=0/3 total_subsets=1352078 examined=450693 with_vector_outside_isotropic=0
W=11 part=1/3 total_subsets=1352078 examined=450693 with_vector_outside_isotropic=0
W=11 part=2/3 total_subsets=1352078 examined=450692 with_vector_outside_isotropic=0
T=[9, 10, 11, 12, 13, 14, 15, 17, 19, 20, 21, 22]
v_x=0 0 0 0 0 0 0 0 0 0 0 2 1 0 0 1 0 2 0 1 2 1 0
v_z=0 0 0 0 0 0 0 0 0 1 1 2 1 2 2 0 0 0 0 0 2 1 2
symplectic_weight=12 orthogonal_to_all_rows_of_S=True in_span_S=False support=[9, 10, 11, 12, 13, 14, 15, 17, 19, 20, 21, 22]
1. n=23 rank S=28 rank(S J S^T)=18 c=9 k=4
2. E_11: 9 monomials (pole orders [0, 3, 4, 6, 7, 8, 9, 10, 11]), top monomial (1, 2); deleted coordinates [0, 3, 11, 12, 16] (affine points [(0, 0), (1, 2), (3, 6), (4, 2), (5, 5)]); columns [1, 3, 6, 8, 10, 11, 14, 15, 16, 17, 19, 21] of the result times w
3. phi(E') orthogonal to every row of S: True; dim_GF(3) phi(E') = 18; 2n - rank S = 18; span(S)^perp = phi(E'): True
   GF(9) dimension of E' = 9 (E_11 has 9 monomials)
4. bound (proved in the docstring): d(E') >= 28 - 11 - 5 = 12, so d_EA >= 12
5. witness weight 12, in E': True, phi(witness) in span(S): False -> d_EA <= 12
RESULT: d_EA = 12 exactly (no distance search): True
ok:   parameters computed from S
ok:   computed n=23 s=28 c=9 k=4; claimed n=23 k=4 c=9
ok:   GF(9) description consistent with S
ok:   all parts of the W=11 subset test present
ok:   examined 1352078 of C(23,11) = 1352078 subsets
ok:   no vector of span(S)^perp outside the isotropic part on <= 11 positions (found 0)
ok:   witness of symplectic weight 12 outside span(S), claimed d=12
computed d=12; claimed d=12
PASS
sh verify-it-yourself/run_checks.sh 1.54 total (0.92 user, 0.29 sys)
```
