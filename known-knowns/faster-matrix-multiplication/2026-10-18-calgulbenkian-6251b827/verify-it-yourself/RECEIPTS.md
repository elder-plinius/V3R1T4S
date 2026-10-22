# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 1 seconds on a laptop):

```text
sha256 matches INDEX.csv (6251b8275ad429823b4b00e535720e352df412ed71f51a9b65535f9cd5238cca)
== check_fmm_fast.py: exact Brent equations over Z, rank 1830, coefficient class Z
coefficient class: Z (max |coefficient| = 2; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 49152 blocks of 192 slots compared
PASS format=12x16x16 rank=1830
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=12x16x16 rank=1830: 24 of 49152 (a, b) blocks differ; first at A[4][1] x B[7][0]
negative control rejected as expected
ALL CHECKS PASS
```

## Lossless re-encoding

The panel checked the original file `object/12x16x16_m1830_Z.json` (dense rows): 2389541 bytes, sha256 `63fe3ce95aa2c533d8799310fc94769f0f48d090b2fc039de89f5ff23ab1b731`. It is over the 1,000,000-byte limit, so the package holds `object/12x16x16_m1830_Z.json` re-encoded with `"encoding": "sparse_flat_pairs"`: 460070 bytes, sha256 `6251b8275ad429823b4b00e535720e352df412ed71f51a9b65535f9cd5238cca`.

Conversion: `python3 -I verify-it-yourself/convert_sparse.py to-sparse ORIGINAL.json object/12x16x16_m1830_Z.json` (script in this folder, standard library only).

Round trip, run locally before packaging:

- Expanded the packaged file back to dense rows and compared it with the original entry by entry (`convert_sparse.py compare`): `SAME: n=[12, 16, 16] m=1830, 1171200 entries compared, 0 differ`.
- The expansion, written as compact JSON, is byte for byte the original (sha256 `63fe3ce95aa2c533d8799310fc94769f0f48d090b2fc039de89f5ff23ab1b731`).
- `check_fmm_fast.py` (output above) reads the packaged sparse file directly and passes.
