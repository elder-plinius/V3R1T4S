# Skeptic 1 — Reproducibility & Adversarial Mutation Audit (`reproduce.md`)

- `context`: `fresh independent skeptic review initialized from clean package directory`
- `target_id`: `openproblems-spatially-variable-genes-correlation`
- `command_checked`: `sh verify-it-yourself/run_checks.sh`
- `corrupt_checked`: `sh verify-it-yourself/run_checks.sh --corrupt`

## Audit Findings

1. **Clean Blind Isolated Execution:** Running `sh verify-it-yourself/run_checks.sh` from a clean copy executes `verify-it-yourself/verify.py` with bytecode generation disabled (`-B` / `sys.dont_write_bytecode = True`), writing only `blind_dataset.h5ad` (with scrambled feature columns and opaque `g_0..g_{G-1}` identifiers) into an isolated `tempfile.TemporaryDirectory` for each of the `12` panel datasets across all `9` spatial technologies, exiting `0` with final line `PASS`.
2. **Exact Invariance & Baseline Anchor Checks:** On `42_slide_tag_human_skin_melanoma`, `object/method.py` (`sha256: 4503ac7a6e97aa6816353b486e8c87f7b64f5caeba32c6ae3f486eb6f44a7336`) satisfies gene-column permutation equivariance (`rel_err < 1e-12`), 2D rotation/reflection/translation/uniform-scale invariance (`rel_err < 1e-12`), coordinate-shuffle null collapse (`|tau_null| < 0.05` vs `tau_pos = 0.797905`), and 6-decimal Delaunay `MoranI` parity (`0.196000 == 0.196000`) against `Zenodo 18193366`.
3. **All-Object Semantic & Hash-Transparent Mutation Rejection:** Both `sh verify-it-yourself/run_checks.sh --corrupt` and individual single-digit / hash-transparent perturbations across all `6` JSON certificates in `object/` (`benchmark_50_datasets.json`, `ablation_p3.json`, `depth_paradox_benchmark.json`, `wave2_eb_v2_benchmark_50.json`, `bayes_ceiling_dev4.json`, `verification_certificate.json`) plus `object/method.py` and `object/ams_svg_eb_v2.py` exit `1` with final line `FAIL`.

pass: true
