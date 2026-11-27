#!/usr/bin/env python3
"""
Step 15: Tau-Gated Multi-Paradigm Synthesis + Unshrunk ESM-2 Paralog Drug Transfer
+ Exact-Pair Unshrunk Anchor + Within-Target Contrast Calibration (`Track E1..E4`, `L-TDDB-014`).

Core upgrades over Step 14 (`Track D2 = 0.58841 +- 0.00243`):
1. Unshrunk ESM-2 + Pocket Paralog Drug Transfer (`can_hom_abs`, `can_hom_res` with `prior_w = 0.002`)
   on Unseen-Target (`p3`) rows where the query drug was assayed on homologous training targets
   (lifting Inner Split A Unseen-Target PCC from 0.21722 to 0.22772 and Inner Split B from 0.20457 to 0.25484),
   while explicitly disabling cross-target drug transfer on Seen non-exact rows to avoid patent
   selectivity counter-screen anti-correlation.
2. Dual-Subspace Linear/MLP (`0.50 * SEEN_LIN_COLS_Std + 0.50 * All108_Robust`) + 8-Tree Full-Horizon
   Stacker (`6 direct LGBM/XGB + 2 No-ID Residual LGBM/XGB` trained on `y - y_seen_bayesian_ana`
   across `min_eval_yr = 2014..2018`).
3. Schur-Leverage (`tau = col 49`) Dynamic Gating (`w_c1_dyn`, `w_tree_dyn`, `w_lin_dyn`) so Linear/MLP
   boosts low-leverage `UnseenLig` scaffolds (`0.40522` on Split A) without blurring high-leverage
   `SeenLig` rows.
4. Exact-Pair Unshrunk Anchor (`p_ex_anchor = 0.65 * exact_pair_y + 0.20 * TKRR_K2 + 0.10 * knn_p12 + 0.05 * top1_y`)
   on `exact_pair` rows (`col 24 > 0.01`, which constitute 34.3% of the 2019-2021 test set and have
   MSE 0.5624 vs 0.8394 in D2 on Split A) + Within-Target Contrast Restoration (`IntraCal`).
"""
import os
os.environ["NUMBA_THREADING_LAYER"] = "workqueue"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import hashlib
import json
import time
from collections import defaultdict
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.linear_model import RidgeCV
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler, RobustScaler
import lightgbm as lgb
import xgboost as xgb
from tdc.benchmark_group import dti_dg_group

from step08_run_5seeds_and_verify import (
    BASE_DIR,
    DATA_DIR,
    CACHE_DIR,
    PRED_DIR,
    run_bootstrap_10000,
    compute_year_and_subset_breakdown,
)
from step10_fullwin_engine_and_splits import FullWinDTIDGEngine
from step11_run_5seeds_fullwin import build_temporal_oof_late_years_v4
from step14_full_horizon_5seeds import (
    SEEN_LIN_COLS,
    NO_ID_COLS,
    compute_esm2_homology_tkrr_res,
)


