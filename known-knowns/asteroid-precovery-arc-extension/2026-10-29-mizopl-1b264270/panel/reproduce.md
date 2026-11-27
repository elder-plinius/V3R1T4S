# Skeptic Panel Report — Role: `REPRODUCE`

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target: `asteroid-precovery-arc-extension` (`sky-archives`)

## 1. Mandate & Verbatim Definition Quoted Before Reading Author Code

Mandate:
"Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

Verbatim definition quoted from the bank target `asteroid-precovery-arc-extension`:
"A saved bundle {object designation, JPL SBDB JSON (orbit, covariance, first_obs) as fetched, the MPC observation record for the object as fetched (get-obs API OBS80 output or the MPCAT-OBS extract), archival image identifiers and download URLs, cutout FITS for every frame used, source detections with centroid and RA/Dec/uncertainty, predicted position and 3-sigma error ellipse from back-propagation (code saved), refit orbit residuals including the new points, static-sky check} such that: (1) the image epoch precedes JPL SBDB orbit.first_obs for that object (https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=[designation], re-fetched live immediately before claiming) by at least one apparition (more than 60 days), and the MPC observation record for the object (get-obs API, re-fetched live) contains no observation within 1 day of that epoch; (2) at least 2 detections of the object in distinct frames (same night separated by at least 20 min, or different nights), each inside the propagated 3-sigma ellipse, with the measured motion vector between them consistent with the predicted rate and direction within 3 sigma; (3) the residual of each detection against the a-priori orbit is inside the 3-sigma ellipse AND the refit orbit residual at the new epochs is less than 2 arcsec (less than 1 arcsec for PS1), with the refit changing the semi-major axis by less than its a-priori 3-sigma; (4) the predicted magnitude is within 1.5 mag of the measured one; (5) no static source is present at any detection position in another-epoch frame or in Gaia DR3/PS1 catalogs within 2 arcsec, and a SkyBoT cone search at each epoch shows no other known object within 30 arcsec. Claim is 'precovery detection, verified against the current orbit'; nothing is submitted to the MPC."

Enumerated Partial Win:
- `precovery-neocp-style-short-arc`: Stretch tier: a fully verified precovery (more than 60 d earlier) for an object with n_obs_used less than 50 in SBDB, where the added points reduce the semi-major-axis uncertainty by more than 50% in the refit; the covariance before/after saved.

---

## 2. Independent Checker Written Before Reading Author Code

Before reading `verify-it-yourself/check_precovery_claim.py`, `verify-it-yourself/nbody_precovery.py`, or `verify-it-yourself/fits_astrometry.py`, an independent checker (`indep_precovery_check.py`) was written from scratch directly from the definition, implementing:
1. Exact byte-size and `SHA-256` verification of all saved files in `object/precovery_2014_OV236/` and public JPL `de421.bsp` (`https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de421.bsp`, `16,788,480` bytes, `sha256: a20a7139da04cbc462454634918e9a9ca69127044e2cc9d4f9c16e238d2deedc`; NAIF mirror `16,790,528` bytes, `sha256: 08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3`).
2. A standalone FITS primary-HDU parser (`80`-byte ASCII header cards + big-endian `IEEE-754` float32 pixel arrays), gnomonic `TAN` WCS forward/inverse transformations (`CRVAL1/2`, `CRPIX1/2`, `CD` / `CDELT` / `PC` matrices), and exposure midpoint `JD_UTC` calculation (`TIMESYS = TAI` minus `34 s` before `MJD 56109` for 2010 Pan-STARRS 1 warps).
3. Sigma-clipped background estimation (`r_in = 10` to `r_out = 20` pix), iterative positive-flux moment centroiding (`r` at most `2.5` pix), circular aperture SNR (`r = 2.5` pix), calibrated magnitudes (`FPA.ZP + 2.5 * log10(EXPTIME)`), and forced circular aperture SNR at detection coordinates on all 4 reference-epoch cutouts.
4. A standalone MPC `OBS80` parser and a standalone 6D relativistic (`1PN` Schwarzschild + `DE421` Sun, Moon, and 8 planets) `DOP853` N-body integrator (`rtol = 1e-11`, `atol = 1e-13`) with topocentric light-time iteration and finite-difference $6 \times 6$ covariance propagation.

### 2.1 Artifact Integrity (Byte Sizes and SHA-256 Checksums)

