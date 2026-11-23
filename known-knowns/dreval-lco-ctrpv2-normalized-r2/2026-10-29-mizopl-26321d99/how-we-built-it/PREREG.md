# Pre-Registration & Strict Air-Gap Protocol (`dreval-lco-ctrpv2-normalized-r2`)

- **Pre-Registration Lock File:** `object/preregistration_lock.json`
- **Pre-Registration Lock SHA-256:** `5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a`
- **Locked Timestamp (UTC):** `2026-10-29T16:54:12.009517+00:00`
- **CoT Transcript Audit (`MONITOR 556ad873`):** `how-we-built-it/COT_CHAIN_OF_THOUGHT_AND_AIRGAP_AUDIT.md` (`steps 0..383` pre-lock design & inner `CTRPv2` validation; `steps 384..449` post-lock cross-study / ex vivo execution)

## Air-Gap Guarantee (`Anti-Trap #1`)

1. All model architecture choices (`SchurBilinearExVivoDRP`), within-sample van der Waerden normal-score gene expression transformations, 35-Hallmark pathway activity projections, doubly-centered residual kernel ridge regression (`lambda_C = 25.0`, `lambda_D = 10.0`), Kronecker bilinear ridge (`lambda_B = 250.0`), and Bayes-MMSE shrinkage gate (`tau_0 = 0.08`, `beta_max = 0.90`) were designed and selected **exclusively** on internal `CTRPv2` cross-validation (`Stage 2`).
2. Zero response values from `BeatAML2`, `PDX_Bruna`, or `GDSC2` were inspected or touched prior to stamping `preregistration_lock.json` (`5c9295e157e58376a63e0ef358edbfc950bcff6f30499c494ffc01a47cd6c33a`).
