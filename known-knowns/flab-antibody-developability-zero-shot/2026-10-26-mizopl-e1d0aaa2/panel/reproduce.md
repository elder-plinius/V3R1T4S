# Skeptic Audit — Stage 4: REPRODUCE (`panel/reproduce.md`)

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Target ID:** `flab-antibody-developability-zero-shot`
- **Auditor Role:** Independent V3R1T4S Skeptic `REPRODUCE` (CONSTITUTION v18 Stage 4)
- **Verification Script Audited:** `claim/verify.py` (`SHA-256: 3571b51d0e1d0eac9156047fdb985fa46661b2fb1361c4beda694e2df3948e38`)
- **Certificate Audited:** `claim/certificate.json` (`SHA-256: e1d0aaa2449c9f1b8f5f83beb8d4dc717ad3f40893b281f1576d73273219c1c5`)

---

## 1. Zero-Shot & Zero-Network Static AST Audit

We parsed the Abstract Syntax Tree (`ast.parse`) of `claim/verify.py` and inspected every descriptor, regional FWR/CDR landmark partitioning, and scoring function (`clean`, `bp_gravy`, `bp_aromaticity`, `bp_molecular_weight`, `bp_instability_index`, `bp_average_flexibility`, `_charge_tables`, `_charge_at_pH_from_tables`, `bp_charge_at_7_4`, `bp_isoelectric_point`, `get_anchors`, `pure_germline_info`, `split_fwr_cdr`, `raw_descriptors`, `score_imgt_z_df`, `score_shrink_z_df`):

1. **Zero `fitness` reads during scoring:** `AST fitness_refs in scoring functions = []`. Both `score_imgt_z_df` and `score_shrink_z_df` access exclusively `df["heavy"]` and `df["light"]`. Ground-truth `fitness` values are read solely in the outer evaluation loop after per-antibody predictions have been computed and frozen.
2. **Zero external network calls:** `AST network imports = []`. Only standard local libraries (`os`, `glob`, `json`, `re`, `time`, `hashlib`, `tarfile`, `numpy`, `pandas`, `scipy.stats`) are imported. All Biopython `ProtParam` scales (Kyte-Doolittle hydropathy, Vihinen flexibility, Guruprasad instability index DIWV table, Bjellqvist pKa tables, and IUPAC amino acid weights), conserved immunoglobulin landmark anchor detection (`Cys22`, `Trp36`, `Cys92/104`, `WGQG/FGQG`), and the 24 human IGHV + 5 IGHJ and 18 human IGKV/IGLV + 7 IGKJ/IGLJ IMGT germline reference sequences are self-contained inside `claim/verify.py`.
3. **Parameter-free equal-weight standardization:**
   - **Regional FWR-Scaffold + CDR-Paratope Equal-Weight IMGT-Z (`CLSS_Reg8_AllBP_IMGT_Z`, `CLSS_Reg7_MW_IMGT_Z`, `CLSS_Reg7_IMGT_Z`, `CLSS_Reg6_IMGT_Z`):** Uses strictly equal weights (`1/8`, `1/7`, `1/7`, `1/6`) over the regional FWR scaffold folding descriptors (`fwr_flex`, `neg_fwr_gravy`, `neg_fwr_inst`), CDR paratope stickiness/electrostatic descriptors (`neg_cdr_arom`, `neg_cdr_pI`, `neg_cdr_chg`), `mw`, and `germ`.
   - **Whole-Chain Equal-Weight IMGT-Z (`CLSS_EqWt6_IMGT_Z`, `CLSS_EqWt6_Shrink_Z`, `CLSS_EqWt7_IMGT_Z`, `CLSS_EqWt5_NoPI_IMGT_Z`, `CLSS_EqWt4_Fold_IMGT_Z`):** Uses strictly equal weights (`1:1:...:1`) over the whole-chain intensive descriptors.
   - All descriptors are standardized strictly by the external $24 \times 18 = 432$ human IMGT germline Fv reference mean and standard deviation (`IMGT_MEAN`, `IMGT_STD`).

---

## 2. Clean-Room Execution & Runtime Verification

We re-executed `python3 claim/verify.py` from scratch on a single Apple M1 CPU core:

- **Exit Code:** `0`
- **Wall Time:** `13.92 s` (`< 15 s` threshold; matches the `14.69 s` recorded run within normal OS scheduling variance)
- **CPU Time:** `13.72 s` (`14.02 s` recorded)
- **Unique Antibody Pairs Scored & Cached:** `5,961` across `score/` and `data/thermostability/` (`6,405` total scored rows across the 35 non-binding developability datasets in `score/`).
- **Generated Per-Antibody Prediction Files:** All 35 non-binding developability datasets in `score/` (`15 tm + 6 polyreactivity + 6 aggregation + 7 expression + 1 immunogenicity = 35` CSV files under `claim/predictions/<category>/<dataset>_scores.csv`) were generated and verified non-empty with exact row-for-row sequence alignment (`heavy`, `light`, `clss_reg8_allbp_imgt_z`, `clss_reg7_mw_imgt_z`, `clss_reg6_imgt_z`, `clss_eqwt6_imgt_z`) against the raw FLAb `score/` files.

