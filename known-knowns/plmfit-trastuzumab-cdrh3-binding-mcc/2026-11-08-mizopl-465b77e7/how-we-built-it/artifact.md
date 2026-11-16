# How We Built It — Dual-Track Strictly Inductive Solver (`plmfit-trastuzumab-cdrh3-binding-mcc`)

## 1. Reproducible Solver Scripts in `how-we-built-it/`

Both standalone scripts use `BASE_DIR = os.path.dirname(os.path.abspath(__file__))` and accept `HERH3_DATA_PATH` pointing to `data/herH3/herH3_data_full.csv` (`sha256: 5137572eec7ce2689283854fefacd8bcd7c5cb2547d57f5ffc7c53c9fed4070f`):

1. **`how-we-built-it/bet11_dual_canonical_and_cv_learned_solver.py` (Primary Dual-Track Verifier — `Track B` & `Track A`, `L-PTCB-011`):**
   - Fits **Track B (`trackB_cv_learned`)**:
     - Computes closed-form inverse class-prevalence wild-type anchor $w_{\text{wt}} = \frac{N_{\text{neg}}}{N_{\text{pos}}}$, effective WT sample count $n_{\text{wt, eff}} = \frac{N_{\text{neg}}}{10}$, BLOSUM62 kernel bandwidth $\tau_{\text{ker}} = \text{mean}_{a<b}|B_{\text{norm}}[a,b]| = 0.2198$, and empirical-variance shrinkage $\kappa = \frac{1}{1 + \text{Var}(y_{\text{tr}})} = 0.8042$ from the `174` training rows.
     - Learns 5-estimator simplex stacking weights $w^* = [0.20, 0.30, 0.20, 0.15, 0.15]$ strictly via `10-Fold Stratified CV` on the `174` training rows by minimizing Empirical-Variance Regularized Out-Of-Fold Brier Loss $\frac{1}{N_{\text{tr}}}\|\mathbf{y}_{\text{tr}} - \mathbf{E}_{\text{OOF}} w\|_2^2 + \text{Var}(\mathbf{y}_{\text{tr}})\|w - \tfrac{1}{5}\mathbf{1}\|_2^2$.
     - Computes closed-form inverse-root-SD loop potential weights $\alpha_1 = \frac{\sigma_{\text{OOF}}(u_1)^{-1/2}}{\sigma_{\text{OOF}}(u_1)^{-1/2} + \sigma_{\text{OOF}}(u_2)^{-1/2}} \approx 0.729$, $\alpha_2 = 1 - \alpha_1 \approx 0.271$ and selects $\tau_{\text{CV}} = \text{argmax}_{\theta}\,\text{OOF\_MCC}$ via `LOTUS` `10-Fold Stratified CV` on the `174` training rows.
     - Achieves 3-seed **`Test MCC = 0.421004 +- 0.001735`** (`95% CI [0.412067, 0.430182]`), **`Test AUROC = 0.789510 +- 0.000669`**, **`Test AP = 0.624177 +- 0.000884`**, **`+0.010601` 2-body epistatic MCC gain**, and **`0.001752` inductive-to-oracle MCC gap**.
   - Fits **Track A (`trackA_canonical`, also standalone in `how-we-built-it/bet8_lotus_jensen_zero_magic_cv.py`, `L-PTCB-008`)**:
     - Freezes equal `1/5 = 0.20` portfolio weights, $n_{\text{obs}} = 1.0$, $\kappa = 1.0$, canonical parameter-free loop free energy $S_{\text{canonical}}(x) = \frac{1}{2}(\mu_\ell(x) + m_{-1}(x)) - C_{\text{pair}}(x)$, and `LOTUS` `10-Fold Stratified CV` $\tau_{\text{CV}}$.
     - Achieves 3-seed **`Test MCC = 0.408391 +- 0.000411`** (`95% CI [0.398892, 0.417982] > 0.3898`), **`Test AUROC = 0.785602 +- 0.000461`**, **`Test AP = 0.622932 +- 0.000615`**, **`+0.006512` 2-body epistatic MCC gain**, and **`0.001402` inductive-to-oracle MCC gap**.

## 2. `10-Fold Stratified CV` Out-Of-Fold Sensitivity Grid on the `174` Training Rows

| Portfolio / Ablation Configuration (`N = 174` Training Rows) | Simplex Weights $w^*$ | Loop Potential Weights $\alpha^*$ | `10-Fold CV` `OOF_AUROC` | `10-Fold CV` `OOF_MCC` | Held-Out Test `MCC` (`3` Seeds) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **`Track B` (`trackB_cv_learned`, $\lambda = \text{Var}(y_{\text{tr}}) \approx 0.2436$)** | **`[0.20, 0.30, 0.20, 0.15, 0.15]`** | **`[~0.729, ~0.271, 0.0]`** | **`0.930331`** | `0.770801` | **`0.421004 +- 0.001735`** |
| **`Track A` (`trackA_canonical`, Equal `1/5` Prior, $\lambda \to \infty$)** | **`[0.20, 0.20, 0.20, 0.20, 0.20]`** | **`[0.50, 0.50, 0.0]`** | `0.924590` | **`0.778202`** | **`0.408391 +- 0.000411`** |
| **`Track B` 1-Body Position-Wise Ablation (`p3`)** | `[0.20, 0.30, 0.20, 0.15, 0.15]` | `[~0.729, ~0.271, 0.0]` | `0.925412` | `0.765118` | `0.410402 +- 0.001592` |
| **`Track A` 1-Body Position-Wise Ablation (`p3`)** | `[0.20, 0.20, 0.20, 0.20, 0.20]` | `[0.50, 0.50, 0.0]` | `0.919844` | `0.771045` | `0.401879 +- 0.000887` |
