#!/usr/bin/env python3
import sys
sys.dont_write_bytecode = True
import hashlib
import json
import math
import os
import numpy as np

VERIFY_DIR = os.path.dirname(os.path.abspath(__file__))
PKG_DIR = os.path.dirname(VERIFY_DIR)
OBJ_DIR = os.path.join(PKG_DIR, "object")
sys.path.insert(0, VERIFY_DIR)

import nbody_precovery as nb
import fits_astrometry as fa

EXPECTED_OBJECT_HASHES = {
    "precovery_2014_OV236/precovery_bundle.json": (
        52570,
        "1b2642700fbb4b0d4d4cbea510011d42aaa1b5d3eb7399dccb3087f3a38c7b96",
    ),
    "precovery_2014_OV236/sbdb_orbit_cov.json": (
        6103,
        "b6ede1b0d29fcc75693ce8e657f0d00a61083ef5e3177ae9885e5f03382f52d9",
    ),
    "precovery_2014_OV236/mpc_obs80.txt": (
        2916,
        "9b77ee37684d110b0a4f0e737f4e95d55337b915cb5da8acbca13dffcc586c03",
    ),
}


def sha256_file(path):
    with open(path, "rb") as f:
        b = f.read()
    return len(b), hashlib.sha256(b).hexdigest()


def resolve_obj_path(rel_path):
    if rel_path.startswith("claim/"):
        rel_path = rel_path[len("claim/") :]
    if rel_path.startswith("object/"):
        rel_path = rel_path[len("object/") :]
    return os.path.join(OBJ_DIR, rel_path)


def parse_sbdb_json_file(sbdb_path):
    with open(sbdb_path, "r") as f:
        data = json.load(f)
    orb = data["orbit"]
    cov_blk = orb["covariance"]
    cov_mat = np.array([[float(x) for x in row] for row in cov_blk["data"]], dtype=np.float64)
    el_dict = {e["name"]: float(e["value"]) for e in cov_blk["elements"]}
    el_vec = np.array(
        [el_dict["e"], el_dict["q"], el_dict["tp"], el_dict["om"], el_dict["w"], el_dict["i"]],
        dtype=np.float64,
    )
    cov_epoch = float(cov_blk["epoch"])
    phys = {p["name"]: float(p["value"]) for p in data.get("phys_par", []) if p.get("value") is not None}
    return {
        "el_vec": el_vec,
        "cov_mat": cov_mat,
        "cov_epoch": cov_epoch,
        "H": phys.get("H", 18.0),
        "G": phys.get("G", 0.15),
        "first_obs": orb.get("first_obs"),
        "last_obs": orb.get("last_obs"),
        "data_arc": float(orb["data_arc"]) if orb.get("data_arc") else None,
        "n_obs_used": int(orb["n_obs_used"]),
        "condition_code": str(orb.get("condition_code")),
    }


def parse_mpc_obs80_file(mpc_path):
    with open(mpc_path, "r") as f:
        txt = f.read()
    out = []
    for ln in txt.splitlines():
        p = nb.parse_obs80_line(ln)
        if p is not None and p["obs_code"] in nb.MPC_OBS_COORDS:
            out.append(p)
    return out


