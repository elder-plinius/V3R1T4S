# Finnis-Sinclair Molybdenum and Iron Nanoclusters (`N = 3..100`): 11 New Putative Global Minima (`Mo_75`, `Mo_90`, `Fe_86`–`Fe_100`) and Complete 196-Cluster Audit

## What
Explicit 3D Cartesian coordinate sets in object/fs_mo_fe_11_records_and_196_audit.json for 11 Finnis-Sinclair transition-metal nanoclusters (Mo_75, Mo_90, Fe_86, Fe_87, Fe_90, Fe_91, Fe_92, Fe_96, Fe_97, Fe_98, and Fe_100) achieve strict local-minimum energies under the exact calibrated Finnis-Sinclair (1984 Mo and 1986 modified Fe) parameter sets (Mo_75: -439.5640256673 vs -439.4197932305 eV, -0.144232 eV; Mo_90: -533.2142178271 vs -532.7899433214 eV, -0.424275 eV; Fe_86: -312.7609188697 vs -312.6006513052 eV, -0.160268 eV; Fe_87: -316.6115843892 vs -316.4759023549 eV, -0.135682 eV; Fe_90: -327.9864583540 vs -327.8503707653 eV, -0.136088 eV; Fe_91: -332.0252838865 vs -331.9072022873 eV, -0.118082 eV; Fe_92: -335.9470373457 vs -335.9034309081 eV, -0.043606 eV; Fe_96: -351.2401491626 vs -351.2027399452 eV, -0.037409 eV; Fe_97: -355.1385265715 vs -354.9919830214 eV, -0.146544 eV; Fe_98: -359.0082985625 vs -358.8031191667 eV, -0.205179 eV; and Fe_100: -366.6082856510 vs -366.5806583336 eV, -0.027627 eV), verified in both float64 (gradient norm <= 1.26e-13) and 55-digit Decimal arithmetic (gradient norm <= 1.20e-27) with 6 near-zero rigid-body Hessian modes and 3N - 6 strictly positive vibrational eigenvalues, alongside a full reproduction and polishing audit of all 196 posted Mo and Fe point files (p1).

## Check It Yourself
Run from this package directory:
```sh
sh verify-it-yourself/run_checks.sh
```
Expected last output line: `PASS` (runs in `< 7` seconds using only the Python 3 standard library `math`, `decimal.Decimal`, and `json`).

## Compared To
All comparisons are against the Cambridge Cluster Database tables of J. A. Elliott, Y. Shibuta, and D. J. Wales (*"Global minima of transition metal clusters described by Finnis-Sinclair potentials: a comparison with semi-empirical molecular orbital theory"*, *Philosophical Magazine* 89, 3311-3332, 2009; `https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Mo/moly_fs.html` and `https://www-wales.ch.cam.ac.uk/~wales/CCD/FS_Fe/iron_fs.html`, fetched on `2026-10-17T20:27:05Z` and recorded in `the-record-we-beat/snapshot_2026-10-17.md`):

