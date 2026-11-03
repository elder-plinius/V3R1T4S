# Run It Yourself (`2026-10-20-mizopl-4fc5757e`)

1. Ensure `python3` (`>= 3.9`) with `numpy`, `scipy`, `scikit-learn`, and `onnxruntime` is installed.
2. From the root of this package directory, execute:
   ```sh
   sh verify-it-yourself/run_checks.sh
   ```
3. The script (`verify-it-yourself/check_jarvis_clss_package.py`) imports **zero contributor code**, verifies the SHA-256 digests of `object/jarvis_clss_results_manifest.json`, all per-material feature CSV shards (`object/features_*_part*.csv`), standard-operator ONNX models (`object/model_*.onnx`), prediction CSVs, `.csv.zip` archives, and 5-fold CV CSVs (`object/cv5_oof_*.csv`), audits disjoint `train`/`val`/`test` split hygiene, evaluates `object/model_dft_3d_exfoliation_energy.onnx` and `object/model_tinnet_N_ead.onnx` directly via `onnxruntime.InferenceSession` on the per-material feature CSVs to confirm exact agreement (`max |diff| < 1e-8`) with the submitted prediction CSVs, independently computes `sklearn.metrics.mean_absolute_error` and 1,000-sample bootstrap 90% CIs across seeds `0..9`, verifies the `p1` (`tinnet_N_ead`) and `p2` (5-fold CV paired superiority) results and negative controls, and prints `PASS` on the final line.
