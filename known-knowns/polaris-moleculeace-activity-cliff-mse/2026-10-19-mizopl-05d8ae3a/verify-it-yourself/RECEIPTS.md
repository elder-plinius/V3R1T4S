# Verification Receipts (`polaris-moleculeace-activity-cliff-mse`)

## 1. Execution Receipt: `sh verify-it-yourself/run_checks.sh`

- **Command:** `sh verify-it-yourself/run_checks.sh`
- **Checker Script:** `verify-it-yourself/check_moleculeace_clss.py` (`17021` bytes, `sha256: f567b75d2f854c236d737aa3ab2e1e7f0ff0b928cdd605225f26acc20da69413`)
- **Primary Object File:** `object/CHEMBL287_Ki_test_predictions.csv` (`28516` bytes, `sha256: 37ced5b182f800041f6fcbff6bf9d5c5436fab3fc19f11155545067dff3d7d38`, columns: `test_row_index,csv_row_index,y_pred_clss,y_pred_stage1,y_pred_stage2,y_pred_lens1,y_pred_svm_ecfp_baseline` — zero copied MoleculeACE columns)
- **Primary Manifest File:** `object/CHEMBL287_Ki_manifest.json` (`5860` bytes, `sha256: d3e9d581acd324c9a780697edff8111bb79149772db2b216028011eef75c5f6f`)
- **30-Target Sweep Manifest:** `object/moleculeace_30_sweep_manifest.json` (`51074` bytes, `sha256: e10850b18add6800af7fd6d032db341a05c9deaae1ed9837f1ce7785c84c62c5`)
- **Exit Code:** `0`

### Exact Terminal Output
```text
=== [1/2] Verifying polaris-moleculeace-activity-cliff-mse predictions and 30-target sweep ===
Verified polaris-moleculeace-activity-cliff-mse: CHEMBL287_Ki MSE=0.40802135 (-18.91% vs Polaris 0.50318131, -20.01% vs Paper 0.51009699, boot_paired=99.97%, boot_scalar=97.98%, cliff_MSE=0.50213600 -18.85%, null_400_z=-13.61); 30-target sweep: 29/30 Polaris wins, 21/30 full-gate wins, macro_cliff_RMSE=0.7211
PASS
=== [2/2] Negative control: constant-mean predictions on CHEMBL287_Ki (must fail) ===
Negative control rejected as expected.
ALL CHECKS PASS
```

## 2. Deterministic Retraining Receipt (`CHEMBL287_Ki`)
- **Command:** `python3 how-we-built-it/run_clss_moleculeace.py --dataset CHEMBL287_Ki`
- **Script:** `how-we-built-it/run_clss_moleculeace.py` (`25450` bytes, `sha256: d0b03f84bb29218a1c5e495d83fc36319e8d46947f7ab31864b6a6332d24fdcf`)
- **Exit Code:** `0`
- **Max Absolute Difference vs. Saved `object/CHEMBL287_Ki_test_predictions.csv`:** `4.44e-16` (exact IEEE-754 floating-point match across `y_pred_clss`, `y_pred_stage1`, `y_pred_stage2`, and `y_pred_svm_ecfp_baseline`).
