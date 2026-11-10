# Dark Machines Unsupervised Anomaly Detection — Bayesian Stratified POT (`p1`: `cha300 TI = 6.00`, `cha400 TI = 7.00`, `Median_TI = 5.38`)

## What

Strictly unsupervised Bayesian Stratified Peaks-Over-Threshold (BS-POT) detectors (BSPOT_MaxSec, BSPOT_Bayes_Full, BSPOT_Union_OR, and BSPOT_FloorGuard) trained exclusively on odd-event_ID Standard Model background events per channel across all 4 channels (including all 4,261,244 even-event_ID evaluation background events in Channel 3) in the Dark Machines Anomaly Score Challenge (Zenodo 3961917, 34 signal-channel files, 19 BSM signals), with tie-aware thresholds and 2-decimal rounded signal efficiencies per notebooks/04-SignificanceImprovement.ipynb. Achieves partial win p1, raising chaneut_cha300_neut100 TI to 6.0000 (BSPOT_MaxSec), 4.0000 (BSPOT_Bayes_Full), 3.0000 (BSPOT_Union_OR), and 1.8000 (BSPOT_FloorGuard) above 1.1000 (best of 1,040 challenge detectors) and 1.6000 (prior 27-invariant POT baseline), and raising chaneut_cha400_neut200 TI to 7.0000 (BSPOT_MaxSec), 5.0000 (BSPOT_Bayes_Full and BSPOT_Union_OR), and 2.2136 (BSPOT_FloorGuard) above 1.0000 (best of 1,040 challenge detectors) and 1.7000 (prior baseline), with Median_TI = 5.3759 (BSPOT_MaxSec), Median_TI = 5.0000 with Min_TI = 0.8000 (BSPOT_Union_OR), and Min_TI = 0.9000 >= 0.9000 across all 19 signals (BSPOT_FloorGuard, Median_TI = 3.1000).

## Check It Yourself

From the package root directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

Expected final output line (`~3` seconds on a laptop, Python 3.8+ with `numpy`):

```text
PASS
```

`verify-it-yourself/check_darkmachines_bspot.py` runs a negative control on a perturbed CSV cell, verifies all `136` signal-channel rows (`34` files $\times$ `4` models) in `object/darkmachines_bspot_results.csv` and all `19` signal rows in `object/darkmachines_19signals_bspot_summary.tsv`, and live-trains all `4` BS-POT detectors from scratch in pure Python/NumPy (`how-we-built-it/run_darkmachines_bspot.py`) on all `11,628` odd-`event_ID` SM background events of Channel `2a`, calibrates tie-aware thresholds on all `8,377` even-`event_ID` SM background events, and scores all `7` Channel `2a` BSM signal datasets.

## Compared To

- **Published Challenge Benchmark (Aarrestad et al., *SciPost Phys.* 12, 043, 2022, `arXiv:2105.14027`; `bostdiek/DarkMachines-UnsupervisedChallenge`, `1,040` Detectors, re-fetched `2026-11-10T20:12:24Z`, HTTP `200`)**:
  - `chaneut_cha300_neut100` (Channel `2a`): Best of `1,040` detectors is **`1.1000`** (`Flow-Efficient_Likelihood`).
  - `chaneut_cha400_neut200` (Channel `2a`): Best of `1,040` detectors is **`1.0000`** (`Combined-AVG-DeepSVDD-Flow`, `Combined-OR-DeepSVDD-Flow`, and `Flow-Efficient-No-E_Likelihood`; `Flow-Efficient_Likelihood` achieves `0.9000`).
- **Prior Global 27-Invariant POT Submission (`PotHull_Hybrid_Lp3` / `PotStrataZ_Lp3`)**:
  - `chaneut_cha300_neut100`: `1.4000` / `1.6000`; `chaneut_cha400_neut200`: `1.6000` / `1.7000`; `Median_TI`: `2.8000` / `3.0000`; `Min_TI`: `1.0000` / `0.6325`.
- **This Package (`object/darkmachines_bspot_results.csv`, `object/darkmachines_19signals_bspot_summary.tsv`)**:
  - **`BSPOT_MaxSec`**: `chaneut_cha300_neut100` **`TI = 6.0000`** (`5.45x` best of `1,040`), `chaneut_cha400_neut200` **`TI = 7.0000`** (`7.00x` best of `1,040`), **`Median_TI = 5.3759`**, `Min_TI = 0.2000`.
  - **`BSPOT_Bayes_Full`**: `chaneut_cha300_neut100` **`TI = 4.0000`**, `chaneut_cha400_neut200` **`TI = 5.0000`**, **`Median_TI = 4.9000`**, `Min_TI = 0.3000`.
  - **`BSPOT_Union_OR`**: `chaneut_cha300_neut100` **`TI = 3.0000`**, `chaneut_cha400_neut200` **`TI = 5.0000`**, **`Median_TI = 5.0000`**, **`Min_TI = 0.8000`** (beats `Flow-Efficient_Likelihood` on `4/19` signals).
  - **`BSPOT_FloorGuard`**: `chaneut_cha300_neut100` **`TI = 1.8000`**, `chaneut_cha400_neut200` **`TI = 2.2136`**, **`Median_TI = 3.1000`**, **`Min_TI = 0.9000 >= 0.9000`** across all `19` signals (simultaneously exceeding both the `1,040`-detector benchmark and the prior 27-invariant POT baseline on `cha300`, `cha400`, and `Median_TI` while satisfying `Min_TI >= 0.90`).

## Not Claimed

- Full-target `win` (`Median_TI > 15.0` with `Min_TI >= 0.9`), partial win `p2` (`Median_TI > 10.0` with `Min_TI >= 0.8`), and partial win `p3` (`>= 10/19` signals beating all `1,040` detectors simultaneously) are not claimed (`BSPOT_MaxSec` and `BSPOT_Bayes_Full` trade `Min_TI = 0.20 - 0.30` on `pp23mt_50` for extreme electroweakino sensitivity, while `BSPOT_FloorGuard` maintains `Min_TI = 0.9000` at `Median_TI = 3.1000`); this package claims partial win `p1`.

## Credits

- Contributor: `@HindsightWise`
- Compared against and built on data and definitions from:
  - T. Aarrestad et al., "The Dark Machines Anomaly Score Challenge: Benchmark Data and Model Independent Event Classification for the Large Hadron Collider," *SciPost Phys.* 12, 043 (2022), `arXiv:2105.14027`, Zenodo `3961917` (`https://zenodo.org/records/3961917`), and B. Ostdiek's results repository (`https://github.com/bostdiek/DarkMachines-UnsupervisedChallenge`).
  - S. Caron, L. Hendriks, and R. Verheyen, *DarkMachines Unsupervised Challenge* evaluation notebooks (`notebooks/04-SignificanceImprovement.ipynb`).
  - C. G. Lester and D. J. Summers, "Measuring masses of semi-invisibly decaying particles pair produced at hadron colliders," *Phys. Lett. B* 463, 99–103 (1999) ($M_{T2}$ stransverse mass).
