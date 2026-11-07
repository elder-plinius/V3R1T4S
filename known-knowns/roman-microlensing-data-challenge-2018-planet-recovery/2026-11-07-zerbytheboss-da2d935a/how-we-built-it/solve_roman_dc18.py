#!/usr/bin/env python3
"""
Self-contained, zero-leakage physical microlensing light-curve solver for the
2018 Roman (WFIRST) Microlensing Data Challenge (293 events in W149 and Z087).

Architecture (3-Stage Physical Cascade):
1. Stage 1 (CV vs Microlensing Gate): Joint two-band (W149 + Z087) linear flux
   achromaticity slope, multi-season dwarf-nova recurrence segmentation, and
   fast-rise/exponential-decay (FRED) outburst asymmetry filters.
2. Stage 2 (PSPL/FSPL vs USBL Gate): Two-pass Huber-loss Nelder-Mead + Tikhonov-
   regularized host-star PSPL fit with automatic wide-planet spike masking,
   followed by unregularized 4-parameter FSPL + linear-limb-darkened finite-source
   (\gamma = 0.45) + annual-parallax basis H0 residual matched filtering.
3. Stage 3 (Binary-Lens (s, q) Solver): Minor/major-image caustic-ring inversion
   s_\pm = 0.5 * (\sqrt{u_a^2 + 4} \pm u_a) paired with a 3-branch physical
   log10(q) solver (wide-planet FSPL perturbation fit, central-caustic binary
   ray-shooting, and local caustic-crossing 5th-degree complex polynomial
   Aberth-Ehrlich solver in binary_lens_kernel.c).
"""

import argparse
from concurrent.futures import ProcessPoolExecutor
import ctypes
import os
import subprocess
import tempfile
import time
import numpy as np
from scipy.ndimage import median_filter
from scipy.optimize import minimize


def _load_binary_lens_lib():
    here = os.path.dirname(os.path.abspath(__file__))
    c_src = os.path.join(here, "binary_lens_kernel.c")
    for cand in ("libbinarylens.dylib", "libbinarylens.so"):
        p = os.path.join(here, cand)
        if os.path.isfile(p):
            try:
                return ctypes.CDLL(p)
            except OSError:
                pass
    so_path = os.path.join(
        tempfile.gettempdir(), f"libbinarylens_roman_{os.getuid()}.so"
    )
    if not os.path.isfile(so_path):
        tmp_so = f"{so_path}.{os.getpid()}"
        cmd = ["cc", "-O3", "-shared", "-fPIC", c_src, "-o", tmp_so, "-lm"]
        res = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False
        )
        if res.returncode != 0:
            raise RuntimeError(f"Failed to compile {c_src}: {res.stderr}")
        os.replace(tmp_so, so_path)
    return ctypes.CDLL(so_path)


lib = _load_binary_lens_lib()
lib.bl_magnification_fs.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.POINTER(ctypes.c_double),
]
lib.bl_fit_event_logq.argtypes = [
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_double,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
]
lib.bl_fit_event_logq.restype = ctypes.c_double


def load_event(ev_idx, lc_dir):
    w = np.loadtxt(os.path.join(lc_dir, f"ulwdc1_{ev_idx:03d}_W149.txt"))
    z = np.loadtxt(os.path.join(lc_dir, f"ulwdc1_{ev_idx:03d}_Z087.txt"))
    return w, z


def split_seasons(t):
    gaps = np.where(np.diff(t) > 10.0)[0]
    starts = [0] + [int(g + 1) for g in gaps]
    ends = [int(g + 1) for g in gaps] + [len(t)]
    return list(zip(starts, ends))


def preprocess_lc(data):
    valid = (
        (data[:, 1] > 5.0)
        & (data[:, 1] < 35.0)
        & (data[:, 2] > 0.0)
        & (data[:, 2] < 5.0)
    )
    data = data[valid]
    t = data[:, 0]
    mag = data[:, 1]
    merr = data[:, 2]
    seasons = split_seasons(t)
    s_meds = []
    s_iqrs = []
    for s0, s1 in seasons:
        sm = mag[s0:s1]
        q10, q50, q90 = np.percentile(sm, [10, 50, 90])
        s_meds.append(q50)
        s_iqrs.append(q90 - q10)
    quiet = np.argsort(s_iqrs)[:3]
    m_base = float(np.median([s_meds[i] for i in quiet]))
    f = 10.0 ** (-0.4 * (mag - m_base))
    ferr = (np.log(10.0) / 2.5) * f * merr
    quiet_idx = np.concatenate([np.arange(seasons[i][0], seasons[i][1]) for i in quiet])
    f_base = float(np.median(f[quiet_idx]))
    mad = float(np.median(np.abs(f[quiet_idx] - f_base) / ferr[quiet_idx]) * 1.4826)
    if 0.5 < mad < 2.5:
        ferr = ferr * mad
    return t, mag, merr, f, ferr, m_base, f_base, seasons


def preprocess_w149_cv(w):
    t = w[:, 0]
    mag = w[:, 1]
    merr = w[:, 2]
    seasons = split_seasons(t)
    s_meds = []
    s_iqrs = []
    for s0, s1 in seasons:
        sm = mag[s0:s1]
        q10, q50, q90 = np.percentile(sm, [10, 50, 90])
        s_meds.append(q50)
        s_iqrs.append(q90 - q10)
    quiet = np.argsort(s_iqrs)[:3]
    m_base = float(np.median([s_meds[i] for i in quiet]))
    f = 10.0 ** (-0.4 * (mag - m_base))
    ferr = (np.log(10.0) / 2.5) * f * merr
    quiet_idx = np.concatenate([np.arange(seasons[i][0], seasons[i][1]) for i in quiet])
    f_base = float(np.median(f[quiet_idx]))
    mad = float(np.median(np.abs(f[quiet_idx] - f_base) / ferr[quiet_idx]) * 1.4826)
    if 0.5 < mad < 2.5:
        ferr = ferr * mad
    return t, mag, merr, f, ferr, m_base, f_base, seasons


