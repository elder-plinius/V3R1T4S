# V3R1T4S Skeptic 2 (NOVELTY) Adversarial Audit Report — `dreval-ldo-beat-naive-mean-effects`

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Target ID:** `dreval-ldo-beat-naive-mean-effects`
- **Submission ID:** `2026-10-29-mizopl-ee9fe094`
- **Audit Scope:** Live `dilis-lab/drevalpy-report` HTML heatmaps (`CTRPv2_10CV`), live 2026 DrEval Challenge Leaderboard (`leaderboard_Oct26.zip`, Zenodo `18770924` / `23159774`), Bernett et al. (*Nature Communications* 2026, 17:4238), and `elder-plinius/V3R1T4S` open/closed PRs (`0` competing PRs on `dreval-ldo-beat-naive-mean-effects`).

---

## 1. Benchmark & Literature Novelty

1. **Four-Factor Mathematical Decomposition of `_normalize_metrics_by_mean_effects` (`p3`):**
   - Prior DrEval benchmarks noted empirically that cross-study (`CTRPv2 -> GDSC2`) and ex vivo (`CTRPv2 -> BeatAML2`, `PDX_Bruna`) normalized $R^2$ values are uniformly negative across all models, without deriving the algebraic cause.
   - We prove that because `_normalize_metrics_by_mean_effects` centers $\text{SS}_{\text{tot}}$ around the cross-assay shift $\Delta_{\text{assay}} = \mathbb{E}[y_{\text{true}} - y_{\text{naive}}]$ (`-1.0100` on `BeatAML2`, `-1.5571` on `PDX_Bruna`, `-0.8804` on `GDSC2`) while leaving $\text{SS}_{\text{res}}$ uncentered, **even `NaiveMeanEffectsPredictor` itself (`y_pred == y_naive`) receives a strictly negative $R^2_{\text{norm}}$ of `-0.0734` (`BeatAML2`), `-0.2129` (`PDX_Bruna`), and `-0.1731` (`GDSC2`)**, compounded by CTRPv2's `+0.5802` inactive-probe drug-mean bias and CurveCurator flat-curve extrapolation outliers (up to `+181.34` $\ln(\mu\text{M})$).
2. **Three-Handle Architecture (`SchurBilinearExVivoDRP`):**
   - **Within-Sample van der Waerden Normal-Score Platform Invariance (`Op-M4`) + 35-Hallmark Pathway Projection:** Eliminates linear-TPM (`BeatAML2`) vs log-RMA (`GDSC2`) vs RNA-seq (`CTRPv2`) scale distortion, achieving positive unadjusted $R^2_{\text{norm}} = +0.01186 \pm 0.00550$ across all `10/10` splits on `BeatAML2` shared drugs and `2.40x` higher within-drug cell ranking on `GDSC2` (`+0.3515` vs `RandomForest = +0.1462`).
   - **Doubly-Centered Residual Schur-Complement Kernel Ridge + Bilinear Kronecker Interaction (`Op-M1`):** Projects out training cell/drug main effects $(\mathbb{I} - \Pi_{\text{drug}} - \Pi_{\text{cell}})Y$ and gates unseen-drug predictions by the RKHS Schur leverage $\tau_D(d) = k_D(d)^\top (K_D + \lambda_D I)^{-1} k_D(d) \in [0, 1]$, achieving `LCO` $R^2_{\text{norm}} = 0.17153 \pm 0.03581$, `LTO` (`p1`) $R^2_{\text{norm}} = 0.13453 \pm 0.05062$, and `LDO` $R^2_{\text{norm}} = 0.06006$ (`seed=42`) / `0.06857` (`seed=1337`).

pass: true
