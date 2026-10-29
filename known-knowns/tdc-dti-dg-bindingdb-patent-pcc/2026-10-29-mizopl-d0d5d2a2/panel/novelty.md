# Skeptic 2 (NOVELTY) Adversarial Audit Report — `tdc-dti-dg-bindingdb-patent-pcc`

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Target ID:** `tdc-dti-dg-bindingdb-patent-pcc`
- **Submission ID:** `2026-10-29-mizopl-d0d5d2a2`
- **Audit Scope:** Live TDC `DTI_DG_Group` (`BindingDB_Patent`) leaderboard (`https://tdcommons.ai/benchmark/dti_dg_group/bindingdb_patent/`), `elder-plinius/V3R1T4S` open/closed PRs, and 2022–2026 drug-target interaction / temporal domain-generalization literature.

---

## 1. Live Leaderboard & Literature Survey

1. **Live TDC Leaderboard (`checked 2026-10-29`):**
   - Rank #1: `Otter-Knowledge-Ensemble` (Lam et al., IBM Research, *arXiv:2306.13780*) — `0.588 ± 0.002` (knowledge-graph pretraining + protein language model ensemble).
   - Rank #2: `OrangeBalls-ProtBertMorgan` (MIT) — `0.538 ± 0.008` (ProtBert PLM + Morgan fingerprint MLP).
   - Ranks #3–#9: `MMD` (`0.433 ± 0.010`), `CORAL` (`0.432 ± 0.010`), `ERM` (`0.427 ± 0.012`), `MTL` (`0.425 ± 0.010`), `GroupDRO` (`0.384 ± 0.006`), `AndMASK` (`0.288 ± 0.019`), `IRM` (`0.284 ± 0.021`).
   - Open/merged PRs on `elder-plinius/V3R1T4S` for `tdc-dti-dg-bindingdb-patent-pcc`: `0`.

2. **Literature Check (`2023–2026`):**
   - Checked follow-up DTI domain-generalization papers evaluating on TDC `BindingDB_Patent` under the official 5-seed `group.evaluate_many` protocol without external BindingDB/ChEMBL/Papyrus affinity leakage. No published leakage-free method exceeds `Otter-Knowledge-Ensemble` (`0.588 ± 0.002`) by `>= +0.010` (`>= 0.598`), and no strictly CPU-only, PLM-free method approaches `0.580 ± 0.003`.

---

## 2. Methodological Novelty of the Three-Handle Architecture

1. **Target-Centered Residual Subspace Projection (`(\mathbb{I} - \Pi_{\text{target}})y`) + RKHS Schur-Complement Leverage $\tau_t(d)$ (`Op-M1 + Op-M5`):**
   - Prior DTI-DG baselines train global regressors directly on raw affinity $y$, confounding chemical scaffold identity with historical target-mean shifts across patent years (`2014` mean `3.86` vs `2018` mean `4.90`). Projecting onto target-centered residuals before fitting per-target Multi-View Cholesky `TKRR` ($0.50 S_{\text{ECFP4}} + 0.30 S_{\text{FCFP4}} + 0.20 S_{\text{MACCS}}$) and unhashed `4,328D` Ligand CG Ridge enables a purely CPU-only, PLM-free pipeline (`Track A`) to reach **`0.580 ± 0.003`** (`+0.0420` above `OrangeBalls-ProtBertMorgan = 0.538 ± 0.008`).
2. **Slope-1 Diagonal-Offset-Invariant Catalytic Pocket Homology (`S_pocket`) & Unshrunk ESM-2 Paralog Transfer (`Op-M3`):**
   - Lifts mean maximum homology across the $49$ unseen test targets (`3,997` rows) **$3.1\times$ (`0.139 -> 0.428`)** and improves `Unseen-Target` (`p3`) PCC from `0.12204` (`ERM`) to **`0.20806 ± 0.00546`** (`Track F2`) and **`0.20932`** (`Track B`, `+70.5%` relative gain).
3. **Asymmetric Stratum Gate Inversion (`Op-M4`) & Single-Row Bayes-MMSE Excursion Equalization (`Op-M1`):**
   - Identifies and resolves the $1.39\times$ residual excursion over-dispersion on `Ex` (`Exact-Pair`, $\sigma \approx 2.25$) vs `NonEx` (`Novel-Ligand`, $\sigma \approx 1.62$) via a 100% single-row inductive Bayes-MMSE shrinkage factor $\beta_{\text{Ex}} \in \{0.72, 0.75\}$ around the training-only Bayesian target anchor $\mu_{\text{anc}, i}$, lifting 5-seed test PCC to **`0.600 ± 0.003`** (`Track F2 = 0.60018 ± 0.00266`, `Track F1 = 0.59996 ± 0.00266`).

**Overall Skeptic 2 (NOVELTY) Verdict: `PASS`**

pass: true
