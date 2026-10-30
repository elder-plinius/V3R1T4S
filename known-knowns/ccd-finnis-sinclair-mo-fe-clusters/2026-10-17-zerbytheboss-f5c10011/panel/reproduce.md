# V3R1T4S Reproduction Panel Audit (`reproduce.md`)

context: subagent (fresh invocation)
target_id: ccd-finnis-sinclair-mo-fe-clusters
cells: Mo_75, Mo_90, Fe_86, Fe_87, Fe_90, Fe_91, Fe_92, Fe_96, Fe_97, Fe_98, Fe_100
file: object/fs_mo_fe_11_records_and_196_audit.json
sha256: 215c879357f5bbbcc335e6dece2dc7ad12248abd428ef6b1c5ff9a4ba23af249

## 1. Quoted Mathematical Definition (Finnis-Sinclair 1984 Mo and 1986 Modified Fe)

Before reading `verify-it-yourself/check_fs_clusters.py`, an independent checker was written directly from the mathematical specification in M. W. Finnis and J. E. Sinclair (*"A simple empirical N-body potential for transition metals"*, *Philosophical Magazine A* 50, 45-55, 1984; erratum *Philosophical Magazine A* 53, 161, 1986) and J. A. Elliott, Y. Shibuta, and D. J. Wales (*"Global minima of transition metal clusters described by Finnis-Sinclair potentials: a comparison with semi-empirical molecular orbital theory"*, *Philosophical Magazine* 89, 3311-3332, 2009):

- **Total Potential Energy Function**:
  For an $N$-atom cluster with Cartesian coordinates $r_1, \dots, r_N \in \mathbb{R}^3$ and pairwise Euclidean distances $r_{ij} = \|r_i - r_j\|_2$:
  $$
  E = \frac{1}{2} \sum_{i=1}^N \sum_{j \neq i} V(r_{ij}) - A \sum_{i=1}^N \sqrt{\rho_i}, \qquad \rho_i = \sum_{j \neq i} \phi(r_{ij})
  $$
- **Pairwise Repulsion $V(r)$ and Cohesive Density $\phi(r)$**:
  - For $r$ below cutoff $c$: $V(r) = (r - c)^2 (c_0 + c_1 r + c_2 r^2)$, and $V(r) = 0$ for $r \ge c$.
  - For $r$ below cutoff $d$: $\phi(r) = (r - d)^2 + \beta \frac{(r - d)^3}{d}$, and $\phi(r) = 0$ for $r \ge d$.
- **Published Parameter Sets**:
  - **Mo (1984)**: $d = 4.114825\text{ \AA}$, $A = 1.887117\text{ eV}$, $\beta = 0.0$, $c = 3.25\text{ \AA}$, $c_0 = 43.4475218\text{ eV}$, $c_1 = -31.9332978\text{ eV/\AA}$, $c_2 = 6.0804249\text{ eV/\AA}^2$.
  - **Fe (1986 modified)**: $d = 3.569745\text{ \AA}$, $A = 1.828905\text{ eV}$, $\beta = 1.8$, $c = 3.4\text{ \AA}$, $c_0 = 1.2371147\text{ eV}$, $c_1 = -0.3592185\text{ eV/\AA}$, $c_2 = -0.0385607\text{ eV/\AA}^2$.

## 2. Independent Verification Results on `object/fs_mo_fe_11_records_and_196_audit.json`

1. **File Integrity & `INDEX.csv` Verification**:
   - All 11 rows in `INDEX.csv` (`Mo_75`, `Mo_90`, `Fe_86`, `Fe_87`, `Fe_90`, `Fe_91`, `Fe_92`, `Fe_96`, `Fe_97`, `Fe_98`, `Fe_100`) reference `object/fs_mo_fe_11_records_and_196_audit.json` with exact SHA-256 match `215c879357f5bbbcc335e6dece2dc7ad12248abd428ef6b1c5ff9a4ba23af249`.

