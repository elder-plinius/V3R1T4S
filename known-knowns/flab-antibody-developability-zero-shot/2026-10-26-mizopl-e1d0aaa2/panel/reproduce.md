# Skeptic Audit — Stage 4: REPRODUCE (`panel/reproduce.md`)

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Target ID:** `flab-antibody-developability-zero-shot`
- **Auditor Role:** Independent V3R1T4S Skeptic `REPRODUCE` (`CONSTITUTION v19` Stage 4)
- **Offline Package Verifier Audited (`verify-it-yourself/verify.py`):** `sha256: 891335835b8ec6cecba04373a4ae820915abdcaac76747884e7905207ec7ee50`
- **Full Benchmark Re-Evaluation Script Audited (`how-we-built-it/verify_full_benchmark.py`):** `sha256: 88644033fd678cd8f369fb3b60f5977ff96cff39ba849d70268d4cc2c159b85f`
- **Machine-Verified Certificate Audited (`object/certificate.json`):** `sha256: d59325d4892db661c638af2d7d2bdf6e35a6c06f95e869d2bc361470def74ecb`
- **No-Sequence Per-Antibody Prediction Table Audited (`object/predictions_tm_polyreactivity.csv`):** `sha256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e` (`4,499` rows across `76` dataset evaluations)

---

## 1. Zero-Shot, Zero-Network & No-Sequence-Leak Static AST Audit

We parsed the Abstract Syntax Tree (`ast.parse`) of both `verify-it-yourself/verify.py` and `how-we-built-it/verify_full_benchmark.py`:

1. **Zero `fitness` reads during scoring:** `AST fitness_refs in scoring functions = []`. Both `score_imgt_z_df` and `score_shrink_z_df` access exclusively `df["heavy"]` and `df["light"]`. Ground-truth `fitness` values are read solely in the outer evaluation loop after per-antibody predictions have been computed and frozen (`reads_fitness_column = false`).
2. **Zero external network calls:** `AST network imports = []`. All Biopython `ProtParam` scales, conserved immunoglobulin landmark detection (`Cys22`, `Trp36`, `Cys92/104`, `WGQG/FGQG`), and the 24 human IGHV + 5 IGHJ and 18 human IGKV/IGLV + 7 IGKJ/IGLJ IMGT germline reference sequences are self-contained inside `how-we-built-it/verify_full_benchmark.py`.
3. **Zero third-party sequence redistribution:** `object/predictions_tm_polyreactivity.csv` (`sha256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`) has header `universe,category,dataset,row_index,clss_reg8_allbp_imgt_z,exploratory_clss_reg7_mw_imgt_z,exploratory_clss_eqwt6_imgt_z` and contains **zero** `heavy` or `light` amino-acid sequence strings (`embeds_third_party_sequences = false`).
4. **Single claimed method (`CLSS_Reg8_AllBP_IMGT_Z`):** Uses all 7 Biopython `ProtParam` scales from `FLAb/models/biopython_score.py` partitioned by conserved FWR/CDR landmarks (`fwr_flex`, `neg_fwr_gravy`, `neg_fwr_inst`, `neg_cdr_arom`, `neg_cdr_pI`, `neg_cdr_chg`, `mw`) plus human IMGT germline identity (`germ`), standardized strictly by the external $24 \times 18 = 432$ human IMGT germline Fv reference mean and standard deviation (`IMGT_MEAN`, `IMGT_STD`) with strictly equal `1/8` weights (`role = "claimed_primary"`). All other composite variants are labeled `role = "exploratory_ablation"`.

---

## 2. Clean-Room Execution & Runtime Verification

