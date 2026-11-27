# FLAb Antibody Developability Zero-Shot: Sequence-Only Regional Biophysical Z-Score Composite (CLSS_Reg8_AllBP_IMGT_Z — Partial Wins p2 & p3)

## What

Verified zero-shot sequence-only developability scoring on the FLAb therapeutic antibody benchmark (`Graylab/FLAb`, commit `e05e3f0135783ffb7de412df6a1467e7a0031911`, Chungyoun & Gray, bioRxiv 2025, `doi:10.64898/2025.12.27.696706`) claiming Partial Wins `p2` and `p3` only (with Full Win and `p1` not claimed): the single frozen sequence-only zero-shot formula `CLSS_Reg8_AllBP_IMGT_Z` (frozen at `2026-10-26T00:26:00Z` in commit `654c23f056b932c310723f591bc3fec89102ad73`, with zero assay-label fitting and all other composite rules reported strictly as exploratory ablations) achieves directional sign consistency (`p2`) of `14/15 = 93.3%` positive datasets on `score/tm` (mean Spearman $\rho = +0.4636$), `16/20 = 80.0%` on the 20 standard Fv `data/thermostability` datasets ($\rho = +0.3270$; $+0.3048$, `16/21 = 76.2%` across all 21 `data/thermostability` CSVs, and $+0.2834$, `20/25 = 80.0%` across the 25-dataset `score/tm` plus `data/thermostability` union), and `6/6 = 100.0%` on `score/polyreactivity` ($\rho = +0.4467$; $+0.1407$, `17/25 = 68.0%` across all 25 `data/polyreactivity` CSVs, and $+0.1671$, `18/26 = 69.2%` across the 26-dataset `score/polyreactivity` plus `data/polyreactivity` union), preserves within-stratum germline-and-length confound-controlled correlation (`p3`) of $\rho_{\text{matched}} = +0.4308$ on `score/tm` (`78` strata across `11` datasets) and $\rho_{\text{matched}} = +0.5262$ on `score/polyreactivity` (`61` strata across `4` datasets), and scores $\rho = -0.0060$ (`6/16 > 0` vs $-K_d$; $+0.0060$, `10/16 > 0` vs $+K_d$) on the 16 `score/binding` datasets (below `iglm` at $0.1742$) and $\rho = -0.0987$ (`36/80 > 0`; $-0.1123$ on the 12 primary `score/`-mapped CSVs, $-0.1640$ on the 15 study-mapped CSVs, $-0.0964$ on the 68 excluded CSVs, and $-0.0837$ on the 65 excluded CSVs) across all 80 `data/binding` CSVs (`97,778` rows), so `binding`, `thermostability`, `polyreactivity`, and `p1` are not claimed as category wins.