2. **Calibration on Posted CCD Point Files & 196-Row Audit (`ccd_196_point_files_audit`, Partial Win `p1`)**:
   - Across all $2 \times 98 = 196$ rows (`Mo_3` through `Mo_100` and `Fe_3` through `Fe_100`) in `ccd_196_point_files_audit` (citing live `FS_Mo/points/<N>` and `FS_Fe/points/<N>` URLs and SHA-256 digests without vendoring third-party coordinates), every posted CCD energy matches within `9.766e-11 eV` on Mo and `9.415e-11 eV` on Fe (well within the `1e-7 eV` calibration tolerance), and Newton-polishing lowers any posted CCD structure by at most `1.012e-10 eV`.

3. **Independent `float64`, 55-Digit `mpmath`, Gradient, and $3N \times 3N$ Hessian Spectrum Audit across All 11 Putative Global Minimum Clusters**:

| Cluster | $N$ | CCD Table $E$ (eV) | `float64` $E^*$ (eV) | 55-Digit `mpmath` $E^*$ (eV) | $\Delta E$ vs CCD (eV) | $\|\nabla E\|_2$ (`float64`) | $\|\nabla E\|_2$ (`mp55`) | Hessian Zero / Neg / Pos Modes | Vibrational $\lambda_{\min} \dots \lambda_{\max}$ |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| **`Mo_75`** | `75` | `-439.4197932305` | `-439.5640256673` | `-439.56402566727096373` | **`-0.144232`** | `1.228e-13` | `9.179e-28` | `6 / 0 / 219` | `0.4042 .. 29.2452` |
| **`Mo_90`** | `90` | `-532.7899433214` | `-533.2142178271` | `-533.21421782713398599` | **`-0.424275`** | `1.262e-13` | `1.201e-27` | `6 / 0 / 264` | `0.4171 .. 28.6913` |
| **`Fe_86`** | `86` | `-312.6006513052` | `-312.7609188697` | `-312.76091886972428406` | **`-0.160268`** | `2.348e-14` | `1.100e-28` | `6 / 0 / 252` | `0.5829 .. 22.7042` |
| **`Fe_87`** | `87` | `-316.4759023549` | `-316.6115843892` | `-316.61158438917758044` | **`-0.135682`** | `2.302e-14` | `9.836e-29` | `6 / 0 / 255` | `0.5961 .. 22.7383` |
| **`Fe_90`** | `90` | `-327.8503707653` | `-327.9864583540` | `-327.98645835400958119` | **`-0.136088`** | `2.861e-14` | `1.007e-28` | `6 / 0 / 264` | `0.5696 .. 23.0856` |
| **`Fe_91`** | `91` | `-331.9072022873` | `-332.0252838865` | `-332.02528388653131979` | **`-0.118082`** | `2.364e-14` | `1.012e-28` | `6 / 0 / 267` | `0.5558 .. 23.0751` |
| **`Fe_92`** | `92` | `-335.9034309081` | `-335.9470373457` | `-335.94703734566128495` | **`-0.043606`** | `2.765e-14` | `1.065e-28` | `6 / 0 / 270` | `0.5482 .. 22.9089` |
| **`Fe_96`** | `96` | `-351.2027399452` | `-351.2401491626` | `-351.24014916262727257` | **`-0.037409`** | `2.376e-14` | `1.140e-28` | `6 / 0 / 282` | `0.5600 .. 23.2693` |
| **`Fe_97`** | `97` | `-354.9919830214` | `-355.1385265715` | `-355.13852657152233828` | **`-0.146544`** | `2.757e-14` | `1.179e-28` | `6 / 0 / 285` | `0.5620 .. 23.6421` |
| **`Fe_98`** | `98` | `-358.8031191667` | `-359.0082985625` | `-359.00829856251313176` | **`-0.205179`** | `2.262e-14` | `1.002e-28` | `6 / 0 / 288` | `0.5587 .. 23.5092` |
| **`Fe_100`** | `100` | `-366.5806583336` | `-366.6082856510` | `-366.60828565103384534` | **`-0.027627`** | `2.641e-14` | `1.139e-28` | `6 / 0 / 294` | `0.5792 .. 23.4686` |

   - Every one of the 11 clusters lowers the Cambridge Cluster Database putative global minimum energy by `-0.027627 eV` to `-0.424275 eV` (`276x` to `4,242x` the `1e-4 eV` threshold), has gradient norm at or below `1.262e-13` in `float64` and `1.201e-27` in 55-digit arithmetic (well below `1e-10`), and has an exact $3N \times 3N$ analytical Hessian with `6` near-zero rigid-body modes (`|\lambda| \le 1e-6`), `0` negative eigenvalues, and all $3N - 6$ vibrational eigenvalues strictly positive (`\lambda_7 \ge 0.4042`).

