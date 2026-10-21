# `asteroid-precovery-arc-extension` — Archival Pan-STARRS 1 (`F51`) Precovery of Short-Arc Asteroid `2019 QT15` (`20.93x` Arc Extension, `-87.38%` $\sigma_a$) and `2014 OV236` (`-62.92%` $\sigma_a$) + 12-Object Calibration Gate (`2026-10-21-mizopl-a8fd1d6a`)

## What

Precovery detection verified against the current orbit (nothing submitted to the MPC) across two complete Pan-STARRS 1 (F51) archival FITS bundles — short-arc asteroid 2019 QT15 in claim/precovery_2019_QT15/precovery_bundle.json (sha256 a8fd1d6acaa5d05e238ca05078cff4fd0522908dabc12cbf6099eca35bfeca15, 3 i-band detections on 2014-11-11 spanning 39.15 min at 1,754.08 days before first_obs = 2019-08-31, 2.16-2.85 sigma inside the 3-sigma ellipse, 0.39 sigma / 0.97 sigma motion consistency, post-refit PS1 residuals 0.0216", 0.2275", 0.1756" with RMS = 0.1176" below 1.0", delta_a = 0.5962 sigma_a, multiplying the 88.0-day arc by 20.93x to 1,841.80 days / 1,841.82 days for precovery-arc-doubling and reducing sigma_a by 87.38% SBDB / 83.25% LS for n_obs_used = 41 below 50 in precovery-neocp-style-short-arc) and multi-night U=0 asteroid 2014 OV236 in claim/precovery_2014_OV236/precovery_bundle.json (sha256 1b2642700fbb4b0d4d4cbea510011d42aaa1b5d3eb7399dccb3087f3a38c7b96, 4 r/i/g-band detections on 2010-08-18/19 at 1,374.02 days before first_obs = 2014-05-24, post-refit PS1 RMS = 0.0442" and max = 0.0853" below 1.0", reducing sigma_a by 62.92% LS / 55.37% SBDB for n_obs_used = 36 below 50) — with zero Gaia DR3, PS1 DR2, reference-epoch, or SkyBoT contaminants, accompanied by 12 known-observation re-detections in ZTF (I41) and PS1 (F51) to max 0.4301" below 1.0" (precovery-reproduce-known-obs) and 400 negative controls (best_control = 1.0644" vs real = 0.0442").

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `~14` seconds on CPU (`python3`).

## Compared To

- **Target ID**: `asteroid-precovery-arc-extension` (`category: sky-archives`, Full `CONFIRMED_SOLUTION` + `precovery-reproduce-known-obs` + `precovery-arc-doubling` + `precovery-neocp-style-short-arc`)
- **Primary Sources**:
  - JPL Small-Body Database (`SBDB`) API (`https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2019%20QT15&cov=mat&phys-par=1`, fetched `2026-10-21T13:49:08Z`, `sha256: f95d64f54fb52a3423930a433a626fb1ecf0125263d7cdecef07c00bc5ab6c73`; `https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2014%20OV236&cov=mat&phys-par=1`, fetched `2026-10-21T13:49:24Z`, `sha256: 757855c3c6b1ad86ec674ad0e393adc21cbb6164b65d422a008a15ef602a7db9`)
  - Minor Planet Center (`MPC`) `get-obs` API (`https://data.minorplanetcenter.net/api/get-obs`, fetched `2026-10-21T13:49:08Z` and `2026-10-21T13:50:48Z`)
  - STScI Pan-STARRS DR2 Image Cutout Service (`https://ps1images.stsci.edu/cgi-bin/fitscut.cgi`) & IRSA ZTF Science Archive (`https://irsa.ipac.caltech.edu/ibe/data/ztf/products/sci/`)

| Bundle / Criterion | Prior SBDB / MPC Record | Our Verified Precovery Result | Improvement / Threshold | Status |
|---|---|---|---|---|
| **Calibration Gate (`precovery-reproduce-known-obs`)** | `12` known MPC `OBS80` observations (`I41` & `F51`) | `mean = 0.2801"`, `RMS = 0.2961"`, **`max = 0.4301"`** | `< 1.0 arcsec` on `>= 10` objects | **PASS** |
| **`2019 QT15` First Observation & Arc (`precovery-arc-doubling`)** | `first_obs = 2019-08-31`, `data_arc = 88.0 d` (`< 365 d`), `41` obs | `3` PS1 $i$-band warps on **`2014-11-11`** (`1,754.08 d` earlier, `39.15 min` span) $\to$ **`1,841.82 d`** | **`20.93x` arc multiplication** (`>= 2.0x`) | **PASS** |
| **`2019 QT15` Post-Fit Residuals & $\sigma_a$ (`precovery-neocp-style-short-arc`)** | `n_obs_used = 41 < 50`, $\sigma_{a,\text{SBDB}} = 2.1185 \times 10^{-5}\text{ AU}$ | Post-fit `0.022", 0.228", 0.176"` (**`RMS = 0.1176"`**), $\sigma_{a,\text{SBDB}} = 2.6743 \times 10^{-6}\text{ AU}$ | **`-87.38%` (`SBDB`) / `-83.25%` (`LS`)** (`> 50%`) | **PASS** |
| **`2014 OV236` First Observation & Arc** | `first_obs = 2014-05-24`, `data_arc = 3,870 d`, `n_obs_used = 36 < 50` | `4` PS1 $r/i/g$-band warps across **2 nights (`2010-08-18/19`)**, **`1,374.02 d` earlier** | `+1,375.0 d` (`1.36x` arc extension) | **PASS** |
| **`2014 OV236` Post-Fit Residuals & $\sigma_a$ (`precovery-neocp-style-short-arc`)** | `n_obs_used = 36 < 50`, $\sigma_{a,\text{LS}} = 5.5982 \times 10^{-8}\text{ AU}$ | Post-fit `0.058", 0.052", 0.048", 0.085"` (**`RMS = 0.0442"`**), $\sigma_{a,\text{LS}} = 2.0758 \times 10^{-8}\text{ AU}$ | **`-62.92%` (`LS`) / `-55.37%` (`SBDB`)** (`> 50%`) | **PASS** |
| **400-Control Null Model (`null_test.md`)** | `400` background/displaced-epoch control tracklets | `real = 0.0442"` vs `control_median = 3.3097"`, **`best_control = 1.0644"`** | `0 / 400` false-positive passes | **PASS** |

## Not Claimed

- Per the bank instructions, the claim is strictly `'precovery detection, verified against the current orbit'`; nothing is submitted to the Minor Planet Center (MPC).
- We do not claim `precovery-single-detection-unvetted` (which is for unvetted single-frame detections that are logged and never claimed); both of our precovery bundles are multi-frame (`3` frames for `2019 QT15` and `4` frames across 2 nights for `2014 OV236`).

## Credits

- **Primary Archival Surveys & Ephemerides**: Pan-STARRS1 (`F51`, STScI MAST Archive), Zwicky Transient Facility (`I41`, Caltech/IPAC IRSA), NASA/JPL Small-Body Database (`SBDB` & `DE421`), IAU Minor Planet Center (`MPC`), ESA Gaia DR3, and IMCCE SkyBoT.
- **Contributor**: `mizopl`.