- **Target ID:** `flab-antibody-developability-zero-shot`
- **Submission ID:** `2026-10-26-mizopl-e1d0aaa2`
- **Status:** `CONFIRMED_PARTIAL` (`partial_win: p2, p3`; Full Win and `p1` not claimed)
- **Single Frozen Method:** `CLSS_Reg8_AllBP_IMGT_Z` (frozen at `2026-10-26T00:26:00Z` in commit `654c23f056b932c310723f591bc3fec89102ad73`; see `how-we-built-it/PREREG.md`)
- **Primary Object Files (`object/`, all $\le 1\text{ MB}$):**
  - `object/certificate.json` (`sha256: b6be3abe5d0dcff18fcf18d8e7a16f64164d434290274613f79b76f80f598eb6`, `609,170` bytes)
  - `object/predictions_tm_polyreactivity.csv` (`sha256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`, `417,060` bytes, `4,499` rows across `76` dataset evaluations for `tm`, `polyreactivity`, and `pharmacokinetics`)
  - `object/predictions_binding_part1.csv` (`sha256: 8e748b57b03ae4b59f8218f29f36c9ca953c24180ded58335ba362716067535c`, `894,791` bytes, `13,093` rows)
  - `object/predictions_binding_part2.csv` (`sha256: ba6c287e5b2b68005a7364e80fd35158d22ab28bc0f0cb1703d7a5008afb391c`, `909,107` bytes, `13,093` rows)
  - `object/predictions_binding_part3.csv` (`sha256: f34f344dd88ca9f87c664bcfe667685dcbac65957591f48b4220ae94f22cf3c7`, `862,391` bytes, `13,093` rows)
  - `object/predictions_binding_part4.csv` (`sha256: 34287e9f3492063ffefe6945c14675530b621eba63852bb3ac8f5d0c3aba750c`, `896,838` bytes, `13,093` rows)
  - `object/predictions_binding_part5.csv` (`sha256: 0dc9735f13bfde50d6ee20a49a5ad81627ffc30f79c869287b03eb4097eb0ab3`, `903,476` bytes, `13,093` rows)
  - `object/predictions_binding_part6.csv` (`sha256: 927068ffec0443c33ce4434fc2077db3e9665a2fca6738b1189329727ad7c5d3`, `892,366` bytes, `13,093` rows)
  - `object/predictions_binding_part7.csv` (`sha256: 52f106d72ed81d0a3e4b4795ebd004ada3d1881d2a3c81751b60a6a3606b76be`, `903,476` bytes, `13,093` rows)
  - `object/predictions_binding_part8.csv` (`sha256: f41772d054c180cb6f4dd900d615887973d0e16ee9909cc292cda986b306b912`, `879,686` bytes, `13,086` rows)
  - Total row-indexed predictions: **`109,236` rows across `172` dataset evaluations** (`4,499` rows in `predictions_tm_polyreactivity.csv` + `104,737` rows across `predictions_binding_part1..8.csv` covering all `16` `score/binding` datasets [`6,959` rows] and all `80` `data/binding` CSVs [`97,778` rows], with zero copied third-party sequences).

---

## Check it yourself

From this package folder (`known-knowns/flab-antibody-developability-zero-shot/2026-10-26-mizopl-e1d0aaa2/`), run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line:** `PASS`
- **Rough laptop time:** `~1.5s` (offline verification of `object/certificate.json`, `object/predictions_tm_polyreactivity.csv`, `object/predictions_binding_part1..8.csv` [`109,236` rows], and all `190` upstream FLAb data-file SHA-256 commitments; full from-scratch re-evaluation from `Graylab/FLAb` commit `e05e3f0135783ffb7de412df6a1467e7a0031911` via `python3 how-we-built-it/verify_full_benchmark.py` takes `~46s` on Apple Silicon M-series CPU).

---

## Binding Evaluation (`data/binding` 80 CSVs & `score/binding` 16 Datasets — Not Claimed)

At pinned commit `e05e3f0135783ffb7de412df6a1467e7a0031911`, `Graylab/FLAb` contains `80` CSV files in `data/binding/` (`97,778` total rows) and `16` dataset directories in `score/<model>/binding/` (`6,959` total rows). Neither `data/binding/` nor `score/binding/` was inspected when `CLSS_Reg8_AllBP_IMGT_Z` was frozen at commit `654c23f056b932c310723f591bc3fec89102ad73`. Running the frozen `CLSS_Reg8_AllBP_IMGT_Z` rule unchanged across all `binding` datasets yields:

