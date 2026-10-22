# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 0 seconds on a laptop):

```text
sha256 matches INDEX.csv (66011ac1f5e75b0684243a5546c3a163f98eb01e79ead74b30785c07829f0f66)
== check_fmm_fast.py: exact Brent equations over Z, rank 1540, coefficient class Z
coefficient class: Z (max |coefficient| = 2; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 34496 blocks of 176 slots compared
PASS format=11x14x16 rank=1540
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=11x14x16 rank=1540: 8 of 34496 (a, b) blocks differ; first at A[5][3] x B[0][2]
negative control rejected as expected
ALL CHECKS PASS
```

## Lossless re-encoding

The panel checked the original file `object/11x14x16_m1540_Z.json` (dense rows): 1734675 bytes, sha256 `3941762fa020763da24af886cc5e98a8c9b0e006dcb1e2f9cea9e061cc2712d1`. It is over the 1,000,000-byte limit, so the package holds `object/11x14x16_m1540_Z.json` re-encoded with `"encoding": "sparse_flat_pairs"`: 248515 bytes, sha256 `66011ac1f5e75b0684243a5546c3a163f98eb01e79ead74b30785c07829f0f66`.

Conversion: `python3 -I verify-it-yourself/convert_sparse.py to-sparse ORIGINAL.json object/11x14x16_m1540_Z.json` (script in this folder, standard library only).

Round trip, run locally before packaging:

- Expanded the packaged file back to dense rows and compared it with the original entry by entry (`convert_sparse.py compare`): `SAME: n=[11, 14, 16] m=1540, 853160 entries compared, 0 differ`.
- The expansion, written as compact JSON, is byte for byte the original (sha256 `3941762fa020763da24af886cc5e98a8c9b0e006dcb1e2f9cea9e061cc2712d1`).
- `check_fmm_fast.py` (output above) reads the packaged sparse file directly and passes.
