# Verification Receipts (`polaris-moleculeace-activity-cliff-mse`)

## 1. Execution Receipt (`verify-it-yourself/run_checks.sh`)

```text
=== [1/2] Verifying polaris-moleculeace-activity-cliff-mse predictions and 30-target sweep ===
Verified polaris-moleculeace-activity-cliff-mse: CHEMBL287_Ki MSE=0.40802135 (-18.91% vs Polaris 0.50318131, -20.01% vs Paper 0.51009699, boot_paired=99.97%, boot_scalar=97.98%, cliff_MSE=0.50213600 -18.85%, null_400_z=-13.61); 30-target sweep: 29/30 Polaris wins, 21/30 full-gate wins, macro_cliff_RMSE=0.7211
PASS
=== [2/2] Negative control: constant-mean predictions on CHEMBL287_Ki (must fail) ===
Negative control rejected as expected.
ALL CHECKS PASS
```

## 2. End-to-End CPU Retraining Receipt (`CHEMBL287_Ki`)

```text
CHEMBL287_Ki     | Pol=0.5032 Pap=0.5101 -> CLSS=0.408021 | Cliff: Pap=0.6188 -> 0.502136 [44.6s]
  [PASS] Retrained CHEMBL287_Ki from scratch: max |y_retrained - y_saved| = 4.441e-16 <= 1e-10
```