| Binding Evaluation Universe | Datasets ($N$) | Total Variants ($n$) | Frozen `CLSS_Reg8_AllBP_IMGT_Z` Mean $\rho$ (Unweighted) | Positive Datasets ($\rho > 0$) | Size-Weighted $\rho$ ($n \ge 10$ / $\sqrt{n}$ / $n$) | Best Released Model in `score/binding` | Margin vs Best Released | Claimed? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **`score/binding` (`16` datasets, favorable $-K_d$)** | 16 | 6,959 | **`-0.0060`** | `6/16 (37.5%)` | `-0.0671 / -0.0070 / +0.0058` | `iglm (+ppl)` (`+0.1742`) | `-0.1802` | **No** |
| **`score/binding` (`16` datasets, raw $+K_d$)** | 16 | 6,959 | **`+0.0060`** | `10/16 (62.5%)` | `+0.0671 / +0.0070 / -0.0058` | `iglm (-ppl)` (`+0.1742`) | `-0.1682` | **No** |
| **All `data/binding` CSVs (`80` datasets, `README.md` $\uparrow$)** | 80 | 97,778 | **`-0.0987`** | `36/80 (45.0%)` | `-0.0990 / -0.0889 / -0.0725` | — | — | **No** |
| **`data/binding` standard-header CSVs (`77` datasets)** | 77 | 89,922 | **`-0.1012`** | `35/77 (45.5%)` | `-0.1015 / -0.0969 / -0.0842` | — | — | **No** |
| **`data/binding` primary `score/`-mapped subset (`12` CSVs)** | 12 | 6,987 | **`-0.1123`** | `5/12 (41.7%)` | `-0.1134 / -0.0561 / +0.0051` | — | — | **No** |
| **`data/binding` study-level `score/`-mapped subset (`15` CSVs)** | 15 | 7,024 | **`-0.1640`** | `5/15 (33.3%)` | `-0.1456 / -0.0793 / +0.0030` | — | — | **No** |
| **`data/binding` excluded by `score/binding` (`68` CSVs vs 12 mapped)** | 68 | 90,791 | **`-0.0964`** | `31/68 (45.6%)` | `-0.0966 / -0.0928 / -0.0785` | — | — | **No** |
| **`data/binding` excluded by `score/binding` (`65` CSVs vs 15 mapped)** | 65 | 90,754 | **`-0.0837`** | `31/65 (47.7%)` | `-0.0888 / -0.0902 / -0.0783` | — | — | **No** |
| **`score/binding` plus `data/binding` Union (`84` datasets)** | 84 | 97,729 | **`-0.0809`** | `37/84 (44.0%)` | `-0.0913 / -0.0846 / -0.0724` | — | — | **No** |

### Recomputed Released Baselines on `score/binding` (`16` Datasets)

In `score/<model>/binding/`, the `fitness` column stores raw dissociation constants $K_d$ (where lower $K_d$ indicates stronger binding, i.e., `sgn = -1` for $-K_d$, whereas `data/binding/` transforms those overlapping datasets to $-\log_{10} K_d$ so higher `fitness` indicates stronger binding). Across all `12` released model directories in `score/*/binding/`:

| Released Model / Method | Datasets ($N$) | Mean $\rho$ (`-ppl` vs $-K_d$) | Mean $\rho$ (`+ppl` vs $-K_d$ / `-ppl` vs $+K_d$) | Best Sign Mean $|\rho|$ | Positive Datasets (`+ppl` vs $-K_d$) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `iglm` | 16 | `-0.1742` | **`+0.1742`** | **`0.1742`** | `12/16 (75.0%)` |
| `progen/base` | 16 | `-0.1575` | `+0.1575` | `0.1575` | `12/16 (75.0%)` |
| `progen/BFD90` | 16 | `-0.1481` | `+0.1481` | `0.1481` | `12/16 (75.0%)` |
| `progen/oas` | 16 | `-0.1422` | `+0.1422` | `0.1422` | `13/16 (81.2%)` |
| `progen/xlarge` | 16 | `-0.1421` | `+0.1421` | `0.1421` | `11/16 (68.8%)` |
| `pyrosetta` | 16 | `+0.1379` (`-score`) | `-0.1379` (`+score`) | `0.1379` | `12/16 (75.0%)` (`-score`) |
| `progen/large` | 16 | `-0.1215` | `+0.1215` | `0.1215` | `11/16 (68.8%)` |
| `antiberty` | 16 | `-0.1169` | `+0.1169` | `0.1169` | `11/16 (68.8%)` |
| `progen/medium` | 16 | `-0.0943` | `+0.0943` | `0.0943` | `9/16 (56.2%)` |
| `progen/small` | 16 | `-0.0616` | `+0.0616` | `0.0616` | `9/16 (56.2%)` |
| `mpnn` | 16 | `+0.0106` | `-0.0106` | `0.0106` | `9/16 (56.2%)` (`-ppl`) |
| `esmif` | 14 | `-0.0066` | `+0.0066` | `0.0066` | `8/14 (57.1%)` |
| **`CLSS_Reg8_AllBP_IMGT_Z` (Frozen)** | 16 | **`-0.0060`** (vs $-K_d$) | **`+0.0060`** (vs $+K_d$) | `0.0060` | `6/16` (vs $-K_d$) / `10/16` (vs $+K_d$) |

