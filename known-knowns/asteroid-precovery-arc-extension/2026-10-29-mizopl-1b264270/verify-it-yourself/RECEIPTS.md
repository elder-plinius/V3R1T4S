# Verification Receipts — `2026-10-29-mizopl-1b264270` (`asteroid-precovery-arc-extension`: `2014 OV236`)

## 1. Clean Copy Execution (`sh verify-it-yourself/run_checks.sh`)

```text
[1/2] Public JPL DE421 ephemeris (de421.bsp, 16788480 B, sha256=a20a7139da04cbc4...) verified and loaded.
[2/2] 2014 OV236 verified: 4 detections, postfit new RMS=0.0442" (< 1.0"), arc=1.36x, sigma_a reduction=62.92% LS / 55.37% SBDB.
PASS
```

## 2. Corrupted Copy Rejection

When any FITS cutout or JSON/text manifest inside `object/precovery_2014_OV236/` is perturbed (e.g. modifying a single byte or digit of `object/precovery_2014_OV236/precovery_bundle.json`, `sbdb_orbit_cov.json`, `mpc_obs80.txt`, or any FITS cutout), or if the `de421.bsp` ephemeris file fails its SHA-256 check, `sh verify-it-yourself/run_checks.sh` exits with code `1` and prints `FAIL` on its final line.
