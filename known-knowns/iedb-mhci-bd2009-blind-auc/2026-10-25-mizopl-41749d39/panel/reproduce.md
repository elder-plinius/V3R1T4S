context: isolated Antigravity subagent cca5fb65-98f3-45d5-a731-f2e6712856d3 (V3R1T4S Skeptic REPRODUCE)
target_id: iedb-mhci-bd2009-blind-auc
run_id: 2026-10-25-2115

# Skeptic 1 (`REPRODUCE`) Verification Report — `iedb-mhci-bd2009-blind-auc` (`PARTIAL_PROGRESS`: `p1`, `p2`, `p3`)

- **Run ID:** `2026-10-25-2115`
- **Target ID:** `iedb-mhci-bd2009-blind-auc`
- **Claimed Verdict:** `PARTIAL_PROGRESS` (`p1`: `iedb-mhci-small-allele-blind-auc`, `p2`: `iedb-mhci-cv-blind-optimism-gap-shrink`, `p3`: `iedb-mhci-bd2013-leakage-quantification`)
- **Python Interpreter Used:** `python3` (`3.11`, `numpy`, `scipy`, `scikit-learn`)

---

## 1. Checksum & Standalone Verifier Audit (`SHA256SUMS` & `verify.py`)

Executed inside `claim/` (and `verify-it-yourself/`):
```bash
shasum -a 256 -c SHA256SUMS
python3 verify.py
```

- **`shasum -a 256 -c SHA256SUMS`:**
  - `bd2009_blind_certificate.json: OK` (`41749d395512d1d02975bfa03c861bbdb93c57c7dd9f1df95414751d3b2a6046`)
  - `blind_predictions.npz: OK` (`c59c21de2b11786e78973fbf9ebdc85737b6b6770f19cc34e777345cba79d2dc`)
- **`verify.py` Output:** Completed in `< 0.5 s` with exit code `0` and output `VERIFIED: PASS` / `PASS`.
- **Zero-Contamination Firewall Hashes (`bd2009_blind_certificate.json` vs disk):** All 7 raw benchmark files in `bd2009_blind_certificate.json` match the exact SHA-256 digests on disk (`bdata.2009.mhci.public.1.txt = 261df865af42db48f11600e56235224c168b505e302270d290a28ebb62cc08f1`, `bdata.2013.mhci.public.blind.1.txt = ab15f0480f1e2c08cefacd9f2832e0263b4ab05a176c8da774c9172d7264d768`, `bdata.2009.mhci.public.1.cv_rnd.txt = a510694eb6b7d2250462738f7bd7c9e42e2e1461a1254d100ab2d4358071925c`, `bdata.20130222.mhci.public.1.txt = 772d4aab7a1ecfea15e908348f4c11d4214a8888c304af46dda9e13882081d0e`, `table.cv_features.updated.auc.netmhc.xls = 9d603c41bbd362b4b02b8763a0f61ce25273f539432a7f7a805d533fbd3da6df`, `table.cv_features.updated.auc.netmhcpan.xls = 04a5d08b12787d151884a04c160d699a4521f894952374ee4a92006220059ed1`, `table.cv_features.updated.auc.smmpmbec_cpp.xls = 2ee58f77469963aeabb67e828299d07613acbed82b944233231906347fae91fd`).

---

## 2. Independent Verification of the 87 Blind Datasets & Reference Tables

Using an independent Python verification script reading directly from `binding/blind.1/bdata.2013.mhci.public.blind.1.txt` and `data/table.cv_features.updated.auc.{netmhc,netmhcpan,smmpmbec_cpp}.xls`:

