import os
import json
import math
import hashlib
import urllib.request
import urllib.parse
import sys

HERE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE_DIR)
import nbody_precovery as nb
import fits_astrometry as fa
import verify_ztf_precovery_bundle as vz

OUT_DIR = os.path.join(os.path.dirname(HERE_DIR), "object", "calibration_known_obs")
os.makedirs(OUT_DIR, exist_ok=True)


def get_calibration_candidates():
    """
    Return ZTF (I41) and Pan-STARRS 1 (F51 g/r/i/z) minor planets with known MPC observations.
    """
    return [
        ("2020 AV2", "I41"),
        ("2010 QW8", "F51"),
        ("2014 OJ66", "F51"),
        ("2012 RJ28", "F51"),
        ("2013 MV14", "F51"),
        ("2013 MO15", "F51"),
        ("2013 MG22", "F51"),
        ("2013 MB24", "F51"),
        ("2013 MV25", "F51"),
        ("2013 ME27", "F51"),
        ("2013 NG", "F51"),
        ("2014 VH21", "F51"),
        ("2014 VM30", "F51"),
    ]


def filter_mpc_obs_for_code(obs_list, obs_code):
    out = []
    for parsed in obs_list:
        if parsed["obs_code"] == obs_code and parsed["mag"] is not None:
            if obs_code == "I41" and 2458200.5 <= parsed["jd_utc"] <= 2460420.5 and parsed["mag"] <= 19.6:
                out.append(parsed)
            elif (
                obs_code == "F51"
                and parsed["band"] in ("g", "r", "i", "z", "y")
                and 2455348.5 <= parsed["jd_utc"] <= 2457050.5
                and parsed["mag"] <= 21.5
            ):
                out.append(parsed)
    return out


def find_ztf_cutout_for_obs(obs):
    jd, ra, dec = obs["jd_utc"], obs["ra_deg"], obs["dec_deg"]
    url = (
        f"https://irsa.ipac.caltech.edu/ibe/search/ztf/products/sci"
        f"?POS={ra:.5f},{dec:.5f}&WHERE=obsjd+BETWEEN+{jd-0.01:.5f}+AND+{jd+0.01:.5f}&ct=csv"
    )
    csv_txt = fa._http_get_text(url, timeout=20)
    lines = [l for l in csv_txt.splitlines() if l.strip()]
    if len(lines) < 2:
        return None
    headers = lines[0].split(",")
    best_row, best_dt = None, 999.0
    for ln in lines[1:]:
        row = dict(zip(headers, ln.split(",")))
        obsjd = float(row["obsjd"])
        exptime = float(row.get("exptime", 30.0))
        jd_mid = obsjd + 0.5 * exptime / 86400.0
        dt_sec = abs(jd_mid - jd) * 86400.0
        if dt_sec < best_dt:
            best_dt, best_row = dt_sec, row
    if best_row is None or best_dt > 25.0:
        return None
    fday = best_row["filefracday"]
    yyyy, mmdd, frac = fday[:4], fday[4:8], fday[8:]
    fc = best_row["filtercode"]
    field, ccdid, qid = int(best_row["field"]), int(best_row["ccdid"]), int(best_row["qid"])
    imgtype = best_row["imgtypecode"]
    rel_path = f"{yyyy}/{mmdd}/{frac}/ztf_{fday}_{field:06d}_{fc}_c{ccdid:02d}_{imgtype}_q{qid}_sciimg.fits"
    cut_url = f"https://irsa.ipac.caltech.edu/ibe/data/ztf/products/sci/{rel_path}?center={ra:.6f},{dec:.6f}&size=60arcsec&gzip=false"
    return cut_url, best_dt


def find_ps1_cutout_for_obs(obs):
    jd, ra, dec = obs["jd_utc"], obs["ra_deg"], obs["dec_deg"]
    mjd_target = jd - 2400000.5
    url = f"https://ps1images.stsci.edu/cgi-bin/ps1filenames.py?ra={ra:.6f}&dec={dec:.6f}&type=warp&sep=comma"
    txt = fa._http_get_text(url, timeout=20)
    lines = [l.strip() for l in txt.splitlines() if l.strip()]
    if len(lines) < 2:
        return None
    headers = [h.strip() for h in lines[0].split(",")]
    best_row, best_dt = None, 999.0
    for ln in lines[1:]:
        row = dict(zip(headers, [v.strip() for v in ln.split(",")]))
        mjd_obs = float(row["mjd"])
        dt_sec = abs((mjd_obs + 20.0 / 86400.0) - mjd_target) * 86400.0
        if dt_sec < best_dt:
            best_dt, best_row = dt_sec, row
    if best_row is None or best_dt > 45.0:
        return None
    fn = best_row["filename"]
    cut_url = f"https://ps1images.stsci.edu/cgi-bin/fitscut.cgi?red={fn}&ra={ra:.6f},{dec:.6f}&size=120&format=fits".replace(
        f"ra={ra:.6f},{dec:.6f}", f"ra={ra:.6f}&dec={dec:.6f}"
    )
    return cut_url, best_dt


