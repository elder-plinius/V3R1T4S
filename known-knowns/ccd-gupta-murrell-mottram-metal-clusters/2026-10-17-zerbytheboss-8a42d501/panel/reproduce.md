# V3R1T4S Reproduction Panel Audit (`reproduce.md`)

context: subagent (fresh invocation)
target_id: ccd-gupta-murrell-mottram-metal-clusters
cells: Zn_106, Cd_71, Cd_84, Cd_94, Cd_106
file: object/gupta_zn_cd_5_records_and_780_audit.json
sha256: 50c4a29c08cbe9c1e2a9a0790ce53e5a65e9cb2c11de0e78ea3199d1ba7db44c

## 1. Quoted Mathematical Definition (Cleri-Rosato Gupta Many-Body Potential)

Before reading `verify-it-yourself/check_gupta_clusters.py`, an independent checker was written directly from the mathematical specification in R. P. Gupta (*"Lattice relaxation at a metal surface"*, *Physical Review B* 23, 6265, 1981), F. Cleri and V. Rosato (*"Tight-binding potentials for transition metals and alloys"*, *Physical Review B* 48, 22, 1993), and J. P. K. Doye (*"Identifying structural patterns in 'disordered' metal clusters"*, *Physical Review B* 68, 195418, 2003):

- **Total Potential Energy Function**:
  For an $N$-atom cluster in reduced nearest-neighbor coordinates ($r_0 = 1$) with Cartesian positions $r_1, \dots, r_N \in \mathbb{R}^3$ and pairwise Euclidean distances $r_{ij} = \|r_i - r_j\|_2$:
  $$
  E = \sum_{i=1}^N \left[ \sum_{j \neq i} A \exp\bigl(-p(r_{ij} / r_0 - 1)\bigr) - \xi \sqrt{\sum_{j \neq i} \exp\bigl(-2q(r_{ij} / r_0 - 1)\bigr)} \right]
  $$
- **Calibrated Parameter Sets ($r_0 = 1$)**:
  - **Zn**: $p = 9.689$, $q = 4.602$, $A = 0.1477\text{ eV}$, $\xi = 0.8900\text{ eV}$.
  - **Cd**: $p = 10.612$, $q = 5.206$, $A = 0.1420\text{ eV}$, $\xi = 0.8117\text{ eV}$.
  - **Pb**: $p = 9.576$, $q = 3.648$, $A = 0.0980\text{ eV}$, $\xi = 0.9140\text{ eV}$.
  - **Na\_Gupta**: $p = 10.130$, $q = 1.300$, $A = 0.0159554019\text{ eV}$, $\xi = 0.2911347198\text{ eV}$.

## 2. Independent Verification Results on `object/gupta_zn_cd_5_records_and_780_audit.json`

1. **File Integrity & `INDEX.csv` Verification**:
   - All 5 rows in `INDEX.csv` (`Zn_106`, `Cd_71`, `Cd_84`, `Cd_94`, `Cd_106`) reference `object/gupta_zn_cd_5_records_and_780_audit.json` with exact SHA-256 match `50c4a29c08cbe9c1e2a9a0790ce53e5a65e9cb2c11de0e78ea3199d1ba7db44c`.

2. **Parameter Calibration on 48 Embedded Point Files & 780-Row Audit (`ccd_780_point_files_audit`)**:
   - Independently evaluating all 48 embedded calibration point files (`12` per metal across `Zn`, `Cd`, `Pb`, and `Na_Gupta`) reproduces the posted 6-decimal Cambridge Cluster Database energies with maximum absolute difference `4.673e-7 eV` (`Zn`), `4.539e-7 eV` (`Cd`), `4.596e-7 eV` (`Pb`), and `4.933e-7 eV` (`Na_Gupta`), all well within the `1e-5 eV` calibration requirement.
   - Across all 780 posted point files (`123` `Zn`, `123` `Cd`, `148` `Pb` table + `9` `Pb_Gupta.rar`, and `377` `Na_Gupta`) in `ccd_780_point_files_audit`, every posted CCD energy matches within `7.165e-7 eV` (`0` unreproduced rows over `1e-5 eV`).

3. **Independent `float64`, 55-Digit `mpmath`, Distinct-Basin, Gradient, and $3N \times 3N$ Hessian Spectrum Audit across All 5 Record Clusters**:

