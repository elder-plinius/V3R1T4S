# Skeptic Panel Report — Role: CRITERION

panelist: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: asteroid-precovery-arc-extension
category: sky-archives
confirmed_scope: Precovery detection verified against the current orbit (nothing submitted to the MPC) across two complete Pan-STARRS 1 (F51) archival FITS bundles — short-arc asteroid 2019 QT15 in claim/precovery_2019_QT15/precovery_bundle.json (sha256 a8fd1d6acaa5d05e238ca05078cff4fd0522908dabc12cbf6099eca35bfeca15, 3 i-band detections on 2014-11-11 spanning 39.15 min at 1,754.08 days before first_obs = 2019-08-31, 2.16-2.85 sigma inside the 3-sigma ellipse, 0.39 sigma / 0.97 sigma motion consistency, post-refit PS1 residuals 0.0216", 0.2275", 0.1756" with RMS = 0.1176" below 1.0", delta_a = 0.5962 sigma_a, multiplying the 88.0-day arc by 20.93x to 1,841.80 days / 1,841.82 days for precovery-arc-doubling and reducing sigma_a by 87.38% SBDB / 83.25% LS for n_obs_used = 41 below 50 in precovery-neocp-style-short-arc) and multi-night U=0 asteroid 2014 OV236 in claim/precovery_2014_OV236/precovery_bundle.json (sha256 1b2642700fbb4b0d4d4cbea510011d42aaa1b5d3eb7399dccb3087f3a38c7b96, 4 r/i/g-band detections on 2010-08-18/19 at 1,374.02 days before first_obs = 2014-05-24, post-refit PS1 RMS = 0.0442" and max = 0.0853" below 1.0", reducing sigma_a by 62.92% LS / 55.37% SBDB for n_obs_used = 36 below 50) — with zero Gaia DR3, PS1 DR2, reference-epoch, or SkyBoT contaminants, accompanied by 12 known-observation re-detections in ZTF (I41) and PS1 (F51) to max 0.4301" below 1.0" (precovery-reproduce-known-obs) and 400 negative controls (best_control = 1.0644" vs real = 0.0442").

---

## 1. Mandate and Verification Summary

As the **CRITERION** panelist operating under strict isolation (reading only files inside `claim/`), I executed an independent audit of `claim/CLAIM.md`, `claim/REPRODUCE.md`, `claim/author_checker_precovery.py`, `claim/nbody_precovery.py`, `claim/fits_astrometry.py`, `claim/calibration_known_obs/calibration_12_known_obs_manifest.json`, `claim/precovery_2019_QT15/precovery_bundle.json`, and `claim/precovery_2014_OV236/precovery_bundle.json`.

I verified all file sizes and SHA-256 digests, re-ran `python3 claim/author_checker_precovery.py --run-null-test`, re-queried the live JPL SBDB API (`https://ssd-api.jpl.nasa.gov/sbdb.api`), and checked every clause (1)–(5) of the full bank success criterion as well as all three substantive enumerated partial wins (`precovery-reproduce-known-obs`, `precovery-arc-doubling`, and `precovery-neocp-style-short-arc`) and the 400-trial null model.

---

## 2. Bundle Completeness Check

Both `claim/precovery_2019_QT15/` and `claim/precovery_2014_OV236/` contain every required element of the bank's saved bundle specification:

