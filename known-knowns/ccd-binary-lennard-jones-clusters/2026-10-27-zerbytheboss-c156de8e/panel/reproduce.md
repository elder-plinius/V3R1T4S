# Reproduction Audit (`ccd-binary-lennard-jones-clusters`)

- Context: Independent coordinate re-evaluation audit of the package.

1. Evaluated the exact pairwise binary Lennard-Jones potential without cutoff from 3D Cartesian coordinates:
   `E = sum_{i<j} 4 * ((sigma_ij / r_ij)^12 - (sigma_ij / r_ij)^6)`
   with `sigma_AA = 1.0`, `sigma_BB = ratio`, and Lorentz-Berthelot arithmetic mean `sigma_AB = (1.0 + ratio) / 2.0`.
2. Verified analytical positive control (`N=2` dimer at `r = 2^(1/6)` gives `-1.000000000000`) and negative control (`r = 1.25` gives `-0.773698093056 > -1.0`), plus the analytical `3N x 3N` Hessian zero-mode threshold (`|lambda| < 1e-6`, `max_zero_eval = 1.69e-14`) on polished canonical cluster `1.05/5`.
3. Re-evaluated from 3D coordinates all 666 point files stored in `verify-it-yourself/data/blj_all_666_point_files.json.gz`:
   - `576` canonical `all.tar` point files (`max header reproduction error = 4.99e-11 < 1e-5`).
   - `27` live `new` point files (`1.05/43new`, `1.05/90new`, `1.1/47new`, `1.1/62new..65new`, `1.1/67new`, `1.1/70new..81new`, `1.1/83new..89new`) that return `HTTP 200` on the Cambridge server (`max header error = 4.89e-11 < 1e-5`; all `27/27` reproduce `table.html` within `5e-7 < 1e-5`).
   - `63` point files across the 4 hosted improvement archives (`Wenqi_Tao_BLJ` [12], `Wenqi_Tao_BLJ2` [17], `Istvan_Kolossvary` [17], `NEW_BINARY_LJ_MINIMA` [17]; `max header error = 9.14e-8 < 1e-5`).
4. Confirmed `sh verify-it-yourself/run_checks.sh` exits `0` and prints `PASS`, and corrupting a digit of `object/blj_600_cell_audit.csv` causes the checker to print `FAIL` and exit non-zero.

pass: true
