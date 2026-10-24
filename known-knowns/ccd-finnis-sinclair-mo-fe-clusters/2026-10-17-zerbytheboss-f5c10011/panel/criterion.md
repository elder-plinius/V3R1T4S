# Criterion Skeptic Audit (`ccd-finnis-sinclair-mo-fe-clusters`)

context: subagent (fresh invocation)
target_id: ccd-finnis-sinclair-mo-fe-clusters
confirmed_scope: Explicit 3D Cartesian coordinate sets in object/fs_mo_fe_11_records_and_196_audit.json for 11 Finnis-Sinclair transition-metal nanoclusters (Mo_75, Mo_90, Fe_86, Fe_87, Fe_90, Fe_91, Fe_92, Fe_96, Fe_97, Fe_98, and Fe_100) achieve strict local-minimum energies under the exact calibrated Finnis-Sinclair (1984 Mo and 1986 modified Fe) parameter sets (Mo_75: -439.5640256673 vs -439.4197932305 eV, -0.144232 eV; Mo_90: -533.2142178271 vs -532.7899433214 eV, -0.424275 eV; Fe_86: -312.7609188697 vs -312.6006513052 eV, -0.160268 eV; Fe_87: -316.6115843892 vs -316.4759023549 eV, -0.135682 eV; Fe_90: -327.9864583540 vs -327.8503707653 eV, -0.136088 eV; Fe_91: -332.0252838865 vs -331.9072022873 eV, -0.118082 eV; Fe_92: -335.9470373457 vs -335.9034309081 eV, -0.043606 eV; Fe_96: -351.2401491626 vs -351.2027399452 eV, -0.037409 eV; Fe_97: -355.1385265715 vs -354.9919830214 eV, -0.146544 eV; Fe_98: -359.0082985625 vs -358.8031191667 eV, -0.205179 eV; and Fe_100: -366.6082856510 vs -366.5806583336 eV, -0.027627 eV), verified in both float64 (gradient norm <= 1.26e-13) and 55-digit Decimal arithmetic (gradient norm <= 1.20e-27) with 6 near-zero rigid-body Hessian modes and 3N - 6 strictly positive vibrational eigenvalues, alongside a full reproduction and polishing audit of all 196 posted Mo and Fe point files (p1).

## Clause-by-Clause Verification Against `targets.json`

1. **Per-Metal Finnis-Sinclair Parameter Calibration (`1e-7 eV` Requirement)**:
   - The target requires first calibrating the exact Finnis-Sinclair potential parameters on at least ten posted point files per metal to within `1e-7 eV`, noting the pitfall that `Mo` uses the 1984 parameters (`d = 4.114825`, `A = 1.887117`, `beta = 0.0`, `c = 3.25`, `c0 = 43.4475218`, `c1 = -31.9332978`, `c2 = 6.0804249`) while `Fe` uses the 1986 modified parameters (`d = 3.569745`, `A = 1.828905`, `beta = 1.8`, `c = 3.40`, `c0 = 1.2371147`, `c1 = -0.3592185`, `c2 = -0.0385607`).
   - `verify-it-yourself/check_fs_clusters.py` calibrates 11 embedded `Mo` point files (maximum deviation `4.73e-11 eV`) and 18 embedded `Fe` point files (maximum deviation `4.70e-11 eV`), plus all 196 posted `Mo_3`..`Mo_100` and `Fe_3`..`Fe_100` point files (maximum deviation `9.77e-11 eV` across all 196 files), more than three orders of magnitude tighter than the `1e-7 eV` threshold.

