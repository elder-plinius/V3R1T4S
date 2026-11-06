# Run it yourself

## 1. Check the shipped object

From a fresh shell in this package folder, run:

```sh
sh verify-it-yourself/run_checks.sh
```

The last line should be `ALL CHECKS PASS`. A real run is recorded in `verify-it-yourself/RECEIPTS.md`. The script checks the sha256 of the object against `INDEX.csv`, runs the standalone checker (standard library only), prints the comparison with the saved record in `the-record-we-beat/`, and runs a negative control that must be rejected.

## Regenerating the data files (optional)

`verify-it-yourself/data/dual_certificates.txt` and `verify-it-yourself/data/lower_bound_witness.txt` were made by `verify-it-yourself/optional/e8_gen_dual.py` (numpy and scipy) and `verify-it-yourself/optional/e8_gen_witness.py` (pulp with CBC). `run_checks.sh` does not run them; it only verifies the shipped data exactly.

## Rebuild

`how-we-built-it/RESULTS.md` is the contributor's write-up of the argument and `verify-it-yourself/UPPER_BOUND.md` is the step-by-step argument the checker relies on. The commands of the contributor's original run are not recorded.