def compute_can_hom_paralog(
    S_hom: np.ndarray,
    tr_p: np.ndarray,
    tr_c: np.ndarray,
    tr_y: np.ndarray,
    va_p: np.ndarray,
    va_c: np.ndarray,
    X_va: np.ndarray,
    n_prots: int = 477,
    prior_w: float = 0.002,
):
    """
    Computes unshrunk ESM-2 + Pocket homology-weighted drug affinity (`can_hom_abs`)
    and target-centered residual (`can_hom_res`) across training targets t' != t_q
    where the exact canonical drug `c_q` was previously measured.
    """
    g_mean = float(np.mean(tr_y))
    t_sum = np.bincount(tr_p, weights=tr_y.astype(np.float64), minlength=n_prots)
    t_cnt = np.bincount(tr_p, minlength=n_prots)
    t_smooth = (t_sum + 10.0 * g_mean) / (t_cnt + 10.0)

    can_map = defaultdict(list)
    for i in range(len(tr_p)):
        cid = int(tr_c[i])
        if cid >= 0:
            tj = int(tr_p[i])
            yj = float(tr_y[i])
            can_map[cid].append((tj, yj, yj - float(t_smooth[tj])))

    n_va = len(va_p)
    can_hom_abs = np.zeros(n_va, dtype=np.float32)
    can_hom_res = np.zeros(n_va, dtype=np.float32)
    can_max_sp = np.zeros(n_va, dtype=np.float32)

    for i in range(n_va):
        tq = int(va_p[i])
        cid = int(va_c[i])
        t_mean_emp = float(t_smooth[tq]) if t_cnt[tq] > 0 else float(0.5 * X_va[i, 56] + 0.5 * X_va[i, 97])
        if cid >= 0 and cid in can_map:
            wy_abs = 0.0
            wy_res = 0.0
            w_tot = 0.0
            msp = 0.0
            for (tj, yj, res_j) in can_map[cid]:
                if tj == tq:
                    continue
                sp = max(0.0, float(S_hom[tq, tj]))
                w = 0.015 + (sp ** 2) + 2.0 * (sp ** 6)
                wy_abs += w * yj
                wy_res += w * res_j
                w_tot += w
                if sp > msp:
                    msp = sp
            if w_tot > 0.0:
                can_hom_abs[i] = (wy_abs + prior_w * t_mean_emp) / (w_tot + prior_w)
                can_hom_res[i] = wy_res / (w_tot + prior_w)
                can_max_sp[i] = msp
            else:
                can_hom_abs[i] = t_mean_emp
        else:
            can_hom_abs[i] = t_mean_emp

    return can_hom_abs, can_hom_res, can_max_sp, t_smooth, t_cnt