Because `CLSS_Reg8_AllBP_IMGT_Z` (`-0.0060` vs $-K_d$, `+0.0060` vs $+K_d$ on `score/binding`; `-0.0987` across all 80 `data/binding` CSVs) does not beat `iglm` (`0.1742`), **we do not claim `binding`**.

### Mapping Between `score/binding` (`16` Datasets) and `data/binding` (`80` CSVs) & Excluded Datasets

1. **12 Primary `data/binding` CSVs Covered by `score/binding` (`data_binding_12_score_mapped`, mean $\rho = -0.1123$):**
   - 11 one-to-one datasets: `hie2023efficient_CoV2Beta_C143_Kd.csv` (`Hie2022_C143_Kd`), `hie2023efficient_MEDIUCA_H1Solomon_Kd.csv` (`Hie2022_MEDI8852UCA_Kd`), `hie2023efficient_MEDI_H4Hubei_Kd.csv` (`Hie2022_MEDI8852_Kd`), `hie2023efficient_CoV2Beta_REGN10987_Kd.csv` (`Hie2022_REGN10987_Kd`), `hie2023efficient_CoV2_S309_Kd.csv` (`Hie2022_S309_Kd`), `hie2023efficient_ebola_mab114_Kd.csv` (`Hie2022_mAb114_Kd`), `koenig2017mutational_kd_g6.csv` (`Koenig2017_g6_Kd`), `rosace2023automated_kd_adalimumab.csv` (`Rosace2023_Adalimumab_Kd`), `rosace2023automated_kd_golimumab.csv` (`Rosace2023_Golimumab_Kd`), `shanehsazzadeh2023unlocking_zerokd_trastuzumab.csv` (`Shanehsazzadeh2023_trastuzumab_zero_kd`), and `warszawski2019_d44_Kd.csv` (`Warszawski2019_d44_Kd`).
   - 1 pooled GSK dataset: `garbinski2023_kd.csv` (`n = 81`), which pools `gsk2023_AM14_Kd` (`n = 29`), `gsk2023_D25_Kd` (`n = 22`), and `gsk2023_MOTA_Kd` (`n = 11`) from `score/binding/` together with `19` rows of `RSB1`.
2. **3 Secondary Viral-Strain CSVs from Hie et al. 2023 (`data_binding_15_score_family_mapped` = 12 + 3 = 15 CSVs, mean $\rho = -0.1640$):**
   - `hie2023efficient_MEDIUCA_H4Hubei_Kd.csv`, `hie2023efficient_MEDI_H7HK16_Kd.csv`, `hie2023efficient_CoV2omicron_REGN10987_Kd.csv`.
3. **2 Datasets Present in `score/binding/` Only (No `data/binding/` CSV):**
   - `Rosace2023_CR3022_Kd` (`n = 6`) and `Shanehsazzadeh2023_trastuzumab_multi_kd` (`n = 24`).
