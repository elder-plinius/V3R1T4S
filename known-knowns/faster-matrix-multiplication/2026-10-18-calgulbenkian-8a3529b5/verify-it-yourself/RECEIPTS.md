# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 0 seconds on a laptop):

```text
sha256 matches INDEX.csv (8a3529b5faa6980bfd9cfa355ead52b93efec2cb36f6d6f2ab076a43e1215922)
== check_fmm_fast.py: exact Brent equations over Z, rank 1547, coefficient class ZT
coefficient class: ZT (max |coefficient| = 1; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 34496 blocks of 176 slots compared
PASS format=11x14x16 rank=1547
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=11x14x16 rank=1547: 8 of 34496 (a, b) blocks differ; first at A[5][3] x B[0][2]
negative control rejected as expected
ALL CHECKS PASS
```

## Lossless re-encoding

The panel checked the original file `object/11x14x16_m1547_ZT.json` (dense rows): 1743002 bytes, sha256 `2a7d22e9c0e1881aeedfe29f53a8d2423673ca7dbf827f4eece7a598d2a93da7`. It is over the 1,000,000-byte limit, so the package holds `object/11x14x16_m1547_ZT.json` re-encoded with `"encoding": "sparse_flat_pairs"`: 249977 bytes, sha256 `8a3529b5faa6980bfd9cfa355ead52b93efec2cb36f6d6f2ab076a43e1215922`.

Conversion: `python3 -I verify-it-yourself/convert_sparse.py to-sparse ORIGINAL.json object/11x14x16_m1547_ZT.json` (script in this folder, standard library only).

Round trip, run locally before packaging:

- Expanded the packaged file back to dense rows and compared it with the original entry by entry (`convert_sparse.py compare`): `SAME: n=[11, 14, 16] m=1547, 857038 entries compared, 0 differ`.
- The expansion, written as compact JSON, is byte for byte the original (sha256 `2a7d22e9c0e1881aeedfe29f53a8d2423673ca7dbf827f4eece7a598d2a93da7`).
- `check_fmm_fast.py` (output above) reads the packaged sparse file directly and passes.
