context: isolated Antigravity subagent 45129379-d6d5-4304-a79a-60708eab59a4 (V3R1T4S Skeptic NOVELTY)
target_id: iedb-mhci-bd2009-blind-auc
run_id: 2026-10-25-2115

# Skeptic 2 (`NOVELTY & CONTAMINATION FIREWALL`) Audit Report — `iedb-mhci-bd2009-blind-auc`

- **Run ID:** `2026-10-25-2115`
- **Target ID:** `iedb-mhci-bd2009-blind-auc` (`known-unknowns/disease-research/iedb-mhci-bd2009-blind-auc.md`)
- **Claimed Verdict:** `PARTIAL_PROGRESS` (`p1`: `iedb-mhci-small-allele-blind-auc`, `p2`: `iedb-mhci-cv-blind-optimism-gap-shrink`, `p3`: `iedb-mhci-bd2013-leakage-quantification`)
- **Panel Role:** Skeptic 2 — Novelty, Provenance & Zero-Contamination Firewall Auditor

---

## 1. Prior Submissions & Competing PR Check

1. **`elder-plinius/V3R1T4S` Repository & PR History:**
   - Audited `scout.md` and searched `elder-plinius/V3R1T4S` (`known-unknowns/disease-research/iedb-mhci-bd2009-blind-auc.md`).
   - Only the target specification `known-unknowns/disease-research/iedb-mhci-bd2009-blind-auc.md` exists (`open as of 2026-10-15`).
   - There are **0 competing PRs** and **0 prior submissions** for `iedb-mhci-bd2009-blind-auc` in `elder-plinius/V3R1T4S`.
2. **Official Benchmark Archive (`benchmark_mhci_reliability.tar.gz`) Contents Check:**
   - Inspected all files in `benchmark_mhci_reliability.tar.gz`. The archive contains only raw tab-separated binding datasets (`bd2009.1`, `bd2013.1`, `blind.1`), precomputed reference prediction text files (`netmhc`, `netmhcpan`, `smmpmbec_cpp`, `smmpmbec_cpp_rerun`), `.xls` performance tables, and a 30-line data check script (`quick-check-cv-data.py`). None of the modeling, optimization, or audit algorithms in this claim exist in the benchmark archive.

---

## 2. Strict `BD2009` Zero-Contamination Firewall Audit

I performed a line-by-line code audit of:
- `how-we-built-it/test_modular_pan.py` (Lens 1)
- `how-we-built-it/test_lens2_blind.py` (Lens 2)
- `how-we-built-it/verify_p2_optimism_gap.py` (`p2`)
- `how-we-built-it/run_cv_and_p3_audit.py` (`p3`)
- `how-we-built-it/build_claim_package.py`
- `verify-it-yourself/verify.py`

### Findings:
1. **No Post-2009 Training Data in `BD2009 -> Blind` Predictors:**
   - In both `test_modular_pan.py` (Lens 1) and `test_lens2_blind.py` (Lens 2), `bdata.20130222.mhci.public.1.txt` (`BD2013`) is **never imported or read**.
   - Every learned parameter—9-mer base profiles (`w9_init`), serological family priors (`w9_fam`), per-allele anchor position norms (`pos_norms_allele`), position-specific pocket similarity matrices (`S_pos`, `S_N`, `S_C`), empirical peptide co-binding correlations (`corr_raw`, `S_comb`), modular supertype priors (`w9_sup_prior`), Exon-2/Exon-3 split weights (`wN_raw`, `wC_raw`, `wN_ens`, `wC_ens`), exact dual 9-mer kernel models (`exact_dual_9mer`), supertype-pooled Nyström 9-mer and multi-length groove kernels (`nonlinear_9mer_models`, `allele_nystrom_cache`), native length-$L$ linear/Nyström/chemical-epistasis models (`wL`, `wzL`, `wzC`), and the cross-allele IRT lookup (`seq_bd_lookup`)—is fitted **exclusively on `bdata.2009.mhci.public.1.txt`** ($137{,}654$ rows, SHA-256 `261df865af42db48f11600e56235224c168b505e302270d290a28ebb62cc08f1`).
   - Note on `seq_cores_X` precomputation: `encode_len(candidate_9mer_cores(s), 9)` is a purely deterministic, per-peptide string-to-BLOSUM62 array map with zero learned parameters or corpus statistics.
   - `bdata.2013.mhci.public.blind.1.txt` (SHA-256 `ab15f0480f1e2c08cefacd9f2832e0263b4ab05a176c8da774c9172d7264d768`) is used strictly at test time to evaluate `sub_te["sequence"]` and score ROC-AUC against `y_true = (sub_te["meas"].values < 500.0).astype(int)`.
   - `bdata.20130222.mhci.public.1.txt` is loaded **only** in `run_cv_and_p3_audit.py` Part 2 to run the separate `p3` temporal contamination response curve after `clean_seq_scores` and `clean_full_scores` ($f = 0.00$) have already been frozen.
2. **No Pretrained Protein Language Models or Post-2009 Structural/Sequence Databases:**
   - Zero neural/PLM weights (no ESM, ProtTrans, UniProt, or pretrained MHCflurry/NetMHCpan weights) and zero crystal structures are loaded.
   - All domain constants are hardcoded and strictly pre-date 2009:
     - `BLOSUM62_RAW`: Henikoff & Henikoff (*PNAS* 89:10915–10919, 1992).
     - `PHYS5_RAW`: Kyte & Doolittle hydropathy (*J. Mol. Biol.* 157:105–132, 1982) plus standard amino acid side-chain volume, net charge, polarity, and aromaticity.
     - `SUPERTYPE_MAP`: Sidney, Peters, Frahm, Sette (*BMC Immunology* 9:1, 2008) canonical HLA-A / HLA-B supertype classification.
     - `candidate_9mer_cores`: Lundegaard et al. (*Nucleic Acids Research* 36:W509–W512, 2008) L29 9-mer core insertion/deletion rules.