1. **Offline Verifier (`sh verify-it-yourself/run_checks.sh`):**
   - **Exit Code:** `0` (`PASS` in `0.06 s` wall time)
   - Verifies SHA-256 commitments of `object/certificate.json` (`d59325d4892db661...`), `object/predictions_tm_polyreactivity.csv` (`63cf82e9994c98a2...`), and all `94` evaluated upstream `Graylab/FLAb` CSV files at commit `e05e3f0135783ffb7de412df6a1467e7a0031911`, checks all `4,499` prediction rows and column sums (`clss_reg8_allbp_imgt_z = 2015.128106`, `exploratory_clss_reg7_mw_imgt_z = 2178.978284`, `exploratory_clss_eqwt6_imgt_z = -2573.050315`), and recomputes all `score/`-subset, full-category (`data/`), untouched-category (`data/pharmacokinetics`, `data/expression`), `p1`/`p2`/`p3`, and $B=1,000$ permutation null metrics.
2. **Full Benchmark Re-Evaluation (`python3 how-we-built-it/verify_full_benchmark.py` against `Graylab/FLAb` commit `e05e3f0135783ffb7de412df6a1467e7a0031911`):**
   - **Exit Code:** `0`
   - **Wall Time:** `19.65 s` (`19.39 s` CPU time on a single Apple M1 core)
   - **Unique Antibody Pairs Scored & Cached:** `8,900` across `94` upstream FLAb CSV files (`score/` + `data/thermostability/` + `data/polyreactivity/` + `data/pharmacokinetics/` + `data/expression/`).

---

## 3. Independent Metric Recomputation (`object/predictions_tm_polyreactivity.csv` & `object/certificate.json`)

| Universe / Category | Method | Role | Datasets ($D$) | Unweighted $\bar{\rho}$ | $\bar{\rho}_{N\ge 10}$ | $\bar{\rho}_{\sqrt{N}}$ | $\bar{\rho}_{N}$ | Positive Datasets | Max $\|\Delta\|$ vs `certificate.json` |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| **`score/tm`** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Single Claimed** | 15 | **`+0.4636`** | `+0.2106` | `+0.3001` | `+0.1666` | **`14/15` (`93.33%`)** | `0.0000` |
| **`data/thermostability` (std)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Single Claimed** | 20 | **`+0.3270`** | `+0.1449` | `+0.1328` | `+0.0663` | **`16/20` (`80.00%`)** | `0.0000` |
| **`data/thermostability` (all)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Single Claimed** | 21 | **`+0.3048`** | `+0.1235` | `+0.1178` | `+0.0596` | **`16/21` (`76.19%`)** | `0.0000` |
| **Combined Thermostability** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Single Claimed** | 25 | **`+0.2834`** | `+0.0882` | `+0.1196` | `+0.0596` | **`19/25` (`76.00%`)** | `0.0000` |
| **`score/polyreactivity`** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Single Claimed** | 6 | **`+0.4467`** | `+0.2379` | `+0.3073` | `+0.2569` | **`6/6` (`100.00%`)** | `0.0000` |
| **`data/polyreactivity` (all)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Single Claimed** | 25 | **`+0.1407`** | `+0.0715` | `+0.0882` | `+0.0680` | **`17/25` (`68.00%`)** | `0.0000` |
| **Combined Polyreactivity** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Single Claimed** | 26 | **`+0.1671`** | `+0.0715` | `+0.0977` | `+0.0710` | **`18/26` (`69.23%`)** | `0.0000` |
| **Unseen `data/polyreactivity`** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Single Claimed** | 20 | **`+0.0844`** | `+0.0382` | `+0.0568` | `+0.0510` | **`12/20` (`60.00%`)** | `0.0000` |
| **Untouched `data/pharmacokinetics`** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Single Claimed** | 9 | **`+0.2287`** | `+0.2287` | `+0.2248` | `+0.2148` | **`6/9` (`66.67%`)** | `0.0000` |
| **Untouched `data/expression`** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Single Claimed** | 4 | **`+0.1913`** | `+0.1913` | `+0.2183` | `+0.2266` | **`4/4` (`100.00%`)** | `0.0000` |

pass: true
