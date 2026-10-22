# Gupta Metal Nanoclusters (`Zn`, `Cd`, `Pb`, `Na_Gupta`): 5 New Putative Global Minima (`Zn_106`, `Cd_71`, `Cd_84`, `Cd_94`, `Cd_106`) and Complete 780-Point-File Calibration Audit

## What
Explicit 3D Cartesian coordinate sets in object/gupta_zn_cd_5_records_and_780_audit.json for 5 Gupta metal nanoclusters (Zn_106, Cd_71, Cd_84, Cd_94, and Cd_106) achieve strict local-minimum energies under the exact calibrated Cleri-Rosato Gupta parameter sets (Zn_106: -141.9309047390 vs -141.928489 eV, -0.002416 eV; Cd_71: -82.3022257380 vs -82.302019 eV, -0.000207 eV; Cd_84: -97.4196981104 vs -97.415006 eV, -0.004692 eV; Cd_94: -109.0494558230 vs -109.048698 eV, -0.000758 eV; and Cd_106: -123.0018760970 vs -123.000416 eV, -0.001460 eV), verified in both float64 (gradient norm <= 2.43e-14) and 55-digit Decimal arithmetic (gradient norm <= 6.58e-35) with 6 near-zero rigid-body Hessian modes and 3N - 6 strictly positive vibrational eigenvalues, alongside a full parameter calibration and reproduction audit of all 780 posted Zn, Cd, Pb, Pb_Gupta.rar, and Na_Gupta point files (p1, p3).

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last output line: `PASS` (runs in `< 9` seconds using only the Python 3 standard library `math`, `decimal.Decimal`, and `json`).

## Compared To
All comparisons are against the Cambridge Cluster Database Gupta tables of J. P. K. Doye (*"Everything you wanted to know about Zn and Cd clusters (if they are described by a Gupta potential)"*, *Physical Review B* 68, 195418, 2003; `https://www-wales.ch.cam.ac.uk/~wales/CCD/Gupta.html`, `https://www-wales.ch.cam.ac.uk/~wales/CCD/Zn/zn.html`, and `https://www-wales.ch.cam.ac.uk/~wales/CCD/Cd/cd.html`, fetched on `2026-10-17T23:05:12Z` and recorded in `the-record-we-beat/snapshot_2026-10-17.md`):

| Cluster | $N$ | CCD Table Energy (eV) | Polished CCD Structure (eV) | Our New Minimum $E^*$ (eV) | Improvement $\Delta E$ (eV) | $\|\nabla E\|_2$ (`float64`) | $\|\nabla E\|_2$ (`Decimal50`) | Vibrational Hessian $\lambda_{\min} \dots \lambda_{\max}$ |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`Zn_106`** | `106` | `-141.928489` | `-141.9284893514` | **`-141.9309047390`** | **`-0.002416`** | `1.91e-14` | `6.50e-35` | `0.0957 .. 48.86` (`312/312 > 0`) |
| **`Cd_71`** | `71` | `-82.302019` | `-82.3020188326` | **`-82.3022257380`** | **`-0.000207`** | `2.04e-14` | `6.58e-35` | `0.0658 .. 69.21` (`207/207 > 0`) |
| **`Cd_84`** | `84` | `-97.415006` | `-97.4150057630` | **`-97.4196981104`** | **`-0.004692`** | `2.22e-14` | `5.63e-35` | `0.0600 .. 67.39` (`246/246 > 0`) |
| **`Cd_94`** | `94` | `-109.048698` | `-109.0486983843` | **`-109.0494558230`** | **`-0.000758`** | `1.95e-14` | `5.68e-35` | `0.0584 .. 52.39` (`276/276 > 0`) |
| **`Cd_106`** | `106` | `-123.000416` | `-123.0004155585` | **`-123.0018760970`** | **`-0.001460`** | `2.43e-14` | `6.02e-35` | `0.0388 .. 51.92` (`312/312 > 0`) |

### Complete 780-Point-File Calibration & Reproduction Audit (Partial Wins `p1` and `p3`)
We calibrated the exact Gupta potential parameters (`E = sum_i [ sum_{j!=i} A exp(-p(r_ij/r0 - 1)) - xi sqrt(sum_{j!=i} exp(-2q(r_ij/r0 - 1))) ]`, `r0 = 1`) and audited all 780 posted CCD Gupta point files (`Zn` `N = 3..125`, `Cd` `N = 3..125`, `Pb` `N = 3..150` + 9 `Pb_Gupta.rar` files, and `Na_Gupta` `N = 3..379`, embedded in `object/gupta_zn_cd_5_records_and_780_audit.json` under `ccd_780_point_files_audit`):
- **Exact Parameter Calibration (`< 1e-6 eV` across all 780 point files)**:
  - `Zn` (`123` files): `p = 9.689, q = 4.602, A = 0.1477 eV, xi = 0.8900 eV` (`max |dE| = 4.984e-7 eV < 1e-5 eV`).
  - `Cd` (`123` files): `p = 10.612, q = 5.206, A = 0.1420 eV, xi = 0.8117 eV` (`max |dE| = 4.955e-7 eV < 1e-5 eV`).
  - `Pb` (`148` table files + `9` `Pb_Gupta.rar` files): `p = 9.576, q = 3.648, A = 0.0980 eV, xi = 0.9140 eV` (`max |dE| = 4.998e-7 eV < 1e-5 eV`).
  - `Na_Gupta` (`377` files): `p = 10.130, q = 1.300, A = 0.0159554019 eV, xi = 0.2911347198 eV` (`max |dE| = 7.165e-7 eV < 1e-5 eV`).
- **Distinct Structural Basins**: Newton-polishing the posted CCD point files for `Zn_106`, `Cd_71`, `Cd_84`, `Cd_94`, and `Cd_106` lowers their energies by `< 5e-7 eV` (all within rounding of the 6-decimal CCD table values), confirming that all 5 new records reside in strictly distinct structural basins (`-0.000207 eV` to `-0.004692 eV` below the polished CCD structures).

## Not Claimed
- We do not claim that these 5 new local minima are the mathematical global minima of their respective cluster sizes; each is a verified strict local minimum in a distinct structural basin that lowers the putative global minimum in the Cambridge Cluster Database by `0.000207 eV` to `0.004692 eV` (`2.07x` to `46.9x` the `1e-4 eV` threshold).

## Credits
- **Contributor**: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`).
- **J. P. K. Doye, D. J. Wales, E. G. Noya, and A. Aguado** (*Physical Review B* 68, 195418, 2003; *Computational Materials Science* 35, 227, 2006; *European Physical Journal D* 43, 57, 2007) and the **Cambridge Cluster Database** for the benchmark `Zn`, `Cd`, `Pb`, and `Na_Gupta` tables and coordinate archives.
- **R. P. Gupta** (*Physical Review B* 23, 6265, 1981) and **F. Cleri and V. Rosato** (*Physical Review B* 48, 22, 1993) for the tight-binding second-moment approximation potential.
