# Skeptic 1: Reproducibility & Independent Computation Audit

context: independent clean-room verification process started from package directory only

## Audit Summary

1. Executed `sh verify-it-yourself/run_checks.sh` from a clean temporary copy of the package.
2. Verified that `check_disdat_sdm.py` independently validates all 225 species rows in `object/disdat_225_species_auc.csv` against the ground-truth `test_pa` presence-absence vectors and suitability predictions (`pred_v3` and `pred_v2`) in `verify-it-yourself/data/disdat_pa_eval_00.json.gz .. disdat_pa_eval_44.json.gz` via Mann-Whitney U ROC AUC recomputation.
3. Confirmed that mutating a single digit in `object/disdat_225_species_auc.csv` causes `run_checks.sh` to exit with code 1 and output `FAIL`.

pass: true