| Check | Expected / Certificate | Independently Recomputed | Discrepancies |
| :--- | :---: | :---: | :---: |
| Total `Blind` datasets (`(allele, length)` pairs) | `87` | `87` | `0 / 87` |
| Total `Blind` rows across 87 datasets (`sum(size_bl)`) | `26,861` | `26,861` | `0 / 87` |
| Total `Blind` binders (`meas < 500.0 nM`, `sum(size_bl_binder)`) | `9,213` | `9,213` | `0 / 87` |
| Exact per-peptide binary label match (`y_raw == npz["{i}_y"]`) | `87 / 87` | `87 / 87` | `0 / 87` |
| `NetMHC` 87-dataset mean `Blind` ROC-AUC | `0.883322` | `0.883322` | `0 / 87` |
| `NetMHCpan` 87-dataset mean `Blind` ROC-AUC | `0.883048` | `0.883048` | `0 / 87` |
| `SMM-PMBEC` 87-dataset mean `Blind` ROC-AUC | `0.847389` | `0.847389` | `0 / 87` |
| **CLSS Variant A (`Pure Sequence`)** 87-dataset mean `Blind` ROC-AUC | **`0.889379`** | **`0.889379`** (`+0.006057` vs NetMHC, `+0.006331` vs Pan) | **`0 / 87`** |
| **CLSS Variant B (`Sequence + BD2009 IRT`)** 87-dataset mean `Blind` ROC-AUC | **`0.889556`** | **`0.889556`** (`+0.006234` vs NetMHC, `+0.006508` vs Pan) | **`0 / 87`** |
| Dataset Wins vs `NetMHC` (`Variant A` / `Variant B`) | `55 / 87` / `57 / 87` | `55 / 87` ($p = 0.017828$) / **`57 / 87`** (**$p = 0.005014 < 0.01$**) | `0` |
| Dataset Wins vs `NetMHCpan` (`Variant A` / `Variant B`) | `45 / 87` / `47 / 87` | `45 / 87` / `47 / 87` | `0` |
| Dataset Wins vs `SMM-PMBEC` (`Variant A` / `Variant B`) | `73 / 87` / `74 / 87` | `73 / 87` / `74 / 87` ($p = 1.59 \times 10^{-11}$) | `0` |

---

## 3. Independent Reproduction of Partial Wins `p1`, `p2`, and `p3`

1. **`p1` (`iedb-mhci-small-allele-blind-auc` — 20 smallest datasets by `size_cv` $\in [57, 326]$):**
   - Reference means on the 20 smallest datasets by `size_cv`: `NetMHC = 0.830038`, `NetMHCpan = 0.829313`, `SMM-PMBEC = 0.746466`.
   - **Variant A (`Pure Sequence`):** `0.850714` (**`+0.020676` vs `NetMHC`**, **`+0.021401` vs `NetMHCpan`**, strictly $\ge +0.0200$).
   - **Variant B (`Sequence + BD2009 IRT`):** `0.850861` (**`+0.020823` vs `NetMHC`**, **`+0.021548` vs `NetMHCpan`**, strictly $\ge +0.0200$; `17 / 20` wins vs `NetMHC`, `12 / 20` wins vs `NetMHCpan`).
   - On the 20 smallest datasets by `size_bl` ($\in [53, 164]$): Variant A = `0.888622` (`+0.011630` vs `NetMHC = 0.876992`, `+0.016286` vs `NetMHCpan = 0.872336`, vs `SMM-PMBEC = 0.812827`), Variant B = `0.888725` (`+0.011733` vs `NetMHC`, `+0.016389` vs `NetMHCpan`).
   - **Status:** **PASS**.

2. **`p2` (`iedb-mhci-cv-blind-optimism-gap-shrink` — 5-fold `cv_rnd` vs `Blind` optimism gap shrinkage):**
   - Re-executed `python3 how-we-built-it/verify_p2_optimism_gap.py` from scratch (`21.45 s` single-thread runtime).
   - **Reproduced 87-Dataset 5-Fold `cv_rnd` OOF Mean ROC-AUC:** `0.907408` (exact match to `bd2009_blind_certificate.json`).
   - **Reproduced `cv_rnd - blind` Optimism Gap:** `0.017852` (Variant B) / `0.018028` (Variant A), vs `NetMHCpan = 0.034553` (official updated table) / `0.031700` (paper text).
   - **Reproduced Optimism Gap Shrinkage vs `NetMHCpan`:** **`+0.016701` (vs table) / `+0.013848` (vs paper)** for Variant B, and **`+0.016524` (vs table) / `+0.013672` (vs paper)** for Variant A — both strictly $\ge +0.0100$ while beating both `NetMHCpan` (`0.883048`) and `NetMHC` (`0.883322`) on `Blind` (`0.889556` / `0.889379`).
   - **Status:** **PASS**.

3. **`p3` (`iedb-mhci-bd2013-leakage-quantification` — 6-point temporal contamination audit):**
   - Independently verified that `(BD2013 U Blind) \ BD2009` contains exactly **`42,038` unique post-2009 `(mhckey, sequence)` measurements**.
   - Verified the 6-point contamination curve across $f \in \{0.00, 0.10, 0.25, 0.50, 0.75, 1.00\}$ in both Regime A (`0.888874 -> 0.889102 -> 0.889561 -> 0.890256 -> 0.891196 -> 0.891777`, `+0.002903`) and Regime B (`0.888874 -> 0.902231 -> 0.922173 -> 0.947028 -> 0.964877 -> 0.980744`, `+0.091869`, reaching `75/87` wins at $f=10\%$ and `86/87` wins at $f=100\%$).
   - **Status:** **PASS**.

pass: true