4. **68 `data/binding` CSVs Excluded by the Released `score/binding` Protocol (`unseen_data_binding_68_excluded_by_score`, mean $\rho = -0.0964$; or `65` CSVs excluding the 3 secondary Hie 2023 strains, mean $\rho = -0.0837$):**
   - `adams2017measuring_4420-fluorescein_kd-titeseq.csv`, `birtalan2008contributions_4d5_her2_kd.csv`, `birtalan2010functional_4d5_her2_kd.csv`, `boder2000directed_4-4-20_fluorescein_kd.csv`, `bostrom2009variants_bH1_her2_kd.csv`, `bostrom2009variants_bH1_vegf_kd.csv`, `chen1999selection_y0101_vegf_fab-kd.csv`, `cognano_AVIDa-hTNFa.csv` (uses `VHH_sequence`), `dyson2020beyond_12_igg-fetch.csv`, `dyson2020beyond_7_fetch.csv`, `fennell2010cdr_A2_tnfa_ic50.csv`, `forsyth2013mabs_13_hu4D5-8_her2_kd.csv`, `fujino2012in_F5111_il2_kd.csv`, `gai2007yeast_scfv_kd.csv`, `gerstner2002adp_4d5_her2_kd.csv`, `hashimoto2010engineering_2E8_k562_ec50.csv`, `hie2023efficient_CoV2omicron_REGN10987_Kd.csv` (in 68-list only), `hie2023efficient_MEDIUCA_H4Hubei_Kd.csv` (in 68-list only), `hie2023efficient_MEDI_H7HK16_Kd.csv` (in 68-list only), `hutchinson2023enhancement_multikd_igg.csv`, `hutchinson2023enhancement_singlekd_igg.csv`, `hutchinson2023enhancement_top200kd_igg.csv`, `hutchinson2023enhancement_top27kd_igg.csv`, `jain2023identifying_CHO.csv`, `jain2023identifying_EXPI.csv`, `jain2023identifying_OVA.csv`, `jain2024assessment_Affinity_wt.csv`, `kelley1993antigen_4d5_her2_kd.csv`, `kirby2024retrospective_ab-SARSCoV2_binary_kd.csv` (fitness column `KD [bind/no bind]`), `kirby2024retrospective_ab-SARSCoV2_kd.csv` (fitness column `Kd [M]`), `koenig2015deep_g6_vegf_kd.csv`, `kuroda2012computer_12_kd.csv`, `lee2004high_bH1_her2_kd.csv`, `lee2004high_bH1_vegf_kd.csv`, `li2016in_6_okt3_cd3_kd.csv`, `lippow2007computational_10_d44.1_lysozyme_kd.csv`, `lippow2007computational_4_cetuximab_egfr_kd.csv`, `lippow2007computational_b9_lysozyme_kd.csv`, `makowski2022cooptimization_binary.csv`, `makowski2022cooptimization_continuous.csv`, `mason2021optimization_trastuzumab_her2_binary.csv`, `midelfort2004substantial_d1.3_lysozyme_kd.csv`, `miller2019stability_2_scfv_ec50.csv`, `muller1998model_y0317_vegf_kd.csv`, `near1993in_26-10_digoxin_kd.csv`, `nicolaou2020cooperative_3_m396_sars_kd.csv`, `oh2023affinity_11_scfv_ec50.csv`, `peterson2024integrated_ab_H1HA_binary.csv`, `peterson2024integrated_ab_H1HA_kd.csv`, `phillips2021binding_cr6261_h1_kd.csv`, `phillips2021binding_cr6261_h9_kd.csv`, `phillips2021binding_cr9114_b_kd.csv`, `phillips2021binding_cr9114_h1_kd.csv`, `phillips2021binding_cr9114_h3_kd.csv`, `pierce2014conformational_2_d44.1_lysozyme_kd.csv`, `pons1999energetic_d1.3_lysozyme_kd.csv`, `rajpal2005general_d2e7_tnfa_kd.csv`, `rawat2022abcov_ic50.csv`, `rawat2022abcov_kd.csv`, `saka2021antibody_kynurenine_ec50.csv`, `schier1996isolation_c6.5_erbb2_kd.csv`, `shanehsazzadeh2023unlocking_adcc_ec50.csv`, `shanehsazzadeh2023unlocking_kd_hher2_fab.csv`, `shanehsazzadeh2023unlocking_kd_hher2_mab.csv`, `shanker2024unsupervised_Binding_Elotuzumab-Ixekuzimab.csv`, `shanker2024unsupervised_Binding_Ly1404.csv`, `shanker2024unsupervised_Binding_SA58.csv`, and `tharakaraman2013redesign_4e10_hiv_kd.csv`.

---

## Compared to