---

## 3. Independent Metric Recomputation (`claim/predictions/` vs Raw FLAb `score/`)

We independently loaded the generated per-antibody CSVs in `claim/predictions/` and the raw ground-truth `fitness` columns from the FLAb `score/` files and recomputed every per-dataset, unweighted category-mean, $N \ge 10$ mean, $\sqrt{N}$-weighted mean, and $N$-weighted mean Spearman rank correlation to 4 decimal places:

| Category (`score/`) | Method | Datasets ($D$) | Unweighted $\bar{\rho}$ | $\bar{\rho}_{N\ge 10}$ | $\bar{\rho}_{\sqrt{N}}$ | $\bar{\rho}_{N}$ | Positive Datasets | Max $\|\Delta\|$ vs `certificate.json` |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| **Thermostability (`tm`)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 15 | **`+0.4636`** | `+0.2106` | `+0.3001` | `+0.1666` | **`14/15` (`93.33%`)** | `0.0000` |
| **Thermostability (`tm`)** | **`CLSS_Reg7_MW_IMGT_Z`** | 15 | **`+0.5160`** | `+0.2272` | `+0.3426` | **`+0.1911`** | **`15/15` (`100.00%`)** | `0.0000` |
| **Thermostability (`tm`)** | **`CLSS_Reg6_IMGT_Z`** | 15 | **`+0.5365`** | `+0.2328` | `+0.3451` | `+0.1683` | **`14/15` (`93.33%`)** | `0.0000` |
| **Thermostability (`tm`)** | **`CLSS_EqWt6_IMGT_Z`** | 15 | **`+0.3528`** | **`+0.2470`** | `+0.2542` | `+0.1328` | `11/15` (`73.33%`) | `0.0000` |
| **Polyreactivity (`polyreactivity`)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | 6 | **`+0.4467`** | **`+0.2379`** | **`+0.3073`** | **`+0.2569`** | **`6/6` (`100.00%`)** | `0.0000` |
| **Polyreactivity (`polyreactivity`)** | **`CLSS_Reg7_MW_IMGT_Z`** | 6 | **`+0.3459`** | `+0.1867` | `+0.2297` | `+0.1870` | **`6/6` (`100.00%`)** | `0.0000` |
| **Polyreactivity (`polyreactivity`)** | **`CLSS_Reg6_IMGT_Z`** | 6 | **`+0.3185`** | `+0.1457` | `+0.2077` | `+0.1695` | **`6/6` (`100.00%`)** | `0.0000` |
| **Polyreactivity (`polyreactivity`)** | **`CLSS_EqWt6_IMGT_Z`** | 6 | **`+0.3987`** | `+0.2088` | `+0.2398` | `+0.1771` | **`6/6` (`100.00%`)** | `0.0000` |

### Null Batteries & Partial Wins (`p1`, `p2`, `p3`) Reproduction

- **Thermostability (`p1`, all 4 dataset universes):** All 4 universes (`15`-ds `score/tm`, `20`-ds `data/std`, `21`-ds `data/all`, and `25`-ds combined) reproduced to 4 decimal places (`CLSS_Reg7_MW_IMGT_Z`: `+0.5160`, `+0.3568`, `+0.3334`, `+0.3313`; `CLSS_Reg8_AllBP_IMGT_Z`: `+0.4636`, `+0.3270`, `+0.3048`, `+0.2834`).
- **Sign Consistency (`p2`, $\ge 80\%$):** Confirmed `15/15 = 100.0%` (`CLSS_Reg7_MW_IMGT_Z`) and `14/15 = 93.3%` (`CLSS_Reg8_AllBP_IMGT_Z`) on Thermostability, and `6/6 = 100.0%` across all Regional and Whole-Chain CLSS methods on Polyreactivity.
- **Length & Germline Confound Control (`p3`) & Two $B = 1,000$ Permutation Null Batteries (`seed = 20261026`):** Reproduced identically to 4 decimal places (`CLSS_Reg8_AllBP_IMGT_Z`: $Z = +3.46, p = 0.000999$ on `tm` and $Z = +3.76, p = 0.000999$ on `polyreactivity`, with `0/1,000` random permutations reaching the observed category mean on either category).

pass: true
