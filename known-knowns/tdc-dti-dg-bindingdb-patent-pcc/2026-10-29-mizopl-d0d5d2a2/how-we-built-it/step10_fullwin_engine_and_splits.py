#!/usr/bin/env python3
"""
Step 10: Full-Win Engine (`Track C`) — Bayesian Patent-Series Shrinkage (`Op-M1 + Op-M6`)
+ 552x176 Frozen ESM-2 Factored Bilinear Kronecker Ridge (`Op-M2 + Op-M5`)
+ ESM-2 Enhanced Pocket-LOTO Target-KRR (`Op-M3`)
+ Schur-Augmented Two-Regime Ensemble on Inner Temporal Splits A & B (`L-TDDB-009`).
"""
import os
os.environ["NUMBA_THREADING_LAYER"] = "workqueue"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import time
from pathlib import Path
import numpy as np
from scipy.sparse.linalg import LinearOperator, cg
from scipy.stats import pearsonr
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler, normalize
from tdc.benchmark_group import dti_dg_group

from step06_test_universal_kriging_and_unseen import (
    unpack_bits_u8_to_f32,
    fast_bilinear_matvec_numba,
    fast_bilinear_rhs_numba,
)
from step07_test_full_modular_stack_splits import (
    UnifiedDTIDGFeatureEngine,
    fit_predict_pocket_loto_krr_v3,
    fit_predict_two_regime_ensemble_v3,
    BASE_DIR,
    DATA_DIR,
    CACHE_DIR,
)


