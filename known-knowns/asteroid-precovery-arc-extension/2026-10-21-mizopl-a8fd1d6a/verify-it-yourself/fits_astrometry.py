import math
import json
import urllib.request
import urllib.parse
import numpy as np


def read_fits_cutout(path_or_bytes):
    """Pure-Python FITS reader returning (header_dict, img_2d_float64)."""
    if isinstance(path_or_bytes, (bytes, bytearray)):
        raw = bytes(path_or_bytes)
    else:
        with open(path_or_bytes, "rb") as f:
            raw = f.read()

    hdr = {}
    offset = 0
    while True:
        block = raw[offset : offset + 2880]
        offset += 2880
        if not block:
            raise ValueError("Unexpected EOF while reading FITS header")
        end_found = False
        for i in range(0, 2880, 80):
            card = block[i : i + 80].decode("ascii", errors="replace")
            key = card[:8].strip()
            if key == "END":
                end_found = True
                break
            if card[8:10] == "= ":
                val_comment = card[10:]
            elif key == "HIERARCH" and "=" in card[9:]:
                eq_idx = card.index("=", 9)
                key = card[9:eq_idx].strip()
                val_comment = card[eq_idx + 1 :]
            else:
                continue
            # Split off comment outside quotes
            if val_comment.lstrip().startswith("'"):
                q1 = val_comment.find("'")
                q2 = val_comment.find("'", q1 + 1)
                val_str = val_comment[q1 + 1 : q2].strip() if q2 > q1 else val_comment.strip()
                hdr[key] = val_str
            else:
                val_str = val_comment.split("/")[0].strip()
                if val_str in ("T", "F"):
                    hdr[key] = (val_str == "T")
                else:
                    try:
                        if "." in val_str or "E" in val_str or "e" in val_str:
                            hdr[key] = float(val_str)
                        else:
                            hdr[key] = int(val_str)
                    except Exception:
                        hdr[key] = val_str
        if end_found:
            break

    naxis1 = int(hdr["NAXIS1"])
    naxis2 = int(hdr["NAXIS2"])
    bitpix = int(hdr["BITPIX"])
    npix = naxis1 * naxis2
    if bitpix == -32:
        dt = ">f4"
        nbytes = npix * 4
    elif bitpix == -64:
        dt = ">f8"
        nbytes = npix * 8
    elif bitpix == 16:
        dt = ">i2"
        nbytes = npix * 2
    elif bitpix == 32:
        dt = ">i4"
        nbytes = npix * 4
    else:
        raise ValueError(f"Unsupported BITPIX={bitpix}")

    img = np.frombuffer(raw[offset : offset + nbytes], dtype=dt).reshape((naxis2, naxis1)).astype(np.float64)
    bscale = float(hdr.get("BSCALE", 1.0))
    bzero = float(hdr.get("BZERO", 0.0))
    if bscale != 1.0 or bzero != 0.0:
        img = img * bscale + bzero
    return hdr, img


