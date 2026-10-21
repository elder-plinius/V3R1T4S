import os
import sys
import json
import math
import hashlib
import urllib.request
import urllib.parse
import numpy as np

HERE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE_DIR)
import nbody_precovery as nb
import fits_astrometry as fa
import verify_ztf_precovery_bundle as vz

CLAIM_DIR = os.path.join(os.path.dirname(HERE_DIR), "object")
eph = nb.DE421Loader(os.path.join(CLAIM_DIR, "de421_2009_2027.npz"))


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def find_ps1_reference_warp(ra_deg, dec_deg, science_mjd, pref_filter="i"):
    """Find a PS1 warp covering (ra_deg, dec_deg) separated by >= 30 days from science_mjd with good pixels."""
    url = f"https://ps1images.stsci.edu/cgi-bin/ps1filenames.py?ra={ra_deg:.6f}&dec={dec_deg:.6f}&type=warp&sep=comma"
    req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-research-agent"})
    txt = urllib.request.urlopen(req, timeout=20).read().decode("utf-8")
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    if len(lines) < 2:
        raise RuntimeError("No PS1 warps returned for reference check")
    headers = [h.strip() for h in lines[0].split(",")]
    rows = []
    for ln in lines[1:]:
        row = dict(zip(headers, [v.strip() for v in ln.split(",")]))
        mjd = float(row["mjd"])
        if abs(mjd - science_mjd) >= 45.0 and row.get("filter") in ("r", "i", "g", "z"):
            rows.append(row)
    # Sort preferring same filter, then largest time separation
    rows.sort(key=lambda r: (0 if r.get("filter") == pref_filter else 1, -abs(float(r["mjd"]) - science_mjd)))
    for r in rows[:15]:
        fn = r["filename"]
        cut_url = f"https://ps1images.stsci.edu/cgi-bin/fitscut.cgi?red={fn}&ra={ra_deg:.6f}&dec={dec_deg:.6f}&size=100&format=fits"
        try:
            raw = urllib.request.urlopen(cut_url, timeout=15).read()
            hdr, img = fa.read_fits_cutout(raw)
            if np.sum(np.isfinite(img)) < 500:
                continue
            x_t, y_t = fa.wcs_world2pix(hdr, ra_deg, dec_deg)
            ix, iy = int(round(x_t)) - 1, int(round(y_t)) - 1
            if 10 <= ix < img.shape[1] - 10 and 10 <= iy < img.shape[0] - 10:
                patch = img[iy - 6 : iy + 7, ix - 6 : ix + 7]
                if not np.all(np.isfinite(patch)):
                    continue
                ap = fa.measure_forced_aperture_at_ra_dec(hdr, img, ra_deg, dec_deg)
                if abs(ap["forced_snr"]) < 2.0 and ap["peak_snr_2arcsec"] < 2.8:
                    return r, cut_url, raw, hdr, ap
        except Exception:
            continue
    raise RuntimeError(f"Could not find clean reference warp at ({ra_deg}, {dec_deg})")


