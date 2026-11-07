# Null & Negative Control Tests: `tdc-dti-dg-bindingdb-patent-pcc`

## 1. Adversarial Object Corruption Test (`--corrupt` & Byte/Digit Mutation)

- **Command:** `/opt/homebrew/bin/python3 verify-it-yourself/verify.py --corrupt`
- **Mechanism:** Perturbs `mean_5seed_pcc` in `object/certificate.json` (and `kit/check_run.py` / `github_zero_trust_gate.py` independently mutate digits/arrays inside `object/*.json` and `object/seed_*.csv`).
- **Result:** `verify.py` detects the mismatch against its cryptographic and algebraic moment invariants (`l1_norm`, `l2_norm`, `mean`, `std`, and 5x5 `cross_seed_dot_matrix`), prints `VERIFY ERROR: ...` followed by `FAIL`, and exits with code `1`.

## 2. Target-Mean & ERM Baselines vs. 4-Level Universal Kriging Stacker (`Track A`)

1. **Smoothed Target Mean Null Baseline (`step02_inner_temporal_anatomy.py`):**
   - Predicting only the empirical Bayes target mean $\hat{\mu}_t$ achieves `0.45340` on Inner Split A (`2013–2016 -> 2017–2018`) and `0.45172` on Inner Split B (`2013–2017 -> 2018`), confirming that target identity alone explains only $\sim 20\%$ of out-of-time affinity variance.
2. **Reproduced 5-Seed Static-Feature `ERM` Baseline (`object/seed_{1..5}_erm_baseline_part{1,2}.csv`):**
   - Training a standard 2-model LightGBM ERM on static protein + ligand features without our 4-Level Matryoshka Functional ANOVA + Universal Kriging TKRR + `S_pocket` homology transfer yields `0.51310 ± 0.00271` on the 2019–2021 test set (`0.12204 ± 0.03027` on `Unseen-Target` and `0.07611 ± 0.03700` on `2021` patents).
   - Adding the 4-Level Universal Kriging TKRR + Homology-Gated Stacker (`Track A`) improves 5-seed test PCC by **`+0.06632`** (`0.51310` $\to$ `0.57942 ± 0.00299`).
