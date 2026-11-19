# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` from this package folder (with the date, platform, compiler and
Python version printed before it and the timing after it):

```
2026-10-24T23:43:46Z
Darwin arm64
Apple clang version 21.0.0 (clang-2100.1.1.101)
Python 3.14.7
n=28 s=30 c=9 k=7 dim_isotropic=12 dim_dual=26
{"n": 28, "s": 30, "c": 9, "k": 7, "dim_perp": 26, "dim_isotropic": 12, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
W=12 part=0/3 total_subsets=30421755 examined=10140585 with_vector_outside_isotropic=0
W=12 part=1/3 total_subsets=30421755 examined=10140585 with_vector_outside_isotropic=0
W=12 part=2/3 total_subsets=30421755 examined=10140585 with_vector_outside_isotropic=0
T=[12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
v_x=0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 2 2 2 2 2 2 1
v_z=0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 1 1 1 1 1 1 2 2 2 0
symplectic_weight=13 orthogonal_to_all_rows_of_S=True in_span_S=False support=[12, 13, 14, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27]
1. n=28 rank S=30 rank(S J S^T)=18 c=9 k=7
2. E: 13 monomials (pole orders [0, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]), 27 affine points, top monomial (5, 0)
3. phi(E) orthogonal to every row of S: True; dim_GF(3) phi(E) = 26; 2n - rank S = 26; span(S)^perp = phi(E): True
   GF(9) dimension of E = 13
4. Goppa-type bound (proved in the docstring): d(E) >= 28 - 15 = 13, so d_EA >= 13
5. witness weight 13, in E: True, phi(witness) in span(S): False -> d_EA <= 13
RESULT: d_EA = 13 exactly (no distance search): True
ok:   parameters computed from S
ok:   computed n=28 s=30 c=9 k=7; claimed n=28 k=7 c=9
ok:   GF(9) description consistent with S
ok:   all parts of the W=12 subset test present
ok:   examined 30421755 of C(28,12) = 30421755 subsets
ok:   no vector of span(S)^perp outside the isotropic part on <= 12 positions (found 0)
ok:   witness of symplectic weight 13 outside span(S), claimed d=13
computed d=13; claimed d=13
PASS
real 8.77
user 21.18
sys 0.47
```