def wcs_pix2world(hdr, x_fits, y_fits):
    """
    Convert 1-indexed FITS pixel coordinates (x_fits, y_fits) to ICRS (ra_deg, dec_deg).
    Supports both ZTF RA---TPV / DEC--TPV distortion polynomials and standard TAN WCS.
    """
    u = float(x_fits) - float(hdr["CRPIX1"])
    v = float(y_fits) - float(hdr["CRPIX2"])
    if "CD1_1" in hdr:
        cd11 = float(hdr["CD1_1"])
        cd12 = float(hdr.get("CD1_2", 0.0))
        cd21 = float(hdr.get("CD2_1", 0.0))
        cd22 = float(hdr["CD2_2"])
    else:
        cdelt1 = float(hdr.get("CDELT1", 1.0))
        cdelt2 = float(hdr.get("CDELT2", 1.0))
        pc11 = float(hdr.get("PC1_1", hdr.get("PC001001", 1.0)))
        pc12 = float(hdr.get("PC1_2", hdr.get("PC001002", 0.0)))
        pc21 = float(hdr.get("PC2_1", hdr.get("PC002001", 0.0)))
        pc22 = float(hdr.get("PC2_2", hdr.get("PC002002", 1.0)))
        cd11, cd12 = cdelt1 * pc11, cdelt1 * pc12
        cd21, cd22 = cdelt2 * pc21, cdelt2 * pc22

    x = cd11 * u + cd12 * v
    y = cd21 * u + cd22 * v
    ctype1 = str(hdr.get("CTYPE1", "RA---TAN"))
    if "TPV" in ctype1 and "PV1_1" in hdr:
        r = math.hypot(x, y)
        def eval_pv(prefix, a, b):
            p = lambda k, default=0.0: float(hdr.get(f"{prefix}_{k}", default))
            val = (p(0, 0.0) + p(1, 1.0)*a + p(2, 0.0)*b + p(3, 0.0)*r +
                   p(4, 0.0)*a*a + p(5, 0.0)*a*b + p(6, 0.0)*b*b +
                   p(7, 0.0)*a*a*a + p(8, 0.0)*a*a*b + p(9, 0.0)*a*b*b + p(10, 0.0)*b*b*b)
            return val
        xi_deg = eval_pv("PV1", x, y)
        eta_deg = eval_pv("PV2", y, x)
    else:
        xi_deg = x
        eta_deg = y

    xi = math.radians(xi_deg)
    eta = math.radians(eta_deg)
    ra0 = math.radians(float(hdr["CRVAL1"]))
    dec0 = math.radians(float(hdr["CRVAL2"]))
    rho = math.hypot(xi, eta)
    if rho == 0.0:
        return math.degrees(ra0) % 360.0, math.degrees(dec0)
    c = math.atan(rho)
    cos_c, sin_c = math.cos(c), math.sin(c)
    sin_dec = cos_c * math.sin(dec0) + (eta * sin_c * math.cos(dec0)) / rho
    dec = math.asin(max(-1.0, min(1.0, sin_dec)))
    ra = ra0 + math.atan2(xi * sin_c, rho * math.cos(dec0) * cos_c - eta * math.sin(dec0) * sin_c)
    return math.degrees(ra) % 360.0, math.degrees(dec)


def wcs_world2pix(hdr, target_ra_deg, target_dec_deg):
    """Invert wcs_pix2world via 4-step Newton iteration starting at image center."""
    x = float(hdr["NAXIS1"]) / 2.0 + 0.5
    y = float(hdr["NAXIS2"]) / 2.0 + 0.5
    cos_d = math.cos(math.radians(target_dec_deg))
    for _ in range(6):
        ra0, dec0 = wcs_pix2world(hdr, x, y)
        dra = ((target_ra_deg - ra0 + 180.0) % 360.0 - 180.0) * cos_d
        ddec = target_dec_deg - dec0
        ra_x, dec_x = wcs_pix2world(hdr, x + 0.5, y)
        ra_y, dec_y = wcs_pix2world(hdr, x, y + 0.5)
        J11 = ((ra_x - ra0 + 180.0) % 360.0 - 180.0) * cos_d / 0.5
        J21 = (dec_x - dec0) / 0.5
        J12 = ((ra_y - ra0 + 180.0) % 360.0 - 180.0) * cos_d / 0.5
        J22 = (dec_y - dec0) / 0.5
        det = J11 * J22 - J12 * J21
        if abs(det) < 1e-18:
            break
        dx = (J22 * dra - J12 * ddec) / det
        dy = (-J21 * dra + J11 * ddec) / det
        x += dx
        y += dy
    return x, y


