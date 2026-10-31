# Stage 4 Adversary Report — **CRITERION** (`linear-baseline-perturbation-replogle-k562`)

- **Run Directory:** `.`
- **Target ID:** `linear-baseline-perturbation-replogle-k562`
- **Pinned Benchmark Commit:** `bfa6eeea2bd145a1af2ec0127a2e808cc38456a9` (`const-ae/linear_perturbation_prediction-Paper`)
- **Certificate:** [`claim/certificate_replogle_k562.json`](object/certificate_replogle_k562.json) (`sha256 = 71c4fdf154e6f8cccfe44f18817dfa78f0863a5cadd8f964026e2a4670bf6c7e`)

---

## 1. Line-by-Line Audit of `target.md` & `PREREG.md` Full Win Criteria (`replogle_k562_essential`)

### 1.1 Split Firewall, Provenance & Zero-Leakage Training Scope
- **Dataset & Source Data SHA-256 Provenance:** All 8 dataset and Source Data SHA-256 hashes logged in `certificate_replogle_k562.json` match the exact GEARS Harvard Dataverse `.h5ad` files and Europe PMC Source Data `.xlsx` files:
  - `gears_pert_data/replogle_k562_essential/perturb_processed.h5ad`: `550fde89ac85c258c9fd517638fe34fb42c0e748c9305fe6355761a2bb754170`
  - `gears_pert_data/replogle_rpe1_essential/perturb_processed.h5ad`: `cc3e13da13ecd3cf7fb027b8261514a2bdcfab16fe47fc685b2714f79781afba`
  - `gears_pert_data/adamson/perturb_processed.h5ad`: `a737244a4e4c7cc20c0265185417523af8295769b23af274ac23be61fed25f91`
  - `gears_pert_data/go_essential_all/go_essential_all.csv`: `99622d9215462e7bbea99a5f6c0b1e86febfef9f57226269418053484fcb3f9f`
  - `single_perturbation_prediction.xlsx`: `09c6c198aff4e8a827064183f9cff13eb6f33e56f1689940527304bf78957efe`
  - `suppl-pearson_delta_performance_single_pert.xlsx`: `61658661412f385356a383c3ed506f4454c6db79b28c272151bb15a725b0faaa`
- **Zero-Leakage Training Verification (`PREREG.md` §1):** Code inspection of [`claim/certify_all_splits_and_controls.py`](how-we-built-it/certify_all_splits_and_controls.py) (`run_ablation_variant`, lines 71–361) and [`claim/reproduce_baselines.py`](how-we-built-it/reproduce_baselines.py) confirms that for every split seed:
  - Only `train_mask = (splits_psce == "train")` perturbations (plus `ctrl`, which GEARS assigns to `train`) are used to compute the control baseline `baseline`, the de-spiked training mean `mu_trans`, the cis-knockdown attenuation ridge weights `w_cis`, the PCA/SVD subspaces (`pca_x`, `E_svd_unit`), the training co-expression matrices (`S_coexp_full`, `S_coexp_svd`), and the non-negative Hollow-LOO stacking weights (`w_stack_A`, `w_stack_B`).
  - No `val` or `test` perturbation expression measurements enter training, gene selection, normalization, hyperparameter choice, or stacking, and zero cross-cell-line expression transfer (`RPE1` $\not\to$ `K562`) is used in `hollow_loo_dual_lens`.
  - Top-1,000 gene selection is determined solely by descending unperturbed `ctrl` expression (`np.argsort(-baseline, kind="mergesort")[:1000]`), matching `single_perturbation_analysis.Rmd` at commit `bfa6eeea2bd145a1af2ec0127a2e808cc38456a9`.

### 1.2 Quantitative Full Win Thresholds on `replogle_k562_essential`
- **Metric 1: Mean $L_2$ Distance over Top-1,000 Expressed Genes (`direction: min`):**
  - `lpm_selftrained` (published & same-env re-run): **`4.097028`** (`across_split_sd = 0.013196`)
  - Best published method in `single_perturbation_prediction.xlsx` (`gears`): **`4.078658`** (`across_split_sd = 0.064478`)
  - `hollow_loo_dual_lens` (Ours): **`3.320307`** (`across_split_sd = 0.024271`)
  - **Margin vs `lpm_selftrained`:** $-0.776721$ (**$-18.96\%$**, required $\ge 5\%$) and **$58.86\times$ `lpm_selftrained` SD** / **$32.00\times$ own SD** (required $\ge 2\times$ SD).
  - **Margin vs best published (`gears`):** $-0.758351$ (**$-18.51\%$ of `lpm_selftrained`**) and **$57.47\times$ `lpm_selftrained` SD** / **$31.25\times$ own SD** / **$11.76\times$ `gears` SD**.
