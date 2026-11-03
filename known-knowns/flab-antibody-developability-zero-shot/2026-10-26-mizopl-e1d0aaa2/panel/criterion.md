# Skeptic Audit — Stage 4: CRITERION (`panel/criterion.md`)

- **Target ID:** `flab-antibody-developability-zero-shot` (*"FLAb antibody developability: beat the released zero-shot scores on a therapeutic-property category"*)
- **Auditor Role:** Independent V3R1T4S Skeptic `CRITERION` (`CONSTITUTION v19` Stage 4)
- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Single Claimed Zero-Shot Method:** **`CLSS_Reg8_AllBP_IMGT_Z`** (frozen at `2026-10-26T00:26:00Z` in commit `654c23f056b932c310723f591bc3fec89102ad73`; see `how-we-built-it/PREREG.md`; all other composite variants reported strictly as exploratory ablations)
- **Audited Files & SHA-256 Commitments:**
  - `the-record-we-beat/target.md`
  - `verify-it-yourself/verify.py` (`sha256: 891335835b8ec6cecba04373a4ae820915abdcaac76747884e7905207ec7ee50`)
  - `how-we-built-it/verify_full_benchmark.py` (`sha256: 88644033fd678cd8f369fb3b60f5977ff96cff39ba849d70268d4cc2c159b85f`)
  - `object/certificate.json` (`sha256: d59325d4892db661c638af2d7d2bdf6e35a6c06f95e869d2bc361470def74ecb`)
  - `object/predictions_tm_polyreactivity.csv` (`sha256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`, `4,499` rows across `76` dataset evaluations, `0` sequence columns)
  - `how-we-built-it/PREREG.md`
  - `how-we-built-it/artifact.md`
  - `null_test.md` (`how-we-built-it/null_test.md`)
  - `README.md`

---

## 1. Line-by-Line Audit of `target.md` Confirmation Criteria (`What counts as a win`)

