context: isolated Antigravity subagent b7676112-e173-477b-924c-cc563f142a3e (V3R1T4S Skeptic CRITERION)
target_id: iedb-mhci-bd2009-blind-auc
run_id: 2026-10-25-2115

# Skeptic 3 (`CRITERION`) Verification Report — `iedb-mhci-bd2009-blind-auc` (`2026-10-25-2115`)

- **Target ID:** `iedb-mhci-bd2009-blind-auc` (*"Peptide-MHC class I binding: beat NetMHCpan's blind-set AUC on the frozen public IEDB BD2009-to-Blind benchmark"*)
- **Audited Verdict:** `PARTIAL_PROGRESS` (`p1: iedb-mhci-small-allele-blind-auc`, `p2: iedb-mhci-cv-blind-optimism-gap-shrink`, `p3: iedb-mhci-bd2013-leakage-quantification`)
- **Files Audited:** `target.md`, `PREREG.md`, `null_test.md`, `attempts/lens1_pan_allele_pocket_tobit_kernel/NOTES.md`, `attempts/lens2_empirical_bayes_potts_ensemble_and_p1_p2_p3/NOTES.md`, `claim/artifact.md`, `claim/bd2009_blind_certificate.json`, `claim/blind_predictions.npz`, and `claim/verify.py`.

---

## 1. Pre-Registration & Null-Gate Audit (`PREREG.md`, `null_test.md`)

1. **Frozen Split & Zero-Contamination Firewall:**
   - All model training for the `Blind` benchmark is restricted strictly to `bdata.2009.mhci.public.1.txt` (`137,654` rows, SHA-256 `261df865af42db48f11600e56235224c168b505e302270d290a28ebb62cc08f1`), with 5-fold cross-validation (`p2`) evaluated strictly on `bdata.2009.mhci.public.1.cv_rnd.txt` (`131,558` rows across the 87 `(allele, length)` datasets, SHA-256 `a510694eb6b7d2250462738f7bd7c9e42e2e1461a1254d100ab2d4358071925c`).
   - Zero post-2009 measurements (`post2009_training_rows_used = 0`), zero pretrained protein language models (`pretrained_protein_language_models_used = false`), and zero external structural databases are used in `Variant A` or `Variant B`.
   - `bdata.20130222.mhci.public.1.txt` (`BD2013`) is touched strictly in the isolated `p3` leakage-quantification experiment.
2. **Dataset Alignment & Binder Convention (`target.md` Trap Check):**
   - Across all 87 `(allele, length)` datasets in the official reference tables (`table.cv_features.updated.auc.{netmhc,netmhcpan,smmpmbec_cpp}.xls`), matching `mhckey` in `BD2009` and `Blind` (`bdata.2013.mhci.public.blind.1.txt`, `26,861` measurements across the 87 datasets) with the published binder threshold `meas < 500.0` nM reproduces `size_cv`, `size_cv_binder`, `size_bl`, and `size_bl_binder` with **`0 / 87` discrepancies**.
3. **Random-Score Null Baseline (`null_test.md`):**
   - Across `400` independent standard-normal random score controls on the 87 `Blind` datasets (`26,861` measurements), the mean ROC-AUC is `0.500020` (`std = 0.006675`) and `best_control = 0.519954` (single-seed `seed=42` control = `0.504497`), confirming zero label leakage in the evaluation harness (`real_beats_all_controls: yes`).

---

## 2. Criterion-by-Criterion Audit

### 2.1 Honest `PARTIAL_PROGRESS` Classification vs. `CONFIRMED_SOLUTION` Full-Win Bar
- **Full-Win Requirement (`target.md` / `PREREG.md`):**
  1. Unweighted 87-dataset mean `Blind` ROC-AUC $\ge \max(\text{ref}) + 0.01 = 0.883322 + 0.01 = \mathbf{0.893322}$.
  2. Strict per-dataset `Blind` AUC higher than the reference on **$\ge 60 / 87$** datasets (two-sided exact binomial sign test $p < 0.01$).
- **Achieved Performance on the 87-Dataset `Blind` Benchmark:**
  - **Reference Means:** `NetMHC = 0.883322`, `NetMHCpan = 0.883048`, `SMM-PMBEC = 0.847389`.
  - **CLSS Variant A (`Pure Sequence f(allele, seq)`):** **`0.889379`** (`+0.006057` vs `NetMHC`, `+0.006331` vs `NetMHCpan`, `+0.041990` vs `SMM-PMBEC`), winning `55 / 87` datasets vs `NetMHC` ($p_{\text{sign}} = 0.017828$), `45 / 87` vs `NetMHCpan`, and `73 / 87` vs `SMM-PMBEC` ($p_{\text{sign}} = 8.8 \times 10^{-11}$).
  - **CLSS Variant B (`Sequence + BD2009 IRT`):** **`0.889556`** (`+0.006234` vs `NetMHC`, `+0.006508` vs `NetMHCpan`, `+0.042167` vs `SMM-PMBEC`), winning **`57 / 87` datasets vs `NetMHC` (two-sided binomial sign test $p = 0.005014 < 0.01$)**, `47 / 87` vs `NetMHCpan`, and `74 / 87` vs `SMM-PMBEC` ($p_{\text{sign}} = 1.59 \times 10^{-11}$).
- **Criterion Audit:** Although both Variant A and Variant B beat all three published reference methods on unweighted 87-dataset mean `Blind` AUC and Variant B achieves a statistically significant majority dataset win against `NetMHC` (`57 / 87`, $p = 0.005014 < 0.01$), the mean gain (`+0.006234` / `+0.006057`) is below the strict `+0.0100` (`>= 0.893322`) and `>= 60 / 87` bar required for `CONFIRMED_SOLUTION`. Claiming `PARTIAL_PROGRESS` rather than `CONFIRMED_SOLUTION` is **100% honest and compliant** with `target.md` and `PREREG.md`.