class FullWinDTIDGEngine:
    """
    Extends UnifiedDTIDGFeatureEngine (97 columns) with 11 high-signal columns (cols 97..107):
      97: f_target_loto_esm (ESM-2 + Pocket LOTO Target-KRR)
      98: q_lig_res_800 (4328D Target-Centered Ligand CG Ridge, lambda=800)
      99: q_lig_raw_800 (4328D Uncentered Ligand CG Ridge, lambda=800)
     100: q_bilin_res_552_esm (552x176 ESM-2 Kronecker Bilinear Ridge on double residuals)
     101: q_bilin_raw_552_esm (552x176 ESM-2 Kronecker Bilinear Ridge on raw centered Y)
     102: L_loc_bayesian (Local high-leverage TKRR + kNN interpolant)
     103: G_glob_bayesian (Bayesian Patent-Series Out-of-Scaffold Prior)
     104: y_seen_bayesian_ana (w(tau)*L_loc + (1-w(tau))*G_glob)
     105: w_times_L_loc (Schur-gated local basis)
     106: one_minus_w_times_G_glob (Schur-gated global basis)
     107: unseen_analytical_esm (ESM-2 + 4328D Centered Analytical Cold Specialist)
    """
    def __init__(self, cache_dir: Path, base_engine: UnifiedDTIDGFeatureEngine = None):
        t0 = time.time()
        self.cache_dir = cache_dir
        self.base_engine = base_engine if base_engine is not None else UnifiedDTIDGFeatureEngine(cache_dir)
        self.targets = self.base_engine.targets
        self.smiles = self.base_engine.smiles
        self.n_prots = self.base_engine.n_prots
        self.n_drugs = self.base_engine.n_drugs

        esm_npz = np.load(cache_dir / "protein_esm2.npz", allow_pickle=True)
        self.S_esm2_pocket = (np.maximum(0.0, esm_npz["S_esm2_pocket"].astype(np.float32)) ** 2).astype(np.float32)
        self.S_esm2_cos = (np.maximum(0.0, esm_npz["S_esm2_cos"].astype(np.float32)) ** 2).astype(np.float32)
        self.V_esm2_64 = (esm_npz["V_esm2_96"][:, :64].astype(np.float32) * 0.75).astype(np.float32)

        self.S_pocket_esm = (0.85 * self.base_engine.S_pocket + 0.15 * self.S_esm2_pocket).astype(np.float32)
        self.S_prot_esm = (0.75 * self.base_engine.S_prot + 0.25 * self.S_esm2_cos).astype(np.float32)
        self.V_prot_176 = np.hstack([self.base_engine.V_prot_all, self.V_esm2_64]).astype(np.float32)

        rng = np.random.default_rng(108)
        proj_512 = rng.standard_normal((self.base_engine.X_lig_all.shape[1], 512), dtype=np.float32) / np.sqrt(512.0)
        self.U_lig_552 = np.hstack([
            self.base_engine.X_lig_all @ proj_512,
            self.base_engine.mol_desc_std * 0.35,
        ]).astype(np.float32)
        print(f"Initialized FullWinDTIDGEngine (552x176 ESM-2 Bilinear) in {time.time()-t0:.2f}s", flush=True)

    def compute_extra_columns_from_base(
        self,
        X_base: np.ndarray,
        tr_d: np.ndarray,
        tr_p: np.ndarray,
        tr_yr: np.ndarray,
        tr_y: np.ndarray,
        q_d: np.ndarray,
        q_p: np.ndarray,
    ) -> np.ndarray:
        g_mean = float(np.mean(tr_y))

        # 1. ESM-2 Enhanced Pocket-LOTO Target-KRR
        _, f_target_loto_esm, emp_target_mean_esm, _ = fit_predict_pocket_loto_krr_v3(
            tr_p, tr_y,
            self.S_prot_esm,
            self.base_engine.S_kmer,
            self.base_engine.S_sw,
            self.base_engine.S_contain,
            self.S_pocket_esm,
            self.base_engine.prot_feats_norm,
            g_mean,
        )

        # 2. 4328D Ligand CG Ridge (lambda = 800.0 for smoother cross-year generalization)
        tr_y_res = (tr_y - emp_target_mean_esm[tr_p]).astype(np.float32)
        tr_y_raw_c = (tr_y - g_mean).astype(np.float32)

        uniq_d, inv_d = np.unique(tr_d, return_inverse=True)
        cnt_d = np.bincount(inv_d).astype(np.float32)
        mean_res_d = (np.bincount(inv_d, weights=tr_y_res) / cnt_d).astype(np.float32)
        mean_raw_d = (np.bincount(inv_d, weights=tr_y_raw_c) / cnt_d).astype(np.float32)
        w_d = np.sqrt(cnt_d)
        X_u = self.base_engine.X_lig_all[uniq_d]
        d_lig = self.base_engine.X_lig_all.shape[1]

        def matvec_lig_800(v):
            v32 = v.astype(np.float32)
            return (X_u.T @ (w_d * (X_u @ v32)) + 800.0 * v32).astype(np.float64)

        A_lig = LinearOperator((d_lig, d_lig), matvec=matvec_lig_800, dtype=np.float64)
        w_lig_res_800, _ = cg(A_lig, (X_u.T @ (w_d * mean_res_d)).astype(np.float64), maxiter=22, rtol=1e-3)
        w_lig_raw_800, _ = cg(A_lig, (X_u.T @ (w_d * mean_raw_d)).astype(np.float64), maxiter=22, rtol=1e-3)

        q_lig_res_800 = (self.base_engine.X_lig_all[q_d] @ w_lig_res_800.astype(np.float32)).astype(np.float32)
        q_lig_raw_800 = g_mean + (self.base_engine.X_lig_all[q_d] @ w_lig_raw_800.astype(np.float32)).astype(np.float32)
        tr_lig_res_800 = (self.base_engine.X_lig_all[tr_d] @ w_lig_res_800.astype(np.float32)).astype(np.float32)

        # 3. 552x176 ESM-2 Factored Bilinear Kronecker Ridge (Centered & Uncentered)
        double_res = (tr_y_res - 0.70 * tr_lig_res_800).astype(np.float32)
        d_u = self.U_lig_552.shape[1]
        d_v = self.V_prot_176.shape[1]

        p_order = np.argsort(tr_p, kind="mergesort")
        p_sorted = tr_p[p_order]
        U_sorted = np.ascontiguousarray(self.U_lig_552[tr_d[p_order]])
        r_res_sorted = np.ascontiguousarray(double_res[p_order])
        r_raw_sorted = np.ascontiguousarray(tr_y_raw_c[p_order])
        p_starts = np.searchsorted(p_sorted, np.arange(self.n_prots), side="left").astype(np.int32)
        p_ends = np.searchsorted(p_sorted, np.arange(self.n_prots), side="right").astype(np.int32)

        def matvec_bilin_552(w_flat):
            W = w_flat.reshape(d_u, d_v).astype(np.float32)
            M = np.ascontiguousarray(W @ self.V_prot_176.T)
            G_mat = fast_bilinear_matvec_numba(M, U_sorted, p_starts, p_ends)
            grad = G_mat @ self.V_prot_176 + 1000.0 * W
            return grad.ravel().astype(np.float64)

        A_bilin = LinearOperator((d_u * d_v, d_u * d_v), matvec=matvec_bilin_552, dtype=np.float64)

        G_rhs_res = fast_bilinear_rhs_numba(U_sorted, r_res_sorted, p_starts, p_ends, self.n_prots)
        w_b_res, _ = cg(A_bilin, (G_rhs_res @ self.V_prot_176).ravel().astype(np.float64), maxiter=18, rtol=2e-3)
        M_b_res = w_b_res.reshape(d_u, d_v).astype(np.float32) @ self.V_prot_176.T
        q_bilin_res_552 = np.sum(self.U_lig_552[q_d] * M_b_res[:, q_p].T, axis=1).astype(np.float32)

        G_rhs_raw = fast_bilinear_rhs_numba(U_sorted, r_raw_sorted, p_starts, p_ends, self.n_prots)
        w_b_raw, _ = cg(A_bilin, (G_rhs_raw @ self.V_prot_176).ravel().astype(np.float64), maxiter=18, rtol=2e-3)
        M_b_raw = w_b_raw.reshape(d_u, d_v).astype(np.float32) @ self.V_prot_176.T
        q_bilin_raw_552 = g_mean + np.sum(self.U_lig_552[q_d] * M_b_raw[:, q_p].T, axis=1).astype(np.float32)

        # 4. Bayesian Patent-Series Shrinkage Law (Op-M1 + Op-M6)
        Xb = np.nan_to_num(X_base, 0.0)
        tau = np.clip(Xb[:, 49], 0.0, 1.0)

        L_loc_bayesian = (
            0.38 * Xb[:, 45]   # TKRR K2
            + 0.24 * Xb[:, 46] # TKRR Mix
            + 0.18 * Xb[:, 47] # TKRR Rec
            + 0.12 * Xb[:, 10] # knn_p12
            + 0.08 * Xb[:, 18] # oos_knn_p12
        ).astype(np.float32)

        G_glob_bayesian = (
            0.50 * Xb[:, 48]          # TKRR UK
            + 0.22 * q_bilin_raw_552  # 552x176 ESM-2 Bilinear Raw
            + 0.14 * Xb[:, 62]        # 232x112 Bilinear Raw
            + 0.08 * (0.5 * Xb[:, 60] + 0.5 * q_lig_raw_800)
            + 0.06 * (Xb[:, 35] + 0.5 * Xb[:, 59] + 0.5 * q_bilin_res_552)
        ).astype(np.float32)

        w_tau = np.clip(tau ** 0.65, 0.0, 1.0).astype(np.float32)
        w_times_L_loc = (w_tau * L_loc_bayesian).astype(np.float32)
        one_minus_w_times_G_glob = ((1.0 - w_tau) * G_glob_bayesian).astype(np.float32)
        y_seen_bayesian_ana = (w_times_L_loc + one_minus_w_times_G_glob).astype(np.float32)

        # 5. ESM-2 + 4328D Centered Analytical Cold Specialist (col 107)
        q_loto_blend = 0.72 * Xb[:, 56] + 0.28 * f_target_loto_esm[q_p]
        q_lig_res_blend = 0.55 * Xb[:, 59] + 0.45 * q_lig_res_800
        q_bilin_res_blend = 0.50 * Xb[:, 61] + 0.50 * q_bilin_res_552
        unseen_analytical_esm = (
            q_loto_blend
            + 0.56 * q_lig_res_blend
            + 0.24 * q_bilin_res_blend
            + 0.12 * Xb[:, 31]  # global_can_resid
            + 0.08 * Xb[:, 43]  # glob_knn_res8
            + 0.12 * Xb[:, 52]  # pred_hom_res
        ).astype(np.float32)

        extra = np.column_stack([
            f_target_loto_esm[q_p],    # 97
            q_lig_res_800,             # 98
            q_lig_raw_800,             # 99
            q_bilin_res_552,           # 100
            q_bilin_raw_552,           # 101
            L_loc_bayesian,            # 102
            G_glob_bayesian,           # 103
            y_seen_bayesian_ana,       # 104
            w_times_L_loc,             # 105
            one_minus_w_times_G_glob,  # 106
            unseen_analytical_esm,     # 107
        ]).astype(np.float32)
        return np.hstack([Xb, extra]).astype(np.float32)

    def extract_all_features_v4(
        self,
        tr_d: np.ndarray,
        tr_p: np.ndarray,
        tr_yr: np.ndarray,
        tr_y: np.ndarray,
        tr_rid: np.ndarray,
        q_d: np.ndarray,
        q_p: np.ndarray,
        q_yr: np.ndarray,
        q_rid: np.ndarray,
    ) -> np.ndarray:
        X_base = self.base_engine.extract_all_features(
            tr_d, tr_p, tr_yr, tr_y, tr_rid,
            q_d, q_p, q_yr, q_rid,
        )
        return self.compute_extra_columns_from_base(X_base, tr_d, tr_p, tr_yr, tr_y, q_d, q_p)


