# Verification Receipts — `2026-10-21-mizopl-a8fd1d6a` (`asteroid-precovery-arc-extension`)

## 1. Clean Copy Execution (`sh verify-it-yourself/run_checks.sh`)

```text
[1/3] Calibration gate verified: 12/12 minor planets (< 1.0", mean=0.2801", max=0.4301").
[2/3] 2019 QT15 verified: 3 detections, postfit new RMS=0.1176" (< 1.0"), arc=20.93x, sigma_a reduction=83.25% LS / 87.38% SBDB.
[3/3] 2014 OV236 verified: 4 detections, postfit new RMS=0.0442" (< 1.0"), arc=1.36x, sigma_a reduction=62.92% LS / 55.37% SBDB.
PASS
```

## 2. Corrupted Copy Rejection

When any FITS cutout or JSON manifest inside `object/` is perturbed (e.g. modifying a single byte of `object/precovery_2019_QT15/precovery_bundle.json` or any FITS file), `sh verify-it-yourself/run_checks.sh` exits with code `1` and prints `FAIL` on its final line.