| Cluster | $N$ | CCD Table $E$ (eV) | Polished CCD $E$ (eV) | `float64` $E^*$ (eV) | 55-Digit `mpmath` $E^*$ (eV) | $\Delta E$ vs CCD (eV) | $\|\nabla E\|_2$ (`float64`) | $\|\nabla E\|_2$ (`mp55`) | Hessian Zero / Neg / Pos Modes | Vibrational $\lambda_{\min} \dots \lambda_{\max}$ |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| **`Zn_106`** | `106` | `-141.928489` | `-141.9284893514` | `-141.9309047390` | `-141.93090473902379015` | **`-0.002416`** | `2.021e-14` | `6.501e-35` | `6 / 0 / 312` | `0.0957 .. 48.8551` |
| **`Cd_71`** | `71` | `-82.302019` | `-82.3020188326` | `-82.3022257380` | `-82.302225737955977359` | **`-0.000207`** | `2.057e-14` | `6.585e-35` | `6 / 0 / 207` | `0.0658 .. 69.2056` |
| **`Cd_84`** | `84` | `-97.415006` | `-97.4150057630` | `-97.4196981104` | `-97.419698110415354234` | **`-0.004692`** | `1.990e-14` | `5.626e-35` | `6 / 0 / 246` | `0.0600 .. 67.3902` |
| **`Cd_94`** | `94` | `-109.048698` | `-109.0486983843` | `-109.0494558230` | `-109.04945582298477224` | **`-0.000758`** | `1.871e-14` | `5.677e-35` | `6 / 0 / 276` | `0.0584 .. 52.3866` |
| **`Cd_106`** | `106` | `-123.000416` | `-123.0004155585` | `-123.0018760970` | `-123.00187609704602258` | **`-0.001460`** | `2.346e-14` | `6.019e-35` | `6 / 0 / 312` | `0.0388 .. 51.9185` |

   - **Distinct-Basin Verification**: For each of the 5 clusters, the polished CCD reference structure (`ccd_polished_coords_float64`) has gradient norm below `1e-13` and remains within `5e-7 eV` of the 6-decimal CCD table value, whereas our new local minimum lies `-0.000207 eV` to `-0.004692 eV` lower (`2.07x` to `46.9x` the `1e-4 eV` Full Win threshold).
   - **Stationarity & Strict Local Minima**: Every new minimum has gradient norm at or below `2.346e-14` in `float64` (`2.66e-14` in pure-Python summation order) and `6.585e-35` in 55-digit arithmetic (well below `1e-10`), and its exact $3N \times 3N$ analytical Hessian has `6` near-zero rigid-body modes (`|\lambda| \le 3.80e-15`, well below `1e-6`), `0` negative eigenvalues, and all $3N - 6$ vibrational eigenvalues strictly positive (`\lambda_7 \ge 0.0388`).

## 3. Execution of `verify-it-yourself/run_checks.sh`

Running `sh verify-it-yourself/run_checks.sh` from the package root completed in `6` seconds with exit code `0` and output:
```text
Calibrated Zn       (12 files, max |dE| = 4.67e-07 eV within 1e-5 eV)
Calibrated Cd       (12 files, max |dE| = 4.54e-07 eV within 1e-5 eV)
Calibrated Pb       (12 files, max |dE| = 4.60e-07 eV within 1e-5 eV)
Calibrated Na_Gupta (12 files, max |dE| = 4.93e-07 eV within 1e-5 eV)
Verified Zn_106  : E* = -141.9309047390 eV (CCD = -141.928489, dE =  -0.002416 eV, ||g||_f64=2.03e-14, ||g||_dec=6.50e-35, ||H Q0||=1.31e-14)
Verified Cd_71   : E* = -82.3022257380 eV (CCD =  -82.302019, dE =  -0.000207 eV, ||g||_f64=2.12e-14, ||g||_dec=6.58e-35, ||H Q0||=1.27e-14)
Verified Cd_84   : E* = -97.4196981104 eV (CCD =  -97.415006, dE =  -0.004692 eV, ||g||_f64=2.18e-14, ||g||_dec=5.63e-35, ||H Q0||=1.21e-14)
Verified Cd_94   : E* = -109.0494558230 eV (CCD = -109.048698, dE =  -0.000758 eV, ||g||_f64=2.07e-14, ||g||_dec=5.68e-35, ||H Q0||=1.24e-14)
Verified Cd_106  : E* = -123.0018760970 eV (CCD = -123.000416, dE =  -0.001460 eV, ||g||_f64=2.66e-14, ||g||_dec=6.02e-35, ||H Q0||=1.22e-14)
Verified all 5 Gupta putative global minimum records + all 780 CCD point files.
PASS
```

pass: true
