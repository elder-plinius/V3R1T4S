# Chain-of-Thought & Air-Gap Provenance Audit (`dreval-cross-study-ctrpv2-to-gdsc2`)

- **Target ID:** `dreval-cross-study-ctrpv2-to-gdsc2`
- **Submission ID:** `2026-10-29-mizopl-f732aed6`
- **Claim Scope:** `CONFIRMED_PARTIAL` (`partial_win: p3`, internal 3-skeptic panel status) — measured decomposition of the `CTRPv2` (`CellTiter-Glo` luminescent ATP assay, RNA-seq TPM) $\to$ `GDSC2` (`Syto60` fluorescent nucleic-acid stain / `Resazurin` assay, Affymetrix RMA microarray) transfer gap across all 10 official `drevalpy` `LCO` splits by re-scoring the **same** model predictions under isolated mechanisms `(i)` concentration-range restriction, `(ii)` cell-line overlap restriction, and `(iii)` response-scale calibration.

---

## 1. Chronological Air-Gap Provenance (`Stage 0` $\to$ `Stage 4`)

1. **`Stage 0` (`how-we-built-it/stage0_download_and_manifest.py`, `2026-10-29T15:14:01Z`):**
   - Downloaded the official `drevalpy==1.6.0` Zenodo benchmark archives (Record `23159774`, DOI `10.5281/zenodo.23159774`) and recorded their cryptographic hashes in `object/manifest_sha256.json`:
     - `GDSC2.zip` (`https://zenodo.org/api/records/23159774/files/GDSC2.zip/content`, `521,509,357` bytes, `md5 = 49dc16929c6baa2b5d75c508429fa11f`, `sha256 = 4b0230cfcf7a670aba386d4af559eebabf3f13190517d9eb0dc67596b84ac031`).
     - Extracted `GDSC2/GDSC2.csv` (`57,384,361` bytes, **`sha256 = 87c284eaf50c41e4ffd870220f67230b826068c3d08085a9a83caec62024bcbd`**): `234,436` total rows, `90,666` non-NaN `LN_IC50_curvecurator` rows, `88,401` feature-complete `(cell_line_name, drug_name)` pairs, and **`47,296` shared-drug pairs** across `509` GDSC2 cell lines and `118` drugs shared with `CTRPv2` via PubChem CID.
     - `CTRPv2.zip` (`https://zenodo.org/api/records/23159774/files/CTRPv2.zip/content`, `518,522,899` bytes, `md5 = a3a6cc49ed57ba1c9b163e56b88cce2f`, `sha256 = 5ad3e867d3eda55595a981fd3f6426cb0a6a59218f109e9df68af50ffe2673bd`) and extracted `CTRPv2/CTRPv2.csv` (`143,722,503` bytes, **`sha256 = 14488de3ecff0a7499eddbc10d22cdec389549c8506a93516a547e619f90b412`**).

2. **`Stage 1` (`how-we-built-it/stage1_inspect_and_verify_metrics.py`):**
   - Verified the `drevalpy` `eval_metrics.py` normalization formula `_normalize_metrics_by_mean_effects(y_true, y_pred, y_pred_naive)` without reading any `GDSC2` response values:
     $$R^2_{\text{norm}} = 1 - \frac{\sum_{i=1}^N (y_i - \hat{y}_i)^2}{\sum_{i=1}^N \big((y_i - y_{\text{naive},i}) - \overline{(y - y_{\text{naive}})}\big)^2}$$
   - Identified the exact algebraic asymmetry that drives cross-study `R^2_norm < 0`: the denominator $\text{SS}_{\text{tot}}$ centers $y - y_{\text{naive}}$ by the cross-study assay mean shift $\Delta_{\text{assay}} = \overline{y - y_{\text{naive}}}$, whereas the numerator $\text{SS}_{\text{res}} = \sum (y_i - \hat{y}_i)^2$ is uncentered. Consequently, even `NaiveMeanEffectsPredictor` ($\hat{y} = y_{\text{naive}}$) incurs $\text{SS}_{\text{res}} = \text{SS}_{\text{tot}} + N \Delta_{\text{assay}}^2$ and scores $R^2_{\text{norm}} = -N \Delta_{\text{assay}}^2 / \text{SS}_{\text{tot}} < 0$.

3. **`Stage 2` (`how-we-built-it/stage2_inner_ablation.py` & `how-we-built-it/models.py`, locked at `2026-10-29T16:54:12Z`):**
   - Trained and selected all hyperparameters of `SchurBilinearExVivoDRP` strictly on the `CTRPv2` `LCO` inner validation splits (`GDSC2.csv` untouched, `external_response_files_touched_during_stage2 = false`, pre-registration lock hash `5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a`).
   - Replaced raw cross-platform gene-expression scaling with within-sample van der Waerden rank-normal scores ($\Phi^{-1}(\text{rank}/(G+1))$ across the overlapping gene set) plus 35-Hallmark pathway activity projection so each test cell line's transcriptomic vector is computed from that single cell line alone (`single_row_inductive_max_diff = 0.0`).
   - On `CTRPv2` `LCO` test splits, `SchurBilinearExVivoDRP` achieves $R^2_{\text{norm}} = +0.17153 \pm 0.03581$, $\text{Pearson}_{\text{norm}} = +0.41460 \pm 0.04189$, $\text{MSE} = 1.57581$.

4. **`Stage 3` & `Stage 4` (`how-we-built-it/stage3_exvivo_and_cross_study_eval.py` & `how-we-built-it/stage4_formalities_and_nulls.py`):**
   - Evaluated the frozen `CTRPv2`-trained models (`SchurBilinearExVivoDRP`, `RawPlatformKRR_Ablation`, `RandomForest_SameEnv`, `GradientBoosting_SameEnv`, `NaiveMeanEffectsPredictor`) on `GDSC2` across all 10 official `LCO` splits.
   - **Row-count accounting (`40,292.4` vs `47,296`):** Out of `47,296` shared-drug `(cell_line_name, drug_name)` pairs in `GDSC2` (`509` GDSC2 cell lines $\times$ `118` shared drugs), each split excludes the `352–386` overlapping cell lines that appear in that split's 90% `CTRPv2` training fold (preventing cell-line train$\to$test leakage), leaving `427–436` GDSC2 test cell lines (`375` disjoint GDSC2-only lines + `52–61` overlapping lines from the held-out 10% `CTRPv2` test fold) and **`39,377–40,730` evaluated rows per split (mean `40,292.4 ± 389.4`, total `402,924` rows across 10 splits)**.
   - Exported keyed per-split predictions in `object/gdsc2_split_{0..9}_{sr,yn}.csv` with schema `(split, cell_line_name, drug_name, y_pred, y_pred_naive, y_pred_rf)` (zero upstream `y` values copied into `object/`, zero duplicate keys) and executed the isolated `p3` mechanism decomposition on the exact same predictions.
