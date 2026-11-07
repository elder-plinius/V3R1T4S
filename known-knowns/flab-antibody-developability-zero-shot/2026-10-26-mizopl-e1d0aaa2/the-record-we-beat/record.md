# The Record We Beat (`Graylab/FLAb` Released Zero-Shot Developability Scores)

- **Paper:** Michael Chungyoun & Jeffrey J. Gray, *"FLAb: Benchmarking deep learning methods for antibody fitness prediction"*, *bioRxiv* `10.64898/2025.12.27.696706` (Dec 2025).
- **Benchmark Repository URL:** `https://github.com/Graylab/FLAb`
- **Pinned Commit (`Graylab/FLAb`):** `e05e3f0135783ffb7de412df6a1467e7a0031911` (*"Fix sort direction for jetha and kraft datasets in aggregation README"*)
- **UTC Fetch Time:** `2026-10-26T00:17:00Z`
- **Fetched Upstream `Graylab/FLAb/README.md` SHA-256:** `5a5184094ed4a13c64b1cb914a2168a58e3b16abe956b794a163888ec70996ff`
- **Single Frozen Zero-Shot Method:** **`CLSS_Reg8_AllBP_IMGT_Z`** (frozen at `2026-10-26T00:26:00Z` in commit `654c23f056b932c310723f591bc3fec89102ad73`; see [`how-we-built-it/PREREG.md`](../how-we-built-it/PREREG.md); all other composite rules are reported strictly as exploratory ablations).
- **Claim Scope (`status: CONFIRMED_PARTIAL`):** **Partial Wins `p2` and `p3`** (Full Win, Binding, and `p1` are **not claimed**).

---

## 1. Released Zero-Shot Scores (`score/` Subset) vs Single Frozen Method (`CLSS_Reg8_AllBP_IMGT_Z`) and Exploratory Ablations

