# Run It Yourself (`dreval-cross-study-ctrpv2-to-gdsc2`)

## 1. Fast Standalone Verification (`< 4 seconds`, Python 3.8+ Standard Library Only)

From the package root:
```bash
sh verify-it-yourself/run_checks.sh
```
This runs `verify-it-yourself/verify.py`, which:
1. Checks the `SHA-256` hash of `object/certificate.json` (`2b12c375e5851cdcccb0a617aaa10ffb61daca5e1fdd1d972984fe55658b0d69`) and all 26 files in `object/`.
2. Verifies that all 20 keyed prediction files `object/gdsc2_split_{0..9}_{sr,yn}.csv` have schema `(split, cell_line_name, drug_name, y_pred, y_pred_naive, y_pred_rf)` with **no copied `y` column** and **0 duplicate `(split, cell_line_name, drug_name)` keys** across all `402,924` evaluated rows (`39,377–40,730` rows/split, mean `40,292.4 ± 389.4` out of `47,296` shared-drug `GDSC2` pairs).
3. Joins `(cell_line_name, drug_name)` directly against the official `drevalpy` `GDSC2/GDSC2.csv` (`sha256 = 87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd`, from <https://zenodo.org/api/records/23159774/files/GDSC2.zip/content>) when present locally (via `DREVAL_GDSC2_CSV=/path/to/GDSC2.csv` or default cache paths) or against `keyed_reference_checksums` in `object/stage3_p3_gap_decomposition.json` when running offline.
4. Recomputes the 10-split means for `SchurBilinearExVivoDRP`, `RandomForest`, and `NaiveMeanEffectsPredictor`, and verifies the isolated `p3` mechanisms `(i)`, `(ii)`, and `(iii)` on the exact same predictions with the official `SS_tot` denominator held fixed.

## 2. Re-Scoring with External `GDSC2/GDSC2.csv`

To join and re-score the 20 keyed CSV files against your own copy of `GDSC2/GDSC2.csv` (`sha256 = 87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd`):
```bash
DREVAL_GDSC2_CSV=/path/to/GDSC2/GDSC2.csv python3 verify-it-yourself/verify.py
```
