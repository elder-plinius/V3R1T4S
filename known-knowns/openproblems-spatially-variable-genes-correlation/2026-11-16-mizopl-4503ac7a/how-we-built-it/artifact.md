# Operator Specification & Mechanistic Architecture (`artifact.md`)

## 1. Primary Frozen Operator (`object/method.py`, `sha256: 4503ac7a6e97aa6816353b486e8c87f7b64f5caeba32c6ae3f486eb6f44a7336`)

Given only raw `counts` (`N x G` CSR/dense) and 2D spatial coordinates `coords` (`N x 2` float64):

1. **Gene-Marginal Variance Stabilization (Zero `1 / L_s` Division):**
   Each gene column $y_g \in \mathbb{R}_+^N$ is mapped independently through `log1p(y_g)` and Freeman-Tukey `sqrt(y_g) + sqrt(y_g + 1) - 1`, then column-standardized to zero mean and unit $L_2$ norm (`||z_g||_2 = 1`).
2. **Six-Scale Locally Density-Adapted & `O(2)`-Invariant Spatial Bank:**
   - **Three tie-free locally density-adapted biweight kNN operators (`k_eff in {8, 20, 48}` capped at `N - 1`):** Local scale $\sigma_i = d_k(x_i)$ sets $A_{ij} = \max(0, 1 - d_{ij}^2 / (\sigma_i \sigma_j))^2$ with symmetric degree normalization $D^{-1/2} A D^{-1/2}$, removing Delaunay cavity-bridging edges (`p99 / median = 3.9565x` on `42_slide_tag_human_skin_melanoma`) and tie-order dependence whenever coordinate multiplicity satisfies $m(x) \le k_{\text{eff}} + 1$ (`max = 2` across all `50` datasets).
   - **Three `O(2)`-invariant low-rank Mercer polynomial-Gaussian operators (`alpha_bw in {0.14, 0.26, 0.50}` of RMS radius, degree `M = 6`, `28` exact monomials):** Evaluated in $O(N M G)$ BLAS matrix multiplications without forming $N \times N$ matrices; exactly invariant under 2D rotations, reflections, translations, and uniform coordinate scaling (`rel_err < 1e-12`).
3. **Underflow-Free Cliff & Ord (1981) Analytical Permutation Standardization:**
   For each spatial operator $W$ and standardized gene vector $z_g$ with sample kurtosis $b_{2,g} = N \sum_i z_{i,g}^4$, exact first and second moments under uniform spot permutation $S_N$ yield an unbounded real-valued $Z$-score, avoiding IEEE-754 binary64 `p < 1e-300` (`Z >= 37.17`) clipping ties.

## 2. Companion Capture-Deconfounded Operator (`object/ams_svg_eb_v2.py`, `sha256: 4c27e2538339e69f18061879d5418afd2a1ea1de14355b649860ae5cd097b05f`)

1. **Hilbert-Sphere Riemannian Geodesic Scale Quadrature:** Replaces equal-weight averaging and avoids ill-conditioned Kac-Murdock-Szego $R^{-1}$ boundary concentration by integrating along the centered operator curve $\tilde{W}_s / \|\tilde{W}_s\|_F$ with trapezoid arc-length weights $\Delta\theta_{s,s+1} = \arccos(R_{s,s+1})$ (`< 1e-14` duplicate-scale invariant).
2. **Scale-Separated Wiener + Deflated-Spectral Empirical-Bayes Capture Gate:** Estimates spot nuisance $\hat{\eta} = \tilde{s} - P_{\text{meso}} \tilde{s}$ from pooled standardized gene profiles above a Marchenko-Pastur-deflated copula noise floor, shrinking sub-compartment bead/channel capture dropout while preserving smooth tissue compartments (`kappa = 0.0` on intact `42_melanoma`, rising automatically to `kappa > 0.40` under `sigma_tech = 0.85` dropout).