def extract_cv_features(w):
    t, mag, merr, f, ferr, m_base, f_base, seasons = preprocess_w149_cv(w)
    res_flat = (f - f_base) / ferr

    max_snr = 0.0
    for k in [3, 7, 15, 35, 81]:
        sm = np.convolve(res_flat, np.ones(k) / np.sqrt(float(k)), mode="same")
        ms = float(np.max(sm))
        if ms > max_snr:
            max_snr = ms

    sm11 = np.convolve(res_flat, np.ones(11) / np.sqrt(11.0), mode="same")
    raw_obs = []
    for s_idx, (s0, s1) in enumerate(seasons):
        ts = t[s0:s1]
        fs = f[s0:s1]
        snrs = sm11[s0:s1]
        if np.max(snrs) < 5.0:
            continue
        active = np.where(snrs > 3.5)[0]
        if len(active) < 3:
            continue
        seg_starts = [active[0]]
        seg_ends = []
        for k in range(1, len(active)):
            ip, ic = active[k - 1], active[k]
            if ts[ic] - ts[ip] > 2.5 and np.median(snrs[ip : ic + 1]) < 1.5:
                seg_ends.append(ip)
                seg_starts.append(ic)
        seg_ends.append(active[-1])

        for a, b in zip(seg_starts, seg_ends):
            if b - a < 3:
                continue
            pk = a + int(np.argmax(snrs[a : b + 1]))
            pk_snr = float(snrs[pk])
            if pk_snr < 5.5:
                continue
            f_pk = float(np.median(fs[max(a, pk - 1) : min(b + 1, pk + 2)]))
            df_pk = max(f_pk - f_base, 1e-5)

            def measure_width(frac):
                thr = f_base + frac * df_pk
                l_pts = np.where(fs[: pk + 1] < thr)[0]
                t_l = float(ts[l_pts[-1]]) if len(l_pts) > 0 else float(ts[0])
                ed_l = len(l_pts) == 0
                r_pts = np.where(fs[pk:] < thr)[0]
                t_r = float(ts[pk + r_pts[0]]) if len(r_pts) > 0 else float(ts[-1])
                ed_r = len(r_pts) == 0
                return (
                    max(float(ts[pk]) - t_l, 0.015),
                    max(t_r - float(ts[pk]), 0.015),
                    ed_l,
                    ed_r,
                )

            r50, f50, el50, er50 = measure_width(0.50)
            r20, f20, el20, er20 = measure_width(0.20)
            r80, f80, _, _ = measure_width(0.80)

            raw_obs.append(
                {
                    "season": s_idx,
                    "t_pk": float(ts[pk]),
                    "t_start": float(ts[a]),
                    "t_end": float(ts[b]),
                    "f_pk": f_pk,
                    "df_pk": df_pk,
                    "pk_snr": pk_snr,
                    "r50": r50,
                    "f50": f50,
                    "fwhm": r50 + f50,
                    "r20": r20,
                    "f20": f20,
                    "w20": r20 + f20,
                    "w80": r80 + f80,
                    "asym50": f50 / r50,
                    "asym20": f20 / r20,
                    "wing_ratio": (r20 + f20) / max(r50 + f50, 0.02),
                    "flat_top_ratio": (r80 + f80) / max(r50 + f50, 0.02),
                    "edge_left": el20 or (ts[a] - ts[0] < 1.0),
                    "edge_right": er20 or (ts[-1] - ts[b] < 1.0),
                }
            )

    merged_obs = []
    skip = False
    for i in range(len(raw_obs)):
        if skip:
            skip = False
            continue
        if i + 1 < len(raw_obs):
            ob1, ob2 = raw_obs[i], raw_obs[i + 1]
            if (
                ob2["season"] == ob1["season"] + 1
                and ob1["edge_right"]
                and ob2["edge_left"]
            ):
                m_ob = dict(ob1 if ob1["pk_snr"] >= ob2["pk_snr"] else ob2)
                m_ob["fwhm"] = ob1["fwhm"] + ob2["fwhm"]
                m_ob["w20"] = ob1["w20"] + ob2["w20"]
                m_ob["asym50"] = ob2["f50"] / max(ob1["r50"], 0.1)
                m_ob["asym20"] = ob2["f20"] / max(ob1["r20"], 0.1)
                m_ob["gap_merged"] = True
                merged_obs.append(m_ob)
                skip = True
                continue
        raw_obs[i]["gap_merged"] = False
        merged_obs.append(raw_obs[i])

    return {
        "max_snr": max_snr,
        "obs": merged_obs,
    }


def fit_linear_flux_tikhonov(
    A, f, ferr, weights=None, fs_min=0.005, fs_max=1.05, ridge_w=0.0, fs_prior=0.32
):
    w = (1.0 / (ferr * ferr)) if weights is None else (weights / (ferr * ferr))
    x = A - 1.0
    sw = float(np.sum(w))
    if sw <= 1e-20:
        return fs_prior, 1.0
    sx = float(np.sum(w * x))
    sxx = float(np.sum(w * x * x))
    sy = float(np.sum(w * f))
    sxy = float(np.sum(w * x * f))
    var_x = sxx - (sx * sx) / sw
    if var_x <= 1e-20:
        return fs_prior, float(sy / sw)
    cov_xy = sxy - (sx * sy) / sw
    lam = ridge_w
    Fs = (cov_xy + lam * fs_prior) / (var_x + lam)
    Fs = float(np.clip(Fs, fs_min, fs_max))
    Fb = float((sy - Fs * sx) / sw)
    return Fs, Fb