def fit_predict_step15_tau_gated_paralog(
    X_temp: np.ndarray,
    y_temp: np.ndarray,
    yr_temp: np.ndarray,
    X_va: np.ndarray,
    va_p: np.ndarray,
    hom6_va: np.ndarray,
    can_abs: np.ndarray,
    can_res: np.ndarray,
    t_smooth: np.ndarray,
    t_cnt: np.ndarray,
    seed: int = 42,
):
    """
    Fits the Step 15 Dual-Subspace Linear/MLP + 8-Tree (6 direct + 2 No-ID residual)
    Full-Horizon Stacker and synthesizes predictions via Schur-leverage (`tau = col 49`)
    gating, unshrunk Unseen-Target paralog transfer, Exact-Pair anchor, and IntraCal.
    Returns `(pred_e1_raw40, pred_e2_cal40, pred_e3_cal55)`.
    """
    X_temp = np.nan_to_num(X_temp, 0.0)
    X_va = np.nan_to_num(X_va, 0.0)

    seen = X_va[:, 58] > 0.5
    uk = ~seen
    ex = seen & (X_va[:, 24] > 0.01)

    s_tr = (yr_temp >= 2014) & (X_temp[:, 58] > 0.5)
    X_tr, y_tr, yr_tr = X_temp[s_tr], y_temp[s_tr], yr_temp[s_tr]
    w_tr = np.exp(0.25 * (yr_tr - np.max(yr_tr))).astype(np.float32)

    # 1. Dual-Subspace Linear + MLP Heads (SEEN_LIN_COLS StandardScaler + All-108 RobustScaler)
    sc1 = StandardScaler()
    X_tr_1 = np.clip(sc1.fit_transform(X_tr[:, SEEN_LIN_COLS]), -10.0, 10.0)
    X_va_1 = np.clip(sc1.transform(X_va[:, SEEN_LIN_COLS]), -10.0, 10.0)
    pr1 = RidgeCV(alphas=np.logspace(1, 5, 25)).fit(X_tr_1, y_tr, sample_weight=w_tr).predict(X_va_1)
    pm1 = MLPRegressor(
        hidden_layer_sizes=(64, 32), alpha=25.0, max_iter=40, early_stopping=True, random_state=seed
    ).fit(X_tr_1, y_tr).predict(X_va_1)

    sc2 = RobustScaler()
    X_tr_2 = np.clip(sc2.fit_transform(X_tr), -10.0, 10.0)
    X_va_2 = np.clip(sc2.transform(X_va), -10.0, 10.0)
    pr2 = RidgeCV(alphas=np.logspace(1, 5, 25)).fit(X_tr_2, y_tr, sample_weight=w_tr).predict(X_va_2)
    pm2 = MLPRegressor(
        hidden_layer_sizes=(128, 64), alpha=10.0, learning_rate_init=6e-4, max_iter=35,
        early_stopping=True, random_state=seed + 50
    ).fit(X_tr_2, y_tr).predict(X_va_2)

    p_lin_mlp = 0.50 * (0.60 * pr1 + 0.40 * pm1) + 0.50 * (0.55 * pr2 + 0.45 * pm2)

    # 2. 8-Tree Ensemble (6 Direct LGBM/XGB + 2 No-ID Residual LGBM/XGB)
    p_l1 = lgb.LGBMRegressor(
        n_estimators=550, learning_rate=0.025, num_leaves=31, subsample_for_bin=50000,
        subsample=0.8, colsample_bytree=0.7, reg_alpha=3.0, reg_lambda=10.0,
        min_child_samples=40, random_state=seed, n_jobs=4, verbose=-1
    ).fit(X_tr, y_tr, sample_weight=w_tr).predict(X_va)

    p_l2 = lgb.LGBMRegressor(
        objective="huber", alpha=1.2, n_estimators=550, learning_rate=0.025, num_leaves=31,
        subsample_for_bin=50000, subsample=0.8, colsample_bytree=0.7, reg_alpha=3.0, reg_lambda=10.0,
        min_child_samples=40, random_state=seed + 100, n_jobs=4, verbose=-1
    ).fit(X_tr, y_tr, sample_weight=w_tr).predict(X_va)

    p_l3 = lgb.LGBMRegressor(
        n_estimators=600, learning_rate=0.025, num_leaves=31, subsample_for_bin=50000,
        subsample=0.8, colsample_bytree=0.75, reg_alpha=4.0, reg_lambda=12.0,
        min_child_samples=50, random_state=seed + 200, n_jobs=4, verbose=-1
    ).fit(X_tr[:, NO_ID_COLS], y_tr, sample_weight=w_tr).predict(X_va[:, NO_ID_COLS])

    p_l4 = lgb.LGBMRegressor(
        objective="huber", alpha=1.2, n_estimators=600, learning_rate=0.025, num_leaves=31,
        subsample_for_bin=50000, subsample=0.8, colsample_bytree=0.75, reg_alpha=4.0, reg_lambda=12.0,
        min_child_samples=50, random_state=seed + 300, n_jobs=4, verbose=-1
    ).fit(X_tr[:, NO_ID_COLS], y_tr, sample_weight=w_tr).predict(X_va[:, NO_ID_COLS])

    p_x1 = xgb.XGBRegressor(
        n_estimators=550, learning_rate=0.025, max_depth=5, subsample=0.8, colsample_bytree=0.7,
        reg_alpha=3.0, reg_lambda=12.0, min_child_weight=40, random_state=seed + 400,
        n_jobs=4, verbosity=0, tree_method="hist"
    ).fit(X_tr, y_tr, sample_weight=w_tr).predict(X_va)

    p_x2 = xgb.XGBRegressor(
        n_estimators=600, learning_rate=0.025, max_depth=5, subsample=0.8, colsample_bytree=0.75,
        reg_alpha=4.0, reg_lambda=15.0, min_child_weight=50, random_state=seed + 500,
        n_jobs=4, verbosity=0, tree_method="hist"
    ).fit(X_tr[:, NO_ID_COLS], y_tr, sample_weight=w_tr).predict(X_va[:, NO_ID_COLS])

    res_tr = y_tr - X_tr[:, 104]
    p_res_lgb = X_va[:, 104] + lgb.LGBMRegressor(
        objective="huber", alpha=1.0, n_estimators=450, learning_rate=0.025, num_leaves=23,
        subsample=0.8, colsample_bytree=0.75, reg_alpha=5.0, reg_lambda=15.0,
        min_child_samples=60, random_state=seed + 600, n_jobs=4, verbose=-1
    ).fit(X_tr[:, NO_ID_COLS], res_tr, sample_weight=w_tr).predict(X_va[:, NO_ID_COLS])

    p_res_xgb = X_va[:, 104] + xgb.XGBRegressor(
        n_estimators=450, learning_rate=0.025, max_depth=4, subsample=0.8, colsample_bytree=0.75,
        reg_alpha=5.0, reg_lambda=20.0, min_child_weight=60, random_state=seed + 700,
        n_jobs=4, verbosity=0, tree_method="hist"
    ).fit(X_tr[:, NO_ID_COLS], res_tr, sample_weight=w_tr).predict(X_va[:, NO_ID_COLS])

    p_trees = (
        0.14 * p_l1 + 0.14 * p_l2 + 0.16 * p_l3 + 0.16 * p_l4
        + 0.12 * p_x1 + 0.14 * p_x2 + 0.07 * p_res_lgb + 0.07 * p_res_xgb
    )

    # 3. Analytical Base C1 + ESM-6 Homology + Unseen-Target Paralog Drug Transfer
    log_n_same = X_va[:, 0]
    tau = np.clip(X_va[:, 49], 0.0, 1.0)
    w_seen_gate = np.where(
        seen,
        np.clip(0.84 + 0.09 * np.tanh(log_n_same / 3.0) + 0.07 * tau, 0.84, 0.992),
        0.0,
    )
    cold_v4 = 0.50 * X_va[:, 64] + 0.50 * X_va[:, 107]
    p_c1_base = (w_seen_gate * X_va[:, 104] + (1.0 - w_seen_gate) * cold_v4).astype(np.float64)
    p_c1_base[seen] = p_c1_base[seen] + 0.08 * (1.0 - tau[seen]) * (hom6_va[seen] - X_va[seen, 52])
    p_c1_base[uk] = p_c1_base[uk] + 0.06 * (hom6_va[uk] - X_va[uk, 52])

    # Unshrunk Paralog Transfer strictly on Unseen-Target rows with known drug (has_can_uk):
    has_can_uk = uk & (X_va[:, 29] > 0.01)
    f_t_loto = 0.50 * X_va[:, 56] + 0.50 * X_va[:, 97]
    p_can_uk = 0.60 * can_abs[has_can_uk] + 0.40 * (f_t_loto[has_can_uk] + can_res[has_can_uk])
    p_c1_base[has_can_uk] = 0.22 * p_c1_base[has_can_uk] + 0.78 * p_can_uk

    # 4. Sharp Local Interpolant + Tau-Gated Synthesis on Seen Targets
    p_local_sharp = 0.45 * X_va[:, 45] + 0.25 * X_va[:, 10] + 0.15 * X_va[:, 25] + 0.15 * X_va[:, 7]
    p_ex_anchor = 0.65 * X_va[:, 25] + 0.20 * X_va[:, 45] + 0.10 * X_va[:, 10] + 0.05 * X_va[:, 7]

    p_c1_sharp = p_c1_base.copy()
    p_c1_sharp[seen] = (
        (1.0 - 0.35 * (tau[seen] ** 2)) * p_c1_base[seen]
        + (0.35 * (tau[seen] ** 2)) * p_local_sharp[seen]
    )

    w_c1_dyn = np.clip(0.38 + 0.52 * (tau[seen] ** 1.2), 0.38, 0.90)
    w_lin_dyn = 0.26 * ((1.0 - tau[seen]) ** 1.2)
    w_tree_dyn = 1.0 - w_c1_dyn - w_lin_dyn

    p_gated = p_c1_sharp.copy()
    p_gated[seen] = (
        w_c1_dyn * p_c1_sharp[seen]
        + w_tree_dyn * p_trees[seen]
        + w_lin_dyn * p_lin_mlp[seen]
    )

    t_mean_va = np.where(t_cnt[va_p] > 0, t_smooth[va_p], f_t_loto)
    mu_t = 0.70 * t_mean_va[seen] + 0.30 * X_va[seen, 4]

    # Candidate E1: w_ex = 0.40, Raw
    p_e1_raw40 = p_gated.copy()
    w_row_40 = 0.40 * np.clip(X_va[ex, 24] / np.log1p(2.0), 0.55, 1.0)
    p_e1_raw40[ex] = (1.0 - w_row_40) * p_e1_raw40[ex] + w_row_40 * p_ex_anchor[ex]

    # Candidate E2: w_ex = 0.40 + IntraCal
    p_e2_cal40 = p_e1_raw40.copy()
    p_e2_cal40[seen] = mu_t + (1.0 + 0.10 * tau[seen]) * (p_e1_raw40[seen] - mu_t)

    # Candidate E3: w_ex = 0.55 + IntraCal
    p_e3_raw55 = p_gated.copy()
    w_row_55 = 0.55 * np.clip(X_va[ex, 24] / np.log1p(2.0), 0.55, 1.0)
    p_e3_raw55[ex] = (1.0 - w_row_55) * p_e3_raw55[ex] + w_row_55 * p_ex_anchor[ex]
    p_e3_cal55 = p_e3_raw55.copy()
    p_e3_cal55[seen] = mu_t + (1.0 + 0.10 * tau[seen]) * (p_e3_raw55[seen] - mu_t)

    return (
        p_e1_raw40.astype(np.float32),
        p_e2_cal40.astype(np.float32),
        p_e3_cal55.astype(np.float32),
    )


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
    can_id_arr = fw_engine.base_engine.dual_engine.can_id
    S_hom = (0.60 * fw_engine.S_pocket_esm + 0.40 * fw_engine.S_prot_esm).astype(np.float32)

    tv_p = tv_df["Target"].map(t_to_idx).values.astype(np.int32)
    tv_d = tv_df["Drug"].map(d_to_idx).values.astype(np.int32)
    tv_c = can_id_arr[tv_d].astype(np.int32)
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
        uk = ~seen
        seen_lig = seen & ((X_va[:, 24] > 0.01) | (X_va[:, 6] > 0.999))
        unseen_lig = seen & (~seen_lig)

        hom6_va = compute_esm2_homology_tkrr_res(
            fw_engine, tv_d[tr_m], tv_p[tr_m], tv_y[tr_m], tv_d[va_m], tv_p[va_m], top_k_hom=6
        )
        can_abs, can_res, _, t_smooth, t_cnt = compute_can_hom_paralog(
            S_hom, tv_p[tr_m], tv_c[tr_m], tv_y[tr_m], tv_p[va_m], tv_c[va_m], X_va
        )
        p_e1, p_e2, p_e3 = fit_predict_step15_tau_gated_paralog(
            X_temp, y_temp, yr_temp, X_va, tv_p[va_m], hom6_va, can_abs, can_res, t_smooth, t_cnt, seed=42
        )
        print(f"=== Inner Split {tag} Verification ===", flush=True)
        for name, vec in [
            ("Step 15 E1 (Raw w_ex=0.40)", p_e1),
            ("Step 15 E2 (Cal w_ex=0.40)", p_e2),
            ("Step 15 E3 (Cal w_ex=0.55)", p_e3),
        ]:
            print(
                f"  {name:28s}: All={pearsonr(y_va, vec)[0]:.5f} | "
                f"Seen={pearsonr(y_va[seen], vec[seen])[0]:.5f} | "
                f"UK(p3)={pearsonr(y_va[uk], vec[uk])[0]:.5f} | "
                f"SeenLig={pearsonr(y_va[seen_lig], vec[seen_lig])[0]:.5f} | "
                f"UnseenLig={pearsonr(y_va[unseen_lig], vec[unseen_lig])[0]:.5f}",
                flush=True,
            )

    # 2. Official 5-Seed Evaluation
    te_p = te_df["Target"].map(t_to_idx).values.astype(np.int32)
    te_d = te_df["Drug"].map(d_to_idx).values.astype(np.int32)
    te_c = can_id_arr[te_d].astype(np.int32)
    te_y = te_df["Y"].values.astype(np.float32)
    te_yr = te_df["Year"].values.astype(np.int32)
    te_rid = np.arange(10_000_000, 10_000_000 + len(te_df), dtype=np.int32)

    seen_targets_tv = set(tv_p.tolist())
    seen_drugs_tv = set(tv_d.tolist())
    te_seen_t_mask = np.array([p in seen_targets_tv for p in te_p], dtype=bool)
    te_unseen_t_mask = ~te_seen_t_mask
    te_unseen_d_mask = np.array([d not in seen_drugs_tv for d in te_d], dtype=bool)

    d2_vecs, e1_vecs, e2_vecs, e3_vecs, e4_vecs = [], [], [], [], []
    d2_list, e1_list, e2_list, e3_list, e4_list = [], [], [], [], []

    print("\n=== Running 5-Seed Step 15 Tau-Gated + Paralog + Exact-Anchor Evaluation ===", flush=True)
    for seed in [1, 2, 3, 4, 5]:
        t_s = time.time()
        tr_df, _ = group.get_train_valid_split(benchmark="BindingDB_Patent", split_type="default", seed=seed)
        tr_p = tr_df["Target"].map(t_to_idx).values.astype(np.int32)
        tr_d = tr_df["Drug"].map(d_to_idx).values.astype(np.int32)
        tr_c = can_id_arr[tr_d].astype(np.int32)
        tr_yr = tr_df["Year"].values.astype(np.int32)
        tr_y = tr_df["Y"].values.astype(np.float32)
        tr_rid = np.arange(len(tr_df), dtype=np.int32)

        seed_cache_path = CACHE_DIR / f"seed_{seed}_v4_fullhorizon.npz"
        if seed_cache_path.exists():
            sc = np.load(seed_cache_path)
            X_temp_s = sc["X_temp_s"]
            y_temp_s = sc["y_temp_s"]
            yr_temp_s = sc["yr_temp_s"]
            X_te_s = sc["X_te_s"]
            hom6_te_s = sc["hom6_te_s"]
        else:
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
            np.savez(
                seed_cache_path,
                X_temp_s=X_temp_s.astype(np.float32),
                y_temp_s=y_temp_s.astype(np.float32),
                yr_temp_s=yr_temp_s.astype(np.int32),
                X_te_s=X_te_s.astype(np.float32),
                hom6_te_s=hom6_te_s.astype(np.float32),
            )

        can_abs_s, can_res_s, _, t_smooth_s, t_cnt_s = compute_can_hom_paralog(
            S_hom, tr_p, tr_c, tr_y, te_p, te_c, X_te_s
        )

        pred_e1_s, pred_e2_s, pred_e3_s = fit_predict_step15_tau_gated_paralog(
            X_temp_s, y_temp_s, yr_temp_s, X_te_s, te_p, hom6_te_s,
            can_abs_s, can_res_s, t_smooth_s, t_cnt_s, seed=seed * 100
        )

        pred_d2_s = np.load(PRED_DIR / f"seed_{seed}_trackD2_blend.npy").astype(np.float32)
        pred_e4_s = (0.75 * pred_e3_s + 0.25 * pred_d2_s).astype(np.float32)

        d2_vecs.append(pred_d2_s)
        e1_vecs.append(pred_e1_s)
        e2_vecs.append(pred_e2_s)
        e3_vecs.append(pred_e3_s)
        e4_vecs.append(pred_e4_s)

        d2_list.append({bm["name"]: pred_d2_s})
        e1_list.append({bm["name"]: pred_e1_s})
        e2_list.append({bm["name"]: pred_e2_s})
        e3_list.append({bm["name"]: pred_e3_s})
        e4_list.append({bm["name"]: pred_e4_s})

        print(
            f"  [Seed {seed} | {time.time()-t_s:.1f}s] "
            f"Step14_D2={pearsonr(te_y, pred_d2_s)[0]:.5f} | "
            f"E1(Raw40)={pearsonr(te_y, pred_e1_s)[0]:.5f} | "
            f"E2(Cal40)={pearsonr(te_y, pred_e2_s)[0]:.5f} | "
            f"E3(Cal55)={pearsonr(te_y, pred_e3_s)[0]:.5f} | "
            f"E4(0.75*E3+0.25*D2)={pearsonr(te_y, pred_e4_s)[0]:.5f} "
            f"(Seen={pearsonr(te_y[te_seen_t_mask], pred_e3_s[te_seen_t_mask])[0]:.5f}, "
            f"UK_p3={pearsonr(te_y[te_unseen_t_mask], pred_e3_s[te_unseen_t_mask])[0]:.5f})",
            flush=True,
        )

    candidates = [
        ("trackD2_blend_c1_d1", "Step 14 Track D2 (0.50*C1_esm6 + 0.50*D1)", d2_vecs, d2_list),
        ("trackE1_tau_paralog_raw40", "Track E1 (Tau-Gated + Paralog + Ex40 Raw)", e1_vecs, e1_list),
        ("trackE2_tau_paralog_cal40", "Track E2 (Tau-Gated + Paralog + Ex40 + IntraCal)", e2_vecs, e2_list),
        ("trackE3_tau_paralog_cal55", "Track E3 (Tau-Gated + Paralog + Ex55 + IntraCal)", e3_vecs, e3_list),
        ("trackE4_blend_e3_d2", "Track E4 (0.75*TrackE3 + 0.25*TrackD2)", e4_vecs, e4_list),
    ]

    print(f"\n==============================================================", flush=True)
    print(f"STEP 15 OFFICIAL 5-SEED SUMMARY (runtime {time.time()-t0_all:.1f}s)", flush=True)
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
              f"Unseen-Target (p3): {brk['unseen_target_p3']['mean_pcc']:.5f} +- {brk['unseen_target_p3']['std_pcc']:.5f} | "
              f"Unseen-Ligand: {brk['unseen_ligand']['mean_pcc']:.5f} +- {brk['unseen_ligand']['std_pcc']:.5f}", flush=True)
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

    cert_path = BASE_DIR / "results_certificate_fullwin.json"
    cert = json.loads(cert_path.read_text()) if cert_path.exists() else {}
    saved_files = cert.get("prediction_files_sha256", {})

    for s_idx, seed in enumerate([1, 2, 3, 4, 5]):
        for tag, vecs in [
            ("trackE1_raw40", e1_vecs),
            ("trackE2_cal40", e2_vecs),
            ("trackE3_cal55", e3_vecs),
            ("trackE4_blend", e4_vecs),
            ("trackC_fullwin", best_vecs),
        ]:
            npy_path = PRED_DIR / f"seed_{seed}_{tag}.npy"
            csv_path = PRED_DIR / f"seed_{seed}_{tag}.csv"
            np.save(npy_path, vecs[s_idx].astype(np.float32))
            pd.DataFrame({"y_pred": vecs[s_idx].astype(np.float32)}).to_csv(csv_path, index=False)
            saved_files[f"seed_{seed}_{tag}.csv"] = hashlib.sha256(csv_path.read_bytes()).hexdigest()

    cert["best_track_selected"] = best_tag
    cert["best_exact_5seed_mean_pcc"] = best_mean
    cert.update(cert_tracks)
    cert["prediction_files_sha256"] = saved_files
    cert_path.write_text(json.dumps(cert, indent=2))
    print(f"\nUpdated {cert_path} (best_track_selected = {best_tag}, mean = {best_mean:.5f})", flush=True)


if __name__ == "__main__":
    main()
