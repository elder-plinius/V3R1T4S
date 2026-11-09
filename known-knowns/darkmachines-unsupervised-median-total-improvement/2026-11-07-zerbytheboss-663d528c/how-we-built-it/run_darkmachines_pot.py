#!/usr/bin/env python3
"""
Standalone 27-Invariant Upper-Tail Log-Survival POT & Multiplicity-Stratum Z-Score
Unsupervised Anomaly Detector for the Dark Machines Anomaly Score Challenge (Zenodo 3961917).

Protocol:
- Trains strictly on odd-event_ID SM background events per channel (eids % 2 == 1).
- Evaluates thresholds (eps_B = 1e-2, 1e-3, 1e-4 with tied scores counted as passing)
  strictly on even-event_ID SM background events (eids % 2 == 0).
- Evaluates signal efficiencies eps_S (rounded to 2 decimal places per official challenge
  notebook 04-SignificanceImprovement.ipynb) and SI = eps_S / sqrt(eps_B) across all 34
  signal-channel files (19 unique BSM signals).
"""
import argparse
import glob
import math
import os
import numpy as np
import pandas as pd

LOG1P_COLS = [
    0, 1, 2, 3, 4, 5, 6, 7, 10,
    15, 16, 17, 18,
    21, 22, 23, 24, 25, 26,
    29, 30, 31, 32, 33, 34,
    35, 36, 37, 38, 39, 40,
    41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51
]

CORE_FEATS = [
    0, 8, 9, 52, 53,
    1, 2, 3, 4, 7, 12, 13, 14, 15, 16, 20,
    30, 32, 34,
    38, 39, 40, 43, 44, 47, 48, 51,
]

U_GRID = np.linspace(0.0, 10.5, 1500)
P_GRID = 1.0 - 0.5 * np.exp(-U_GRID)


def load_bin(path):
    raw = np.fromfile(path, dtype=np.uint8)
    rec_size = 8 + 52 * 4
    n_rec = len(raw) // rec_size
    raw = raw.reshape(n_rec, rec_size)
    eids = np.frombuffer(raw[:, :8].tobytes(), dtype=np.int64)
    feats = np.frombuffer(raw[:, 8:].tobytes(), dtype=np.float32).reshape(n_rec, 52)
    return eids, feats


def to_linear_gev(X):
    out = X.astype(np.float64, copy=True)
    for c in LOG1P_COLS:
        out[:, c] = np.expm1(np.maximum(0.0, out[:, c]))
    return out


def augment_features(X_lin):
    met = X_lin[:, 0]
    HT = X_lin[:, 1]
    LT = X_lin[:, 3]
    met_had_sig = met / np.sqrt(HT + 1.0)
    met_lt_sig = met / np.sqrt(LT + 1.0)
    return np.column_stack([X_lin, met_had_sig, met_lt_sig])


def compute_exact_threshold(bg_eval_scores, eps_b):
    n_b = len(bg_eval_scores)
    max_pass = int(math.floor(eps_b * n_b))
    if max_pass <= 0:
        return float(np.max(bg_eval_scores)) + 1e-6
    sorted_desc = np.sort(bg_eval_scores)[::-1]
    cand_tau = sorted_desc[max_pass - 1]
    n_passing = int(np.sum(bg_eval_scores >= cand_tau))
    if n_passing <= max_pass:
        return float(cand_tau)
    higher = sorted_desc[sorted_desc > cand_tau]
    if len(higher) == 0:
        return float(cand_tau) + 1e-6
    return float(higher[-1])


