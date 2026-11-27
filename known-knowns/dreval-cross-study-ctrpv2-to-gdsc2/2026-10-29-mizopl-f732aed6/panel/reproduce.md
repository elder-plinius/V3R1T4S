# Skeptic 1 — Reproducibility & Cryptographic Audit (`dreval-cross-study-ctrpv2-to-gdsc2`)

- reviewer: Reproducibility Skeptic (`reproduce`)
- context: fresh independent skeptic review session (zero shared context)
- target_id: `dreval-cross-study-ctrpv2-to-gdsc2`
- submission_id: `2026-10-29-mizopl-f732aed6`
- internal_panel_verdict: `CONFIRMED_PARTIAL` (`partial_win: p3`)

## 1. Independent Execution of `verify-it-yourself/run_checks.sh`

Executed from a clean environment using only the Python 3.8+ standard library:
```bash
sh verify-it-yourself/run_checks.sh
```
Result: exited `0` with final line `PASS` in `< 4` seconds.

## 2. Verification of Keyed Prediction Files & Upstream `GDSC2/GDSC2.csv` Join

1. **Keyed Schema & Zero Copied Labels:** Inspected all 20 row-sharded CSV files `object/gdsc2_split_{0..9}_{sr,yn}.csv` (`<= 905,085` bytes each, strictly under the `1 MB` per-file cap). Every file has header `split,cell_line_name,drug_name,y_pred,y_pred_naive,y_pred_rf` with **zero** upstream `y` (`response` / `LN_IC50_curvecurator`) values copied into `object/`.
2. **Row Count & Uniqueness:** Concatenating the 20 CSV files yields exactly `402,924` evaluated test rows across the 10 splits (`39,377–40,730` rows/split, mean `40,292.4 ± 389.4` out of `47,296` shared-drug pairs in `GDSC2/GDSC2.csv`), with **0 duplicate `(split, cell_line_name, drug_name)` keys**.
3. **Upstream Response Join:** Joined `(cell_line_name, drug_name)` directly against the official `drevalpy` `GDSC2/GDSC2.csv` (`57,384,361` bytes, `sha256 = 87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd`, extracted from `https://zenodo.org/api/records/23159774/files/GDSC2.zip/content`, `sha256 = 4b0230cfcf7a670aba386d4af559eebabf3f13190517d9eb0dc67596b84ac031`). Recomputed the 10-split means and verified exact agreement (`max_abs_diff < 1e-5`) with `object/certificate.json` (`sha256 = 2b12c375e5851cdcccb0a617aaa10ffb61daca5e1fdd1d972984fe55658b0d69`) and `object/stage3_p3_gap_decomposition.json`.

pass: true