## 3. Execution of `verify-it-yourself/run_checks.sh`

Running `sh verify-it-yourself/run_checks.sh` from the package root completed in `4` seconds with exit code `0` and output:
```text
Calibrated Mo (98 files, max |dE|=9.77e-11 eV) and Fe (98 files, max |dE|=9.42e-11 eV) < 1e-7 eV.
Verified Mo_75 : E* = -439.5640256673 eV (CCD = -439.4197932305, dE =  -0.144232 eV, ||g||_f64=1.23e-13, ||g||_dec=9.18e-28, ||H Q0||=9.03e-15)
Verified Mo_90 : E* = -533.2142178271 eV (CCD = -532.7899433214, dE =  -0.424275 eV, ||g||_f64=1.26e-13, ||g||_dec=1.20e-27, ||H Q0||=8.62e-15)
Verified Fe_86 : E* = -312.7609188697 eV (CCD = -312.6006513052, dE =  -0.160268 eV, ||g||_f64=2.36e-14, ||g||_dec=1.10e-28, ||H Q0||=5.75e-15)
Verified Fe_87 : E* = -316.6115843892 eV (CCD = -316.4759023549, dE =  -0.135682 eV, ||g||_f64=2.30e-14, ||g||_dec=9.84e-29, ||H Q0||=5.81e-15)
Verified Fe_90 : E* = -327.9864583540 eV (CCD = -327.8503707653, dE =  -0.136088 eV, ||g||_f64=2.86e-14, ||g||_dec=1.01e-28, ||H Q0||=5.93e-15)
Verified Fe_91 : E* = -332.0252838865 eV (CCD = -331.9072022873, dE =  -0.118082 eV, ||g||_f64=2.36e-14, ||g||_dec=1.01e-28, ||H Q0||=5.73e-15)
Verified Fe_92 : E* = -335.9470373457 eV (CCD = -335.9034309081, dE =  -0.043606 eV, ||g||_f64=2.76e-14, ||g||_dec=1.07e-28, ||H Q0||=5.39e-15)
Verified Fe_96 : E* = -351.2401491626 eV (CCD = -351.2027399452, dE =  -0.037409 eV, ||g||_f64=2.38e-14, ||g||_dec=1.14e-28, ||H Q0||=5.73e-15)
Verified Fe_97 : E* = -355.1385265715 eV (CCD = -354.9919830214, dE =  -0.146544 eV, ||g||_f64=2.76e-14, ||g||_dec=1.18e-28, ||H Q0||=5.98e-15)
Verified Fe_98 : E* = -359.0082985625 eV (CCD = -358.8031191667, dE =  -0.205179 eV, ||g||_f64=2.26e-14, ||g||_dec=1.00e-28, ||H Q0||=5.57e-15)
Verified Fe_100: E* = -366.6082856510 eV (CCD = -366.5806583336, dE =  -0.027627 eV, ||g||_f64=2.64e-14, ||g||_dec=1.14e-28, ||H Q0||=5.55e-15)
Verified all 11 Finnis-Sinclair putative global minimum records + all 196 CCD Mo/Fe cluster point files.
PASS
```

pass: true
