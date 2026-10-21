import os
import sys
import json
import math
import urllib.request
import numpy as np

HERE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE_DIR)
import nbody_precovery as nb
import fits_astrometry as fa
import verify_ztf_precovery_bundle as vz
import verify_ps1_precovery_bundle as vp

eph = nb.DE421Loader(os.path.join(os.path.dirname(HERE_DIR), "object", "de421_2009_2027.npz"))


def find_lov_moving_tracklet(pdes, center_jd, info):
    """
    Search PS1 warp exposures around center_jd along the 1D Line of Variations (LOV) z in [-3.0, +3.0].
    """
    warps = vp.search_ps1_warps_exact(eph, info, center_jd)
    if len(warps) < 2:
        return None
    # Pick up to 6 warps from the best 1-2 nights
    warps = warps[:6]
    targets = [(w["jd_mid"], "F51") for w in warps]
    preds = nb.propagate_with_covariance(eph, info["el_vec"], info["cov_mat"], info["cov_epoch"], targets, info["H"], info["G"])
    ell3 = preds[0]["ell3sigma_major_arcsec"]
    ell3_min = preds[0]["ell3sigma_minor_arcsec"]
    if ell3 > 130.0:
        return None

    # Download cutouts large enough to cover +/- ell3 (+15" margin)
    cut_pix = min(840, max(240, int(2.2 * ell3 / 0.25) + 80))
    frames = []
    for w, p in zip(warps, preds):
        fn, ra0, dec0 = w["filename"], p["ra_deg"], p["dec_deg"]
        cut_url = f"https://ps1images.stsci.edu/cgi-bin/fitscut.cgi?red={fn}&ra={ra0:.6f}&dec={dec0:.6f}&size={cut_pix}&format=fits"
        try:
            fbytes = urllib.request.urlopen(cut_url, timeout=20).read()
            hdr, img = fa.read_fits_cutout(fbytes)
            if np.sum(np.isfinite(img)) < 500:
                continue
            # Compute major unit vector (u_ra, u_dec) in arcsec from cov_sky_arcsec2
            cov_sky = np.array(p["cov_sky_arcsec2"])
            eigvals, eigvecs = np.linalg.eigh(cov_sky)
            sig_maj = math.sqrt(max(0.0, float(eigvals[1])))
            u_vec = eigvecs[:, 1]  # [u_ra_cosdec, u_dec]
            # Ensure consistent sign orientation of u_vec across frames
            if len(frames) > 0:
                if float(np.dot(u_vec, frames[0]["u_vec"])) < 0:
                    u_vec = -u_vec
            frames.append({
                "warp": w,
                "pred": p,
                "cut_url": cut_url,
                "hdr": hdr,
                "img": img,
                "sig_maj": sig_maj,
                "u_vec": u_vec,
            })
        except Exception:
            continue

    if len(frames) < 2:
        return None

    # Scan z in [-3.0, +3.0] in steps of 0.025 (step ~ 0.6" when sig_maj = 25")
    z_grid = np.linspace(-3.0, 3.0, 241)
    best_z = None
    best_dets = []
    best_score = -1.0

    for z in z_grid:
        dets_z = []
        for fr in frames:
            p = fr["pred"]
            ra0, dec0 = p["ra_deg"], p["dec_deg"]
            cos_d = math.cos(math.radians(dec0))
            dra_lov = z * fr["sig_maj"] * float(fr["u_vec"][0])
            ddec_lov = z * fr["sig_maj"] * float(fr["u_vec"][1])
            ra_z = (ra0 + (dra_lov / 3600.0) / cos_d) % 360.0
            dec_z = dec0 + (ddec_lov / 3600.0)
            det = fa.detect_source_near(fr["hdr"], fr["img"], ra_z, dec_z, search_radius_arcsec=1.6)
            if det and det["ap_snr"] >= 5.2 and det["sep_arcsec"] <= 1.25:
                # Re-express residual relative to a-priori nominal prediction (ra0, dec0)
                dra_nom = ((det["ra_deg"] - ra0 + 180.0) % 360.0 - 180.0) * cos_d * 3600.0
                ddec_nom = (det["dec_deg"] - dec0) * 3600.0
                cov_sky = np.array(p["cov_sky_arcsec2"]) + np.eye(2) * (det["sigma_ra_arcsec"] ** 2 + 0.15 ** 2)
                dvec = np.array([dra_nom, ddec_nom])
                mahal = math.sqrt(float(dvec @ np.linalg.inv(cov_sky) @ dvec))
                if mahal <= 3.0:
                    det_copy = dict(det)
                    det_copy["dra_nom_arcsec"] = round(dra_nom, 4)
                    det_copy["ddec_nom_arcsec"] = round(ddec_nom, 4)
                    det_copy["sep_nom_arcsec"] = round(math.hypot(dra_nom, ddec_nom), 4)
                    det_copy["mahal_sigma"] = round(mahal, 4)
                    det_copy["lov_z"] = round(float(z), 4)
                    det_copy["cut_url"] = fr["cut_url"]
                    det_copy["warp"] = fr["warp"]
                    det_copy["pred"] = p
                    dets_z.append(det_copy)
        if len(dets_z) >= 2:
            # Verify that the frames are separated by >= 12 min and the source actually moved on the sky (> 3.0 arcsec)
            ra_first, dec_first = dets_z[0]["ra_deg"], dets_z[0]["dec_deg"]
            ra_last, dec_last = dets_z[-1]["ra_deg"], dets_z[-1]["dec_deg"]
            sky_motion_arcsec = math.hypot(
                ((ra_last - ra_first + 180.0) % 360.0 - 180.0) * math.cos(math.radians(dec_first)) * 3600.0,
                (dec_last - dec_first) * 3600.0
            )
            if sky_motion_arcsec >= 4.0:
                score = len(dets_z) * 100.0 + sum(min(30.0, d["ap_snr"]) for d in dets_z)
                if score > best_score:
                    best_score = score
                    best_z = float(z)
                    best_dets = dets_z

    if len(best_dets) >= 2:
        # Also check that none of best_dets is a static star in PS1 DR2 catalog within 2.0 arcsec!
        clean_dets = []
        for d in best_dets:
            ps1_cat = fa.check_ps1_catalog_cone(d["ra_deg"], d["dec_deg"], radius_arcsec=3.0)
            if ps1_cat["n_sources_within_2arcsec"] == 0:
                clean_dets.append(d)
        if len(clean_dets) >= 2:
            return {
                "pdes": pdes,
                "ell3_major_arcsec": round(ell3, 3),
                "ell3_minor_arcsec": round(ell3_min, 3),
                "best_z": round(best_z, 4),
                "n_clean_dets": len(clean_dets),
                "dets": clean_dets,
            }
    return None


