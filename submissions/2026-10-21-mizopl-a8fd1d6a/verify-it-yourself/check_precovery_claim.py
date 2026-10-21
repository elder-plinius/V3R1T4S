#!/usr/bin/env python3
import os
import io
import sys
import json
import math
import hashlib
import numpy as np

VERIFY_DIR = os.path.dirname(os.path.abspath(__file__))
PKG_DIR = os.path.dirname(VERIFY_DIR)
OBJ_DIR = os.path.join(PKG_DIR, "object")
sys.path.insert(0, VERIFY_DIR)

import nbody_precovery as nb
import fits_astrometry as fa

EXPECTED_DE421_FULL = (1900024, "4ccc342138b7c5b552eb2f2a88cd5260b361c58741659d181e4a05e27838261c")

EXPECTED_OBJECT_HASHES = {
    "calibration_known_obs/calibration_12_known_obs_manifest.json": (14282, "5a0643819fd46e1a51a0f866fcd31f0232a51e8a2f92422d358592221e899f5b"),
    "precovery_2014_OV236/precovery_bundle.json": (52570, "1b2642700fbb4b0d4d4cbea510011d42aaa1b5d3eb7399dccb3087f3a38c7b96"),
    "precovery_2014_OV236/sbdb_orbit_cov.json": (6103, "b6ede1b0d29fcc75693ce8e657f0d00a61083ef5e3177ae9885e5f03382f52d9"),
    "precovery_2014_OV236/mpc_obs80.txt": (2916, "9b77ee37684d110b0a4f0e737f4e95d55337b915cb5da8acbca13dffcc586c03"),
    "precovery_2019_QT15/precovery_bundle.json": (45519, "a8fd1d6acaa5d05e238ca05078cff4fd0522908dabc12cbf6099eca35bfeca15"),
    "precovery_2019_QT15/sbdb_orbit_cov.json": (6069, "98c97fe6eabb7b58bbabfea79ca3cfc4ab3613411513307da8ad667143dfb1ba"),
    "precovery_2019_QT15/mpc_obs80.txt": (3321, "04f0bbaf3c8191c1d533ef8c7d50efa63f41e6d69d8c652fd41efbdbde797ff5"),
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


def verify_all():
    # 1. Verify top-level manifests and ephemeris
    for rel, (exp_sz, exp_sha) in EXPECTED_OBJECT_HASHES.items():
        p = os.path.join(OBJ_DIR, rel)
        assert os.path.exists(p), f"Missing {p}"
        sz, sha = sha256_file(p)
        assert sz == exp_sz and sha == exp_sha, f"Checksum/size mismatch on {rel}"

    full_npz_path = os.path.join(OBJ_DIR, "de421_2009_2027.npz")
    if os.path.exists(full_npz_path):
        with open(full_npz_path, "rb") as f:
            de421_bytes = f.read()
    else:
        p1 = os.path.join(OBJ_DIR, "de421_2009_2027.npz.part1")
        p2 = os.path.join(OBJ_DIR, "de421_2009_2027.npz.part2")
        assert os.path.exists(p1) and os.path.exists(p2), "Missing DE421 ephemeris parts"
        with open(p1, "rb") as f1, open(p2, "rb") as f2:
            de421_bytes = f1.read() + f2.read()
    assert len(de421_bytes) == EXPECTED_DE421_FULL[0], "DE421 byte length mismatch"
    assert hashlib.sha256(de421_bytes).hexdigest() == EXPECTED_DE421_FULL[1], "DE421 sha256 mismatch"
    eph = nb.DE421Loader(io.BytesIO(de421_bytes))

    # 2. Verify Calibration Gate (12 known minor planets)
    calib_manifest_path = os.path.join(OBJ_DIR, "calibration_known_obs", "calibration_12_known_obs_manifest.json")
    with open(calib_manifest_path, "r") as f:
        calib = json.load(f)
    entries = calib["entries"]
    assert len(entries) == 12
    seps = []
    for e in entries:
        fp = resolve_obj_path(e["fits_file"])
        sz, sha = sha256_file(fp)
        assert sz == e["fits_bytes"] and sha == e["fits_sha256"], f"FITS hash mismatch on {fp}"
        parsed_line = nb.parse_obs80_line(e["mpc_obs80_line"])
        assert parsed_line is not None
        hdr, img = fa.read_fits_cutout(fp)
        det = fa.detect_source_near(hdr, img, parsed_line["ra_deg"], parsed_line["dec_deg"], search_radius_arcsec=2.0)
        assert det is not None and det["sep_arcsec"] < 1.0 and det["ap_snr"] >= 5.5
        assert abs(det["sep_arcsec"] - e["astrometric_error_arcsec"]) < 1e-3
        seps.append(det["sep_arcsec"])
    print(f"[1/3] Calibration gate verified: 12/12 minor planets (< 1.0\", mean={np.mean(seps):.4f}\", max={max(seps):.4f}\").")

    # 3. Verify both precovery bundles (2019 QT15 and 2014 OV236)
    for idx_b, (folder, offset, exp_rms_new, exp_arc_fac, exp_siga_red) in enumerate([
        ("precovery_2019_QT15", (28.50, 6.65), 0.1176, 20.9296, 87.38),
        ("precovery_2014_OV236", (0.0, 0.0), 0.0442, 1.3553, 62.92),
    ], start=2):
        bpath = os.path.join(OBJ_DIR, folder, "precovery_bundle.json")
        with open(bpath, "r") as f:
            bundle = json.load(f)
        sbdb_path = resolve_obj_path(bundle["sbdb_file"])
        mpc_path = resolve_obj_path(bundle["mpc_obs80_file"])
        assert sha256_file(sbdb_path)[1] == bundle["sbdb_sha256"]
        assert sha256_file(mpc_path)[1] == bundle["mpc_obs80_sha256"]

        info = parse_sbdb_json_file(sbdb_path)
        mpc_obs = parse_mpc_obs80_file(mpc_path)
        mpc_jds = [o["jd_utc"] for o in mpc_obs]
        first_mpc_jd, last_mpc_jd = min(mpc_jds), max(mpc_jds)
        dets = bundle["detections"]
        assert len(dets) >= 2

        re_new_obs = []
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
        assert refit["delta_a_over_sigma_a_before"] < 3.0
        new_arc = last_mpc_jd - min(d["jd_utc_mid"] for d in dets)
        arc_fac = new_arc / float(info["data_arc"])
        assert abs(arc_fac - exp_arc_fac) < 1e-2
        assert max(refit["sigma_a_ls_reduction_pct"], refit["sigma_a_sbdb_reduction_pct"]) >= exp_siga_red - 0.1
        print(
            f"[{idx_b}/3] {bundle['designation']} verified: {len(dets)} detections, "
            f"postfit new RMS={refit['rms_postfit_new_arcsec']:.4f}\" (< 1.0\"), "
            f"arc={arc_fac:.2f}x, sigma_a reduction={refit['sigma_a_ls_reduction_pct']:.2f}% LS / {refit['sigma_a_sbdb_reduction_pct']:.2f}% SBDB."
        )

    print("PASS")


if __name__ == "__main__":
    try:
        verify_all()
    except Exception as exc:
        print(f"Verification error: {exc}", file=sys.stderr)
        print("FAIL")
        sys.exit(1)
