# Criterion Skeptic Audit (`ccd-gupta-murrell-mottram-metal-clusters`)

context: subagent (fresh invocation)
target_id: ccd-gupta-murrell-mottram-metal-clusters
confirmed_scope: Explicit 3D Cartesian coordinate sets in object/gupta_zn_cd_5_records_and_780_audit.json for 5 Gupta metal nanoclusters (Zn_106, Cd_71, Cd_84, Cd_94, and Cd_106) achieve strict local-minimum energies under the exact calibrated Cleri-Rosato Gupta parameter sets (Zn_106: -141.9309047390 vs -141.928489 eV, -0.002416 eV; Cd_71: -82.3022257380 vs -82.302019 eV, -0.000207 eV; Cd_84: -97.4196981104 vs -97.415006 eV, -0.004692 eV; Cd_94: -109.0494558230 vs -109.048698 eV, -0.000758 eV; and Cd_106: -123.0018760970 vs -123.000416 eV, -0.001460 eV), verified in both float64 (gradient norm <= 2.43e-14) and 55-digit Decimal arithmetic (gradient norm <= 6.58e-35) with 6 near-zero rigid-body Hessian modes and 3N - 6 strictly positive vibrational eigenvalues, alongside a full parameter calibration and reproduction audit of all 780 posted Zn, Cd, Pb, Pb_Gupta.rar, and Na_Gupta point files (p1, p3).

## Clause-by-Clause Verification Against `targets.json`

1. **Per-Metal Gupta Parameter Calibration (`1e-5 eV` Requirement)**:
   - The target requires calibrating the exact Gupta potential parameter set used for each table by reproducing at least ten posted point-file energies to `1e-5 eV` for the 6-decimal Gupta tables.
   - `verify-it-yourself/check_gupta_clusters.py` calibrates `12` embedded point files per metal across `Zn` (`p = 9.689`, `q = 4.602`, `A = 0.1477 eV`, `xi = 0.8900 eV`, max deviation `4.67e-7 eV`), `Cd` (`p = 10.612`, `q = 5.206`, `A = 0.1420 eV`, `xi = 0.8117 eV`, max deviation `4.54e-7 eV`), `Pb` (`p = 9.576`, `q = 3.648`, `A = 0.0980 eV`, `xi = 0.9140 eV`, max deviation `4.60e-7 eV`), and `Na_Gupta` (`p = 10.130`, `q = 1.300`, `A = 0.0159554019 eV`, `xi = 0.2911347198 eV`, max deviation `4.93e-7 eV`).
   - Furthermore, all 780 posted Gupta point files across `Zn` (`N = 3..125`, `123` files), `Cd` (`N = 3..125`, `123` files), `Pb` (`N = 3..150`, `148` files plus `9` `Pb_Gupta.rar` improvement files), and `Na_Gupta` (`N = 3..379`, `377` files) reproduce their 6-decimal table energies within `7.17e-7 eV` (more than an order of magnitude tighter than the `1e-5 eV` threshold).

2. **Energy Improvements (`E*` Lower by at Least `1e-4 eV` vs Live CCD Table and Literature)**:
   - All 5 reported clusters (`Zn_106`, `Cd_71`, `Cd_84`, `Cd_94`, `Cd_106`) achieve total energies strictly lower by more than `1e-4 eV` than the live Cambridge Cluster Database tables (`Zn/table.html` and `Cd/table.html`, fetched `2026-10-17T23:05:12Z`) and the literature for the bulk-fitted Cleri-Rosato Gupta potential (Doye, *Phys. Rev. B* 68, 195418, 2003):
     - `Zn_106` (`N = 106`): `-141.9309047390 eV` vs `-141.928489 eV` (`-0.002416 eV`, `24.2x` threshold)
     - `Cd_71` (`N = 71`): `-82.3022257380 eV` vs `-82.302019 eV` (`-0.000207 eV`, `2.07x` threshold)
     - `Cd_84` (`N = 84`): `-97.4196981104 eV` vs `-97.415006 eV` (`-0.004692 eV`, `46.9x` threshold)
     - `Cd_94` (`N = 94`): `-109.0494558230 eV` vs `-109.048698 eV` (`-0.000758 eV`, `7.58x` threshold)
     - `Cd_106` (`N = 106`): `-123.0018760970 eV` vs `-123.000416 eV` (`-0.001460 eV`, `14.6x` threshold)

3. **High-Precision Stationarity (`||grad E||_2 <= 6.58e-35` in 55-Digit Decimal) and `3N x 3N` Hessian Spectrum**:
   - In IEEE 754 `float64`, all 5 structures have Euclidean gradient norm `<= 2.66e-14` (and `<= 2.43e-14` in the numpy evaluation), strictly below `1e-10`.
   - Using 45-decimal-place coordinates evaluated in 55-digit `decimal.Decimal` arithmetic (exceeding the 30-digit requirement), all 5 structures have Euclidean gradient norm `<= 6.58e-35` (strictly below `1e-10`) and agree with `float64` energies to within `1e-11 eV`.
   - For each of the 5 clusters, the exact analytical `3N x 3N` double-precision Hessian matrix has 6 rigid-body translation/rotation modes with residual `||H Q_0||_F <= 1.31e-14` (eigenvalues `|lambda| <= 3.88e-15`, well below `1e-6`), zero negative eigenvalues, and all `3N - 6` vibrational eigenvalues strictly positive (`>= 0.0388`, certified via shifted Cholesky factorization in the standalone verifier).

4. **Distinct Basin Verification and Partial Wins**:
   - Newton-polishing the posted CCD point files for `Zn_106`, `Cd_71`, `Cd_84`, `Cd_94`, and `Cd_106` lowers their energies by less than `5e-7 eV` (all within 6-decimal table rounding), so each polished CCD structure remains `+0.000207 eV` to `+0.004692 eV` higher in energy than our new minimum (confirming strictly distinct structural basins).
   - The package also provides a full calibration and reproduction audit of all 780 posted `Zn`, `Cd`, `Pb`, `Pb_Gupta.rar`, and `Na_Gupta` point files and delivers certified strict improvements across 5 cluster sizes.

5. **Pitfalls and Corruption Rejection**:
   - All five listed pitfalls in `targets.json` were verified: bulk-fitted Cleri-Rosato parameters calibrated per metal, avoidance of the `Pb` page prose typo, verification against `Pb_Gupta.rar`, distinct-basin verification above `1e-4 eV`, and exclusion of Aguado et al.'s cluster-refitted parameter sets.
   - Running `sh verify-it-yourself/run_checks.sh` exits `0` and prints `PASS`, and corrupting a digit of the object file causes the verifier to print `FAIL` and exit non-zero.

pass: true
