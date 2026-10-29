# `asteroid-precovery-arc-extension` — Archival Pan-STARRS 1 (`F51`) Precovery of Short-Arc Asteroid `2019 QT15` (`20.93x` Arc Extension, `-87.38%` $\sigma_a$ Reduction) (`2026-10-21-mizopl-a8fd1d6a`)

## What

Precovery detection verified against the current orbit (nothing submitted to the MPC) on short-arc asteroid 2019 QT15 in object/precovery_2019_QT15/precovery_bundle.json (sha256 a8fd1d6acaa5d05e238ca05078cff4fd0522908dabc12cbf6099eca35bfeca15, 3 Pan-STARRS 1 F51 i-band detections on 2014-11-11 spanning 39.15 min at 1,754.08 days before first_obs = 2019-08-31, 2.16-2.85 sigma inside the 3-sigma ellipse, 0.97 sigma motion consistency, post-refit PS1 residuals 0.0216", 0.2275", 0.1756" with RMS = 0.1176" below 1.0", delta_a = 0.5962 sigma_a, multiplying the 88.0-day arc by 20.93x to 1,841.82 days for precovery-arc-doubling and reducing sigma_a by 87.38% SBDB / 83.25% LS for n_obs_used = 41 below 50 in precovery-neocp-style-short-arc) — with zero Gaia DR3, PS1 DR2, reference-epoch, or SkyBoT contaminants and 400 negative controls (0/400 passed, best_control = 1.2800 vs real = 6.3600).

## Check It Yourself

From this package directory, run:

```sh
sh verify-it-yourself/run_checks.sh
```

- **Expected last line**: `PASS`
- **Rough laptop time**: `~7` seconds on CPU (`python3`, plus one-time fetch of public JPL `de421.bsp` if not already cached).
- **Public Planetary Ephemeris (`JPL DE421`)**:
  - Primary URL: `https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de421.bsp` (`16,788,480` bytes, `sha256: a20a7139da04cbc462454634918e9a9ca69127044e2cc9d4f9c16e238d2deedc`)
  - NASA NAIF Mirror URL: `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp` (`16,790,528` bytes, `sha256: 08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3`)
  - The checker (`verify-it-yourself/check_precovery_claim.py` & `verify-it-yourself/nbody_precovery.py`) fetches `de421.bsp`, verifies its exact byte length and SHA-256 digest (stopping immediately with `FAIL` on any hash mismatch), and extracts the 2009–2027 Chebyshev polynomial coefficients in memory.

## Compared To

- **Target ID**: `asteroid-precovery-arc-extension` (`category: sky-archives`, Full `CONFIRMED_SOLUTION` + `precovery-arc-doubling` + `precovery-neocp-style-short-arc` on `2019 QT15`)
- **Primary Sources**:
  - JPL Small-Body Database (`SBDB`) API (`https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=2019%20QT15&cov=mat&phys-par=1`, fetched `2026-10-21T13:49:08Z`, `sha256: f95d64f54fb52a3423930a433a626fb1ecf0125263d7cdecef07c00bc5ab6c73`)
  - Minor Planet Center (`MPC`) `get-obs` API (`https://data.minorplanetcenter.net/api/get-obs`, fetched `2026-10-21T13:49:08Z`, `sha256: 46ee004a37ed19915f9192d83198df86c918cd59caac143c1455e53a834612d5`)
  - STScI Pan-STARRS DR2 Image Cutout Service (`https://ps1images.stsci.edu/cgi-bin/fitscut.cgi`)

| Criterion (`2019 QT15`) | Prior SBDB / MPC Record | Our Verified Precovery Result | Improvement / Threshold | Status |
|---|---|---|---|---|
| **First Observation & Arc (`precovery-arc-doubling`)** | `first_obs = 2019-08-31`, `data_arc = 88.0 d` (`< 365 d`), `41` obs | `3` PS1 $i$-band warps on **`2014-11-11`** (`1,754.08 d` earlier, `39.15 min` span) $\to$ **`1,841.82 d`** | **`20.93x` arc multiplication** (`>= 2.0x`) | **PASS** |
| **A-Priori $3\sigma$ Ellipse & Motion Vector** | $3\sigma$ LOV ellipse $116.91'' \times 0.57''$ (`PA = 77.9 deg`) | Mahalanobis `2.44, 2.16, 2.85 sigma`; motion vector consistency **`0.97 sigma`** (`39.15 min` span) | Inside $3\sigma$ ellipse & `< 3.0 sigma` rate/PA | **PASS** |
| **Post-Fit Residuals & $\sigma_a$ (`precovery-neocp-style-short-arc`)** | `n_obs_used = 41 < 50`, $\sigma_{a,\text{SBDB}} = 2.1185 \times 10^{-5}\text{ AU}$ | Post-fit `0.022", 0.228", 0.176"` (**`RMS = 0.1176"`**), $\sigma_{a,\text{SBDB}} = 2.6743 \times 10^{-6}\text{ AU}$ | **`-87.38%` (`SBDB`) / `-83.25%` (`LS`)** (`> 50%`) | **PASS** |
| **Static-Sky, Catalog & SkyBoT Vetting** | Reference warps (`MJD 55530.315`), Gaia DR3, PS1 DR2, SkyBoT | Reference forced `|SNR| <= 1.90` (`peak <= 2.51`), `0` Gaia/PS1 (`< 2"`), `0` SkyBoT (`< 30"`) | Zero static or moving contaminants | **PASS** |
| **400-Control Null Model (`null_test.md`)** | `400` background/displaced-epoch 3-frame control tracklets | `real min_snr = 6.3600` (`post-fit RMS = 0.1176"`) vs **`best_control = 1.2800`** | `0 / 400` false-positive passes | **PASS** |

## Not Claimed

- Per the bank instructions, the claim is strictly `'precovery detection, verified against the current orbit'`; nothing is submitted to the Minor Planet Center (MPC).
- We do not claim `precovery-single-detection-unvetted` (our `2019 QT15` precovery bundle comprises `3` distinct Pan-STARRS 1 frames spanning `39.15 min`).
- Separate objects (`2014 OV236` and the 12-object `precovery-reproduce-known-obs` calibration) are packaged separately so this submission contains strictly one object (`2019 QT15`).

## Credits

- **Primary Archival Surveys & Ephemerides**: Pan-STARRS1 (`F51`, STScI MAST Archive), NASA/JPL Small-Body Database (`SBDB` & `DE421`), IAU Minor Planet Center (`MPC`), ESA Gaia DR3, and IMCCE SkyBoT.
- **Contributor**: `mizopl`.
