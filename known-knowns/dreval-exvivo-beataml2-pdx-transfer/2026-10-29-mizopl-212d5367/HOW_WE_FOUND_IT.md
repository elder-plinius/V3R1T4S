# How We Found It (`contributor text, unverified`): The Geometry of Differential Drug Sensitivity & Cross-Assay Transfer in DrEval (`dreval-exvivo-beataml2-pdx-transfer`)

> **Note:** This file is contributor text, unverified by the mechanical gate (`check_run.py` verifies `object/certificate.json`, `object/preregistration_lock.json`, and all per-split CSVs in `object/` via `verify-it-yourself/run_checks.sh`).

## 1. Why Standard Models Collapse on DrEval Normalized Metrics

In DrEval (Bernett et al., *Nature Communications* 2026), every prediction $\hat{y}_{c,d}$ is evaluated after subtracting the additive `NaiveMeanEffectsPredictor` baseline:
$$y_{c,d}^{\text{naive}} = \mu_0 + \alpha_c + \beta_d, \qquad R^2_{\text{norm}} = 1 - \frac{\sum_{c,d} (y_{c,d} - \hat{y}_{c,d})^2}{\sum_{c,d} \bigl((y_{c,d} - y_{c,d}^{\text{naive}}) - \overline{y - y^{\text{naive}}}\bigr)^2}.$$

Our diagnostic audit (`stage1_inspect_and_verify_metrics.py` and `stage3_p3_gap_decomposition.py`) uncovered four interacting structural traps that explain the entire behavior of the DrEval benchmark across `LCO`, `LTO`, `LDO`, `GDSC2`, `BeatAML2`, and `PDX_Bruna`:

1. **Main-Effect Variance Swamping in Global Regressors (`LCO` / `LTO` / `LDO`):**
   - In `CTRPv2`, drug main effects $\beta_d$ account for `~74%` of total $\ln(\text{IC}_{50})$ variance, while differential cell-by-drug sensitivity $R_{c,d} = y_{c,d} - y_{c,d}^{\text{naive}}$ accounts for `< 20%`. Standard tree/neural regressors trained on raw $y_{c,d}$ spend their split/weight capacity re-approximating $\beta_d$ with noise, yielding negative $R^2_{\text{norm}}$ (`-1.58` to `-1.62` in default `drevalpy 1.6.0` grids).
   - **Exact Fix (`Op-M1` Doubly-Centered Residual Projection):** Project out training cell and drug main effects *before* fitting: $R = (\mathbb{I} - \Pi_{\text{drug}} - \Pi_{\text{cell}})Y$, and fit a Multi-Scale Cosine Expression Kernel + 35-Hallmark Pathway Kernel + Low-Rank Bilinear Kronecker interaction strictly on $R$.
2. **RKHS Schur-Complement Leverage Gate for Unseen Drugs (`LDO`):**
   - For an unseen test drug $d^*$, chemical similarity $k_D(d^*)$ to training drugs has varying epistemic support. Weighting the transferred drug effect and residual profile by the RKHS Schur leverage $\tau_D(d^*) = k_D(d^*)^\top (K_D + \lambda_D I)^{-1} k_D(d^*) \in [0, 1]$ prevents wild extrapolation on low-similarity scaffolds (`s_max <= 0.50`) while preserving signal on `s_max <= 0.85` (`R2_norm = +0.06012` / `+0.06843`) and `s_max <= 0.70` (`R2_norm = +0.04113` / `+0.05700`).
3. **Uncentered-Numerator Assay-Offset Penalty in `_normalize_metrics_by_mean_effects` (`p3`):**
   - In cross-study (`GDSC2`) and ex vivo (`BeatAML2`, `PDX_Bruna`) transfer, `NaiveMeanEffectsPredictor` predicts the source `CTRPv2` mean while the target assay is shifted by $\Delta_{\text{assay}} = \mathbb{E}[y_{\text{true}} - y_{\text{naive}}]$ (`-1.0100` on `BeatAML2`, `-1.5571` on `PDX_Bruna`, `-0.8804` on `GDSC2`). Because `_normalize_metrics_by_mean_effects` centers $\text{SS}_{\text{tot}}$ by $\Delta_{\text{assay}}$ (`np.var(y_true - y_naive)`) but leaves $\text{SS}_{\text{res}}$ uncentered, **even `NaiveMeanEffectsPredictor` itself gets negative $R^2_{\text{norm}}$ (`-0.0734`, `-0.2129`, `-0.1731`)**.
4. **Within-Sample van der Waerden Normal-Score Alignment (`Op-M4`):**
   - `BeatAML2` ship RNA-seq on a linear TPM scale (`[0, 13448]`), `GDSC2` on log-microarray (`[2.05, 13.72]`), and `CTRPv2` on $\log_2(\text{TPM}+1)$. Mapping each sample's expression ranks over the $G_{\text{shared}} = 908$ core genes to exact normal quantiles $\Phi^{-1}\bigl((r_{c,g} - 0.5)/G_{\text{shared}}\bigr)$ is 100% single-row inductive and invariant to any monotone platform transformation, yielding **positive unadjusted $R^2_{\text{norm}} = +0.01186 \pm 0.00550$ across all 10 splits on `BeatAML2` shared drugs** and **`2.40x` higher within-drug cell ranking (`+0.3515` vs `+0.1462`) on `GDSC2`**.
