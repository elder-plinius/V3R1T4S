# Skeptic Panel Report — Role: `REPRODUCE`

context: Antigravity fresh subagent (invoke_subagent, role REPRODUCE)
target: `asteroid-precovery-arc-extension` (`sky-archives`)

## 1. Mandate & Verbatim Definition Quoted Before Reading Author Code

Mandate:
"Before reading the author's code, write your own checker from the definition (quote it). Verify every property and the claimed value from the saved files; re-derive every proof step. For an exhaustive search, a sample is a spot check and cannot pass. Fail on any mismatch, missing object or non-determinism."

Verbatim definition quoted from the bank target `asteroid-precovery-arc-extension`:
"A saved bundle {object designation, JPL SBDB JSON (orbit, covariance, first_obs) as fetched, the MPC observation record for the object as fetched (get-obs API OBS80 output or the MPCAT-OBS extract), archival image identifiers and download URLs, cutout FITS for every frame used, source detections with centroid and RA/Dec/uncertainty, predicted position and 3-sigma error ellipse from back-propagation (code saved), refit orbit residuals including the new points, static-sky check} such that: (1) the image epoch precedes JPL SBDB orbit.first_obs for that object (https://ssd-api.jpl.nasa.gov/sbdb.api?sstr=[designation], re-fetched live immediately before claiming) by at least one apparition (more than 60 days), and the MPC observation record for the object (get-obs API, re-fetched live) contains no observation within 1 day of that epoch; (2) at least 2 detections of the object in distinct frames (same night separated by at least 20 min, or different nights), each inside the propagated 3-sigma ellipse, with the measured motion vector between them consistent with the predicted rate and direction within 3 sigma; (3) the residual of each detection against the a-priori orbit is inside the 3-sigma ellipse AND the refit orbit residual at the new epochs is less than 2 arcsec (less than 1 arcsec for PS1), with the refit changing the semi-major axis by less than its a-priori 3-sigma; (4) the predicted magnitude is within 1.5 mag of the measured one; (5) no static source is present at any detection position in another-epoch frame or in Gaia DR3/PS1 catalogs within 2 arcsec, and a SkyBoT cone search at each epoch shows no other known object within 30 arcsec. Claim is 'precovery detection, verified against the current orbit'; nothing is submitted to the MPC."

Enumerated Partial Wins:
- `precovery-arc-doubling`: Stretch tier: a fully verified precovery (all of (1)-(5)) that doubles an object's data arc (new arc at least 2x JPL data_arc) for an object with data_arc less than 365 d; independently checkable against SBDB.
- `precovery-neocp-style-short-arc`: Stretch tier: a fully verified precovery (more than 60 d earlier) for an object with n_obs_used less than 50 in SBDB, where the added points reduce the semi-major-axis uncertainty by more than 50% in the refit; the covariance before/after saved.

---

## 2. Independent Checker Written Before Reading Author Code

Before reading `verify-it-yourself/check_precovery_claim.py`, `verify-it-yourself/nbody_precovery.py`, or `verify-it-yourself/fits_astrometry.py`, an independent checker (`indep_precovery_check.py`) was written from scratch directly from the definition, implementing:
1. Exact byte-size and `SHA-256` verification of all saved files in `object/precovery_2019_QT15/` and public JPL `de421.bsp` (`https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de421.bsp`, `16,788,480` bytes, `sha256: a20a7139da04cbc462454634918e9a9ca69127044e2cc9d4f9c16e238d2deedc`; NAIF mirror `16,790,528` bytes, `sha256: 08b20db2ae22488650641c5a9033e5bfda4b1c4b440cfeaf20f621cfa18ecdb3`).
2. A standalone FITS primary-HDU parser (`80`-byte ASCII header cards + big-endian `IEEE-754` float32 pixel arrays), gnomonic `TAN` WCS forward/inverse transformations (`CRVAL1/2`, `CRPIX1/2`, `CD` / `CDELT` / `PC` matrices), and exposure midpoint `JD_UTC` calculation (`TIMESYS = TAI` minus `35 s` before `MJD 57204` for Pan-STARRS 1 warps).
3. Sigma-clipped background estimation (`r_in = 10` to `r_out = 20` pix), iterative positive-flux moment centroiding (`r` at most `2.5` pix), circular aperture SNR (`r = 2.5` pix), calibrated magnitudes (`FPA.ZP + 2.5 * log10(EXPTIME)`), and forced circular aperture SNR at detection coordinates on all 3 reference-epoch cutouts.
4. A standalone MPC `OBS80` parser and a standalone 6D relativistic (`1PN` Schwarzschild + `DE421` Sun, Moon, and 8 planets) `DOP853` N-body integrator (`rtol = 1e-11`, `atol = 1e-13`) with topocentric light-time iteration and finite-difference $6 \times 6$ covariance propagation.

### 2.1 Artifact Integrity (Byte Sizes and SHA-256 Checksums)

All saved files in `object/precovery_2019_QT15/` were independently hashed and matched their recorded sizes and `SHA-256` digests:
- `object/precovery_2019_QT15/precovery_bundle.json`: `45,519` bytes, `sha256: a8fd1d6acaa5d05e238ca05078cff4fd0522908dabc12cbf6099eca35bfeca15`
- `object/precovery_2019_QT15/sbdb_orbit_cov.json`: `6,069` bytes, `sha256: 98c97fe6eabb7b58bbabfea79ca3cfc4ab3613411513307da8ad667143dfb1ba`
- `object/precovery_2019_QT15/mpc_obs80.txt`: `3,321` bytes, `sha256: 04f0bbaf3c8191c1d533ef8c7d50efa63f41e6d69d8c652fd41efbdbde797ff5`
- `object/precovery_2019_QT15/science_warp_01..03_*.fits` (`69,120` bytes each, `sha256: 654de59c..`, `9a6de81b..`, `0673ba63..`) and `ref_warp_01..03_*.fits` (`51,840` bytes each, `sha256: c3956d4b..`, `1e9eb95e..`, `607c2cd0..`)