def detect_source_near(hdr, img, target_ra_deg, target_dec_deg, search_radius_arcsec=6.0, box_half_pix=2):
    """
    Measure background, find peak pixel within search_radius_arcsec of (target_ra_deg, target_dec_deg),
    compute iterative 2D flux-weighted centroid, aperture SNR, and calibrated magnitude.
    """
    H_im, W_im = img.shape
    x_pred, y_pred = wcs_world2pix(hdr, target_ra_deg, target_dec_deg)
    # Pixel scale (arcsec/pix)
    ra_c, dec_c = wcs_pix2world(hdr, W_im / 2.0, H_im / 2.0)
    ra_1, dec_1 = wcs_pix2world(hdr, W_im / 2.0 + 1.0, H_im / 2.0)
    pix_scale = math.hypot(((ra_1 - ra_c + 180.0) % 360.0 - 180.0) * math.cos(math.radians(dec_c)), dec_1 - dec_c) * 3600.0
    if pix_scale <= 0.0:
        pix_scale = 1.012

    # Sigma-clipped background outside 6 pixels of predicted location
    yy, xx = np.mgrid[0:H_im, 0:W_im]
    dist_pred = np.hypot((xx + 1.0) - x_pred, (yy + 1.0) - y_pred)
    bg_pix = img[(dist_pred > 6.0) & np.isfinite(img)]
    if len(bg_pix) < 20:
        bg_pix = img[np.isfinite(img)]
    med = float(np.median(bg_pix))
    mad = float(np.median(np.abs(bg_pix - med)))
    clip_pix = bg_pix[np.abs(bg_pix - med) < 3.5 * 1.4826 * max(mad, 1e-6)]
    if len(clip_pix) >= 20:
        med = float(np.median(clip_pix))
        rms = 1.4826 * float(np.median(np.abs(clip_pix - med)))
    else:
        rms = 1.4826 * mad
    rms = max(rms, 1e-6)

    sub = img - med
    search_r_pix = max(2.0, search_radius_arcsec / pix_scale)
    cand_mask = (dist_pred <= search_r_pix) & np.isfinite(sub)
    if not np.any(cand_mask):
        return None

    # Find highest 3x3 smoothed peak inside cand_mask
    best_val = -1e30
    best_iy, best_ix = int(round(y_pred - 1.0)), int(round(x_pred - 1.0))
    for iy, ix in np.argwhere(cand_mask):
        if 1 <= iy < H_im - 1 and 1 <= ix < W_im - 1:
            patch3 = sub[iy - 1 : iy + 2, ix - 1 : ix + 2]
            if np.all(np.isfinite(patch3)):
                val = float(np.sum(patch3))
                if val > best_val:
                    best_val = val
                    best_iy, best_ix = int(iy), int(ix)

    # 2-step positive flux-weighted centroid in (2*box_half_pix+1)x(2*box_half_pix+1) window
    r = box_half_pix
    iy0 = max(0, best_iy - r)
    iy1 = min(H_im, best_iy + r + 1)
    ix0 = max(0, best_ix - r)
    ix1 = min(W_im, best_ix + r + 1)
    patch = np.maximum(0.0, np.nan_to_num(sub[iy0:iy1, ix0:ix1], nan=0.0))
    flux_sum = float(np.sum(patch))
    if flux_sum <= 0.0:
        return None
    py, px = np.mgrid[iy0:iy1, ix0:ix1]
    xc_0 = float(np.sum(px * patch) / flux_sum) + 1.0
    yc_0 = float(np.sum(py * patch) / flux_sum) + 1.0

    # Gaussian-weighted refinement (sigma_g = 1.35 pix)
    gw = np.exp(-0.5 * (((px + 1.0 - xc_0) ** 2 + (py + 1.0 - yc_0) ** 2) / (1.35 ** 2)))
    wpatch = patch * gw
    wsum = float(np.sum(wpatch))
    if wsum > 0.0:
        xc_fits = float(np.sum((px + 1.0) * wpatch) / wsum)
        yc_fits = float(np.sum((py + 1.0) * wpatch) / wsum)
    else:
        xc_fits, yc_fits = xc_0, yc_0

    # Circular aperture flux (radius 2.5 pix) for SNR and photometry
    ap_mask = (np.hypot((xx + 1.0) - xc_fits, (yy + 1.0) - yc_fits) <= 2.5) & np.isfinite(sub)
    n_ap = int(np.sum(ap_mask))
    ap_flux = float(np.sum(sub[ap_mask]))
    ap_snr = ap_flux / (rms * math.sqrt(max(1, n_ap)))
    peak_snr = float(sub[best_iy, best_ix]) / rms

    ra_det, dec_det = wcs_pix2world(hdr, xc_fits, yc_fits)
    cos_d = math.cos(math.radians(target_dec_deg))
    dra_arcsec = ((ra_det - target_ra_deg + 180.0) % 360.0 - 180.0) * cos_d * 3600.0
    ddec_arcsec = (dec_det - target_dec_deg) * 3600.0
    sep_arcsec = math.hypot(dra_arcsec, ddec_arcsec)

    # Astrometric uncertainty (arcsec): photon noise + WCS floor (0.08")
    if "SEEING" in hdr:
        fwhm_arcsec = float(hdr.get("SEEING", 2.0)) * pix_scale
    elif "CHIP.SEEING" in hdr:
        fwhm_arcsec = float(hdr.get("CHIP.SEEING", 5.0)) * pix_scale
    else:
        fwhm_arcsec = 1.8
    sig_centroid = math.hypot(fwhm_arcsec / (2.355 * max(1.0, ap_snr)), 0.08)

    # Calibrated magnitude
    exptime = float(hdr.get("EXPOSURE", hdr.get("EXPTIME", 30.0)))
    magzp = hdr.get("MAGZP", None)
    if magzp is not None and ap_flux > 0:
        mag_inst = -2.5 * math.log10(ap_flux)
        # Apply nominal aperture correction (~0.15 mag from r=2.5 pix to total PSF)
        mag_cal = float(magzp) + mag_inst - 0.15
    elif "FPA.ZP" in hdr and ap_flux > 0:
        # PS1 GPC1 FPA.ZP is for 1 ADU/sec; measure r=4.5 pix total flux (or apply PSF aperture correction)
        ap45_mask = (np.hypot((xx + 1.0) - xc_fits, (yy + 1.0) - yc_fits) <= 4.5) & np.isfinite(sub)
        flux_tot = max(ap_flux, float(np.sum(sub[ap45_mask])))
        mag_cal = float(hdr["FPA.ZP"]) + 2.5 * math.log10(max(1.0, exptime)) - 2.5 * math.log10(flux_tot) - 0.12
    else:
        mag_cal = None

    # Exposure mid-time JD UTC
    if "OBSJD" in hdr:
        jd_mid = float(hdr["OBSJD"]) + 0.5 * exptime / 86400.0
    elif "MJD-OBS" in hdr:
        mjd_obs = float(hdr["MJD-OBS"])
        if str(hdr.get("TIMESYS", "")).strip().upper() == "TAI":
            # In PS1 GPC1 warps, MJD-OBS is TAI mid-exposure; convert TAI -> UTC
            leap_s = 34.0 if mjd_obs < 56109.0 else (35.0 if mjd_obs < 57204.0 else (36.0 if mjd_obs < 57754.0 else 37.0))
            jd_mid = (mjd_obs - leap_s / 86400.0) + 2400000.5
        else:
            jd_mid = mjd_obs + 2400000.5 + 0.5 * exptime / 86400.0
    else:
        jd_mid = None

    return {
        "x_fits": round(xc_fits, 4),
        "y_fits": round(yc_fits, 4),
        "x_pred_fits": round(x_pred, 4),
        "y_pred_fits": round(y_pred, 4),
        "ra_deg": round(ra_det, 7),
        "dec_deg": round(dec_det, 7),
        "sigma_ra_arcsec": round(sig_centroid, 4),
        "sigma_dec_arcsec": round(sig_centroid, 4),
        "ap_flux": round(ap_flux, 2),
        "bg_median": round(med, 3),
        "bg_rms": round(rms, 3),
        "ap_snr": round(ap_snr, 2),
        "peak_snr": round(peak_snr, 2),
        "mag_calibrated": round(mag_cal, 3) if mag_cal is not None else None,
        "dra_cosdec_arcsec": round(dra_arcsec, 4),
        "ddec_arcsec": round(ddec_arcsec, 4),
        "sep_arcsec": round(sep_arcsec, 4),
        "jd_utc_mid": jd_mid,
        "pix_scale_arcsec": round(pix_scale, 4),
        "filter": str(hdr.get("FILTER", hdr.get("FPA.FILTER", ""))),
    }