- **Table / Benchmark Source:** `https://github.com/Graylab/FLAb` (pinned commit `e05e3f0135783ffb7de412df6a1467e7a0031911`; Chungyoun & Gray, bioRxiv 2025, `doi:10.64898/2025.12.27.696706`)
- **Fetched UTC:** `2026-10-25T23:42:08Z`
- **Claimed Scope:** **Partial Wins `p2` and `p3` only** (`status: CONFIRMED_PARTIAL`; Full Win and `p1` not claimed).

### 1. Summary Across All 6 `score/` Categories + Full `data/` Categories (`CLSS_Reg8_AllBP_IMGT_Z`)

| Category & Evaluation Universe | Datasets ($N$) | Total Variants ($n$) | Best Released Model (`score/`) | Best Single Biopython / Germline Descriptor | Frozen `CLSS_Reg8_AllBP_IMGT_Z` Mean $\rho$ (Unweighted) | Positive Datasets ($\rho > 0$) | Claimed Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Thermostability (`score/tm` subset)** | 15 | 2,167 | `progen/xlarge (-ppl)` / `iglm (-ppl)` (`+0.2169`) | `bp_flexibility` (`+0.2429`) | **`+0.4636`** | **`14/15 (93.3%)`** | **`p2` & `p3` only** (Full Win & `p1` not claimed) |
| **Thermostability (`data/thermostability` standard Fv)** | 20 | 956 | — | `bp_flexibility` (`+0.1945`) | **`+0.3270`** | **`16/20 (80.0%)`** | **`p2` only** (`p1` not claimed) |
| **Thermostability (`data/thermostability` all CSVs)** | 21 | 1,093 | — | `bp_flexibility` (`+0.1815`) | **`+0.3048`** | `16/21 (76.2%)` | Not claimed (`p1` not claimed) |
| **Thermostability (`score/tm` plus `data/thermostability` union, 25 datasets)** | 25 | 2,424 | — | `bp_flexibility` (`+0.1954`) | **`+0.2834`** | **`20/25 (80.0%)`** | Not claimed (`p1` not claimed) |
| **Thermostability (unseen `data/thermostability` omitted by `score/tm`)** | 11 | 440 | — | `pure_germline_identity` (`+0.0954`) | **`+0.1190`** | `6/11 (54.5%)` | Not claimed (`p1` not claimed) |
| **Polyreactivity (`score/polyreactivity` subset)** | 6 | 561 | `progen/xlarge (+ppl)` / `esmif (-ppl)` (`+0.1936`) | `neg_bp_isoelectric_point` (`+0.2512`) | **`+0.4467`** | **`6/6 (100.0%)`** | **`p2` & `p3` only** (Full Win not claimed) |
| **Polyreactivity (`data/polyreactivity` all CSVs)** | 25 | 2,265 | — | `neg_bp_isoelectric_point` (`+0.1605`) | **`+0.1407`** | `17/25 (68.0%)` | Not claimed |
| **Polyreactivity (`score/polyreactivity` plus `data/polyreactivity` union, 26 datasets)** | 26 | 2,272 | — | `neg_bp_isoelectric_point` (`+0.1846`) | **`+0.1671`** | `18/26 (69.2%)` | Not claimed |
| **Polyreactivity (unseen `data/polyreactivity` omitted by `score/polyreactivity`)** | 20 | 1,711 | — | `neg_bp_isoelectric_point` (`+0.1538`) | **`+0.0844`** | `12/20 (60.0%)` | Not claimed |
| **Binding (`score/binding` subset, favorable $-K_d$)** | 16 | 6,959 | `iglm (+ppl)` (`+0.1742`) | `neg_bp_gravy` (`+0.1544`) | **`-0.0060`** | `6/16 (37.5%)` | Not claimed |
| **Binding (`data/binding` all CSVs, `README.md` $\uparrow$)** | 80 | 97,778 | — | `bp_molecular_weight` (`+0.0230`) | **`-0.0987`** | `36/80 (45.0%)` | Not claimed |
| **Pharmacokinetics (`data/pharmacokinetics` all CSVs)** | 9 | 785 | — (no `score/` dir) | `neg_bp_charge_at_7_4` (`+0.2896`) | **`+0.2287`** | `6/9 (66.7%)` | Not claimed (no `score/` baselines) |
| **Expression (`data/expression` all CSVs)** | 4 | 596 | — | `pure_germline_identity` (`+0.1695`) | **`+0.1913`** | `4/4 (100.0%)` | Not claimed |
| **Aggregation (`score/aggregation`)** | 6 | 749 | `esmif (-ppl)` (`+0.2847`) | `neg_bp_gravy` (`+0.2280`) | `+0.2143` | `5/6 (83.3%)` | Not claimed (`-0.0704` below `esmif`) |
| **Expression (`score/expression`)** | 7 | 6,162 | `progen/small (-ppl)` (`+0.1509`) | `bp_instability_index` (`+0.0972`) | `-0.0445` | `3/7 (42.9%)` | Not claimed (`-0.1954` below `progen/small`) |
| **Immunogenicity (`score/immunogenicity`)** | 1 | 217 | `progen/oas (-ppl)` (`+0.5200`) | `pure_germline_identity` (`+0.5553`) | `+0.1726` | `1/1 (100.0%)` | Not claimed (`-0.3474` below `progen/oas`) |