### 2.2 Partial Win `p1` (`iedb-mhci-small-allele-blind-auc`) — **PASS**
- **Criterion (`target.md` line 15 / `PREREG.md`):** Beat the best reference `Blind` AUC by **$\ge +0.02$** on the 20 smallest datasets under the same `BD2009`-only training restriction.
- **Verified Results on the 20 Smallest Datasets by Training Sample Size `size_cv` (`size_cv` $\in [57, 326]$):**
  - **Reference Means:** `NetMHC = 0.830038` (best reference), `NetMHCpan = 0.829313`, `SMM-PMBEC = 0.746466`.
  - **CLSS Variant A (`Pure Sequence`):** **`0.850714`** $\to$ **`+0.020676` vs `NetMHC`** ($\ge 0.02$) and **`+0.021401` vs `NetMHCpan`** ($\ge 0.02$).
  - **CLSS Variant B (`Sequence + BD2009 IRT`):** **`0.850861`** $\to$ **`+0.020823` vs `NetMHC`** ($\ge 0.02$), **`+0.021548` vs `NetMHCpan`** ($\ge 0.02$), and **`+0.104395` vs `SMM-PMBEC`**, winning `17 / 20` datasets vs `NetMHC` and `12 / 20` vs `NetMHCpan`.
- **Verified Results on the 20 Smallest Datasets by Blind Test Size `size_bl` (`size_bl` $\in [53, 164]$):**
  - Both Variant A (`0.888622`) and Variant B (`0.888725`) also outperform all three references (`NetMHC = 0.876992`, `NetMHCpan = 0.872336`, `SMM-PMBEC = 0.812827`) by `+0.011733` vs `NetMHC` and `+0.016389` vs `NetMHCpan`.

### 2.3 Partial Win `p2` (`iedb-mhci-cv-blind-optimism-gap-shrink`) — **PASS**
- **Criterion (`target.md` line 16 / `PREREG.md`):** Shrink `NetMHCpan`'s cross-validation-to-blind optimism gap (`0.034553` in the official updated table `0.917601 - 0.883048`; `0.031700` in the paper text `0.9147 - 0.8830`) by **$\ge 0.01$** while maintaining `Blind` AUC not worse than the reference (`>= 0.883322`).
- **Verified Results:**
  - **Zero-Fold-Leakage Homology-Damped 5-Fold `cv_rnd` OOF Mean AUC:** **`0.907408`**.
  - **87-Dataset `Blind` Mean AUC:** **`0.889556`** (Variant B) / **`0.889379`** (Variant A) — both strictly higher than `NetMHC` (`0.883322`) and `NetMHCpan` (`0.883048`).
  - **Attacker Optimism Gap ($\text{mean}(\text{AUC}_{\text{cv\_rnd}}) - \text{mean}(\text{AUC}_{\text{blind}})$):** **`0.017852`** (Variant B) / **`0.018028`** (Variant A).
  - **Optimism Gap Shrinkage vs `NetMHCpan`:**
    - vs Official Updated Table (`0.034553`): **`+0.016701`** (Variant B) and **`+0.016524`** (Variant A) — both **$\ge 0.0100$**.
    - vs Paper Text (`0.031700`): **`+0.013848`** (Variant B) and **`+0.013672`** (Variant A) — both **$\ge 0.0100$**.

### 2.4 Partial Win `p3` (`iedb-mhci-bd2013-leakage-quantification`) — **PASS**
- **Criterion (`target.md` line 17 / `PREREG.md`):** Quantify how much apparent `Blind` AUC the exact same predictor architecture gains on this benchmark purely when post-2009 measurements from the 2013 corpus (`42,038` unique post-2009 `(mhckey, sequence)` rows) leak into training, compared against training strictly on `BD2009`.
- **Verified Results Across Contamination Fractions $f \in \{0.00, 0.10, 0.25, 0.50, 0.75, 1.00\}$:**
  - **Clean `BD2009` Baseline ($f = 0.00$):** `0.888874` (`55 / 87` wins vs `NetMHC`, `46 / 87` vs `NetMHCpan`).
  - **Regime A (Cross-allele sister leakage only, $0\%$ target-allele blind rows):** Monotonically inflates `Blind` AUC from `0.888874` ($f = 0.00$) to `0.889102` ($f = 0.10$), `0.889561` ($f = 0.25$), `0.890256` ($f = 0.50$), `0.891196` ($f = 0.75$), and **`0.891777` (`+0.002903` at $f = 1.00$)**.
  - **Regime B (Full post-2013 corpus leakage):** Monotonically inflates `Blind` AUC from `0.888874` ($f = 0.00$) to **`0.902231` (`+0.013357`, `75 / 87` wins at just $f = 0.10$)**, `0.922173` (`+0.033299`, `82 / 87` wins at $f = 0.25$), `0.947028` (`+0.058154`, `84 / 87` wins at $f = 0.50$), `0.964877` (`+0.076002`, `85 / 87` wins at $f = 0.75$), and **`0.980744` (`+0.091869`, `86 / 87` wins at $f = 1.00$)**.

---

## 3. Standalone Certificate Re-Computation Check (`verify.py`)

Executing `python3 verify.py` independently recomputed all 87 per-dataset ROC-AUC values directly from `blind_predictions.npz` (`26,861` held-out predictions and binary labels) and confirmed:
- Exact agreement (`<= 1e-6`) on all 87 datasets for both `Variant A` and `Variant B`.
- All pre-registration and `target.md` criteria for `PARTIAL_PROGRESS` (`p1`, `p2`, `p3`) are satisfied with zero violations and zero over-claiming.

pass: true
