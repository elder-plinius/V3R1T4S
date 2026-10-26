# Stage 4 Skeptic Audit Report — **NOVELTY** Adversary (`linear-baseline-perturbation-replogle-k562`)

- **Run Directory:** `.`
- **Target ID:** `linear-baseline-perturbation-replogle-k562`
- **Auditor Role:** **NOVELTY** Adversary (3-Skeptic Verification Panel, CONSTITUTION v18 §6 Stage 4)
- **Audit Scope:** Scientific novelty, upstream literature & benchmark context, absence of competing/prior solutions on `elder-plinius/V3R1T4S`, mathematical/algorithmic advance over Ahlmann-Eltze, Huber & Anders (*Nature Methods* 2025), and strict intra-dataset training purity (`no cross-cell-line target expression`).

---

## 1. Competing Solutions & Upstream Repository Audit

1. **V3R1T4S PR & Issue Audit (`elder-plinius/V3R1T4S`):**
   - Queried all open, closed, and merged pull requests and issues on `elder-plinius/V3R1T4S` matching `replogle`, `k562`, `perturbation`, `linear-baseline`, or `ahlmann`.
   - **Result:** **0 competing PRs or issues** exist for `linear-baseline-perturbation-replogle-k562`. The target is completely unclaimed in `elder-plinius/V3R1T4S`.
2. **Upstream Literature Context (Ahlmann-Eltze, Huber & Anders, *Nature Methods* 2025, `doi:10.1038/s41592-025-02772-6`, `PMC12328236`):**
   - The reference benchmark (`const-ae/linear_perturbation_prediction-Paper` at pinned commit `bfa6eeea2bd145a1af2ec0127a2e808cc38456a9`) evaluated six single-cell foundation models (`scGPT`, `scBERT`, `Geneformer`, `scFoundation`, `UCE`, `CPA`), the graph neural network `GEARS`, and linear baselines (`mean`, `lpm_selftrained`, `lpm_gearsPertEmb`, `lpm_*GeneEmb`, `lpm_rpe1PertEmb`, `lpm_k562PertEmb`).
   - In the published `Panel A` benchmark on `replogle_k562_essential` (`n = 262` across `seeds = 1:2`), no model beat `lpm_selftrained` (`Mean L2 = 4.097028`, `Mean Pearson delta = 0.435544`) by a statistically meaningful margin (`gears` achieved `Mean L2 = 4.078658` [`-0.45%`] but degraded in `Mean Pearson delta` to `0.388092` [`-10.89%`]). On `replogle_rpe1_essential` (`Panel A`, `n = 413`), `lpm_selftrained` (`Mean L2 = 5.390179`, `Mean Pearson delta = 0.680388`) was the best model outright across all published methods.

---

## 2. Mathematical & Algorithmic Novelty of `hollow_loo_dual_lens`

Direct code inspection of [`claim/reproduce_baselines.py`](how-we-built-it/reproduce_baselines.py), [`claim/lens1_lens2_engine.py`](how-we-built-it/lens1_lens2_engine.py), and [`claim/certify_all_splits_and_controls.py`](how-we-built-it/certify_all_splits_and_controls.py) confirms that **Hollow Leave-One-Out Dual-Lens Kernel Regression (`hollow_loo_dual_lens`)** identifies and resolves two fundamental mathematical failure modes in the published linear baselines:

