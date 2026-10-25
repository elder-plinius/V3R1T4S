# The Record We Beat (`const-ae/linear_perturbation_prediction-Paper`)

- **Paper:** C. Ahlmann-Eltze, W. Huber & S. Anders, *"Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines"*, *Nature Methods* **22**, 1657–1661 (2025), `doi:10.1038/s41592-025-02772-6`.
- **Pinned Repository Commit:** `bfa6eeea2bd145a1af2ec0127a2e808cc38456a9`.
- **Published Source Data Spreadsheets (`SHA-256` Verified):**
  - `source_data/single_perturbation_prediction.xlsx` (`sha256 = 09c6c198aff4e8a827064183f9cff13eb6f33e56f1689940527304bf78957efe`)
  - `source_data/suppl-pearson_delta_performance_single_pert.xlsx` (`sha256 = 61658661412f385356a383c3ed506f4454c6db79b28c272151bb15a725b0faaa`)
  - `source_data/suppl-k562_rpe1_transfer.xlsx` (`sha256 = 2e4649e8e9ab4bd91df0e7582805856b5c881b8b2741f319875a27ab5048903d`)

---

## Published Benchmark Numbers vs Our Certified Numbers (`Panel A`, `seeds = 1:2`)

| Dataset | Method | Mean $L_2$ ($\downarrow$) | Across-Split SD ($L_2$) | Median $L_2$ ($\downarrow$) | Mean Pearson $\Delta$ ($\uparrow$) | Across-Split SD ($r_{\Delta}$) | Median Pearson $\Delta$ ($\uparrow$) |
|---|---|---:|---:|---:|---:|---:|---:|
| `replogle_k562_essential` (`n = 262`) | `scgpt` (published) | `4.437277` | `0.054868` | `3.924462` | `0.316230` | `0.042009` | `0.282557` |
| `replogle_k562_essential` (`n = 262`) | `geneformer` (published) | `4.235811` | `0.069633` | `3.779902` | `0.403790` | `0.015805` | `0.419822` |
| `replogle_k562_essential` (`n = 262`) | `uce` (published) | `4.199545` | `0.061493` | `3.766328` | `0.409348` | `0.018043` | `0.414745` |
| `replogle_k562_essential` (`n = 262`) | `mean` (published & repro) | `4.193494` | `0.067250` | `3.821091` | `0.407910` | `0.017237` | `0.421438` |
| `replogle_k562_essential` (`n = 262`) | `scbert` (published) | `4.191708` | `0.068361` | `3.807219` | `0.408183` | `0.017147` | `0.424973` |
| `replogle_k562_essential` (`n = 262`) | **`lpm_selftrained` (published)** | **`4.097028`** | **`0.013200`** | **`3.805557`** | **`0.435544`** | **`0.024041`** | **`0.426484`** |
| `replogle_k562_essential` (`n = 262`) | **`lpm_selftrained` (our re-run)** | **`4.097028`** | **`0.013196`** | **`3.805564`** | **`0.435544`** | **`0.024039`** | **`0.426480`** |
| `replogle_k562_essential` (`n = 262`) | `gears` (published) | `4.078658` | `0.064478` | `3.800663` | `0.388092` | `0.020680` | `0.372622` |
| `replogle_k562_essential` (`n = 262`) | **`hollow_loo_dual_lens` (Ours)** | **`3.320307`** | **`0.024271`** | **`3.044310`** | **`0.620623`** | **`0.016671`** | **`0.644965`** |
| `replogle_rpe1_essential` (`n = 413`) | `gears` (published) | `6.113389` | `0.878694` | `6.046423` | `0.636032` | `0.003968` | `0.727245` |
| `replogle_rpe1_essential` (`n = 413`) | `scgpt` (published) | `5.991379` | `0.230710` | `5.464611` | `0.587962` | `0.026477` | `0.662197` |
| `replogle_rpe1_essential` (`n = 413`) | `mean` (published & repro) | `5.533708` | `0.137986` | `5.262884` | `0.677688` | `0.030162` | `0.788175` |
| `replogle_rpe1_essential` (`n = 413`) | `scbert` (published) | `5.527573` | `0.139453` | `5.256178` | `0.678177` | `0.030355` | `0.790121` |
| `replogle_rpe1_essential` (`n = 413`) | `uce` (published) | `5.506540` | `0.145887` | `5.233965` | `0.680243` | `0.031164` | `0.793957` |
| `replogle_rpe1_essential` (`n = 413`) | `geneformer` (published) | `5.493516` | `0.182904` | `5.237263` | `0.677785` | `0.032180` | `0.787624` |
| `replogle_rpe1_essential` (`n = 413`) | **`lpm_selftrained` (published)** | **`5.390179`** | **`0.230746`** | **`5.152959`** | **`0.680388`** | **`0.034730`** | **`0.791594`** |
| `replogle_rpe1_essential` (`n = 413`) | **`lpm_selftrained` (our re-run)** | **`5.390179`** | **`0.230747`** | **`5.152955`** | **`0.680388`** | **`0.034730`** | **`0.791592`** |
| `replogle_rpe1_essential` (`n = 413`) | **`hollow_loo_dual_lens` (Ours)** | **`4.777953`** | **`0.182955`** | **`4.514809`** | **`0.719286`** | **`0.024171`** | **`0.820713`** |