| Cluster | $N$ | CCD Table Energy (eV) | Polished CCD Structure (eV) | Our New Minimum $E^*$ (eV) | Improvement $\Delta E$ (eV) | $\|\nabla E\|_2$ (`float64`) | $\|\nabla E\|_2$ (`Decimal50`) | Vibrational Hessian $\lambda_{\min} \dots \lambda_{\max}$ |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **`Mo_75`** | `75` | `-439.4197932305` | `-439.4197932305` | **`-439.5640256673`** | **`-0.144232`** | `1.23e-13` | `9.18e-28` | `0.4042 .. 29.25` (`219/219 > 0`) |
| **`Mo_90`** | `90` | `-532.7899433214` | `-532.7899433215` | **`-533.2142178271`** | **`-0.424275`** | `1.26e-13` | `1.20e-27` | `0.4171 .. 28.69` (`264/264 > 0`) |
| **`Fe_86`** | `86` | `-312.6006513052` | `-312.6006513052` | **`-312.7609188697`** | **`-0.160268`** | `2.36e-14` | `1.10e-28` | `0.5829 .. 22.70` (`252/252 > 0`) |
| **`Fe_87`** | `87` | `-316.4759023549` | `-316.4759023549` | **`-316.6115843892`** | **`-0.135682`** | `2.30e-14` | `9.84e-29` | `0.5961 .. 22.74` (`255/255 > 0`) |
| **`Fe_90`** | `90` | `-327.8503707653` | `-327.8503707653` | **`-327.9864583540`** | **`-0.136088`** | `2.86e-14` | `1.01e-28` | `0.5696 .. 23.09` (`264/264 > 0`) |
| **`Fe_91`** | `91` | `-331.9072022873` | `-331.9072022874` | **`-332.0252838865`** | **`-0.118082`** | `2.36e-14` | `1.01e-28` | `0.5558 .. 23.08` (`267/267 > 0`) |
| **`Fe_92`** | `92` | `-335.9034309081` | `-335.9034309082` | **`-335.9470373457`** | **`-0.043606`** | `2.76e-14` | `1.07e-28` | `0.5482 .. 22.91` (`270/270 > 0`) |
| **`Fe_96`** | `96` | `-351.2027399452` | `-351.2027399452` | **`-351.2401491626`** | **`-0.037409`** | `2.38e-14` | `1.14e-28` | `0.5600 .. 23.27` (`282/282 > 0`) |
| **`Fe_97`** | `97` | `-354.9919830214` | `-354.9919830215` | **`-355.1385265715`** | **`-0.146544`** | `2.76e-14` | `1.18e-28` | `0.5620 .. 23.64` (`285/285 > 0`) |
| **`Fe_98`** | `98` | `-358.8031191667` | `-358.8031191668` | **`-359.0082985625`** | **`-0.205179`** | `2.26e-14` | `1.00e-28` | `0.5587 .. 23.51` (`288/288 > 0`) |
| **`Fe_100`** | `100` | `-366.5806583336` | `-366.5806583337` | **`-366.6082856510`** | **`-0.027627`** | `2.64e-14` | `1.14e-28` | `0.5792 .. 23.47` (`294/294 > 0`) |

### Complete 196-Point-File Calibration & Polishing Audit (Partial Win `p1`)
We recomputed and Newton-polished all $2 \times 98 = 196$ posted point files (`Mo_3`–`Mo_100` and `Fe_3`–`Fe_100`, embedded in `object/fs_mo_fe_11_records_and_196_audit.json` under `ccd_196_point_files_audit`):
- **Zero Reproduction Discrepancies**: All 98 `Mo` point files reproduce their posted 10-decimal CCD energies within `9.77e-11 eV` under the Finnis-Sinclair (1984) Mo parameter set, and all 98 `Fe` point files reproduce their posted 10-decimal CCD energies within `9.41e-11 eV` under the Finnis-Sinclair (1986 modified) Fe parameter set.
- **Zero Under-Converged CCD Point Files**: Every posted CCD point file has raw gradient norm `||grad E||_2 <= 1.69e-5` and lowers by at most `1.9e-10 eV` upon Newton-polishing to `||grad E||_2 < 1e-13`, confirming that all 196 posted CCD structures are genuine local minima and that all 11 of our new records reside in strictly distinct structural basins.

## Not Claimed
- We do not claim that these 11 new local minima are the mathematical global minima of their respective cluster sizes; each is a verified strict local minimum in a distinct structural basin that lowers the putative global minimum in the Cambridge Cluster Database by `0.027627 eV` to `0.424275 eV` (`276x` to `4,242x` the `1e-4 eV` threshold).

## Credits
- **Contributor**: `Zerbytheboss` (GitHub account `HindsightWise` is operated by `Zerbytheboss`).
- **J. A. Elliott, Y. Shibuta, and D. J. Wales** (*Philosophical Magazine* 89, 3311-3332, 2009) and the **Cambridge Cluster Database** for the benchmark `FS_Mo` and `FS_Fe` tables and coordinate archives.
- **M. W. Finnis and J. E. Sinclair** (*Philosophical Magazine A* 50, 45-55, 1984; *Philosophical Magazine A* 53, 161, 1986) for the many-body transition-metal potential formulation.
