# Skeptic Audit — Stage 4: REPRODUCE (`panel/reproduce.md`)

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Target ID:** `flab-antibody-developability-zero-shot`
- **Auditor Role:** Independent V3R1T4S Skeptic `REPRODUCE` (`CONSTITUTION v19` Stage 4)
- **Claim Scope (`status: CONFIRMED_PARTIAL`):** **Partial Wins `p2` and `p3`** (Full Win, Binding, and `p1` are **not claimed**)
- **Offline Package Verifier Audited (`verify-it-yourself/verify.py`):** `sha256: 3583f9700c89ba0c00bf1d9eaaaaca0566166859880727be705d7b5acf8fbd18`
- **Full Benchmark Re-Evaluation Script Audited (`how-we-built-it/verify_full_benchmark.py`):** `sha256: 51a3a05a27708532df677cb5c49043998eff57b8fa6edfc12a85b841f50dcf45`
- **Machine-Verified Certificate Audited (`object/certificate.json`):** `sha256: b6be3abe5d0dcff18fcf18d8e7a16f64164d434290274613f79b76f80f598eb6`
- **No-Sequence Per-Antibody Prediction Tables Audited (`109,236` Total Rows Across `172` Dataset Evaluations):**
  - `object/predictions_tm_polyreactivity.csv` (`sha256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`, `4,499` rows across `76` dataset evaluations)
  - `object/predictions_binding_part1..8.csv` (`sha256: 8e748b57...` through `f41772d0...`, `104,737` rows across `96` binding dataset evaluations: `16` `score/binding` [`6,959` rows] + `80` `data/binding` [`97,778` rows])

---

## 1. Zero-Shot, Zero-Network & No-Sequence-Leak Static AST Audit

We parsed the Abstract Syntax Tree (`ast.parse`) of both `verify-it-yourself/verify.py` and `how-we-built-it/verify_full_benchmark.py`:

1. **Zero `fitness` reads during scoring:** `AST fitness_refs in scoring functions = []`. Both `score_imgt_z_df` and `score_shrink_z_df` access exclusively `df["heavy"]` and `df["light"]`. Ground-truth `fitness` values are read solely in the outer evaluation loop after per-antibody predictions have been computed and frozen (`reads_fitness_column = false`).
2. **Zero external network calls:** `AST network imports = []`. All Biopython `ProtParam` scales, conserved immunoglobulin landmark detection (`Cys22`, `Trp36`, `Cys92/104`, `WGQG/FGQG`), and the 24 human IGHV + 5 IGHJ and 18 human IGKV/IGLV + 7 IGKJ/IGLJ IMGT germline reference sequences are self-contained inside `how-we-built-it/verify_full_benchmark.py`.
3. **Zero third-party sequence redistribution:** `object/predictions_tm_polyreactivity.csv` (`4,499` rows) and `object/predictions_binding_part1..8.csv` (`104,737` rows) have header `universe,category,dataset,row_index,clss_reg8_allbp_imgt_z,exploratory_clss_reg7_mw_imgt_z,exploratory_clss_eqwt6_imgt_z` and contain **zero** `heavy` or `light` amino-acid sequence strings (`embeds_third_party_sequences = false`).
4. **Single frozen method (`CLSS_Reg8_AllBP_IMGT_Z`):** Uses all 7 Biopython `ProtParam` scales from `FLAb/models/biopython_score.py` partitioned by conserved FWR/CDR landmarks (`fwr_flex`, `neg_fwr_gravy`, `neg_fwr_inst`, `neg_cdr_arom`, `neg_cdr_pI`, `neg_cdr_chg`, `mw`) plus human IMGT germline identity (`germ`), standardized strictly by the external $24 \times 18 = 432$ human IMGT germline Fv reference mean and standard deviation (`IMGT_MEAN`, `IMGT_STD`) with strictly equal `1/8` weights (`role = "claimed_primary"`). All other composite variants are labeled `role = "exploratory_ablation"`.

---

## 2. Clean-Room Execution & Runtime Verification

1. **Offline Verifier (`sh verify-it-yourself/run_checks.sh`):**
   - **Exit Code:** `0` (`PASS` in `~1.5 s` wall time)
   - Verifies SHA-256 commitments of `object/certificate.json` (`b6be3abe5d0dcff1...`), `object/predictions_tm_polyreactivity.csv` (`63cf82e9994c98a2...`), `object/predictions_binding_part1..8.csv` (`8e748b57...` through `f41772d0...`), and all `190` evaluated upstream `Graylab/FLAb` CSV files at commit `e05e3f0135783ffb7de412df6a1467e7a0031911`, checks all `109,236` prediction rows across `172` dataset evaluations (`4,499` in `predictions_tm_polyreactivity.csv` + `104,737` across `predictions_binding_part1..8.csv`), and recomputes all `score/`-subset, full-category (`data/`), `binding` (`16` `score/binding` and `80` `data/binding`), untouched-category (`data/pharmacokinetics`, `data/expression`), `p2`/`p3` (`p1` and Full Win not claimed), and $B=1,000$ permutation null metrics.
