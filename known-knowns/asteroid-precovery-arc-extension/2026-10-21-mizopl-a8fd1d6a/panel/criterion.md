# Skeptic Panel Report — Role: CRITERION

panelist: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: asteroid-precovery-arc-extension
category: sky-archives
confirmed_scope: Precovery detection verified against the current orbit (nothing submitted to the MPC) on short-arc asteroid 2019 QT15 in object/precovery_2019_QT15/precovery_bundle.json (sha256 a8fd1d6acaa5d05e238ca05078cff4fd0522908dabc12cbf6099eca35bfeca15, 3 Pan-STARRS 1 F51 i-band detections on 2014-11-11 spanning 39.15 min at 1,754.08 days before first_obs = 2019-08-31, 2.16-2.85 sigma inside the 3-sigma ellipse, 0.97 sigma motion consistency, post-refit PS1 residuals 0.0216", 0.2275", 0.1756" with RMS = 0.1176" below 1.0", delta_a = 0.5962 sigma_a, multiplying the 88.0-day arc by 20.93x to 1,841.82 days for precovery-arc-doubling and reducing sigma_a by 87.38% SBDB / 83.25% LS for n_obs_used = 41 below 50 in precovery-neocp-style-short-arc) — with zero Gaia DR3, PS1 DR2, reference-epoch, or SkyBoT contaminants and 400 negative controls (0/400 passed, best_control = 1.2800 vs real = 6.3600).

---

## 1. Mandate and Verification Summary

As the **CRITERION** panelist operating under strict isolation, I executed an independent audit of `object/precovery_2019_QT15/precovery_bundle.json`, `object/precovery_2019_QT15/sbdb_orbit_cov.json`, `object/precovery_2019_QT15/mpc_obs80.txt`, the 3 science and 3 reference Pan-STARRS 1 (`F51`) FITS cutouts, and `verify-it-yourself/check_precovery_claim.py`, `verify-it-yourself/nbody_precovery.py`, and `verify-it-yourself/fits_astrometry.py`.

I verified all file sizes and SHA-256 digests, re-ran `python3 verify-it-yourself/check_precovery_claim.py --run-null-test`, re-queried the live JPL SBDB API (`https://ssd-api.jpl.nasa.gov/sbdb.api`), and checked every clause (1)–(5) of the full bank success criterion as well as both stretch partial wins (`precovery-arc-doubling` and `precovery-neocp-style-short-arc`) and the 400-trial null model.

---

## 2. Bundle Completeness Check (`object/precovery_2019_QT15/`)

`object/precovery_2019_QT15/` contains every required element of the bank's saved bundle specification:

| Required Element | `2019 QT15` Artifact (`object/precovery_2019_QT15/`) | Status |
|---|---|---|
| Object designation | `"designation": "2019 QT15"` in `precovery_bundle.json` (`45,519` B, sha256 `a8fd1d6acaa5d05e238ca05078cff4fd0522908dabc12cbf6099eca35bfeca15`) | **PASS** |
| JPL SBDB JSON (orbit, covariance, `first_obs`) as fetched | `sbdb_orbit_cov.json` (`6,069` B, sha256 `98c97fe6eabb7b58bbabfea79ca3cfc4ab3613411513307da8ad667143dfb1ba`) | **PASS** |
| MPC observation record (`get-obs` `OBS80`) as fetched | `mpc_obs80.txt` (`3,321` B, `41` obs, sha256 `04f0bbaf3c8191c1d533ef8c7d50efa63f41e6d69d8c652fd41efbdbde797ff5`) | **PASS** |
| Archival image identifiers and download URLs | `warp_shortname`, `warp_archive_path`, `science_cutout_url`, and `ref_cutout_url` for all 3 detections | **PASS** |
| Cutout FITS for every frame used (science + reference) | `science_warp_01..03_*.fits` (`69,120` B each, sha256 `654de59c..`, `9a6de81b..`, `0673ba63..`) + `ref_warp_01..03_*.fits` (`51,840` B each, sha256 `c3956d4b..`, `1e9eb95e..`, `607c2cd0..`) | **PASS** |
| Source detections with centroid and RA/Dec/uncertainty | `centroid_x_fits`, `centroid_y_fits`, `ra_deg`, `dec_deg`, `sigma_ra_arcsec`, `sigma_dec_arcsec`, `ap_snr`, `mag_calibrated` | **PASS** |
| Predicted position & 3-sigma error ellipse from back-propagation (code saved) | Saved in `detections[*].apriori_prediction` and reproducible via `verify-it-yourself/nbody_precovery.py` + `verify-it-yourself/fits_astrometry.py` using public JPL `de421.bsp` (`sha256: a20a7139da04cbc462454634918e9a9ca69127044e2cc9d4f9c16e238d2deedc`) | **PASS** |
| Refit orbit residuals including the new points | `orbit_refit.postfit_new_residuals` (`3` new points) and `orbit_refit.postfit_all_residuals` (`44` total points) | **PASS** |
| Static-sky & moving-object check | `reference_epoch_check` + `catalog_and_skybot_checks` (`gaia_dr3_within_2arcsec`, `ps1_dr2_within_2arcsec`, `skybot_within_30arcsec`) | **PASS** |

---

## 3. Clause-by-Clause Verification of the Full Success Criterion (`2019 QT15`)

### Clause (1): Precedes `orbit.first_obs` by at least one apparition (above 60 days), and no MPC observation within 1 day

- Live and saved JPL SBDB `orbit.first_obs = 2019-08-31` (`last_obs = 2019-11-27`, `data_arc = 88` days, `n_obs_used = 41`).
- Saved MPC `OBS80` record (`object/precovery_2019_QT15/mpc_obs80.txt`) contains `41` observations spanning `JD_UTC = 2458727.070780` (`2019-08-31.57078`) to `JD_UTC = 2458814.787020` (`2019-11-27.28702`).
- The 3 Pan-STARRS 1 (`F51`) $i$-band precovery detections occur on `2014-11-11` at `JD_UTC = 2456972.966511`, `2456972.980097`, and `2456972.993696` (`MJD_UTC = 56972.466511`, `56972.480097`, `56972.493696`), which precede `first_obs` by **`1,754.10427`, `1,754.09068`, and `1,754.07708` days** (`4.80 years`, well above the `60 days` minimum).
- The minimum time separation from any observation in the MPC record is **`1,754.07708 days`** (well above the `1 day` minimum).
- **Clause (1) Verdict:** **PASS**.

### Clause (2): At least 2 detections in distinct frames (same night separated by at least 20 min, or different nights), each inside the propagated 3-sigma ellipse, with measured motion vector consistent with predicted rate and direction within 3 sigma

- Time span across the `3` distinct frames on `2014-11-11`: `pair 1 to 3` is separated by **`39.147 min`** (`0.65246 hr`, meeting the at-least-`20 min` same-night requirement; `pair 1 to 2` is `19.564 min` and `pair 2 to 3` is `19.583 min`).
- Back-propagated $3\sigma$ error ellipse at `JD 2456972.966511` has semi-major axis $a_{3\sigma} = 116.9141''$, semi-minor axis $b_{3\sigma} = 0.5707''$, position angle `PA = 77.901 deg`.
- A-priori offsets $(\Delta\alpha\cos\delta, \Delta\delta)$ are `(+27.9861", +6.5348")`, `(+27.7690", +6.4117")`, and `(+28.1051", +6.6316")`, corresponding to Mahalanobis distances **`2.4377 sigma`, `2.1571 sigma`, and `2.8534 sigma`** in `precovery_bundle.json`, all strictly inside the $3\sigma$ boundary (`3.0 sigma`).
- Motion vector consistency on `pair 1 to 3` (`dt = 39.147 min`): measured displacement `(-19.2690", -9.8960")` (`total = 21.6616"`), measured rate `(-29.5329"/hr, -15.1673"/hr)` (`PA = 242.816 deg`) vs predicted rate `(-29.7149"/hr, -15.3157"/hr)` (`PA = 242.732 deg`), yielding consistency **`0.9729 sigma`** in `precovery_bundle.json`, and for all pairs `1.5087 sigma` (`pair 1 to 2`) and `2.6564 sigma` (`pair 2 to 3`), all below `3.0 sigma`.
- **Clause (2) Verdict:** **PASS**.

### Clause (3): A-priori residual inside 3-sigma ellipse AND refit orbit residual at new epochs below 2 arcsec (below 1 arcsec for PS1), with refit changing semi-major axis by less than its a-priori 3-sigma

- Post-refit residuals at the 3 new PS1 (`F51`) epochs from 6D relativistic N-body Gauss-Newton differential correction (`refit_orbit_gauss_newton` in `verify-it-yourself/fits_astrometry.py`) are **`0.0216"`, `0.2275"`, and `0.1756"`** (`RMS = 0.1176"`, `max = 0.2275"`), strictly below the `1.0 arcsec` PS1 threshold.
- Overall 44-observation (`41` MPC + `3` new) post-fit `RMS = 0.1779"` (vs `0.1747"` a-priori MPC-only RMS).
- Semi-major axis shift: $a_{\text{before}} = 3.0067541930\text{ AU}$ to $a_{\text{after}} = 3.0067668247\text{ AU}$, $|\Delta a| = 1.263169 \times 10^{-5}\text{ AU} = \mathbf{0.5962\,\sigma_{a,\text{before}}}$, strictly below $3.0\,\sigma_{a,\text{before}}$.
- **Clause (3) Verdict:** **PASS**.

### Clause (4): Predicted magnitude within 1.5 mag of measured magnitude

- Calibrated PS1 magnitudes (`21.383`, `21.293`, `21.186` mag) vs predicted $V$ magnitudes (`20.758`, `20.759`, `20.759` mag) have absolute differences **`0.625`, `0.534`, and `0.427` mag**, all below `1.5 mag`.
- **Clause (4) Verdict:** **PASS**.

### Clause (5): No static source at any detection position in another-epoch frame or in Gaia DR3/PS1 catalogs within 2 arcsec, and SkyBoT cone search at each epoch shows no other known object within 30 arcsec

- Forced-aperture photometry on the 3 reference-epoch cutouts (`MJD 55530.31502`, separated by `1,442 days` from `2014-11-11`) yields `forced_snr = +0.37, -1.90, -0.66` (all `|SNR| below 2.5`) and `peak_snr_within_2arcsec = 2.51, 1.42, 1.28` (all below `3.0`).
- Gaia DR3 cone search (`within 2.0"`): **`0` sources** at all 3 positions.
- Pan-STARRS DR2 `MeanObject` cone search (`within 2.0"`): **`0` sources** at all 3 positions.
- IMCCE SkyBoT cone search (`within 30.0"` at `F51`): **`0` other known solar system objects** at all 3 epochs (nearest background object `2021 HP15` is at `33.716"`, `38.490"`, and `42.875"`, outside `30.0"`).
- **Clause (5) Verdict:** **PASS**.

---

## 4. Verification of Enumerated Partial Wins Subsumed by `2019 QT15`

1. **`precovery-arc-doubling` (Doubles an object's data arc, new arc at least 2x JPL `data_arc`, for an object with `data_arc` below 365 d):**
   - Verified on **`2019 QT15`**: JPL SBDB `data_arc = 88.0 days` (below `365 days`). The verified `2014-11-11` precovery extends the observed arc to **`1,841.82 days`**, a **`20.93x`** multiplication factor (far above `2.0x`). **PASS**.
2. **`precovery-neocp-style-short-arc` (Verified precovery above 60 d earlier for an object with `n_obs_used` below 50 in SBDB, reducing semi-major-axis uncertainty by above 50% in the refit, with covariance before/after saved):**
   - Verified on **`2019 QT15`** (`n_obs_used = 41` below `50`, $\sigma_a$ reduced by **`87.38%` SBDB / `83.25%` LS**, above `50%`), with full $6 \times 6$ covariance matrices (`cov_sbdb_before`, `cov_sbdb_after`, `cov_ls_before`, `cov_ls_after`) saved in `object/precovery_2019_QT15/precovery_bundle.json`. **PASS**.

---

## 5. Null Model and Negative Controls

Running `python3 verify-it-yourself/check_precovery_claim.py --run-null-test` executes `400` deterministic negative control tracklets (`200` sky-offset background tracklets inside the 3 science FITS cutouts + `200` displaced-epoch control tracklets inside the 3 reference-epoch FITS cutouts of `2019 QT15`):
- **`0 / 400`** negative controls pass the detection gate (`min(SNR)` at least `5.0`).
- Control 3-frame `min(SNR)` distribution: `median = -1.0100`, `best_control = 1.2800`, cleanly separated from the real detection (`real min(SNR) = 6.3600`, post-fit `RMS = 0.1176"`).

pass: true
