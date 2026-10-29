# Skeptic Panel Report — Role: CRITERION

panelist: CRITERION
context: Antigravity fresh subagent (invoke_subagent, role CRITERION)
target_id: asteroid-precovery-arc-extension
category: sky-archives
confirmed_scope: Precovery detection verified against the current orbit (nothing submitted to the MPC) on multi-night U=0 asteroid 2014 OV236 in object/precovery_2014_OV236/precovery_bundle.json (sha256 1b2642700fbb4b0d4d4cbea510011d42aaa1b5d3eb7399dccb3087f3a38c7b96, 4 Pan-STARRS 1 F51 r/i/g-band detections across 2 nights on 2010-08-18 and 2010-08-19 at 1,374.02 to 1,375.02 days before first_obs = 2014-05-24, 1.13-1.69 sigma inside the 3-sigma ellipse, 0.22-1.13 sigma motion consistency across all 6 pairs, post-refit PS1 residuals 0.0582", 0.0517", 0.0477", 0.0853" with RMS = 0.0442" and max = 0.0853" below 1.0", delta_a = 1.8422 sigma_a, extending the 3,870.0-day arc by 1,375.0 days to 5,244.96 days and reducing sigma_a by 62.92% LS / 55.37% SBDB for n_obs_used = 36 below 50 in precovery-neocp-style-short-arc) — with zero Gaia DR3, PS1 DR2, reference-epoch, or SkyBoT contaminants and 400 negative controls (0/400 passed, best_control = 1.0644" vs real = 0.0442").

---

## 1. Mandate and Verification Summary

As the **CRITERION** panelist operating under strict isolation, I executed an independent audit of `object/precovery_2014_OV236/precovery_bundle.json`, `object/precovery_2014_OV236/sbdb_orbit_cov.json`, `object/precovery_2014_OV236/mpc_obs80.txt`, the 4 science and 4 reference Pan-STARRS 1 (`F51`) FITS cutouts, and `verify-it-yourself/check_precovery_claim.py`, `verify-it-yourself/nbody_precovery.py`, and `verify-it-yourself/fits_astrometry.py`.

I verified all file sizes and SHA-256 digests, re-ran `python3 verify-it-yourself/check_precovery_claim.py --run-null-test`, re-queried the live JPL SBDB API (`https://ssd-api.jpl.nasa.gov/sbdb.api`), and checked every clause (1)–(5) of the full bank success criterion as well as the stretch partial win (`precovery-neocp-style-short-arc`) and the 400-trial null model.

---

## 2. Bundle Completeness Check (`object/precovery_2014_OV236/`)

`object/precovery_2014_OV236/` contains every required element of the bank's saved bundle specification:

| Required Element | `2014 OV236` Artifact (`object/precovery_2014_OV236/`) | Status |
|---|---|---|
| Object designation | `"designation": "2014 OV236"` in `precovery_bundle.json` (`52,570` B, sha256 `1b2642700fbb4b0d4d4cbea510011d42aaa1b5d3eb7399dccb3087f3a38c7b96`) | **PASS** |
| JPL SBDB JSON (orbit, covariance, `first_obs`) as fetched | `sbdb_orbit_cov.json` (`6,103` B, sha256 `b6ede1b0d29fcc75693ce8e657f0d00a61083ef5e3177ae9885e5f03382f52d9`) | **PASS** |
| MPC observation record (`get-obs` `OBS80`) as fetched | `mpc_obs80.txt` (`2,916` B, `36` obs, sha256 `9b77ee37684d110b0a4f0e737f4e95d55337b915cb5da8acbca13dffcc586c03`) | **PASS** |
| Archival image identifiers and download URLs | `warp_shortname`, `warp_archive_path`, `science_cutout_url`, and `ref_cutout_url` for all 4 detections | **PASS** |
| Cutout FITS for every frame used (science + reference) | `science_warp_01..04_*.fits` (`72,000` / `69,120` B, sha256 `45f9d566..`, `a3a6fd2e..`, `e9241a25..`, `cf59fcc1..`) + `ref_warp_01..04_*.fits` (`51,840` / `54,720` B, sha256 `e31b5b12..`, `53017610..`, `daa6c71f..`, `901ac7a4..`) | **PASS** |
| Source detections with centroid and RA/Dec/uncertainty | `centroid_x_fits`, `centroid_y_fits`, `ra_deg`, `dec_deg`, `sigma_ra_arcsec`, `sigma_dec_arcsec`, `ap_snr`, `mag_calibrated` | **PASS** |
| Predicted position & 3-sigma error ellipse from back-propagation (code saved) | Saved in `detections[*].apriori_prediction` and reproducible via `verify-it-yourself/nbody_precovery.py` + `verify-it-yourself/fits_astrometry.py` using public JPL `de421.bsp` (`sha256: a20a7139da04cbc462454634918e9a9ca69127044e2cc9d4f9c16e238d2deedc`) | **PASS** |
| Refit orbit residuals including the new points | `orbit_refit.postfit_new_residuals` (`4` new points) and `orbit_refit.postfit_all_residuals` (`40` total points) | **PASS** |
| Static-sky & moving-object check | `reference_epoch_check` + `catalog_and_skybot_checks` (`gaia_dr3_within_2arcsec`, `ps1_dr2_within_2arcsec`, `skybot_within_30arcsec`) | **PASS** |

---

## 3. Clause-by-Clause Verification of the Full Success Criterion (`2014 OV236`)

### Clause (1): Precedes `orbit.first_obs` by at least one apparition (above 60 days), and no MPC observation within 1 day

- Live and saved JPL SBDB `orbit.first_obs = 2014-05-24` (`last_obs = 2024-12-27`, `data_arc = 3,870` days, `n_obs_used = 36`).
- Saved MPC `OBS80` record (`object/precovery_2014_OV236/mpc_obs80.txt`) contains `36` observations spanning `JD_UTC = 2456802.012740` (`2014-05-24.51274`) to `JD_UTC = 2460671.953341` (`2024-12-27.453341`).
- The 4 Pan-STARRS 1 (`F51`) $r/i/g$-band precovery detections occur on `2010-08-18` and `2010-08-19` at `JD_UTC = 2455426.992544`, `2455427.921337`, `2455427.933057`, and `2455427.992212`, which precede `first_obs` by **`1,375.02020`, `1,374.09140`, `1,374.07968`, and `1,374.02053` days** (`3.76 years`, well above `60 days`), with minimum MPC separation **`1,374.02053 days`** (well above `1 day`).
- **Clause (1) Verdict:** **PASS**.

### Clause (2): At least 2 detections in distinct frames (same night separated by at least 20 min, or different nights), each inside the propagated 3-sigma ellipse, with measured motion vector consistent with predicted rate and direction within 3 sigma

- Frame separations across the `4` distinct frames on `2` nights (`2010-08-18` and `2010-08-19`): inter-night pairs `1 to 2` (`1,337.461 min` = `22.291 hr`), `1 to 3` (`1,354.338 min` = `22.572 hr`), `1 to 4` (`1,439.522 min` = `23.992 hr`), plus same-night pairs `2 to 4` (**`102.061 min`**, above `20 min`) and `3 to 4` (**`85.183 min`**, above `20 min`).
- Back-propagated $3\sigma$ error ellipse has $a_{3\sigma} = 0.6940''$ to $0.6950''$, $b_{3\sigma} = 0.2542''$ to $0.2547''$.
- A-priori offsets are `(-0.4122", -0.0207")`, `(-0.4130", -0.0459")`, `(-0.3330", -0.0866")`, and `(-0.2762", -0.0434")`, with Mahalanobis distances **`1.6891 sigma`, `1.6946 sigma`, `1.4668 sigma`, and `1.1306 sigma`**, all well inside `3.0 sigma`.
- Motion vector consistency across all 6 pairs in `precovery_bundle.json` is **`0.2205 sigma` (`1 to 2`), `0.9028 sigma` (`1 to 3`), `1.1310 sigma` (`1 to 4`), `0.7863 sigma` (`2 to 3`), `1.1222 sigma` (`2 to 4`), and `0.5878 sigma` (`3 to 4`)**, all well within `3.0 sigma`.
- **Clause (2) Verdict:** **PASS**.

### Clause (3): A-priori residual inside 3-sigma ellipse AND refit orbit residual at new epochs below 2 arcsec (below 1 arcsec for PS1), with refit changing semi-major axis by less than its a-priori 3-sigma

- Post-refit residuals at the 4 new PS1 (`F51`) epochs are **`0.0582"`, `0.0517"`, `0.0477"`, and `0.0853"`** (`RMS = 0.0442"`, `max = 0.0853"`), strictly below the `1.0 arcsec` PS1 threshold.
- Overall 40-observation (`36` MPC + `4` new) post-fit `RMS = 0.1578"` (improving upon `0.1657"` a-priori MPC-only RMS).
- Semi-major axis shift: $a_{\text{before}} = 2.6850464388\text{ AU}$ to $a_{\text{after}} = 2.6850463189\text{ AU}$, $|\Delta a| = 1.199433 \times 10^{-7}\text{ AU} = \mathbf{1.8422\,\sigma_{a,\text{before}}}$, strictly below $3.0\,\sigma_{a,\text{before}}$.
- **Clause (3) Verdict:** **PASS**.

### Clause (4): Predicted magnitude within 1.5 mag of measured magnitude

- Calibrated PS1 magnitudes (`20.085`, `19.843`, `19.607`, `20.860` mag) vs predicted $V$ magnitudes (`20.117`, `20.078`, `20.078`, `20.075` mag) have absolute differences **`0.032`, `0.235`, `0.471`, and `0.785` mag**, all below `1.5 mag`.
- **Clause (4) Verdict:** **PASS**.

### Clause (5): No static source at any detection position in another-epoch frame or in Gaia DR3/PS1 catalogs within 2 arcsec, and SkyBoT cone search at each epoch shows no other known object within 30 arcsec

- Forced-aperture photometry on the 4 reference-epoch cutouts (`MJD 56247.21106`, `56940.36931`, `56630.24244`, separated by `821 to 1,513 days` from `2010-08-18/19`) yields `forced_snr = +0.63, +1.40, -0.28, +1.89` (all `|SNR| below 2.5`) and `peak_snr_within_2arcsec = 2.58, 1.29, 0.92, 2.02` (all below `3.0`).
- Gaia DR3 (`within 2.0"`), Pan-STARRS DR2 `MeanObject` (`within 2.0"`), and IMCCE SkyBoT (`within 30.0"`): **`0` contaminating sources** at all 4 positions/epochs (`2014 OV236` itself is returned by SkyBoT at `4.179"–4.696"`, and the only other object in a `45"` cone is `2019 NL104` at `42.778"` on epoch 1, outside `30.0"`).
- **Clause (5) Verdict:** **PASS**.

---

## 4. Verification of Enumerated Partial Win Subsumed by `2014 OV236`

- **`precovery-neocp-style-short-arc` (Verified precovery above 60 d earlier for an object with `n_obs_used` below 50 in SBDB, reducing semi-major-axis uncertainty by above 50% in the refit, with covariance before/after saved):**
  - Verified on **`2014 OV236`** (`n_obs_used = 36` below `50`, $\sigma_a$ reduced by **`62.92%` LS / `55.37%` SBDB**, above `50%`), with full $6 \times 6$ covariance matrices (`cov_sbdb_before`, `cov_sbdb_after`, `cov_ls_before`, `cov_ls_after`) saved in `object/precovery_2014_OV236/precovery_bundle.json`. **PASS**.

---

## 5. Null Model and Negative Controls

Running `python3 verify-it-yourself/check_precovery_claim.py --run-null-test` executes `400` deterministic negative control tracklets:
- **`0 / 400`** negative controls pass the astrometric gate (`rms_postfit` below `1.0"`).
- Control post-fit RMS distribution: `median = 3.3097"`, `IQR = 0.8790"`, `best_control = 1.0644"`, cleanly separated from the real detection (`0.0442"` on `2014 OV236`).

pass: true