| Required Element | `2019 QT15` Artifact (`claim/precovery_2019_QT15/`) | `2014 OV236` Artifact (`claim/precovery_2014_OV236/`) | Status |
|---|---|---|---|
| Object designation | `"designation": "2019 QT15"` in `precovery_bundle.json` (`45,519` B, sha256 `a8fd1d6acaa5d05e238ca05078cff4fd0522908dabc12cbf6099eca35bfeca15`) | `"designation": "2014 OV236"` in `precovery_bundle.json` (`52,570` B, sha256 `1b2642700fbb4b0d4d4cbea510011d42aaa1b5d3eb7399dccb3087f3a38c7b96`) | **PASS** |
| JPL SBDB JSON (orbit, covariance, `first_obs`) as fetched | `sbdb_orbit_cov.json` (`6,069` B, sha256 `98c97fe6eabb7b58bbabfea79ca3cfc4ab3613411513307da8ad667143dfb1ba`) | `sbdb_orbit_cov.json` (`6,103` B, sha256 `b6ede1b0d29fcc75693ce8e657f0d00a61083ef5e3177ae9885e5f03382f52d9`) | **PASS** |
| MPC observation record (`get-obs` `OBS80`) as fetched | `mpc_obs80.txt` (`3,321` B, `41` obs, sha256 `04f0bbaf3c8191c1d533ef8c7d50efa63f41e6d69d8c652fd41efbdbde797ff5`) | `mpc_obs80.txt` (`2,916` B, `36` obs, sha256 `9b77ee37684d110b0a4f0e737f4e95d55337b915cb5da8acbca13dffcc586c03`) | **PASS** |
| Archival image identifiers and download URLs | `warp_shortname`, `warp_archive_path`, `science_cutout_url`, and `ref_cutout_url` for all 3 detections | `warp_shortname`, `warp_archive_path`, `science_cutout_url`, and `ref_cutout_url` for all 4 detections | **PASS** |
| Cutout FITS for every frame used (science + reference) | `science_warp_01..03_*.fits` (`69,120` B each, sha256 `654de59c..`, `9a6de81b..`, `0673ba63..`) + `ref_warp_01..03_*.fits` (`51,840` B each, sha256 `c3956d4b..`, `1e9eb95e..`, `607c2cd0..`) | `science_warp_01..04_*.fits` (`72,000` / `69,120` B, sha256 `45f9d566..`, `a3a6fd2e..`, `e9241a25..`, `cf59fcc1..`) + `ref_warp_01..04_*.fits` (`51,840` / `54,720` B, sha256 `e31b5b12..`, `53017610..`, `daa6c71f..`, `901ac7a4..`) | **PASS** |
| Source detections with centroid and RA/Dec/uncertainty | `centroid_x_fits`, `centroid_y_fits`, `ra_deg`, `dec_deg`, `sigma_ra_arcsec`, `sigma_dec_arcsec`, `ap_snr`, `mag_calibrated` | `centroid_x_fits`, `centroid_y_fits`, `ra_deg`, `dec_deg`, `sigma_ra_arcsec`, `sigma_dec_arcsec`, `ap_snr`, `mag_calibrated` | **PASS** |
| Predicted position & 3-sigma error ellipse from back-propagation (code saved) | Saved in `detections[*].apriori_prediction` and reproducible via `claim/nbody_precovery.py` (`16,423` B, sha256 `419137715695d624a1a9042cc0d5d21daf270db4c3ef8a24aef7b7a2ba28a21f`) + `claim/fits_astrometry.py` (`26,951` B, sha256 `63c450c616e93229355b13d5e18276941d4672ed068f59fe76f3f3a4fdda11c2`) + `claim/de421_2009_2027.npz` (`1,900,024` B, sha256 `4ccc342138b7c5b552eb2f2a88cd5260b361c58741659d181e4a05e27838261c`) | Same saved code and ephemeris; predictions in `detections[*].apriori_prediction` | **PASS** |
| Refit orbit residuals including the new points | `orbit_refit.postfit_new_residuals` (`3` new points) and `orbit_refit.postfit_all_residuals` (`44` total points) | `orbit_refit.postfit_new_residuals` (`4` new points) and `orbit_refit.postfit_all_residuals` (`40` total points) | **PASS** |
| Static-sky & moving-object check | `reference_epoch_check` + `catalog_and_skybot_checks` (`gaia_dr3_within_2arcsec`, `ps1_dr2_within_2arcsec`, `skybot_within_30arcsec`) | `reference_epoch_check` + `catalog_and_skybot_checks` (`gaia_dr3_within_2arcsec`, `ps1_dr2_within_2arcsec`, `skybot_within_30arcsec`) | **PASS** |

---

## 3. Clause-by-Clause Verification of the Full Success Criterion

### Clause (1): Precedes `orbit.first_obs` by at least one apparition (above 60 days), and no MPC observation within 1 day

- **`2019 QT15`:**
  - Live and saved JPL SBDB `orbit.first_obs = 2019-08-31` (`last_obs = 2019-11-27`, `data_arc = 88` days, `n_obs_used = 41`).
  - Saved MPC `OBS80` record (`claim/precovery_2019_QT15/mpc_obs80.txt`) contains `41` observations spanning `JD_UTC = 2458727.070780` (`2019-08-31.57078`) to `JD_UTC = 2458814.787020` (`2019-11-27.28702`).
  - The 3 Pan-STARRS 1 (`F51`) $i$-band precovery detections occur on `2014-11-11` at `JD_UTC = 2456972.966511`, `2456972.980097`, and `2456972.993696` (`MJD_UTC = 56972.466511`, `56972.480097`, `56972.493696`), which precede `first_obs` by **`1,754.10427`, `1,754.09068`, and `1,754.07708` days** (`4.80 years`, well above the `60 days` minimum).
  - The minimum time separation from any observation in the MPC record is **`1,754.07708 days`** (well above the `1 day` minimum).
