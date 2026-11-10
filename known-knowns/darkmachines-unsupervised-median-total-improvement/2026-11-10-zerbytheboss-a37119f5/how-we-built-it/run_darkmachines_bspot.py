#!/usr/bin/env python3
"""
Standalone Pure-Python/NumPy Bayesian Stratified Peaks-Over-Threshold (BS-POT)
Unsupervised Anomaly Detector for the Dark Machines Anomaly Score Challenge (Zenodo 3961917).

Mirrors `how-we-built-it/dm_bsp_eval.c` in float32 arithmetic:
- Trains 100% on odd-event_ID SM background events per channel (`eid % 2 == 1`).
- Evaluates exact tie-aware thresholds (`eps_B = 1e-2, 1e-3, 1e-4`) on 100% of even-event_ID
  SM background events (`eid % 2 == 0`).
- Zero signal labels, zero signal files read before scoring, and identical rules across all 4 channels.
"""
import math
import numpy as np

N_RAW = 52
N_AUG = 56
N_GRID = 512
U_MAX = 11.0
N_STRATA = 60
MIN_STRATUM_N = 250
MAX_TRAIN_GLOBAL = 250000
MAX_TRAIN_STRATUM = 60000

IS_LOG1P = [
    1,1,1,1,1,1,1,1, 0,0, 1, 0,0,0,0, 1,1,1,1, 0,0,
    1,1,1,1,1,1, 0,0, 1,1,1,1,1,1, 1,1,1,1,1,1,
    1,1,1,1,1,1,1,1,1,1,1
]

SEC_COLS = [
    [0, 8, 9, 10, 52, 53],
    [29, 30, 31, 32, 34, 55],
    [1, 2, 4, 6, 7, 15, 16, 18, 21, 22, 23, 24, 33],
    [3, 35, 36, 37, 38, 39, 40, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 54],
]

CORE27_COLS = [
    0, 8, 9, 52, 53,
    1, 2, 3, 4, 7, 12, 13, 14, 15, 16, 20,
    30, 32, 34,
    38, 39, 40, 43, 44, 47, 48, 51,
]

MODELS = ["BSPOT_MaxSec", "BSPOT_Bayes_Full", "BSPOT_FloorGuard", "BSPOT_Union_OR"]

U_GRID = (np.float32(U_MAX) * np.arange(N_GRID, dtype=np.float32)) / np.float32(N_GRID - 1)
P_GRID_MARGINAL = 1.0 - 0.5 * np.exp(-U_GRID.astype(np.float64))
P_GRID_EXP1 = 1.0 - np.exp(-U_GRID.astype(np.float64))


def augment_events(raw_52):
    n = len(raw_52)
    out = np.zeros((n, N_AUG), dtype=np.float32)
    for j in range(N_RAW):
        v = raw_52[:, j].astype(np.float32, copy=True)
        if IS_LOG1P[j]:
            v = np.expm1(np.maximum(np.float32(0.0), v))
        out[:, j] = v
    met = out[:, 0]
    ht = out[:, 1]
    ht_b = out[:, 2]
    lt = out[:, 3]
    out[:, 52] = met / np.sqrt(ht + np.float32(1.0))
    out[:, 53] = met / np.sqrt(lt + np.float32(1.0))
    out[:, 54] = lt / (ht + np.float32(2.0) * ht_b + np.float32(20.0))
    out[:, 55] = (out[:, 38] + out[:, 39]) * np.sqrt(out[:, 30] + out[:, 32] + np.float32(1.0))
    return out


def stratum_ids(X_aug):
    nl = np.clip(np.rint(X_aug[:, 14]).astype(np.int32), 0, 3)
    nb = np.clip(np.rint(X_aug[:, 13]).astype(np.int32), 0, 2)
    nj = np.clip(np.rint(X_aug[:, 12]).astype(np.int32), 0, 4)
    return nl * 15 + nb * 5 + nj


