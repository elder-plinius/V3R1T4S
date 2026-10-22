# Receipts

Real output of `sh verify-it-yourself/run_checks.sh`, run from this package folder (exit code 0, 0 seconds on a laptop):

```text
sha256 matches INDEX.csv (fe61d3f4095f394da2714da53ef0bc37f20b4d3e621e78439c9fde41f4d02a04)
== check_fmm_fast.py: exact Brent equations over Z, rank 1516, coefficient class Z
coefficient class: Z (max |coefficient| = 2; ZT means all coefficients in {-1, 0, 1})
exact integer check: D=1 (DU=1, DV=1, DW=1), coefficient bound 11 bits, slot width 13 bits, 32448 blocks of 192 slots compared
PASS format=12x13x16 rank=1516
== negative control: a copy with the first nonzero coefficient of u[0] negated must FAIL
FAIL format=12x13x16 rank=1516: 6 of 32448 (a, b) blocks differ; first at A[5][1] x B[1][5]
negative control rejected as expected
ALL CHECKS PASS
```

## Lossless re-encoding

The panel checked the original file `object/12x13x16_m1516_Z.json` (dense rows): 1713599 bytes, sha256 `c60305d57c426d01cb0bafaad4e38fccfbe60ffcda25243f4eed94b1eb1da8bb`. It is over the 1,000,000-byte limit, so the package holds `object/12x13x16_m1516_Z.json` re-encoded with `"encoding": "sparse_flat_pairs"`: 234643 bytes, sha256 `fe61d3f4095f394da2714da53ef0bc37f20b4d3e621e78439c9fde41f4d02a04`.

Conversion: `python3 -I verify-it-yourself/convert_sparse.py to-sparse ORIGINAL.json object/12x13x16_m1516_Z.json` (script in this folder, standard library only).

Round trip, run locally before packaging:

- Expanded the packaged file back to dense rows and compared it with the original entry by entry (`convert_sparse.py compare`): `SAME: n=[12, 13, 16] m=1516, 842896 entries compared, 0 differ`.
- The expansion, written as compact JSON, is byte for byte the original (sha256 `c60305d57c426d01cb0bafaad4e38fccfbe60ffcda25243f4eed94b1eb1da8bb`).
- `check_fmm_fast.py` (output above) reads the packaged sparse file directly and passes.