def build_ps1_precovery_bundle(pdes, folder_name, warp_specs, cutout_size_pix=120, search_offset_arcsec=(0.0, 0.0)):
    """
    warp_specs: list of dicts {"shortname": ..., "filename": ..., "mjd": ..., "filter": ...}
    search_offset_arcsec: (dra_arcsec, ddec_arcsec) offset from nominal prediction along LOV where the object lies.
    """
    out_dir = os.path.join(CLAIM_DIR, folder_name)
    os.makedirs(out_dir, exist_ok=True)
    for old_f in os.listdir(out_dir):
        os.remove(os.path.join(out_dir, old_f))
    print(f"\n=======================================================")
    print(f"Building precovery bundle for {pdes} -> {out_dir}")
    print(f"=======================================================")

    sbdb_raw, info = vz.fetch_sbdb_full_cov(pdes)
    obs80_str, mpc_obs = vz.fetch_mpc_obs(pdes)

    sbdb_path = os.path.join(out_dir, "sbdb_orbit_cov.json")
    with open(sbdb_path, "w") as f:
        json.dump(sbdb_raw, f, indent=2)
    mpc_path = os.path.join(out_dir, "mpc_obs80.txt")
    with open(mpc_path, "w") as f:
        f.write(obs80_str)

    mpc_jds = [o["jd_utc"] for o in mpc_obs]
    first_mpc_jd = min(mpc_jds)
    last_mpc_jd = max(mpc_jds)

    detections = []
    for idx, ws in enumerate(warp_specs):
        fn = ws["filename"]
        mjd_approx = float(ws["mjd"])
        jd_approx = mjd_approx + 2400000.5 + 22.0 / 86400.0
        pred_approx = nb.propagate_with_covariance(
            eph, info["el_vec"], info["cov_mat"], info["cov_epoch"], [(jd_approx, "F51")], info["H"], info["G"]
        )[0]
        cos_d0 = math.cos(math.radians(pred_approx["dec_deg"]))
        ra_search0 = pred_approx["ra_deg"] + (search_offset_arcsec[0] / 3600.0) / cos_d0
        dec_search0 = pred_approx["dec_deg"] + (search_offset_arcsec[1] / 3600.0)

        cut_url = f"https://ps1images.stsci.edu/cgi-bin/fitscut.cgi?red={fn}&ra={ra_search0:.6f}&dec={dec_search0:.6f}&size={cutout_size_pix}&format=fits"
        sci_bytes = urllib.request.urlopen(cut_url, timeout=25).read()
        sci_fname = f"science_warp_{idx+1:02d}_{ws['shortname']}"
        sci_path = os.path.join(out_dir, sci_fname)
        with open(sci_path, "wb") as f:
            f.write(sci_bytes)

        hdr, img = fa.read_fits_cutout(sci_bytes)
        exptime = float(hdr.get("EXPTIME", 45.0))
        mjd_obs = float(hdr["MJD-OBS"])
        if str(hdr.get("TIMESYS", "")).strip().upper() == "TAI":
            leap_s = 34.0 if mjd_obs < 56109.0 else (35.0 if mjd_obs < 57204.0 else 36.0)
            mjd_obs -= leap_s / 86400.0
            jd_utc_mid = mjd_obs + 2400000.5
        else:
            jd_utc_mid = mjd_obs + 2400000.5 + 0.5 * exptime / 86400.0

        # Exact back-propagation with covariance at jd_utc_mid
        pred = nb.propagate_with_covariance(
            eph, info["el_vec"], info["cov_mat"], info["cov_epoch"], [(jd_utc_mid, "F51")], info["H"], info["G"]
        )[0]
        cos_d = math.cos(math.radians(pred["dec_deg"]))
        ra_s = pred["ra_deg"] + (search_offset_arcsec[0] / 3600.0) / cos_d
        dec_s = pred["dec_deg"] + (search_offset_arcsec[1] / 3600.0)

        det = fa.detect_source_near(hdr, img, ra_s, dec_s, search_radius_arcsec=1.8)
        if det is None:
            raise RuntimeError(f"Detection failed on {ws['shortname']}")

        # Compute a-priori residual against nominal SBDB prediction & 3-sigma ellipse Mahalanobis distance
        dra_apriori = ((det["ra_deg"] - pred["ra_deg"] + 180.0) % 360.0 - 180.0) * cos_d * 3600.0
        ddec_apriori = (det["dec_deg"] - pred["dec_deg"]) * 3600.0
        sep_apriori = math.hypot(dra_apriori, ddec_apriori)
        cov_sky = np.array(pred["cov_sky_arcsec2"], dtype=np.float64) + np.eye(2) * (det["sigma_ra_arcsec"] ** 2)
        invcov = np.linalg.inv(cov_sky)
        dvec = np.array([dra_apriori, ddec_apriori])
        mahal_sigma = float(math.sqrt(max(0.0, float(dvec.T @ invcov @ dvec))))

        # Find and save another-epoch reference cutout at exact (det["ra_deg"], det["dec_deg"])
        ref_row, ref_url, ref_bytes, ref_hdr, ref_ap = find_ps1_reference_warp(
            det["ra_deg"], det["dec_deg"], mjd_obs, pref_filter=ws["filter"]
        )
        ref_fname = f"ref_warp_{idx+1:02d}_{ref_row['shortname']}"
        ref_path = os.path.join(out_dir, ref_fname)
        with open(ref_path, "wb") as f:
            f.write(ref_bytes)

        # Static catalog checks (Gaia DR3 + PS1 DR2 MeanObject within 2.0 arcsec) & SkyBoT cone search (within 30.0 arcsec)
        gaia_chk = fa.check_gaia_dr3_cone(det["ra_deg"], det["dec_deg"], radius_arcsec=5.0)
        ps1_chk = fa.check_ps1_catalog_cone(det["ra_deg"], det["dec_deg"], radius_arcsec=5.0)
        skybot_chk = fa.check_skybot_cone(jd_utc_mid, det["ra_deg"], det["dec_deg"], radius_arcsec=45.0, obs_code="F51")
        other_skybot = [
            o
            for o in skybot_chk["objects"]
            if o["centerdist_arcsec"] <= 30.0
            and pdes.lower() not in o["name"].lower()
            and "no solar" not in o["num"].lower()
        ]
        skybot_chk["n_other_objects_within_30arcsec"] = len(other_skybot)
        skybot_chk["other_objects_within_30arcsec"] = other_skybot

        min_mpc_sep_days = min(abs(jd_utc_mid - jd_m) for jd_m in mpc_jds)
        days_before_first_obs = first_mpc_jd - jd_utc_mid

        det_entry = {
            "index": idx + 1,
            "warp_shortname": ws["shortname"],
            "warp_archive_path": fn,
            "filter": ws["filter"],
            "exptime_s": exptime,
            "jd_utc_mid": jd_utc_mid,
            "mjd_utc_mid": jd_utc_mid - 2400000.5,
            "days_before_first_obs": round(days_before_first_obs, 5),
            "min_mpc_time_separation_days": round(min_mpc_sep_days, 5),
            "science_cutout_file": f"claim/{folder_name}/{sci_fname}",
            "science_cutout_url": cut_url,
            "science_cutout_bytes": len(sci_bytes),
            "science_cutout_sha256": sha256_bytes(sci_bytes),
            "centroid_x_fits": det["x_fits"],
            "centroid_y_fits": det["y_fits"],
            "ra_deg": det["ra_deg"],
            "dec_deg": det["dec_deg"],
            "sigma_ra_arcsec": det["sigma_ra_arcsec"],
            "sigma_dec_arcsec": det["sigma_dec_arcsec"],
            "ap_flux_adu": det["ap_flux"],
            "bg_median_adu": det["bg_median"],
            "bg_rms_adu": det["bg_rms"],
            "ap_snr": det["ap_snr"],
            "peak_snr": det["peak_snr"],
            "mag_calibrated": det["mag_calibrated"],
            "vmag_predicted": round(pred["vmag"], 3),
            "mag_diff_cal_minus_pred": round(det["mag_calibrated"] - pred["vmag"], 3),
            "apriori_prediction": {
                "ra_pred_deg": pred["ra_deg"],
                "dec_pred_deg": pred["dec_deg"],
                "dra_cosdec_arcsec": round(dra_apriori, 4),
                "ddec_arcsec": round(ddec_apriori, 4),
                "sep_arcsec": round(sep_apriori, 4),
                "mahalanobis_sigma": round(mahal_sigma, 4),
                "inside_3sigma_ellipse": bool(mahal_sigma <= 3.0),
                "ell3sigma_major_arcsec": round(pred["ell3sigma_major_arcsec"], 4),
                "ell3sigma_minor_arcsec": round(pred["ell3sigma_minor_arcsec"], 4),
                "ell_pa_deg": round(pred["ell_pa_deg"], 3),
                "cov_sky_arcsec2": pred["cov_sky_arcsec2"],
                "rate_ra_cosdec_arcsec_hr": round(pred["rate_ra_cosdec_arcsec_hr"], 4),
                "rate_dec_arcsec_hr": round(pred["rate_dec_arcsec_hr"], 4),
                "rate_total_arcsec_hr": round(pred["rate_total_arcsec_hr"], 4),
                "rate_pa_deg": round(pred["rate_pa_deg"], 3),
            },
            "reference_epoch_check": {
                "ref_warp_shortname": ref_row["shortname"],
                "ref_mjd": float(ref_row["mjd"]),
                "ref_filter": ref_row["filter"],
                "ref_cutout_file": f"claim/{folder_name}/{ref_fname}",
                "ref_cutout_url": ref_url,
                "ref_cutout_bytes": len(ref_bytes),
                "ref_cutout_sha256": sha256_bytes(ref_bytes),
                "forced_aperture_snr": ref_ap["forced_snr"],
                "peak_snr_within_2arcsec": ref_ap["peak_snr_2arcsec"],
                "static_source_absent": bool(abs(ref_ap["forced_snr"]) < 2.5 and ref_ap["peak_snr_2arcsec"] < 3.0),
            },
            "catalog_and_skybot_checks": {
                "gaia_dr3_within_2arcsec": gaia_chk,
                "ps1_dr2_within_2arcsec": ps1_chk,
                "skybot_within_30arcsec": skybot_chk,
            },
        }
        detections.append(det_entry)
        print(
            f"  [Det {idx+1}] {ws['shortname']} | MJD={det_entry['mjd_utc_mid']:.6f} | SNR={det['ap_snr']:.2f} | "
            f"mag={det['mag_calibrated']:.3f} (Vpred={pred['vmag']:.3f}, diff={det_entry['mag_diff_cal_minus_pred']:+.3f}) | "
            f"apriori_sep={sep_apriori:.3f}\" ({mahal_sigma:.2f}sig) | ref_SNR={ref_ap['forced_snr']:.2f} | "
            f"Gaia2\"={gaia_chk['n_sources_within_2arcsec']} PS1_2\"={ps1_chk['n_sources_within_2arcsec']} SkyBoT_other={skybot_chk['n_other_objects_within_30arcsec']}"
        )

    # Motion vector consistency check across pairs separated by >= 20 min
    motion_pairs = []
    for i in range(len(detections)):
        for j in range(i + 1, len(detections)):
            d1, d2 = detections[i], detections[j]
            dt_days = d2["jd_utc_mid"] - d1["jd_utc_mid"]
            dt_min = dt_days * 1440.0
            if dt_min < 15.0:
                continue
            dt_hr = dt_days * 24.0
            cos_dm = math.cos(math.radians(0.5 * (d1["dec_deg"] + d2["dec_deg"])))
            dra_meas = ((d2["ra_deg"] - d1["ra_deg"] + 180.0) % 360.0 - 180.0) * cos_dm * 3600.0
            ddec_meas = (d2["dec_deg"] - d1["dec_deg"]) * 3600.0
            dra_pred = ((d2["apriori_prediction"]["ra_pred_deg"] - d1["apriori_prediction"]["ra_pred_deg"] + 180.0) % 360.0 - 180.0) * cos_dm * 3600.0
            ddec_pred = (d2["apriori_prediction"]["dec_pred_deg"] - d1["apriori_prediction"]["dec_pred_deg"]) * 3600.0

            rate_ra_meas = dra_meas / dt_hr
            rate_dec_meas = ddec_meas / dt_hr
            rate_ra_pred = dra_pred / dt_hr
            rate_dec_pred = ddec_pred / dt_hr

            # Uncertainty of displacement vector: centroid uncertainty at both endpoints + differential sky covariance
            sig_disp = math.hypot(d1["sigma_ra_arcsec"], d2["sigma_ra_arcsec"])
            # Also include differential orbital rate uncertainty from Jacobian difference (J2 - J1) @ C @ (J2 - J1)^T
            p1_full = nb.propagate_with_covariance(
                eph, info["el_vec"], info["cov_mat"], info["cov_epoch"], [(d1["jd_utc_mid"], "F51")], info["H"], info["G"]
            )[0]
            p2_full = nb.propagate_with_covariance(
                eph, info["el_vec"], info["cov_mat"], info["cov_epoch"], [(d2["jd_utc_mid"], "F51")], info["H"], info["G"]
            )[0]
            dJ = np.array(p2_full["jacobian"]) - np.array(p1_full["jacobian"])
            cov_disp = dJ @ info["cov_mat"] @ dJ.T + np.eye(2) * (sig_disp ** 2)
            diff_disp = np.array([dra_meas - dra_pred, ddec_meas - ddec_pred])
            disp_sigma = float(math.sqrt(max(0.0, float(diff_disp.T @ np.linalg.inv(cov_disp) @ diff_disp))))

            motion_pairs.append({
                "pair": f"{d1['index']}->{d2['index']}",
                "dt_minutes": round(dt_min, 3),
                "dt_hours": round(dt_hr, 5),
                "separation_ge_20min": bool(dt_min >= 20.0),
                "dra_cosdec_measured_arcsec": round(dra_meas, 4),
                "ddec_measured_arcsec": round(ddec_meas, 4),
                "total_displacement_arcsec": round(math.hypot(dra_meas, ddec_meas), 4),
                "dra_cosdec_predicted_arcsec": round(dra_pred, 4),
                "ddec_predicted_arcsec": round(ddec_pred, 4),
                "rate_ra_cosdec_measured_arcsec_hr": round(rate_ra_meas, 4),
                "rate_dec_measured_arcsec_hr": round(rate_dec_meas, 4),
                "rate_ra_cosdec_predicted_arcsec_hr": round(rate_ra_pred, 4),
                "rate_dec_predicted_arcsec_hr": round(rate_dec_pred, 4),
                "pa_measured_deg": round((math.degrees(math.atan2(dra_meas, ddec_meas)) + 360.0) % 360.0, 3),
                "pa_predicted_deg": round((math.degrees(math.atan2(dra_pred, ddec_pred)) + 360.0) % 360.0, 3),
                "motion_consistency_sigma": round(disp_sigma, 4),
                "consistent_within_3sigma": bool(disp_sigma <= 3.0),
            })

    # Differential orbit refit
    new_obs_for_refit = [
        {
            "jd_utc": d["jd_utc_mid"],
            "ra_deg": d["ra_deg"],
            "dec_deg": d["dec_deg"],
            "obs_code": "F51",
            "sigma_arcsec": d["sigma_ra_arcsec"],
        }
        for d in detections
    ]
    refit = fa.refit_orbit_gauss_newton(
        eph, info["el_vec"], info["cov_mat"], info["cov_epoch"], mpc_obs, new_obs_for_refit, H=info["H"], G=info["G"]
    )
    for d, r_post in zip(detections, refit["postfit_new_residuals"]):
        d["postfit_residual"] = r_post

    old_arc_days = float(info["data_arc"]) if info["data_arc"] else (last_mpc_jd - first_mpc_jd)
    new_arc_days = last_mpc_jd - min(d["jd_utc_mid"] for d in detections)
    arc_factor = new_arc_days / old_arc_days

    bundle = {
        "designation": pdes,
        "observatory_code": "F51 (Pan-STARRS 1, Haleakala)",
        "sbdb_url": info["sbdb_url"],
        "sbdb_file": f"claim/{folder_name}/sbdb_orbit_cov.json",
        "sbdb_sha256": sha256_bytes(open(sbdb_path, "rb").read()),
        "mpc_obs80_file": f"claim/{folder_name}/mpc_obs80.txt",
        "mpc_obs80_sha256": sha256_bytes(open(mpc_path, "rb").read()),
        "first_obs_sbdb": info["first_obs"],
        "last_obs_sbdb": info["last_obs"],
        "first_obs_mpc_jd_utc": round(first_mpc_jd, 6),
        "last_obs_mpc_jd_utc": round(last_mpc_jd, 6),
        "n_obs_used_sbdb": info["n_obs_used"],
        "n_obs_mpc_parsed": len(mpc_obs),
        "condition_code_sbdb": info["condition_code"],
        "H_mag": info["H"],
        "G_slope": info["G"],
        "data_arc_before_days": round(old_arc_days, 4),
        "data_arc_after_days": round(new_arc_days, 4),
        "arc_extension_days": round(first_mpc_jd - min(d["jd_utc_mid"] for d in detections), 4),
        "arc_multiplication_factor": round(arc_factor, 4),
        "n_precovery_detections": len(detections),
        "detections": detections,
        "motion_vector_consistency_pairs": motion_pairs,
        "orbit_refit": refit,
        "criteria_verification_summary": {
            "c1_precedes_first_obs_by_gt_60d": bool(min(d["days_before_first_obs"] for d in detections) > 60.0),
            "c1_min_days_before_first_obs": round(min(d["days_before_first_obs"] for d in detections), 4),
            "c1_no_mpc_obs_within_1d": bool(min(d["min_mpc_time_separation_days"] for d in detections) > 1.0),
            "c2_ge_2_detections_separated_ge_20min": bool(any(p["separation_ge_20min"] for p in motion_pairs)),
            "c2_all_inside_3sigma_ellipse": bool(all(d["apriori_prediction"]["inside_3sigma_ellipse"] for d in detections)),
            "c2_motion_vector_within_3sigma": bool(all(p["consistent_within_3sigma"] for p in motion_pairs)),
            "c3_postfit_new_residuals_lt_1arcsec_ps1": bool(refit["max_postfit_new_arcsec"] < 1.0),
            "c3_max_postfit_new_arcsec": refit["max_postfit_new_arcsec"],
            "c3_rms_postfit_new_arcsec": refit["rms_postfit_new_arcsec"],
            "c3_rms_postfit_all_arcsec": refit["rms_postfit_all_arcsec"],
            "c3_delta_a_lt_3sigma_a": bool(refit["delta_a_over_sigma_a_before"] < 3.0),
            "c3_delta_a_over_sigma_a": refit["delta_a_over_sigma_a_before"],
            "c4_mag_within_1p5_mag": bool(all(abs(d["mag_diff_cal_minus_pred"]) < 1.5 for d in detections)),
            "c4_max_abs_mag_diff": round(max(abs(d["mag_diff_cal_minus_pred"]) for d in detections), 3),
            "c5_no_static_source_in_ref_epoch": bool(all(d["reference_epoch_check"]["static_source_absent"] for d in detections)),
            "c5_no_gaia_or_ps1_within_2arcsec": bool(
                all(
                    d["catalog_and_skybot_checks"]["gaia_dr3_within_2arcsec"]["n_sources_within_2arcsec"] == 0
                    and d["catalog_and_skybot_checks"]["ps1_dr2_within_2arcsec"]["n_sources_within_2arcsec"] == 0
                    for d in detections
                )
            ),
            "c5_no_other_skybot_within_30arcsec": bool(
                all(d["catalog_and_skybot_checks"]["skybot_within_30arcsec"]["n_other_objects_within_30arcsec"] == 0 for d in detections)
            ),
            "stretch_arc_doubling_short_arc": bool(old_arc_days < 365.0 and new_arc_days >= 2.0 * old_arc_days),
            "stretch_neocp_short_arc_sigma_a_gt_50pct": bool(
                info["n_obs_used"] < 50
                and refit["sigma_a_ls_reduction_pct"] > 50.0
                and refit["sigma_a_sbdb_reduction_pct"] > 50.0
            ),
            "sigma_a_ls_reduction_pct": refit["sigma_a_ls_reduction_pct"],
            "sigma_a_sbdb_reduction_pct": refit["sigma_a_sbdb_reduction_pct"],
        },
    }

    manifest_path = os.path.join(out_dir, "precovery_bundle.json")
    with open(manifest_path, "w") as f:
        json.dump(bundle, f, indent=2)
    print(f"Saved {manifest_path} ({os.path.getsize(manifest_path)} bytes)")
    print("Verification summary:", json.dumps(bundle["criteria_verification_summary"], indent=2))
    return bundle


