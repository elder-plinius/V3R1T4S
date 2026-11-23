# Run It Yourself (`polaris-moleculeace-activity-cliff-mse`)

## 1. Environment & Dependencies
- **OS / Hardware:** Any macOS or Linux CPU (tested on Apple M1 CPU, 16 GB RAM; no GPU required).
- **Python packages:** `numpy`, `pandas`, `scipy`, `scikit-learn`, `lightgbm`, `pyyaml`, `joblib`, `rdkit`.

## 2. Fast Verification of Saved Predictions (`~18 seconds` on CPU)
From the root of this package directory:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected output:
```text
=== [1/2] Verifying polaris-moleculeace-activity-cliff-mse predictions and 30-target sweep ===
Verified polaris-moleculeace-activity-cliff-mse: CHEMBL287_Ki MSE=0.40802135 (-18.91% vs Polaris 0.50318131, -20.01% vs Paper 0.51009699, boot_paired=99.97%, boot_scalar=97.98%, cliff_MSE=0.50213600 -18.85%, null_400_z=-13.61); 30-target sweep: 29/30 Polaris wins, 21/30 full-gate wins, macro_cliff_RMSE=0.7211
PASS
=== [2/2] Negative control: constant-mean predictions on CHEMBL287_Ki (must fail) ===
Negative control rejected as expected.
ALL CHECKS PASS
```

Note: `verify-it-yourself/check_moleculeace_clss.py` (`17021` bytes, `sha256: f567b75d2f854c236d737aa3ab2e1e7f0ff0b928cdd605225f26acc20da69413`) automatically fetches the official MoleculeACE benchmark CSVs from `https://raw.githubusercontent.com/molML/MoleculeACE/main/MoleculeACE/Data/` and verifies their exact `sha256` digests against `the-record-we-beat/polaris_moleculeace_30_audit.json` (`38964` bytes, `sha256: 82a27869cb585c5e0d7d05f4584e9df925b0eeeb3db3a9b60f9e4f481eb2a5c1`). It also verifies that no prediction CSV in `object/` contains copied third-party MoleculeACE columns (`smiles`, `cliff_mol`, `y_true`, `y`) and verifies both the pre-test-scoring predictions (`y_pred_lens1` `0.42747335`, `y_pred_stage1` `0.42640543`, `y_pred_stage2` `0.42716055`) and the 3-stage prediction (`y_pred_clss` `0.40802135`) in `object/CHEMBL287_Ki_test_predictions.csv` (`28516` bytes, `sha256: 37ced5b182f800041f6fcbff6bf9d5c5436fab3fc19f11155545067dff3d7d38`).

## 3. Full Retraining From Scratch (`~30 seconds` for `CHEMBL287_Ki`)
To retrain the deterministic CLSS model (`how-we-built-it/run_clss_moleculeace.py`, `25450` bytes, `sha256: d0b03f84bb29218a1c5e495d83fc36319e8d46947f7ab31864b6a6332d24fdcf`) from raw SMILES on `CHEMBL287_Ki` (after placing the upstream `benchmark_data/`, `configures/`, and `baseline_and_inchikey_audit.json` inside `how-we-built-it/`):

```sh
python3 how-we-built-it/run_clss_moleculeace.py --dataset CHEMBL287_Ki
```

Expected output:
```text
CHEMBL287_Ki     | Pol=0.5032 Pap=0.5101 -> CLSS=0.408021 | Cliff: Pap=0.6188 -> 0.502136
```