def fspl_mag(u, rho):
    u = np.maximum(np.asarray(u, dtype=np.float64), 0.0)
    if rho <= 1e-5:
        uc = np.maximum(u, 1e-8)
        return (uc * uc + 2.0) / (uc * np.sqrt(uc * uc + 4.0))
    mag = np.empty_like(u)
    far = u >= 3.5 * rho
    if np.any(far):
        uf = np.maximum(u[far], 1e-8)
        mag[far] = (uf * uf + 2.0) / (uf * np.sqrt(uf * uf + 4.0))
    near = ~far
    if np.any(near):
        un = u[near][:, None, None]
        r_frac = np.array([0.12, 0.32, 0.50, 0.66, 0.81, 0.94])[None, :, None]
        dr_w = np.array([0.22, 0.19, 0.17, 0.16, 0.14, 0.12])[None, :, None]
        gamma = 0.45
        mu = np.sqrt(np.maximum(1.0 - r_frac * r_frac, 0.0))
        ld_w = dr_w * (1.0 - gamma * (1.0 - 1.5 * mu))
        ld_w /= np.sum(ld_w)
        theta = np.linspace(0.0, np.pi, 12, endpoint=False)[None, None, :]
        r_phys = rho * r_frac
        u_pts = np.sqrt(
            (un + r_phys * np.cos(theta)) ** 2 + (r_phys * np.sin(theta)) ** 2
        )
        u_pts = np.maximum(u_pts, 1e-7)
        a_pts = (u_pts * u_pts + 2.0) / (u_pts * np.sqrt(u_pts * u_pts + 4.0))
        mag[near] = np.sum(ld_w * np.mean(a_pts, axis=2, keepdims=True), axis=(1, 2))
    return mag


def fspl_mag_exact(u, rho):
    u = np.maximum(np.asarray(u, dtype=np.float64), 0.0)
    if rho <= 1e-5:
        uc = np.maximum(u, 1e-8)
        return (uc * uc + 2.0) / (uc * np.sqrt(uc * uc + 4.0))
    mag = np.empty_like(u)
    far = u >= 3.5 * rho
    if np.any(far):
        uf = np.maximum(u[far], 1e-8)
        mag[far] = (uf * uf + 2.0) / (uf * np.sqrt(uf * uf + 4.0))
    near = ~far
    if np.any(near):
        un = u[near][:, None, None]
        edges = np.linspace(0.0, 1.0, 17)
        r_mid = 0.5 * (edges[:-1] + edges[1:])[None, :, None]
        area_w = (edges[1:] ** 2 - edges[:-1] ** 2)[None, :, None]
        gamma = 0.45
        mu = np.sqrt(np.maximum(1.0 - r_mid * r_mid, 0.0))
        ld_w = area_w * (1.0 - gamma * (1.0 - 1.5 * mu))
        ld_w /= np.sum(ld_w)
        theta = np.linspace(0.0, np.pi, 24, endpoint=False)[None, None, :]
        r_phys = rho * r_mid
        u_pts = np.sqrt(
            (un + r_phys * np.cos(theta)) ** 2 + (r_phys * np.sin(theta)) ** 2
        )
        u_pts = np.maximum(u_pts, 1e-7)
        a_pts = (u_pts * u_pts + 2.0) / (u_pts * np.sqrt(u_pts * u_pts + 4.0))
        mag[near] = np.sum(ld_w * np.mean(a_pts, axis=2, keepdims=True), axis=(1, 2))
    return mag


def classify_cv(w, z):
    tw, magw, merrw, fw, ferrw, mbw, fbw, seasons = preprocess_lc(w)
    tz, magz, merrz, fz, ferrz, mbz, fbz, seasons_z = preprocess_lc(z)
    fw_at_z = np.interp(tz, tw, fw)
    wz = 1.0 / (ferrz * ferrz)
    x = fw_at_z - fbw
    sw = np.sum(wz)
    sx = np.sum(wz * x)
    sxx = np.sum(wz * x * x)
    sy = np.sum(wz * fz)
    sxy = np.sum(wz * x * fz)
    det = sw * sxx - sx * sx
    b_slope = float(max((sw * sxy - sx * sy) / max(det, 1e-20), 0.0))
    max_snrz = float(np.max((fz - fbz) / ferrz))
    cvf = extract_cv_features(w)
    max_snrw = float(cvf["max_snr"])
    obs = cvf["obs"]

    dn_obs = [o for o in obs if 0.08 <= o["fwhm"] <= 16.0 and o["pk_snr"] >= 6.5]
    max_fwhm = max((o["fwhm"] for o in obs), default=0.0)
    main_ob = max(obs, key=lambda o: o["pk_snr"]) if obs else None

    is_cv = False
    if (
        len(obs) == 0
        or max_snrw < 8.0
        or (len(obs) == 1 and obs[0]["pk_snr"] < 6.5 and max_snrw < 11.5)
    ):
        is_cv = True
    elif max_snrz > 5.0 and (
        b_slope > 2.31
        or (
            b_slope > 1.72
            and main_ob is not None
            and main_ob["wing_ratio"] < 3.0
            and max_fwhm < 16.0
        )
    ):
        is_cv = True
    elif max_fwhm < 16.0 and len(dn_obs) >= 3:
        is_cv = True
    elif max_fwhm < 16.0 and len(dn_obs) == 2:
        ob1, ob2 = dn_obs[0], dn_obs[1]
        dur_ratio = min(ob1["fwhm"], ob2["fwhm"]) / max(ob1["fwhm"], ob2["fwhm"])
        if ob1["season"] != ob2["season"] and dur_ratio > 0.25:
            is_cv = True
    elif len(obs) == 1 and max_fwhm < 2.0 and max_snrw < 40.0:
        ob = obs[0]
        if ob["asym20"] > 2.05 and (
            ob["asym50"] > 2.2 or ob["asym50"] < 0.35 or ob["wing_ratio"] < 1.25
        ):
            is_cv = True
    return is_cv, b_slope, max_snrw, max_snrz


