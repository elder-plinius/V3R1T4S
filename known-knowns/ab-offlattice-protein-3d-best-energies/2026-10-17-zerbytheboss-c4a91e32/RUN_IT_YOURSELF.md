# Run It Yourself

## 1. Verify the Four Claimed Record Conformations (`F89`, `2EWH`, `1CRN`, `1PCH`) and 23-Sequence Audit
From the package root, run:
```sh
sh verify-it-yourself/run_checks.sh
```
This executes `verify-it-yourself/check_ab_protein.py` using only the Python 3 standard library (`math` and 55-digit `decimal.Decimal`) in `< 2.5` seconds, verifying:
- Exact sequence strings and dimensions for `F89` (`L = 89, D = 173`), `2EWH` (`L = 98, D = 191`), `1CRN` (`L = 46, D = 87`), and `1PCH` (`L = 87, D = 169`),
- Exact 3D coordinate reconstruction with all unit bond lengths equal to `1.0` within `2.22e-16 < 1e-9`,
- Energies verified in both `float64` and 50-digit arithmetic (`-E* = 87.179252478342` on `F89`, `+0.747452 >= 0.5`; `-E* = 257.505676299754` on `2EWH`, `+0.431576`; `-E* = 95.720529801173` on `1CRN`, `+0.404630`; `-E* = 166.978883682418` on `1PCH`, `+0.259484`),
- Analytical and 4th-order Richardson finite-difference gradient norms `||grad E||_2 <= 6.69e-12 < 1e-8`,
- Complete reproduction of all 23 published conformations from Tables 11 and 12 of `arXiv:1903.01456`.

## 2. Compile the C++17 Basin-Hopping & Newton-Raphson Solver
```sh
clang++ -O3 -std=c++17 -march=native -pthread how-we-built-it/AB_Protein_Hunter.cc -o AB_Protein_Hunter
```
