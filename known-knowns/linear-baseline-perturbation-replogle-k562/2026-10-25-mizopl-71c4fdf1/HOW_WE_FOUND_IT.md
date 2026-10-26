# How We Found It (`linear-baseline-perturbation-replogle-k562`)

## 1. Diagnosing the Linear Baseline Bottleneck in `run_linear_pretrained_model.R`

When we inspected the reference R scripts at `const-ae/linear_perturbation_prediction-Paper` (`commit bfa6eeea2bd145a1af2ec0127a2e808cc38456a9`), we reproduced `mean`, `lpm_selftrained`, `lpm_k562PertEmb`, and `lpm_rpe1PertEmb` to `0.000000–0.000007` across all three datasets (`how-we-built-it/reproduce_baselines.py`) and uncovered why `lpm_selftrained` and `lpm_gearsPertEmb` fail to beat the training mean by more than `2.3%`:

1. **Cis-Knockdown Diagonal Smearing (`Lens 1` Bottleneck):**
   - In CRISPRi Perturb-seq screens (`replogle_k562_essential`, `replogle_rpe1_essential`, `adamson`), knocking down target gene $q$ directly depletes transcript $q$ at row $i(q)$ ($\Delta_{q,q} \approx -b_q$).
   - `lpm_selftrained` takes a rank-10 PCA of the raw training matrix (`including` the huge negative diagonal self-knockdown spikes) and fits $Y_{\text{train}} - \bar{y} \approx G W G_{\text{train}}^T$. Because rank-10 PCA cannot isolate diagonal spikes, it simultaneously (a) loses $>80\%$ of the direct cis-knockdown amplitude on target gene $q$ and (b) corrupts the trans-regulatory singular vectors with high-leverage diagonal outliers.
2. **Spectral Localization Collapse in `lpm_gearsPertEmb` (`Lens 2` Bottleneck):**
   - In `extract_pert_embedding_from_gears.R`, the authors extracted only $K = 2$ spectral eigenvectors (`svds(A, k = 2)`) from the unnormalized weighted GO graph (`go_essential_all.csv`). On a scale-free graph of $19{,}264$ genes, the top 2 unnormalized eigenvectors localize on a single high-degree hub cluster, assigning near-zero coordinates to $>95\%$ of perturbed genes (`lpm_gearsPertEmb` collapses to `4.193477` vs `mean = 4.193494` on K562 `Panel A`).

---

## 2. Closed-Form Solution: Hollow-LOO Dual-Lens Kernel Regression

Implemented in [`how-we-built-it/certify_all_splits_and_controls.py`](how-we-built-it/certify_all_splits_and_controls.py) and [`how-we-built-it/lens1_lens2_engine.py`](how-we-built-it/lens1_lens2_engine.py):

1. **Lens 1 (De-Spiked Trans SVD + 6-Feature Cis-Attenuation + Hat-Matrix Hollow-LOO):**
   - Replaces each training self-knockdown entry $(i(q), q)$ with the non-self training mean $\mu_{\text{trans}, i(q)}$ before extracting a rank-20 trans SVD operator equipped with exact Hat-Matrix Leave-One-Out (`Hollow-LOO`) de-biasing, and predicts direct target-gene cis-depletion via a 6-feature cell-count-weighted ridge regression fitted strictly on `train`.
2. **Lens 2 (Full-Rank IDF + Jaccard GO Kernel + Training Co-Expression SVD + Multi-Scale Hollow-LOO Stacking):**
   - Replaces the collapsed 2D spectral embedding with full-rank IDF-weighted cosine similarity ($S_{\text{go, idf}}$) and binary Jaccard similarity ($S_{\text{go, jaccard}}$) across `gene2go_all.pkl`, fused with training-only de-spiked trans co-expression cosine and rank-32 SVD kernels ($S_{\text{coexp, full}}$, $S_{\text{coexp, svd}}$).
   - Evaluates multi-scale (`sharp` $k \in \{15, 20\}$, `broad` $k \in \{50, 60\}$) cell-count-reliability-weighted Hollow-LOO neighborhood channels ($S_{\text{hollow}}[q, q] = 0$ on `train`) and combines them with Lens 1 via closed-form non-negative LOO ridge stacking fitted 100% on `train`.

---

## 3. Compute & Discovery Time (`we*` Single-Thread Architecture)

Executed on 1 thread of [`we*`](https://github.com/mizopl/we-star) on a 16 GB Apple M1 laptop (CPU-only):
- **Wall-Clock Discovery Time (1 `we*` thread):** `27 min` (`23:03 -> 23:30`) to first win (`-18.96%` K562 $L_2$, `-11.36%` RPE1 $L_2$); `36 min` (`23:03 -> 23:39`) to complete 5-seed + `p1/p2/p3` + 300-permutation certification.
- **Single-Core CPU Compute Time:** `7.62 s` GO graph construction + `24.08 s` K562 5-seed & ablation suite + `38.55 s` RPE1 5-seed & ablation suite + `1.99 s` Adamson 5-seed & ablation suite = **`72.24 s` (`1.20 min`)** across all 3 datasets and 5 seeds (`493.51 s` / `8.23 min` including all `300` null permutation evaluations).