- **`2014 OV236`:**
  - Live and saved JPL SBDB `orbit.first_obs = 2014-05-24` (`last_obs = 2024-12-27`, `data_arc = 3,870` days, `n_obs_used = 36`).
  - Saved MPC `OBS80` record (`claim/precovery_2014_OV236/mpc_obs80.txt`) contains `36` observations spanning `JD_UTC = 2456802.012740` (`2014-05-24.51274`) to `JD_UTC = 2460671.953341` (`2024-12-27.453341`).
  - The 4 Pan-STARRS 1 (`F51`) $r/i/g$-band precovery detections occur on `2010-08-18` and `2010-08-19` at `JD_UTC = 2455426.992544`, `2455427.921337`, `2455427.933057`, and `2455427.992212`, which precede `first_obs` by **`1,375.02020`, `1,374.09140`, `1,374.07968`, and `1,374.02053` days** (`3.76 years`, well above `60 days`), with minimum MPC separation **`1,374.02053 days`** (well above `1 day`).
- **Clause (1) Verdict:** **PASS**.

### Clause (2): At least 2 detections in distinct frames (same night separated by at least 20 min, or different nights), each inside the propagated 3-sigma ellipse, with measured motion vector consistent with predicted rate and direction within 3 sigma

- **`2019 QT15` (`3` distinct frames on `2014-11-11`):**
  - Time span: `pair 1 to 3` is separated by **`39.147 min`** (`0.65246 hr`, meeting the at-least-`20 min` same-night requirement; `pair 1 to 2` is `19.564 min` and `pair 2 to 3` is `19.583 min`).
  - Back-propagated $3\sigma$ error ellipse at `JD 2456972.966511` has semi-major axis $a_{3\sigma} = 116.9141''$, semi-minor axis $b_{3\sigma} = 0.5707''$, position angle `PA = 77.901 deg`.
  - A-priori offsets $(\Delta\alpha\cos\delta, \Delta\delta)$ are `(+27.9861", +6.5348")`, `(+27.7690", +6.4117")`, and `(+28.1051", +6.6316")`, corresponding to Mahalanobis distances **`2.4377 sigma`, `2.1571 sigma`, and `2.8534 sigma`** in `precovery_bundle.json` (`2.4383, 2.1566, 2.8529 sigma` in `CLAIM.md` table), all strictly inside the $3\sigma$ boundary (`3.0 sigma`).
  - Motion vector consistency on `pair 1 to 3` (`dt = 39.147 min`): measured displacement `(-19.2690", -9.8960")` (`total = 21.6616"`), measured rate `(-29.5329"/hr, -15.1673"/hr)` (`PA = 242.816 deg`) vs predicted rate `(-29.7149"/hr, -15.3157"/hr)` (`PA = 242.732 deg`), yielding consistency **`0.9729 sigma`** in `precovery_bundle.json` (`0.3881 sigma` under the `0.158"/0.141"` centroid uncertainty floor in `CLAIM.md`), and for all pairs `1.5087 sigma` (`pair 1 to 2`) and `2.6564 sigma` (`pair 2 to 3`) in `precovery_bundle.json` (`1.0531` and `1.4250 sigma` in `CLAIM.md`), all at or below `3.0 sigma`.
- **`2014 OV236` (`4` distinct frames across `2` nights, `2010-08-18` and `2010-08-19`):**
  - Frame separations: inter-night pairs `1 to 2` (`1,337.461 min` = `22.291 hr`), `1 to 3` (`1,354.338 min` = `22.572 hr`), `1 to 4` (`1,439.522 min` = `23.992 hr`), plus same-night pairs `2 to 4` (**`102.061 min`**, above `20 min`) and `3 to 4` (**`85.183 min`**, above `20 min`).
  - Back-propagated $3\sigma$ error ellipse has $a_{3\sigma} = 0.6940''$ to $0.6950''$, $b_{3\sigma} = 0.2542''$ to $0.2547''$.
  - A-priori offsets are `(-0.4122", -0.0207")`, `(-0.4130", -0.0459")`, `(-0.3330", -0.0866")`, and `(-0.2762", -0.0434")`, with Mahalanobis distances **`1.6891 sigma`, `1.6946 sigma`, `1.4668 sigma`, and `1.1306 sigma`** in `precovery_bundle.json` (`1.6889, 1.6897, 1.4660, 1.1325 sigma` in `author_checker_precovery.py`), all well inside `3.0 sigma`.
  - Motion vector consistency across all 6 pairs in `precovery_bundle.json` is **`0.2205 sigma` (`1 to 2`), `0.9028 sigma` (`1 to 3`), `1.1310 sigma` (`1 to 4`), `0.7863 sigma` (`2 to 3`), `1.1222 sigma` (`2 to 4`), and `0.5878 sigma` (`3 to 4`)**, all well within `3.0 sigma`.
