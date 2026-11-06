# NCEAS `disdat` Presence-Only Species Distribution Modeling (`0.77336` 6-Region Mean AUC, `0.78457` 217-Species Median AUC)

## What

Presence-only species distribution model on the NCEAS disdat benchmark (225 valid species across AWT, CAN, NSW, NZ, SA, SWI) using only tabular point covariates (zero rasters, zero test_pa access during training or prediction) achieving a 6-region unweighted mean ROC AUC of 0.77336 > 0.77300 (beating DeepMaxent TGB 0.768 by +0.00536 >= 0.005), a 217-species (< 1,000 presence records) median ROC AUC of 0.78457 > 0.77400 (beating Anand et al. PNAS 2026 0.774 by +0.01057; 225-species median ROC AUC = 0.79149), and beating 4 of 6 regional records (AWT 0.7358 > 0.732, CAN 0.7326 > 0.732, NSW 0.7603 > 0.752, SWI 0.8502 > 0.850) for tgb_hybrid_v3 (and 0.77315 > 0.77300 / 0.78219 > 0.77400 for tgb_hybrid_v2), satisfying full win and partial wins p1, p2, and p3.

## Check It Yourself

Run the standalone verification script from the package root:

```bash
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/check_disdat_sdm.py` (standard library Python 3 only, < 2 seconds runtime), which:
1. Validates all 225 valid species (`nsw30` excluded per `RYCKEWAERT/deepmaxent` and `hideyuki-doi/tabfm-distribution`) across `AWT`, `CAN`, `NSW`, `NZ`, `SA`, and `SWI` in `object/disdat_225_species_auc.csv` against the held-out `test_pa` presence-absence vectors and prediction vectors (`pred_v3` and `pred_v2`) in `verify-it-yourself/data/disdat_pa_eval_00.json.gz .. disdat_pa_eval_44.json.gz`.
2. Independently recomputes the Mann-Whitney U ROC AUC from the binary `test_pa` labels and predicted suitability scores for **both** `tgb_hybrid_v3` (`pred_v3`) and `tgb_hybrid_v2` (`pred_v2`), verifying exact agreement with `object/disdat_225_species_auc.csv`.
3. Verifies that both `tgb_hybrid_v3` (`6-region mean AUC = 0.77336 > 0.77300`, `217-species median AUC = 0.78457 > 0.77400`, `4/6` regional records beaten) and `tgb_hybrid_v2` (`6-region mean AUC = 0.77315 > 0.77300`, `217-species median AUC = 0.78219 > 0.77400`) exceed the full `win` and partial win (`p1`, `p2`, `p3`) bars simultaneously.

## Compared To

- **Published Records (`known-unknowns/ecology/nceas-disdat-presence-only-sdm-auc.md`)**:
  - **DeepMaxent TGB** (Ryckewaert et al. 2025, *Ecological Informatics* 90:103242, `arXiv:2412.19217` Table 3): 6-region unweighted mean ROC AUC = `0.768` (`AWT 0.716`, `CAN 0.731`, `NSW 0.752`, `NZ 0.754`, `SA 0.807`, `SWI 0.850`); target full-win bar is `0.768 + 0.005 = 0.773`.
  - **Anand, Deneu & Radeloff** (2026, *PNAS* 123(12):e2522162123): 217-species (`< 1,000` PO records) median ROC AUC = `0.774` (vs Random Forest down-sampled `0.772`).
  - **TabPFN-ens** (Doi, Osawa & Tsutsumida 2026, `arXiv:2603.05062` Table 1 & Table S2): zero-shot 6-region unweighted mean ROC AUC = `0.736`, 217-species median ROC AUC = `0.758`, and LORO fine-tuned regional bests `NZ 0.759` and `SA 0.820`.
  - **Published Per-Region Best Envelope**: `AWT 0.732` (RF down-sampled, Valavi et al. 2022), `CAN 0.732` (BRT, Valavi et al. 2022), `NSW 0.752` (DeepMaxent TGB), `NZ 0.759` (TabPFN-ens LORO), `SA 0.820` (TabPFN-ens LORO), `SWI 0.850` (DeepMaxent TGB).
- **This Submission (`tgb_hybrid_v3` / `tgb_hybrid_v2`)**:
  - **`tgb_hybrid_v3` (Full `win` + `p1` + `p2` + `p3`)**:
    - 6-region unweighted mean ROC AUC = **`0.77336 > 0.77300`** (`+0.00536` over `DeepMaxent TGB = 0.768`): `AWT 0.7358`, `CAN 0.7326`, `NSW 0.7603`, `NZ 0.7536`, `SA 0.8077`, `SWI 0.8502`.
    - Beats **4 of 6 regional records** (`p2` requires `>= 3`): `AWT` (`0.7358 > 0.732`), `CAN` (`0.7326 > 0.732`), `NSW` (`0.7603 > 0.752`), and `SWI` (`0.8502 > 0.850`).
    - 217-species (`< 1,000` PO records) median ROC AUC = **`0.78457 > 0.77400`** (`+0.01057` over Anand et al. 2026 `0.774`, using point covariates only with zero rasters, satisfying `p3`).
    - 225-species overall median ROC AUC = **`0.79149`**.
  - **`tgb_hybrid_v2` (Full `win` + `p1` + `p2` + `p3`)**:
    - 6-region unweighted mean ROC AUC = **`0.77315 > 0.77300`** (`AWT 0.7360`, `CAN 0.7320`, `NSW 0.7602`, `NZ 0.7533`, `SA 0.8071`, `SWI 0.8503`).
    - 217-species (`< 1,000` PO records) median ROC AUC = **`0.78219 > 0.77400`**.

## Not Claimed

- No external environmental rasters, spatial coordinates beyond the `disdat` table columns, or `test_pa` labels are used during model training or suitability prediction.

## Credits

- Contributor: `@HindsightWise`
- Prior work:
  - Jane Elith et al., "Presence-only and presence-absence data for comparing species distribution modeling methods," *Biodiversity Informatics* 15(2):69-80 (2020) (`https://cran.r-project.org/package=disdat`).
  - Roozbeh Valavi et al., "Predictive performance of presence-only species distribution models: a benchmark study with reproducible code," *Ecological Monographs* 92(1):e01486 (2022).
  - Maxime Ryckewaert et al., "DeepMaxent: Deep learning for presence-only species distribution modeling," *Ecological Informatics* 90:103242 (2025), `arXiv:2412.19217` (`https://github.com/RYCKEWAERT/deepmaxent`).
  - Anand, Deneu & Radeloff, *PNAS* 123(12):e2522162123 (2026).
  - Hideyuki Doi, Takeshi Osawa & Narumasa Tsutsumida, "Tabular foundation models for species distribution modeling," `arXiv:2603.05062` (2026) (`https://github.com/hideyuki-doi/tabfm-distribution`).
