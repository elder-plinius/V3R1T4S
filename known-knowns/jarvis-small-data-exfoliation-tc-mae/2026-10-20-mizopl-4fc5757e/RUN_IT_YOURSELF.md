# Run It Yourself (`2026-10-20-mizopl-4fc5757e`)

1. Ensure `python3` (`>= 3.9`) with `numpy`, `scipy`, `scikit-learn`, and `jarvis-tools` (for optional structure re-featurization) is installed.
2. From the root of this package directory, execute:
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
3. The script verifies the SHA-256 digests of all prediction CSVs, `.csv.zip` archives, 5-fold CV CSVs, and `object/trained_models_jarvis_clss.npz`, audits zero-leakage split hygiene and 4-key structure sanitization against `object/data/*.json.zip` and `object/data/clean_structures/*.json.gz`, independently computes `sklearn.metrics.mean_absolute_error` and 1,000-sample bootstrap 90% CIs across seeds `0..9`, verifies the `p1` (`tinnet_N_ead`) and `p2` (5-fold CV paired superiority) results and negative controls, and prints `PASS` on the final line.
4. To also recompute all structure descriptors and re-train all three CLSS models from scratch on `train U val` (~12 seconds on CPU), run:
   ```sh
   python3 -B verify-it-yourself/check_jarvis_clss_package.py --retrain-from-structures
   ```
