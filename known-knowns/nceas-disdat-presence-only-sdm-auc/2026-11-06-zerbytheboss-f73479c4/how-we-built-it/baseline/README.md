# Published Baseline Reference (`nceas-disdat-presence-only-sdm-auc`)

- **DeepMaxent TGB** (Ryckewaert et al. 2025, *Ecological Informatics* 90:103242, `arXiv:2412.19217` Table 3): 6-region unweighted mean ROC AUC = `0.768` (`AWT 0.716`, `CAN 0.731`, `NSW 0.752`, `NZ 0.754`, `SA 0.807`, `SWI 0.850`); target win bar = `0.768 + 0.005 = 0.773`.
- **Anand, Deneu & Radeloff** (2026, *PNAS* 123(12):e2522162123): 217-species (`< 1,000` presence-only records) median ROC AUC = `0.774` (vs Random Forest down-sampled `0.772`).
- **Doi, Osawa & Tsutsumida** (2026, `arXiv:2603.05062`, `hideyuki-doi/tabfm-distribution` Table 1 & Table S2): zero-shot `TabPFN-ens` 6-region unweighted mean ROC AUC = `0.736`, 217-species median = `0.758`, and LORO fine-tuned regional bests `NZ 0.759` and `SA 0.820`.
- **Valavi et al.** (2022, *Ecological Monographs* 92(1):e01486): `Random Forest down-sampled` `AWT 0.732`, `Boosted Regression Trees (BRT)` `CAN 0.732`.