- **Metric 2: Median $L_2$ Distance over Top-1,000 Expressed Genes (`direction: min`):**
  - `lpm_selftrained` (published `3.805557`, same-env re-run `3.805564`, `across_split_sd = 0.011305`)
  - Best published method (`uce`): **`3.766328`** (`across_split_sd = 0.015954`)
  - `hollow_loo_dual_lens` (Ours): **`3.044310`** (`across_split_sd = 0.058063`)
  - **Margin vs `lpm_selftrained`:** $-0.761254$ (**$-20.00\%$**, required $\ge 5\%$) and **$67.34\times$ `lpm_selftrained` SD**.
  - **Margin vs best published (`uce`):** $-0.722018$ (**$-18.97\%$ of `lpm_selftrained`**) and **$63.87\times$ `lpm_selftrained` SD** / **$45.26\times$ `uce` SD** / **$12.43\times$ own SD**.
- **Metric 3: Mean Pearson Delta (`r2_delta`, `direction: max`):**
  - `lpm_selftrained` (published & same-env re-run, also best published across all methods): **`0.435544`** (`across_split_sd = 0.024039`)
  - `hollow_loo_dual_lens` (Ours): **`0.620623`** (`across_split_sd = 0.016671`)
  - **Margin:** $+0.185079$ (**$+42.49\%$ of `lpm_selftrained`**, required $\ge 5\%$) and **$7.70\times$ `lpm_selftrained` SD** / **$11.10\times$ own SD** (required $\ge 2\times$ SD).
- **Metric 4: Median Pearson Delta (`r2_delta`, `direction: max`):**
  - `lpm_selftrained` (published `0.426484`, same-env re-run `0.426480`, best published, `across_split_sd = 0.020503`)
  - `hollow_loo_dual_lens` (Ours): **`0.644965`** (`across_split_sd = 0.042957`)
  - **Margin:** $+0.218481$ (**$+51.23\%$ of `lpm_selftrained`**, required $\ge 5\%$) and **$10.66\times$ `lpm_selftrained` SD** / **$5.09\times$ own SD** (required $\ge 2\times$ SD).
- **All 5 Published Splits (`seeds = 1:5`, `n = 677` in-readout & `n = 1,770` all held-out):**
  - On `in_readout_genes` (`n = 677`): `hollow_loo_dual_lens` achieves Mean $L_2 = \mathbf{3.332314}$ (`5-seed SD = 0.026505`) vs `lpm_selftrained` $4.168029$ (`5-seed SD = 0.060489`) — a **$-20.05\%$ reduction** (**$13.82\times$ `lpm_selftrained` 5-seed SD**, **$31.53\times$ own 5-seed SD**), Median $L_2 = \mathbf{3.085892}$ vs $3.871448$ (**$-20.29\%$**), and Mean Pearson $\Delta = \mathbf{0.633310}$ vs $0.437119$ (**$+44.88\%$**, **$10.42\times$ SD**).

---

## 2. Audit of Partial Wins (`p1`, `p2`, `p3`)

1. **Partial Win `p1` (`replogle_rpe1_essential` under identical protocol):**
   - **Panel A (`seeds = 1:2`, `n = 413`):**
     - Mean $L_2$: **`4.777953`** (`SD = 0.182955`) vs `lpm_selftrained` (and best published) **`5.390179`** (`SD = 0.230746`) $\longrightarrow$ **$-11.36\%$** ($\ge 5\%$) and **$2.65\times$ `lpm_selftrained` SD** / **$3.35\times$ own SD** ($\ge 2\times$ SD).
     - Median $L_2$: **`4.514809`** vs `lpm_selftrained` **`5.152959`** (`SD = 0.257376`) $\longrightarrow$ **$-12.38\%$** ($\ge 5\%$) and **$2.48\times$ `lpm_selftrained` SD** ($\ge 2\times$ SD).
     - Mean Pearson $\Delta$: **`0.719286`** vs `lpm_selftrained` **`0.680388`** $\longrightarrow$ **$+5.72\%$** ($\ge 5\%$).
   - **5-Seed Evaluation (`seeds = 1:5`, `n = 1,063` in-readout):**
     - Mean $L_2$: **`4.885882`** (`5-seed SD = 0.135296`) vs `lpm_selftrained` **`5.544850`** (`5-seed SD = 0.174215`) $\longrightarrow$ **$-11.88\%$** (**$3.78\times$ `lpm_selftrained` SD**, **$4.87\times$ own SD**).
     - Mean Pearson $\Delta$: **`0.709296`** vs `0.662573` (**$+7.05\%$**, **$2.36\times$ SD**).
   - **Status:** **`p1` PASS**.