def measure_forced_aperture_at_ra_dec(hdr, img, ra_deg, dec_deg):
    """Measure forced circular aperture SNR at exact (ra_deg, dec_deg) in a reference epoch cutout."""
    H_im, W_im = img.shape
    x_t, y_t = wcs_world2pix(hdr, ra_deg, dec_deg)
    yy, xx = np.mgrid[0:H_im, 0:W_im]
    dist = np.hypot((xx + 1.0) - x_t, (yy + 1.0) - y_t)
    bg_pix = img[(dist > 6.0) & np.isfinite(img)]
    med = float(np.median(bg_pix))
    rms = max(1e-6, 1.4826 * float(np.median(np.abs(bg_pix - med))))
    sub = img - med
    ap_mask = (dist <= 2.2) & np.isfinite(sub)
    n_ap = int(np.sum(ap_mask))
    if n_ap == 0:
        return {"x_fits": round(x_t, 3), "y_fits": round(y_t, 3), "forced_snr": 0.0, "peak_snr_2arcsec": 0.0}
    ap_flux = float(np.sum(sub[ap_mask]))
    forced_snr = ap_flux / (rms * math.sqrt(n_ap))
    peak_snr = float(np.max(sub[ap_mask])) / rms
    return {
        "x_fits": round(x_t, 3),
        "y_fits": round(y_t, 3),
        "forced_snr": round(forced_snr, 2),
        "peak_snr_2arcsec": round(peak_snr, 2),
        "bg_median": round(med, 3),
        "bg_rms": round(rms, 3),
    }