---

## 3. Novelty & Non-Triviality of Technical Contributions

The target's Traps section (`target.md` line 56) requires verifying that the method is genuinely novel rather than a trivial re-run of an existing tool or post-2014 architecture, and does not over-claim clinical neoantigen ranking. All four technical pillars in this package are original, mathematically sound, and directly tailored to the structural regimes of `BD2009 -> Blind`:

1. **Majorization-Minimization One-Sided Censored Inequality (`>`) Solver (`MM-Tobit`, `solve_censored_mm`):**
   - Over 30% of `BD2009` rows carry qualitative right-censored inequalities (`> 500`, `> 5000`, `> 20000` nM) from diverse assay dynamic ranges. Standard ridge regression (`SMM-PMBEC`) or clipped regression treats `> 500` nM as an exact equality at $500\text{ nM}$, biasing small-allele motifs toward the boundary.
   - The attacker formulates a fast Majorization-Minimization solver (`solve_censored_mm`) that pre-factors $(X^\top W X + \Lambda)^{-1}$ once and iteratively updates latent censored targets $y_{\text{work}}^{(t)} = \max(y_{\text{raw}}, \hat{y}^{(t)})$ on `>` rows (and $\min$ on `<` rows) in both primal linear space (with supertype prior $\Lambda w_{\text{prior}}$) and dual/Nyström kernel space.
2. **Modular Pocket-Factorized Supertype Similarity (`S_pos[p]`), Exon-2/Exon-3 Split, and Empirical Bayes Scarcity-Gated Model-Space Supertype Ensemble (`p1`):**
   - Without touching external MHC protein sequences, the model extracts position-by-position binding pocket similarity tensors $S_{\text{pos}}[p, a, b]$ ($p \in \{1,\dots,9\}$) directly from `BD2009` 9-mer motifs, decomposes the groove into an N-terminal module ($P_1\text{–}P_4$, $\alpha_1$ / Exon-2, $S_N$) and C-terminal module ($P_5\text{–}P_9$, $\alpha_2$ / Exon-3, $S_C$), and combines `HLA`-gated Sidney-2008 hierarchy priors with a model-space ensemble of exact dual kernel 9-mer predictors (`eval_model_space_supertype_9mer`) weighted by an Empirical Bayes scarcity factor $\text{scarcity} = \min\!\left(0.95, \frac{750}{n_{\text{tr}}+750}\left(\frac{140}{n_{\text{bind}}+140}\right)^{0.40}\right)$.
   - This delivers a certified **`p1` partial win** on the 20 smallest datasets by training sample size (`size_cv` $\in [57, 326]$): Variant A (`Pure Sequence f(allele, seq)`) achieves **`0.850714`** (`+0.020676 >= 0.02` vs `NetMHC = 0.830038`, `+0.021401` vs `NetMHCpan = 0.829313`) and Variant B (`Sequence + BD2009 IRT`) achieves **`0.850861`** (`+0.020823 >= 0.02` vs `NetMHC`, `+0.021548` vs `NetMHCpan`).
3. **Zero-Fold-Leakage Inverse Homology-Cluster Density Weighting for `cv_rnd` (`p2`):**
   - Diagnoses and removes the two sources of `NetMHCpan`'s cross-validation-to-blind optimism gap (`0.034553` in the official updated table / `0.031700` in the paper text): cross-allele fold leakage of identical peptides in independent per-dataset splits, and within-assay point-mutant series memorization ($G_{ij} > 0.60$).
   - By holding out fold $f \in \{0,\dots,4\}$ globally across `BD2009`, weighting training samples by inverse homology-cluster density $w_i = d_i^{-1.15}$, and capping kernel similarity at $G \le 0.65$, the method achieves a 5-fold `cv_rnd` OOF mean AUC of **`0.907408`** vs `Blind` mean AUC of **`0.889556`** (Variant B) / **`0.889379`** (Variant A), yielding an optimism gap of **`0.017852`** (Variant B) / **`0.018028`** (Variant A)—a shrinkage of **`+0.016701`** (table) / **`+0.013848`** (paper), strictly passing the $\ge 0.01$ `p2` bar while outperforming all three reference methods on `Blind`.
4. **Controlled 6-Point Temporal Contamination Audit Curve on `(BD2013 U Blind) \ BD2009` (`p3`):**
   - Isolates the exact `42,038` unique post-2009 `(mhckey, sequence)` measurements added in 2013 and quantifies apparent `Blind` AUC inflation across $f \in \{0.00, 0.10, 0.25, 0.50, 0.75, 1.00\}$ under two distinct leakage mechanisms: Regime A (cross-allele sister leakage only, `0%` target-allele blind rows: `0.888874 -> 0.891777`, `+0.002903`) and Regime B (full post-2013 pretraining corpus overlap: `0.888874 -> 0.902231` (`+0.013357`, `75/87` wins) at just $f = 10\%$ and `0.980744` (`+0.091869`, `86/87` wins) at $f = 100\%$).

---

## 4. Conclusion

The submission has zero competing PRs, strictly obeys the `BD2009` zero-contamination firewall, avoids all benchmark traps (including dataset-set drift and over-claiming), and introduces four novel, reproducible algorithmic and methodological contributions certifying `PARTIAL_PROGRESS` on `p1`, `p2`, and `p3`.

pass: true
