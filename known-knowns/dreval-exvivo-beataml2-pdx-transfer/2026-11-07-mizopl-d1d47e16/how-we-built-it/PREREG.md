# Prospective Pre-Registration — `dreval-exvivo-beataml2-pdx-transfer` (`p3`)

- **Target ID:** `dreval-exvivo-beataml2-pdx-transfer`
- **Pre-Registration Freeze Timestamp (UTC):** `2026-11-07T16:00:00Z`
- **Upstream Stage-2 Lock SHA-256:** `27fe6b922845d06fa50951f82fa6b13ff980d9ac61a7e7b11521a60919529d70`
- **Claimed Ladder Step:** `p3` (Quantitative decomposition of the `CTRPv2` $\to$ ex vivo transfer gap across assay/readout differences, expression-platform shift, and drug overlap, using strictly `CTRPv2` training data and unlabeled ex vivo features/metadata)

## 1. Frozen Training & Evaluation Protocol (Zero Ex Vivo Label Access)

1. **Training Data (`CTRPv2` Only):** All model weights (`SchurBilinearExVivoDRP`, `RawPlatformKRR_Ablation`, `RandomForest_SameEnv`, `GradientBoosting_SameEnv`, `NaiveMeanEffectsPredictor`) and all concentration-window regression slopes are fitted **exclusively** on the 10 official `CTRPv2` cross-validation training splits (`train + validation` per split from `splits.zip`, `sha256: 28dfdd7dca4ea5d2ca7da1ea0f53bb2eb149bd150bfabbf47cd9f1f145fd5839`).
2. **Held-Out Ex Vivo Evaluation Sets:**
   - `BeatAML2` (`sha256: 259d409e33d87be1c63139fd2c38f82d2d94be23442010bc2b5fd71cd5de73d9`): `19,823` feature-valid `(cell_line_name, pubchem_id)` pairs per split across `484` AML patient samples and `154` drugs (`79` shared with `CTRPv2` = `11,901` rows; `75` unseen in `CTRPv2` = `7,922` rows).
   - `PDX_Bruna` (`sha256: 63ef6dc157bc6bf0dc7a08a18ca86ff84509b8d2ef5e1f4a3c42a3cfbf368ee4`): `1,046` feature-valid `(cell_line_name, pubchem_id)` pairs per split across `25` breast-cancer PDX models and `100` drugs (`49` shared with `CTRPv2` = `555` rows; `51` unseen in `CTRPv2` = `491` rows).
3. **Pre-Registered Unlabeled `p3` Corrections Applied to the Same Predictions $\hat{y}_{\text{schur}}(c,d)$:**
   - **Factor (i) — Assay & Readout Concentration-Window Shift ($\Delta^{(i)}_{\text{assay}}(c,d)$):** Fit within-drug Fixed-Effect OLS of `LN_IC50_curvecurator` on $(\ln\text{min\_dose}_{\mu\text{M}}, \ln\text{max\_dose}_{\mu\text{M}})$ strictly on `CTRPv2` training split $k$, and evaluate the shift from drug $d$'s `CTRPv2` reference concentration window (or `CTRPv2` split mean window for unseen drugs) to the target assay's unlabeled plate dilution bounds `[min_dose_M, max_dose_M]`.
   - **Factor (ii) — Expression-Platform Shift ($\Delta^{(ii)}_{\text{platform}}$):** Remove the unlabeled cohort multi-view expression standardization offset $-\mathbb{E}_{(c,d)}[\hat{y}_{\text{schur}}(c,d) - \hat{y}_{\text{raw\_krr}}(c,d)]$ between multi-omic rank-normal views (`SchurBilinearExVivoDRP`) and single-view `CTRPv2`-scaled expression (`RawPlatformKRR_Ablation`).
   - **Factor (iii) — Drug Overlap Between `CTRPv2` and the Ex Vivo Screen ($\Delta^{(iii)}_{\text{overlap}}(c,d)$):** Align unseen drugs ($d \notin D_{\text{CTRPv2}^{(k)}}$) from the inactive-probe-dominated `CTRPv2` global prior to the shared clinical drug panel prior using the unlabeled prediction difference $\mathbb{I}(d \notin D_{\text{CTRPv2}^{(k)}})(\overline{\hat{y}_{\text{shared}}}^{(k)} - \overline{\hat{y}_{\text{unseen}}}^{(k)})$, and report the shared-drug vs unseen-drug strata side-by-side with the full drug set.
