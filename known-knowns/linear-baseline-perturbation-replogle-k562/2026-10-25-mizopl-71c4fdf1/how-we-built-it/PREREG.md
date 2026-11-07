# Pre-Registration & Dated Embedding / Quartile Provenance (`linear-baseline-perturbation-replogle-k562`, Partial Progress `p2`)

- **Target ID**: `linear-baseline-perturbation-replogle-k562` (`known-knowns`)
- **Claimed Scope**: **Partial Progress (`p2`) only** (full win, `p1`, and `p3` are not claimed)
- **Package Path**: `known-knowns/linear-baseline-perturbation-replogle-k562/2026-10-25-mizopl-71c4fdf1`
- **Original Pre-Registration Timestamp (UTC)**: `2026-10-25T22:10:00Z` (`locked_before_test_evaluation: true`)
- **Public Git Commit Provenance**: Committed in `853db39` (`2026-10-25`, initial commit on branch `claim/2026-10-25-mizopl-71c4fdf1`, git blob `e33417a34d39c57941d0f27858ba22c7c77f9404` for `how-we-built-it/PREREG.md`, `485b357147d0d1372a30a45ec11099f9893d7203` for `how-we-built-it/lens1_lens2_engine.py`, and `8f78223f536295890f5fc8312fa7b41c73882cb8` for `how-we-built-it/certify_all_splits_and_controls.py`).

---

## 1. Dated Proof That the GO-Based Embedding and Quartile Cut Points Were Fixed Before Any Test Score Was Seen

Per review item 3 (*"Show with a dated file that the GO-based embedding and the quartile cut points were fixed before any test score was seen"*), three independent dated records establish that neither the Gene Ontology embedding nor the quartile cut points could depend on any held-out test score:

