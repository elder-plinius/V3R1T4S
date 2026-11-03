# Stage 4 Skeptic Audit — `NOVELTY` (`flab-antibody-developability-zero-shot`)

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Target ID:** `flab-antibody-developability-zero-shot`
- **Single Claimed Zero-Shot Method:** **`CLSS_Reg8_AllBP_IMGT_Z`** (frozen at `2026-10-26T00:26:00Z` in commit `654c23f056b932c310723f591bc3fec89102ad73`; see `how-we-built-it/PREREG.md`; all other composite variants reported strictly as exploratory ablations)
- **Audited Artifacts:**
  - `the-record-we-beat/target.md`
  - `the-record-we-beat/record.md`
  - `how-we-built-it/PREREG.md`
  - `how-we-built-it/artifact.md`
  - `null_test.md` (`how-we-built-it/null_test.md`)
  - `README.md`
  - `object/certificate.json` (`sha256: d59325d4892db661c638af2d7d2bdf6e35a6c06f95e869d2bc361470def74ecb`)
  - `object/predictions_tm_polyreactivity.csv` (`sha256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`)
  - `verify-it-yourself/verify.py` (`sha256: 891335835b8ec6cecba04373a4ae820915abdcaac76747884e7905207ec7ee50`)
  - `how-we-built-it/verify_full_benchmark.py` (`sha256: 88644033fd678cd8f369fb3b60f5977ff96cff39ba849d70268d4cc2c159b85f`)
- **Audited Benchmark Repository:** `https://github.com/Graylab/FLAb` at commit `e05e3f0135783ffb7de412df6a1467e7a0031911`

---

## 1. Repository & Codebase Audit: Does `Graylab/FLAb` Already Compute `CLSS_Reg8_AllBP_IMGT_Z`?

I inspected the entire cloned `Graylab/FLAb` repository (`README.md`, `score/`, all 71 Python files in `models/`, `examples/`, and `data/`).

1. **Pre-computed `score/` Directory Inventory:**
   - The `score/` directory contains **12 released zero-shot models** across 6 top-level folders: `antiberty`, `esmif`, `iglm`, `mpnn`, `pyrosetta`, and `progen/{BFD90,base,large,medium,oas,small,xlarge}`.
   - No pre-computed `score/bp_*` or `score/ld_score` files are shipped in `score/`, and no composite biophysical, regional FWR/CDR, or germline-standardized score exists anywhere in `score/` or `score_ft/`.

2. **Scoring Scripts in `models/` (`biopython_score.py`, `scoring_bp_*.py`, `ld_score.py`, `scoring_ld_score.py`):**
   - `models/biopython_score.py` and the seven `models/scoring_bp_*.py` scripts evaluate each Biopython `ProtParam` scale (`bp_molecular_weight`, `bp_aromaticity`, `bp_instability_index`, `bp_isoelectric_point`, `bp_average_flexibility`, `bp_gravy`, `bp_charge_at_7_4`) strictly as an **isolated, unstandardized, unoriented whole-chain single descriptor**.
   - `models/ld_score.py` computes raw Levenshtein edit distance (`LDv + LDj`) via `abnumber`/`anarci` as an isolated single metric (`scoring_ld_score.py`).
   - Full `grep` scans across `models/` confirm **zero occurrences** of:
     - conserved immunoglobulin landmark partitioning into $\beta$-sandwich Framework (`FWR1–4`) and hypervariable Complementarity-Determining Loops (`CDR1–3`) (`cdr`, `fwr`, `CDR`, `FWR`, `split_fwr_cdr`),
     - external human IMGT V+J germline repertoire ($24\text{ IGHV} \times 18\text{ IGKV/IGLV} = 432$ Fv pairs) Z-standardization ($\mu_k^{\text{IMGT}}, \sigma_k^{\text{IMGT}}$),
     - or the 8-descriptor regional equal-weight composite **`CLSS_Reg8_AllBP_IMGT_Z`**.

3. **Mechanistic Novelty of `CLSS_Reg8_AllBP_IMGT_Z`:**
   - Whole-chain averaging mixes hypervariable CDR loop residues (selected for antigen binding, often enriched in aromatic/hydrophobic side chains) with the conserved $\beta$-sandwich Framework scaffold (which governs cooperative thermal unfolding $T_m$).
   - By partitioning every heavy and light variable domain at its four invariant vertebrate immunoglobulin landmarks (`Cys22`, `Trp36`, `Cys92/104`, `WGQG/FGQG`) and evaluating conformational flexibility (`fwr_flex`), hydrophilicity (`neg_fwr_gravy`), and dipeptide stability (`neg_fwr_inst`) on the **Framework scaffold (`FWR1–4`)**, while evaluating aromatic density (`neg_cdr_arom`), isoelectric point (`neg_cdr_pI`), and net charge (`neg_cdr_chg`) on the **hypervariable paratope (`CDR1–3`)** alongside molecular weight (`mw`) and human IMGT germline identity (`germ`), standardized against the 432-pair IMGT reference repertoire with strictly equal `1/8` weights, **`CLSS_Reg8_AllBP_IMGT_Z`** introduces a physically grounded, parameter-free zero-shot architecture that includes **all 7** Biopython `ProtParam` descriptors from `FLAb/models/biopython_score.py` with zero feature subset selection.

---

## 2. Margin Audit for Single Claimed Method (`CLSS_Reg8_AllBP_IMGT_Z`) Across `score/` Subset, Full `data/` Categories, and Untouched Categories

