# Run It Yourself (`ccd-dzugutov-zetterling-polytetrahedral-clusters`)

## 1. Standalone Zero-Dependency Verification (~10 seconds)

Run the standalone verification script (requires only Python 3 standard library):

```sh
sh verify-it-yourself/run_checks.sh
```

This executes `verify-it-yourself/check_dzugutov_clusters.py` on `object/dzugutov_zetterling_20_records_and_502_audit.json`, which independently verifies from first principles:
1. All 48 embedded calibration cluster coordinate sets (12 each for `Dzugutov`, `mDzugutov`, `Z1`, and `Z2`), confirming that every recomputed energy matches the live Cambridge Cluster Database (CCD) table within `< 1e-6` (`max |dE| <= 4.797e-7`).
2. The complete 502-cluster CCD reproduction audit (`98` `Dzugutov`, `248` `mDzugutov`, `78` `Z1`, `78` `Z2`), including the 5 corrupted central-atom origin coordinates in `Z1_13`, `Z1_25`, `Z1_33`, `Z1_37`, and `Z2_25` (`p2`).
3. All 20 new lower-energy global minimum records (`4` on `mDzugutov` including `3` in $N \in 101\dots 250$ satisfying `p1`, `10` on `Z1`, `6` on `Z2`) in both `float64` and 55-digit `decimal.Decimal` arithmetic (`||grad E||_2 < 1e-10`), confirming strict improvement by at least `1e-4` over both the live CCD table and the polished posted CCD point file, plus pure-stdlib Cholesky verification that the $3N \times 3N$ analytical Hessian has 6 rigid-body zero modes (`< 1e-6`) and 0 negative eigenvalues ($\lambda_7 > 0.20$).

## 2. Rebuilding the C++17 Solver (`how-we-built-it/Dzugutov_Cluster_Hunter.cc`)

To compile and run the multi-threaded C++17 polytetrahedral cluster solver from source:

```sh
clang++ -O3 -std=c++17 -pthread how-we-built-it/Dzugutov_Cluster_Hunter.cc -o Dzugutov_Cluster_Hunter
./Dzugutov_Cluster_Hunter
```
