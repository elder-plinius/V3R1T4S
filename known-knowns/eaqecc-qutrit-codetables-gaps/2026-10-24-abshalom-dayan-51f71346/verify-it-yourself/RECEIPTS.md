# Receipts

Real output of `sh verify-it-yourself/run_checks.sh` from this package folder (with the date, platform, compiler and
Python version printed before it and the timing after it):

```
2026-10-24T15:50:51Z
Darwin arm64
Apple clang version 21.0.0 (clang-2100.1.1.101)
Python 3.14.7
n=28 s=28 c=6 k=6 dim_isotropic=16 dim_dual=28
{"n": 28, "s": 28, "c": 6, "k": 6, "dim_perp": 28, "dim_isotropic": 16, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
W=11 part=0/4 total_subsets=21474180 examined=5368545 with_vector_outside_isotropic=0
W=11 part=1/4 total_subsets=21474180 examined=5368545 with_vector_outside_isotropic=0
W=11 part=2/4 total_subsets=21474180 examined=5368545 with_vector_outside_isotropic=0
W=11 part=3/4 total_subsets=21474180 examined=5368545 with_vector_outside_isotropic=0
T=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
v_x=0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 2 2 2 2 2 2 0
v_z=0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 0 0 0 0
symplectic_weight=12 orthogonal_to_all_rows_of_S=True in_span_S=False support=[15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
ok:   parameters computed from S
ok:   computed n=28 s=28 c=6 k=6; claimed n=28 k=6 c=6
ok:   GF(9) description consistent with S
ok:   all parts of the W=11 subset test present
ok:   examined 21474180 of C(28,11) = 21474180 subsets
ok:   no vector of span(S)^perp outside the isotropic part on <= 11 positions (found 0)
ok:   witness of symplectic weight 12 outside span(S), claimed d=12
computed d=12; claimed d=12
PASS
real 4.24
user 11.16
sys 0.62
exit=0
2026-10-24T15:50:56Z
```
