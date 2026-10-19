# Run It Yourself (`polaris-moleculeace-activity-cliff-mse`)

## One-line check

From the package root:

```sh
sh verify-it-yourself/run_checks.sh
```

This runs `verify-it-yourself/check_moleculeace_clss.py` across `object/` and `the-record-we-beat/` (verifying all 30 benchmark splits, RDKit `InChIKey[:14]` disjointness `overlap == 0` across all `30 / 30` targets, independent `sklearn.metrics.mean_squared_error` on overall/cliff/non-cliff subsets, `10,000`-resample paired and scalar bootstrap on `CHEMBL287_Ki` and all 30 targets, and `400` label-permutation null controls), followed by a negative control (replacing test predictions on `CHEMBL287_Ki` with the constant mean) to confirm that any non-record or tampered prediction file is rejected. Expected last line: `ALL CHECKS PASS`.

## Direct Python verification & optional end-to-end CPU retraining

```sh
python3 verify-it-yourself/check_moleculeace_clss.py
```

To retrain the primary headline benchmark `CHEMBL287_Ki` (`moleculeace-chembl287-ki`) from scratch on CPU (~45 seconds) and verify bit-level determinism (`max_abs_diff <= 1e-10`):

```sh
python3 how-we-built-it/run_clss_moleculeace.py --dataset CHEMBL287_Ki
```