2. **Energy Improvements (`E*` Lower by at Least `1e-4 eV` vs Live CCD Table and Literature)**:
   - All 11 reported clusters (`Mo_75`, `Mo_90`, `Fe_86`, `Fe_87`, `Fe_90`, `Fe_91`, `Fe_92`, `Fe_96`, `Fe_97`, `Fe_98`, `Fe_100`) have atom counts `N` in `3..100` and achieve total energies strictly lower than the live Cambridge Cluster Database tables (`moly_fs.html` and `iron_fs.html`, fetched `2026-10-17T20:27:05Z`) and the literature:
     - `Mo_75`: `-439.5640256673 eV` vs `-439.4197932305 eV` (`-0.144232 eV`, `1,442x` threshold)
     - `Mo_90`: `-533.2142178271 eV` vs `-532.7899433214 eV` (`-0.424275 eV`, `4,242x` threshold)
     - `Fe_86`: `-312.7609188697 eV` vs `-312.6006513052 eV` (`-0.160268 eV`, `1,602x` threshold)
     - `Fe_87`: `-316.6115843892 eV` vs `-316.4759023549 eV` (`-0.135682 eV`, `1,356x` threshold)
     - `Fe_90`: `-327.9864583540 eV` vs `-327.8503707653 eV` (`-0.136088 eV`, `1,360x` threshold)
     - `Fe_91`: `-332.0252838865 eV` vs `-331.9072022873 eV` (`-0.118082 eV`, `1,180x` threshold)
     - `Fe_92`: `-335.9470373457 eV` vs `-335.9034309081 eV` (`-0.043606 eV`, `436x` threshold)
     - `Fe_96`: `-351.2401491626 eV` vs `-351.2027399452 eV` (`-0.037409 eV`, `374x` threshold)
     - `Fe_97`: `-355.1385265715 eV` vs `-354.9919830214 eV` (`-0.146544 eV`, `1,465x` threshold)
     - `Fe_98`: `-359.0082985625 eV` vs `-358.8031191667 eV` (`-0.205179 eV`, `2,051x` threshold)
     - `Fe_100`: `-366.6082856510 eV` vs `-366.5806583336 eV` (`-0.027627 eV`, `276x` threshold)

3. **High-Precision Stationarity (`||grad E||_2 <= 1.20e-27` in 55-Digit Decimal) and `3N x 3N` Hessian Spectrum**:
   - In IEEE 754 `float64`, all 11 structures have gradient Euclidean norm `<= 1.26e-13` (well below `1e-10`).
   - Using 32-decimal-place coordinates evaluated in 55-digit `decimal.Decimal` arithmetic (exceeding the 30-digit requirement), all 11 structures have gradient norm `<= 1.20e-27` (well below `1e-10`) and agree with `float64` energies to within `1e-12 eV`.
   - For each of the 11 clusters, the exact analytical `3N x 3N` double-precision Hessian matrix has 6 rigid-body translation/rotation modes with residual `||H Q_0||_F <= 9.03e-15` (well below `1e-6`), zero negative eigenvalues, and all `3N - 6` vibrational eigenvalues strictly positive (`>= 0.4042` for `Mo` and `>= 0.5482` for `Fe`, certified via shifted Cholesky factorization in the standalone verifier).

4. **Distinct Basin Verification and Partial Win `p1` (Complete 196-Point-File Audit)**:
   - Polishing the posted CCD structures for all 11 record cluster sizes lowers their energies by at most `1.1e-10 eV`, so each polished CCD structure remains `0.027627 eV` to `0.424275 eV` higher in energy than our new minimum (confirming strictly distinct structural basins).
   - For Partial Win `p1`, all `2 x 98 = 196` posted point files (`Mo_3`..`Mo_100` and `Fe_3`..`Fe_100`) were recomputed and Newton-polished: zero point files deviate from their posted 10-decimal table energies by more than `9.77e-11 eV` (threshold `1e-6 eV`), and zero posted point files lower by more than `1.9e-10 eV` upon polishing (threshold `1e-4 eV`).

5. **Pitfalls and Corruption Rejection**:
   - All four pitfalls in `targets.json` (1984 Mo vs 1986 modified Fe parameters, exact cubic spline cutoffs `c` and `d`, 10-decimal under-convergence vs true basin separation, and total cluster energy sign convention) were verified.
   - Running `sh verify-it-yourself/run_checks.sh` exits `0` and prints `PASS`, and corrupting a digit of the object file causes the verifier to print `FAIL` and exit non-zero.

pass: true