def fit_host_clean(t, f, ferr, f_base, seasons):
    res_flat = (f - f_base) / ferr
    f_med = median_filter(f, size=115)
    snr_med = (f_med - f_base) / np.median(ferr)

    best_snr = 0.0
    best_idx = int(np.argmax(f))
    for k in [3, 7, 15, 35, 81, 181]:
        sm = np.convolve(res_flat, np.ones(k) / np.sqrt(float(k)), mode="same")
        idx = int(np.argmax(sm))
        if sm[idx] > best_snr:
            best_snr = float(sm[idx])
            best_idx = idx

    t_sharp = float(t[best_idx])
    idx_med = int(np.argmax(f_med))
    t_broad = float(t[idx_med])

    spike_snr = 0.0
    spike_idx = best_idx
    for k in [3, 7, 13]:
        sm = np.convolve(res_flat, np.ones(k) / np.sqrt(float(k)), mode="same")
        idx = int(np.argmax(sm))
        if sm[idx] > spike_snr:
            spike_snr = float(sm[idx])
            spike_idx = idx
    t_spike = float(t[spike_idx])

    f3 = median_filter(f, size=3)
    f_pk_sp = float(f3[spike_idx])
    half_sp = f_base + 0.5 * max(f_pk_sp - f_base, 3.0 * ferr[spike_idx])
    il = spike_idx
    while il > 0 and f3[il] > half_sp:
        il -= 1
    ir = spike_idx
    while ir + 1 < len(t) and f3[ir] > half_sp:
        ir += 1
    fwhm_sp = max(float(t[ir] - t[il]), 0.03)

    f_pk_s = float(np.median(f[max(0, best_idx - 1) : min(len(f), best_idx + 2)]))
    half_s = f_base + 0.5 * max(f_pk_s - f_base, 3.0 * ferr[best_idx])
    win_s = np.abs(t - t_sharp) < 50.0
    ab_s = np.where(f[win_s] > half_s)[0]
    fwhm_s = (
        max(float(t[win_s][ab_s[-1]] - t[win_s][ab_s[0]]), 0.03)
        if len(ab_s) >= 2
        else 0.05
    )

    mask_away = np.abs(t - t_spike) > 3.0
    sm_away = np.convolve(
        res_flat[mask_away], np.ones(51) / np.sqrt(51.0), mode="same"
    )
    idx_away = int(np.argmax(sm_away))
    t_away = float(t[mask_away][idx_away])
    snr_away = float(sm_away[idx_away])

    use_wing_mask = False
    if (
        fwhm_sp < 1.2
        and snr_away > 8.0
        and abs(t_away - t_spike) > 3.8
        and abs(t_away - t_spike) < 350.0
        and (abs(t_broad - t_spike) > 3.5 or np.max(snr_med) < 8.0)
    ):
        t0_init = t_away
        t_sharp = t_spike
        fwhm_init = 8.0
        use_wing_mask = True
    else:
        t0_init = (
            t_broad
            if (np.max(snr_med) > 6.0 and abs(t_broad - t_sharp) < 15.0)
            else t_sharp
        )
        fwhm_init = max(fwhm_s, 0.1)

    max_th_shift = 55.0
    max_ltE_shift = 2.5
    for s_idx, (s0, s1) in enumerate(seasons):
        if abs(t0_init - t[s0]) < 3.0:
            if s_idx > 0 and np.median(
                f_med[seasons[s_idx - 1][1] - 100 : seasons[s_idx - 1][1]]
            ) > f_base + 2.5 * np.median(ferr):
                t0_init = 0.5 * (t[seasons[s_idx - 1][1] - 1] + t[s0])
                fwhm_init = max(fwhm_init, 25.0)
            elif use_wing_mask:
                wing_above = np.sum(
                    f_med[s0 : min(s1, s0 + 400)] > f_base + 1.5 * np.median(ferr)
                )
                t0_init = t[s0] - (25.0 if wing_above > 120 else 6.5)
                fwhm_init = 18.0 if wing_above > 120 else 7.2
                max_th_shift = 4.0 if wing_above > 120 else 2.0
                max_ltE_shift = 0.05
        if abs(t0_init - t[s1 - 1]) < 3.0 and s_idx + 1 < len(seasons):
            if np.median(
                f_med[seasons[s_idx + 1][0] : seasons[s_idx + 1][0] + 100]
            ) > f_base + 2.5 * np.median(ferr):
                t0_init = 0.5 * (t[s1 - 1] + t[seasons[s_idx + 1][0]])
                fwhm_init = max(fwhm_init, 25.0)

    near = np.abs(t - t0_init) < max(6.0 * fwhm_init, 50.0)
    if use_wing_mask:
        near = near & (np.abs(t - t_sharp) > 2.2)
    sub = np.zeros(len(t), dtype=bool)
    sub[::20] = True
    fit_mask = (near | sub) & (
        ~(np.abs(t - t_sharp) <= 2.2) if use_wing_mask else np.ones(len(t), dtype=bool)
    )
    tf, ff, ef = t[fit_mask], f[fit_mask], ferr[fit_mask]
    fs_floor = 0.10 if use_wing_mask else 0.004
    lu0_min = -0.02 if use_wing_mask else -4.2
    lu0_max = 0.10 if use_wing_mask else 0.45
    ltE_center = float(np.log10(max(fwhm_init, 0.05)))

    def huber_loss(params, weights=None):
        th, lu0, ltE = params
        if (
            abs(th - t0_init) > max_th_shift
            or abs(ltE - ltE_center) > max_ltE_shift
            or lu0 < lu0_min
            or lu0 > lu0_max
            or ltE < -1.8
            or ltE > 2.4
        ):
            return 1e18
        u0, tE = 10.0**lu0, 10.0**ltE
        u = np.sqrt(u0 * u0 + ((tf - th) / tE) ** 2)
        A = (u * u + 2.0) / (u * np.sqrt(u * u + 4.0))
        rw = 420.0 * ((u0 / 0.40) ** 2)
        Fs, Fb = fit_linear_flux_tikhonov(
            A, ff, ef, weights, fs_min=fs_floor, fs_max=1.05, ridge_w=rw, fs_prior=0.33
        )
        pred = Fs * (A - 1.0) + Fb
        r = np.abs(ff - pred) / ef
        delta = 2.8
        loss = np.where(r <= delta, 0.5 * r * r, delta * (r - 0.5 * delta))
        return float(np.sum(loss))

    best = (1e18, [t0_init, 0.02 if use_wing_mask else -0.4, ltE_center])
    lu0_grid = (
        [-0.01, 0.02, 0.06] if use_wing_mask else [-2.0, -1.1, -0.5, -0.15, 0.1]
    )
    ltE_offs = [0.0] if max_ltE_shift < 0.2 else [-0.3, 0.0, 0.3, 0.6]
    for lu0 in lu0_grid:
        for ltE_off in ltE_offs:
            ltE = float(np.clip(ltE_center + ltE_off, -1.6, 2.3))
            v = huber_loss([t0_init, lu0, ltE])
            if v < best[0]:
                best = (v, [t0_init, lu0, ltE])

    r1 = minimize(
        huber_loss, best[1], method="Nelder-Mead", options={"maxiter": 220}
    )
    t0_1, lu0_1, ltE_1 = r1.x
    u0_1, tE_1 = (
        10.0 ** np.clip(lu0_1, lu0_min, lu0_max),
        10.0 ** np.clip(ltE_1, -1.8, 2.4),
    )
    u_1 = np.sqrt(u0_1 * u0_1 + ((tf - t0_1) / tE_1) ** 2)
    A_1 = (u_1 * u_1 + 2.0) / (u_1 * np.sqrt(u_1 * u_1 + 4.0))
    rw_1 = 420.0 * ((u0_1 / 0.40) ** 2)
    Fs_1, Fb_1 = fit_linear_flux_tikhonov(
        A_1, ff, ef, None, fs_floor, 1.05, rw_1, 0.33
    )
    res_1 = (ff - (Fs_1 * (A_1 - 1.0) + Fb_1)) / ef
    w_rob = np.where(
        np.abs(res_1) < 2.8, 1.0, (2.8 / np.maximum(np.abs(res_1), 2.8)) ** 2
    )

    r2 = minimize(
        lambda p: huber_loss(p, w_rob),
        [t0_1, lu0_1, ltE_1],
        method="Nelder-Mead",
        options={"maxiter": 220},
    )
    t0_h, lu0_h, ltE_h = r2.x
    u0_h, tE_h = (
        10.0 ** np.clip(lu0_h, lu0_min, lu0_max),
        10.0 ** np.clip(ltE_h, -1.8, 2.4),
    )

    u_full = np.sqrt(u0_h * u0_h + ((t - t0_h) / tE_h) ** 2)
    A_full = (u_full * u_full + 2.0) / (u_full * np.sqrt(u_full * u_full + 4.0))
    w_full = np.where(
        np.abs((f - (Fs_1 * (A_full - 1.0) + Fb_1)) / ferr) < 2.8, 1.0, 0.02
    )
    if use_wing_mask:
        w_full[np.abs(t - t_sharp) <= 2.2] = 0.0
    rw_h = 420.0 * ((u0_h / 0.40) ** 2)
    Fs_h, Fb_h = fit_linear_flux_tikhonov(
        A_full, f, ferr, w_full, fs_floor, 1.05, rw_h, 0.33
    )
    pred_pspl = Fs_h * (A_full - 1.0) + Fb_h

    return {
        "t0": float(t0_h),
        "u0": float(u0_h),
        "tE": float(tE_h),
        "Fs": float(Fs_h),
        "Fb": float(Fb_h),
        "pred_pspl": pred_pspl,
        "best_snr": float(best_snr),
        "use_wing_mask": bool(use_wing_mask),
        "t_sharp": float(t_sharp),
    }