---

### 2. Claimed Partial Win `p2` ($\ge 80\%$ Directional Sign Consistency)

- **`score/tm` (`15` datasets):** `CLSS_Reg8_AllBP_IMGT_Z` achieves **`14/15 = 93.3%`** positive Spearman correlations (`mean = +0.4636`), exceeding the `80%` (`12/15`) threshold.
- **`data/thermostability` (`20` standard Fv datasets):** `CLSS_Reg8_AllBP_IMGT_Z` achieves **`16/20 = 80.0%`** positive correlations (`mean = +0.3270`), and **`20/25 = 80.0%`** (`mean = +0.2834`) across the **`25`-dataset `score/tm` plus `data/thermostability` union** (`16/21 = 76.2%`, `mean = +0.3048` when the single-domain VHH dataset `sulea2019assisted_sdAb_tm.csv` is included in the 21-CSV `data/thermostability` set).
- **`score/polyreactivity` (`6` datasets):** `CLSS_Reg8_AllBP_IMGT_Z` achieves **`6/6 = 100.0%`** positive correlations (`mean = +0.4467`), exceeding every released model (best released sign consistency is `4/6 = 66.7%`).

---

### 3. Claimed Partial Win `p3` (Germline & Sequence-Length Confound Control)

Controlling simultaneously for exact `(L_H, L_L, V_germline, L_germline)` matched strata (`78` strata across `11` multi-variant `score/tm` datasets; `61` strata across `4` multi-variant `score/polyreactivity` datasets) and via rank-based partial Spearman correlation $\rho_{\perp (L,G)}$:

| Category | Method | Role | Raw Unadjusted $\rho$ | Partial $\rho_{\perp L}$ (Length) | Partial $\rho_{\perp G}$ (Germline) | Partial $\rho_{\perp (L,G)}$ (Both) | Within-Stratum Matched $\rho_{\text{matched}}$ |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`score/tm` ($N = 15$)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Claimed Primary** | **`+0.4636`** | **`+0.3910`** | **`+0.4158`** | **`+0.3694`** | **`+0.4308`** |
| `score/tm` ($N = 15$) | `progen/xlarge (-ppl)` | Released Baseline | `+0.1763` | `+0.1930` | `+0.0445` | `+0.0369` | `+0.2193` |
| `score/tm` ($N = 15$) | `antiberty (-ppl)` | Released Baseline | `+0.1306` | `+0.0878` | `+0.0145` | `-0.0155` | `+0.0725` |
| **`score/polyreactivity` ($N = 6$)** | **`CLSS_Reg8_AllBP_IMGT_Z`** | **Claimed Primary** | **`+0.4467`** | **`+0.4716`** | **`+0.4494`** | **`+0.4706`** | **`+0.5262`** |
| `score/polyreactivity` ($N = 6$) | `esmif (-ppl)` | Released Baseline | `+0.1936` | `+0.2586` | `+0.2427` | `+0.2512` | `+0.2463` |
| `score/polyreactivity` ($N = 6$) | `progen/xlarge (-ppl)` | Released Baseline | `-0.1936` | `-0.1469` | `-0.2462` | `-0.2233` | `-0.1194` |