All saved files in `object/precovery_2014_OV236/` were independently hashed and matched their recorded sizes and `SHA-256` digests:
- `object/precovery_2014_OV236/precovery_bundle.json`: `52,570` bytes, `sha256: 1b2642700fbb4b0d4d4cbea510011d42aaa1b5d3eb7399dccb3087f3a38c7b96`
- `object/precovery_2014_OV236/sbdb_orbit_cov.json`: `6,103` bytes, `sha256: b6ede1b0d29fcc75693ce8e657f0d00a61083ef5e3177ae9885e5f03382f52d9`
- `object/precovery_2014_OV236/mpc_obs80.txt`: `2,916` bytes, `sha256: 9b77ee37684d110b0a4f0e737f4e95d55337b915cb5da8acbca13dffcc586c03`
- `object/precovery_2014_OV236/science_warp_01..04_*.fits` (`72,000` / `69,120` bytes, `sha256: 45f9d566..`, `a3a6fd2e..`, `e9241a25..`, `cf59fcc1..`) and `ref_warp_01..04_*.fits` (`51,840` / `54,720` bytes, `sha256: e31b5b12..`, `53017610..`, `daa6c71f..`, `901ac7a4..`)

### 2.2 Independent Verification Results (`2014 OV236`)

1. **Multi-Night `U = 0` Short-Observation-Count Bundle (`2014 OV236`, `object/precovery_2014_OV236/`):**
   - **Clause (1):** `first_obs = 2014-05-24` (`MPC min JD_UTC = 2456802.012740`, `n_obs_used = 36`, `less than 50`). The 4 Pan-STARRS 1 (`F51`) $r/i/g$-band detections across 2 nights (`2010-08-18` and `2010-08-19`, `JD_UTC = 2455426.992544` to `2455427.992212`) precede `first_obs` by `1,374.0205 to 1,375.0202 days` (more than `60 d`), with zero MPC observations within `1,374.02 days`.
   - **Clause (2):** Independent centroids match saved bundle coordinates within `0.0104"` to `0.0213"`, with `SNR = 36.39, 32.59, 46.85, 15.60`. All 4 detections lie inside the $3\sigma$ back-propagated error ellipse (`Mahalanobis sigma = 1.6891, 1.6946, 1.4668, 1.1306`, at most `3.0 sigma`). Five of six frame pairs are separated by at least `20 min` (`102.061 min` and `85.183 min` same-night; `22.29 to 23.99 hr` inter-night), with motion vector consistency `0.2205 to 1.1310 sigma` (at most `3.0 sigma`).
   - **Clause (3) & `precovery-neocp-style-short-arc`:** Post-fit new residuals are `0.0582", 0.0517", 0.0477", 0.0853"` (`RMS = 0.0442"`, `max = 0.0853"`, strictly `less than 1.0"`; overall 40-obs `RMS = 0.1578"`). Semi-major axis shift is $|\Delta a| / \sigma_{a,\text{before}} = 1.8422$ (`less than 3.0`), and $\sigma_a$ uncertainty reduction is `-62.92%` (`LS`) and `-55.37%` (`SBDB`), both exceeding `50%`.
   - **Clauses (4) & (5):** Calibrated magnitudes (`20.085, 19.843, 19.607, 20.860`) are within `-0.471 to +0.785 mag` (at most `1.5 mag`) of $V_{\text{pred}} = 20.075..20.117$. Reference-epoch forced aperture SNR values are `+0.63, +1.40, -0.28, +1.89` (`|SNR|` `less than 2.5`), and Gaia DR3 / PS1 DR2 / SkyBoT show `0` contaminating objects.

---

## 3. Author Checker Determinism & 400-Control Null Model Verification

`verify-it-yourself/check_precovery_claim.py`, `verify-it-yourself/nbody_precovery.py`, and `verify-it-yourself/fits_astrometry.py` were inspected and executed twice back-to-back with `--run-null-test`:
- Both runs exited with code `0` (`~8 s` wall-clock each) and produced byte-for-byte identical stdout:
  * `2014 OV236` bundle: `4` detections (`1,374.0 d` before `first_obs`), `postfit new RMS = 0.0442"` (`max = 0.0853"`, `less than 1.0"`), `|da|/sig_a = 1.8422`, $\sigma_a$ reduction `LS = 62.92%`, `SBDB = 55.37%`.
  * `400`-control null model: `0 / 400` controls passed (`real post-fit new RMS = 0.0442"` vs control `median = 3.3097"`, `IQR = 0.8790"`, `best_control = 1.0644"`).

pass: true
