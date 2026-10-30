# V3R1T4S Skeptic 1 (REPRODUCE) Audit Report — `dreval-cross-study-ctrpv2-to-gdsc2`

- context: fresh subagent invoked via invoke_subagent for independent V3R1T4S panel review
- **Verdict:** PASS
- **Target ID:** `dreval-cross-study-ctrpv2-to-gdsc2`
- **Submission ID:** `2026-10-29-mizopl-f732aed6`
- **Verification Scripts Audited:** `verify-it-yourself/verify.py`, `how-we-built-it/models.py`, `how-we-built-it/stage2_inner_ablation.py`, `how-we-built-it/stage3_exvivo_and_cross_study_eval.py`, `how-we-built-it/stage4_formalities_and_nulls.py`
- **Certificates Audited:** `object/certificate.json` (`f732aed69c26d36462d68fcb25698da019f0ca8e45ae69c78382d287452f6d5a`), `object/preregistration_lock.json` (`5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a`)

---

## 1. Cryptographic Integrity & Air-Gap Pre-Registration Verification

1. **Pre-Registration Lock (`object/preregistration_lock.json`):** Verified SHA-256 `5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a` stamped at `2026-10-29T16:54:12.009517+00:00` immediately after Stage 2 inner `CTRPv2` validation and before any execution of Stage 3 (`BeatAML2`, `PDX_Bruna`, `GDSC2`).
2. **CoT Audit Trail (`how-we-built-it/COT_CHAIN_OF_THOUGHT_AND_AIRGAP_AUDIT.md`):** Independently exported by `MONITOR` (`556ad873`) from the raw system transcript (`steps 0..383` pre-lock, `steps 384..449` post-lock), confirming zero modifications to `models.py` after the pre-registration lock.
3. **100% Single-Row Inductive Evaluation (`single_row_inductive_max_diff = 0.0`):** `SchurBilinearExVivoDRP.predict()` transforms each test cell line's gene-expression vector independently via within-sample van der Waerden normal scores `(rank - 0.5) / G_shared` and projects onto 35 Hallmark gene sets using training-fitted ridge weights only. Evaluating test rows one-by-one vs in a full batch produces `max_abs_diff = 0.0`.

## 2. Independent Recomputation from `object/*.csv`

Running `sh verify-it-yourself/run_checks.sh` verified the SHA-256 digests of all `26` files in `object/` and recomputed all 10-split normalized metrics (`R2_norm`, `Pearson_norm`, `MSE`, `RMSE`, `MAE`), Tanimoto similarity strata, and `p3` transfer-gap closure steps to `< 1e-4` discrepancy. Running a single-digit corruption test on `object/` produced immediate deterministic rejection (`exit 1`, last line `FAIL`).

pass: true
