# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 0 seconds on a laptop):

```text
sha256 matches INDEX.csv (160c2ca18bd51633b189cff33b081be588caec8dd0c124f8021406df547ba053)
== check_fmm_fast.py: exact Brent equations over Z, rank 1165, coefficient class Z
coefficient class: Z (max |coefficient| = 2; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 22176 blocks of 154 slots compared
PASS format=11x12x14 rank=1165
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=11x12x14 rank=1165: 8 of 22176 (a, b) blocks differ; first at A[1][2] x B[2][7]
negative control rejected as expected
ALL CHECKS PASS
```

## Lossless re-encoding

The panel checked the original file `object/11x12x14_m1165_Z.json` (dense rows): 1082598 bytes, sha256 `5cd673ec5425d0a2057030114643b89e7ba64d3c3a60aed4c097ca8b3a895e47`. It is over the 1,000,000-byte limit, so the package holds `object/11x12x14_m1165_Z.json` re-encoded with `"encoding": "sparse_flat_pairs"`: 212737 bytes, sha256 `160c2ca18bd51633b189cff33b081be588caec8dd0c124f8021406df547ba053`.

Conversion: `python3 -I verify-it-yourself/convert_sparse.py to-sparse ORIGINAL.json object/11x12x14_m1165_Z.json` (script in this folder, standard library only).

Round trip, run locally before packaging:

- Expanded the packaged file back to dense rows and compared it with the original entry by entry (`convert_sparse.py compare`): `SAME: n=[11, 12, 14] m=1165, 528910 entries compared, 0 differ`.
- The expansion, written as compact JSON, is byte for byte the original (sha256 `5cd673ec5425d0a2057030114643b89e7ba64d3c3a60aed4c097ca8b3a895e47`).
- `check_fmm_fast.py` (output above) reads the packaged sparse file directly and passes.
