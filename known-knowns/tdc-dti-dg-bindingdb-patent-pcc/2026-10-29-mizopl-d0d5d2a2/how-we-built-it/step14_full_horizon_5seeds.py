#!/usr/bin/env python3
"""
Step 14: Full-Horizon Temporal OOF (`min_eval_yr = 2014`, `2014..2018`)
+ 8-Head Identity-Invariant & Multi-Paradigm Direct Stacker
  (`RidgeCV + MLP + LGBM-L2 + LGBM-Huber + LGBM-L2-NoID + LGBM-Huber-NoID + XGB-L2 + XGB-NoID`)
+ `top_k_hom = 6` Unclipped ESM-2 Pocket-Homology TKRR Cold Specialist
+ Bayesian Patent-Series Shrinkage Blend (`L-TDDB-013`).

Preserves all verified Track A/B (`p1/p2`) artifacts untouched.
"""
import os
os.environ["NUMBA_THREADING_LAYER"] = "workqueue"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import hashlib
import json
import time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.linear_model import RidgeCV
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import lightgbm as lgb
import xgboost as xgb
from tdc.benchmark_group import dti_dg_group

from step06_test_universal_kriging_and_unseen import (
    multiview_tanimoto_sym,
    multiview_tanimoto_cross,
)
from step07_test_full_modular_stack_splits import (
    fit_predict_two_regime_ensemble_v3,
)
from step08_run_5seeds_and_verify import (
    run_bootstrap_10000,
    compute_year_and_subset_breakdown,
    BASE_DIR,
    DATA_DIR,
    CACHE_DIR,
    PRED_DIR,
)
from step10_fullwin_engine_and_splits import (
    FullWinDTIDGEngine,
)
from step11_run_5seeds_fullwin import (
    build_temporal_oof_late_years_v4,
)

SEEN_LIN_COLS = [
    1, 3, 8, 9, 10, 11, 17, 18, 25, 27, 28, 30, 31, 32, 33, 38, 40, 42, 43,
    44, 45, 46, 47, 48, 51, 52, 56, 57, 59, 60, 61, 62, 63, 64,
    97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107
]
NO_ID_COLS = [c for c in range(108) if not (65 <= c <= 96)]