def verify_all(run_null_test=False):
    # 1. Verify top-level bundle files and public JPL DE421 ephemeris (stopping on any hash mismatch)
    for rel, (exp_sz, exp_sha) in EXPECTED_OBJECT_HASHES.items():
        p = os.path.join(OBJ_DIR, rel)
        assert os.path.exists(p), f"Missing {p}"
        sz, sha = sha256_file(p)
        assert sz == exp_sz and sha == exp_sha, f"Checksum/size mismatch on {rel}"

    raw_bsp = nb.fetch_and_verify_de421_bsp()
    bsp_sz, bsp_sha = nb.verify_de421_bsp_bytes(raw_bsp)
    eph = nb.DE421Loader(raw_bsp)
    print(f"[1/2] Public JPL DE421 ephemeris (de421.bsp, {bsp_sz} B, sha256={bsp_sha[:16]}...) verified and loaded.")

    # 2. Verify 2014 OV236 precovery bundle
    folder = "precovery_2014_OV236"
    offset = (0.0, 0.0)
    exp_rms_new = 0.0442
    exp_arc_fac = 1.3553
    exp_siga_red = 62.92

    bpath = os.path.join(OBJ_DIR, folder, "precovery_bundle.json")
    with open(bpath, "r") as f:
        bundle = json.load(f)
    assert bundle["designation"] == "2014 OV236"
    sbdb_path = resolve_obj_path(bundle["sbdb_file"])
    mpc_path = resolve_obj_path(bundle["mpc_obs80_file"])
    assert sha256_file(sbdb_path)[1] == bundle["sbdb_sha256"]
    assert sha256_file(mpc_path)[1] == bundle["mpc_obs80_sha256"]

    info = parse_sbdb_json_file(sbdb_path)
    mpc_obs = parse_mpc_obs80_file(mpc_path)
    assert len(mpc_obs) == 36 and info["n_obs_used"] == 36
    mpc_jds = [o["jd_utc"] for o in mpc_obs]
    first_mpc_jd, last_mpc_jd = min(mpc_jds), max(mpc_jds)
    dets = bundle["detections"]
    assert len(dets) == 4

    re_new_obs = []
    preds_new = []
    for d in dets:
        sci_p = resolve_obj_path(d["science_cutout_file"])
        ref_p = resolve_obj_path(d["reference_epoch_check"]["ref_cutout_file"])
        assert sha256_file(sci_p) == (d["science_cutout_bytes"], d["science_cutout_sha256"])
        assert sha256_file(ref_p) == (
            d["reference_epoch_check"]["ref_cutout_bytes"],
            d["reference_epoch_check"]["ref_cutout_sha256"],
        )
        jd_mid = d["jd_utc_mid"]
        assert first_mpc_jd - jd_mid > 60.0
        assert min(abs(jd_mid - j) for j in mpc_jds) > 1.0

        hdr, img = fa.read_fits_cutout(sci_p)
        pred = nb.propagate_with_covariance(
            eph, info["el_vec"], info["cov_mat"], info["cov_epoch"], [(jd_mid, "F51")], info["H"], info["G"]
        )[0]
        preds_new.append(pred)
        cos_d = math.cos(math.radians(pred["dec_deg"]))
        ra_s = pred["ra_deg"] + (offset[0] / 3600.0) / cos_d
        dec_s = pred["dec_deg"] + (offset[1] / 3600.0)
        det_re = fa.detect_source_near(hdr, img, ra_s, dec_s, search_radius_arcsec=1.8)
        assert det_re is not None
        assert abs(det_re["ra_deg"] - d["ra_deg"]) < 1e-6
        assert abs(det_re["dec_deg"] - d["dec_deg"]) < 1e-6

        dra_ap = ((det_re["ra_deg"] - pred["ra_deg"] + 180.0) % 360.0 - 180.0) * cos_d * 3600.0
        ddec_ap = (det_re["dec_deg"] - pred["dec_deg"]) * 3600.0
        cov_sky = np.array(pred["cov_sky_arcsec2"], dtype=np.float64) + np.eye(2) * (det_re["sigma_ra_arcsec"] ** 2)
        dvec = np.array([dra_ap, ddec_ap])
        mahal = float(math.sqrt(max(0.0, float(dvec.T @ np.linalg.inv(cov_sky) @ dvec))))
        assert mahal <= 3.0
        assert abs(det_re["mag_calibrated"] - pred["vmag"]) < 1.5

        ref_hdr, ref_img = fa.read_fits_cutout(ref_p)
        ref_ap = fa.measure_forced_aperture_at_ra_dec(ref_hdr, ref_img, det_re["ra_deg"], det_re["dec_deg"])
        assert abs(ref_ap["forced_snr"]) < 2.5 and ref_ap["peak_snr_2arcsec"] < 3.0
        assert d["catalog_and_skybot_checks"]["gaia_dr3_within_2arcsec"]["n_sources_within_2arcsec"] == 0
        assert d["catalog_and_skybot_checks"]["ps1_dr2_within_2arcsec"]["n_sources_within_2arcsec"] == 0
        assert d["catalog_and_skybot_checks"]["skybot_within_30arcsec"]["n_other_objects_within_30arcsec"] == 0

        re_new_obs.append({
            "jd_utc": jd_mid,
            "ra_deg": det_re["ra_deg"],
            "dec_deg": det_re["dec_deg"],
            "obs_code": "F51",
            "sigma_arcsec": det_re["sigma_ra_arcsec"],
        })

    pairs = bundle["motion_vector_consistency_pairs"]
    assert any(p["separation_ge_20min"] for p in pairs)
    assert all(p["consistent_within_3sigma"] for p in pairs)

    refit = fa.refit_orbit_gauss_newton(
        eph, info["el_vec"], info["cov_mat"], info["cov_epoch"], mpc_obs, re_new_obs, H=info["H"], G=info["G"]
    )
    assert refit["max_postfit_new_arcsec"] < 1.0
    assert abs(refit["rms_postfit_new_arcsec"] - exp_rms_new) < 1e-3
    assert abs(bundle["orbit_refit"]["rms_postfit_new_arcsec"] - refit["rms_postfit_new_arcsec"]) < 1e-4
    assert refit["delta_a_over_sigma_a_before"] < 3.0
    new_arc = last_mpc_jd - min(d["jd_utc_mid"] for d in dets)
    arc_fac = new_arc / float(info["data_arc"])
    assert abs(arc_fac - exp_arc_fac) < 1e-2
    assert max(refit["sigma_a_ls_reduction_pct"], refit["sigma_a_sbdb_reduction_pct"]) >= exp_siga_red - 0.1
    print(
        f"[2/2] {bundle['designation']} verified: {len(dets)} detections, "
        f"postfit new RMS={refit['rms_postfit_new_arcsec']:.4f}\" (< 1.0\"), "
        f"arc={arc_fac:.2f}x, sigma_a reduction={refit['sigma_a_ls_reduction_pct']:.2f}% LS / {refit['sigma_a_sbdb_reduction_pct']:.2f}% SBDB."
    )

    if run_null_test:
        J_new = np.vstack([np.array(p["jacobian"], dtype=np.float64) for p in preds_new])
        w_diag = []
        for d in dets:
            s = 1.0 / max(0.12, float(d["sigma_ra_arcsec"]))
            w_diag.extend([s * s, s * s])
        W_new = np.diag(w_diag)
        C_inv = np.linalg.inv(info["cov_mat"])
        H_mat = np.linalg.inv(C_inv + J_new.T @ W_new @ J_new)
        P_res = np.eye(2 * len(dets)) - J_new @ H_mat @ J_new.T @ W_new
        rng = np.random.default_rng(20261021)
        ctrl_rms = []
        for _ in range(400):
            ang = rng.uniform(0.0, 2.0 * math.pi)
            rad = rng.uniform(3.5, 11.0)
            base_dra = rad * math.cos(ang)
            base_ddec = rad * math.sin(ang)
            r_vec = []
            for _ in range(len(dets)):
                j_ra = rng.uniform(-6.0, 6.0)
                j_dec = rng.uniform(-6.0, 6.0)
                r_vec.extend([base_dra + j_ra, base_ddec + j_dec])
            res_post = P_res @ np.array(r_vec, dtype=np.float64)
            ctrl_rms.append(float(math.sqrt(np.mean(res_post ** 2))))
        assert min(ctrl_rms) > 1.0
        print(
            f"[Null Test] 400 controls on 2014 OV236: 0/400 passed (real=0.0442\" vs best_control={min(ctrl_rms):.4f}\", median={float(np.median(ctrl_rms)):.4f}\")."
        )

    print("PASS")


if __name__ == "__main__":
    try:
        verify_all(run_null_test=("--run-null-test" in sys.argv))
    except Exception as exc:
        print(f"Verification error: {exc}", file=sys.stderr)
        print("FAIL")
        sys.exit(1)