def refit_orbit_gauss_newton(eph, el_init, cov_sbdb, epoch_tdb, mpc_obs_list, new_obs_list, H=18.0, G=0.15):
    """
    Perform weighted nonlinear Gauss-Newton differential orbit correction in 6D element space
    E = [e, q, tp, om_deg, w_deg, i_deg] at epoch_tdb.
    Computes:
      1. Before-precovery least-squares covariance C_ls_before (from MPC optical observations)
         and SBDB published covariance C_sbdb_before, with semi-major axis uncertainty sigma_a_before.
      2. After-precovery refit orbital elements E_refit, post-fit residuals at all MPC + new epochs,
         updated covariance C_ls_after and C_sbdb_after, and updated semi-major axis uncertainty sigma_a_after.
    """
    import nbody_precovery as nb

    all_obs = []
    for o in mpc_obs_list:
        all_obs.append({
            "jd_utc": float(o["jd_utc"]),
            "ra_deg": float(o["ra_deg"]),
            "dec_deg": float(o["dec_deg"]),
            "obs_code": str(o["obs_code"]),
            "sigma_arcsec": float(o.get("sigma_arcsec", 0.50)),
            "is_new": False,
        })
    for o in new_obs_list:
        all_obs.append({
            "jd_utc": float(o["jd_utc"]),
            "ra_deg": float(o["ra_deg"]),
            "dec_deg": float(o["dec_deg"]),
            "obs_code": str(o.get("obs_code", "I41")),
            "sigma_arcsec": float(o.get("sigma_arcsec", 0.35)),
            "is_new": True,
        })

    def eval_residuals_and_jacobian(el_vec, obs_subset):
        targets = [(o["jd_utc"], o["obs_code"]) for o in obs_subset]
        preds = nb.propagate_with_covariance(eph, el_vec, cov_sbdb, epoch_tdb, targets, H=H, G=G)
        N = len(obs_subset)
        r_vec = np.zeros(2 * N)
        J_mat = np.zeros((2 * N, 6))
        w_vec = np.zeros(2 * N)
        per_obs = []
        for idx, (o, p) in enumerate(zip(obs_subset, preds)):
            cos_d = math.cos(math.radians(p["dec_deg"]))
            dra = ((o["ra_deg"] - p["ra_deg"] + 180.0) % 360.0 - 180.0) * cos_d * 3600.0
            ddec = (o["dec_deg"] - p["dec_deg"]) * 3600.0
            r_vec[2 * idx] = dra
            r_vec[2 * idx + 1] = ddec
            J_mat[2 * idx : 2 * idx + 2, :] = np.array(p["jacobian"])
            w = 1.0 / (o["sigma_arcsec"] ** 2)
            w_vec[2 * idx] = w
            w_vec[2 * idx + 1] = w
            per_obs.append({
                "jd_utc": o["jd_utc"],
                "obs_code": o["obs_code"],
                "is_new": o["is_new"],
                "ra_obs_deg": o["ra_deg"],
                "dec_obs_deg": o["dec_deg"],
                "ra_pred_deg": p["ra_deg"],
                "dec_pred_deg": p["dec_deg"],
                "dra_cosdec_arcsec": round(dra, 4),
                "ddec_arcsec": round(ddec, 4),
                "sep_arcsec": round(math.hypot(dra, ddec), 4),
                "vmag_pred": round(p["vmag"], 3),
            })
        return r_vec, J_mat, w_vec, per_obs

    def sigma_a_from_cov(el_vec, C_mat):
        e, q = float(el_vec[0]), float(el_vec[1])
        a = q / (1.0 - e)
        grad_a = np.array([q / ((1.0 - e) ** 2), 1.0 / (1.0 - e), 0.0, 0.0, 0.0, 0.0])
        var_a = float(grad_a @ C_mat @ grad_a)
        return a, math.sqrt(max(0.0, var_a))

    # 1. Evaluate a-priori orbit on all observations
    r0_all, J0_all, w0_all, per_obs_apriori = eval_residuals_and_jacobian(el_init, all_obs)
    n_mpc = len(mpc_obs_list)
    r0_mpc = r0_all[: 2 * n_mpc]
    J0_mpc = J0_all[: 2 * n_mpc, :]
    w0_mpc = w0_all[: 2 * n_mpc]

    rms_apriori_mpc = math.sqrt(float(np.mean(r0_mpc ** 2)))
    rms_apriori_new = math.sqrt(float(np.mean(r0_all[2 * n_mpc :] ** 2)))

    # Normal matrix on MPC-only observations vs SBDB prior
    W_mpc = np.diag(w0_mpc)
    Info_mpc = J0_mpc.T @ W_mpc @ J0_mpc
    Info_sbdb = np.linalg.inv(cov_sbdb)
    a_before, sig_a_sbdb_before = sigma_a_from_cov(el_init, cov_sbdb)

    # Also compute pure observation-derived LS covariance before precovery (with faint Tikhonov damping if rank-near-deficient)
    dof_before = max(1, 2 * n_mpc - 6)
    s2_before = float(r0_mpc.T @ W_mpc @ r0_mpc) / dof_before
    C_ls_before = np.linalg.inv(Info_mpc + 1e-12 * Info_sbdb) * s2_before
    _, sig_a_ls_before = sigma_a_from_cov(el_init, C_ls_before)

    # 2. Gauss-Newton iterations on ALL (MPC + new precovery) observations
    el_cur = el_init.copy()
    for _ in range(3):
        r_all, J_all, w_all, per_obs_cur = eval_residuals_and_jacobian(el_cur, all_obs)
        W_all = np.diag(w_all)
        # Solve normal equations (J^T W J) dE = J^T W r
        H_norm = J_all.T @ W_all @ J_all + 1e-12 * Info_sbdb
        g_norm = J_all.T @ W_all @ r_all
        dE = np.linalg.solve(H_norm, g_norm)
        el_cur = el_cur + dE
        if float(np.linalg.norm(dE)) < 1e-10:
            break

    r_post, J_post, w_post, per_obs_post = eval_residuals_and_jacobian(el_cur, all_obs)
    W_post = np.diag(w_post)
    dof_after = max(1, 2 * len(all_obs) - 6)
    s2_after = float(r_post.T @ W_post @ r_post) / dof_after

    # Updated covariance under (A) SBDB information + new precovery Fisher information
    J_new = J_post[2 * n_mpc :, :]
    W_new = np.diag(w_post[2 * n_mpc :])
    C_sbdb_after = np.linalg.inv(Info_sbdb + J_new.T @ W_new @ J_new)
    a_after, sig_a_sbdb_after = sigma_a_from_cov(el_cur, C_sbdb_after)

    # Updated covariance under (B) full observation least-squares (MPC + new)
    C_ls_after = np.linalg.inv(J_post.T @ W_post @ J_post + 1e-12 * Info_sbdb) * s2_after
    _, sig_a_ls_after = sigma_a_from_cov(el_cur, C_ls_after)

    rms_post_all = math.sqrt(float(np.mean(r_post ** 2)))
    rms_post_mpc = math.sqrt(float(np.mean(r_post[: 2 * n_mpc] ** 2)))
    rms_post_new = math.sqrt(float(np.mean(r_post[2 * n_mpc :] ** 2)))
    max_post_new = float(max(o["sep_arcsec"] for o in per_obs_post[n_mpc:]))

    delta_a = abs(a_after - a_before)
    return {
        "epoch_tdb": epoch_tdb,
        "elements_before": [float(x) for x in el_init],
        "elements_after": [float(x) for x in el_cur],
        "a_au_before": a_before,
        "a_au_after": a_after,
        "delta_a_au": delta_a,
        "sigma_a_sbdb_before_au": sig_a_sbdb_before,
        "sigma_a_sbdb_after_au": sig_a_sbdb_after,
        "sigma_a_sbdb_reduction_pct": round(100.0 * (1.0 - sig_a_sbdb_after / sig_a_sbdb_before), 2),
        "sigma_a_ls_before_au": sig_a_ls_before,
        "sigma_a_ls_after_au": sig_a_ls_after,
        "sigma_a_ls_reduction_pct": round(100.0 * (1.0 - sig_a_ls_after / sig_a_ls_before), 2),
        "delta_a_over_sigma_a_before": round(delta_a / max(1e-15, sig_a_sbdb_before), 4),
        "cov_sbdb_before": cov_sbdb.tolist(),
        "cov_sbdb_after": C_sbdb_after.tolist(),
        "cov_ls_before": C_ls_before.tolist(),
        "cov_ls_after": C_ls_after.tolist(),
        "rms_apriori_mpc_arcsec": round(rms_apriori_mpc, 4),
        "rms_apriori_new_arcsec": round(rms_apriori_new, 4),
        "rms_postfit_all_arcsec": round(rms_post_all, 4),
        "rms_postfit_mpc_arcsec": round(rms_post_mpc, 4),
        "rms_postfit_new_arcsec": round(rms_post_new, 4),
        "max_postfit_new_arcsec": round(max_post_new, 4),
        "apriori_new_residuals": per_obs_apriori[n_mpc:],
        "postfit_new_residuals": per_obs_post[n_mpc:],
        "postfit_all_residuals": per_obs_post,
    }


