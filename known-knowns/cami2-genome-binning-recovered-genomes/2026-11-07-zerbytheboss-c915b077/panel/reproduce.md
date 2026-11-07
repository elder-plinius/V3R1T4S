# Skeptic 1: Reproducibility & Independent Computation Audit

context: independent clean-room verification process started from package directory only

## Audit Summary

1. Executed `sh verify-it-yourself/run_checks.sh` from a clean temporary copy of the package.
2. Verified that `verify-it-yourself/check_cami2_binning.py` independently parses the refined CAMI `.binning.gz` outputs in `object/` (`strain_madness_refined.binning.gz`, `plant_associated_refined.binning.gz`, `marine_refined_part1.binning.gz`, `marine_refined_part2.binning.gz`) and recomputes every bin's `recall_bp = tp_length_bp / gs_length_bp`, `precision_bp = tp_length_bp / total_length_bp`, high-quality status (`recall_bp > 0.90` and `precision_bp > 0.95`), and base-pair Adjusted Rand Index (`ARI (bp)`) against `verify-it-yourself/data/*_amber_ref*.json.gz`, matching all 1,325 bin rows in `object/amber_cami2_per_bin_metrics.tsv`.
3. Confirmed that mutating a single digit in `object/amber_cami2_per_bin_metrics.tsv` causes `run_checks.sh` to exit with code 1 and output `FAIL`.

pass: true