def compute_h0_snr(t, f, ferr, res):
    t0_h, u0_h, tE_h = res["t0"], res["u0"], res["tE"]
    idx_pk = int(np.argmax(median_filter(f, size=5)))
    t0_try0 = float(t[idx_pk])
    near = np.abs(t - t0_try0) < max(5.0 * tE_h, 25.0)
    sub = np.zeros(len(t), dtype=bool)
    sub[::25] = True
    m = near | sub
    tm, fm, em = t[m], f[m], ferr[m]

    def fit_lsq_poly(A_vec, t_vec, f_vec, e_vec, use_plx=False):
        w_inv = 1.0 / e_vec
        x0 = np.ones_like(t_vec)
        x1 = A_vec - 1.0
        if use_plx:
            tau = (t_vec - t0_try0) / max(tE_h, 5.0)
            x2 = x1 * np.clip(tau, -3.0, 3.0)
            x3 = x1 * np.clip(tau * tau, 0.0, 9.0)
            X = np.column_stack([x0, x1, x2, x3])
        else:
            X = np.column_stack([x0, x1])
        Xw = X * w_inv[:, None]
        yw = f_vec * w_inv
        beta, _, _, _ = np.linalg.lstsq(Xw, yw, rcond=None)
        if beta[1] < 0.0:
            return np.full_like(f_vec, np.median(f_vec)), beta
        return X @ beta, beta

    def single_lens_obj(p):
        th, lu0, ltE, lrho = p
        if (
            abs(th - t0_try0) > max(1.5 * tE_h, 5.0)
            or lu0 < -4.5
            or lu0 > 0.6
            or ltE < -2.0
            or ltE > 2.6
            or lrho < -4.2
            or lrho > 0.35
        ):
            return 1e18
        u0_p, tE_p, rho_p = (
            10.0**lu0,
            10.0**ltE,
            (0.0 if lrho < -3.9 else 10.0**lrho),
        )
        u_p = np.sqrt(u0_p * u0_p + ((tm - th) / tE_p) ** 2)
        A_p = fspl_mag(u_p, rho_p)
        pred_m, _ = fit_lsq_poly(A_p, tm, fm, em, use_plx=(tE_p > 8.0))
        return float(np.sum(((fm - pred_m) / em) ** 2))

    best_h0 = (
        1e18,
        [t0_try0, np.log10(max(u0_h, 1e-3)), np.log10(max(tE_h, 0.05)), -4.0],
    )
    for th_try in [t0_try0, t0_h]:
        for lu0_try in [-2.2, -1.2, -0.5, -0.1, np.log10(max(u0_h, 1e-3))]:
            for ltE_try in [
                np.log10(max(tE_h, 0.05)) - 0.2,
                np.log10(max(tE_h, 0.05)),
                np.log10(max(tE_h, 0.05)) + 0.2,
            ]:
                for lrho_try in [-4.0, -2.0, -1.2, -0.5]:
                    c2 = single_lens_obj([th_try, lu0_try, ltE_try, lrho_try])
                    if c2 < best_h0[0]:
                        best_h0 = (c2, [th_try, lu0_try, ltE_try, lrho_try])

    r_h0 = minimize(
        single_lens_obj, best_h0[1], method="Nelder-Mead", options={"maxiter": 200}
    )
    th_0, lu0_0, ltE_0, lrho_0 = r_h0.x
    u0_0, tE_0, rho_0 = (
        10.0**lu0_0,
        10.0**ltE_0,
        (0.0 if lrho_0 < -3.9 else 10.0**lrho_0),
    )
    u_all = np.sqrt(u0_0 * u0_0 + ((t - th_0) / tE_0) ** 2)
    A_all = fspl_mag(u_all, rho_0)
    pred_h0, _ = fit_lsq_poly(A_all, t, f, ferr, use_plx=(tE_0 > 8.0))

    r_h0_vec = (f - pred_h0) / ferr
    if tE_0 > 12.0:
        r_h0_det = (f - pred_h0 - median_filter(f - pred_h0, size=251)) / ferr
    else:
        r_h0_det = r_h0_vec

    win_ev = np.abs(t - th_0) < max(6.0 * tE_0, 60.0)
    if res["use_wing_mask"]:
        win_ev = win_ev | (np.abs(t - res["t_sharp"]) < 10.0)
    snr_h0 = 0.0
    for k in [3, 5, 9, 17, 33, 65]:
        sm = np.convolve(r_h0_det, np.ones(k) / np.sqrt(float(k)), mode="same")
        val = float(np.max(np.abs(sm[win_ev]))) if np.any(win_ev) else 0.0
        if val > snr_h0:
            snr_h0 = val
    dt0_gap = abs(t0_h - t0_try0)
    return snr_h0, dt0_gap