def _http_get_text(url, timeout=20):
    import subprocess
    for attempt in range(3):
        try:
            out = subprocess.check_output(
                ["curl", "-4", "-sS", "-A", "V3R1T4S-research-agent", "--max-time", str(timeout), url],
                timeout=timeout + 5,
            )
            return out.decode("utf-8", errors="replace")
        except Exception:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-research-agent"})
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return r.read().decode("utf-8", errors="replace")
            except Exception:
                continue
    raise RuntimeError(f"HTTP GET failed after 3 attempts: {url}")


def _http_get_bytes(url, timeout=25):
    import subprocess
    for attempt in range(3):
        try:
            return subprocess.check_output(
                ["curl", "-4", "-sS", "-A", "V3R1T4S-research-agent", "--max-time", str(timeout), url],
                timeout=timeout + 5,
            )
        except Exception:
            try:
                req = urllib.request.Request(url, headers={"User-Agent": "V3R1T4S-research-agent"})
                with urllib.request.urlopen(req, timeout=timeout) as r:
                    return r.read()
            except Exception:
                continue
    raise RuntimeError(f"HTTP GET bytes failed after 3 attempts: {url}")


def check_gaia_dr3_cone(ra_deg, dec_deg, radius_arcsec=5.0):
    """Query CDS VizieR Gaia DR3 (I/355/gaiadr3) for any static sources within radius_arcsec."""
    c_str = f"{ra_deg:.7f}{dec_deg:+.7f}"
    url = (
        f"https://vizier.cds.unistra.fr/viz-bin/asu-tsv?-source=I/355/gaiadr3"
        f"&-c={urllib.parse.quote(c_str)}&-c.rs={radius_arcsec:.2f}&-out=Source,RA_ICRS,DE_ICRS,Gmag&-out.add=_r"
    )
    txt = _http_get_text(url, timeout=15)
    data_lines = [ln.strip() for ln in txt.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    sources = []
    # In VizieR asu-tsv, first 3 non-comment lines are header, units, dashed separator
    for ln in data_lines[3:]:
        parts = [p.strip() for p in ln.split("\t")]
        if len(parts) >= 5:
            try:
                sep = float(parts[0])
                sid = parts[1]
                s_ra = float(parts[2])
                s_dec = float(parts[3])
                gmag = float(parts[4]) if parts[4] else None
                sources.append({
                    "source_id": sid,
                    "ra": s_ra,
                    "dec": s_dec,
                    "phot_g_mean_mag": gmag,
                    "sep_arcsec": round(sep, 4),
                })
            except Exception:
                continue
    within_2arcsec = [s for s in sources if s["sep_arcsec"] <= 2.0]
    return {
        "query_url": url,
        "ra_deg": ra_deg,
        "dec_deg": dec_deg,
        "radius_arcsec": radius_arcsec,
        "n_sources_within_radius": len(sources),
        "n_sources_within_2arcsec": len(within_2arcsec),
        "sources": sources,
    }


def check_ps1_catalog_cone(ra_deg, dec_deg, radius_arcsec=5.0):
    """Query MAST Pan-STARRS DR2 MeanObject catalog for static sources within radius_arcsec."""
    rad_deg = radius_arcsec / 3600.0
    url = f"https://catalogs.mast.stsci.edu/api/v0.1/panstarrs/dr2/mean.json?ra={ra_deg:.7f}&dec={dec_deg:.7f}&radius={rad_deg:.6f}&nDetections.gt=2"
    data = json.loads(_http_get_text(url, timeout=20))
    rows = data.get("data", [])
    cos_d = math.cos(math.radians(dec_deg))
    sources = []
    for row in rows:
        s_ra = float(row.get("raMean", 0.0))
        s_dec = float(row.get("decMean", 0.0))
        sep = math.hypot(((s_ra - ra_deg + 180.0) % 360.0 - 180.0) * cos_d, s_dec - dec_deg) * 3600.0
        sources.append({
            "objID": row.get("objID"),
            "raMean": s_ra,
            "decMean": s_dec,
            "nDetections": row.get("nDetections"),
            "rMeanPSFMag": row.get("rMeanPSFMag"),
            "sep_arcsec": round(sep, 4),
        })
    sources.sort(key=lambda x: x["sep_arcsec"])
    within_2 = [s for s in sources if s["sep_arcsec"] <= 2.0]
    return {
        "query_url": url,
        "ra_deg": ra_deg,
        "dec_deg": dec_deg,
        "radius_arcsec": radius_arcsec,
        "n_sources_within_radius": len(sources),
        "n_sources_within_2arcsec": len(within_2),
        "sources": sources,
    }


def check_skybot_cone(jd_utc, ra_deg, dec_deg, radius_arcsec=30.0, obs_code="I41"):
    """Query IMCCE SkyBoT cone-search API at (jd_utc, ra_deg, dec_deg) to check for any known solar system object within 30 arcsec."""
    params = urllib.parse.urlencode({
        "-ep": f"{jd_utc:.6f}",
        "-ra": f"{ra_deg:.6f}",
        "-dec": f"{dec_deg:.6f}",
        "-rs": f"{radius_arcsec:.1f}",
        "-mime": "text",
        "-output": "object",
        "-loc": obs_code,
        "-from": "V3R1T4S",
    })
    url = f"https://ssp.imcce.fr/webservices/skybot/api/conesearch.php?{params}"
    raw_txt = _http_get_text(url, timeout=25)
    lines = [ln.strip() for ln in raw_txt.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    objects = []
    for ln in lines:
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) >= 8:
            try:
                err_arcsec = float(parts[6])
            except Exception:
                err_arcsec = 0.0
            try:
                sep = float(parts[7])
            except Exception:
                sep = 0.0
            objects.append({
                "num": parts[0],
                "name": parts[1],
                "ra_h": parts[2],
                "dec_d": parts[3],
                "class": parts[4],
                "vmag": parts[5],
                "err_arcsec": err_arcsec,
                "centerdist_arcsec": sep,
            })
    return {
        "query_url": url,
        "jd_utc": jd_utc,
        "ra_deg": ra_deg,
        "dec_deg": dec_deg,
        "radius_arcsec": radius_arcsec,
        "raw_response": raw_txt.strip(),
        "objects": objects,
    }
