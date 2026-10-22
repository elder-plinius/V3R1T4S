# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 0 seconds on a laptop):

```text
sha256 matches INDEX.csv (5e82723f950cbeb60fda34ab64c3705dd1d7f3aacb2cbbdf74f6277dae6cd49f)
== check_fmm_fast.py: exact Brent equations over Z, rank 1472, coefficient class ZT
coefficient class: ZT (max |coefficient| = 1; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 32928 blocks of 168 slots compared
PASS format=12x14x14 rank=1472
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=12x14x14 rank=1472: 12 of 32928 (a, b) blocks differ; first at A[6][3] x B[0][0]
negative control rejected as expected
ALL CHECKS PASS
```

## Lossless re-encoding

The panel checked the original file `object/12x14x14_m1472_ZT.json` (dense rows): 1594029 bytes, sha256 `0cebed78a0b198d25f02ba2e7b6960bb4b83cc57c41f4f35e6501d8f731cd006`. It is over the 1,000,000-byte limit, so the package holds `object/12x14x14_m1472_ZT.json` re-encoded with `"encoding": "sparse_flat_pairs"`: 229171 bytes, sha256 `5e82723f950cbeb60fda34ab64c3705dd1d7f3aacb2cbbdf74f6277dae6cd49f`.

Conversion: `python3 -I verify-it-yourself/convert_sparse.py to-sparse ORIGINAL.json object/12x14x14_m1472_ZT.json` (script in this folder, standard library only).

Round trip, run locally before packaging:

- Expanded the packaged file back to dense rows and compared it with the original entry by entry (`convert_sparse.py compare`): `SAME: n=[12, 14, 14] m=1472, 783104 entries compared, 0 differ`.
- The expansion, written as compact JSON, is byte for byte the original (sha256 `0cebed78a0b198d25f02ba2e7b6960bb4b83cc57c41f4f35e6501d8f731cd006`).
- `check_fmm_fast.py` (output above) reads the packaged sparse file directly and passes.
