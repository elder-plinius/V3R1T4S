# Stage 4 Skeptic Audit — `NOVELTY` (`flab-antibody-developability-zero-shot`)

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Target ID:** `flab-antibody-developability-zero-shot`
- **Single Frozen Zero-Shot Method:** **`CLSS_Reg8_AllBP_IMGT_Z`** (frozen at `2026-10-26T00:26:00Z` in commit `654c23f056b932c310723f591bc3fec89102ad73`; see `how-we-built-it/PREREG.md`; all other composite variants reported strictly as exploratory ablations)
- **Claim Scope (`status: CONFIRMED_PARTIAL`):** **Partial Wins `p2` and `p3`** (Full Win, Binding, and `p1` are **not claimed**)
- **Audited Artifacts:**
  - `the-record-we-beat/target.md`
  - `the-record-we-beat/record.md`
  - `how-we-built-it/PREREG.md`
  - `how-we-built-it/artifact.md`
  - `how-we-built-it/null_test.md`
  - `README.md`
  - `object/certificate.json` (`sha256: b6be3abe5d0dcff18fcf18d8e7a16f64164d434290274613f79b76f80f598eb6`)
  - `object/predictions_tm_polyreactivity.csv` (`sha256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`)
  - `object/predictions_binding_part1..8.csv` (`sha256: 8e748b57...` through `f41772d0...`, `104,737` rows)
  - `verify-it-yourself/verify.py` (`sha256: 3583f9700c89ba0c00bf1d9eaaaaca0566166859880727be705d7b5acf8fbd18`)
  - `how-we-built-it/verify_full_benchmark.py` (`sha256: 51a3a05a27708532df677cb5c49043998eff57b8fa6edfc12a85b841f50dcf45`)
- **Audited Benchmark Repository:** `https://github.com/Graylab/FLAb` at commit `e05e3f0135783ffb7de412df6a1467e7a0031911`

---

## 1. Repository & Codebase Audit: Does `Graylab/FLAb` Already Compute `CLSS_Reg8_AllBP_IMGT_Z` or the `p3` Confound Decomposition?

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
     - the 8-descriptor regional equal-weight composite **`CLSS_Reg8_AllBP_IMGT_Z`**, or
     - rank-residualized partial Spearman ($\perp L$, $\perp G$, $\perp (L,G)$) and matched-stratum `(L_H, L_L, V_H_idx, V_L_idx)` confound controls (`p3`).

---

## 2. Audit of Claimed Partial Wins (`p2`, `p3`) and Non-Claimed Categories (`Binding`, `p1`, Full Win)

1. **Claimed Partial Win `p2` ($\ge 80\%$ Sign Consistency):**
   - **`CLSS_Reg8_AllBP_IMGT_Z`** achieves positive correlation on **`14/15 = 93.3%`** of `score/tm` datasets, **`16/20 = 80.0%`** of standard `data/thermostability` datasets, **`6/6 = 100.0%`** of `score/polyreactivity` datasets, and **`4/4 = 100.0%`** of untouched `data/expression` datasets (whereas no released model in `score/tm` or `score/polyreactivity` exceeds `66.7%` under standard `-ppl`).
2. **Claimed Partial Win `p3` (Length & Germline Confound Decomposition):**
   - The `p3` analysis in `how-we-built-it/null_test.md` §3 and `object/certificate.json` computes rank-residualized partial Spearman ($\perp L$, $\perp G$, $\perp (L,G)$) and exact matched-stratum Spearman ($\bar{\rho}_{\text{matched}}$) within `(L_H, L_L, V_H_idx, V_L_idx)` strata across all 12 released models, 9 single descriptors, and 10 CLSS parameter-free methods.
   - Explains mechanistically why sequence PLM perplexities (`antiberty`, `iglm`, `progen/*`) flip sign between Thermostability (`+0.1674` to `+0.2169`) and Polyreactivity (`-0.1424` to `-0.1936`): human IMGT germline identity correlates positively with thermostability ($+0.1297$) but negatively with favourable low polyreactivity ($-0.2129$).
   - Confirms that **`CLSS_Reg8_AllBP_IMGT_Z`** retains strong predictive power within exact length-and-germline-matched strata (**`+0.4308`** matched on `score/tm` and **`+0.5262`** matched on `score/polyreactivity`).
3. **Full Transparency on Non-Claimed Categories (`Binding`, `p1`, Full Win):**
   - **Binding (`score/binding` 16 datasets and `data/binding` 80 CSVs — not claimed):** Evaluated unchanged from commit `654c23f0`, `CLSS_Reg8_AllBP_IMGT_Z` achieves **`-0.0060`** (`+0.0060` for $+K_d$) on `score/binding` vs `iglm = 0.1742`, **`-0.0987`** across all `80` `data/binding` CSVs, **`-0.1123`** / **`-0.1640`** across the `12` / `15` `score/`-covered `data/binding` CSVs, **`-0.0964`** / **`-0.0837`** across the `68` / `65` excluded `data/binding` CSVs, and **`-0.0809`** across the `84`-dataset `score/binding` plus `data/binding` union.
   - **Thermostability (`p1` and Full Win — not claimed):** Because `CLSS_Reg8_AllBP_IMGT_Z` was defined at `00:13Z` after looking at `Wittrup2017_CST_Tm` in `score/tm`, `p1` and Full Win are marked as not claimed, and the 25-dataset figure (`+0.2834`) is explicitly labeled as the `score/tm` plus `data/thermostability` union.

---

## 3. Summary of Novelty Audit Checks

| Audit Criterion | Finding | Status |
|---|---|---|
| Absent from `Graylab/FLAb` (`score/`, `models/`, `examples/`)? | Confirmed: no FWR/CDR landmark partitioning, IMGT repertoire Z-standardization, 8-descriptor composite, or `p3` confound decomposition exists in `FLAb`. | **PASS** |
| Evaluated on `score/binding` (`16` datasets) and all `80` `data/binding` CSVs without modification from commit `654c23f0`? | Confirmed: all `104,737` binding predictions saved in `object/predictions_binding_part1..8.csv`, with `binding`, `p1`, and Full Win explicitly marked not claimed. | **PASS** |
| Claimed Partial Wins `p2` ($\ge 80\%$ sign consistency) and `p3` (length & germline confound control) novel & verified? | Confirmed for `CLSS_Reg8_AllBP_IMGT_Z`: `93.3%` (`14/15`) on `score/tm`, `80.0%` (`16/20`) on `data/thermostability`, `100.0%` (`6/6`) on `score/polyreactivity`, `100.0%` (`4/4`) on `data/expression`, and `+0.4308` / `+0.5262` matched-stratum Spearman. | **PASS** |

pass: true