### 2.2 Independent Verification Results (`2019 QT15`)

1. **Short-Arc `20.93x` Arc-Doubling & `87.38%` $\sigma_a$-Reduction Bundle (`2019 QT15`, `object/precovery_2019_QT15/`):**
   - **Clause (1):** `first_obs = 2019-08-31` (`MPC min JD_UTC = 2458727.070780`, `n_obs_used = 41`, `data_arc = 88.0 d`). The 3 Pan-STARRS 1 (`F51`) $i$-band warp detections on `2014-11-11` (`JD_UTC = 2456972.966511`, `2456972.980097`, `2456972.993696`) precede `first_obs` by `1,754.0771 to 1,754.1043 days` (more than `60 d`), with zero MPC observations within `1,754.08 days` (more than `1 d`).
   - **Clause (2):** Independent centroids match saved bundle coordinates within `0.0178"`, `0.0291"`, and `0.0732"`, with `SNR = 6.82, 6.36, 8.27`. Independent N-body propagation confirms all 3 detections lie inside the $3\sigma$ back-propagated error ellipse (`Mahalanobis sigma = 2.4238, 2.1452, 2.8430` independent; `2.4377, 2.1571, 2.8534` in `precovery_bundle.json`, all at most `3.0 sigma`). Frame pair `1 to 3` is separated by `39.147 min` (at least `20 min`), and all motion vector consistency values in `precovery_bundle.json` (`1.5087 sigma` on `1 to 2`, `0.9729 sigma` on `1 to 3`, `2.6564 sigma` on `2 to 3`) are strictly at most `3.0 sigma`.
   - **Clause (3):** Independent N-body evaluation of the post-fit orbit (`elements_after`) across all `44` observations (`41` MPC + `3` new) yields `rms_postfit_new = 0.1173"` (`0.1176"` in bundle) and `max_postfit_new = 0.2189"` (`0.2275"` in bundle, strictly `less than 1.0"`). Semi-major axis shift is $|\Delta a| = 1.2632 \times 10^{-5}\text{ AU} = 0.5962\,\sigma_{a,\text{before}}$ (strictly `less than 3.0`).
   - **Stretch Partial Wins on `2019 QT15`:**
     * `precovery-arc-doubling`: `data_arc` increases from `88.0 d` (`less than 365 d`) to `1,841.82 d` (`20.9298x`, at least `2.0x`).
     * `precovery-neocp-style-short-arc` (`n_obs_used = 41`, `less than 50`): $\sigma_a$ decreases from $2.1185 \times 10^{-5}\text{ AU}$ to $2.6743 \times 10^{-6}\text{ AU}$ (`-87.38%` SBDB reduction) and from $1.6783 \times 10^{-5}\text{ AU}$ to $2.8113 \times 10^{-6}\text{ AU}$ (`-83.25%` LS reduction), both exceeding `50%`.
   - **Clauses (4) & (5):** Calibrated magnitudes (`21.383, 21.293, 21.186`) are within `0.427 to 0.625 mag` (at most `1.5 mag`) of $V_{\text{pred}} = 20.758..20.759$. Forced aperture SNR on the 3 reference-epoch cutouts (`MJD 55530.31502`) is `+0.37, -1.90, -0.66` (`|SNR|` `less than 2.5`), with `0` Gaia DR3 (`less than 2"`), `0` PS1 DR2 (`less than 2"`), and `0` other SkyBoT (`less than 30"`) sources.
2. **Live Archival FITS Re-Download Verification:**
   - Re-downloading `science_warp_01_rings.v3.skycell.1600.050.wrp.i.56972_46650.fits` live from `https://ps1images.stsci.edu/cgi-bin/fitscut.cgi?red=/rings.v3.skycell/1600/050/rings.v3.skycell.1600.050.wrp.i.56972_46650.fits&ra=42.613783&dec=14.234694&size=120&format=fits` via `curl -4 -sS` yielded a `(120, 120)` float32 image with `max_pixel_diff = 0.0` (exact pixel-for-pixel identity with the saved FITS cutout in `object/precovery_2019_QT15/`).
3. **Negative Controls (Fault Injection):**
   - Corrupting Detection 1 of `2019 QT15` by `+5.0 arcsec` in RA yields a post-fit residual of `4.8652 arcsec` (exceeding the `1.0 arcsec` PS1 threshold and failing as required).
   - Evaluating forced-aperture SNR at Detection 1 coordinates on the reference-epoch cutout (`ref_warp_01`) yields `SNR = +0.40` (below the `5.0` detection threshold and failing as required).

---

## 3. Author Checker Determinism & 400-Control Null Model Verification

`verify-it-yourself/check_precovery_claim.py`, `verify-it-yourself/nbody_precovery.py`, and `verify-it-yourself/fits_astrometry.py` were inspected and executed twice back-to-back with `--run-null-test`:
- Both runs exited with code `0` (`~7 s` wall-clock each) and produced byte-for-byte identical stdout:
  * `2019 QT15` bundle: `3` detections (`1,754.1 d` before `first_obs`), `arc: 88 d to 1,841.8 d (20.93x)`, `postfit new RMS = 0.1176"` (`max = 0.2275"`, `less than 1.0"`), `|da|/sig_a = 0.5962`, $\sigma_a$ reduction `LS = 83.25%`, `SBDB = 87.38%`.
  * `400`-control null model: `0 / 400` controls passed (`real min_snr = 6.3600` vs control `median = -1.0100`, `best_control = 1.2800`).

pass: true
