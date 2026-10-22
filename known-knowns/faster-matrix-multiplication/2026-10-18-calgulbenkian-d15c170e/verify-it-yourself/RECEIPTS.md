# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 0 seconds on a laptop):

```text
sha256 matches INDEX.csv (d15c170ec1b2e851ae520231c573b378daae1bedafb3c9362d4b73bc00751792)
== check_fmm_fast.py: exact Brent equations over Z, rank 1293, coefficient class Z
coefficient class: Z (max |coefficient| = 3; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 25344 blocks of 176 slots compared
PASS format=11x12x16 rank=1293
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=11x12x16 rank=1293: 12 of 25344 (a, b) blocks differ; first at A[2][10] x B[1][3]
negative control rejected as expected
ALL CHECKS PASS
```

## Lossless re-encoding

The panel checked the original file `object/11x12x16_m1293_Z.json` (dense rows): 1319972 bytes, sha256 `7b6a1a8cd9194651c7d7338fafdd2dcc3b3bd83c0a3edbafd21f414715f37565`. It is over the 1,000,000-byte limit, so the package holds `object/11x12x16_m1293_Z.json` re-encoded with `"encoding": "sparse_flat_pairs"`: 231741 bytes, sha256 `d15c170ec1b2e851ae520231c573b378daae1bedafb3c9362d4b73bc00751792`.

Conversion: `python3 -I verify-it-yourself/convert_sparse.py to-sparse ORIGINAL.json object/11x12x16_m1293_Z.json` (script in this folder, standard library only).

Round trip, run locally before packaging:

- Expanded the packaged file back to dense rows and compared it with the original entry by entry (`convert_sparse.py compare`): `SAME: n=[11, 12, 16] m=1293, 646500 entries compared, 0 differ`.
- The expansion, written as compact JSON, is byte for byte the original (sha256 `7b6a1a8cd9194651c7d7338fafdd2dcc3b3bd83c0a3edbafd21f414715f37565`).
- `check_fmm_fast.py` (output above) reads the packaged sparse file directly and passes.
