# Skeptic Audit — Stage 4: CRITERION (`panel/criterion.md`)

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Target ID:** `flab-antibody-developability-zero-shot` (*"FLAb antibody developability: beat the released zero-shot scores on a therapeutic-property category"*)
- **Auditor Role:** Independent V3R1T4S Skeptic `CRITERION` (`CONSTITUTION v19` Stage 4)
- **Single Frozen Zero-Shot Method:** **`CLSS_Reg8_AllBP_IMGT_Z`** (frozen at `2026-10-26T00:26:00Z` in commit `654c23f056b932c310723f591bc3fec89102ad73`; see `how-we-built-it/PREREG.md`; all other composite variants reported strictly as exploratory ablations)
- **Claim Scope (`status: CONFIRMED_PARTIAL`):** **Partial Wins `p2` and `p3`** (Full Win, Binding, and `p1` are **not claimed**)
- **Audited Files & SHA-256 Commitments:**
  - `the-record-we-beat/target.md`
  - `verify-it-yourself/verify.py` (`sha256: 3583f9700c89ba0c00bf1d9eaaaaca0566166859880727be705d7b5acf8fbd18`)
  - `how-we-built-it/verify_full_benchmark.py` (`sha256: 51a3a05a27708532df677cb5c49043998eff57b8fa6edfc12a85b841f50dcf45`)
  - `object/certificate.json` (`sha256: b6be3abe5d0dcff18fcf18d8e7a16f64164d434290274613f79b76f80f598eb6`)
  - `object/predictions_tm_polyreactivity.csv` (`sha256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`, `4,499` rows across `76` dataset evaluations, `0` sequence columns)
  - `object/predictions_binding_part1..8.csv` (`sha256: 8e748b57...` through `f41772d0...`, `104,737` rows across `96` binding dataset evaluations: `16` `score/binding` + `80` `data/binding`, `0` sequence columns)
  - `how-we-built-it/PREREG.md`
  - `how-we-built-it/artifact.md`
  - `how-we-built-it/null_test.md`
  - `README.md`

---

## 1. Line-by-Line Audit of `target.md` Confirmation Criteria & Pre-Registration Timeline (`how-we-built-it/PREREG.md`)