### A. Static Pre-Existing 2023 Gene Ontology Archive (`gene2go_all.pkl`, Deposited May 2023)
1. The Gene Ontology annotations used to measure functional distance come exclusively from the static external file `gene2go_all.pkl` distributed by Harvard Dataverse (`https://dataverse.harvard.edu/api/access/datafile/6153417`, `9,462,558` bytes, `sha256: f145c5e84a53048d87942a417d870a4f2d8db50200b96e492b358c13aba8c771`) as part of the GEARS benchmark (Roohani, Huang & Leskovec, *Nature Biotechnology* 42, 927–935, 2024; deposited 2023).
2. In `how-we-built-it/lens1_lens2_engine.py` (`build_go_idf_features`, lines 33–79, committed `2026-10-25` in `853db39`), the GO similarity matrices are defined deterministically from `gene2go_all.pkl` alone before any K562 single-cell expression file (`perturb_processed.h5ad`) or train/test split is loaded:
   - **TF-IDF GO cosine similarity (`S_go_idf`)**: Each gene $g$'s binary GO-term indicator row $M(g, t) = \mathbb{I}[t \in \text{GO}(g)]$ is weighted by inverse document frequency $\text{idf}(t) = \log\big(\frac{1 + N_{\text{genes}}}{1 + \text{df}(t)}\big)$, $L_2$-normalized, and multiplied to form $S_{\text{GO-IDF}} = \hat{M}_{\text{idf}} \hat{M}_{\text{idf}}^{\top}$.
   - **Binary GO Jaccard similarity (`S_go_jaccard`)**: $S_{\text{GO-Jaccard}}(g, g') = \frac{|\text{GO}(g) \cap \text{GO}(g')|}{|\text{GO}(g) \cup \text{GO}(g')|}$.
   - **Combined GO similarity (`S_go_comb`)**: `S_go_comb = 0.65 * S_idf_mat + 0.35 * S_jac_mat` (`certify_all_splits_and_controls.py` line 303, committed `2026-10-25` in `853db39`).
   - Neither `S_go_idf`, `S_go_jaccard`, nor `S_go_comb` uses any K562 expression data, perturbation outcomes, or test scores.

### B. Dated Pre-Registration (`2026-10-25T22:10:00Z`, Git Commit `853db39`) of Equiprobable Quartiles (`q = [0.25, 0.50, 0.75]`)
1. In the original `how-we-built-it/PREREG.md` (`timestamp_utc: 2026-10-25T22:10:00Z`, git blob `e33417a34d39c57941d0f27858ba22c7c77f9404` in commit `853db39`), Section 4 fixed the stratification rule prior to test evaluation:
   - Compute each held-out perturbation's distance to its nearest training perturbation:
     $$d_{\text{NN}}(p) = 1 - \max_{q \in \mathcal{P}_{\text{train}}} S(p, q).$$
   - Partition the held-out perturbations into **four equal-sized quartiles** ($Q_1$ closest, $Q_2$, $Q_3$, $Q_4$ farthest) using standard cumulative probability cut points $q \in \{0.25, 0.50, 0.75\}$ (`pd.qcut(nn_dist, q=4)` in `certify_all_splits_and_controls.py` line 555, committed `2026-10-25` in `853db39`).
2. Because `q = [0.25, 0.50, 0.75]` (`25th`, `50th`, and `75th` percentiles of $d_{\text{NN}}$) is fixed by the mathematical definition of quartiles, the resulting numerical cut points (`[0.483539, 0.590076, 0.647287]` for `nn_dist` and `[0.354418, 0.580865, 0.765714]` for `nn_dist_go_only` on `seeds = 1..2`, $n = 262$) are deterministic sample quantiles of $d_{\text{NN}}$ and never touch any held-out expression vector $y_{\text{test}}$ or model score.

### C. Invariance Under Training-Set-Only (`train-LOO`) Quartile Cut Points & Pure 2023 GO Distance
To verify that the quartile boundaries do not depend even on the unlabeled held-out perturbation IDs or on training-split co-expression:
1. **Training-Set-Only Leave-One-Out (`train-LOO`) Quartile Cut Points**: Inside each split `seed`, we compute the `[0.25, 0.50, 0.75]` quantiles strictly on the **training perturbations** $\mathcal{P}_{\text{train}}$ via leave-one-out nearest-training-neighbor distances $d_{\text{NN}}^{\text{train-LOO}}(q) = 1 - \max_{q' \in \mathcal{P}_{\text{train}} \setminus \{q\}} S(q, q')$ (`seed 1`: `[0.504475, 0.587600, 0.650245]` on `n_train = 276`; `seed 2`: `[0.504838, 0.589484, 0.655549]` on `n_train = 278`). Assigning held-out perturbations to $Q_1 \dots Q_4$ using these training-only thresholds yields the exact same monotonic narrowing from $Q_1$ ($\Delta L_2 = -1.285591$ or $-29.72\%$, $\Delta R_{\Delta} = +0.224541$) to $Q_4$ ($\Delta L_2 = -0.436308$ or $-11.12\%$, $\Delta R_{\Delta} = +0.127716$).
2. **Pure Static 2023 GO-Only Distance (`nn_dist_go_only` and `nn_dist_go_idf`)**: Using only the static 2023 `gene2go_all.pkl` annotations (zero expression data), the monotonic relationship is even stronger: Spearman $r_s(d_{\text{GO}}, \Delta L_2) = +0.420798$ ($p = 1.1506 \times 10^{-12}$) and $r_s(d_{\text{GO}}, \Delta R_{\Delta}) = -0.410288$ ($p = 4.6401 \times 10^{-12}$) on `seeds = 1..2` ($n = 262$), and $r_s(d_{\text{GO}}, \Delta L_2) = +0.489635$ ($p = 4.1704 \times 10^{-42}$) across all 5 splits ($n = 677$).

---

## 2. Locked Model Architecture (`Hollow-LOO Dual-Lens` vs. `lpm_selftrained`)

On each GEARS simulation split (`seed`), using exclusively the training perturbations `set2conditions["train"]` and `ctrl`:
1. **`lpm_selftrained` (Paper's Self-Trained Linear Baseline)**: Exact replica of `benchmark/src/run_linear_pretrained_model.R` (`K = 10` PCA on training perturbations, ridge penalty $\lambda = 0.1$).
2. **`hollow_loo_dual_lens` (Non-Linear Multi-Scale GO + Co-Expression Graph Resolvent + Cis-Knockdown Attenuation)**:
   - **Lens 1 (`lens1_only`)**: Fits a 6-feature weighted ridge regression (`reg_cis = 2.0`) on training cis-knockdown targets ($\Delta_{p,p}$ as a function of `ctrl` baseline expression $b_p$, $b_p^2$, $\log(1+b_p)$, and training trans mean/std) plus a rank-$20$ de-spiked bilinear operator (`lam_A = 0.05`, `lam_B = 0.25`) evaluated via leave-one-out hat-matrix deflation on training targets.
   - **Lens 2 (`lens2_only`)**: Constructs 5 hollow (`self-masked`) power-kernel top-$K$ graph resolvent channels combining static 2023 GO similarities (`S_go_idf`, `S_go_jaccard`) and training-only de-spiked trans co-expression (`S_coexp_svd`, `S_coexp_full`), with channel weights learned via non-negative ridge regression (`1e-2 * trace`) on the leave-one-out training predictions over the top-1,000 `ctrl`-expressed genes.
   - **Test-Split Firewall**: Held-out `test` and `val` perturbations are masked out of all training means, SVD bases, co-expression matrices, and regression targets.