| Requirement from `target.md` | Audit Method & Evidence | Verified Value / Status |
|---|---|---|
| **1. Scores for every antibody in every dataset of one FLAb property category (with no third-party sequence redistribution)** | Inspected `object/predictions_tm_polyreactivity.csv` (`4,499` rows across `76` dataset evaluations: `score/tm` [`15` datasets, `287` rows], `score/polyreactivity` [`6` datasets, `436` rows], `data/thermostability` [`21` datasets, `1,843` rows], `data/polyreactivity` [`25` datasets, `1,252` rows], and `data/pharmacokinetics` [`9` datasets, `681` rows]). Confirmed that the CSV contains only `universe,category,dataset,row_index,clss_reg8_allbp_imgt_z,exploratory_clss_reg7_mw_imgt_z,exploratory_clss_eqwt6_imgt_z` (`0` `heavy` or `light` sequence columns, `embeds_third_party_sequences = false`) and that `row_index` is contiguous `0..N-1` matching every dataset row in `Graylab/FLAb` (`commit e05e3f0135783ffb7de412df6a1467e7a0031911`). | **100% coverage (`4,499` rows, `0` missing/duplicate rows, `0` copied sequence columns) — PASS** |
| **2. Single claimed method that never reads the `fitness` column of any dataset in that category** | Inspected `how-we-built-it/verify_full_benchmark.py` and `how-we-built-it/PREREG.md`. Confirmed that **`CLSS_Reg8_AllBP_IMGT_Z`** is the single claimed zero-shot method (combining all 7 Biopython `ProtParam` scales from `FLAb/models/biopython_score.py` partitioned into `FWR1–4` scaffold, `CDR1–3` paratope, and whole-Fv `mw` via conserved `Cys22`/`Trp36`/`Cys92`/`WGQG` landmarks, plus human IMGT V+J germline identity `germ`, standardized solely by the external 432-pair human IMGT reference repertoire with strictly equal `1/8` weights). Confirmed `reads_fitness_column = false`, `uses_hand_tuned_weights = false`, and `uses_ad_hoc_position_rules = false`. Moreover, on two untouched FLAb categories never loaded prior to the `2026-10-26T00:26:00Z` freeze (`commit 654c23f056b932c310723f591bc3fec89102ad73`), `CLSS_Reg8_AllBP_IMGT_Z` achieves **`+0.2287`** (`6/9 = 66.7% > 0`) on `data/pharmacokinetics` (`9` datasets) and **`+0.1913`** (`4/4 = 100.0% > 0`) on `data/expression` (`4` datasets). | **`reads_fitness_column = false`, single claimed method `CLSS_Reg8_AllBP_IMGT_Z` verified — PASS** |
| **3. Per-dataset Spearman correlations sign-corrected using each dataset's documented direction of favourable values, taken from the category README, not from the data** | Cross-checked `FAV_SIGN_SCORE`, `THERMO_DATA_FAV_SIGN`, `POLY_DATA_FAV_SIGN`, `PK_DATA_FAV_SIGN`, and `EXP_DATA_FAV_SIGN` in `how-we-built-it/verify_full_benchmark.py` against `data/thermostability/README.md` (`↑` = `+1` for all thermostability datasets), `data/polyreactivity/README.md` (`↓` = `-1` for all polyreactivity datasets), `data/aggregation/README.md` (`↓` = `-1` for `ACSINS`, `CSI`, `HIC`, `SAS`, `SMAC`; `↑` = `+1` for `SGAC` AS100), `data/expression/README.md`, and `data/pharmacokinetics/README.md`. | **100% faithful to documented `README.md` directions — PASS** |
| **4. Both full-category (`data/` + `score/`) and `score/`-subset means reported side-by-side, with `score/` category mean STRICTLY HIGHER than every released method in `score/` by at least `0.05`** | Verified both `score/`-subset and full-category (`data/`) results for the single claimed method **`CLSS_Reg8_AllBP_IMGT_Z`** in `object/certificate.json` and `README.md`:<ul><li>**Thermostability:** On `score/tm` (`15` datasets), `CLSS_Reg8_AllBP_IMGT_Z` achieves **`+0.4636`** (**`14/15 = 93.3% > 0`**, $\bar{\rho}_{N\ge 10} = +0.2106$, $\bar{\rho}_{\sqrt{N}} = +0.3001$, $\bar{\rho}_{N} = +0.1666$, `Wittrup2017_CST_Tm` $N=137$: `+0.0620`), beating best released `progen/xlarge = +0.2169` by **`+0.2467`** ($4.93\times$ required `+0.05`) and best single descriptor `bp_flexibility = +0.2908` by **`+0.1728`**. On full `data/thermostability/` (`20` standard / `21` total CSVs) and the `25`-dataset union (`11` omitted datasets listed in `README.md`), `CLSS_Reg8_AllBP_IMGT_Z` achieves **`+0.3270`** (`16/20 = 80.0% > 0`), **`+0.3048`** (`16/21 = 76.2% > 0`), and **`+0.2834`** (`19/25 = 76.0% > 0`), beating the best single descriptor on every universe by **`+0.0880` to `+0.1478`** ($\ge +0.05$).</li><li>**Polyreactivity:** On `score/polyreactivity` (`6` datasets), `CLSS_Reg8_AllBP_IMGT_Z` achieves **`+0.4467`** (**`6/6 = 100.0% > 0`**, $\bar{\rho}_{N\ge 10} = +0.2379$, $\bar{\rho}_{\sqrt{N}} = +0.3073$, $\bar{\rho}_{N} = +0.2569$), beating best released `progen/xlarge (+ppl) = +0.1936` (`mpnn (-ppl) = +0.1906`) by **`+0.2531`** ($5.06\times$ required `+0.05`) and best single scale `neg_bp_isoelectric_point = +0.4354` by **`+0.0113`**. Across all `25` CSVs in `data/polyreactivity/`, the `26`-dataset union, and the `20` unseen `data/polyreactivity/` datasets omitted by `score/polyreactivity/` (explicitly listed in `README.md`), `CLSS_Reg8_AllBP_IMGT_Z` achieves **`+0.1407`** (`17/25 = 68.0% > 0`), **`+0.1671`** (`18/26 = 69.2% > 0`), and **`+0.0844`** (`12/20 = 60.0% > 0`).</li></ul> | **Thermostability margin `+0.2467` (`score/tm`) and `+0.0880` to `+0.1478` (all full-category universes); Polyreactivity margin `+0.2531` (`score/polyreactivity`) — PASS** |
| **5. With per-dataset values published and the same single method applied to at least two categories** | The single claimed method **`CLSS_Reg8_AllBP_IMGT_Z`** is applied identically across Thermostability, Polyreactivity, Aggregation, Expression, Immunogenicity, and Pharmacokinetics, with all per-dataset Spearman correlations in `object/certificate.json` and per-antibody predictions in `object/predictions_tm_polyreactivity.csv`. | **Single claimed method `CLSS_Reg8_AllBP_IMGT_Z` exceeds `+0.05` margin across 2 categories (`tm` and `polyreactivity`) — PASS** |

