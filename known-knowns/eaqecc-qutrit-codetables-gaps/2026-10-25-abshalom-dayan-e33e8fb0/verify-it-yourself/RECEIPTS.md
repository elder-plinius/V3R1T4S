# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` from this package folder (with the date, platform, compiler and
Python version printed before it and the timing after it):

```
2026-10-25T10:29:59Z
Darwin arm64
Apple clang version 21.0.0 (clang-2100.1.1.101)
Python 3.14.7
n=25 s=28 c=8 k=5 dim_isotropic=12 dim_dual=22
{"n": 25, "s": 28, "c": 8, "k": 5, "dim_perp": 22, "dim_isotropic": 12, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
W=11 part=0/3 total_subsets=4457400 examined=1485800 with_vector_outside_isotropic=0
W=11 part=1/3 total_subsets=4457400 examined=1485800 with_vector_outside_isotropic=0
W=11 part=2/3 total_subsets=4457400 examined=1485800 with_vector_outside_isotropic=0
T=[1, 8, 11, 14, 15, 16, 17, 18, 19, 21, 23, 24]
v_x=0 2 0 0 0 0 0 0 2 0 0 1 0 0 0 2 0 0 2 2 0 2 0 2 1
v_z=0 1 0 0 0 0 0 0 2 0 0 1 0 0 2 1 1 2 0 1 0 2 0 1 0
symplectic_weight=12 orthogonal_to_all_rows_of_S=True in_span_S=False support=[1, 8, 11, 14, 15, 16, 17, 18, 19, 21, 23, 24]
1. n=25 rank S=28 rank(S J S^T)=16 c=8 k=5
2. E_13: 11 monomials (pole orders [0, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13]), top monomial (3, 1); deleted coordinates [0, 1, 2] (affine points [(0, 0), (0, 4), (0, 8)]); columns [6, 7, 8, 12, 13, 14, 15, 16, 17, 18, 19, 20, 24] of the result times w
3. phi(E') orthogonal to every row of S: True; dim_GF(3) phi(E') = 22; 2n - rank S = 22; span(S)^perp = phi(E'): True
   GF(9) dimension of E' = 11 (E_13 has 11 monomials)
4. bound (proved in the docstring): d(E') >= 28 - 13 - 3 = 12, so d_EA >= 12
5. witness weight 12, in E': True, phi(witness) in span(S): False -> d_EA <= 12
RESULT: d_EA = 12 exactly (no distance search): True
ok:   parameters computed from S
ok:   computed n=25 s=28 c=8 k=5; claimed n=25 k=5 c=8
ok:   GF(9) description consistent with S
ok:   all parts of the W=11 subset test present
ok:   examined 4457400 of C(25,11) = 4457400 subsets
ok:   no vector of span(S)^perp outside the isotropic part on <= 11 positions (found 0)
ok:   witness of symplectic weight 12 outside span(S), claimed d=12
computed d=12; claimed d=12
PASS
real 6.30
user 3.66
sys 0.46
```
