# Run It Yourself

## 1. Verify the 11 New Finnis-Sinclair Putative Global Minima and Stored 196-Row Audit
From the package root, run:
```sh
sh verify-it-yourself/run_checks.sh
```
This executes `verify-it-yourself/check_fs_clusters.py` using only the Python 3 standard library (`hashlib`, `math`, `decimal.Decimal`, and `json`) in `< 7` seconds. Only the 11 new putative global minimum structures (`Mo_75`, `Mo_90`, `Fe_86`, `Fe_87`, `Fe_90`, `Fe_91`, `Fe_92`, `Fe_96`, `Fe_97`, `Fe_98`, `Fe_100`) are recomputed from their coordinates; the calibration, polished-CCD energies, and 196-row audit are stored values checked against hashes, and reproducing them from coordinates requires downloading the cited `points.tgz` archives (`https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Mo/points.tgz`, SHA-256 `b60a90adc8392f479bc08ecd19fd25c2cbcd1bb14e4f276f082164d07dad7720`, and `https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Fe/points.tgz`, SHA-256 `d95407e5ee2e55fc4149531f2e5a2d65c39c53f633c5fb839f0f3dc834665624`):
- Stored calibration and 196-row reproduction/polishing audit rows (`ccd_196_point_files_audit`, Partial Win `p1`) checked against SHA-256 for Finnis-Sinclair `Mo` (1984, 98 files, `max |dE| = 9.77e-11 eV < 1e-7 eV`) and `Fe` (1986 modified, 98 files, `max |dE| = 9.42e-11 eV < 1e-7 eV`), citing live CCD `points/` URLs and SHA-256 digests without vendoring third-party coordinates,
- Recomputed energies and gradient norms of all 11 new putative global minimum records (`Mo_75`, `Mo_90`, `Fe_86`, `Fe_87`, `Fe_90`, `Fe_91`, `Fe_92`, `Fe_96`, `Fe_97`, `Fe_98`, `Fe_100`) from their coordinates in both `float64` (`||grad E||_2 <= 1.26e-13 < 1e-10`) and 55-digit `decimal.Decimal` (`||grad E||_2 <= 1.20e-27 < 1e-10`),
- Recomputed exact $3N \times 3N$ analytical Hessian inertia (`6` rigid-body zero modes `||H Q_0||_F < 1e-14 < 1e-6` and all `3N - 6` vibrational eigenvalues strictly `> 0.35 > 0`) for the 11 new structures.

## 2. Compile the C++17 Bidirectional Cascade Solver
```sh
clang++ -O3 -std=c++17 -march=native -pthread how-we-built-it/FS_Cluster_Hunter.cc -o FS_Cluster_Hunter
```
