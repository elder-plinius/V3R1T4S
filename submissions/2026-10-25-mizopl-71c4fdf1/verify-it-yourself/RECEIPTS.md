# Verification Receipts — `2026-10-25-mizopl-71c4fdf1` (`linear-baseline-perturbation-replogle-k562`)

## 1. Zero-Trust Certificate Audit (`sh verify-it-yourself/run_checks.sh`)
```text
=== [1/5] Auditing Certificate & Dataset Provenance SHA-256 Hashes ===
  [PASS] Certificate SHA-256 (71c4fdf154e6f8cc...) and all 8 benchmark dataset SHA-256 hashes verified.

=== [2/5] Auditing p3 Reproduction of Record (seeds = 1:2 & seeds = 1:5) ===
  [PASS] Reproduction of record (`mean`, `lpm_selftrained`, `lpm_k562PertEmb`, `lpm_rpe1PertEmb`, `lpm_gearsPertEmb`) verified across all 3 datasets and both split regimes (seeds 1..2 and seeds 1..5).

=== [3/5] Auditing Full Win Criteria on replogle_k562_essential ===
  [PASS] K562 Mean L2: 3.320307 vs 4.097028 (lpm_selftrained) & 4.078658 (gears) [-18.96% vs lpm, 57.47x lpm SD / 31.25x dual SD]
  [PASS] K562 Median L2: 3.044310 vs 3.805564 (lpm_selftrained) & 3.766328 (uce) [-20.00% vs lpm, 63.87x lpm SD]
  [PASS] K562 Mean Pearson delta: 0.620623 vs 0.435544 (lpm_selftrained) [+42.49%, 7.70x lpm SD]
  [PASS] K562 Median Pearson delta: 0.644965 vs 0.426484 (lpm_selftrained) [+51.23%]

=== [4/5] Auditing Partial Win p1 (replogle_rpe1_essential) & p2 (Functional Distance) ===
  [PASS] p1 RPE1 Mean L2: 4.777953 vs 5.390179 [-11.36%, 2.65x lpm SD]; Mean Pearson delta: 0.719286 vs 0.680388 [+5.72%]
  [PASS] p2 K562 Functional Distance Stratification: Q1_closest dL2=-1.4049 (-32.33%) vs Q4_farthest dL2=-0.4043 (-10.40%), Spearman r=0.3451 (p=9.7126e-09)

=== [5/5] Auditing Null / Permutation Controls ===
  [PASS] K562 Null Control (100 combined / 200 split evals): real L2=3.320307 vs null=4.971309 +/- 0.067250 (Z=24.55 sigma)
  [PASS] RPE1 Null Control (50 combined / 100 split evals): real L2=4.777953 vs null=6.231428 +/- 0.064759 (Z=22.44 sigma)

ALL VERIFICATION CHECKS PASSED in 0.01s.
PASS
```

## 2. Live Solver Recomputation (`python3 verify-it-yourself/verify.py --recompute`, `14.37 s` Single-Thread on 16 GB M1)
```text
=== [LIVE RECOMPUTE] Running Hollow-LOO Dual-Lens Solver on data/ ===
  [PASS] Live solver recomputation matches certificate to < 1e-6: lpm_selftrained L2=4.097028 -> Hollow-LOO Dual-Lens L2=3.320307 (-18.96%), r2_delta=0.435544 -> 0.620623 (+42.49%).

ALL VERIFICATION CHECKS PASSED in 14.37s.
PASS
```