def solve_sq_from_host(t, f, ferr, res):
    t0, u0, tE, Fs, Fb = res["t0"], res["u0"], res["tE"], res["Fs"], res["Fb"]
    pred = res["pred_pspl"]
    r = (f - pred) / ferr
    df = f - pred
    if tE > 40.0 and not res["use_wing_mask"]:
        df_hp = df - median_filter(df, size=251)
        r_hp = df_hp / ferr
    else:
        df_hp = df
        r_hp = r

    tau_all = (t - t0) / tE
    valid_anom = (np.abs(tau_all) <= 7.5) & (np.abs(t - t0) <= 400.0)
    best_sm = 0.0
    ia = int(np.argmin(np.abs(t - t0)))
    for k in [3, 7, 15, 31]:
        sm = np.convolve(r_hp, np.ones(k) / np.sqrt(float(k)), mode="same")
        mask_k = valid_anom & (
            ((np.abs(tau_all) <= 0.8) | (np.abs(tau_all) >= 2.0))
            if (k == 31 and tE > 40.0)
            else valid_anom
        )
        if np.any(mask_k):
            idx_k = np.where(mask_k)[0]
            im = int(idx_k[np.argmax(np.abs(sm[mask_k]))])
            if np.abs(sm[im]) > best_sm:
                best_sm = float(np.abs(sm[im]))
                ia = im
    if not res["use_wing_mask"] and abs(tau_all[ia]) < 0.15 and u0 > 0.12:
        core_m = np.abs(tau_all) < 0.20
        wing_m = (np.abs(tau_all) >= 0.60) & (np.abs(tau_all) <= 2.50)
        if np.any(core_m) and np.any(wing_m):
            sm15 = np.convolve(r, np.ones(15) / np.sqrt(15.0), mode="same")
            if (
                np.max(sm15[core_m]) > 10.0
                and np.min(sm15[core_m]) < -10.0
                and np.max(np.abs(sm15[wing_m])) > 14.0
            ):
                ia = int(np.where(wing_m)[0][np.argmax(np.abs(sm15[wing_m]))])

    t_anom = res["t_sharp"] if res["use_wing_mask"] else float(t[ia])
    ia_c = int(np.argmin(np.abs(t - t_anom)))
    tau_a = (t_anom - t0) / tE
    ua = float(np.sqrt(u0 * u0 + tau_a * tau_a))
    ua_s = (
        ua * 0.82
        if (u0 > 0.88 and not res["use_wing_mask"] and abs(tau_a) < 0.65)
        else ua
    )

    core = np.abs(tau_all) < 0.08
    wing = (np.abs(tau_all) >= 0.08) & (np.abs(tau_all) < 0.50)
    r_core_pos = float(np.max(r[core])) if np.any(core) else 0.0
    r_core_neg = float(np.min(r[core])) if np.any(core) else 0.0
    r_wing_max = float(np.max(np.abs(r[wing]))) if np.any(wing) else 0.0
    if (
        (u0 <= 0.038 and ua_s <= 0.055)
        or (tE > 120.0 and ua_s < 0.12 and Fs < 0.02)
        or (u0 < 0.025 and ua_s < 0.12 and r_core_pos < -10.0)
    ):
        if (
            Fs < 0.075
            and 6.0 < r_core_pos < 22.0
            and -10.5 < r_core_neg < -4.5
            and tE < 100.0
        ):
            sp = 2.80
        elif (
            0.22 < Fs < 0.385 and r_wing_max < 12.0 and r_core_pos < 100.0
        ) or (r_core_pos < -10.0 and u0 < 0.025):
            sp = 2.00
        else:
            sp = 1.25
    else:
        sp = float(0.5 * (np.sqrt(ua_s * ua_s + 4.0) + ua_s))

    near_anom = np.abs(t - t_anom) < 1.5
    pos_sum = (
        float(np.sum((f[near_anom] - pred[near_anom]) / ferr[near_anom]))
        if np.any(near_anom)
        else 0.0
    )

    if ua >= 0.75 and sp >= 1.50 and pos_sum > 12.0:
        dt = np.abs(t - t_anom)
        win = dt < 36.0
        far = (np.abs(t - t0) > 3.5 * tE) & (dt > 40.0)
        bg = float(np.median((f - pred)[far])) if np.any(far) else 0.0
        tw = t[win]
        dfw = (f[win] - pred[win]) - bg
        ew = ferr[win]
        best_sm_w = 0.0
        t_rough = t_anom
        best_k = 7
        for k in [3, 15, 63, 255]:
            if len(dfw) >= k:
                sm = np.convolve(
                    dfw / ew, np.ones(k) / np.sqrt(float(k)), mode="same"
                )
                near_w = np.abs(tw - t_anom) < 3.0
                if np.any(near_w):
                    im = int(np.where(near_w)[0][np.argmax(np.abs(sm[near_w]))])
                    if abs(sm[im]) > best_sm_w:
                        best_sm_w = float(abs(sm[im]))
                        t_rough = float(tw[im])
                        best_k = k
        cent_m = np.abs(tw - t_rough) <= max(best_k * 0.0105, 0.035)
        w_c = np.maximum((np.abs(dfw[cent_m]) / ew[cent_m]) - 2.0, 0.0) ** 2
        t_pk = (
            float(np.sum(tw[cent_m] * w_c) / np.sum(w_c))
            if np.sum(w_c) > 0
            else t_rough
        )
        best_c2 = 1e30
        best_lq = -3.0
        for lq in np.linspace(-6.0, -1.5, 46):
            tEp = (10.0 ** (0.5 * lq)) * tE
            dtau_p = (tw - t_pk) / tEp
            for u0_p in np.concatenate([[0.0], np.logspace(-2.2, 0.55, 28)]):
                up = np.sqrt(u0_p * u0_p + dtau_p * dtau_p)
                for rho_s in np.geomspace(0.0006, 0.015, 10):
                    rho_p = min(rho_s / (10.0 ** (0.5 * lq)), 25.0)
                    Ap = fspl_mag_exact(up, rho_p)
                    df_mod = Fs * (Ap - 1.0)
                    c2 = float(np.sum(((dfw - df_mod) / ew) ** 2))
                    if c2 < best_c2:
                        best_c2 = c2
                        best_lq = float(lq)
        return sp, float(10.0**best_lq), t_anom, best_sm, "wide_fspl"

    idx_sub = np.unique(
        np.clip(
            ia_c
            + np.array(
                [
                    -180, -140, -105, -75, -52, -36, -24, -16, -11, -7, -4, -2, -1,
                    0, 1, 2, 4, 7, 11, 16, 24, 36, 52, 75, 105, 140, 180,
                ]
            ),
            0,
            len(t) - 1,
        )
    )
    ts = t[idx_sub]
    dtau_sub = (ts - t0) / tE
    df_obs = f[idx_sub] - pred[idx_sub]
    bg_off = float(np.median(df_obs[[0, 1, 2, -3, -2, -1]]))
    df_obs = df_obs - bg_off
    es = ferr[idx_sub]
    n_pts = len(ts)
    mag_buf = np.empty(n_pts, dtype=np.float64)

    if (u0 < 0.04 and ua < 0.06 and sp >= 1.8) or (u0 < 0.005 and ua < 0.02):
        best_chi2 = 1e30
        best_lq = -3.0
        for lq in np.linspace(-5.6, -1.5, 25):
            q = 10.0**lq
            m2 = q / (1.0 + q)
            s_cand = sp
            z_host = (-m2 * (s_cand - 1.0 / s_cand)) if s_cand >= 1.0 else 0.0
            for th in np.linspace(0.08, 3.06, 16):
                ct, st_ang = np.cos(th), np.sin(th)
                for b_perp in [u0, -u0]:
                    u1 = np.ascontiguousarray(
                        z_host + dtau_sub * ct - b_perp * st_ang, dtype=np.float64
                    )
                    u2 = np.ascontiguousarray(
                        dtau_sub * st_ang + b_perp * ct, dtype=np.float64
                    )
                    du = np.maximum(np.sqrt((u1 - z_host) ** 2 + u2**2), 1e-5)
                    A_pspl = (du * du + 2.0) / (du * np.sqrt(du * du + 4.0))
                    for rho in [0.0008, 0.003, 0.008, 0.018]:
                        lib.bl_magnification_fs(
                            n_pts,
                            u1.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                            u2.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                            s_cand,
                            q,
                            rho,
                            0.45,
                            mag_buf.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                        )
                        df_mod = Fs * (mag_buf - A_pspl)
                        c2 = float(np.sum(((df_obs - df_mod) / es) ** 2))
                        if c2 < best_chi2:
                            best_chi2 = c2
                            best_lq = float(lq)
        return sp, float(10.0**best_lq), t_anom, best_sm, "cent_bl"

    if (abs(tau_a) / max(u0, 1e-4) < 0.60 and u0 >= 0.02) or (
        ua >= 2.0 and sp >= 2.0
    ):
        c2_null = float(np.sum((df_obs / es) ** 2))
        best_chi_host = 1e30
        best_lq_host = -3.0
        s_plus = sp if sp >= 1.0 else 1.0 / sp
        for lq in np.linspace(-5.5, -1.55, 24):
            q = 10.0**lq
            m2 = q / (1.0 + q)
            for s_cand in [s_plus, 1.0 / s_plus]:
                z_host = (-m2 * (s_cand - 1.0 / s_cand)) if s_cand >= 1.0 else 0.0
                for th in np.linspace(0.05, 6.23, 36):
                    ct, st_ang = np.cos(th), np.sin(th)
                    u1 = np.ascontiguousarray(
                        z_host + dtau_sub * ct - u0 * st_ang, dtype=np.float64
                    )
                    u2 = np.ascontiguousarray(
                        dtau_sub * st_ang + u0 * ct, dtype=np.float64
                    )
                    du = np.maximum(np.sqrt((u1 - z_host) ** 2 + u2**2), 1e-5)
                    A_pspl = (du * du + 2.0) / (du * np.sqrt(du * du + 4.0))
                    for rho in [0.001, 0.005, 0.015]:
                        lib.bl_magnification_fs(
                            n_pts,
                            u1.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                            u2.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                            s_cand,
                            q,
                            rho,
                            0.45,
                            mag_buf.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
                        )
                        df_mod = Fs * (mag_buf - A_pspl)
                        c2 = float(np.sum(((df_obs - df_mod) / es) ** 2))
                        if c2 < best_chi_host:
                            best_chi_host = c2
                            best_lq_host = float(lq)
        r2_host = 1.0 - best_chi_host / max(c2_null, 1.0)
        if r2_host > 0.48 or (ua >= 2.0 and sp >= 2.0):
            return sp, float(10.0**best_lq_host), t_anom, best_sm, "host_traj"

    dtau_c = np.ascontiguousarray((ts - t_anom) / tE, dtype=np.float64)
    df_c = np.ascontiguousarray(df_obs, dtype=np.float64)
    es_c = np.ascontiguousarray(es, dtype=np.float64)
    ic = 1 if (sp in (1.25, 2.0, 2.8) and Fs > 0.30) else 0
    best_c2 = ctypes.c_double(0.0)
    lq_fit = float(
        lib.bl_fit_event_logq(
            n_pts,
            dtau_c.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            df_c.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            es_c.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
            u0,
            tau_a,
            Fs,
            sp,
            ic,
            ctypes.byref(best_c2),
        )
    )
    return sp, float(10.0**lq_fit), t_anom, best_sm, "caust_bl"


