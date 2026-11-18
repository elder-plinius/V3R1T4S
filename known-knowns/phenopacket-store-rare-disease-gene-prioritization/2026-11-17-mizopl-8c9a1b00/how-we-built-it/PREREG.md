# Prospective Pre-Registration & Total Blind-Evaluation Accounting (`PREREG.md`)

- `target_id`: `phenopacket-store-rare-disease-gene-prioritization`
- `milestone`: `p2`
- `claimed_primary_method`: `MARG-P2 (object/marg_p2_ranker.py, l2_reg = 0.03, temp = 0.18)`
- `method_sha256`: `8c9a1b001a6de22406675281c04de5eb20f9c4bd1a4660f45536cb0b3de5176d`
- `dev_cohort`: `P2-Dev (1,132 cases across 112 even-indexed sorted corpus-only genes)`
- `blind_test_cohorts`: `P2-Raw (127 cases, 10 untouched-unannotated genes) and P2-Holdout (988 cases, 112 odd-indexed sorted corpus-only genes)`
- `stage0_stratification_frozen_utc`: `2026-11-17T06:59:00Z`
- `architecture_seam_frozen_utc`: `2026-11-17T08:18:18Z`
- `pass1_evaluated_utc`: `2026-11-17T09:19:00Z`
- `temporal_audit_gate_utc`: `2026-11-17T11:00:55Z`
- `pass2_strict_precorpus_evaluated_utc`: `2026-11-17T12:25:59Z`
- `total_blind_test_evaluations`: `2`

## 1. Prospective Design & Complete Accounting of All `2` Blind-Split Evaluation Passes

1. **Prospective `P2-Dev` Design (`2026-11-17T06:59Z` to `08:18Z`, `0` Test-Set Peeking):** All channel operators (`f1..f6`), L2-row-norm hub whitening (`gamma = 0.75..0.80`), and 5-fold gene-grouped cross-validation (`temp = 0.18`, `l2_reg = 0.03` shrinkage toward uniform `1/6`) were designed exclusively on `P2-Dev` before loading `P2-Raw` or `P2-Holdout`. `object/marg_p2_ranker.py` accepts only `obs_hpo_terms` (`Sequence[str]`) and is AST-checked in `verify-it-yourself/verify.py`.
2. **Exact Accounting of Pass 1 vs. Pass 2 (`total_blind_test_evaluations = 2`, Zero Formula/Hyperparameter Changes):** After Pass 1 (`2026-11-17T09:19Z`), an internal pre-submission temporal provenance audit identified that two auxiliary disease-gene mapping files in the local workspace — unversioned NCBI `mim2gene_medgen` (fetched Nov 2026, adding `98` post-cutoff OMIM links, giving `12` extra human genes HPO terms in `clean_gene_terms`, and excluding `OTUD7A` [`2` cases] from `P2-Cleaned`) and `LIRICAL`'s Orphanet `en_product6.xml` (header date `2026-06-23`, `14` days past `2026-06-09`) — post-dated the `2026-06-09` corpus cutoff. Because pinned `HPO v2026-06-06` (`2026-06-08 < 2026-06-09`) already ships `genes_to_disease.txt` (`sha256: 81e8d2e0bc1c1052c383614ad85388325deeacb4b9478c6d9585597f45602bac`) containing the exact pre-corpus `2026-06-06` snapshots of both OMIM (`7,653` rows) and Orphanet (`8,288` rows), Pass 2 purged both post-cutoff files and re-ran the **exact unchanged** 6-channel `MARG-P2` formula and hyperparameters (`l2_reg = 0.03`, `temp = 0.18`). Both passes are reported transparently below:

| Evaluation Pass & Method | `P2-Raw` (`127` Cases) `MRR` (`Median`) | `P2-Holdout` Cases (`Genes`) | `P2-Holdout` `MRR` (`Top-1`, `Top-10`, `Median`) | `LIRICAL 2.4.1` `P2-Raw` / `P2-Holdout` `MRR` |
| :--- | ---: | ---: | ---: | ---: |
| `Pass 1` (pre-audit `mim2gene_medgen` + `en_product6.xml`): `MARG-P2` (`l2=0.03`) | `0.001147` (`3795.0`) | `1,062 (111)` | `0.017450` (`13/1,062`, `28/1,062`, `2869.0`) | `0.000083` / `0.000089` |
| `Pass 1` Inclusive `6/6` Equal-Weight (`[1/6]*6`, baseline) | `0.001059` (`8091.0`) | `1,062 (111)` | `0.017473` (`13/1,062`, `30/1,062`, `4178.0`) | `0.000083` / `0.000089` |
| **`Pass 2` (strict `< 2026-06-09` `genes_to_disease.txt` ONLY): `MARG-P2` (`l2=0.03`, claimed primary)** | **`0.001089`** (`8957.0`) | **`988 (112)`** | **`0.008803`** (`5/988`, `9/988`, `4052.5`) | `0.000083` / `0.000089` |
| `Pass 2` Inclusive `6/6` Equal-Weight (`[1/6]*6`, inclusive baseline) | `0.001057` (`8123.0`) | `988 (112)` | `0.008274` (`5/988`, `9/988`, `3818.5`) | `0.000083` / `0.000089` |
| `Pass 2` `l2_reg = 0.08` (`exploratory_ablation`) | `0.001108` (`8805.0`) | `988 (112)` | `0.008654` (`5/988`, `9/988`, `4099.5`) | `0.000083` / `0.000089` |

## 2. `P2-Dev` (`1,132` Cases, `112` Genes) 5-Fold Gene-Grouped CV `l2_reg` Sensitivity Grid

| `l2_reg` (`Role`) | `OOF MRR` | `Macro-Gene MRR` | `Top-1` | `Top-10` | `Top-100` | `Median Rank` | Mean Weights `[f1, f2, f3, f4, f5, f6]` |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | :--- |
| `0.0` (`exploratory_ablation`) | `0.013096` | `0.024491` | `0.0062` (`7`) | `0.0186` (`21`) | `0.0795` (`90`) | `2911.0` | `[0.1318, 0.4201, 0.0000, 0.0005, 0.0000, 0.4476]` |
| `0.02` (`exploratory_ablation`) | `0.017934` | `0.024040` | `0.0124` (`14`) | `0.0212` (`24`) | `0.0857` (`97`) | `6076.0` | `[0.2410, 0.2469, 0.0906, 0.1868, 0.0109, 0.2239]` |
| `0.03` (`claimed_primary`) | `0.017895` | `0.023778` | `0.0124` (`14`) | `0.0212` (`24`) | `0.0866` (`98`) | `6075.0` | `[0.2351, 0.2365, 0.1078, 0.1846, 0.0171, 0.2189]` |
| `0.08` (`exploratory_ablation`) | `0.018419` | `0.024039` | `0.0133` (`15`) | `0.0203` (`23`) | `0.0848` (`96`) | `5809.0` | `[0.2159, 0.2149, 0.1335, 0.1743, 0.0619, 0.1995]` |
| `0.2` (`exploratory_ablation`) | `0.017285` | `0.020835` | `0.0115` (`13`) | `0.0274` (`31`) | `0.0848` (`96`) | `4621.0` | `[0.1809, 0.1911, 0.1478, 0.1675, 0.1230, 0.1897]` |
| `infinity_uniform_1_over_6` (`inclusive_6_of_6_equal_weight_baseline`) | `0.017206` | `0.019406` | `0.0115` (`13`) | `0.0283` (`32`) | `0.0839` (`95`) | `4244.0` | `[0.1667, 0.1667, 0.1667, 0.1667, 0.1667, 0.1667]` |
