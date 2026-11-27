# How We Found It (`HOW_WE_FOUND_IT.md` — contributor text, unverified)

> **Note (`contributor text, unverified`)**: This document records the engineering notes behind our Partial Progress `p2` stratification on `linear-baseline-perturbation-replogle-k562`. For standalone verification of the saved per-perturbation K562 predictions and distances, run `sh verify-it-yourself/run_checks.sh`.

---

## 1. Decomposing the Linear Baseline (`lpm_selftrained`) on Replogle K562

In Ahlmann-Eltze, Huber & Anders (*Nature Methods* 22, 1657–1661, 2025; `const-ae/linear_perturbation_prediction-Paper`, commit `bfa6eeea2bd145a1af2ec0127a2e808cc38456a9`), the self-trained linear baseline (`lpm_selftrained`, implemented in `benchmark/src/run_linear_pretrained_model.R`) computes:
1. Condition-level pseudobulk averages across single cells for each CRISPRi perturbation condition $p$ and unperturbed control `ctrl`.
2. Training-set change matrix $Y_{\text{train}} = X_{\text{train}} - x_{\text{ctrl}}\mathbf{1}^{\top}$.
3. Top $K = 10$ principal components (`irlba::prcomp_irlba(train_X, n = 10)`) over the read-out genes, using $G = U_{10} \Sigma_{10}$ as both the gene embedding and (for perturbations whose target gene is among the read-out genes) the perturbation embedding $P = G^{\top}$.
4. Ridge regression ($\lambda = 0.1$):
   $$\hat{Y}_{\text{test}} = x_{\text{ctrl}}\mathbf{1}^{\top} + \mu_{\text{train}}\mathbf{1}^{\top} + G\,(G^{\top}G + \lambda I)^{-1} G^{\top}(Y_{\text{train}} - \mu_{\text{train}}\mathbf{1}^{\top}) P_{\text{train}}^{\top}(P_{\text{train}}P_{\text{train}}^{\top} + \lambda I)^{-1} P_{\text{test}}.$$

When we inspected the training matrix $Y_{\text{train}}$ and the perturbation geometry on `replogle_k562_essential`, two structural properties stood out:
1. **Diagonal Cis-Knockdown Impulse vs. Trans Co-Regulation (`Lens 1`)**: In CRISPRi, knocking down target gene $p$ produces a direct cis-attenuation spike $\Delta_{p,p} \ll 0$ on the diagonal entry $g = p$ whose magnitude scales with the baseline `ctrl` expression $b_p = x_{\text{ctrl}}(p)$. Because `lpm_selftrained` leaves the diagonal cis spikes inside $Y_{\text{train}}$ before computing its rank-10 PCA subspace and bilinear fit, the singular vectors and bilinear weights are distorted by diagonal variance, while failing to apply the direct cis-knockdown attenuation law on held-out perturbations $p^*$ whose target gene lies in the read-out panel.
2. **Multi-Scale Functional Neighborhood Propagation (`Lens 2`)**: In `lpm_selftrained`, replacing $P$ by a 2-dimensional spectral embedding of the GEARS GO graph (`lpm_gearsPertEmb`, $d = 2$) collapses nearly to the training mean because 2 dimensions discard almost all pathway and complex structure. By contrast, constructing a hollow (`leave-one-out` on training targets) multi-scale kernel resolvent from the static 2023 GEARS Gene Ontology dictionary (`gene2go_all.pkl`, TF-IDF cosine `S_go_idf` + Jaccard `S_go_jaccard`) and de-spiked training-split trans co-expression (`S_coexp_svd`, `S_coexp_full`), with channel weights learned via leave-one-out cross-validation on the training split, transfers multi-pathway regulatory responses across functionally related perturbations.

---

## 2. Answering Target `p2`: Functional-Distance Stratification (`Q1` Closest vs. `Q4` Farthest)

Target `p2` asks us to stratify held-out perturbations by functional distance from the training set and test whether the performance gap between linear and non-linear models widens for out-of-distribution (OOD) perturbations.

Using both the pre-registered hybrid GO + training co-expression distance $d_{\text{NN}}(p) = 1 - \max_{q \in \mathcal{P}_{\text{train}}} S_{\text{hyb}}(p, q)$ and the pure static 2023 `gene2go_all.pkl` Gene Ontology distance $d_{\text{GO}}(p) = 1 - \max_{q \in \mathcal{P}_{\text{train}}} S_{\text{GO}}(p, q)$ (which uses zero expression data of any kind), we partitioned held-out K562 perturbations into four quartiles ($Q_1$ closest to $Q_4$ farthest, under both equiprobable `q = [0.25, 0.50, 0.75]` quantiles and training-set-only `train-LOO` quantile thresholds):
- In **$Q_1$ (`Q1_closest`, in-distribution functional neighborhoods)**, perturbations share dense Gene Ontology / complex neighborhoods with training perturbations, allowing the non-linear graph resolvent (`Lens 2`) to achieve its largest advantage over `lpm_selftrained`: $\Delta L_2 = -1.404930$ (**$-32.33\%$**) and $\Delta R_{\Delta} = +0.224525$ on hybrid distance ($\Delta L_2 = -1.267239$ or **$-27.68\%$**, $\Delta R_{\Delta} = +0.264148$ on static 2023 GO distance).
- As functional distance increases from $Q_1 \to Q_2 \to Q_3 \to Q_4$ (**`Q4_farthest`, most out-of-distribution perturbations**), the graph resolvent's neighborhood similarity weights decay and smoothly fall back toward the shrinkage bilinear + direct cis-attenuation channel (`Lens 1`), so the gap **narrows monotonically** rather than widening: in $Q_4$, $\Delta L_2 = -0.404255$ (**$-10.40\%$**) and $\Delta R_{\Delta} = +0.123755$ on hybrid distance ($\Delta L_2 = -0.331111$ or **$-8.94\%$**, $\Delta R_{\Delta} = +0.107679$ on static 2023 GO distance; Spearman $r_s(d_{\text{GO}}, \Delta L_2) = +0.420798, p = 1.1506 \times 10^{-12}$ on `seeds = 1..2` $n = 262$, and $r_s(d_{\text{GO}}, \Delta L_2) = +0.489635, p = 4.1704 \times 10^{-42}$ across `seeds = 1..5` $n = 677$).