1. **Resolution of the Cis-Knockdown Smearing & Self-Prediction Diagonal Bias (`Lens 1`):**
   - **Published Baseline Bottleneck:** In `lpm_selftrained` (`run_linear_pretrained_model.R`), the $G \times |P_{\text{train}}|$ expression matrix is compressed to $K = 10$ principal components (`pca_dim = 10`) and regressed onto its own transpose $P = G_{\text{pca}}^T$ via $W = (G^T G + \lambda I)^{-1} G^T (Y - \bar{y}) P_{\text{train}}^T (P_{\text{train}} P_{\text{train}}^T + \lambda I)^{-1}$ without removing the diagonal self-knockdown entries $(i(q), q)$. In CRISPRi screens, knocking down gene $q$ directly depletes transcript $q$ ($\Delta_{q,q} \approx -b_q$). Including $\Delta_{q,q}$ inside a low-rank trans-regression simultaneously smears >80% of the direct cis-knockdown signal across all 5,000 genes and corrupts the trans singular vectors with high-leverage diagonal spikes.
   - **Novelty in `Lens 1`:** `run_ablation_variant` explicitly separates the training perturbation matrix into:
     - A **pure trans-response matrix** $Y_{\text{trans}}^{\text{train}}$ by replacing each training self-knockdown entry $(i(q), q)$ with the non-self training mean $\mu_{\text{trans}, i(q)}$ (`lines 133–150`).
     - A **6-feature cell-count-weighted ridge cis-attenuation model** $\hat{\Delta}_{\text{cis}}(g) = \operatorname{clip}(f_{\text{cis}}(b_g, b_g^2, \log(1+b_g), \mu_{\text{trans}, g}, \sigma_{\text{trans}, g}), -b_g, 0)$ fitted strictly on training perturbations whose target gene lies in the read-out set (`lines 152–180`).
     - A **de-spiked rank-20 bilinear SVD operator** equipped with an **exact Hat-Matrix Leave-One-Out (`Hollow-LOO`) transformation** (`lines 196–229`):
       $$Z_{\text{bilin, tr}}^{\text{LOO}}[:, j] = \frac{(Y_{\text{proj}} H_B)[:, j] - Y_{\text{proj}}[:, j] (H_B)_{jj}}{1 - (H_B)_{jj}}, \qquad H_B = B_{\text{tr}}^T (B_{\text{tr}} B_{\text{tr}}^T + \lambda_B I)^{-1} B_{\text{tr}}$$
       which eliminates in-sample self-prediction leverage so training predictions match the out-of-sample test distribution.

2. **Resolution of the Spectral Localization Collapse in `lpm_gearsPertEmb` (`Lens 2`):**
   - **Published Baseline Bottleneck:** In `extract_pert_embedding_from_gears.R`, the benchmark authors truncated the unnormalized weighted GO graph (`go_essential_all.csv`) to only $K = 2$ spectral eigenvectors (`svds(A, k = 2)`). On a sparse scale-free biological graph, a 2D unnormalized spectral embedding localizes on a single hub cluster and collapses to near-zero coordinates for $>95\%$ of genes, causing `lpm_gearsPertEmb` to degenerate to the uninformative training mean (`L2 = 4.193477` vs `4.193494` on K562 `Panel A`; `4.125210` on `Panel C`).
   - **Novelty in `Lens 2`:** Instead of a rank-2 unnormalized spectral truncation, `build_go_idf_features` (`lens1_lens2_engine.py` `lines 33–79`) constructs full-rank **IDF-weighted Gene Ontology cosine similarity** ($S_{\text{go, idf}}$) and **exact binary Jaccard similarity** ($S_{\text{go, jaccard}}$) matrices across all `gene2go_all.pkl` genes, and fuses them with **training-only de-spiked trans co-expression cosine and rank-32 SVD kernels** ($S_{\text{coexp, full}}$, $S_{\text{coexp, svd}}$). Multi-scale (`sharp` $k \in \{15, 20\}$, `broad` $k \in \{50, 60\}$) cell-count-reliability-weighted **Hollow-LOO neighborhood channels** ($S_{\text{hollow}}[q, q] = 0$ on `train`) are then combined with `Lens 1` via closed-form non-negative LOO ridge stacking (`w_stack_A` for in-readout perturbations, `w_stack_B` for out-of-readout perturbations, `lines 285–360`) fitted **100% on `train`**.

---