| Requirement / Review Criterion | Audit Method & Evidence | Verified Value / Status |
|---|---|---|
| **1. Per-antibody predictions keyed by dataset and row index (with no third-party sequence redistribution)** | Inspected `object/predictions_tm_polyreactivity.csv` (`4,499` rows across `76` dataset evaluations: `score/tm` [`15`], `score/polyreactivity` [`6`], `data/thermostability` [`21`], `data/polyreactivity` [`25`], `data/pharmacokinetics` [`9`]) and `object/predictions_binding_part1..8.csv` (`104,737` rows across `96` binding dataset evaluations: `score/binding` [`16` datasets, `6,959` rows] and `data/binding` [`80` CSVs, `97,778` rows]). Confirmed zero `heavy` or `light` sequence columns (`embeds_third_party_sequences = false`) and contiguous `0..N-1` row indexing matching `Graylab/FLAb` commit `e05e3f0135783ffb7de412df6a1467e7a0031911`. | **100% coverage (`109,236` rows across `172` dataset evaluations, `0` copied sequence columns) — PASS** |
| **2. Single frozen method (`commit 654c23f0`) evaluated unchanged on `data/binding` and `score/binding`** | Verified that `CLSS_Reg8_AllBP_IMGT_Z` (frozen at commit `654c23f0`) was evaluated unchanged across all `16` `score/binding` datasets (`6,959` rows) and all `80` `data/binding` CSVs (`97,778` rows):<ul><li>`score/binding` (`16` datasets): **`-0.0060`** (`6/16 = 37.5% > 0`, $N$-weighted `+0.0058`) vs $-K_d$, or **`+0.0060`** (`10/16 = 62.5% > 0`) vs $+K_d$, vs best released `iglm = 0.1742` (`margin = -0.1802` for $-K_d$, `-0.1682` for $+K_d`).</li><li>All `80` `data/binding` CSVs: **`-0.0987`** (`36/80 = 45.0% > 0`; `-0.1012` [`35/77 > 0`] on the 77 standard-header CSVs).</li><li>`score/`-covered `data/binding` subset: **`-0.1123`** (`5/12 = 41.7% > 0`) on the `12` primary mapped CSVs; **`-0.1640`** (`5/15 = 33.3% > 0`) on the `15` study-mapped CSVs.</li><li>Excluded `data/binding` subset (all `68` / `65` excluded CSVs listed in `README.md` and `object/certificate.json`): **`-0.0964`** (`31/68 = 45.6% > 0`) / **`-0.0837`** (`31/65 = 47.7% > 0`).</li><li>`score/binding` plus `data/binding` union (`84` datasets): **`-0.0809`** (`37/84 = 44.0% > 0`).</li></ul>Because `CLSS_Reg8_AllBP_IMGT_Z` does not beat `iglm` (`0.1742`) by $\ge 0.05$, **Binding is not claimed**. | **Binding fully evaluated, reported, and marked not claimed — PASS** |
| **3. Category & `p1` claim scope aligned with `PREREG.md`** | Verified in `panel/gate.md` (`status: CONFIRMED_PARTIAL`, `claim_type: partial_win`, `partial_win: p2, p3`) and `README.md` that:<ul><li>Thermostability (`p1` and main category claim) is marked **not claimed** because `CLSS_Reg8_AllBP_IMGT_Z` was defined at `00:13Z` after looking at per-dataset results on `Wittrup2017_CST_Tm` in `score/tm`, and the `'25 datasets'` figure (`+0.2834`) is explicitly labeled as the **`score/tm` plus `data/thermostability` union**.</li><li>Polyreactivity is marked **not claimed** as a Full Win because `CLSS_EqWt6_IMGT_Z` had been scored on `score/polyreactivity` at `23:51Z`.</li><li>Aggregation (`-0.0704`), Expression (`-0.1954`), Immunogenicity (`-0.3474`), Pharmacokinetics (no `score/` files), and Binding (`-0.1802` vs `iglm`) are marked **not claimed**.</li></ul> | **Full Win, Binding, and `p1` marked not claimed; `25 datasets` labeled as `score/tm` plus `data/thermostability` union — PASS** |

---

## 2. Audit of Claimed Partial Wins (`p2`, `p3`) for Single Frozen Method `CLSS_Reg8_AllBP_IMGT_Z`

### Partial Win `p1`: Thermostability on a Laptop CPU (`NOT CLAIMED`)
- **Status:** **NOT CLAIMED** (`CLSS_Reg8_AllBP_IMGT_Z` was defined at `00:13Z` after inspecting `Wittrup2017_CST_Tm` in `score/tm`; the 25-dataset figure `+0.2834` is labeled as the `score/tm` plus `data/thermostability` union).

### Partial Win `p2`: Positively Correlated on $\ge 80\%$ of Datasets in a Category (`CLAIMED`)
- **Audit Findings:** The single frozen method **`CLSS_Reg8_AllBP_IMGT_Z`** is positively correlated on **`14/15 = 93.3%`** of `score/tm` datasets, **`16/20 = 80.0%`** of standard `data/thermostability/` datasets, **`6/6 = 100.0%`** of `score/polyreactivity` datasets, and **`4/4 = 100.0%`** of untouched `data/expression/` datasets (all $\ge 80\%$).
- **Status:** **`p2` CONFIRMED (`PASS`)**.

### Partial Win `p3`: Reproducible Length & Germline Confound Control (`CLAIMED`)
- **Audit Findings:** Within exact length-and-germline-matched strata `(L_H, L_L, V_H_idx, V_L_idx)`, the single frozen method **`CLSS_Reg8_AllBP_IMGT_Z`** achieves **`+0.4308`** matched-stratum Spearman on Thermostability (`+0.2184` partial $\perp (L,G)$) and **`+0.5262`** on Polyreactivity (`+0.4474` partial $\perp (L,G)$), with full rank-residualized partial Spearman ($\perp L$, $\perp G$, $\perp (L,G)$) and matched-stratum Spearman reported across all 12 released models, 9 single descriptors, and 10 CLSS parameter-free methods in `object/certificate.json`.
- **Status:** **`p3` CONFIRMED (`PASS`)**.

---

## 3. `K12` Digit-for-Digit Consistency Audit

Every numerical value and SHA-256 hash across `README.md`, `how-we-built-it/null_test.md`, `how-we-built-it/PREREG.md`, `how-we-built-it/artifact.md`, `the-record-we-beat/record.md`, and `verify-it-yourself/RECEIPTS.md` matches `object/certificate.json` (`sha256: b6be3abe5d0dcff18fcf18d8e7a16f64164d434290274613f79b76f80f598eb6`), `object/predictions_tm_polyreactivity.csv` (`sha256: 63cf82e9994c98a2dd2a69b47ff154b5ea9344fbfca0c4535ab11626ad0d7a9e`), and `object/predictions_binding_part1..8.csv` (`sha256: 8e748b57...` through `f41772d0...`) digit-for-digit (`0` discrepancies).

VERDICT: PASS
pass: true
