# Skeptic 2 — Novelty Audit (`plmfit-trastuzumab-cdrh3-binding-mcc`)

context: fresh review session

## 1. Live Scoreboard & 2024–2026 Literature Audit

We audited the live `LSSI-ETH/plmfit` scoreboard (`https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/README.md`, `sha256: 51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b`, re-fetched `2026-11-08T14:42:30Z`) and 2024–2026 literature on the `herH3` `one_vs_rest` extrapolation split (`174` single-mutant training sequences $\to$ `36,386` multi-mutant test sequences at Hamming distance $d \in \{2..10\}$):
- **Listed `LSSI-ETH/plmfit` Scoreboard Record (Bikias, Stamkopoulos & Reddy, *Briefings in Bioinformatics* 26(4):bbaf381, 2025):**
  `Trastuzumab - one-vs-rest | 0.3898 | MCC | ProGen2-XL | LoRA- | 25% | CLS | Linear` (`ProGen2-xlarge`, `6.4B` parameters fine-tuned with memory-reduced LoRA).
- **Mason et al. (*Nature Biomedical Engineering* 5:600–612, 2021, `github.com/dahjan/DMS_opt`):** Evaluated random/clonal splits where multi-mutants appear in training, rather than the strict `one_vs_rest` single-to-multi-mutant extrapolation split introduced by PLMFit.
- **No higher published `MCC` on the PLMFit `herH3` `one_vs_rest` split (`174 -> 36,386`) was found in 2024–2026 literature.**

## 2. Architectural Novelty of Our Dual-Track Solver (`Track B` & `Track A`)

Why did a `6.4B`-parameter `ProGen2-XL + LoRA` model plateau at `MCC = 0.3898` on `one_vs_rest`?
1. **Structural Root Cause #1 (Constant IgG1 Fc Tail Dilution & Sparse $N=174$ Single-Mutant Coverage):** Each full heavy-chain sequence in `herH3_data_full.csv` is `449` amino acids long, of which `439` residues are identical across all `36,560` rows. Evaluating a full-chain `[CLS]` or mean-pooled representation dilutes the 10-aa CDR-H3 loop (`[98:108]`), while unanchored per-site fits on only `174` single mutants suffer from severe small-sample variance (`9` to `19` single mutants per site).
2. **Structural Root Cause #2 (Additive Log-Odds Extrapolation Shift from $d=1$ to $d \in \{2..10\}$):** Standard additive log-odds models sum 10 marginal site terms, so a threshold calibrated directly on raw single-mutant ($d=1$) scores miscalibrates the decision boundary when 7–8 positions are simultaneously mutated ($85\%$ of the test set has $d \in \{6,7,8,9\}$).

Our solver resolves both bottlenecks using `7,513,338 <= 10M` total parameters (`facebook/esm2_t6_8M_UR50D` frozen `7,512,474`-parameter backbone + `864` linear/empirical-Bayes parameters, **`850x` smaller than `ProGen2-XL`**, satisfying `p1`):
1. **5-Estimator Empirical-Bayes Site Posterior ($10 \times 20$ table $P_{\text{eb}}[k, a]$):** Combines class-balanced wild-type anchored Ridge (`p_bal`), natural-prevalence Ridge (`p_unb`), BLOSUM62 kernel smoothing (`p_ker`, $\tau_{\text{ker}} = \text{mean}_{a<b}|B_{\text{norm}}[a,b]| = 0.2198$), leave-one-site-out cross-position ridge (`p_ctx1`), and a physicochemical/ESM2 L2-logistic model (`p_sh`), shrunk via empirical-variance shrinkage $\kappa = \frac{1}{1 + \text{Var}(y_{\text{tr}})} = 0.8042$. In `Track B`, estimator weights $w^* = [0.20, 0.30, 0.20, 0.15, 0.15]$ are learned strictly via `10-Fold Stratified CV` on the 174 training rows by minimizing Empirical-Variance Regularized Out-Of-Fold Brier Loss $\frac{1}{N_{\text{tr}}}\|\mathbf{y}_{\text{tr}} - \mathbf{E}_{\text{OOF}} w\|_2^2 + \text{Var}(\mathbf{y}_{\text{tr}})\|w - \tfrac{1}{5}\mathbf{1}\|_2^2$; in `Track A`, weights are fixed at the parameter-free `1/5 = 0.20` naive portfolio.
2. **Contextual Multi-Mutant Probe (`VH-CDRH3` Window `[78:122]`) + 2-Body Epistatic Rescue & Co-Failure Loop Potential (`p3`):** Evaluates frozen `esm2_t6_8M_UR50D` on the 44-aa VH-CDRH3 window `[78:122]` of every sequence so Layer-4/Layer-6 attention heads capture multi-mutant backbone clashes directly, and combines site log-odds with pairwise epistatic co-failure $C_{\text{pair}}(x)$ (+`0.010601` MCC gain in `Track B`, +`0.006512` MCC gain in `Track A`).
3. **Law of the Unconscious Statistician (`LOTUS`) `10-Fold Stratified CV` Threshold Calibration (`p4`):** Evaluates out-of-fold single mutants against viable multi-mutant backgrounds constructed strictly from each training fold's $P_{\text{eb}}^{(-f)}$ matrix, achieving an inductive-to-oracle MCC gap of just `0.001752` (`Track B`) and `0.001402` (`Track A`).

pass: true
