# Reference Links & SHA-256 Digests (`linear-baseline-perturbation-replogle-k562`, Partial Progress `p2`)

- **Target ID**: `linear-baseline-perturbation-replogle-k562` (`known-knowns`, **Partial Progress `p2` only**)
- **Primary Paper**: Constantin Ahlmann-Eltze, Wolfgang Huber, and Simon Anders, *"Deep-learning-based gene perturbation effect prediction does not yet outperform simple linear baselines"*, **Nature Methods** 22, 1657–1661 (2025).
  - **Article URL**: https://www.nature.com/articles/s41592-025-02772-6
  - **Preprint URL**: https://www.biorxiv.org/content/10.1101/2024.09.16.613342v4
- **Upstream Code & Source Data Repository**: https://github.com/const-ae/linear_perturbation_prediction-Paper (commit `bfa6eeea2bd145a1af2ec0127a2e808cc38456a9`)
- **Zenodo Archive**: https://doi.org/10.5281/zenodo.15300707
- **Fetched / Verified Timestamp (UTC)**: `2026-10-25T22:03:00Z`

---

## 1. Upstream Source Data Links & SHA-256 Digests

Per review guidance, copied Source Data tables have been removed and replaced with stable links and SHA-256 digests:

| Upstream File | Stable Link (Commit `bfa6eeea2bd145a1af2ec0127a2e808cc38456a9`) | Size (Bytes) | SHA-256 Digest |
| :--- | :--- | ---: | :--- |
| `source_data/single_perturbation_prediction.xlsx` (Fig. 1a / Panel A $L_2$ Source Data) | https://github.com/const-ae/linear_perturbation_prediction-Paper/raw/bfa6eeea2bd145a1af2ec0127a2e808cc38456a9/source_data/single_perturbation_prediction.xlsx | `565,586` | `09c6c198aff4e8a827064183f9cff13eb6f33e56f1689940527304bf78957efe` |
| `source_data/suppl-pearson_delta_performance_single_pert.xlsx` (Suppl. Fig. 4 / Panel C $R_{\Delta}$ Source Data) | https://github.com/const-ae/linear_perturbation_prediction-Paper/raw/bfa6eeea2bd145a1af2ec0127a2e808cc38456a9/source_data/suppl-pearson_delta_performance_single_pert.xlsx | `569,165` | `61658661412f385356a383c3ed506f4454c6db79b28c272151bb15a725b0faaa` |
| `source_data/suppl-k562_rpe1_transfer.xlsx` (Suppl. Fig. 6 Transfer Source Data) | https://github.com/const-ae/linear_perturbation_prediction-Paper/raw/bfa6eeea2bd145a1af2ec0127a2e808cc38456a9/source_data/suppl-k562_rpe1_transfer.xlsx | `520,256` | `2e4649e8e9ab4bd91df0e7582805856b5c881b8b2741f319875a27ab5048903d` |
| `source_data/perturbation_prediction.xlsx` (Double Perturbation Source Data) | https://github.com/const-ae/linear_perturbation_prediction-Paper/raw/bfa6eeea2bd145a1af2ec0127a2e808cc38456a9/source_data/perturbation_prediction.xlsx | `238,243` | `e097df99adf72d983c63c4e9293c1abf8d10bff2a06c752a1a20644e95b9d591` |

---

## 2. Public Benchmark Dataset Links & SHA-256 Digests (`replogle_k562_essential` + GEARS GO Annotations)

All K562 single-perturbation evaluations and functional-distance stratifications use the unmodified Harvard Dataverse archives loaded by `gears.PertData` and `benchmark/src/run_linear_pretrained_model.py`:

| Archive / File | Stable Harvard Dataverse URL | Size (Bytes) | SHA-256 Digest |
| :--- | :--- | ---: | :--- |
| `gene2go_all.pkl` (Static 2023 GEARS Gene Ontology map, *Nature Biotechnology* 2023) | https://dataverse.harvard.edu/api/access/datafile/6153417 | `9,462,558` | `f145c5e84a53048d87942a417d870a4f2d8db50200b96e492b358c13aba8c771` |
| `essential_all_data_pert_genes.pkl` (Essential perturbation universe) | https://dataverse.harvard.edu/api/access/datafile/6934320 | `558,811` | `46c3dfe354d8ad5c0da22c69f3d0ca451987b1a61ed9d984279b22b9565ff8d7` |
| `go_essential_all.tar.gz` (Pre-computed GEARS GO Jaccard graph) | https://dataverse.harvard.edu/api/access/datafile/6934319 | `60,654,049` | `3d2ee2ebbcdf3ca2ca8fd8fb0d3bbf0a63db9dd2ff9fc7587abbd57a55b78998` |
| `go_essential_all/go_essential_all.csv` (Extracted edge list from `go_essential_all.tar.gz`) | https://dataverse.harvard.edu/api/access/datafile/6934319 | `181,694,556` | `99622d9215462e7bbea99a5f6c0b1e86febfef9f57226269418053484fcb3f9f` |
| `replogle_k562_essential.zip` (Replogle K562 single-perturbation archive) | https://dataverse.harvard.edu/api/access/datafile/7458695 | `669,703,049` | `ba5dc5eb7cdbb1cc32fb9ed3fd9ddab9f0eb7bc8b72a57a098cefb705d86e92d` |
| `replogle_k562_essential/perturb_processed.h5ad` (Extracted AnnData matrix from `replogle_k562_essential.zip`) | https://dataverse.harvard.edu/api/access/datafile/7458695 | `692,000,190` | `550fde89ac85c258c9fd517638fe34fb42c0e748c9305fe6355761a2bb754170` |

---

## 3. Target `p2` Definition (`bank/targets.json`)

Under `linear-baseline-perturbation-replogle-k562` in `bank/targets.json`:
- **`p2`**: *"Stratify perturbations by functional distance from the training set (for example, gene-ontology or pathway distance) and test whether the performance gap between linear and non-linear models widens for out-of-distribution perturbations."*
- **Scope**: This package claims **Partial Progress (`p2`) only**. Full target win, `p1` (RPE1 transfer), and `p3` (re-running published deep models across all 5 splits of both datasets) are **not claimed**.
