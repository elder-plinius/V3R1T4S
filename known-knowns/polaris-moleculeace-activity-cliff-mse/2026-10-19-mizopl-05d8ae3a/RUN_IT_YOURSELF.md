# Run It Yourself (`polaris-moleculeace-activity-cliff-mse`)

## 1. Fast Verification of Saved Predictions (`~18 seconds` on CPU)
From the package root directory, run:
```sh
sh verify-it-yourself/run_checks.sh
```
This executes `verify-it-yourself/check_moleculeace_clss.py`, which:
1. Fetches the upstream `MoleculeACE_results.csv` and all 30 `CHEMBL*.csv` benchmark files from `https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/` (caching in `${MOLECULEACE_UPSTREAM_CACHE:-/tmp/moleculeace_upstream_cache}`) and verifies every `sha256` against `the-record-we-beat/polaris_moleculeace_30_audit.json` (stopping with an error if any `sha256` does not match), along with `object/CHEMBL287_Ki_test_predictions.csv` (`sha256: 05d8ae3a3797f666ed320364280c2ba0c099417174d42a0a4736f0366726623c`), `object/CHEMBL287_Ki_manifest.json`, `object/moleculeace_30_sweep_manifest.json`, and all 30 prediction CSVs in `object/predictions/`.
2. Verifies that every `split == 'test'` row index, `smiles`, `cliff_mol` indicator, and `y` (`log10(nM)`) value matches the official MoleculeACE CSV and Polaris API split counts (`1,061` train, `267` test, `103` cliff on `CHEMBL287_Ki`).
3. Recomputes RDKit canonical SMILES and stereo-stripped 14-character `InChIKey[:14]` sets across all 30 datasets and asserts `0` overlap between the training molecules used and the test set on all `30 / 30` benchmarks.
4. Recomputes `sklearn.metrics.mean_squared_error` on overall, `cliff_mol == 1`, and `cliff_mol == 0` subsets, runs the `10,000`-resample paired and scalar bootstrap (`seed=0`), and runs `400` label-permutation null controls (`seed=42`) on `CHEMBL287_Ki`.
5. Prints `PASS` on the final line and exits with code `0`.

## 2. Optional End-to-End CPU Retraining from Scratch (`~45 seconds` for `CHEMBL287_Ki`)
To retrain the deterministic 3-stage CLSS model from scratch on CPU for the primary headline benchmark `CHEMBL287_Ki`:
```sh
python3 how-we-built-it/run_clss_moleculeace.py --dataset CHEMBL287_Ki
```
