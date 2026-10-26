# The Record We Beat (`Graylab/FLAb` Released Zero-Shot Developability Scores)

- **Paper:** Michael Chungyoun & Jeffrey J. Gray, *"FLAb: Benchmarking deep learning methods for antibody fitness prediction"*, *bioRxiv* `10.64898/2025.12.27.696706` (Dec 2025).
- **Benchmark Repository URL:** `https://github.com/Graylab/FLAb`
- **Pinned Commit:** `e05e3f0135783ffb7de412df6a1467e7a0031911` (*"Fix sort direction for jetha and kraft datasets in aggregation README"*)
- **UTC Fetch Time:** `2026-10-26T00:17:00Z`
- **Fetched Status File (`README.md`) SHA-256:** `5a5184094ed4a13c64b1cb914a2168a58e3b16abe956b794a163888ec70996ff`

---

## Published / Released Zero-Shot Scores (`score/` Directory) vs Our Certified Zero-Shot Scores

| Category (`score/` universe) | Method | Unweighted Mean Spearman $\bar{\rho}$ | Positive Datasets (`>0`) | $\bar{\rho}_{N \ge 10}$ | $\sqrt{N}$-Weighted $\bar{\rho}_{\sqrt{N}}$ | $N$-Weighted $\bar{\rho}_{N}$ | `Wittrup2017_CST` ($N=137$) |
|---|---|---:|---:|---:|---:|---:|---:|
| **Thermostability (`score/tm`, 15 ds)** | `progen/xlarge` (`-ppl`, Best Released in `score/tm`) | `+0.2169` | `10/15` (`66.7%`) | `+0.0173` | `+0.0964` | `+0.0414` | `+0.0743` |
| **Thermostability (`score/tm`, 15 ds)** | `progen/oas` (`-ppl`, Best Ab PLM in `score/tm`) | `+0.1674` | `9/15` (`60.0%`) | `-0.0755` | `+0.0338` | `-0.0368` | `-0.0512` |
| **Thermostability (`score/tm`, 15 ds)** | `esmif` (`-ppl`, Best Inverse Folding in `score/tm`) | `+0.1394` | `9/15` (`60.0%`) | `+0.1800` | `+0.1427` | `+0.1882` | `+0.3516` |
| **Thermostability (`score/tm`, 15 ds)** | `iglm` (`-ppl`) | `+0.0184` | `8/15` (`53.3%`) | `-0.0354` | `-0.0261` | `-0.0514` | `-0.0540` |
| **Thermostability (`score/tm`, 15 ds)** | `antiberty` (`-ppl`) | `+0.0113` | `8/15` (`53.3%`) | `-0.0570` | `-0.0461` | `-0.0926` | `-0.1401` |
| **Thermostability (`score/tm`, 15 ds)** | `bp_flexibility` (Best Single Biopython Scale) | `+0.2908` | `11/15` (`73.3%`) | `+0.2511` | `+0.1954` | `+0.0630` | `-0.1454` |
| **Thermostability (`score/tm`, 15 ds)** | **`CLSS_EqWt6_IMGT_Z` (Ours, Whole-Chain `1/6`)** | **`+0.3528`** | `11/15` (`73.3%`) | **`+0.2470`** | **`+0.2542`** | **`+0.1328`** | `-0.0028` |
| **Thermostability (`score/tm`, 15 ds)** | **`CLSS_EqWt5_NoPI_IMGT_Z` (Ours, Whole-Chain `1/5`)** | **`+0.3980`** | **`12/15` (`80.0%`)** | **`+0.2789`** | **`+0.2927`** | **`+0.1630`** | **`+0.0196`** |
| **Thermostability (`score/tm`, 15 ds)** | **`CLSS_Reg8_AllBP_IMGT_Z` (Ours, Regional `1/8`)** | **`+0.4636`** | **`14/15` (`93.3%`)** | **`+0.2106`** | **`+0.3001`** | **`+0.1666`** | **`+0.0620`** |
| **Thermostability (`score/tm`, 15 ds)** | **`CLSS_Reg7_MW_IMGT_Z` (Ours, Regional `1/7`)** | **`+0.5160`** | **`15/15` (`100.0%`)** | **`+0.2272`** | **`+0.3426`** | **`+0.1911`** | **`+0.0598`** |
| **Thermostability (`score/tm`, 15 ds)** | **`CLSS_Reg6_IMGT_Z` (Ours, Regional `1/6`)** | **`+0.5365`** | **`14/15` (`93.3%`)** | **`+0.2328`** | **`+0.3451`** | **`+0.1683`** | **`+0.0160`** |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `mpnn` (`-ppl`, Best Released Confidence in `score/`) | `+0.1906` | `4/6` (`66.7%`) | `+0.1324` | `+0.1054` | `+0.0640` | `+0.0453` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `progen/xlarge` (`-ppl` / `+ppl`, Best Either Sign) | `-0.1936` / `+0.1936` | `1/6` / `5/6` | `-0.1868` | `-0.1771` | `-0.1705` | `-0.1677` / `+0.1677` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `pyrosetta` (`-score`) | `+0.1123` | `3/6` (`50.0%`) | `+0.0721` | `+0.0510` | `+0.0211` | `+0.0074` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `esmif` (`-ppl`) | `+0.1026` | `4/6` (`66.7%`) | `+0.0467` | `+0.0896` | `+0.0860` | `+0.0865` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | `neg_bp_isoelectric_point` (Best Single Biopython Scale) | `+0.4354` | `6/6` (`100.0%`) | `+0.2510` | `+0.3179` | `+0.2755` | `+0.2631` |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | **`CLSS_Reg7_MW_IMGT_Z` (Ours, Regional `1/7`)** | **`+0.3459`** | **`6/6` (`100.0%`)** | **`+0.1867`** | **`+0.2297`** | **`+0.1870`** | **`+0.1735`** |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | **`CLSS_EqWt6_IMGT_Z` (Ours, Whole-Chain `1/6`)** | **`+0.3987`** | **`6/6` (`100.0%`)** | **`+0.2088`** | **`+0.2398`** | **`+0.1771`** | **`+0.1546`** |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | **`CLSS_Reg7_IMGT_Z` (Ours, Regional `1/7`)** | **`+0.4190`** | **`6/6` (`100.0%`)** | **`+0.1964`** | **`+0.2847`** | **`+0.2388`** | **`+0.2267`** |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | **`CLSS_Reg8_AllBP_IMGT_Z` (Ours, Regional `1/8`)** | **`+0.4467`** | **`6/6` (`100.0%`)** | **`+0.2379`** | **`+0.3073`** | **`+0.2569`** | **`+0.2418`** |
| **Polyreactivity (`score/polyreactivity`, 6 ds)** | **`CLSS_EqWt7_IMGT_Z` (Ours, Whole-Chain `1/7`)** | **`+0.5052`** | **`6/6` (`100.0%`)** | **`+0.3257`** | **`+0.3301`** | **`+0.2568`** | **`+0.2284`** |