2. **Partial Win `p2` (Functional Distance Stratification in Pre-Declared Embedding):**
   - `PREREG.md` §2 pre-declares $d_{\text{NN}}(p, \mathcal{T}_{\text{train}}) = 1 - \max_{q \in \mathcal{T}_{\text{train}}} S_{\text{func}}(p, q)$ combining GO similarity (`gene2go_all.pkl`) and training co-expression SVD cosine similarity.
   - On `replogle_k562_essential` (`n = 262`), quartile stratification shows strict monotonic concentration of $L_2$ error reduction and Pearson $\Delta$ gain in perturbations with close functional neighbors in `train`:
     - `Q1_closest` (`n = 66`, `nn_dist` $\in [0.1306, 0.4835]$): $\Delta L_2 = \mathbf{-1.404930}$ (**$-32.33\%$**), $\Delta r_{\Delta} = \mathbf{+0.224525}$
     - `Q2_mid_close` (`n = 65`): $\Delta L_2 = \mathbf{-0.776871}$ (**$-18.98\%$**), $\Delta r_{\Delta} = \mathbf{+0.219978}$
     - `Q3_mid_far` (`n = 65`): $\Delta L_2 = \mathbf{-0.516892}$ (**$-12.73\%$**), $\Delta r_{\Delta} = \mathbf{+0.172395}$
     - `Q4_farthest` (`n = 66`, `nn_dist` $\in [0.6475, 0.8338]$): $\Delta L_2 = \mathbf{-0.404255}$ (**$-10.40\%$**), $\Delta r_{\Delta} = \mathbf{+0.123755}$
     - Spearman rank correlation: $r_s = +0.345058$ ($p = 9.7126 \times 10^{-9}$) for $\Delta L_2$ and $r_s = -0.198624$ ($p = 0.0012297$) for $\Delta r_{\Delta}$.
   - Same direction and statistical significance hold on `replogle_rpe1_essential` (`n = 413`, `Q1_closest` $-17.39\%$ vs `Q4_farthest` $-7.38\%$, Spearman $p = 0.027768$ for $\Delta L_2$ and $p = 0.0024364$ for $\Delta r_{\Delta}$).
   - **Status:** **`p2` PASS**.

3. **Partial Win `p3` (Reproduction of Record across `seeds = 1:2` and `seeds = 1:5`):**
   - Exact reproduction (`abs_diff <= 7e-6`, `0.000000` on `mean` and `lpm_selftrained` across K562 and RPE1) of the paper's baselines (`mean`, `lpm_selftrained`, `lpm_k562PertEmb`, `lpm_rpe1PertEmb`) and `lpm_gearsPertEmb` across all 3 datasets (`replogle_k562_essential`, `replogle_rpe1_essential`, `adamson`), plus full 5-seed (`seeds = 1:5`) evaluation logged in `certificate_replogle_k562.json`.
   - **Status:** **`p3` PASS**.

---

## 3. Audit of `null_test.md` against `PREREG.md` §3

- `PREREG.md` §3 requires a target-gene identity permutation control battery demonstrating that permuted controls degrade back to (or worse than) the uninformative `mean` baseline and that the real model beats the null distribution by $>5\sigma$ (and beats the best of all permutation controls).
- `null_test.md` and `certificate_replogle_k562.json` report `300` split-level permutation evaluations (`200` split-level runs / `100` combined 2-seed runs on `replogle_k562_essential`, plus `100` split-level runs / `50` combined 2-seed runs on `replogle_rpe1_essential`):
  - **K562 (`200` split runs):** Null Mean $L_2 = 4.971309 \pm 0.067250$ (worse than `mean` baseline $4.193494$), best random realization $L_2 = 4.798990$ vs real model $L_2 = \mathbf{3.320307}$ (**$Z = 24.55\sigma$**; Pearson $\Delta$ **$Z = 31.78\sigma$**).
  - **RPE1 (`100` split runs):** Null Mean $L_2 = 6.231428 \pm 0.064759$ (worse than `mean` baseline $5.533708$), best random realization $L_2 = 6.085542$ vs real model $L_2 = \mathbf{4.777953}$ (**$Z = 22.44\sigma$**; Pearson $\Delta$ **$Z = 33.57\sigma$**).
- Live execution of `python3 claim/verify.py` completed in `12.96 s` with exit code `0`, confirming both cryptographic certificate integrity and live solver recomputation to `< 1e-6`.

---

VERDICT: PASS