| Category (`score/` universe) | Method | Role | Unweighted Mean Spearman $\bar{\rho}$ | Positive Datasets (`>0`) | $\bar{\rho}_{N \ge 10}$ | $\sqrt{N}$-Weighted $\bar{\rho}_{\sqrt{N}}$ | $N$-Weighted $\bar{\rho}_{N}$ | `Wittrup2017_CST` ($N=137$) |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **Thermostability (`score/tm`, 15 ds; `p1` not claimed)** | `progen/xlarge` (`-ppl`, Best Released in `score/tm`) | Released Baseline | `+0.2169` | `10/15` (`66.7%`) | `+0.0173` | `+0.0964` | `+0.0414` | `+0.0743` |
| **Thermostability (`score/tm`, 15 ds)** | `progen/oas` (`-ppl`, Best Ab PLM in `score/tm`) | Released Baseline | `+0.1674` | `9/15` (`60.0%`) | `-0.0755` | `+0.0338` | `-0.0368` | `-0.0512` |
| **Thermostability (`score/tm`, 15 ds)** | `esmif` (`-ppl`, Best Inverse Folding in `score/tm`) | Released Baseline | `+0.1394` | `9/15` (`60.0%`) | `+0.1800` | `+0.1427` | `+0.1882` | `+0.3516` |
| **Thermostability (`score/tm`, 15 ds)** | `iglm` (`-ppl`) | Released Baseline | `+0.0184` | `8/15` (`53.3%`) | `-0.0354` | `-0.0261` | `-0.0514` | `-0.0540` |
| **Thermostability (`score/tm`, 15 ds)** | `antiberty` (`-ppl`) | Released Baseline | `+0.0113` | `8/15` (`53.3%`) | `-0.0570` | `-0.0461` | `-0.0926` | `-0.1401` |
| **Thermostability (`score/tm`, 15 ds)** | `bp_flexibility` (Best Single Biopython Scale) | Single Descriptor | `+0.2908` | `11/15` (`73.3%`) | `+0.2511` | `+0.1954` | `+0.0630` | `-0.1454` |
| **Thermostability (`score/tm`, 15 ds)** | **`CLSS_Reg8_AllBP_IMGT_Z` (Regional `1/8`, All 7 BP + `germ`)** | **Single Frozen Method** | **`+0.4636`** | **`14/15` (`93.3%`)** | **`+0.2106`** | **`+0.3001`** | **`+0.1666`** | **`+0.0620`** |
| **Thermostability (`score/tm`, 15 ds)** | `CLSS_EqWt6_IMGT_Z` (Whole-Chain `1/6`) | Exploratory Ablation | `+0.3528` | `11/15` (`73.3%`) | `+0.2470` | `+0.2542` | `+0.1328` | `-0.0028` |
| **Thermostability (`score/tm`, 15 ds)** | `CLSS_EqWt5_NoPI_IMGT_Z` (Whole-Chain `1/5`) | Exploratory Ablation | `+0.3980` | `12/15` (`80.0%`) | `+0.2789` | `+0.2927` | `+0.1630` | `+0.0196` |
| **Thermostability (`score/tm`, 15 ds)** | `CLSS_Reg7_MW_IMGT_Z` (Regional `1/7`) | Exploratory Ablation | `+0.5160` | `15/15` (`100.0%`) | `+0.2272` | `+0.3426` | `+0.1911` | `+0.0598` |
| **Thermostability (`score/tm`, 15 ds)** | `CLSS_Reg6_IMGT_Z` (Regional `1/6`) | Exploratory Ablation | `+0.5365` | `14/15` (`93.3%`) | `+0.2328` | `+0.3451` | `+0.1683` | `+0.0160` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `mpnn` (`-ppl`, Best Released Confidence in `score/`) | Released Baseline | `+0.1906` | `4/6` (`66.7%`) | `+0.1324` | `+0.1054` | `+0.0640` | `+0.0453` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `progen/xlarge` (`-ppl` / `+ppl`, Best Either Sign) | Released Baseline | `-0.1936` / `+0.1936` | `1/6` / `5/6` | `-0.1868` | `-0.1771` | `-0.1705` | `-0.1677` / `+0.1677` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `pyrosetta` (`-score`) | Released Baseline | `+0.1123` | `3/6` (`50.0%`) | `+0.0721` | `+0.0510` | `+0.0211` | `+0.0074` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `esmif` (`-ppl`) | Released Baseline | `+0.1026` | `4/6` (`66.7%`) | `+0.0467` | `+0.0896` | `+0.0860` | `+0.0865` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `neg_bp_isoelectric_point` (Best Single Biopython Scale) | Single Descriptor | `+0.4354` | `6/6` (`100.0%`) | `+0.2510` | `+0.3179` | `+0.2755` | `+0.2631` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | **`CLSS_Reg8_AllBP_IMGT_Z` (Regional `1/8`, All 7 BP + `germ`)** | **Single Frozen Method** | **`+0.4467`** | **`6/6` (`100.0%`)** | **`+0.2379`** | **`+0.3073`** | **`+0.2569`** | **`+0.2418`** |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `CLSS_Reg7_MW_IMGT_Z` (Regional `1/7`) | Exploratory Ablation | `+0.3459` | `6/6` (`100.0%`) | `+0.1867` | `+0.2297` | `+0.1870` | `+0.1735` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `CLSS_EqWt6_IMGT_Z` (Whole-Chain `1/6`) | Exploratory Ablation | `+0.3987` | `6/6` (`100.0%`) | `+0.2088` | `+0.2398` | `+0.1771` | `+0.1546` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `CLSS_Reg7_IMGT_Z` (Regional `1/7`) | Exploratory Ablation | `+0.4190` | `6/6` (`100.0%`) | `+0.1964` | `+0.2847` | `+0.2388` | `+0.2267` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `CLSS_EqWt7_IMGT_Z` (Whole-Chain `1/7`) | Exploratory Ablation | `+0.5052` | `6/6` (`100.0%`) | `+0.3257` | `+0.3301` | `+0.2568` | `+0.2284` |
| **Binding (`score/binding`, 16 ds; not claimed)** | `iglm` (`-ppl` vs $-K_d$ / `+ppl` vs $+K_d$, Best Released) | Released Baseline | `+0.1742` / `-0.1742` | `10/16` / `6/16` | `-0.1180` | `-0.0258` | `+0.0282` | — |
| **Binding (`score/binding`, 16 ds; not claimed)** | `progen/oas` (`-ppl` vs $-K_d$) | Released Baseline | `+0.1644` | `11/16` (`68.8%`) | `+0.0110` | `+0.0442` | `+0.0246` | — |
| **Binding (`score/binding`, 16 ds; not claimed)** | `pyrosetta` (`-score` vs $-K_d$) | Released Baseline | `+0.1547` | `9/13` (`69.2%`) | `+0.0725` | `+0.1455` | `+0.1869` | — |
| **Binding (`score/binding`, 16 ds; not claimed)** | `bp_molecular_weight` (Best Single Biopython Scale) | Single Descriptor | `+0.2314` | `10/14` (`71.4%`) | `+0.2848` | `+0.2738` | `+0.2862` | — |
| **Binding (`score/binding`, 16 ds; not claimed)** | **`CLSS_Reg8_AllBP_IMGT_Z` (vs $-K_d$ / vs $+K_d`)** | **Single Frozen Method** | **`-0.0060`** / **`+0.0060`** | `6/16` / `10/16` | `-0.0038` | `-0.0017` | `+0.0058` | — |

---

## 2. Full-Category (`data/`) vs `score/`-Subset Breakdown and Untouched Categories (`CLSS_Reg8_AllBP_IMGT_Z`)

| Category & Dataset Universe | Datasets ($D$) | `CLSS_Reg8_AllBP_IMGT_Z` Mean $\bar{\rho}$ | Positive Datasets (`>0`) | Best Single / Released | Margin vs Best Single / Released |
|---|---:|---:|---:|---|---:|
| **Thermostability (`score/tm` subset; `p1` not claimed)** | `15` | **`+0.4636`** | **`14/15` (`93.3%`)** | `bp_flexibility` (`+0.2908`) / `progen/xlarge` (`+0.2169`) | `+0.1728` / `+0.2467` |
| **Thermostability (`data/thermostability` standard; `p1` not claimed)** | `20` | **`+0.3270`** | **`16/20` (`80.0%`)** | `neg_bp_aromaticity` (`+0.1792`) | `+0.1478` |
| **Thermostability (`data/thermostability` all CSVs; `p1` not claimed)** | `21` | **`+0.3048`** | **`16/21` (`76.2%`)** | `neg_bp_aromaticity` (`+0.1599`) | `+0.1449` |
| **Thermostability (`score/tm` plus `data/thermostability` union; `p1` not claimed)** | `25` | **`+0.2834`** | **`19/25` (`76.0%`)** | `bp_flexibility` (`+0.1954`) | `+0.0880` |
| **Polyreactivity (`score/polyreactivity` subset)** | `6` | **`+0.4467`** | **`6/6` (`100.0%`)** | `neg_bp_isoelectric_point` (`+0.4354`) / `progen/xlarge (+ppl)` (`+0.1936`) | `+0.0113` / `+0.2531` |
| **Polyreactivity (`data/polyreactivity` all CSVs)** | `25` | **`+0.1407`** | **`17/25` (`68.0%`)** | `neg_bp_isoelectric_point` (`+0.1731`) | `-0.0324` |
| **Polyreactivity (`score/polyreactivity` plus `data/polyreactivity` union)** | `26` | **`+0.1671`** | **`18/26` (`69.2%`)** | `neg_bp_isoelectric_point` (`+0.2007`) | `-0.0336` |
| **Polyreactivity (`20` unseen `data/` CSVs omitted by `score/`)** | `20` | **`+0.0844`** | **`12/20` (`60.0%`)** | `neg_bp_isoelectric_point` (`+0.1233`) | `-0.0389` |
| **Binding (`score/binding` subset, vs $-K_d$ / vs $+K_d$; not claimed)** | `16` | **`-0.0060`** / **`+0.0060`** | `6/16` (`37.5%`) / `10/16` (`62.5%`) | `iglm` (`+0.1742`) / `bp_molecular_weight` (`+0.2314`) | `-0.1802` / `-0.1682` |
| **Binding (`data/binding` all 80 CSVs; not claimed)** | `80` | **`-0.0987`** | `36/80` (`45.0%`) | `bp_flexibility` (`+0.0725`) | `-0.1712` |
| **Binding (`data/binding` 77 standard-header CSVs; not claimed)** | `77` | **`-0.1012`** | `35/77` (`45.5%`) | `bp_flexibility` (`+0.0789`) | `-0.1801` |
| **Binding (`data/binding` 12 primary `score/`-mapped CSVs; not claimed)** | `12` | **`-0.1123`** | `5/12` (`41.7%`) | `bp_flexibility` (`+0.1518`) | `-0.2641` |
| **Binding (`data/binding` 15 study-mapped CSVs; not claimed)** | `15` | **`-0.1640`** | `5/15` (`33.3%`) | `bp_flexibility` (`+0.1795`) | `-0.3435` |
| **Binding (`data/binding` 68 excluded CSVs vs 12-CSV map; not claimed)** | `68` | **`-0.0964`** | `31/68` (`45.6%`) | `bp_flexibility` (`+0.0585`) | `-0.1549` |
| **Binding (`data/binding` 65 excluded CSVs vs 15-CSV map; not claimed)** | `65` | **`-0.0837`** | `31/65` (`47.7%`) | `bp_flexibility` (`+0.0478`) | `-0.1315` |
| **Binding (`score/binding` plus `data/binding` union; not claimed)** | `84` | **`-0.0809`** | `37/84` (`44.0%`) | `bp_flexibility` (`+0.0764`) | `-0.1573` |
| **Untouched Category: `data/pharmacokinetics` (no `score/` files)** | `9` | **`+0.2287`** | **`6/9` (`66.7%`)** | `neg_bp_charge_at_7_4` (`+0.2738`) | `-0.0451` |
| **Untouched Category: `data/expression`** | `4` | **`+0.1913`** | **`4/4` (`100.0%`)** | `bp_flexibility` (`+0.3037`) | `-0.1124` |