def fit_and_score_matrix(X_tr_27, X_ev_27, sig_dict_27):
    X_tr = X_tr_27.astype(np.float64)
    d = X_tr.shape[1]
    q_table = np.quantile(X_tr, P_GRID, axis=0)
    idx_99 = np.searchsorted(P_GRID, 0.99)
    idx_999 = np.searchsorted(P_GRID, 0.999)
    idx_9995 = np.searchsorted(P_GRID, 0.9995)

    active = np.zeros(d, dtype=bool)
    tail_scale = np.ones(d, dtype=np.float64)
    for j in range(d):
        diff = q_table[idx_9995, j] - q_table[idx_99, j]
        if diff > 1e-4:
            active[j] = True
            tail_scale[j] = max(
                (q_table[-1, j] - q_table[idx_999, j]) / (U_GRID[-1] - U_GRID[idx_999]),
                diff / 3.0,
                1e-4,
            )
    act_idx = np.where(active)[0]

    def transform_u(X_part):
        X = X_part.astype(np.float64)
        U = np.zeros((len(X), len(act_idx)), dtype=np.float64)
        for k_i, j in enumerate(act_idx):
            col = X[:, j]
            u_col = np.interp(col, q_table[:, j], U_GRID)
            q0 = q_table[0, j]
            u_col[col <= q0 + 1e-9] = 0.0
            above = col > q_table[-1, j]
            if np.any(above):
                u_col[above] = U_GRID[-1] + (col[above] - q_table[-1, j]) / tail_scale[j]
            U[:, k_i] = u_col
        return U, X[:, act_idx], X

    U_tr, X_tr_act, X_tr_sub = transform_u(X_tr[:150000])
    corr = np.nan_to_num(np.corrcoef(U_tr, rowvar=False), nan=0.0)
    crowding = np.sum(np.maximum(0.0, corr) ** 2, axis=1)
    weights = 1.0 / np.maximum(1.0, crowding)
    weights /= np.sum(weights)

    mean_lin = np.mean(X_tr_act, axis=0)
    std_lin = np.maximum(np.std(X_tr_act, axis=0), 1e-4)
    Z_act = (X_tr_act - mean_lin) / std_lin
    rng = np.random.RandomState(42)
    W = rng.exponential(scale=1.0, size=(len(act_idx), 256))
    W *= weights[:, None] ** 0.5
    W /= np.linalg.norm(W, axis=0, keepdims=True)
    proj_sub = Z_act @ W
    proj_q99 = np.quantile(proj_sub, 0.99, axis=0)
    proj_scale = np.maximum(np.quantile(proj_sub, 0.999, axis=0) - proj_q99, 0.1)

    def get_strata(X_27):
        n_jb = np.clip(np.round(X_27[:, 10]).astype(np.int32), 0, 5)
        n_b = np.clip(np.round(X_27[:, 11]).astype(np.int32), 0, 2)
        n_l = np.clip(np.round(X_27[:, 12]).astype(np.int32), 0, 3)
        return n_l * 18 + n_b * 6 + n_jb

    s_keys = get_strata(X_tr_sub)
    ukeys, ucnts = np.unique(s_keys, return_counts=True)
    strata_stats = {}
    for k, cnt in zip(ukeys, ucnts):
        if cnt < 200:
            continue
        m_k = s_keys == k
        U_k = U_tr[m_k]
        strata_stats[int(k)] = (np.mean(U_k, axis=0), np.maximum(np.std(U_k, axis=0), 0.1))

    models = ["PotHull_Hybrid_Lp3", "PotStrataZ_Lp3", "PotHull_L1_L2_Hull"]

    def score_batch(X_27):
        n_tot = len(X_27)
        out = {m: np.zeros(n_tot, dtype=np.float64) for m in models}
        bsz = 200000
        for s in range(0, n_tot, bsz):
            e = min(n_tot, s + bsz)
            U, X_act, X_f = transform_u(X_27[s:e])
            l1 = np.sum(weights * U, axis=1)
            l2 = np.sqrt(np.sum(weights * (U ** 2), axis=1))
            lp3 = np.sum(weights * (U ** 3), axis=1) ** (1.0 / 3.0)

            Z = (X_act - mean_lin) / std_lin
            proj = Z @ W
            exceed = np.maximum(0.0, (proj - proj_q99) / proj_scale)
            hull = np.sqrt(np.mean(exceed ** 2, axis=1))

            sk = get_strata(X_f)
            zpos_s = np.zeros(e - s, dtype=np.float64)
            for k in np.unique(sk):
                if int(k) not in strata_stats:
                    continue
                mk = sk == k
                mu_u, std_u = strata_stats[int(k)]
                Uk_pos = np.maximum(0.0, (U[mk] - mu_u) / std_u)
                zpos_s[mk] = np.sqrt(np.sum(weights * (Uk_pos ** 2), axis=1))

            out["PotHull_Hybrid_Lp3"][s:e] = l1 + l2 + lp3
            out["PotStrataZ_Lp3"][s:e] = l1 + l2 + lp3 + 0.5 * zpos_s
            out["PotHull_L1_L2_Hull"][s:e] = l1 + l2 + hull
        return out

    bg_sc = score_batch(X_ev_27)
    taus = {
        m: {
            k: compute_exact_threshold(bg_sc[m], eps)
            for k, eps in [("1e-2", 1e-2), ("1e-3", 1e-3), ("1e-4", 1e-4)]
        }
        for m in models
    }
    sig_sc = {sname: score_batch(X_s) for sname, X_s in sig_dict_27.items()}
    return bg_sc, taus, sig_sc


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache-dir", required=True, help="Directory with featurized .bin files")
    args = parser.parse_args()
    for chan_dir, chan_label in [("chan1", "1"), ("chan2a", "2a"), ("chan2b", "2b"), ("chan3", "3")]:
        bg_bin = glob.glob(os.path.join(args.cache_dir, chan_dir, "background_*.bin"))[0]
        eids, feats = load_bin(bg_bin)
        odd = (eids % 2) == 1
        X_tr = feats[odd]
        if len(X_tr) > 300000:
            X_tr = X_tr[np.linspace(0, len(X_tr) - 1, 300000, dtype=np.int64)]
        X_tr_27 = augment_features(to_linear_gev(X_tr))[:, CORE_FEATS]
        X_ev_27 = augment_features(to_linear_gev(feats[~odd]))[:, CORE_FEATS]
        sigs = {}
        for sb in sorted(glob.glob(os.path.join(args.cache_dir, chan_dir, "*.bin"))):
            if os.path.basename(sb).startswith("background_"):
                continue
            sname = os.path.basename(sb).replace(f"_chan{chan_label}.bin", "")
            sigs[sname] = augment_features(to_linear_gev(load_bin(sb)[1]))[:, CORE_FEATS]
        bg_sc, taus, sig_sc = fit_and_score_matrix(X_tr_27, X_ev_27, sigs)
        print(f"Channel {chan_label}: scored {len(sigs)} signals.")