## 3. Verification of Intra-Dataset Training Constraint & Zero Cross-Cell-Line Leakage

1. **Zero Cross-Cell-Line Expression Transfer (`lpm_rpe1PertEmb` / `lpm_k562PertEmb` Exclusion):**
   - In `certify_all_splits_and_controls.py`, `pca_pert_embs["replogle_k562_essential"]` and `pca_pert_embs["replogle_rpe1_essential"]` are used **exclusively** to reproduce the paper's `Panel C` baselines `lpm_k562PertEmb` and `lpm_rpe1PertEmb` (`lines 455–456`) as required by `p3`.
   - `run_ablation_variant(..., mode="dual")` (`lines 71–361`) never receives any cross-cell-line embedding or expression data. For each dataset and each split `seed`, it accesses **only** `train_mask = splits_psce == "train"` of that single dataset (`X_mean`, `counts`) plus the static `gene2go_all.pkl` ontology annotations (`S_go_idf`, `S_go_jaccard`).
   - Despite using **zero cross-cell-line transfer**, `hollow_loo_dual_lens` achieves `Mean L2 = 3.273909` (`Mean Pearson delta = 0.608814`) on K562 `Panel C` (`n = 214`), decisively outperforming even the paper's cross-cell-line `lpm_rpe1PertEmb` (`Mean L2 = 3.543026`, `Mean Pearson delta = 0.546455`), and achieves `Mean L2 = 4.914609` (`Mean Pearson delta = 0.815232`) on RPE1 `Panel C` (`n = 224`), outperforming the cross-cell-line `lpm_k562PertEmb` (`Mean L2 = 5.147212`, `Mean Pearson delta = 0.790271`).
2. **Satisfaction of All Quantitative Win & Partial-Win Thresholds:**
   - **Full Win (`replogle_k562_essential`, `Panel A`, `n = 262`):** Mean $L_2 = \mathbf{3.320307}$ (`-18.96%` vs `lpm_selftrained` `4.097028`, `-18.59%` vs `gears` `4.078658`, `57.47x` `lpm_selftrained` across-split SD); Median $L_2 = \mathbf{3.044310}$ (`-20.00%` vs `lpm_selftrained` `3.805564`); Mean Pearson $\Delta = \mathbf{0.620623}$ (`+42.49%` vs `lpm_selftrained` `0.435544`, `7.70x` SD); Median Pearson $\Delta = \mathbf{0.644965}$ (`+51.23%`).
   - **Partial Win `p1` (`replogle_rpe1_essential`, `Panel A`, `n = 413`):** Mean $L_2 = \mathbf{4.777953}$ (`-11.36%` vs `lpm_selftrained` `5.390179`, `2.65x` SD); Median $L_2 = \mathbf{4.514809}$ (`-12.38%`, `2.48x` SD); Mean Pearson $\Delta = \mathbf{0.719286}$ (`+5.72%`).
   - **Partial Win `p2` (Functional Distance Stratification):** Monotonic concentration of gain in `Q1_closest` (`-32.33%` $L_2$ reduction on K562, Spearman $r_s = +0.345058$, $p = 9.7126 \times 10^{-9}$; `-17.39%` on RPE1, $p = 0.027768$).
   - **Partial Win `p3` (Reproduction of Record):** Exact reproduction (`0.000000` to `0.000007`) of `mean`, `lpm_selftrained`, `lpm_k562PertEmb`, and `lpm_rpe1PertEmb` across all 3 datasets, plus full 5-seed (`seeds = 1:5`) evaluation.
   - **Null Permutation Control Battery (`300` split-level runs):** Real model beats random gene-identity permutations by **$24.55\sigma$** in $L_2$ ($31.78\sigma$ in Pearson $\Delta$) on K562 and **$22.44\sigma$** in $L_2$ ($33.57\sigma$ in Pearson $\Delta$) on RPE1.

---

VERDICT: PASS