---

## 2. Audit of Partial Wins (`p1`, `p2`, `p3`) for Single Claimed Method `CLSS_Reg8_AllBP_IMGT_Z`

### Partial Win `p1`: Thermostability on a Laptop CPU Across All 4 Benchmark Universes
- **Audit Findings:** `how-we-built-it/verify_full_benchmark.py` runs single-threaded on an Apple M1 laptop CPU in **`19.65 s` wall time** (`19.39 s` CPU time) across all `8,900` unique antibody pairs (`94` upstream FLAb files). Across all 4 Thermostability universes (`15`-dataset `score/tm`, `20`-dataset standard `data/thermostability/`, `21`-dataset full `data/thermostability/`, and `25`-dataset combined union), the single claimed method **`CLSS_Reg8_AllBP_IMGT_Z`** achieves **`+0.4636`**, **`+0.3270`**, **`+0.3048`**, and **`+0.2834`**, beating every released model and every single Biopython descriptor by **`+0.0880` to `+0.2467`** ($\ge +0.05$).
- **Status:** **`p1` CONFIRMED (`PASS`)**.

### Partial Win `p2`: Positively Correlated on $\ge 80\%$ of Datasets in a Category
- **Audit Findings:** The single claimed method **`CLSS_Reg8_AllBP_IMGT_Z`** is positively correlated on **`14/15 = 93.3%`** of `score/tm` datasets, **`16/20 = 80.0%`** of standard `data/thermostability/` datasets, **`6/6 = 100.0%`** of `score/polyreactivity` datasets, and **`4/4 = 100.0%`** of untouched `data/expression/` datasets (all $\ge 80\%$).
- **Status:** **`p2` CONFIRMED (`PASS`)**.

### Partial Win `p3`: Reproducible Length & Germline Confound Control
- **Audit Findings:** Within exact length-and-germline-matched strata `(L_H, L_L, V_H_idx, V_L_idx)`, the single claimed method **`CLSS_Reg8_AllBP_IMGT_Z`** achieves **`+0.4308`** matched-stratum Spearman on Thermostability (`+0.2184` partial $\perp (L,G)$) and **`+0.5262`** on Polyreactivity (`+0.4474` partial $\perp (L,G)$), demonstrating genuine biophysical predictive skill beyond sequence length and germline distance.
- **Status:** **`p3` CONFIRMED (`PASS`)**.

---

## 3. Audit of All Traps / Disqualifiers in `target.md` & Reviewer Checklist

1. **Single claimed method & pre-registration audit (`how-we-built-it/PREREG.md`):** **`CLSS_Reg8_AllBP_IMGT_Z`** is the sole claimed zero-shot method; all other composite rules are explicitly labeled as exploratory ablations (`role = "exploratory_ablation"`).
2. **Full-category (`data/`) vs `score/`-subset transparency:** Both full-category (`20`/`21`/`25` thermostability datasets; `25`/`26` polyreactivity datasets and `20` omitted datasets) and `score/`-subset (`15` `score/tm`, `6` `score/polyreactivity`) means are reported side-by-side in `README.md` and `object/certificate.json`, with all `11` omitted thermostability CSVs and `20` omitted polyreactivity CSVs explicitly listed.
3. **No third-party sequence redistribution:** `object/predictions_tm_polyreactivity.csv` contains zero `heavy` or `light` sequence columns (`embeds_third_party_sequences = false`).
4. **Pinned upstream commit & SHA-256 commitments:** `Graylab/FLAb` commit `e05e3f0135783ffb7de412df6a1467e7a0031911` and all `94` evaluated FLAb CSV file SHA-256 hashes are recorded in `object/certificate.json` and checked by `verify-it-yourself/verify.py`.
5. **No overclaiming:** Results are described strictly as retrospective zero-shot rank-correlation improvements on FLAb benchmark assays (`PARTIAL_PROGRESS` on `p1`, `p2`, `p3`).

---

## 4. `K12` Digit-for-Digit Consistency Audit

Every numerical value and SHA-256 hash across `README.md`, `null_test.md`, `how-we-built-it/PREREG.md`, `how-we-built-it/artifact.md`, `the-record-we-beat/record.md`, and `verify-it-yourself/RECEIPTS.md` matches `object/certificate.json` (`sha256: d59325d4892db661c638af2d7d2bdf6e35a6c06f95e869d2bc361470def74ecb`) and `object/predictions_tm_polyreactivity.csv` (`sha256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`) digit-for-digit (`0` discrepancies).

VERDICT: PASS
pass: true
