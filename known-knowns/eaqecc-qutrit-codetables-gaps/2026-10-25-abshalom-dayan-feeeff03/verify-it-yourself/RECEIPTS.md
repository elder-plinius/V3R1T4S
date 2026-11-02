# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` from this package folder (with the date, platform, compiler and
Python version printed before it and the timing after it):

```
2026-10-25T11:34:52Z
Darwin arm64
Apple clang version 21.0.0 (clang-2100.1.1.101)
Python 3.14.7
n=24 s=30 c=10 k=4 dim_isotropic=10 dim_dual=18
{"n": 24, "s": 30, "c": 10, "k": 4, "dim_perp": 18, "dim_isotropic": 10, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
W=12 part=0/3 total_subsets=2704156 examined=901386 with_vector_outside_isotropic=0
W=12 part=1/3 total_subsets=2704156 examined=901385 with_vector_outside_isotropic=0
W=12 part=2/3 total_subsets=2704156 examined=901385 with_vector_outside_isotropic=0
T=[0, 10, 11, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23]
v_x=0 0 0 0 0 0 0 0 0 0 2 1 0 2 0 0 0 1 1 1 0 1 1 2
v_z=2 0 0 0 0 0 0 0 0 0 0 2 0 2 2 0 2 1 2 0 1 2 0 1
symplectic_weight=13 orthogonal_to_all_rows_of_S=True in_span_S=False support=[0, 10, 11, 13, 14, 16, 17, 18, 19, 20, 21, 22, 23]
1. n=24 rank S=30 rank(S J S^T)=20 c=10 k=4
2. E_11: 9 monomials (pole orders [0, 3, 4, 6, 7, 8, 9, 10, 11]), top monomial (1, 2); deleted coordinates [0, 3, 6, 11] (affine points [(0, 0), (1, 2), (2, 2), (3, 6)]); columns [1, 3, 5, 7, 10, 11, 12, 15, 17, 18, 20, 22] of the result times w
3. phi(E') orthogonal to every row of S: True; dim_GF(3) phi(E') = 18; 2n - rank S = 18; span(S)^perp = phi(E'): True
   GF(9) dimension of E' = 9 (E_11 has 9 monomials)
4. bound (proved in the docstring): d(E') >= 28 - 11 - 4 = 13, so d_EA >= 13
5. witness weight 13, in E': True, phi(witness) in span(S): False -> d_EA <= 13
RESULT: d_EA = 13 exactly (no distance search): True
ok:   parameters computed from S
ok:   computed n=24 s=30 c=10 k=4; claimed n=24 k=4 c=10
ok:   GF(9) description consistent with S
ok:   all parts of the W=12 subset test present
ok:   examined 2704156 of C(24,12) = 2704156 subsets
ok:   no vector of span(S)^perp outside the isotropic part on <= 12 positions (found 0)
ok:   witness of symplectic weight 13 outside span(S), claimed d=13
computed d=13; claimed d=13
PASS
real 2.23
user 1.61
sys 0.38
```