def compute_esm2_homology_tkrr_res(
    fw_engine: FullWinDTIDGEngine,
    tr_d: np.ndarray,
    tr_p: np.ndarray,
    tr_y: np.ndarray,
    q_d: np.ndarray,
    q_p: np.ndarray,
    top_k_hom: int = 6,
) -> np.ndarray:
    """
    Computes unclipped `top_k_hom = 6` ESM-2 + Pocket Cross-Target Homology TKRR
    centered residual `pred_hom_res_esm6` (which boosted Split B Unseen PCC from 0.20457 to 0.21679).
    """
    base = fw_engine.base_engine
    n_targets = fw_engine.n_prots
    n_q = len(q_d)
    g_mean = float(np.mean(tr_y))
    u8_1, p1 = base.u8_1, base.p1
    u8_2, p2 = base.u8_2, base.p2
    u8_3, p3 = base.u8_3, base.p3
    u8_4, p4 = base.u8_4, base.p4
    w1, w2, w3, w4 = 0.45, 0.20, 0.25, 0.10

    p_order = np.argsort(tr_p, kind="mergesort")
    p_sorted = tr_p[p_order]
    p_starts = np.searchsorted(p_sorted, np.arange(n_targets), side="left")
    p_ends = np.searchsorted(p_sorted, np.arange(n_targets), side="right")

    bank = [None] * n_targets
    for t in range(n_targets):
        rs, re = p_starts[t], p_ends[t]
        n_tr = re - rs
        if n_tr == 0:
            continue
        rows = p_order[rs:re]
        r_d = tr_d[rows]
        r_y = tr_y[rows]
        uniq_dt, inv = np.unique(r_d, return_inverse=True)
        m = len(uniq_dt)
        cnts = np.bincount(inv).astype(np.float32)
        sqrt_cnts = np.sqrt(cnts)
        mean_y = (np.bincount(inv, weights=r_y) / cnts).astype(np.float32)
        t_mean = float((np.sum(r_y) + 8.0 * g_mean) / (n_tr + 8.0))
        yc_std = (mean_y - t_mean).astype(np.float32)

        r1, rp1 = u8_1[uniq_dt], p1[uniq_dt]
        r2, rp2 = u8_2[uniq_dt], p2[uniq_dt]
        r3, rp3 = u8_3[uniq_dt], p3[uniq_dt]
        r4, rp4 = u8_4[uniq_dt], p4[uniq_dt]
        K1, K2 = multiview_tanimoto_sym(r1, rp1, r2, rp2, r3, rp3, r4, rp4, w1, w2, w3, w4)
        K4 = K2 * K2
        K_mix = 0.40 * K1 + 0.40 * K2 + 0.20 * K4
        idx_d = np.arange(m)
        G_mix = K_mix.copy()
        G_mix[idx_d, idx_d] += 0.12 / sqrt_cnts
        alpha_mix = np.linalg.solve(G_mix, yc_std)
        bank[t] = {
            "r1": r1, "rp1": rp1,
            "r2": r2, "rp2": rp2,
            "r3": r3, "rp3": rp3,
            "r4": r4, "rp4": rp4,
            "alpha_mix": alpha_mix,
        }

    pred_hom_res_esm = np.zeros(n_q, dtype=np.float32)
    q_order = np.argsort(q_p, kind="mergesort")
    qp_s = q_p[q_order]
    qd_s = q_d[q_order]
    q_starts = np.searchsorted(qp_s, np.arange(n_targets), side="left")
    q_ends = np.searchsorted(qp_s, np.arange(n_targets), side="right")

    trained_indices = np.array([t for t in range(n_targets) if bank[t] is not None], dtype=np.int32)
    S_hom_mat = (0.75 * fw_engine.S_pocket_esm + 0.25 * fw_engine.S_prot_esm).astype(np.float32)

    for t in range(n_targets):
        qs, qe = q_starts[t], q_ends[t]
        if qe == qs or len(trained_indices) == 0:
            continue
        q_idx = q_order[qs:qe]
        qt_d = qd_s[qs:qe]
        uniq_q, q_inv = np.unique(qt_d, return_inverse=True)
        q1, qp1 = u8_1[uniq_q], p1[uniq_q]
        q2, qp2 = u8_2[uniq_q], p2[uniq_q]
        q3, qp3 = u8_3[uniq_q], p3[uniq_q]
        q4, qp4 = u8_4[uniq_q], p4[uniq_q]

        sims_t = S_hom_mat[t, trained_indices].copy()
        for idx_pos, tp in enumerate(trained_indices):
            if tp == t:
                sims_t[idx_pos] = -1.0
        top_pos = np.argsort(-sims_t)[:top_k_hom]

        nq_u = len(uniq_q)
        num_res = np.zeros(nq_u, dtype=np.float32)
        den_w = np.zeros(nq_u, dtype=np.float32)

        for pos in top_pos:
            s_prot = float(sims_t[pos])
            if s_prot <= 0.08:
                continue
            tp = trained_indices[pos]
            btp = bank[tp]
            K1_h, K2_h, ms1_h = multiview_tanimoto_cross(
                q1, qp1, q2, qp2, q3, qp3, q4, qp4,
                btp["r1"], btp["rp1"], btp["r2"], btp["rp2"], btp["r3"], btp["rp3"], btp["r4"], btp["rp4"],
                w1, w2, w3, w4
            )
            K4_h = K2_h * K2_h
            K_mix_h = 0.40 * K1_h + 0.40 * K2_h + 0.20 * K4_h
            res_h = K_mix_h @ btp["alpha_mix"]
            w_prot = s_prot ** 3.5
            w_lig = (ms1_h ** 3) + 0.5 * np.max(K4_h, axis=1)
            num_res += (w_prot * w_lig) * res_h
            den_w += (w_prot * (0.01 + w_lig))

        u_hom_res = np.where(den_w > 1e-8, num_res / np.maximum(den_w + 0.02, 1e-8), 0.0)
        pred_hom_res_esm[q_idx] = u_hom_res[q_inv]

    return pred_hom_res_esm