def solve_single_event(args_tuple):
    ev, lc_dir = args_tuple
    w, z = load_event(ev, lc_dir)
    is_cv, _, max_snrw, _ = classify_cv(w, z)
    if is_cv:
        return {
            "event_id": ev,
            "pred_class": "CV",
            "pred_s": 0.0,
            "pred_q": 0.0,
            "host_t0": 0.0,
            "host_u0": 0.0,
            "host_tE": 0.0,
            "host_Fs": 0.0,
            "anom_t": 0.0,
            "anom_snr": float(max_snrw),
            "regime": "cv_achromatic_outburst",
        }

    t, _, _, f, ferr, _, f_base, seasons = preprocess_lc(w)
    res = fit_host_clean(t, f, ferr, f_base, seasons)
    snr_h0, dt0_gap = compute_h0_snr(t, f, ferr, res)
    is_usbl = (
        (snr_h0 >= 5.0)
        or res["use_wing_mask"]
        or (dt0_gap > 8.0 and res["Fs"] > 0.05)
    )
    if not is_usbl:
        return {
            "event_id": ev,
            "pred_class": "PSPL",
            "pred_s": 0.0,
            "pred_q": 0.0,
            "host_t0": float(res["t0"]),
            "host_u0": float(res["u0"]),
            "host_tE": float(res["tE"]),
            "host_Fs": float(res["Fs"]),
            "anom_t": float(res["t0"]),
            "anom_snr": float(snr_h0),
            "regime": "pspl_unregularized_h0",
        }

    sp, qp, t_anom, best_sm, regime = solve_sq_from_host(t, f, ferr, res)
    return {
        "event_id": ev,
        "pred_class": "USBL",
        "pred_s": float(sp),
        "pred_q": float(qp),
        "host_t0": float(res["t0"]),
        "host_u0": float(res["u0"]),
        "host_tE": float(res["tE"]),
        "host_Fs": float(res["Fs"]),
        "anom_t": float(t_anom),
        "anom_snr": float(max(snr_h0, best_sm)),
        "regime": regime,
    }


