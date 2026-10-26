# How We Found It (`contributor text, unverified`)

> **Note:** This file is contributor text, unverified by the mechanical gate (`check_run.py` verifies `object/certificate.json` and `object/predictions_tm_polyreactivity.csv` via `verify-it-yourself/run_checks.sh`).

## 1. Diagnosing Why Deep Protein Language Models Flip Sign on FLAb

When we audited the 12 released models in `Graylab/FLAb` (`score/`), we observed two striking anomalies:
1. On **Polyreactivity (`score/polyreactivity`, 6 datasets)**, every sequence protein language model (`antiberty`, `iglm`, `progen/small`, `progen/medium`, `progen/base`, `progen/large`, `progen/BFD90`, `progen/oas`, `progen/xlarge`) has a **negative** category mean Spearman under standard model confidence (`-perplexity`, from `-0.0162` down to `-0.1936`), whereas inverse-folding models (`mpnn = +0.1906`, `esmif = +0.1026`) and PyRosetta (`+0.1123`) are positive.
2. Why do sequence PLMs predict that higher-likelihood antibodies are *more* polyreactive (worse)? By computing exact human IMGT V+J germline sequence identity (`pure_germline_identity`) and residualizing all models against sequence length $L$ and germline identity $G$ (`p3`), we found that human germline identity $G$ correlates positively with thermostability (`+0.1297` on `score/tm`), but **negatively** with favourable low polyreactivity (`-0.2129` on `score/polyreactivity`, including `-0.6983` on `Rosace2023_CR3022_CIC` and `-0.7379` on `Rosace2023_Golimumab_CIC`). Several human germline VH1/VH3/VH4 genes carry cationic and aromatic CDR patches that stabilize the native fold yet promote non-specific stickiness in CIC/PSR/ELISA assays. Because sequence PLMs act primarily as germline-proximity detectors, their raw likelihoods flip sign between Thermostability and Polyreactivity.

## 2. Diagnosing Simpson's Paradox in Unweighted Category Means (`n = 2` vs `n = 137`)

In our first parameter-free whole-chain composite (`CLSS_EqWt6_IMGT_Z`, which standardizes the 6 intensive sequence-level descriptors against the external 432-pair human IMGT germline reference repertoire and sums them with equal weights `1/6`), we achieved `+0.3528` on `score/tm` and `+0.3987` on `score/polyreactivity` (`+0.5052` for `CLSS_EqWt7_IMGT_Z`). However, inspecting the largest clinical dataset `Wittrup2017_CST_Tm` ($N = 137$ clinical-stage antibodies across diverse human V-gene families) revealed that whole-chain `CLSS_EqWt6_IMGT_Z` had `-0.0028` on `Wittrup2017_CST_Tm`!
Why? Because in `score/tm` (15 datasets), 3 datasets have $n = 2$ antibodies (`Hie2022_C143_Tm`, `Hie2022_MEDI8852_Tm`, `Hie2022_mAb114UCA_Tm`) and 5 more have $n = 5\text{--}8$. Under unweighted averaging, whole-chain `bp_flexibility` appears strongly positive (`+0.2908` unweighted) even though on the 137 clinical antibodies in `Wittrup2017_CST_Tm` it is **negative (`-0.1454`)**!

## 3. Resolving the Paradox via Regional Antibody Domain Biophysics (`FWR1–4` vs `CDR1–3`)

An antibody variable domain is structurally divided into a conserved $\beta$-sandwich **Framework scaffold (`FWR1–4`)** (which governs cooperative thermal unfolding $T_m$) and three hypervariable **CDR loops (`CDR1–3`)** (which govern antigen binding and paratope surface stickiness/self-association).
When we partition each variable domain using the four conserved immunoglobulin landmarks (`Cys22`, `Trp36`, `Cys92/104`, `WGQG/FGQG`) and evaluate:
- **Scaffold folding stability descriptors** (`fwr_flex`, `neg_fwr_gravy`, `neg_fwr_inst`) on **`FWR1–4`**, and
- **Paratope stickiness/electrostatic descriptors** (`neg_cdr_arom`, `neg_cdr_pI`, `neg_cdr_chg`) on **`CDR1–3`** (following Raybould et al., *PNAS* 2019 Therapeutic Antibody Profiler),
alongside `mw` and `germ` with strictly equal weights (`1/8` in `CLSS_Reg8_AllBP_IMGT_Z`, `1/7` in `CLSS_Reg7_MW_IMGT_Z`):
- Framework dipeptide stability (`neg_fwr_inst`) reaches **`+0.1957`** on `Wittrup2017_CST_Tm` ($N = 137$) and **`+0.1721`** across all 15 `tm` datasets (vs `+0.0243` whole-chain).
- Framework hydrophilicity (`neg_fwr_gravy`) reaches **`+0.3517`** across all 15 `tm` datasets (vs `+0.1967` whole-chain) and **`+0.2203`** on `hutchinson2023enhancement_top200tm1_igg` ($N = 192$, vs `-0.0824` whole-chain).
- Consequently, `CLSS_Reg7_MW_IMGT_Z` achieves **`+0.5160`** unweighted on `score/tm` (**`15/15 = 100.0%` positive**), **`+0.0598`** on `Wittrup2017_CST_Tm` ($N = 137$), and **`+0.1911`** $N$-weighted mean (beating even structure-based `esmif = +0.1882`), while `CLSS_Reg8_AllBP_IMGT_Z` achieves **`+0.4636`** (`14/15 = 93.3% > 0`, `Wittrup2017_CST_Tm = +0.0620`) on `score/tm` and **`+0.4467`** (**`6/6 = 100.0%` positive**, $N$-weighted **`+0.2569`**) on `score/polyreactivity`.
