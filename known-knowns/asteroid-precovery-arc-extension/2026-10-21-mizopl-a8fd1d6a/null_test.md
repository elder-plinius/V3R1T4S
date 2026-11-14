# Null Model Control Test (`asteroid-precovery-arc-extension`: `2019 QT15`)

controls: 400
best_control: 1.2800
real: 6.3600
command: python3 verify-it-yourself/check_precovery_claim.py --run-null-test
real_beats_all_controls: yes

## Summary of 400 Deterministic Background & Displaced-Epoch Null Control Trials (`2019 QT15`)

- **Number of independent null controls**: `400` (`seed = 20261021` in `python3 verify-it-yourself/check_precovery_claim.py --run-null-test`)
- **Generator & Pipeline**:
  - `200` random sky-offset 3-frame control tracklets sampled in the `3.5" .. 11.0"` background annulus around the detected trajectory inside the 3 Pan-STARRS 1 science FITS cutouts (`science_warp_01..03_*.fits`) of `2019 QT15`, evaluated with the exact forced-aperture photometry pipeline (`measure_forced_aperture_at_ra_dec` in `verify-it-yourself/fits_astrometry.py`).
  - `200` displaced-epoch 3-frame control tracklets sampled identically on the 3 different-epoch Pan-STARRS 1 reference FITS cutouts (`ref_warp_01..03_*.fits`, `MJD 55530.31502`).
- **400-control null distribution (`3-frame minimum forced-aperture SNR`, higher is better)**:
  - `real` (`2019 QT15` 3-frame precovery tracklet): **`6.3600`** (`SNR = 6.82, 6.36, 8.27` across the 3 frames, with 6D N-body post-fit residual `RMS = 0.1176 arcsec` and `max = 0.2275 arcsec < 1.0 arcsec`)
  - `control_median`: **`-1.0100`**
  - `best_control` (`max` 3-frame minimum SNR across all 400 controls): **`1.2800`** (well below the `5.0` detection threshold and `4.97x` below `real = 6.3600`)
  - False-positive controls passing `min(SNR) >= 5.0`: **`0 / 400` (`0.00%`)**