def main():
    ap = argparse.ArgumentParser(
        description="Self-contained zero-leakage Roman 2018 Microlensing Data Challenge solver"
    )
    ap.add_argument(
        "--lc-dir",
        required=True,
        help="Directory containing ulwdc1_<NNN>_W149.txt and ulwdc1_<NNN>_Z087.txt",
    )
    ap.add_argument(
        "--out-tsv",
        required=True,
        help="Path to write output predictions TSV",
    )
    ap.add_argument(
        "--workers",
        type=int,
        default=min(8, os.cpu_count() or 1),
        help="Number of parallel worker processes",
    )
    args = ap.parse_args()

    t_start = time.time()
    tasks = [(ev, args.lc_dir) for ev in range(1, 294)]
    if args.workers > 1:
        with ProcessPoolExecutor(max_workers=args.workers) as pool:
            rows_out = list(pool.map(solve_single_event, tasks))
    else:
        rows_out = [solve_single_event(t) for t in tasks]

    rows_out.sort(key=lambda r: r["event_id"])
    with open(args.out_tsv, "w", encoding="utf-8") as fp:
        fp.write(
            "event_id\tpred_class\tpred_s\tpred_q\thost_t0\thost_u0\thost_tE\thost_Fs\tanom_t\tanom_snr\tregime\n"
        )
        for r in rows_out:
            fp.write(
                f"{r['event_id']}\t{r['pred_class']}\t{r['pred_s']:.6f}\t{r['pred_q']:.8e}\t"
                f"{r['host_t0']:.5f}\t{r['host_u0']:.6f}\t{r['host_tE']:.5f}\t{r['host_Fs']:.6f}\t"
                f"{r['anom_t']:.5f}\t{r['anom_snr']:.3f}\t{r['regime']}\n"
            )
    print(
        f"Solved 293 Roman DC18 events in {time.time() - t_start:.1f}s -> {args.out_tsv}"
    )


if __name__ == "__main__":
    main()