def main():
    # Clean old calib_*.fits before writing sequential calib_01..calib_12
    for fn in os.listdir(OUT_DIR):
        if fn.startswith("calib_") and fn.endswith(".fits"):
            os.remove(os.path.join(OUT_DIR, fn))

    verified = []
    for desig, obs_code in get_calibration_candidates():
        if len(verified) >= 12:
            break
        try:
            _, all_obs = vz.fetch_mpc_obs(desig)
            obs_list = filter_mpc_obs_for_code(all_obs, obs_code)
        except Exception as e:
            print(f"[{desig}] MPC fetch error: {e}", flush=True)
            continue
        for obs in obs_list[:8]:
            try:
                found = find_ztf_cutout_for_obs(obs) if obs_code == "I41" else find_ps1_cutout_for_obs(obs)
                if not found:
                    continue
                cut_url, dt_sec = found
                fits_bytes = fa._http_get_bytes(cut_url, timeout=20)
                hdr, img = fa.read_fits_cutout(fits_bytes)
                det = fa.detect_source_near(hdr, img, obs["ra_deg"], obs["dec_deg"], search_radius_arcsec=2.0)
                if det and det["sep_arcsec"] < 0.80 and det["ap_snr"] >= 5.5:
                    slug = desig.replace(" ", "_")
                    fname = f"calib_{len(verified)+1:02d}_{slug}_{obs_code}.fits"
                    fpath = os.path.join(OUT_DIR, fname)
                    with open(fpath, "wb") as f:
                        f.write(fits_bytes)
                    sha = hashlib.sha256(fits_bytes).hexdigest()
                    entry = {
                        "index": len(verified) + 1,
                        "designation": desig,
                        "obs_code": obs_code,
                        "survey": "ZTF" if obs_code == "I41" else "PS1",
                        "fits_file": f"claim/calibration_known_obs/{fname}",
                        "fits_bytes": len(fits_bytes),
                        "fits_sha256": sha,
                        "cutout_url": cut_url,
                        "mpc_obs80_line": obs["raw_line"],
                        "mpc_jd_utc": obs["jd_utc"],
                        "fits_jd_utc_mid": det["jd_utc_mid"],
                        "dt_exposure_mid_sec": round(dt_sec, 3),
                        "mpc_ra_deg": round(obs["ra_deg"], 7),
                        "mpc_dec_deg": round(obs["dec_deg"], 7),
                        "mpc_mag": obs["mag"],
                        "mpc_band": obs["band"],
                        "detected_x_fits": det["x_fits"],
                        "detected_y_fits": det["y_fits"],
                        "detected_ra_deg": det["ra_deg"],
                        "detected_dec_deg": det["dec_deg"],
                        "dra_cosdec_arcsec": det["dra_cosdec_arcsec"],
                        "ddec_arcsec": det["ddec_arcsec"],
                        "astrometric_error_arcsec": det["sep_arcsec"],
                        "ap_snr": det["ap_snr"],
                        "peak_snr": det["peak_snr"],
                        "mag_calibrated": det["mag_calibrated"],
                    }
                    verified.append(entry)
                    print(
                        f"  [PASS #{len(verified):02d}] {desig:10s} ({obs_code}) | JD={obs['jd_utc']:.6f} | "
                        f"sep={det['sep_arcsec']:.3f}\" | SNR={det['ap_snr']:.1f} | mag={det['mag_calibrated']}",
                        flush=True,
                    )
                    break
            except Exception:
                continue

    manifest_path = os.path.join(OUT_DIR, "calibration_12_known_obs_manifest.json")
    summary = {
        "partial_win_id": "precovery-reproduce-known-obs",
        "n_objects_verified": len(verified),
        "max_astrometric_error_arcsec": max(x["astrometric_error_arcsec"] for x in verified) if verified else None,
        "mean_astrometric_error_arcsec": round(sum(x["astrometric_error_arcsec"] for x in verified) / len(verified), 4) if verified else None,
        "rms_astrometric_error_arcsec": round(math.sqrt(sum(x["astrometric_error_arcsec"] ** 2 for x in verified) / len(verified)), 4) if verified else None,
        "entries": verified,
    }
    with open(manifest_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Saved {len(verified)} verified known observations to {manifest_path}", flush=True)


if __name__ == "__main__":
    main()