def augment_cached_temporal_oof(
    fw_engine: FullWinDTIDGEngine,
    X_temp_base: np.ndarray,
    tr_d: np.ndarray,
    tr_p: np.ndarray,
    tr_yr: np.ndarray,
    tr_y: np.ndarray,
) -> np.ndarray:
    years = sorted(np.unique(tr_yr).tolist())
    rows_out = []
    offset = 0
    for yr in years[1:]:
        hist_mask = tr_yr < yr
        curr_mask = tr_yr == yr
        n_curr = int(np.sum(curr_mask))
        if np.sum(hist_mask) < 500 or n_curr < 100:
            continue
        X_slice = X_temp_base[offset: offset + n_curr]
        offset += n_curr
        X_aug = fw_engine.compute_extra_columns_from_base(
            X_slice,
            tr_d[hist_mask], tr_p[hist_mask], tr_yr[hist_mask], tr_y[hist_mask],
            tr_d[curr_mask], tr_p[curr_mask],
        )
        rows_out.append(X_aug)
    assert offset == X_temp_base.shape[0], f"Offset mismatch: {offset} != {X_temp_base.shape[0]}"
    return np.vstack(rows_out).astype(np.float32)


def fit_predict_fullwin_ensemble_v4(
    X_temp: np.ndarray,
    y_temp: np.ndarray,
    yr_temp: np.ndarray,
    X_va: np.ndarray,
    seed: int = 42,
):
    import lightgbm as lgb
    import xgboost as xgb

    seen_temp_mask = X_temp[:, 58] > 0.5
    X_seen_tr = np.nan_to_num(X_temp[seen_temp_mask], 0.0)
    y_seen_tr = y_temp[seen_temp_mask]
    yr_seen_tr = yr_temp[seen_temp_mask]
    w_seen = np.exp(0.25 * (yr_seen_tr - np.max(yr_seen_tr))).astype(np.float32)

    # Residual around Analytical Bayesian Patent-Series Shrinkage Anchor (col 104)
    res_tr = (y_seen_tr - X_seen_tr[:, 104]).astype(np.float32)

    m_res1 = lgb.LGBMRegressor(
        objective="regression",
        n_estimators=380,
        learning_rate=0.02,
        num_leaves=15,
        max_depth=4,
        min_child_samples=100,
        subsample=0.8,
        colsample_bytree=0.70,
        reg_alpha=10.0,
        reg_lambda=50.0,
        random_state=seed,
        n_jobs=1,
        verbose=-1,
    )
    m_res1.fit(X_seen_tr, res_tr, sample_weight=w_seen)

    m_res2 = lgb.LGBMRegressor(
        objective="huber",
        alpha=1.30,
        n_estimators=380,
        learning_rate=0.02,
        num_leaves=15,
        max_depth=4,
        min_child_samples=100,
        subsample=0.8,
        colsample_bytree=0.70,
        reg_alpha=12.0,
        reg_lambda=60.0,
        random_state=seed + 100,
        n_jobs=1,
        verbose=-1,
    )
    m_res2.fit(X_seen_tr, res_tr, sample_weight=w_seen)

    m_xgb = xgb.XGBRegressor(
        n_estimators=320,
        learning_rate=0.02,
        max_depth=4,
        min_child_weight=100,
        subsample=0.8,
        colsample_bytree=0.70,
        reg_alpha=10.0,
        reg_lambda=50.0,
        random_state=seed + 200,
        n_jobs=1,
        verbosity=0,
    )
    m_xgb.fit(X_seen_tr, res_tr, sample_weight=w_seen)

    X_va_clean = np.nan_to_num(X_va, 0.0)
    d1 = m_res1.predict(X_va_clean)
    d2 = m_res2.predict(X_va_clean)
    d3 = m_xgb.predict(X_va_clean)
    delta_res = 0.40 * d1 + 0.30 * d2 + 0.30 * d3

    # Analytical Bayesian Patent-Series Shrinkage Predictor (col 104)
    pred_seen_bayesian = X_va_clean[:, 104]
    pred_seen = pred_seen_bayesian + 0.38 * delta_res

    # Analytical Target-Centered ESM-2 Cold Specialist (50/50 blend of col 64 & col 107)
    pred_cold = 0.50 * X_va_clean[:, 64] + 0.50 * X_va_clean[:, 107]

    log_n_same = X_va_clean[:, 0]
    tau_same = X_va_clean[:, 49]
    seen_flag = X_va_clean[:, 58]

    w_seen_gate = np.where(
        seen_flag > 0.5,
        np.clip(0.84 + 0.09 * np.tanh(log_n_same / 3.0) + 0.07 * tau_same, 0.84, 0.992),
        0.0,
    )
    pred_final = w_seen_gate * pred_seen + (1.0 - w_seen_gate) * pred_cold
    pred_bayesian_only = w_seen_gate * pred_seen_bayesian + (1.0 - w_seen_gate) * pred_cold
    return pred_final, pred_seen, pred_cold, pred_bayesian_only, delta_res