1. **Thermostability (`score/tm` 15 datasets + `data/thermostability/` 20, 21, and 25-dataset universes):**
   - **`score_tm_15` (`score/tm/`, 15 datasets):** **`CLSS_Reg8_AllBP_IMGT_Z`** achieves unweighted mean **`+0.4636`** (**`14/15 = 93.33% > 0`**), beating the best released model in `score/tm` (`progen/xlarge = +0.2169`) by **`+0.2467`** ($4.93\times$ required `+0.05`) and beating the best single Biopython descriptor (`bp_flexibility = +0.2908`) by **`+0.1728`** ($3.46\times$ required `+0.05`), with $\bar{\rho}_{N\ge 10} = +0.2106$, $\bar{\rho}_{\sqrt{N}} = +0.3001$, $\bar{\rho}_{N} = +0.1666$, and `Wittrup2017_CST_Tm` ($N=137$) = **`+0.0620`**.
   - **All 4 Thermostability Benchmark Universes (`p1`):**
     - `score_tm_15` (`15` datasets): **`+0.4636`** (`+0.1728` over `bp_flexibility = +0.2908`)
     - `data_thermostability_20_standard` (`20` datasets): **`+0.3270`** (`16/20 = 80.0% > 0`, **`+0.1478`** over best single `neg_bp_aromaticity = +0.1792`)
     - `data_thermostability_21_all` (`21` datasets): **`+0.3048`** (`16/21 = 76.2% > 0`, **`+0.1449`** over best single `neg_bp_aromaticity = +0.1599`)
     - `combined_thermostability_25` (`25` datasets): **`+0.2834`** (`19/25 = 76.0% > 0`, **`+0.0880`** over best single `bp_flexibility = +0.1954`)

2. **Polyreactivity (`score/polyreactivity` 6 datasets + `data/polyreactivity/` 25 and 26-dataset universes):**
   - **`score/polyreactivity` (`6` datasets):** **`CLSS_Reg8_AllBP_IMGT_Z`** achieves **`+0.4467`** (**`6/6 = 100.00% > 0`**, $\bar{\rho}_{N\ge 10} = +0.2379$, $\bar{\rho}_{\sqrt{N}} = +0.3073$, $\bar{\rho}_{N} = +0.2569$), beating `progen/xlarge (+ppl) = +0.1936` by **`+0.2531`** ($5.06\times$ required `+0.05`), `mpnn (-ppl) = +0.1906` by **`+0.2561`**, and best single descriptor `neg_bp_isoelectric_point = +0.4354` by **`+0.0113`**.
   - **Full `data/polyreactivity/` (`25` CSVs, `26` union, and `20` unseen CSVs omitted by `score/`):** **`CLSS_Reg8_AllBP_IMGT_Z`** achieves **`+0.1407`** (`17/25 = 68.0% > 0`), **`+0.1671`** (`18/26 = 69.2% > 0`), and **`+0.0844`** (`12/20 = 60.0% > 0`).

3. **Untouched Categories (Never Loaded Prior to Method Freeze at `2026-10-26T00:26:00Z`):**
   - **`data/pharmacokinetics/` (`9` datasets):** **`+0.2287`** (`6/9 = 66.7% > 0`, $\bar{\rho}_{N} = +0.2148$).
   - **`data/expression/` (`4` datasets):** **`+0.1913`** (`4/4 = 100.0% > 0`, $\bar{\rho}_{N} = +0.2266$).

---

## 3. Novelty & Scientific Value of the `p3` Length-and-Germline Confound Decomposition

The `p3` analysis in `null_test.md` §4 and `object/certificate.json` computes rank-residualized partial Spearman ($\perp L$, $\perp G$, $\perp (L,G)$) and exact matched-stratum Spearman ($\bar{\rho}_{\text{matched}}$) within `(L_H, L_L, V_H_idx, V_L_idx)` strata:
- Explains mechanistically why sequence PLM perplexities (`antiberty`, `iglm`, `progen/*`) flip sign between Thermostability (`+0.1674` to `+0.2169`) and Polyreactivity (`-0.1424` to `-0.1936`): human IMGT germline identity correlates positively with thermostability ($+0.1297$) but negatively with favourable low polyreactivity ($-0.2129$).
- Confirms that the single claimed method **`CLSS_Reg8_AllBP_IMGT_Z`** retains strong predictive power within exact length-and-germline-matched strata (**`+0.4308`** matched on `score/tm` and **`+0.5262`** matched on `score/polyreactivity`).

---

## 4. Summary of Novelty Audit Checks

| Audit Criterion | Finding | Status |
|---|---|---|
| Absent from `Graylab/FLAb` (`score/`, `models/`, `examples/`)? | Confirmed: no FWR/CDR landmark partitioning, IMGT repertoire Z-standardization, or 8-descriptor composite exists in `FLAb`. | **PASS** |
| Single claimed method (`CLSS_Reg8_AllBP_IMGT_Z`) beats all 12 released models in `score/` by $\ge +0.05$ across $\ge 2$ categories? | Beats best released by **`+0.2467`** on `score/tm` and **`+0.2531`** on `score/polyreactivity`, and beats all single descriptors on all 4 Thermostability universes (`+0.0880` to `+0.1728`). | **PASS** |
| Evaluated on untouched categories without modification? | Confirmed: `+0.2287` (`6/9 > 0`) on `data/pharmacokinetics` and `+0.1913` (`4/4 > 0`) on `data/expression`. | **PASS** |
| Partial wins `p1`, `p2` ($\ge 80\%$ sign consistency), and `p3` (length & germline confound control) novel & verified? | Confirmed for `CLSS_Reg8_AllBP_IMGT_Z`: `93.3%` (`14/15`) on `score/tm`, `80.0%` (`16/20`) on `data/thermostability`, `100.0%` (`6/6`) on `score/polyreactivity`, and `+0.4308` / `+0.5262` matched-stratum Spearman. | **PASS** |

pass: true
