# Run It Yourself — `2026-10-21-mizopl-a8fd1d6a` (`asteroid-precovery-arc-extension`)

## 1. Offline Verification of Saved FITS Cutouts, Astrometry, N-Body Propagation, and Orbit Refits (`~14` seconds)

```sh
sh verify-it-yourself/run_checks.sh
```

## 2. Live Archival Re-Fetch & Bundle Rebuild (`how-we-built-it/`)

To re-query JPL SBDB, the MPC `get-obs` API, STScI Pan-STARRS DR2 (`ps1filenames.py` & `fitscut.cgi`), IRSA ZTF (`ibe`), ESA Gaia DR3, MAST PS1 DR2 `MeanObject`, and IMCCE SkyBoT from scratch:

```sh
/opt/homebrew/bin/python3 how-we-built-it/build_calibration_gate_12.py
/opt/homebrew/bin/python3 how-we-built-it/build_both_precovery_bundles.py
```