def main():
    t0_all = time.time()
    group = dti_dg_group(path=str(DATA_DIR))
    bm = group.get("BindingDB_Patent")
    tv = bm["train_val"].copy()

    fw_engine = FullWinDTIDGEngine(CACHE_DIR)
    t_to_idx = {t: i for i, t in enumerate(fw_engine.targets)}
    d_to_idx = {s: i for i, s in enumerate(fw_engine.smiles)}

    tv_p = tv["Target"].map(t_to_idx).values.astype(np.int32)
    tv_d = tv["Drug"].map(d_to_idx).values.astype(np.int32)
    tv_y = tv["Y"].values.astype(np.float32)
    tv_yr = tv["Year"].values.astype(np.int32)

    cache_v3 = dict(np.load(CACHE_DIR / "inner_splits_v3.npz"))

    for tag, name, cut_yr in [
        ("A", "Inner Temporal A (2013-2016 -> 2017-2018)", 2016),
        ("B", "Inner Temporal B (2013-2017 -> 2018)", 2017),
    ]:
        t0 = time.time()
        tr_m = tv_yr <= cut_yr
        va_m = tv_yr > cut_yr

        X_temp_v3 = cache_v3[f"X_temp_{tag}"]
        y_temp = cache_v3[f"y_temp_{tag}"]
        yr_temp = cache_v3[f"yr_temp_{tag}"]
        X_va_v3 = cache_v3[f"X_va_{tag}"]
        va_y = cache_v3[f"y_va_{tag}"]

        X_temp_v4 = augment_cached_temporal_oof(
            fw_engine, X_temp_v3,
            tv_d[tr_m], tv_p[tr_m], tv_yr[tr_m], tv_y[tr_m],
        )
        X_va_v4 = fw_engine.compute_extra_columns_from_base(
            X_va_v3,
            tv_d[tr_m], tv_p[tr_m], tv_yr[tr_m], tv_y[tr_m],
            tv_d[va_m], tv_p[va_m],
        )
        t_aug = time.time() - t0

        pred_v3, seen_v3, cold_v3, _, _ = fit_predict_two_regime_ensemble_v3(
            X_temp_v3, y_temp, yr_temp, X_va_v3, seed=42
        )
        pred_v4, seen_v4, cold_v4, bayes_v4, ridge_v4 = fit_predict_fullwin_ensemble_v4(
            X_temp_v4, y_temp, yr_temp, X_va_v4, seed=42
        )

        seen_mask = X_va_v4[:, 58] > 0.5
        unseen_mask = ~seen_mask

        print(f"\n=== {name} (augmented in {t_aug:.2f}s, total {time.time()-t0:.2f}s) ===", flush=True)
        for lbl, vec in [
            ("Step 7/8 Baseline (v3 Stacker)", pred_v3),
            ("Step 10 Bayesian Patent-Shrinkage Only", np.where(seen_mask, bayes_v4, cold_v4)),
            ("Step 10 Seen-Ridge + ESM2 Cold", np.where(seen_mask, ridge_v4, cold_v4)),
            ("Step 10 Full-Win Ensemble (v4)", pred_v4),
        ]:
            p_all = pearsonr(va_y, vec)[0]
            p_seen = pearsonr(va_y[seen_mask], vec[seen_mask])[0]
            p_unseen = pearsonr(va_y[unseen_mask], vec[unseen_mask])[0]
            print(f"  {lbl:40s}: All PCC = {p_all:.5f} | Seen PCC = {p_seen:.5f} | Unseen PCC = {p_unseen:.5f}", flush=True)


if __name__ == "__main__":
    main()
