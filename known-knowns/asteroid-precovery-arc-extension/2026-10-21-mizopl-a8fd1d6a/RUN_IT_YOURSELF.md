# Run It Yourself — `2026-10-21-mizopl-a8fd1d6a` (`asteroid-precovery-arc-extension`: `2019 QT15`)

## 1. Verification of Saved FITS Cutouts, Astrometry, N-Body Propagation, and Orbit Refit (`~7` seconds)

```sh
sh verify-it-yourself/run_checks.sh
```

- The verifier (`verify-it-yourself/check_precovery_claim.py` & `verify-it-yourself/nbody_precovery.py`) automatically locates or downloads the public NASA/JPL DE421 planetary ephemeris (`https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de421.bsp`, `16,788,480` bytes, `sha256: a20a7139da04cbc462454634918e9a9ca69127044e2cc9d4f9c16e238d2deedc`; or NAIF mirror `https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/a_old_versions/de421.bsp`, `16,790,528` bytes, `sha256: 08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3`), halts immediately on any hash mismatch, extracts the 2009–2027 Chebyshev polynomial coefficients, and verifies `object/precovery_2019_QT15/`.

## 2. Live Archival Re-Fetch & Bundle Rebuild (`how-we-built-it/`)

To re-query JPL SBDB, the MPC `get-obs` API, STScI Pan-STARRS DR2 (`ps1filenames.py` & `fitscut.cgi`), ESA Gaia DR3, MAST PS1 DR2 `MeanObject`, and IMCCE SkyBoT from scratch for `2019 QT15`:

```sh
python3 how-we-built-it/build_both_precovery_bundles.py
```
