# Run It Yourself

## 1. Verify the 5 New Gupta Putative Global Minimum Structures and Stored 780-Row Gupta Audit
From the package root, run:
```sh
sh verify-it-yourself/run_checks.sh
```
This executes `verify-it-yourself/check_gupta_clusters.py` using only the Python 3 standard library (`hashlib`, `math`, `decimal.Decimal`, and `json`) in `< 9` seconds. Only the five new putative global minimum structures (`Zn_106`, `Cd_71`, `Cd_84`, `Cd_94`, `Cd_106`) are recomputed from their coordinates; the calibration, polished-CCD energies, and 780-row audit are stored values checked against hashes, and reproducing them from coordinates requires downloading the cited points archives (`https://www-wales.ch.cam.ac.uk/~wales/CCD/jon/structures/Gupta/{Zn,Cd,Pb,Na}/points/all.tar` and `https://www-wales.ch.cam.ac.uk/~wales/CCD/Pb_Gupta.rar`):
- Stored calibration values checked against SHA-256 for the Gupta parameters of `Zn`, `Cd`, `Pb`, and `Na_Gupta` across 12 point files per metal (`48` files total, each cited by its live `jon/structures/Gupta/<metal>/points/<N>` URL and SHA-256 digest) to `< 1e-5 eV` (`max |dE| = 4.93e-7 eV`),
- Stored 780-row `Zn`, `Cd`, `Pb`, `Pb_Gupta.rar`, and `Na_Gupta` Gupta reproduction audit values checked against SHA-256 (`max |dE| = 7.17e-7 eV < 1e-5 eV`, `0` unreproduced rows),
- Recomputed energies and gradient norms of all 5 new putative global minimum records (`Zn_106`, `Cd_71`, `Cd_84`, `Cd_94`, `Cd_106`) from their coordinates in both `float64` (`||grad E||_2 <= 2.66e-14 < 1e-10`) and 55-digit `decimal.Decimal` (`||grad E||_2 <= 6.58e-35 < 1e-10`),
- Stored polished-CCD energies and SHA-256 digests for `Zn_106`, `Cd_71`, `Cd_84`, `Cd_94`, and `Cd_106` (cited by live `jon/structures/Gupta/<metal>/points/<N>` URL and SHA-256), which remain higher in energy by `0.000207 eV` to `0.004692 eV` (`> 1e-4 eV`),
- Recomputed exact $3N \times 3N$ analytical Hessian inertia (`6` rigid-body zero modes `||H Q_0||_F <= 1.31e-14 < 1e-6` and all `3N - 6` vibrational eigenvalues strictly `> 0.030 > 0`) for the 5 new structures.

## 2. Compile the C++17 Bidirectional Cascade & Tournament Solver
```sh
clang++ -O3 -std=c++17 -march=native -pthread how-we-built-it/Gupta_Cluster_Hunter.cc -o Gupta_Cluster_Hunter
```

