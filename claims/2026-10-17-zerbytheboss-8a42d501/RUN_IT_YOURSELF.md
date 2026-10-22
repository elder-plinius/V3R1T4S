# Run It Yourself

## 1. Verify All 5 New Gupta Global Minima and the 780-Point-File Audit
From the package root, run:
```sh
sh verify-it-yourself/run_checks.sh
```
This executes `verify-it-yourself/check_gupta_clusters.py` using only the Python 3 standard library (`math`, `decimal.Decimal`, and `json`) in `< 9` seconds, verifying:
- Calibration of the Gupta parameters for `Zn`, `Cd`, `Pb`, and `Na_Gupta` across 12 embedded point files per metal (`48` files total) to `< 1e-5 eV` (`max |dE| = 4.93e-7 eV`),
- All 780 rows of the `Zn`, `Cd`, `Pb`, `Pb_Gupta.rar`, and `Na_Gupta` reproduction audit (`max |dE| = 7.17e-7 eV < 1e-5 eV`, `0` unreproduced rows),
- Energies and gradient norms of all 5 new records (`Zn_106`, `Cd_71`, `Cd_84`, `Cd_94`, `Cd_106`) in both `float64` (`||grad E||_2 <= 2.66e-14 < 1e-10`) and 55-digit `decimal.Decimal` (`||grad E||_2 <= 6.58e-35 < 1e-10`),
- Distinct-basin verification confirming that the polished posted CCD point files for `Zn_106`, `Cd_71`, `Cd_84`, `Cd_94`, and `Cd_106` remain higher in energy by `0.000207 eV` to `0.004692 eV` (`> 1e-4 eV`),
- Exact $3N \times 3N$ analytical Hessian inertia (`6` rigid-body zero modes `||H Q_0||_F <= 1.31e-14 < 1e-6` and all `3N - 6` vibrational eigenvalues strictly `> 0.030 > 0`).

## 2. Compile the C++17 Bidirectional Cascade & Tournament Solver
```sh
clang++ -O3 -std=c++17 -march=native -pthread how-we-built-it/Gupta_Cluster_Hunter.cc -o Gupta_Cluster_Hunter
```
