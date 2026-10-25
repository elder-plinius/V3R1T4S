# V3R1T4S 3-Skeptic Verification Panel — REPRODUCE Adversary Report

- **Target ID:** `linear-baseline-perturbation-replogle-k562`
- **Run Directory:** `.`
- **Role:** `REPRODUCE` Adversary (CONSTITUTION v18 §6 Stage 4)
- **Certificate:** [`claim/certificate_replogle_k562.json`](object/certificate_replogle_k562.json)
- **Certificate SHA-256:** `71c4fdf154e6f8cccfe44f18817dfa78f0863a5cadd8f964026e2a4670bf6c7e` (Expected: `71c4fdf154e6f8cccfe44f18817dfa78f0863a5cadd8f964026e2a4670bf6c7e` — **EXACT MATCH**)

---

## 1. Independent Execution of `claim/verify.py`

Executed `python3 claim/verify.py` in a clean read-only session. It completed in **`13.49 s`** with **exit code `0`**, passing all 5 certificate audit gates and the live solver recomputation gate:

1. **Dataset Provenance & SHA-256 Audit (`[1/5]`):** Verified all 8 SHA-256 hashes (`single_perturbation_prediction.xlsx`, `suppl-pearson_delta_performance_single_pert.xlsx`, `suppl-k562_rpe1_transfer.xlsx`, `perturbation_prediction.xlsx`, `go_essential_all.csv`, and the three GEARS `perturb_processed.h5ad` files for `replogle_k562_essential`, `replogle_rpe1_essential`, and `adamson`).
2. **Partial Win `p3` Reproduction of Record (`[2/5]`):** Verified exact reproduction of `mean` and `lpm_selftrained` (`Panel A`), and `lpm_k562PertEmb`, `lpm_rpe1PertEmb`, and `lpm_gearsPertEmb` (`Panel C`) across `replogle_k562_essential`, `replogle_rpe1_essential`, and `adamson` (`abs_diff <= 7e-6` for all deterministic baselines), as well as the 5-seed GEARS simulation splits (`seeds = 1:5`, `n = 677` on K562, `n = 1,063` on RPE1, `n = 135` on Adamson).
3. **Full Win Criteria on `replogle_k562_essential` (`[3/5]`):**
   - **Mean $L_2$ (`direction: min`):** `3.320307` vs `4.097028` (`lpm_selftrained`) and `4.078658` (`gears`, best published) $\longrightarrow$ **`-18.96%` vs `lpm_selftrained` (`57.47x` `lpm` SD, `31.25x` dual SD)**.
   - **Median $L_2$ (`direction: min`):** `3.044310` vs `3.805564` (`lpm_selftrained`) and `3.766328` (`uce`, best published median) $\longrightarrow$ **`-20.00%` vs `lpm_selftrained` (`63.87x` `lpm` SD)**.
   - **Mean Pearson $\Delta$ (`direction: max`):** `0.620623` vs `0.435544` (`lpm_selftrained`, best published) $\longrightarrow$ **`+42.49%` (`7.70x` `lpm` SD)**.
   - **Median Pearson $\Delta$ (`direction: max`):** `0.644965` vs `0.426484` (`lpm_selftrained`, best published) $\longrightarrow$ **`+51.23%`**.
4. **Partial Wins `p1` & `p2` (`[4/5]`):**
   - **`p1` (`replogle_rpe1_essential`, `Panel A`, `n = 413`):** Mean $L_2 = 4.777953$ vs `5.390179` (`-11.36%`, `2.65x` `lpm` SD); Mean Pearson $\Delta = 0.719286$ vs `0.680388` (`+5.72%`).
   - **`p2` (Functional Distance Stratification):** `Q1_closest` (`n = 66`) achieves $\Delta L_2 = -1.404930$ (`-32.33%`) vs `Q4_farthest` (`n = 66`) $\Delta L_2 = -0.404255$ (`-10.40%`), Spearman $r_s = +0.345058$ ($p = 9.7126 \times 10^{-9}$).
5. **Null / Permutation Control Battery (`[5/5]`):**
   - `replogle_k562_essential` (`100` combined / `200` split runs): Real $L_2 = 3.320307$ vs Null $4.971309 \pm 0.067250$ (`min = 4.798990`, **$Z = 24.55\sigma$**).
   - `replogle_rpe1_essential` (`50` combined / `100` split runs): Real $L_2 = 4.777953$ vs Null $6.231428 \pm 0.064759$ (`min = 6.085542`, **$Z = 22.44\sigma$**).
