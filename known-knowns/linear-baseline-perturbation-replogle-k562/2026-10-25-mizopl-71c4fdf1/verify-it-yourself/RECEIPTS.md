# Verification Receipts (`verify-it-yourself/RECEIPTS.md`)

- **Target ID**: `linear-baseline-perturbation-replogle-k562` (`known-knowns`, Partial Progress `p2` only)
- **Package Path**: `known-knowns/linear-baseline-perturbation-replogle-k562/2026-10-25-mizopl-71c4fdf1`
- **Certificate**: `object/certificate_replogle_k562.json` (`54,328` bytes, `sha256: f7a404a7891275367e46e7e312084b42ce4e687274d7b72da6da4aa4f2794b5a`)
- **Per-Perturbation Metrics TSV**: `object/k562_p2_per_perturbation_metrics.tsv` (`176,975` bytes, `sha256: 0e2ae30e6f9f0942b4adf46e9a2798d74206321ddb13b8dc4027f2c0a6fdfd75`)

## Command & Exact Output (`sh verify-it-yourself/run_checks.sh`)

```text
=== [1/3] Running positive verification on .../object/certificate_replogle_k562.json ===
======================================================================
[PASS] ALL VERIFICATION CHECKS SUCCEEDED FOR linear-baseline-perturbation-replogle-k562 (p2)
  - Scope: PARTIAL_PROGRESS (p2 only)
  - Plain-Text Per-Perturbation TSVs Verified: 5 splits (n=677 held-out K562 perturbations; n=262 Panel A in seeds 1..2), 1,000 genes per perturbation
  - K562 Panel A (n=262, seeds 1..2): LPM L2=4.097028 -> Dual-Lens L2=3.320307; LPM R_delta=0.435544 -> Dual-Lens R_delta=0.620623
  - Partial Progress p2 (Hybrid GO+CoExp, n=262): Q1 delta_L2=-1.4049 (-32.33%), Q4 delta_L2=-0.4043 (-10.40%), Spearman r_L2=0.3451 (p=9.71e-09)
  - Partial Progress p2 (Pure 2023 Static GO-Only, n=262): Q1 delta_L2=-1.2672 (-27.68%), Q4 delta_L2=-0.3311 (-8.94%), Spearman r_L2=0.4208 (p=1.15e-12), r_Rdelta=-0.4103 (p=4.64e-12)
  - Null Permutation Controls (200 split runs): z_L2=-24.55, z_R_delta=31.78 (p=0.0099)
======================================================================
=== [2/3] Running negative-control test (corrupted certificate must fail) ===
[PASS] Verifier correctly rejected corrupted certificate with non-zero exit code.
=== [3/3] Running negative-control test (corrupted plain-text prediction TSV must fail) ===
[PASS] Verifier correctly rejected corrupted plain-text prediction TSV with non-zero exit code.
PASS: all verification and negative-control checks succeeded.
```
