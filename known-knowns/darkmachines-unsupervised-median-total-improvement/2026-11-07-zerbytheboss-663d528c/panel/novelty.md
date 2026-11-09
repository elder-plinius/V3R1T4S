# Skeptic 2: Novelty & Prior-Art Audit

- Context: Fresh independent comparison against the 13 official evaluation CSVs in `bostdiek/DarkMachines-UnsupervisedChallenge` (1,040 detectors, SciPost Phys. 12, 043, 2022) and subsequent literature (`arXiv:2406.18469`).
- Question: Do the reported Total Improvement scores on `chaneut_cha300_neut100` (`1.4000` / `1.6000`) and `chaneut_cha400_neut200` (`1.6000` / `1.7000`) strictly exceed every detector in the 1,040-detector challenge benchmark and published follow-ups?

## Audit Summary

1. Audited all 13 official CSV files (`AE.csv`, `VAE.csv`, `DeepSetVAE.csv`, `ConvVAE_and_Flows.csv`, `CNN_VAE.csv`, `CNN_BVAE.csv`, `KDE.csv`, `Flow.csv`, `DeepSVDD.csv`, `Combined.csv`, `DAGMM.csv`, `ALAD.csv`, `MethodsInLatentSpaceOfVAE.csv`) in `bostdiek/DarkMachines-UnsupervisedChallenge` (SHA-256 digests recorded in `the-record-we-beat/darkmachines_1040_benchmark_summary.md`).
2. Confirmed that across all 1,040 detectors evaluated on all 4 channels, the best Total Improvement on `chaneut_cha300_neut100` is `1.1000` (`Flow-Efficient_Likelihood`) and on `chaneut_cha400_neut200` is `1.0000` (`Combined-AVG-DeepSVDD-Flow` and `Combined-PROD-DeepSVDD-Flow`; `Flow-Efficient_Likelihood` achieves `0.9000`).
3. Confirmed that `PotHull_Hybrid_Lp3` (`cha300 = 1.4000`, `cha400 = 1.6000`, `Min_TI = 1.0000`), `PotStrataZ_Lp3` (`cha300 = 1.6000`, `cha400 = 1.7000`), and `PotHull_L1_L2_Hull` (`cha300 = 1.2000`, `cha400 = 1.6000`, `Min_TI = 1.0000`) strictly beat all 1,040 challenge detectors on both chargino-neutralino signals while also beating `Flow-Efficient_Likelihood`'s `0.9000` minimum-TI floor across all 19 signals.

pass: true
