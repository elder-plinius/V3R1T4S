# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 1 seconds on a laptop):

```text
sha256 matches INDEX.csv (e6a4c45402117cbaf7655b4a7f678ada83795053cd102c24873a5f1100519e2d)
== check_fmm_fast.py: exact Brent equations over Z, rank 2159, coefficient class Z
coefficient class: Z (max |coefficient| = 6; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 13 bits, slot width 15 bits, 57344 blocks of 224 slots compared
PASS format=14x16x16 rank=2159
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=14x16x16 rank=2159: 15 of 57344 (a, b) blocks differ; first at A[0][3] x B[0][2]
negative control rejected as expected
ALL CHECKS PASS
```

## Lossless re-encoding

The panel checked the original file `object/14x16x16_m2159_Z.json` (dense rows): 3105711 bytes, sha256 `b7a26ff2e48fc42540d7b837421651ac747fc9b6e8b69b745ddf78091f8dffd8`. It is over the 1,000,000-byte limit, so the package holds `object/14x16x16_m2159_Z.json` re-encoded with `"encoding": "sparse_flat_pairs"`: 632672 bytes, sha256 `e6a4c45402117cbaf7655b4a7f678ada83795053cd102c24873a5f1100519e2d`.

Conversion: `python3 -I verify-it-yourself/convert_sparse.py to-sparse ORIGINAL.json object/14x16x16_m2159_Z.json` (script in this folder, standard library only).

Round trip, run locally before packaging:

- Expanded the packaged file back to dense rows and compared it with the original entry by entry (`convert_sparse.py compare`): `SAME: n=[14, 16, 16] m=2159, 1519936 entries compared, 0 differ`.
- The expansion, written as compact JSON, is byte for byte the original (sha256 `b7a26ff2e48fc42540d7b837421651ac747fc9b6e8b69b745ddf78091f8dffd8`).
- `check_fmm_fast.py` (output above) reads the packaged sparse file directly and passes.
