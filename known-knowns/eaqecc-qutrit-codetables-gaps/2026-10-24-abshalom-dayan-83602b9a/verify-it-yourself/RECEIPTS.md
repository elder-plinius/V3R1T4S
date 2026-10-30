# Receipts: real output of `sh verify-it-yourself/run_checks.sh`

Run from this package folder on 2026-10-24 (UTC start and end times below), on an Apple-silicon laptop
(Darwin arm64, Apple clang 21.0.0, Python 3.14.7) that was busy with other jobs. `real`, `user` and `sys` are from
`/usr/bin/time -p`.

```
2026-10-24T11:35:54Z
{"n": 28, "s": 34, "c": 11, "k": 5, "dim_perp": 22, "dim_isotropic": 12, "D9_herm_orthogonal_to_G9": true, "rowspace_S_equals_phi_D9": true}
d=15 count=26676 enumerated=10460353203
d=15 count=22302 enumerated=10460353203
d=15 count=22302 enumerated=10460353203
computed n=28 k=5 c=11 d=15 (71280 words of weight d; enumerated 31381059609 vectors, 3^22 = 31381059609); claimed n=28 k=5 c=11 d=15
D9 Hermitian-orthogonal to G9: True; rowspace(S) = phi(D9): True
PASS
real 57.35
user 141.15
sys 1.22
exit=0
2026-10-24T11:36:52Z
```
