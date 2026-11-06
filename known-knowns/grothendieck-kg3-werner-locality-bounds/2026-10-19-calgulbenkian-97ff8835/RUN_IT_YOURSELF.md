# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`.

The object is the certificate: `object/dual_certificates.txt` (main object, sha256 in `INDEX.csv`) and `object/lower_bound_witness.txt`; their format is in `verify-it-yourself/DATA.md`. The instance matrix `d8_n1_120x120.mat` is the paper authors' file and is not shipped. The script fetches it with curl from Zenodo record 10.5281/zenodo.13693164 (https://zenodo.org/records/13693164/files/d8_n1_120x120.mat, 239024 bytes) and checks its sha256 `a78361f200b669741a4a0636bb4e1027a1e6cdfeca174c84ef67269a17bbeaac`. If you already have the file, run `MAT=/path/to/d8_n1_120x120.mat sh verify-it-yourself/run_checks.sh` instead.

The script checks the sha256 of the certificate against `INDEX.csv` and of the matrix against the value above, runs the standalone checker (standard library only), and runs two negative controls that must be rejected.

## Regenerating the data files (optional)

`object/dual_certificates.txt` and `object/lower_bound_witness.txt` were made by `verify-it-yourself/optional/e8_gen_dual.py` (numpy and scipy) and `verify-it-yourself/optional/e8_gen_witness.py` (pulp with CBC). `run_checks.sh` does not run them; it only verifies the shipped data exactly.

## Rebuild

`how-we-built-it/RESULTS.md` is the contributor's write-up of the argument and `verify-it-yourself/UPPER_BOUND.md` is the step-by-step argument the checker relies on. The commands of the contributor's original run are not recorded.