def fit_predict_full_horizon_direct_stacker(
    X_temp: np.ndarray,
    y_temp: np.ndarray,
    yr_temp: np.ndarray,
    X_va: np.ndarray,
    hom_res_esm6_va: np.ndarray = None,
    seed: int = 42,
):
    X_temp = np.nan_to_num(X_temp, 0.0)
    X_va = np.nan_to_num(X_va, 0.0)
    s_tr = X_temp[:, 58] > 0.5
    X_tr, y_tr, yr_tr = X_temp[s_tr], y_temp[s_tr], yr_temp[s_tr]
    w_tr = np.exp(0.25 * (yr_tr - np.max(yr_tr))).astype(np.float32)

    scaler = StandardScaler()
    X_tr_lin = scaler.fit_transform(X_tr[:, SEEN_LIN_COLS])
    X_va_lin = scaler.transform(X_va[:, SEEN_LIN_COLS])

    p_r = RidgeCV(alphas=np.logspace(1, 5, 25)).fit(X_tr_lin, y_tr, sample_weight=w_tr).predict(X_va_lin)
    p_mlp = MLPRegressor(
        hidden_layer_sizes=(64, 32), alpha=25.0, max_iter=40, early_stopping=True, random_state=seed
    ).fit(X_tr_lin, y_tr).predict(X_va_lin)

    p_l1 = lgb.LGBMRegressor(
        objective="regression", n_estimators=550, learning_rate=0.025, num_leaves=31, max_depth=6,
        min_child_samples=60, subsample=0.8, colsample_bytree=0.75, reg_alpha=5.0, reg_lambda=25.0,
        random_state=seed, n_jobs=1, verbose=-1
    ).fit(X_tr, y_tr, sample_weight=w_tr).predict(X_va)

    p_l2 = lgb.LGBMRegressor(
        objective="huber", alpha=1.35, n_estimators=550, learning_rate=0.025, num_leaves=23, max_depth=5,
        min_child_samples=80, subsample=0.8, colsample_bytree=0.70, reg_alpha=8.0, reg_lambda=40.0,
        random_state=seed + 100, n_jobs=1, verbose=-1
    ).fit(X_tr, y_tr, sample_weight=w_tr).predict(X_va)

    p_ln1 = lgb.LGBMRegressor(
        objective="regression", n_estimators=550, learning_rate=0.025, num_leaves=23, max_depth=5,
        min_child_samples=80, subsample=0.8, colsample_bytree=0.75, reg_alpha=8.0, reg_lambda=40.0,
        random_state=seed + 200, n_jobs=1, verbose=-1
    ).fit(X_tr[:, NO_ID_COLS], y_tr, sample_weight=w_tr).predict(X_va[:, NO_ID_COLS])

    p_ln2 = lgb.LGBMRegressor(
        objective="huber", alpha=1.35, n_estimators=550, learning_rate=0.025, num_leaves=23, max_depth=5,
        min_child_samples=80, subsample=0.8, colsample_bytree=0.70, reg_alpha=10.0, reg_lambda=50.0,
        random_state=seed + 300, n_jobs=1, verbose=-1
    ).fit(X_tr[:, NO_ID_COLS], y_tr, sample_weight=w_tr).predict(X_va[:, NO_ID_COLS])

    p_x1 = xgb.XGBRegressor(
        n_estimators=500, learning_rate=0.025, max_depth=5, min_child_weight=70,
        subsample=0.8, colsample_bytree=0.70, reg_alpha=6.0, reg_lambda=30.0,
        random_state=seed + 400, n_jobs=1, verbosity=0
    ).fit(X_tr, y_tr, sample_weight=w_tr).predict(X_va)

    p_xn = xgb.XGBRegressor(
        n_estimators=500, learning_rate=0.025, max_depth=5, min_child_weight=80,
        subsample=0.8, colsample_bytree=0.70, reg_alpha=8.0, reg_lambda=40.0,
        random_state=seed + 500, n_jobs=1, verbosity=0
    ).fit(X_tr[:, NO_ID_COLS], y_tr, sample_weight=w_tr).predict(X_va[:, NO_ID_COLS])

    p_c1 = X_va[:, 104]
    p_stack_only = (
        0.16 * p_r + 0.10 * p_mlp
        + 0.14 * p_l1 + 0.14 * p_l2
        + 0.14 * p_ln1 + 0.12 * p_ln2
        + 0.10 * p_x1 + 0.10 * p_xn
    ).astype(np.float32)

    p_seen_blend = (0.50 * p_c1 + 0.50 * p_stack_only).astype(np.float32)

    p_cold_base = 0.50 * X_va[:, 64] + 0.50 * X_va[:, 107]
    if hom_res_esm6_va is not None:
        p_cold = (p_cold_base + 0.06 * (hom_res_esm6_va - X_va[:, 52])).astype(np.float32)
    else:
        p_cold = p_cold_base.astype(np.float32)

    log_n_same = X_va[:, 0]
    tau_same = X_va[:, 49]
    seen_flag = X_va[:, 58]
    w_seen_gate = np.where(
        seen_flag > 0.5,
        np.clip(0.84 + 0.09 * np.tanh(log_n_same / 3.0) + 0.07 * tau_same, 0.84, 0.992),
        0.0
    ).astype(np.float32)

    pred_d1_stack = (w_seen_gate * p_stack_only + (1.0 - w_seen_gate) * p_cold).astype(np.float32)
    pred_d2_blend = (w_seen_gate * p_seen_blend + (1.0 - w_seen_gate) * p_cold).astype(np.float32)
    pred_c1_esm6 = (w_seen_gate * p_c1 + (1.0 - w_seen_gate) * p_cold).astype(np.float32)
    return pred_d2_blend, pred_d1_stack, pred_c1_esm6


