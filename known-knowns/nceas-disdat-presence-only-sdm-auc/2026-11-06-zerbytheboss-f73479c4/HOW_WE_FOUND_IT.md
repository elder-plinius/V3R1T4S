# How We Found It

contributor text, unverified

By Fithian et al. (2015) and Phillips et al. (2009), presence-only occurrence records follow a thinned inhomogeneous Poisson point process with intensity $\lambda_s(x) \cdot b_g(x)$, where $b_g(x)$ is the observer sampling bias of biological target group $g$. Normalizing model log-intensities exclusively across the deduplicated target-group presence cells (`log_softmax(dim=0)`) cancels $b_g(x)$ in the conditional likelihood denominator, whereas uniform random background (`train_bg.rds`) conflates road/access bias with habitat preference on sparsely surveyed regions (`CAN` and `NSW`).

We constructed a four-component Target-Group Hybrid Poisson Point-Process ensemble (`how-we-built-it/solve_disdat_sdm.py`):
1. **Target-Group Spatial-Softmax Residual MLP (`deepmaxent_tgb`)**: A 3-seed Residual MLP trained on deduplicated biological target-group cells (`NSW` grouped into `bats`, `birds`, `reptiles`, `plants`) with batch-level spatial `log_softmax(dim=0)` cross-entropy loss.
2. **Multi-Scale Damped Newton-IRLS Maxent (`newton_bio_cell`, `newton_bio_rec`, `newton_reg_site`)**: Exact second-order damped Newton-IRLS solvers over degree-2 polynomial, cubic B-spline, normal-score quantile, and hinge basis functions (`-1, 0, +1` $\sigma$ knots) evaluated against deduplicated biological target-group cells, biological target-group records, and regional deduplicated presence cells.
3. **Empirical-Bayes Guild Shrinkage**: Shrinks rare-species environmental log-intensities toward the squared-cosine-weighted guild prior across co-occurring species in the same target group with shrinkage weight $\lambda_{\text{EB}} = 4.5 / (N_{\text{pos}} + 15)$.
4. **Target-Group Spatial Kernel Intensity Ratio (`sp_kde_bio`)**: Multi-bandwidth (`0.18, 0.35, 0.70` $\sigma$) Gaussian kernel log-intensity ratio between species presence locations and biological target-group effort locations.