def fit_cal1d(vals_f32, p_grid):
    s = np.sort(vals_f32.astype(np.float32))
    n = len(s)
    pos = p_grid * float(n - 1)
    lo = np.clip(pos.astype(np.int64), 0, max(0, n - 1))
    q = np.empty(N_GRID, dtype=np.float32)
    mask_end = lo >= (n - 1)
    q[mask_end] = s[n - 1]
    not_end = ~mask_end
    if np.any(not_end):
        lo_ne = lo[not_end]
        frac = (pos[not_end] - lo_ne.astype(np.float64)).astype(np.float32)
        q[not_end] = s[lo_ne] + frac * (s[lo_ne + 1] - s[lo_ne])

    i99 = int(np.max(np.where(p_grid <= 0.99)[0]))
    i999 = int(np.max(np.where(p_grid <= 0.999)[0]))
    i9995 = int(np.max(np.where(p_grid <= 0.9995)[0]))
    span = float(q[i9995] - q[i99])
    if span > 1e-4:
        du = float(U_GRID[-1] - U_GRID[i999])
        s1 = float(q[-1] - q[i999]) / du if du > 1e-3 else 0.0
        sc = max(s1, span / 3.0, 1e-4)
        return {"q": q, "scale": np.float32(sc), "active": True}
    return {"q": q, "scale": np.float32(1.0), "active": False}


def apply_cal1d_vec(x_f32, cal):
    if not cal["active"]:
        return np.zeros(len(x_f32), dtype=np.float32)
    q = cal["q"]
    x = x_f32.astype(np.float32)
    out = np.zeros(len(x), dtype=np.float32)
    m_hi = x >= q[-1]
    if np.any(m_hi):
        out[m_hi] = U_GRID[-1] + (x[m_hi] - q[-1]) / cal["scale"]
    m_mid = (x > (q[0] + np.float32(1e-7))) & (~m_hi)
    if np.any(m_mid):
        xm = x[m_mid]
        hi = np.clip(np.searchsorted(q, xm, side="right"), 1, N_GRID - 1)
        lo = hi - 1
        denom = q[hi] - q[lo]
        flat = denom <= np.float32(1e-12)
        res = np.empty(len(xm), dtype=np.float32)
        if np.any(flat):
            res[flat] = U_GRID[hi[flat]]
        if np.any(~flat):
            nf = ~flat
            res[nf] = U_GRID[lo[nf]] + ((xm[nf] - q[lo[nf]]) / denom[nf]) * (U_GRID[hi[nf]] - U_GRID[lo[nf]])
        out[m_mid] = res
    return out


def train_stratum_model(X):
    n = len(X)
    feat_cal = [fit_cal1d(X[:, j], P_GRID_MARGINAL) for j in range(N_AUG)]
    U_mat = np.column_stack([apply_cal1d_vec(X[:, j], feat_cal[j]) for j in range(N_AUG)])

    feat_w = []
    sec_active = []
    sec_cal = []
    sec_scores = np.zeros((n, len(SEC_COLS)), dtype=np.float32)
    n_act_sec = 0

    for s_idx, scols in enumerate(SEC_COLS):
        act_cols = [j for j in scols if feat_cal[j]["active"]]
        if not act_cols:
            feat_w.append(np.zeros(len(scols), dtype=np.float32))
            sec_active.append(False)
            sec_cal.append({"q": np.zeros(N_GRID, dtype=np.float32), "scale": np.float32(1.0), "active": False})
            continue
        U_sub = U_mat[:, act_cols].astype(np.float64)
        mean_u = np.mean(U_sub, axis=0)
        var_u = np.mean(U_sub * U_sub, axis=0) - mean_u * mean_u
        std_u = np.where(var_u > 1e-8, np.sqrt(np.maximum(var_u, 0.0)), 1e-4)
        step = n // 20000 if n > 20000 else 1
        Z_sub = (U_sub[::step] - mean_u) / std_u
        R = (Z_sub.T @ Z_sub) / float(len(Z_sub))
        np.fill_diagonal(R, 1.0)
        crowd = np.sum(np.maximum(0.0, R) ** 2, axis=1)
        w_raw = (1.0 / np.maximum(1.0, crowd)).astype(np.float32)
        w_norm = w_raw / np.sum(w_raw)

        w_full = np.zeros(len(scols), dtype=np.float32)
        for k_i, j in enumerate(scols):
            if j in act_cols:
                w_full[k_i] = w_norm[act_cols.index(j)]
        feat_w.append(w_full)

        U_s = U_mat[:, scols]
        l1 = U_s @ w_full
        l2 = (U_s * U_s) @ w_full
        l4 = (U_s * U_s * U_s * U_s) @ w_full
        r_sec = (l1 + np.sqrt(l2) + np.sqrt(np.sqrt(l4))).astype(np.float32)
        scal = fit_cal1d(r_sec, P_GRID_EXP1)
        sec_cal.append(scal)
        sec_active.append(scal["active"])
        if scal["active"]:
            n_act_sec += 1
            sec_scores[:, s_idx] = apply_cal1d_vec(r_sec, scal)

    mx = np.max(sec_scores, axis=1)
    sm_c = np.sum(sec_scores, axis=1)
    l4_c = np.sum(sec_scores ** 4, axis=1)
    denom_s = np.float32(max(1, n_act_sec))
    mean_c = sm_c / denom_s if n_act_sec > 0 else np.zeros(n, dtype=np.float32)
    comb_raw = (np.float32(0.5) * mx + np.float32(0.5) * np.sqrt(np.sqrt(l4_c / denom_s)) + np.float32(0.35) * mean_c).astype(np.float32)
    comb_cal = fit_cal1d(comb_raw, P_GRID_EXP1)
    return {
        "feat_cal": feat_cal,
        "feat_w": feat_w,
        "sec_active": sec_active,
        "sec_cal": sec_cal,
        "comb_cal": comb_cal,
        "n_act_sec": n_act_sec,
    }