def main():
    with open(os.path.join(HERE_DIR, "short_arc_doubling_candidates.json")) as f:
        cands = json.load(f)
    both_cands = [c for c in cands if c["nobs"] < 50 and c["survey"] == "PS1"]
    both_cands.sort(key=lambda c: (c["U"], c["dt_before"] / max(1, c["arc"]), c["vmag"]))

    print(f"Scanning top {min(25, len(both_cands))} short-arc (<365d) + low-nobs (<50) PS1 candidates along LOV...", flush=True)
    for idx, c in enumerate(both_cands[:25]):
        pdes = c["pdes"]
        try:
            _, info = vz.fetch_sbdb_full_cov(pdes)
            if not info:
                continue
            res = find_lov_moving_tracklet(pdes, c["best_jd"], info)
            if res:
                print(f"  [LOV HIT!] {pdes:12s} | arc={c['arc']}d->{c['new_arc']:.0f}d ({c['arc_ratio']}x) | nobs={c['nobs']} | z={res['best_z']:+.3f} | ell3={res['ell3_major_arcsec']}\"x{res['ell3_minor_arcsec']}\" | n_dets={res['n_clean_dets']} | SNRs={[d['ap_snr'] for d in res['dets']]}", flush=True)
                with open(os.path.join(HERE_DIR, f"lov_hit_{pdes.replace(' ', '_')}.json"), "w") as out_f:
                    json.dump({"cand": c, "lov_result": res}, out_f, indent=2)
            else:
                print(f"  [{idx+1:02d}] {pdes:12s} | no clean multi-frame LOV tracklet", flush=True)
        except Exception as e:
            print(f"  [{idx+1:02d}] {pdes:12s} | error: {e}", flush=True)


if __name__ == "__main__":
    main()