- **Clause (2) Verdict:** **PASS**.

### Clause (3): A-priori residual inside 3-sigma ellipse AND refit orbit residual at new epochs below 2 arcsec (below 1 arcsec for PS1), with refit changing semi-major axis by less than its a-priori 3-sigma

- **`2019 QT15`:**
  - Post-refit residuals at the 3 new PS1 (`F51`) epochs from 6D relativistic N-body Gauss-Newton differential correction (`refit_orbit_gauss_newton` in `claim/fits_astrometry.py`) are **`0.0216"`, `0.2275"`, and `0.1756"`** (`RMS = 0.1176"`, `max = 0.2275"`), strictly below the `1.0 arcsec` PS1 threshold.
  - Overall 44-observation (`41` MPC + `3` new) post-fit `RMS = 0.1779"` (vs `0.1747"` a-priori MPC-only RMS).
  - Semi-major axis shift: $a_{\text{before}} = 3.0067541930\text{ AU}$ to $a_{\text{after}} = 3.0067668247\text{ AU}$, $|\Delta a| = 1.263169 \times 10^{-5}\text{ AU} = \mathbf{0.5962\,\sigma_{a,\text{before}}}$, strictly below $3.0\,\sigma_{a,\text{before}}$.
- **`2014 OV236`:**
  - Post-refit residuals at the 4 new PS1 (`F51`) epochs are **`0.0582"`, `0.0517"`, `0.0477"`, and `0.0853"`** (`RMS = 0.0442"`, `max = 0.0853"`), strictly below the `1.0 arcsec` PS1 threshold.
  - Overall 40-observation (`36` MPC + `4` new) post-fit `RMS = 0.1578"` (improving upon `0.1657"` a-priori MPC-only RMS).
  - Semi-major axis shift: $a_{\text{before}} = 2.6850464388\text{ AU}$ to $a_{\text{after}} = 2.6850463189\text{ AU}$, $|\Delta a| = 1.199433 \times 10^{-7}\text{ AU} = \mathbf{1.8422\,\sigma_{a,\text{before}}}$, strictly below $3.0\,\sigma_{a,\text{before}}$.
- **Clause (3) Verdict:** **PASS**.

### Clause (4): Predicted magnitude within 1.5 mag of measured magnitude

- **`2019 QT15`:** Calibrated PS1 magnitudes (`21.383`, `21.293`, `21.186` mag) vs predicted $V$ magnitudes (`20.758`, `20.759`, `20.759` mag) have absolute differences **`0.625`, `0.534`, and `0.427` mag**, all below `1.5 mag`.
- **`2014 OV236`:** Calibrated PS1 magnitudes (`20.085`, `19.843`, `19.607`, `20.860` mag) vs predicted $V$ magnitudes (`20.117`, `20.078`, `20.078`, `20.075` mag) have absolute differences **`0.032`, `0.235`, `0.471`, and `0.785` mag**, all below `1.5 mag`.
- **Clause (4) Verdict:** **PASS**.

### Clause (5): No static source at any detection position in another-epoch frame or in Gaia DR3/PS1 catalogs within 2 arcsec, and SkyBoT cone search at each epoch shows no other known object within 30 arcsec

- **`2019 QT15`:**
  - Forced-aperture photometry on the 3 reference-epoch cutouts (`MJD 55530.31502`, separated by `1,442 days` from `2014-11-11`) yields `forced_snr = +0.37, -1.90, -0.66` (all `|SNR| below 2.5`) and `peak_snr_within_2arcsec = 2.51, 1.42, 1.28` (all below `3.0`).
  - Gaia DR3 cone search (`within 2.0"`): **`0` sources** at all 3 positions.
  - Pan-STARRS DR2 `MeanObject` cone search (`within 2.0"`): **`0` sources** at all 3 positions.
  - IMCCE SkyBoT cone search (`within 30.0"` at `F51`): **`0` other known solar system objects** at all 3 epochs (nearest background object `2021 HP15` is at `33.716"`, `38.490"`, and `42.875"`, outside `30.0"`).
