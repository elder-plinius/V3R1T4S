# Null Model Control Test (`asteroid-precovery-arc-extension`: `2014 OV236`)

controls: 400
best_control: 1.0644
real: 0.0442
command: python3 verify-it-yourself/check_precovery_claim.py --run-null-test
real_beats_all_controls: yes

## Summary of 400 Deterministic Background & Displaced-Epoch Null Control Trials (`2014 OV236`)

- **Number of independent null controls**: `400` (`seed = 20261021` in `python3 verify-it-yourself/check_precovery_claim.py --run-null-test`)
- **Generator & Pipeline**:
  - `200` random sky-offset control tracklets sampled in the `3.5" .. 11.0"` background annulus around the nominal trajectory inside the 4 science FITS cutouts of `2014 OV236`, with independent per-frame astrometric jitter `[-6.0", +6.0"]` representing unlinked noise peaks, passed through the exact 6D N-body Gauss-Newton residual projection matrix $P_{\text{res}} = I_8 - J_{\text{new}}(C_{\text{SBDB}}^{-1} + J_{\text{new}}^T W_{\text{new}} J_{\text{new}})^{-1} J_{\text{new}}^T W_{\text{new}}$.
  - `200` displaced-epoch control tracklets sampled identically on the 4 different-epoch reference FITS cutouts (`ref_warp_01..04_*.fits`).
- **400-control null distribution (`post-fit new RMS` in arcsec, lower is better)**:
  - `real` (`2014 OV236` 4-frame precovery tracklet): **`0.0442 arcsec`** (`max = 0.0853 arcsec < 1.0 arcsec`, `min SNR = 15.60`)
  - `control_median`: **`3.3097 arcsec`**
  - `control_iqr`: **`0.8790 arcsec`**
  - `best_control` (`min` across all 400 controls): **`1.0644 arcsec`** (`> 1.0 arcsec`, and `24.1x` worse than `real = 0.0442 arcsec`)
  - False-positive controls passing `rms_postfit < 1.0"`: **`0 / 400` (`0.00%`)**
