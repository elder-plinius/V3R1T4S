# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. The script checks the sha256 of the object against `INDEX.csv`, runs the standalone checker (standard library only), prints the comparison with the saved record in `the-record-we-beat/`, and runs a negative control that must be rejected.

## What the check does

`run_checks.sh` first reassembles `object/feigenbaum_z4_certificates.part01.txt` to `part06.txt` into the whole JSON file (4846021 bytes, sha256 2fd7595e5467256b137eb202bfcfe1ddbae3bc843bb6df1a8b601ea40ecd1ca6) and checks the sha256 of the whole file and of each part against `object/PARTS.sha256` and `INDEX.csv`. The object was split only because the original file is larger than the 1 MB per-file limit; the parts are the original bytes, cut every 900000 bytes. The panel's claim folder named them `feigenbaum_z4_certificates.json.part01` to `part06`; here they are named `feigenbaum_z4_certificates.part01.txt` to `part06.txt` (same bytes, sha256 values unchanged in `object/PARTS.sha256`, whose file names were updated). `cat object/feigenbaum_z4_certificates.part*.txt > whole.json` makes the file by hand. Then `z4_check.py` (standard library only) evaluates both Chebyshev series by Clenshaw's recurrence in decimal arithmetic at 1300 digits, forms the fixed-point and eigen-equation residuals at 31 points for each resolution, and prints alpha_4, delta_4 and the numbers of agreeing decimals. A negative control changes one coefficient by 1e-900 and must be rejected.

## Rebuild

`how-we-built-it/` holds the solver and polisher (Python with numpy, scipy and gmpy2, plus a C library over MPFR). The compiled library is not shipped, the compile command is not recorded, and the original run commands are inferred, not logged (see `how-we-built-it/README.md`). A rebuild is not promised to give byte-identical output.