- **`2014 OV236`:**
  - Forced-aperture photometry on the 4 reference-epoch cutouts (`MJD 56247.21106`, `56940.36931`, `56630.24244`, separated by `821 to 1,513 days` from `2010-08-18/19`) yields `forced_snr = +0.63, +1.40, -0.28, +1.89` (all `|SNR| below 2.5`) and `peak_snr_within_2arcsec = 2.58, 1.29, 0.92, 2.02` (all below `3.0`).
  - Gaia DR3 (`within 2.0"`), Pan-STARRS DR2 `MeanObject` (`within 2.0"`), and IMCCE SkyBoT (`within 30.0"`): **`0` contaminating sources** at all 4 positions/epochs (`2014 OV236` itself is returned by SkyBoT at `4.179"–4.696"`, and the only other object in a `45"` cone is `2019 NL104` at `42.778"` on epoch 1, outside `30.0"`).
- **Clause (5) Verdict:** **PASS**.

---

## 4. Verification of Enumerated Partial Wins (Subsumed by the Full Win)

1. **`precovery-reproduce-known-obs` (For at least 10 objects, re-detect in public ZTF/PS1 frames observations in the MPC record to below 1 arcsec):**
   - Verified in `claim/calibration_known_obs/calibration_12_known_obs_manifest.json` (`14,282` B, sha256 `5a0643819fd46e1a51a0f866fcd31f0232a51e8a2f92422d358592221e899f5b`) across **`12` distinct minor planets** (`1` ZTF `I41` cutout + `11` PS1 `F51` cutouts): `2020 AV2` (`0.2339"`), `2010 QW8` (`0.2515"`), `2014 OJ66` (`0.3709"`), `2012 RJ28` (`0.1162"`), `2013 MV14` (`0.1844"`), `2013 MO15` (`0.2874"`), `2013 MG22` (`0.4301"`), `2013 MB24` (`0.4154"`), `2013 MV25` (`0.3045"`), `2013 ME27` (`0.3630"`), `2013 NG` (`0.1617"`), and `2014 VH21` (`0.2417"`).
   - Aggregate metrics: `mean = 0.2801"`, `RMS = 0.2961"`, `max = 0.4301"` (strictly below `1.0"`). **PASS**.
2. **`precovery-arc-doubling` (Doubles an object's data arc, new arc at least 2x JPL `data_arc`, for an object with `data_arc` below 365 d):**
   - Verified on **`2019 QT15`**: JPL SBDB `data_arc = 88.0 days` (below `365 days`). The verified `2014-11-11` precovery extends the observed arc to **`1,841.82 days`** (`1,841.80 days` in `CLAIM.md`), a **`20.93x`** multiplication factor (far above `2.0x`). **PASS**.
3. **`precovery-neocp-style-short-arc` (Verified precovery above 60 d earlier for an object with `n_obs_used` below 50 in SBDB, reducing semi-major-axis uncertainty by above 50% in the refit, with covariance before/after saved):**
   - Verified independently on **both** **`2019 QT15`** (`n_obs_used = 41` below `50`, $\sigma_a$ reduced by **`87.38%` SBDB / `83.25%` LS**, above `50%`) and **`2014 OV236`** (`n_obs_used = 36` below `50`, $\sigma_a$ reduced by **`62.92%` LS / `55.37%` SBDB**, above `50%`), with full $6 \times 6$ covariance matrices (`cov_sbdb_before`, `cov_sbdb_after`, `cov_ls_before`, `cov_ls_after`) saved in each bundle. **PASS**.

---

## 5. Null Model and Negative Controls

Running `python3 claim/author_checker_precovery.py --run-null-test` executes `400` deterministic negative control tracklets (`200` sky-offset background tracklets inside the 4 science FITS cutouts + `200` displaced-epoch control tracklets inside the 4 reference-epoch FITS cutouts):
- **`0 / 400`** negative controls pass the joint astrometric + SNR gate (`rms_postfit` below `1.0"` and `min(SNR)` at least `5.0`).
- Control post-fit RMS distribution: `median = 3.3097"`, `IQR = 0.8790"`, `best_control = 1.0644"`, cleanly separated from the real detections (`0.0442"` on `2014 OV236` and `0.1176"` on `2019 QT15`).

pass: true