def eval_stratum_kin_batch(X, sm):
    n = len(X)
    n_act = sm["n_act_sec"]
    if n_act == 0:
        z = np.zeros(n, dtype=np.float32)
        return z, z
    mx = np.zeros(n, dtype=np.float32)
    sm_c = np.zeros(n, dtype=np.float32)
    l4_c = np.zeros(n, dtype=np.float32)
    for s_idx, scols in enumerate(SEC_COLS):
        if not sm["sec_active"][s_idx]:
            continue
        w = sm["feat_w"][s_idx]
        act_k = [k for k in range(len(scols)) if w[k] > 0.0]
        l1 = np.zeros(n, dtype=np.float32)
        l2 = np.zeros(n, dtype=np.float32)
        lf4 = np.zeros(n, dtype=np.float32)
        for k in act_k:
            j = scols[k]
            u = apply_cal1d_vec(X[:, j], sm["feat_cal"][j])
            u2 = u * u
            l1 += w[k] * u
            l2 += w[k] * u2
            lf4 += w[k] * u2 * u2
        r_sec = l1 + np.sqrt(l2) + np.sqrt(np.sqrt(lf4))
        c = apply_cal1d_vec(r_sec, sm["sec_cal"][s_idx])
        mx = np.maximum(mx, c)
        sm_c += c
        l4_c += (c * c) * (c * c)
    denom = np.float32(n_act)
    raw_comb = np.float32(0.5) * mx + np.float32(0.5) * np.sqrt(np.sqrt(l4_c / denom)) + np.float32(0.35) * (sm_c / denom)
    return apply_cal1d_vec(raw_comb, sm["comb_cal"]), mx