---

## Not Claimed

1. **No Full Win (`CONFIRMED_SOLUTION`) on any FLAb category:**
   - **Thermostability (`score/tm` & `data/thermostability`) and Partial Win `p1` are NOT claimed:** `CLSS_Reg8_AllBP_IMGT_Z` was defined at `2026-10-26T00:13:00Z` after inspecting per-dataset results on `Wittrup2017_CST_Tm` in `score/tm`. The 25-dataset thermostability figure (`+0.2834`, `20/25 = 80.0%` positive) is the **`score/tm` plus `data/thermostability` union** (`21` CSVs in `data/thermostability/` plus `5` datasets in `score/tm/` only, with the 4 `gsk2023_*_Tm` splits replacing pooled `garbinski2023_tm1.csv`).
   - **Polyreactivity (`score/polyreactivity` & `data/polyreactivity`) is NOT claimed as a Full Win:** its predecessor `CLSS_EqWt6_IMGT_Z` had been scored on `score/polyreactivity` at `2026-10-25T23:51:00Z`, before the `CLSS_Reg8_AllBP_IMGT_Z` rule was chosen.
   - **Binding (`score/binding` & `data/binding`) is NOT claimed:** `CLSS_Reg8_AllBP_IMGT_Z` achieves `-0.0060` (`6/16 > 0` vs $-K_d$) / `+0.0060` (`10/16 > 0` vs $+K_d$) on `score/binding` (below `iglm` at `0.1742` by `-0.1802` / `-0.1682`) and `-0.0987` (`36/80 > 0`) across all `80` `data/binding` CSVs (`-0.1123` on the 12 primary `score/`-mapped CSVs, `-0.1640` on the 15 study-mapped CSVs, `-0.0964` on the 68 excluded CSVs, and `-0.0837` on the 65 excluded CSVs).
   - **Aggregation, Expression, Immunogenicity, and Pharmacokinetics are NOT claimed:** on `score/aggregation`, `score/expression`, and `score/immunogenicity`, `CLSS_Reg8_AllBP_IMGT_Z` is `-0.0704`, `-0.1954`, and `-0.3474` below the best released method, and `pharmacokinetics` (`+0.2287` across 9 `data/pharmacokinetics` CSVs) has no `score/` files.
2. **Exploratory ablations are not claimed:** all other composite variants (`CLSS_Reg7_MW_IMGT_Z`, `CLSS_Reg7_IMGT_Z`, `CLSS_Reg6_IMGT_Z`, `CLSS_EqWt6_IMGT_Z`, `CLSS_EqWt6_Shrink_Z`, `CLSS_EqWt7_IMGT_Z`, `CLSS_EqWt5_NoPI_IMGT_Z`, `CLSS_EqWt5_NoPI_Shrink_Z`, `CLSS_EqWt4_Fold_IMGT_Z`) are reported in `object/certificate.json` strictly as exploratory ablations (`role = "exploratory_ablation"`).

---

## Credits

- **FLAb Benchmark & Released Baseline Scores:** Michael Chungyoun and Jeffrey J. Gray (*"FLAb: Benchmarking deep learning methods for antibody fitness prediction"*, bioRxiv 2025, `doi:10.64898/2025.12.27.696706`; repository: `https://github.com/Graylab/FLAb`, commit `e05e3f0135783ffb7de412df6a1467e7a0031911`).
- **Biopython `ProtParam` Scales:** Peter J. A. Cock et al. (*"Biopython: freely available Python tools for computational molecular biology and bioinformatics"*, *Bioinformatics* 2009), Kyte & Doolittle (1982), Guruprasad et al. (1990), Vihinen et al. (1994), and Bjellqvist et al. (1993).
- **IMGT Human Immunoglobulin Germline Repertoire & Numbering:** Marie-Paule Lefranc et al. (*"IMGT unique numbering for immunoglobulin and T cell receptor variable domains and Ig superfamily V-like domains"*, *Dev. Comp. Immunol.* 2003).