2. **Full Benchmark Re-Evaluation (`python3 how-we-built-it/verify_full_benchmark.py` against `Graylab/FLAb` commit `e05e3f0135783ffb7de412df6a1467e7a0031911`):**
   - **Exit Code:** `0`
   - **Wall Time:** `45.95 s` (`43.28 s` CPU time on a single Apple M1 core)
   - **Unique Antibody Pairs Scored & Cached:** `54,131` across `190` upstream FLAb CSV files (`score/` + `data/thermostability/` + `data/polyreactivity/` + `data/binding/` + `data/pharmacokinetics/` + `data/expression/`).

---

## 3. Independent Metric Recomputation (`object/certificate.json` & Prediction CSVs)

| Universe / Category | Method | Datasets ($D$) | Unweighted $\bar{\rho}$ | $\bar{\rho}_{N\ge 10}$ | $\bar{\rho}_{\sqrt{N}}$ | $\bar{\rho}_{N}$ | Positive Datasets | Max $\|\Delta\|$ vs `certificate.json` |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **`score/tm` (`p1` not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 15 | **`+0.4636`** | `+0.2106` | `+0.3001` | `+0.1666` | **`14/15` (`93.33%`)** | `0.0000` |
| **`data/thermostability` (std; `p1` not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 20 | **`+0.3270`** | `+0.1449` | `+0.1328` | `+0.0663` | **`16/20` (`80.00%`)** | `0.0000` |
| **`data/thermostability` (all; `p1` not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 21 | **`+0.3048`** | `+0.1235` | `+0.1178` | `+0.0596` | **`16/21` (`76.19%`)** | `0.0000` |
| **`score/tm` plus `data/thermostability` union (`p1` not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 25 | **`+0.2834`** | `+0.0882` | `+0.1196` | `+0.0596` | **`19/25` (`76.00%`)** | `0.0000` |
| **`score/polyreactivity`** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 6 | **`+0.4467`** | `+0.2379` | `+0.3073` | `+0.2569` | **`6/6` (`100.00%`)** | `0.0000` |
| **`data/polyreactivity` (all)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 25 | **`+0.1407`** | `+0.0715` | `+0.0882` | `+0.0680` | **`17/25` (`68.00%`)** | `0.0000` |
| **`score/polyreactivity` plus `data/polyreactivity` union** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 26 | **`+0.1671`** | `+0.0715` | `+0.0977` | `+0.0710` | **`18/26` (`69.23%`)** | `0.0000` |
| **`score/binding` (vs $-K_d$ / vs $+K_d$; not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 16 | **`-0.0060`** / **`+0.0060`** | `-0.0038` | `-0.0017` | `+0.0058` | `6/16` / `10/16` | `0.0000` |
| **`data/binding` (all 80 CSVs; not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 80 | **`-0.0987`** | `-0.1046` | `-0.0882` | `-0.0566` | `36/80` (`45.00%`) | `0.0000` |
| **`data/binding` (12 primary `score/`-mapped; not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 12 | **`-0.1123`** | `-0.0910` | `-0.0604` | `-0.0046` | `5/12` (`41.67%`) | `0.0000` |
| **`data/binding` (15 study-mapped; not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 15 | **`-0.1640`** | `-0.1304` | `-0.0811` | `-0.0067` | `5/15` (`33.33%`) | `0.0000` |
| **`data/binding` (68 excluded CSVs; not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 68 | **`-0.0964`** | `-0.1069` | `-0.0914` | `-0.0606` | `31/68` (`45.59%`) | `0.0000` |
| **`data/binding` (65 excluded CSVs; not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 65 | **`-0.0837`** | `-0.0998` | `-0.0890` | `-0.0605` | `31/65` (`47.69%`) | `0.0000` |
| **`score/binding` plus `data/binding` union (not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 84 | **`-0.0809`** | `-0.0897` | `-0.0824` | `-0.0562` | `37/84` (`44.05%`) | `0.0000` |
| **Untouched `data/pharmacokinetics`** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 9 | **`+0.2287`** | `+0.2287` | `+0.2248` | `+0.2148` | **`6/9` (`66.67%`)** | `0.0000` |
| **Untouched `data/expression`** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 4 | **`+0.1913`** | `+0.1913` | `+0.2183` | `+0.2266` | **`4/4` (`100.00%`)** | `0.0000` |

pass: true
