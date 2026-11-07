# Verification Receipts — `2026-10-21-mizopl-a8fd1d6a` (`asteroid-precovery-arc-extension`: `2019 QT15`)

## 1. Clean Copy Execution (`sh verify-it-yourself/run_checks.sh`)

```text
[1/2] Public JPL DE421 ephemeris (de421.bsp, 16790528 B, sha256=08b20db2ae224886...) verified and loaded.
[2/2] 2019 QT15 verified: 3 detections, postfit new RMS=0.1176" (< 1.0"), arc=20.93x, sigma_a reduction=83.25% LS / 87.38% SBDB.
PASS
```

## 2. Corrupted Copy Rejection

When any FITS cutout or JSON/text manifest inside `object/precovery_2019_QT15/` is perturbed (e.g. modifying a single byte or digit of `object/precovery_2019_QT15/precovery_bundle.json`, `sbdb_orbit_cov.json`, `mpc_obs80.txt`, or any FITS cutout), or if the `de421.bsp` ephemeris file fails its SHA-256 check, `sh verify-it-yourself/run_checks.sh` exits with code `1` and prints `FAIL` on its final line.