def fit_and_score_channel(X_odd_raw, X_even_raw, sig_raw_dict):
    X_odd = augment_events(X_odd_raw)
    X_even = augment_events(X_even_raw)
    n_odd = len(X_odd)
    sids_odd = stratum_ids(X_odd)
    cids_odd = (sids_odd // 15) * 2 + (((sids_odd % 15) // 5) >= 1).astype(np.int32)

    strat_tot = np.bincount(sids_odd, minlength=N_STRATA)
    coarse_tot = np.bincount(cids_odd, minlength=12)
    stratum_nlp = (-np.log((strat_tot.astype(np.float64) + 1.0) / (float(n_odd) + float(N_STRATA)))).astype(np.float32)

    global_sm = train_stratum_model(X_odd)
    strata_sm = {}
    for s in range(N_STRATA):
        if strat_tot[s] >= MIN_STRATUM_N:
            strata_sm[s] = train_stratum_model(X_odd[sids_odd == s])
    coarse_sm = {}
    for c in range(12):
        if coarse_tot[c] >= MIN_STRATUM_N:
            coarse_sm[c] = train_stratum_model(X_odd[cids_odd == c])

    # Fit FloorGuardCal on X_odd
    act_k = [k for k, j in enumerate(CORE27_COLS) if global_sm["feat_cal"][j]["active"]]
    U27 = np.column_stack([apply_cal1d_vec(X_odd[:, CORE27_COLS[k]], global_sm["feat_cal"][CORE27_COLS[k]]) for k in act_k]).astype(np.float64)
    mu27 = np.mean(U27, axis=0)
    var27 = np.mean(U27 * U27, axis=0) - mu27 * mu27
    sd27 = np.where(var27 > 1e-8, np.sqrt(np.maximum(var27, 0.0)), 1e-4)
    Z27 = (U27 - mu27) / sd27
    R27 = (Z27.T @ Z27) / float(len(Z27))
    np.fill_diagonal(R27, 1.0)
    crowd27 = np.sum(np.maximum(0.0, R27) ** 2, axis=1)
    w_raw27 = (1.0 / np.maximum(1.0, crowd27)).astype(np.float32)
    w_norm27 = w_raw27 / np.sum(w_raw27)
    w27 = np.zeros(len(CORE27_COLS), dtype=np.float32)
    for idx_a, k in enumerate(act_k):
        w27[k] = w_norm27[idx_a]

    def eval_g27(X):
        l1 = np.zeros(len(X), dtype=np.float32)
        l2 = np.zeros(len(X), dtype=np.float32)
        l3 = np.zeros(len(X), dtype=np.float32)
        for k, j in enumerate(CORE27_COLS):
            if w27[k] <= 0.0:
                continue
            u = apply_cal1d_vec(X[:, j], global_sm["feat_cal"][j])
            l1 += w27[k] * u
            l2 += w27[k] * u * u
            l3 += w27[k] * u * u * u
        return l1 + np.sqrt(l2) + np.cbrt(l3)

    def eval_kin_pair(X):
        s_glob, mx_glob = eval_stratum_kin_batch(X, global_sm)
        sids = stratum_ids(X)
        cids = (sids // 15) * 2 + (((sids % 15) // 5) >= 1).astype(np.int32)
        s_cond = np.empty(len(X), dtype=np.float32)
        mx_cond = np.empty(len(X), dtype=np.float32)
        for sid in np.unique(sids):
            m = sids == sid
            cid = int((sid // 15) * 2 + (1 if ((sid % 15) // 5) >= 1 else 0))
            sm = strata_sm.get(int(sid), coarse_sm.get(cid, global_sm))
            sc_m, mx_m = eval_stratum_kin_batch(X[m], sm)
            s_cond[m] = sc_m
            mx_cond[m] = mx_m
        nlp = stratum_nlp[sids]
        ms = np.maximum(mx_cond + np.float32(0.45) * nlp, mx_glob)
        raw_ms = np.float32(0.50) * ms + np.float32(0.50) * s_cond + np.float32(0.25) * s_glob
        return raw_ms, s_glob, s_cond, nlp

    g27_odd = eval_g27(X_odd)
    ms_odd, _, _, _ = eval_kin_pair(X_odd)
    g27_cal = fit_cal1d(g27_odd, P_GRID_EXP1)
    ms_cal = fit_cal1d(ms_odd, P_GRID_EXP1)

    def score_aug(X):
        raw_ms, s_glob, s_cond, nlp = eval_kin_pair(X)
        jb = np.maximum(s_cond + np.float32(0.50) * nlp, s_glob)
        raw_bayes = jb + np.float32(0.25) * (s_cond + s_glob)
        u_g27 = apply_cal1d_vec(eval_g27(X), g27_cal)
        u_ms = apply_cal1d_vec(raw_ms, ms_cal)
        u_mx = np.maximum(u_ms, u_g27)
        return {
            "BSPOT_MaxSec": raw_ms,
            "BSPOT_Bayes_Full": raw_bayes,
            "BSPOT_FloorGuard": np.float32(0.75) * u_g27 + np.float32(0.25) * u_ms + np.float32(0.25) * u_mx,
            "BSPOT_Union_OR": u_mx + np.float32(0.35) * u_g27 + np.float32(0.15) * u_ms,
        }

    bg_sc = score_aug(X_even)
    taus = {}
    n_b = len(X_even)
    for m in MODELS:
        asc = np.sort(bg_sc[m])
        taus[m] = {}
        for k, eps in [("1e-2", 1e-2), ("1e-3", 1e-3), ("1e-4", 1e-4)]:
            mp = int(math.floor(eps * n_b))
            if mp <= 0:
                taus[m][k] = float(asc[-1]) + 1e-5
                continue
            pos = n_b - mp
            ct = asc[pos]
            if pos > 0 and asc[pos - 1] == ct:
                higher = asc[pos + 1 :]
                gt = higher[higher > ct]
                taus[m][k] = float(gt[0]) if len(gt) > 0 else float(ct) + 1e-5
            else:
                taus[m][k] = float(ct)

    sig_sc = {sname: score_aug(augment_events(Xs)) for sname, Xs in sig_raw_dict.items()}
    return bg_sc, taus, sig_sc
