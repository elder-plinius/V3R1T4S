# Skeptic 2: Baseline & Prior-Work Review — `dreval-exvivo-beataml2-pdx-transfer` (`p3`)

context: independent comparison against dilis-lab/drevalpy baseline records
target_id: dreval-exvivo-beataml2-pdx-transfer
package: 2026-11-07-mizopl-d1d47e16

## Checks Performed

1. **Published `drevalpy` Comparators:** Verified live comparator links (`https://dilis-lab.github.io/drevalpy-report/index.html`, `https://dilis-lab.github.io/drevalpy-report/LCO.html`, and `https://zenodo.org/records/14974099`) and same-environment 10-split re-runs of `RandomForest_SameEnv`, `GradientBoosting_SameEnv`, `RawPlatformKRR_Ablation`, and `NaiveMeanEffectsPredictor` on the exact same 10 `CTRPv2` splits (`splits.zip`, `sha256: 28dfdd7dca4ea5d2ca7da1ea0f53bb2eb149bd150bfabbf47cd9f1f145fd5839`).
2. **Distinctness of the Unlabeled `p3` Decomposition:** Unlike post-hoc test-label calibration, the three `p3` adjustments here are estimated strictly from `CTRPv2` training data and unlabeled ex vivo metadata/features:
   - `(i)` Within-drug Fixed-Effect (`FE`) regression of `LN_IC50_curvecurator` on $(\ln\text{min\_dose}_{\mu\text{M}}, \ln\text{max\_dose}_{\mu\text{M}})$ fitted on `CTRPv2` training split $k$ (`beta_log_min_uM = +0.000642`, `beta_log_max_uM = +0.376184`) and evaluated on the target screen's unlabeled plate dilution bounds `[min_dose_M, max_dose_M]`.
   - `(ii)` Unlabeled cohort multi-view expression standardization shift $-\mathbb{E}[\hat{y}_{\text{schur}} - \hat{y}_{\text{raw\_krr}}]$ (`-0.14191` on `BeatAML2` RNA-seq; `-0.36781` on `PDX_Bruna` Illumina BeadChip microarray) paired with within-sample van der Waerden normal-score alignment.
   - `(iii)` Unlabeled unseen-drug clinical overlap prior shift $\mathbb{I}(d \notin D_{\text{CTRPv2}^{(k)}})(\overline{\hat{y}_{\text{shared}}}^{(k)} - \overline{\hat{y}_{\text{unseen}}}^{(k)})$ (`-1.29523` on `BeatAML2`; `-0.75936` on `PDX_Bruna`), paired side-by-side with the shared-drug (`79` / `49` drugs) and unseen-drug (`75` / `51` drugs) strata.

pass: true
