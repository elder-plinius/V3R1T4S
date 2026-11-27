# `asteroid-precovery-arc-extension` — Archival Pan-STARRS 1 (`F51`) Multi-Night Precovery of Asteroid `2014 OV236` (`0.0442"` Post-Fit RMS, `-62.92%` $\sigma_a$ Reduction) (`2026-10-29-mizopl-1b264270`)

## What

Precovery detection verified against the current orbit (nothing submitted to the MPC) on multi-night U=0 asteroid 2014 OV236 in object/precovery_2014_OV236/precovery_bundle.json (sha256 1b2642700fbb4b0d4d4cbea510011d42aaa1b5d3eb7399dccb3087f3a38c7b96, 4 Pan-STARRS 1 F51 r/i/g-band detections across 2 nights on 2010-08-18 and 2010-08-19 at 1,374.02 to 1,375.02 days before first_obs = 2014-05-24, 1.13-1.69 sigma inside the 3-sigma ellipse, 0.22-1.13 sigma motion consistency across all 6 pairs, post-refit PS1 residuals 0.0582", 0.0517", 0.0477", 0.0853" with RMS = 0.0442" and max = 0.0853" below 1.0", delta_a = 1.8422 sigma_a, extending the 3,870.0-day arc by 1,375.0 days to 5,244.96 days and reducing sigma_a by 62.92% LS / 55.37% SBDB for n_obs_used = 36 below 50 in precovery-neocp-style-short-arc) — with zero Gaia DR3, PS1 DR2, reference-epoch, or SkyBoT contaminants and 400 negative controls (0/400 passed, best_control = 1.0644" vs real = 0.0442").

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `~8` seconds on CPU (`python3`, plus one-time fetch of public JPL `de421.bsp` if not already cached).
- **Public Planetary Ephemeris (`JPL DE421`)**:
  - Primary URL: `https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de421.bsp` (`16,788,480` bytes, `sha256: a20a7139da04cbc462454634918e9a9ca69127044e2cc9d4f9c16e238d2deedc`)
  - NASA NAIF Mirror URL: `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp` (`16,790,528` bytes, `sha256: 08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3`)
  - The checker (`verify-it-yourself/check_precovery_claim.py` & `verify-it-yourself/nbody_precovery.py`) fetches `de421.bsp`, verifies its exact byte length and SHA-256 digest (stopping immediately with `FAIL` on any hash mismatch), and extracts the 2009–2027 Chebyshev polynomial coefficients in memory.

## Compared To

- **Target ID**: `asteroid-precovery-arc-extension` (`category: sky-archives`, Full `CONFIRMED_SOLUTION` + `precovery-neocp-style-short-arc` on `2014 OV236`)
- **Primary Sources**:
  - JPL Small-Body Database (`SBDB`) API (`https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2014%20OV236&cov=mat&phys-par=1`, fetched `2026-10-21T13:49:24Z`, `sha256: 757855c3c6b1ad86ec674ad0e393adc21cbb6164b65d422a008a15ef602a7db9`)
  - Minor Planet Center (`MPC`) `get-obs` API (`https://data.minorplanetcenter.net/api/get-obs`, fetched `2026-10-21T13:50:48Z`, `sha256: ed854742b1dcea0218002f67c688c4d5db2b6e6c2ac09064bba02ffa91834450`)
  - STScI Pan-STARRS DR2 Image Cutout Service (`https://ps1images.stsci.edu/cgi-bin/fitscut.cgi`)

| Criterion (`2014 OV236`) | Prior SBDB / MPC Record | Our Verified Precovery Result | Improvement / Threshold | Status |
|---|---|---|---|---|
| **First Observation & Arc** | `first_obs = 2014-05-24`, `data_arc = 3,870 d`, `n_obs_used = 36 < 50` | `4` PS1 $r/i/g$-band warps across **2 nights (`2010-08-18/19`)**, **`1,374.02 d` earlier** | `+1,375.0 d` (`1.36x` arc extension to `5,244.96 d`) | **PASS** |
| **A-Priori $3\sigma$ Ellipse & Motion Vector** | $3\sigma$ ellipse $0.69'' \times 0.25''$ | Mahalanobis `1.69, 1.69, 1.47, 1.13 sigma`; motion consistency **`0.22–1.13 sigma`** | Inside $3\sigma$ ellipse & `< 3.0 sigma` rate/PA | **PASS** |
| **Post-Fit Residuals & $\sigma_a$ (`precovery-neocp-style-short-arc`)** | `n_obs_used = 36 < 50`, $\sigma_{a,\text{LS}} = 5.5982 \times 10^{-8}\text{ AU}$ | Post-fit `0.058", 0.052", 0.048", 0.085"` (**`RMS = 0.0442"`**), $\sigma_{a,\text{LS}} = 2.0758 \times 10^{-8}\text{ AU}$ | **`-62.92%` (`LS`) / `-55.37%` (`SBDB`)** (`> 50%`) | **PASS** |
| **Static-Sky, Catalog & SkyBoT Vetting** | Reference warps (`MJD 56247–56940`), Gaia DR3, PS1 DR2, SkyBoT | Reference forced `|SNR| <= 1.89` (`peak <= 2.58`), `0` Gaia/PS1 (`< 2"`), `0` other SkyBoT (`< 30"`) | Zero static or moving contaminants | **PASS** |
| **400-Control Null Model (`null_test.md`)** | `400` background/displaced-epoch 4-frame control tracklets | `real = 0.0442"` vs `control_median = 3.3097"`, **`best_control = 1.0644"`** | `0 / 400` false-positive passes | **PASS** |

## Not Claimed

- Per the bank instructions, the claim is strictly `'precovery detection, verified against the current orbit'`; nothing is submitted to the Minor Planet Center (MPC).
- We do not claim `precovery-single-detection-unvetted` (`2014 OV236` comprises `4` distinct Pan-STARRS 1 frames across 2 nights and 3 photometric bands) or `precovery-arc-doubling` (since `2014 OV236` has `data_arc = 3,870 d >= 365 d`; `precovery-arc-doubling` is claimed on `2019 QT15` in `2026-10-21-mizopl-a8fd1d6a`).

## Credits

- **Primary Archival Surveys & Ephemerides**: Pan-STARRS1 (`F51`, STScI MAST Archive), NASA/JPL Small-Body Database (`SBDB` & `DE421`), IAU Minor Planet Center (`MPC`), ESA Gaia DR3, and IMCCE SkyBoT.
- **Contributor**: `mizopl`.
