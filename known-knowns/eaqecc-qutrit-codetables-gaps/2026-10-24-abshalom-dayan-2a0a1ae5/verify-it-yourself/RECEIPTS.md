# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` from this package folder (with the date, platform, compiler and
Python version printed before it and the timing after it):

```
2026-10-24T17:52:50Z
Darwin arm64
Apple clang version 21.0.0 (clang-2100.1.1.101)
Python 3.14.7
n=28 s=26 c=7 k=9 dim_isotropic=12 dim_dual=30
{"n": 28, "s": 26, "c": 7, "k": 9, "dim_perp": 30, "dim_isotropic": 12, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
W=10 part=0/3 total_subsets=13123110 examined=4374370 with_vector_outside_isotropic=0
W=10 part=1/3 total_subsets=13123110 examined=4374370 with_vector_outside_isotropic=0
W=10 part=2/3 total_subsets=13123110 examined=4374370 with_vector_outside_isotropic=0
T=[0, 1, 2, 3, 4, 5, 6, 11, 18, 26, 27]
v_x=0 1 1 2 0 2 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2
v_z=1 0 2 1 2 0 2 0 0 0 0 2 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0
symplectic_weight=11 orthogonal_to_all_rows_of_S=True in_span_S=False support=[0, 1, 2, 3, 4, 5, 6, 11, 18, 26, 27]
ok:   parameters computed from S
ok:   computed n=28 s=26 c=7 k=9; claimed n=28 k=9 c=7
ok:   GF(9) description consistent with S
ok:   all parts of the W=10 subset test present
ok:   examined 13123110 of C(28,10) = 13123110 subsets
ok:   no vector of span(S)^perp outside the isotropic part on <= 10 positions (found 0)
ok:   witness of symplectic weight 11 outside span(S), claimed d=11
computed d=11; claimed d=11
PASS
real 4.04
user 9.48
sys 0.38
```
