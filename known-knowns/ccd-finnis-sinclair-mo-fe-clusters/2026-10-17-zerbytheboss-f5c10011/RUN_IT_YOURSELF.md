# Run It Yourself

## 1. Verify All 11 New Finnis-Sinclair Putative Global Minima and the 196-Cluster Audit
From the package root, run:
```sh
sh verify-it-yourself/run_checks.sh
```
This executes `verify-it-yourself/check_fs_clusters.py` using only the Python 3 standard library (`hashlib`, `math`, `decimal.Decimal`, and `json`) in `< 7` seconds, verifying:
- Calibration of Finnis-Sinclair `Mo` (1984) and `Fe` (1986) parameters across all 98 posted `Mo` and 98 posted `Fe` point files to `< 1e-7 eV` (`max |dE| = 9.77e-11 eV`), citing live CCD `points/` URLs and SHA-256 digests without vendoring third-party coordinates,
- All 196 rows of the `Mo` (`N = 3..100`) and `Fe` (`N = 3..100`) reproduction and polishing audit (Partial Win `p1`),
- Energies and gradient norms of all 11 new putative global minimum records (`Mo_75`, `Mo_90`, `Fe_86`, `Fe_87`, `Fe_90`, `Fe_91`, `Fe_92`, `Fe_96`, `Fe_97`, `Fe_98`, `Fe_100`) in both `float64` (`||grad E||_2 <= 1.26e-13 < 1e-10`) and 55-digit `decimal.Decimal` (`||grad E||_2 <= 1.20e-27 < 1e-10`),
- Exact $3N \times 3N$ analytical Hessian inertia (`6` rigid-body zero modes `||H Q_0||_F < 1e-14 < 1e-6` and all `3N - 6` vibrational eigenvalues strictly `> 0.35 > 0`).

## 2. Compile the C++17 Bidirectional Cascade Solver
```sh
clang++ -O3 -std=c++17 -march=native -pthread how-we-built-it/FS_Cluster_Hunter.cc -o FS_Cluster_Hunter
```
