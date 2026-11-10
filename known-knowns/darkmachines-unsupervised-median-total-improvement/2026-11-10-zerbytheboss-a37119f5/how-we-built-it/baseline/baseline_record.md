# Step-3c Baseline Record — `darkmachines-unsupervised-median-total-improvement`

- **Official Challenge Repository Audited**: `https://github.com/bostdiek/DarkMachines-UnsupervisedChallenge` (`1,040` unsupervised detectors across `13` CSV tables in `data/`).
- **Live Verification (`2026-11-10T20:12:24Z`, HTTP `200`)**:
  - `data/Flow.csv`: `4,838` bytes, `sha256 = e2e17152c3222f6ea089706836a6b0f274a041c717a1138c93669629536098e0`
  - `data/Combined.csv`: `19,439` bytes, `sha256 = 7754b06b4a820769ac38986e94b299a54c2e1e845ae30e013e99a4bbc3c5f3b6`
- **Recomputed Baseline Metrics (Notebook `04-SignificanceImprovement.ipynb` Formula)**:
  - `Flow-Efficient_Likelihood`: `Median_TI = 15.0000` (`7.9057` from `1e-2` and `1e-3` alone; `1e-4` equals `1e-3` identically across all `34/34` rows), `Min_TI = 0.9000` (`chaneut_cha400_neut200`), `chaneut_cha300_neut100 TI = 1.1000` (best of `1,040`), `chaneut_cha400_neut200 TI = 0.9000`.
  - `Combined-AVG-DeepSVDD-Flow`: `Median_TI = 10.0000`, `Min_TI = 0.8000`, `chaneut_cha300_neut100 TI = 0.8000`, `chaneut_cha400_neut200 TI = 1.0000` (tied best of `1,040` alongside `Combined-OR-DeepSVDD-Flow` and `Flow-Efficient-No-E_Likelihood`).
  - Prior Global 27-Invariant POT Baseline (`PotHull_Hybrid_Lp3` / `PotStrataZ_Lp3`): `chaneut_cha300_neut100 TI = 1.4000 / 1.6000`, `chaneut_cha400_neut200 TI = 1.6000 / 1.7000`, `Median_TI = 2.8000 / 3.0000`, `Min_TI = 1.0000 / 0.6325`.