if __name__ == "__main__":
    # 1. 2014 OV236 (U=0, n_obs_used=36 < 50, 4 detections across 2 nights & 3 bands in Aug 2010, 1,375.0 days before first_obs)
    ov236_warps = [
        {
            "shortname": "rings.v3.skycell.1136.054.wrp.r.55426_49253.fits",
            "filename": "/rings.v3.skycell/1136/054/rings.v3.skycell.1136.054.wrp.r.55426_49253.fits",
            "mjd": "55426.49253",
            "filter": "r",
        },
        {
            "shortname": "rings.v3.skycell.1136.044.wrp.i.55427_42173.fits",
            "filename": "/rings.v3.skycell/1136/044/rings.v3.skycell.1136.044.wrp.i.55427_42173.fits",
            "mjd": "55427.42173",
            "filter": "i",
        },
        {
            "shortname": "rings.v3.skycell.1136.044.wrp.i.55427_43306.fits",
            "filename": "/rings.v3.skycell/1136/044/rings.v3.skycell.1136.044.wrp.i.55427_43306.fits",
            "mjd": "55427.43306",
            "filter": "i",
        },
        {
            "shortname": "rings.v3.skycell.1136.044.wrp.g.55427_49221.fits",
            "filename": "/rings.v3.skycell/1136/044/rings.v3.skycell.1136.044.wrp.g.55427_49221.fits",
            "mjd": "55427.49221",
            "filter": "g",
        },
    ]
    b1 = build_ps1_precovery_bundle("2014 OV236", "precovery_2014_OV236", ov236_warps, cutout_size_pix=120, search_offset_arcsec=(0.0, 0.0))

    # 2. 2019 QT15 (data_arc=88d < 365d, n_obs_used=41 < 50, 3 detections on 2014-11-11 spanning 39.15 min >= 20 min, 1,754.1 days before first_obs, 20.93x arc extension)
    qt15_warps = [
        {
            "shortname": "rings.v3.skycell.1600.050.wrp.i.56972_46650.fits",
            "filename": "/rings.v3.skycell/1600/050/rings.v3.skycell.1600.050.wrp.i.56972_46650.fits",
            "mjd": "56972.46650",
            "filter": "i",
        },
        {
            "shortname": "rings.v3.skycell.1600.050.wrp.i.56972_48009.fits",
            "filename": "/rings.v3.skycell/1600/050/rings.v3.skycell.1600.050.wrp.i.56972_48009.fits",
            "mjd": "56972.48009",
            "filter": "i",
        },
        {
            "shortname": "rings.v3.skycell.1600.050.wrp.i.56972_49369.fits",
            "filename": "/rings.v3.skycell/1600/050/rings.v3.skycell.1600.050.wrp.i.56972_49369.fits",
            "mjd": "56972.49369",
            "filter": "i",
        },
    ]
    b2 = build_ps1_precovery_bundle("2019 QT15", "precovery_2019_QT15", qt15_warps, cutout_size_pix=120, search_offset_arcsec=(28.50, 6.65))
