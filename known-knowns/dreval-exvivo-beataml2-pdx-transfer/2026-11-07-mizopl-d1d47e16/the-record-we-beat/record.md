# Baseline Record & Upstream Dataset Provenance — `dreval-exvivo-beataml2-pdx-transfer` (`p3`)

- **Target ID:** `dreval-exvivo-beataml2-pdx-transfer`
- **Leaderboard / Report Index URL:** https://dilis-lab.github.io/drevalpy-report/index.html
- **LCO & Cross-Study Report URL:** https://dilis-lab.github.io/drevalpy-report/LCO.html
- **Official Zenodo Dataset Archive URL:** https://zenodo.org/records/14974099
- **Benchmark Repository URL:** https://github.com/dilis-lab/drevalpy
- **UTC Fetch & Verification Timestamp:** `2026-11-07T16:00:00Z`
- **Upstream `BeatAML2/BeatAML2.csv` SHA-256:** `259d409e33d87be1c63139fd2c38f82d2d94be23442010bc2b5fd71cd5de73d9`
- **Upstream `PDX_Bruna/PDX_Bruna.csv` SHA-256:** `63ef6dc157bc6bf0dc7a08a18ca86ff84509b8d2ef5e1f4a3c42a3cfbf368ee4`
- **Upstream `CTRPv2/CTRPv2.csv` SHA-256:** `3069f5df0ffefeb2adeeb2ae4be2e0e43ff588154e3be2d414cfbd1224a7dc41`
- **Upstream `CTRPv2/splits.zip` SHA-256:** `28dfdd7dca4ea5d2ca7da1ea0f53bb2eb149bd150bfabbf47cd9f1f145fd5839`

## 1. Published Benchmark Record (`dilis-lab/drevalpy` v1.3.0)

In the `drevalpy` benchmark report (https://dilis-lab.github.io/drevalpy-report/index.html and https://dilis-lab.github.io/drevalpy-report/LCO.html), every cross-study model trained on `CTRPv2` (`10` CV splits, `LN_IC50_curvecurator`) yields negative test-set `R^2` and near-zero normalized `R^2_norm` on out-of-the-box zero-shot transfer to `BeatAML2` primary AML patient blasts and `PDX_Bruna` breast-cancer PDX tumor explants:

| Benchmark Cohort | Published Best (`drevalpy` Report) | Same-Environment `RandomForest` (10-Split Mean $\pm$ SD) | Same-Environment `GradientBoosting` (10-Split Mean $\pm$ SD) | `NaiveMeanEffectsPredictor` (10-Split Mean $\pm$ SD) | `RawPlatformKRR_Ablation` (10-Split Mean $\pm$ SD) | Unadjusted `SchurBilinearExVivoDRP` (10-Split Mean $\pm$ SD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`BeatAML2` (`19,823` rows/split, `484` AML patients, `154` drugs)** | `RandomForest` (`R^2 = -0.355`, `Pearson = 0.258`; `R2_norm <= 0` for all models) | `R2_norm = -0.11782 +- 0.03878`<br>`Pearson_norm = +0.23218 +- 0.00657`<br>`Spearman_norm = +0.26537 +- 0.01891`<br>`MSE = 15.5381 +- 0.5340` | `R2_norm = -0.13324 +- 0.02836`<br>`Pearson_norm = +0.20922 +- 0.00770`<br>`Spearman_norm = +0.23199 +- 0.01827`<br>`MSE = 15.7526 +- 0.3933` | `R2_norm = -0.07339 +- 0.00203`<br>`Pearson_norm = +0.00000 +- 0.00000`<br>`MSE = 14.9207 +- 0.0330` | `R2_norm = -0.10512 +- 0.00698`<br>`Pearson_norm = -0.01006 +- 0.00955`<br>`Spearman_norm = -0.00090 +- 0.01568`<br>`MSE = 15.3618 +- 0.1024` | `R2_norm = -0.09514 +- 0.00706`<br>`Pearson_norm = +0.08461 +- 0.00873`<br>`Spearman_norm = +0.12617 +- 0.01275`<br>`MSE = 15.2230 +- 0.1055`<br>*(79 shared drugs, $N=11,901$: `R2_norm = +0.01186 +- 0.00550`, `Pearson_norm = +0.18519 +- 0.01202`)* |
| **`PDX_Bruna` (`1,046` rows/split, `25` PDX models, `100` drugs)** | `GradientBoosting` (`R^2 = -0.163`, `Pearson = 0.091`; `R2_norm <= 0` for all models) | `R2_norm = -0.29623 +- 0.02244`<br>`Pearson_norm = +0.07715 +- 0.01008`<br>`Spearman_norm = +0.18460 +- 0.01987`<br>`MSE = 14.7737 +- 0.2625` | `R2_norm = -0.16638 +- 0.02703`<br>`Pearson_norm = +0.13012 +- 0.01639`<br>`Spearman_norm = +0.20569 +- 0.02034`<br>`MSE = 13.2936 +- 0.3074` | `R2_norm = -0.21288 +- 0.01246`<br>`Pearson_norm = +0.00000 +- 0.00000`<br>`MSE = 13.8237 +- 0.1440` | `R2_norm = -0.18939 +- 0.01549`<br>`Pearson_norm = +0.21946 +- 0.01303`<br>`Spearman_norm = +0.26100 +- 0.02103`<br>`MSE = 13.5558 +- 0.1758` | `R2_norm = -0.39248 +- 0.02784`<br>`Pearson_norm = +0.10046 +- 0.01842`<br>`Spearman_norm = +0.20911 +- 0.00906`<br>`MSE = 15.8705 +- 0.3121` |

## 2. Summary of the `p3` Unlabeled Transfer-Gap Decomposition

Because unadjusted out-of-the-box predictions on all evaluated rows yield `R2_norm = -0.09514` on `BeatAML2` and `R2_norm = -0.39248` on `PDX_Bruna` (below the primary `0.02` floor and below same-environment `RandomForest` on `p1` and `GradientBoosting` on `p2`), this submission addresses **`p3`**: a quantitative decomposition of the `CTRPv2` $\to$ ex vivo transfer gap across **(i) assay and readout differences**, **(ii) expression-platform shift**, and **(iii) drug overlap between `CTRPv2` and the ex vivo screen**, where every correction is estimated **strictly from `CTRPv2` training splits and unlabeled ex vivo features/metadata (zero access to `y_true`)** and applied both **each on its own** and **cumulatively** to the same `SchurBilinearExVivoDRP` predictions (`object/stage3_p3_gap_decomposition.json`).