6. **Live Solver Recomputation across All 3 Datasets:**
   - In addition to `verify.py`'s live check on `replogle_k562_essential`, I independently ran live solver recomputations in memory on `replogle_rpe1_essential` and `adamson` (`seeds = 1:2`, `Panel A`). All three datasets reproduced the certificate values to `0.000000` (`K562`: `3.320307` / `0.620623`; `RPE1`: `4.777953` / `0.719286`; `Adamson`: `3.572436` / `0.770321`).

---

## 2. Code & Leakage Audit (`certify_all_splits_and_controls.py`, `reproduce_baselines.py`, `lens1_lens2_engine.py`)

### (a) Zero Train/Test/Val Leakage Audit & Active Poisoning Test
1. **Static Code Audit:**
   - In [`certify_all_splits_and_controls.py`](how-we-built-it/certify_all_splits_and_controls.py#L112-L361) (`run_ablation_variant`):
     - `train_mask = splits_psce == "train"` strictly isolates training conditions (`train` plus `ctrl`).
     - `train_change = change_psce[:, train_mask].copy()`, `train_clean = clean_psce[train_mask]`, and `train_counts = counts_psce[train_mask]` are the **only** expression responses and cell counts used anywhere in the function.
     - The de-spiked trans-mean `mu_trans`, residual matrix `R_trans_train`, cis-knockdown ridge regression weights `w_cis` (lines `132–179`), Lens 1 SVD subspace `pca_x` and bilinear operator `P_A, G_B, H_B` (lines `196–229`), Lens 2 co-expression similarities `R_nc_unit` and `E_svd_unit` (lines `254–274`), Hollow-LOO top-$k$ channels (lines `276–312`), and non-negative stacking weights `w_stack_A, w_stack_B` (lines `314–335`) are all fitted exclusively on `train_mask` columns (`idx_A` / `tr_nc_global_idx`).
     - In [`lens1_lens2_engine.py`](how-we-built-it/lens1_lens2_engine.py#L33-L79) (`build_go_idf_features`), the GO IDF cosine and Jaccard matrices `S_go_idf` and `S_go_jaccard` are built purely from `gene2go_all.pkl` and `essential_all_data_pert_genes.pkl` with zero expression data.
2. **Active Held-Out Expression Poisoning Test:**
   - To mathematically prove zero leakage from held-out (`test` and `val`) columns of `X_mean` and `counts`, I executed an in-memory poisoning test across all 3 datasets (`replogle_k562_essential`, `replogle_rpe1_essential`, `adamson`) and both splits (`seed = 1, 2`) where every non-`train` column of `X_mean` and `counts` was overwritten with `1e9` prior to calling `run_ablation_variant`.
   - **Result:** `max_poison_diff = 0.0` across all conditions and all three datasets (`0.0` maximum absolute difference between clean and poisoned runs). Held-out expression measurements are never read or touched during training or inference.

### (b) Exact Agreement with the Paper's Scoring Code (`evaluate_predictions`)
- Inspected [`reproduce_baselines.py`](how-we-built-it/reproduce_baselines.py#L345-L396) (`evaluate_predictions`):
  - Identifies the control profile `baseline = X_mean[:, ctrl_idx]` and ranks genes in descending order of control expression using stable mergesort (`order = np.argsort(-baseline, kind="mergesort")[:1000]`), which is an exact match to R's `rank(desc(observed), ties = "first") <= 1000` in `single_perturbation_analysis.Rmd`.
  - Computes per-perturbation Euclidean distance `l2 = sqrt(sum((p_v - o_v)**2))` over the top 1,000 read-out genes, Pearson correlation `r2 = corrcoef(p_v, o_v)[0, 1]`, and Pearson delta `r2_delta = corrcoef(p_v - b_v, o_v - b_v)[0, 1]`.
  - Confirmed that this scoring function reproduces the paper's published Source Data (`single_perturbation_prediction.xlsx`) for `mean` and `lpm_selftrained` to `0.000000` (`L2`) and `0.000000–0.000001` (`r2_delta`) across all three datasets.

### (c) Cryptographic Hash Verification
- `shasum -a 256 claim/certificate_replogle_k562.json` returned:
  `71c4fdf154e6f8cccfe44f18817dfa78f0863a5cadd8f964026e2a4670bf6c7e`
  which matches the expected hash in `RESULT.md`, `claim/artifact.md`, and `null_test.md` digit-for-digit.

---

VERDICT: PASS