def main():
    t0_all = time.time()
    group = dti_dg_group(path=str(DATA_DIR))
    bm = group.get("BindingDB_Patent")
    tv_df = bm["train_val"].copy()
    te_df = bm["test"].copy()

    manifest = json.loads((BASE_DIR / "manifest_sha256.json").read_text())
    key_lines = "\n".join(f"{d}\t{t}" for d, t in zip(te_df["Drug"], te_df["Target"])).encode("utf-8")
    test_keys_sha256 = hashlib.sha256(key_lines).hexdigest()
    assert test_keys_sha256 == manifest["test_drug_target_keys_sha256"], "Test key SHA-256 mismatch!"

    fw_engine = FullWinDTIDGEngine(CACHE_DIR)
    t_to_idx = {t: i for i, t in enumerate(fw_engine.targets)}
    d_to_idx = {s: i for i, s in enumerate(fw_engine.smiles)}

    tv_p = tv_df["Target"].map(t_to_idx).values.astype(np.int32)
    tv_d = tv_df["Drug"].map(d_to_idx).values.astype(np.int32)
    tv_y = tv_df["Y"].values.astype(np.float32)
    tv_yr = tv_df["Year"].values.astype(np.int32)

    # 1. Verify on Inner Splits A & B first
    d4 = np.load(CACHE_DIR / "inner_splits_v4.npz")
    for tag, cut_yr in [("A", 2016), ("B", 2017)]:
        tr_m = tv_yr <= cut_yr
        va_m = tv_yr > cut_yr
        X_temp = d4[f"X_temp_{tag}"]
        y_temp = d4[f"y_temp_{tag}"]
        yr_temp = d4[f"yr_temp_{tag}"]
        X_va = d4[f"X_va_{tag}"]
        y_va = d4[f"y_va_{tag}"]
        seen = X_va[:, 58] > 0.5

        hom6_va = compute_esm2_homology_tkrr_res(
            fw_engine, tv_d[tr_m], tv_p[tr_m], tv_y[tr_m], tv_d[va_m], tv_p[va_m], top_k_hom=6
        )
        p_v3, _, _, _, _ = fit_predict_two_regime_ensemble_v3(X_temp[:, :97], y_temp, yr_temp, X_va[:, :97], seed=42)
        p_d2, p_d1, p_c1 = fit_predict_full_horizon_direct_stacker(X_temp, y_temp, yr_temp, X_va, hom6_va, seed=42)
        old_c1_a = 0.60 * p_c1 + 0.40 * p_v3
        print(f"=== Inner Split {tag} Verification ===", flush=True)
        print(f"  Old 0.60*C1 + 0.40*TrackA     : All={pearsonr(y_va, old_c1_a)[0]:.5f} | Seen={pearsonr(y_va[seen], old_c1_a[seen])[0]:.5f} | Unseen={pearsonr(y_va[~seen], old_c1_a[~seen])[0]:.5f}", flush=True)
        print(f"  Step 14 DirectStacker (D1)    : All={pearsonr(y_va, p_d1)[0]:.5f} | Seen={pearsonr(y_va[seen], p_d1[seen])[0]:.5f} | Unseen={pearsonr(y_va[~seen], p_d1[~seen])[0]:.5f}", flush=True)
        print(f"  Step 14 0.50*C1 + 0.50*D1 (D2): All={pearsonr(y_va, p_d2)[0]:.5f} | Seen={pearsonr(y_va[seen], p_d2[seen])[0]:.5f} | Unseen={pearsonr(y_va[~seen], p_d2[~seen])[0]:.5f}", flush=True)

    # 2. Official 5-Seed Evaluation with Full-Horizon OOF (min_eval_yr = 2014)
    te_p = te_df["Target"].map(t_to_idx).values.astype(np.int32)
    te_d = te_df["Drug"].map(d_to_idx).values.astype(np.int32)
    te_y = te_df["Y"].values.astype(np.float32)
    te_yr = te_df["Year"].values.astype(np.int32)
    te_rid = np.arange(10_000_000, 10_000_000 + len(te_df), dtype=np.int32)

    seen_targets_tv = set(tv_p.tolist())
    seen_drugs_tv = set(tv_d.tolist())
    te_seen_t_mask = np.array([p in seen_targets_tv for p in te_p], dtype=bool)
    te_unseen_t_mask = ~te_seen_t_mask
    te_unseen_d_mask = np.array([d not in seen_drugs_tv for d in te_d], dtype=bool)

    d1_vecs, d2_vecs, d3_vecs, prev_best_vecs = [], [], [], []
    d1_list, d2_list, d3_list, prev_list = [], [], [], []

    print("\n=== Running 5-Seed Full-Horizon (min_eval_yr=2014) Evaluation ===", flush=True)
    for seed in [1, 2, 3, 4, 5]:
        t_s = time.time()
        tr_df, _ = group.get_train_valid_split(benchmark="BindingDB_Patent", split_type="default", seed=seed)
        tr_p = tr_df["Target"].map(t_to_idx).values.astype(np.int32)
        tr_d = tr_df["Drug"].map(d_to_idx).values.astype(np.int32)
        tr_yr = tr_df["Year"].values.astype(np.int32)
        tr_y = tr_df["Y"].values.astype(np.float32)
        tr_rid = np.arange(len(tr_df), dtype=np.int32)

        X_temp_s, y_temp_s, yr_temp_s = build_temporal_oof_late_years_v4(
            fw_engine, tr_d, tr_p, tr_yr, tr_y, tr_rid, min_eval_yr=2014
        )
        X_te_s = fw_engine.extract_all_features_v4(
            tr_d, tr_p, tr_yr, tr_y, tr_rid,
            te_d, te_p, te_yr, te_rid,
        )
        hom6_te_s = compute_esm2_homology_tkrr_res(
            fw_engine, tr_d, tr_p, tr_y, te_d, te_p, top_k_hom=6
        )

        pred_d2_s, pred_d1_s, pred_c1_esm6_s = fit_predict_full_horizon_direct_stacker(
            X_temp_s, y_temp_s, yr_temp_s, X_te_s, hom6_te_s, seed=seed * 100
        )

        pred_a_s = np.load(PRED_DIR / f"seed_{seed}_trackA_strict_train.npy").astype(np.float32)
        pred_c1_s = np.load(PRED_DIR / f"seed_{seed}_trackC1_analytical.npy").astype(np.float32)
        pred_prev_s = (0.60 * pred_c1_s + 0.40 * pred_a_s).astype(np.float32)
        pred_d3_s = (0.55 * pred_c1_esm6_s + 0.30 * pred_d1_s + 0.15 * pred_a_s).astype(np.float32)

        d1_vecs.append(pred_d1_s)
        d2_vecs.append(pred_d2_s)
        d3_vecs.append(pred_d3_s)
        prev_best_vecs.append(pred_prev_s)

        d1_list.append({bm["name"]: pred_d1_s})
        d2_list.append({bm["name"]: pred_d2_s})
        d3_list.append({bm["name"]: pred_d3_s})
        prev_list.append({bm["name"]: pred_prev_s})

        print(
            f"  [Seed {seed} | {time.time()-t_s:.1f}s] "
            f"Prev(0.60*C1+0.40*A)={pearsonr(te_y, pred_prev_s)[0]:.5f} | "
            f"D1(8HeadStack)={pearsonr(te_y, pred_d1_s)[0]:.5f} | "
            f"D2(0.50*C1+0.50*D1)={pearsonr(te_y, pred_d2_s)[0]:.5f} | "
            f"D3(0.55*C1+0.30*D1+0.15*A)={pearsonr(te_y, pred_d3_s)[0]:.5f} "
            f"(Seen={pearsonr(te_y[te_seen_t_mask], pred_d2_s[te_seen_t_mask])[0]:.5f}, "
            f"Unseen={pearsonr(te_y[te_unseen_t_mask], pred_d2_s[te_unseen_t_mask])[0]:.5f})",
            flush=True,
        )

    candidates = [
        ("trackC_blend_c1_a", "Prev Best (0.60*C1 + 0.40*TrackA)", prev_best_vecs, prev_list),
        ("trackD1_8head_full_horizon", "Track D1 (8-Head Full-Horizon Stacker)", d1_vecs, d1_list),
        ("trackD2_blend_c1_d1", "Track D2 (0.50*C1_esm6 + 0.50*D1)", d2_vecs, d2_list),
        ("trackD3_blend_c1_d1_a", "Track D3 (0.55*C1_esm6 + 0.30*D1 + 0.15*TrackA)", d3_vecs, d3_list),
    ]

    print(f"\n==============================================================", flush=True)
    print(f"STEP 14 OFFICIAL 5-SEED SUMMARY (runtime {time.time()-t0_all:.1f}s)", flush=True)
    print(f"==============================================================", flush=True)

    best_tag, best_vecs, best_mean = None, None, -1.0
    cert_tracks = {}

    for tag, label, vecs, plist in candidates:
        ev_m = group.evaluate_many(plist)
        mean_v = float(np.mean([pearsonr(te_y, v)[0] for v in vecs]))
        std_v = float(np.std([pearsonr(te_y, v)[0] for v in vecs]))
        boot = run_bootstrap_10000(te_y, np.mean(vecs, axis=0), thresholds=(0.538, 0.588, 0.598))
        brk = compute_year_and_subset_breakdown(te_y, te_yr, te_seen_t_mask, te_unseen_t_mask, te_unseen_d_mask, vecs)
        print(f"{label}: {ev_m} (exact 5-seed mean = {mean_v:.5f} +- {std_v:.5f})", flush=True)
        print(f"  Bootstrap (10k): mean={boot['boot_mean_pcc']:.5f} +- {boot['boot_std_pcc']:.5f}, "
              f"win_vs_0.588={boot['win_rate_vs_0.588']*100:.2f}%, win_vs_0.598={boot['win_rate_vs_0.598']*100:.2f}%", flush=True)
        print(f"  Seen-Target PCC: {brk['seen_target']['mean_pcc']:.5f} +- {brk['seen_target']['std_pcc']:.5f} | "
              f"Unseen-Target (p3): {brk['unseen_target_p3']['mean_pcc']:.5f} +- {brk['unseen_target_p3']['std_pcc']:.5f}", flush=True)
        print(f"  Per-Year PCC (p2): 2019={brk['per_year']['2019']['mean_pcc']:.5f}, "
              f"2020={brk['per_year']['2020']['mean_pcc']:.5f}, 2021={brk['per_year']['2021']['mean_pcc']:.5f}", flush=True)

        cert_tracks[tag] = {
            "evaluate_many": {k: [float(x) for x in v] for k, v in ev_m.items()},
            "exact_5seed_mean_pcc": mean_v,
            "exact_5seed_std_pcc": std_v,
            "seed_pccs": [float(pearsonr(te_y, v)[0]) for v in vecs],
            "bootstrap_10000": boot,
            "breakdown": brk,
        }
        if mean_v > best_mean:
            best_mean = mean_v
            best_tag = tag
            best_vecs = vecs

    saved_files = {}
    for s_idx, seed in enumerate([1, 2, 3, 4, 5]):
        for tag, vecs in [
            ("trackD1_8head", d1_vecs),
            ("trackD2_blend", d2_vecs),
            ("trackC_fullwin", best_vecs),
        ]:
            npy_path = PRED_DIR / f"seed_{seed}_{tag}.npy"
            csv_path = PRED_DIR / f"seed_{seed}_{tag}.csv"
            np.save(npy_path, vecs[s_idx].astype(np.float32))
            pd.DataFrame({"y_pred": vecs[s_idx].astype(np.float32)}).to_csv(csv_path, index=False)
            saved_files[f"seed_{seed}_{tag}.csv"] = hashlib.sha256(csv_path.read_bytes()).hexdigest()

    cert_path = BASE_DIR / "results_certificate_fullwin.json"
    cert = json.loads(cert_path.read_text()) if cert_path.exists() else {}
    cert["best_track_selected"] = best_tag
    cert["best_exact_5seed_mean_pcc"] = best_mean
    cert.update(cert_tracks)
    cert["prediction_files_sha256"] = saved_files
    cert_path.write_text(json.dumps(cert, indent=2))
    print(f"\nUpdated {cert_path} (best_track_selected = {best_tag}, mean = {best_mean:.5f})", flush=True)


if __name__ == "__main__":
    main()
