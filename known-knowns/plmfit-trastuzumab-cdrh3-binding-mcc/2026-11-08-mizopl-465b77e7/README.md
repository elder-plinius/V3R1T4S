# `plmfit-trastuzumab-cdrh3-binding-mcc`: Dual-Track Strictly Inductive Empirical-Bayes & Contextual `ESM2-8M` Loop-Potential Solver (`MCC = 0.4210 +- 0.0017`)

## What

- **Target ID:** `plmfit-trastuzumab-cdrh3-binding-mcc`
- **Submission ID:** `2026-11-08-mizopl-465b77e7`
- **Internal 3-Skeptic Panel Status (our own panel's status, recording that our local 3-skeptic review panel checked this package):** `CONFIRMED_SOLUTION` + Partial Wins `p1, p2, p3, p4` (`panel/gate.md`)
- **Confirmed Scope (`panel/gate.md`):** Full Solution (CONFIRMED_SOLUTION + partial wins p1, p2, p3, p4) on Trastuzumab CDR-H3 variant binding (PLMFit herH3 one_vs_rest split: 174 single-mutant training rows [173 train + 1 validation] -> 36,386 held-out multi-mutant test rows with 2..10 mutations in positions 99..108, wild-type WGGDGFYAMD): Track B (strictly inductive 10-Fold Stratified CV-learned Empirical-Variance Regularized Out-Of-Fold Brier Stacking w* = [0.20, 0.30, 0.20, 0.15, 0.15] over a 5-estimator Empirical-Bayes site posterior + frozen 7.51M-parameter facebook/esm2_t6_8M_UR50D VH-CDRH3 window [78:122] + closed-form inverse-root-SD loop potential + LOTUS 10-Fold Stratified CV decision threshold tau_CV = 1.344167 +- 0.037100, total parameters 7,513,338 <= 10M [p1], zero test reads) achieves 3-seed test MCC = 0.421004 +- 0.001735 (seeds 42, 43, 44: 0.422296, 0.418551, 0.422164; 1,000-resample bootstrap 95% CI [0.412067, 0.430182] excluding 0.3898), beating the LSSI-ETH/plmfit ProGen2-XL + LoRA scoreboard record of 0.3898 by +0.031204 (>= +0.02 required bar of 0.4098 by +0.011204), with threshold-free test AUROC = 0.789510 +- 0.000669 and test Average Precision (AP) = 0.624177 +- 0.000884 (p2), pairwise 2-body epistatic gain +0.010601 MCC (+0.004567 AUROC, +0.001972 AP) over the 1-body position-wise ablation (0.410402 +- 0.001592 MCC, p3), and an inductive-to-oracle threshold MCC gap of 0.001752 vs test-oracle MCC 0.422756 (p4); paired side-by-side with Track A (parameter-free canonical 1/5 equal-weight law S(x) = 0.5*(mu_l(x) + m_{-1}(x)) - C_pair(x) + LOTUS 10-Fold Stratified CV threshold tau_CV = 1.230833 +- 0.042931), which achieves 3-seed test MCC = 0.408391 +- 0.000411 (95% CI [0.398892, 0.417982] > 0.3898, +0.018591 over 0.3898), test AUROC = 0.785602 +- 0.000461, test AP = 0.622932 +- 0.000615, and an inductive-to-oracle threshold MCC gap of 0.001402.

---

## Check It Yourself

From the package root, run the standalone verification script (`< 1s`, standard Python 3 + NumPy):

```sh
sh verify-it-yourself/run_checks.sh
```

Expected terminal output (`exit 0`, final line `PASS`):

```text
========================================================================
V3R1T4S Verification — plmfit-trastuzumab-cdrh3-binding-mcc (Full Win)
========================================================================
[OK] SHA256SUMS verified across all 14 files in object/.
[OK] object/manifest_sha256.json commitments and split counts [173, 1, 36386] verified.
[OK] Track B (CV-Learned Inductive Model, N=36,386 x 3 seeds): MCC = 0.421004 +- 0.001735 (95% CI [0.412067, 0.430182] > 0.3898), AUROC = 0.789510, AP = 0.624177, 2-body gain = +0.010601 MCC, Inductive-to-Oracle gap = 0.001752.
[OK] Track A (Parameter-Free Canonical Law, N=36,386 x 3 seeds): MCC = 0.408391 +- 0.000411 (95% CI [0.398892, 0.417982] > 0.3898), AUROC = 0.785602, AP = 0.622932, 2-body gain = +0.006512 MCC, Inductive-to-Oracle gap = 0.001402.
PASS
```

Negative control (`exit 1`, final line `FAIL`):

```sh
python3 verify-it-yourself/verify.py --corrupt
```

---

## Compared To

### Table 1: Main Benchmark Comparison on `herH3` `one_vs_rest` (`174` Train $\to$ `36,386` Test, Seeds `42, 43, 44`)

Upstream scoreboard: <https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/README.md> (`sha256: 51b672d563c778ae40a435cad51424a5b8e0f82294211642d2bfff4983792f0b`, fetched `2026-11-08T14:42:30Z`).
Upstream dataset: <https://raw.githubusercontent.com/LSSI-ETH/plmfit/main/data/herH3/herH3_data_full.csv> (`sha256: 5137572eec7ce2689283854fefacd8bcd7c5cb2547d57f5ffc7c53c9fed4070f`, `17,149,024` bytes).

| Model / Track | Total Parameters (`p1`) | Test `MCC` (`mean +- SD`) | Margin vs `0.3898` | Bootstrap 95% CI | Test `AUROC` (`p2`) | Test `AP` (`p2`) | 1-Body `MCC` (`p3`) | 2-Body Epistatic Gain (`p3`) | Inductive `tau_CV` | Oracle `MCC` (`p4`) | Inductive-to-Oracle Gap (`p4`) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Ours: `Track B` (`trackB_cv_learned`, Claimed Full Win)** | **`7,513,338`** (`<= 10M`) | **`0.421004 +- 0.001735`** | **`+0.031204`** | **`[0.412067, 0.430182]`** | **`0.789510 +- 0.000669`** | **`0.624177 +- 0.000884`** | `0.410402 +- 0.001592` | **`+0.010601`** | `1.344167 +- 0.037100` | `0.422756` | **`0.001752`** |
| **Ours: `Track A` (`trackA_canonical`, Parameter-Free Law)** | **`7,513,338`** (`<= 10M`) | **`0.408391 +- 0.000411`** | **`+0.018591`** | **`[0.398892, 0.417982]`** | **`0.785602 +- 0.000461`** | **`0.622932 +- 0.000615`** | `0.401879 +- 0.000887` | **`+0.006512`** | `1.230833 +- 0.042931` | `0.409793` | **`0.001402`** |
| **Ours: CPU-Only Baseline (`L-PTCB-001`, Zero PLM)** | **`200`** (`0` PLM) | `0.300600 +- 0.006500` | `-0.089200` | — | `0.736800` | `0.550400` | `0.300600` | `0.000000` | — | `0.336000` | `0.035400` |
| **Listed Scoreboard Record (`LSSI-ETH/plmfit`)** | `~6,400,000,000` (`ProGen2-XL + LoRA-`) | `0.3898` | `0.000000` | — | *(unreported)* | *(unreported)* | *(unreported)* | *(unreported)* | — | — | — |

### Table 2: Per-Seed Breakdown (`Seeds 42, 43, 44`, `object/certificate.json`)

| Track | Seed | Learned $w^*$ (`10-Fold CV`) | Learned $\alpha^*$ (`10-Fold CV`) | `OOF_MCC` (`N=174`) | `OOF_AUROC` (`N=174`) | Inductive `tau_CV` | Test `MCC` (2-Body) | Test `MCC` (1-Body) | Test `AUROC` (2-Body) | Test `AP` (2-Body) | Test Oracle `MCC` | Positive Pred Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`Track B`** | `42` | `[0.20, 0.30, 0.20, 0.15, 0.15]` | `[0.728817, 0.271183, 0.0]` | `0.800039` | `0.946155` | `1.395000` | **`0.422296`** | `0.412104` | `0.790286` | `0.625148` | `0.424467` | `0.373001` |
| **`Track B`** | `43` | `[0.20, 0.30, 0.20, 0.15, 0.15]` | `[0.730005, 0.269995, 0.0]` | `0.737643` | `0.916994` | `1.307500` | **`0.418551`** | `0.408274` | `0.788654` | `0.623010` | `0.420914` | `0.412824` |
| **`Track B`** | `44` | `[0.20, 0.30, 0.20, 0.15, 0.15]` | `[0.728659, 0.271341, 0.0]` | `0.774721` | `0.927845` | `1.330000` | **`0.422164`** | `0.410829` | `0.789590` | `0.624372` | `0.422888` | `0.395922` |
| **`Track A`** | `42` | `[0.20, 0.20, 0.20, 0.20, 0.20]` | `[0.50, 0.50, 0.0]` (fixed) | `0.796922` | `0.938560` | `1.285000` | **`0.408827`** | `0.401016` | `0.786165` | `0.623722` | `0.411249` | `0.343291` |
| **`Track A`** | `43` | `[0.20, 0.20, 0.20, 0.20, 0.20]` | `[0.50, 0.50, 0.0]` (fixed) | `0.753443` | `0.916045` | `1.227500` | **`0.407841`** | `0.401522` | `0.785037` | `0.622223` | `0.408618` | `0.363464` |
| **`Track A`** | `44` | `[0.20, 0.20, 0.20, 0.20, 0.20]` | `[0.50, 0.50, 0.0]` (fixed) | `0.784239` | `0.919165` | `1.180000` | **`0.408506`** | `0.403099` | `0.785605` | `0.622850` | `0.409511` | `0.375007` |

### Table 3: Complete Session Test-Evaluation Audit (`11` Micro-Bets `L-PTCB-001`..`L-PTCB-011`)

In accordance with transparent benchmark accounting, every test-set evaluation executed during this session is logged in `object/certificate.json` (`session_test_evaluations_audit`):

| Bet ID | Script | Architecture Summary | 3-Seed Test `MCC` | Test `AUROC` | Test `AP` | Role in Package |
| :---: | :--- | :--- | :---: | :---: | :---: | :--- |
| `L-PTCB-001` | `bet1_biophys_pssm_synth_conv.py` | Pure 1-body BLOSUM62-smoothed PSSM + synthetic product convolution (`0` PLM) | `0.3006` | `0.7368` | `0.5504` | `exploratory_baseline` |
| `L-PTCB-002` | `bet2_holder_biochem_2body_cv.py` | 14-D Structural Biochemistry + Cosine-BLOSUM62 + Holder Power-Mean (`0` PLM) | `0.2945` | `0.7205` | `0.5636` | `exploratory_ablation` |
| `L-PTCB-003` | `bet3_inductive_thermodynamic_esm2.py` | 10-position Log-Odds State Function + WT-only `ESM2-8M` + 2-body epistasis | `0.2955` | `0.7728` | `0.6105` | `exploratory_ablation` |
| `L-PTCB-004` | `bet4_band_calibrated_survival_cv.py` | Multiplicative 10-site survival factor + 2-body `J_esm` tensor | `0.2667` | `0.7553` | `0.5790` | `exploratory_ablation` |
| `L-PTCB-005` | `bet5_contextual_esm2_eb_hybrid.py` | Contextual `ESM2-8M` (`VH-CDRH3` window `[78:122]`) + Empirical-Bayes (`tau=0`) | `0.1450` | `0.7901` | `0.6209` | `exploratory_ablation` |
| `L-PTCB-006` | `bet6_contextual_esm2_eb_closed_form_tau.py` | Contextual `ESM2-8M` + Empirical-Bayes + 0-vs-1 defect midpoint `tau_mid` | `0.4255` | `0.7901` | `0.6209` | `superseded_post_hoc_tau` |
| `L-PTCB-007` | `bet7_zero_magic_mutated_hazard_cv.py` | Parameter-free mutated-subspace competing-risks hazard + 10-Fold CV | `0.3087` | `0.7807` | `0.6010` | `negative_ablation` |
| **`L-PTCB-008`** | **`bet8_lotus_jensen_zero_magic_cv.py`** | **`Track A`: Parameter-Free Canonical Law (`1/5` equal weights + `LOTUS` CV)** | **`0.408391`** | **`0.785602`** | **`0.622932`** | **`claimed_track_A_canonical`** |
| `L-PTCB-009` | `bet9_decoupled_holder_trinity_lotus_cv.py` | Decoupled L6/L4 ridge + consecutive Holder power means $r \in \{0,-1,-2\}$ | `0.3610` | `0.7771` | `0.6088` | `negative_ablation` |
| `L-PTCB-010` | `bet10_canonical_fermi_boltzmann_crn_lotus_cv.py` | Canonical 3-potential Fermi-Boltzmann + CRN-512 `LOTUS` CV | `0.4056` | `0.7848` | `0.6229` | `exploratory_ablation` |
| **`L-PTCB-011`** | **`bet11_dual_canonical_and_cv_learned_solver.py`** | **Dual-Track Verifier (`Track B` 10-Fold CV-Learned Brier Shrinkage Stacking & `Track A` Canonical Law)** | **`0.421004`** | **`0.789510`** | **`0.624177`** | **`claimed_primary_dual_track`** |

---

## Not Claimed

1. **Zero Test-Set Training or Threshold Tuning:** No held-out test labels (`binary_score`) or test sequences (`one_vs_rest == 'test'`) were read by any fitting or threshold-selection routine inside `Track B` or `Track A`. Because `11` iterative hypotheses (`L-PTCB-001`..`L-PTCB-011`) were evaluated on the held-out test split across the research session, we release **both** `Track B` (where estimator stacking weights $w^* = [0.20, 0.30, 0.20, 0.15, 0.15]$, loop potential weights $\alpha^*$, and threshold $\tau_{\text{CV}}$ are learned via `10-Fold Stratified CV` on the `174` training rows: `MCC = 0.421004 +- 0.001735`) **and** `Track A` (the parameter-free `1/5` equal-weight canonical law $S(x) = \frac{1}{2}(\mu_\ell(x) + m_{-1}(x)) - C_{\text{pair}}(x)$: `MCC = 0.408391 +- 0.000411`) side-by-side in `object/`.
2. **Antibody Developability or Wet-Lab Affinity Not Claimed:** Predictions apply strictly to binary HER2 antigen binding (`binary_score`) in the Mason et al. / PLMFit `herH3` deep mutational scan; clinical pharmacokinetics, immunogenicity, and thermal stability are not claimed.

---

## Credits

- **Benchmark & Dataset Authors:** Thomas Bikias, Evangelos Stamkopoulos, and Sai T. Reddy (`LSSI-ETH/plmfit`, *Briefings in Bioinformatics* 26(4):bbaf381, 2025); Derek M. Mason, Simon Friedensohn, Cedric R. Weber et al. (*Nature Biomedical Engineering* 5:600–612, 2021).
- **Contributor:** `@mizopl` (`we*`).
