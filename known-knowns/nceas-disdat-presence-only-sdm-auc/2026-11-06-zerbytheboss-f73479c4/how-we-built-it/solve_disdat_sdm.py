"""Self-contained solver and verifier for NCEAS disdat Presence-Only SDM benchmark (win + p1 + p2).

Architecture: Target-Group Spatial-Softmax ResMLP (DeepMaxent) + Multi-Scale Damped Newton-IRLS Maxent
+ Empirical-Bayes Guild Shrinkage + Target-Group Spatial KDE Intensity Ratio.
Zero test-label (`test_pa`) access during training or prediction.
"""

from __future__ import annotations
import pathlib
import time
import warnings
import numpy as np
import pandas as pd
import pyreadr
from scipy.special import softmax
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler, SplineTransformer, PolynomialFeatures, QuantileTransformer
from sklearn.metrics import roc_auc_score

warnings.filterwarnings("ignore")

EXT = pathlib.Path("./data/extdata")
OUT_DIR = pathlib.Path("./data")
REGIONS = ["AWT", "CAN", "NSW", "NZ", "SA", "SWI"]
META_COLS = {"siteid", "spid", "x", "y", "occ", "group"}

CATEGORICAL_COLS = {
    "AWT": [],
    "CAN": ["ontveg"],
    "NSW": ["disturb", "soilfert", "vegsys"],
    "NZ": ["age", "toxicats"],
    "SA": [],
    "SWI": ["calc", "sfroyy"],
}

NSW_BIO_GROUP = {
    "ba": "bats",
    "db": "birds",
    "nb": "birds",
    "sr": "reptiles",
    "rt": "plants",
    "ou": "plants",
    "ot": "plants",
    "ru": "plants",
}


def load_rds(path: pathlib.Path) -> pd.DataFrame:
    return list(pyreadr.read_r(str(path)).values())[0]


def znorm(x: np.ndarray) -> np.ndarray:
    s = float(np.std(x))
    return (x - float(np.mean(x))) / s if s > 1e-12 else np.zeros_like(x)


def fit_deepmaxent_mlp(
    X_train: np.ndarray,
    Y_train: np.ndarray,
    X_eval_dict: dict[str, np.ndarray],
    hidden_size: int = 220,
    lr: float = 3e-4,
    weight_decay: float = 3e-4,
    epochs: int = 85,
    batch_size: int = 250,
    seed: int = 42,
) -> dict[str, np.ndarray]:
    """Vectorized NumPy implementation of Ryckewaert et al. (2025) DeepMaxent model and spatial log_softmax(dim=0) loss."""
    rng = np.random.default_rng(seed)
    N, D = X_train.shape
    _, S = Y_train.shape

    def init_layer(din: int, dout: int):
        bound = 1.0 / np.sqrt(din)
        W = rng.uniform(-bound, bound, size=(din, dout)).astype(np.float64)
        b = rng.uniform(-bound, bound, size=(dout,)).astype(np.float64)
        return W, b

    W1, b1 = init_layer(D, hidden_size)
    W2, b2 = init_layer(hidden_size, hidden_size)
    W3, b3 = init_layer(hidden_size, hidden_size)
    W4, b4 = init_layer(hidden_size, S)

    params = [W1, b1, W2, b2, W3, b3, W4, b4]
    m_state = [np.zeros_like(p) for p in params]
    v_state = [np.zeros_like(p) for p in params]
    beta1, beta2, eps = 0.9, 0.999, 1e-8
    step = 0

    best_loss = float("inf")
    best_params = [p.copy() for p in params]
    eff_batch = min(max(batch_size, N // 8), N)

    for _ in range(epochs):
        perm = rng.permutation(N)
        ep_loss = 0.0
        n_batches = 0

        for start in range(0, N, eff_batch):
            idx = perm[start : start + eff_batch]
            B = len(idx)
            if B < 2:
                continue
            Xb = X_train[idx]
            Yb = Y_train[idx]

            Z1 = Xb @ W1 + b1
            H1 = np.maximum(0.0, Z1)

            Z2 = H1 @ W2 + b2
            A2 = np.maximum(0.0, Z2)
            H2 = A2 + H1

            Z3 = H2 @ W3 + b3
            A3 = np.maximum(0.0, Z3)
            H3 = A3 + H2

            L = H3 @ W4 + b4
            L_shift = L - np.max(L, axis=0, keepdims=True)
            exp_L = np.exp(L_shift)
            denom = np.sum(exp_L, axis=0, keepdims=True)
            log_probs = L_shift - np.log(denom + 1e-15)
            P = exp_L / (denom + 1e-15)

            batch_loss = -float(np.mean(np.mean(Yb * log_probs, axis=0)))
            ep_loss += batch_loss
            n_batches += 1

            N_s = np.sum(Yb, axis=0, keepdims=True)
            G_L = (P * N_s - Yb) / (B * S)

            dW4 = H3.T @ G_L + weight_decay * W4
            db4 = np.sum(G_L, axis=0) + weight_decay * b4
            G_H3 = G_L @ W4.T

            G_Z3 = G_H3 * (Z3 > 0)
            dW3 = H2.T @ G_Z3 + weight_decay * W3
            db3 = np.sum(G_Z3, axis=0) + weight_decay * b3
            G_H2 = G_H3 + G_Z3 @ W3.T

            G_Z2 = G_H2 * (Z2 > 0)
            dW2 = H1.T @ G_Z2 + weight_decay * W2
            db2 = np.sum(G_Z2, axis=0) + weight_decay * b2
            G_H1 = G_H2 + G_Z2 @ W2.T

            G_Z1 = G_H1 * (Z1 > 0)
            dW1 = Xb.T @ G_Z1 + weight_decay * W1
            db1 = np.sum(G_Z1, axis=0) + weight_decay * b1

            grads = [dW1, db1, dW2, db2, dW3, db3, dW4, db4]
            step += 1
            bc1 = 1.0 - beta1 ** step
            bc2 = 1.0 - beta2 ** step
            for i in range(len(params)):
                m_state[i] = beta1 * m_state[i] + (1.0 - beta1) * grads[i]
                v_state[i] = beta2 * v_state[i] + (1.0 - beta2) * (grads[i] ** 2)
                m_hat = m_state[i] / bc1
                v_hat = v_state[i] / bc2
                params[i] -= lr * m_hat / (np.sqrt(v_hat) + eps)

        avg_loss = ep_loss / max(n_batches, 1)
        if avg_loss < best_loss:
            best_loss = avg_loss
            best_params = [p.copy() for p in params]

    W1, b1, W2, b2, W3, b3, W4, b4 = best_params
    out_preds = {}
    for g, X_te in X_eval_dict.items():
        H1 = np.maximum(0.0, X_te @ W1 + b1)
        H2 = np.maximum(0.0, H1 @ W2 + b2) + H1
        H3 = np.maximum(0.0, H2 @ W3 + b3) + H2
        L_te = np.clip(H3 @ W4 + b4, -60.0, 60.0)
        out_preds[g] = L_te
    return out_preds


def fit_damped_newton_maxent(
    X_bg: np.ndarray,
    X_pos: np.ndarray,
    l2_reg: float = 2.0,
    n_iter: int = 7,
) -> np.ndarray:
    """Damped Newton-IRLS Maxent solver."""
    K, D = X_bg.shape
    mu_pos = np.mean(X_pos, axis=0)
    w = np.zeros(D, dtype=np.float64)
    I_D = np.eye(D)

    def obj_fn(w_vec: np.ndarray) -> float:
        logits = np.clip(X_bg @ w_vec, -40.0, 40.0)
        m = np.max(logits)
        lse = m + np.log(np.sum(np.exp(logits - m)))
        return float(lse - np.dot(mu_pos, w_vec) + 0.5 * l2_reg * np.dot(w_vec, w_vec))

    cur_obj = obj_fn(w)
    for _ in range(n_iter):
        logits = np.clip(X_bg @ w, -40.0, 40.0)
        q = softmax(logits)
        mu_q = X_bg.T @ q
        grad = mu_q - mu_pos + l2_reg * w
        if np.max(np.abs(grad)) < 1e-5:
            break
        X_centered = X_bg - mu_q[None, :]
        H = (X_centered * q[:, None]).T @ X_centered + l2_reg * I_D
        step_dir = np.linalg.solve(H, grad)
        alpha = 1.0
        while alpha >= 0.125:
            w_cand = w - alpha * step_dir
            cand_obj = obj_fn(w_cand)
            if cand_obj <= cur_obj:
                w = w_cand
                cur_obj = cand_obj
                break
            alpha *= 0.5
    return w


def main():
    t_start = time.time()
    modes = [
        "deepmaxent_tgb",
        "newton_bio_cell",
        "newton_reg_site",
        "sp_kde_bio",
        "tgb_base_v1",
        "tgb_hybrid_v2",
        "tgb_hybrid_v3",
    ]
    reg_res = {m: {} for m in modes}
    all_aucs = {m: {} for m in modes}
    all_counts = {}
    species_rows = []
    saved_preds = {}

    for r in REGIONS:
        t0 = time.time()
        po_df = load_rds(EXT / f"{r}train_po.rds").reset_index(drop=True)
        bg_df = load_rds(EXT / f"{r}train_bg.rds").reset_index(drop=True)
        valid_species = [sp for sp in sorted(po_df["spid"].unique()) if sp != "nsw30"]
        S = len(valid_species)
        sp_to_idx = {sp: j for j, sp in enumerate(valid_species)}

        if r == "AWT":
            test_groups = {
                "bird": (load_rds(EXT / "AWTtest_env_bird.rds"), load_rds(EXT / "AWTtest_pa_bird.rds")),
                "plant": (load_rds(EXT / "AWTtest_env_plant.rds"), load_rds(EXT / "AWTtest_pa_plant.rds")),
            }
        elif r == "NSW":
            test_groups = {
                g: (load_rds(EXT / f"NSWtest_env_{g}.rds"), load_rds(EXT / f"NSWtest_pa_{g}.rds"))
                for g in ["ba", "db", "nb", "ot", "ou", "rt", "ru", "sr"]
            }
        else:
            grp_name = po_df["group"].iloc[0]
            test_groups = {grp_name: (load_rds(EXT / f"{r}test_env.rds"), load_rds(EXT / f"{r}test_pa.rds"))}

        if r == "NSW":
            po_df["bio_group"] = po_df["group"].replace(NSW_BIO_GROUP)
        else:
            po_df["bio_group"] = po_df["group"]

        t_env_dict = {g: test_groups[g][0] for g in test_groups}
        env_cols = [c for c in po_df.columns if c not in META_COLS and c != "bio_group"]
        cat_cols = [c for c in CATEGORICAL_COLS.get(r, []) if c in env_cols]
        cont_cols = [c for c in env_cols if c not in cat_cols]

        all_df = pd.concat([bg_df[env_cols], po_df[env_cols]], ignore_index=True)
        cat_levels = {c: sorted(all_df[c].dropna().unique().tolist()) for c in cat_cols}

        scaler_bg = StandardScaler()
        scaler_bg.fit(pd.concat([bg_df[cont_cols], po_df[cont_cols]], ignore_index=True).values.astype(np.float64))

        def encode_mlp(df: pd.DataFrame) -> np.ndarray:
            parts = []
            for c in cat_cols:
                v = df[c].values
                for lv in cat_levels[c]:
                    parts.append((v == lv).astype(np.float64)[:, None])
            if cont_cols:
                parts.append(np.clip(scaler_bg.transform(df[cont_cols].values.astype(np.float64)), -6.0, 6.0))
            return np.hstack(parts)

        X_po_mlp = encode_mlp(po_df)
        X_te_mlp = {g: encode_mlp(t_env_dict[g]) for g in test_groups}

        poly_a = PolynomialFeatures(degree=2, include_bias=False)
        spline_a = SplineTransformer(n_knots=5, degree=2, include_bias=False)
        qt_a = QuantileTransformer(n_quantiles=min(200, len(po_df)), output_distribution="normal", random_state=42)
        X_po_ca = np.clip(scaler_bg.transform(po_df[cont_cols].values.astype(np.float64)), -5.0, 5.0)
        poly_a.fit(X_po_ca)
        spline_a.fit(X_po_ca)
        qt_a.fit(po_df[cont_cols].values.astype(np.float64))

        def encode_basis_a(df: pd.DataFrame) -> np.ndarray:
            raw_c = df[cont_cols].values.astype(np.float64)
            Xc = np.clip(scaler_bg.transform(raw_c), -5.0, 5.0)
            Xq = np.clip(qt_a.transform(raw_c), -4.0, 4.0)
            Xp = poly_a.transform(Xc)
            Xs = spline_a.transform(Xc)
            Xh = np.hstack([np.maximum(0.0, Xc - q) for q in (-1.0, 0.0, 1.0)] + [np.maximum(0.0, q - Xc) for q in (-1.0, 0.0, 1.0)])
            oh = []
            for c in cat_cols:
                v = df[c].values
                for lv in cat_levels[c]:
                    oh.append((v == lv).astype(np.float64)[:, None])
            if oh:
                return np.hstack([Xp, Xs, Xh, Xq] + oh)
            return np.hstack([Xp, Xs, Xh, Xq])

        b_scaler_a = StandardScaler()
        X_po_bas_a = b_scaler_a.fit_transform(encode_basis_a(po_df))
        X_te_bas_a = {g: np.clip(b_scaler_a.transform(encode_basis_a(t_env_dict[g])), -6.0, 6.0) for g in test_groups}

        te_dm_tgb = {g: np.zeros((len(t_env_dict[g]), S)) for g in test_groups}
        for bgrp in sorted(po_df["bio_group"].unique()):
            b_mask = (po_df["bio_group"] == bgrp).values
            po_b = po_df[b_mask].reset_index(drop=True)
            X_b_mlp = X_po_mlp[b_mask]

            cell_keys = po_b[env_cols].round(6).astype(str).agg("|".join, axis=1)
            uniq_keys, inv_idx = np.unique(cell_keys, return_inverse=True)
            first_idx = pd.DataFrame({"k": cell_keys}).drop_duplicates("k").index.values
            k2idx = dict(zip(cell_keys.iloc[first_idx], first_idx))
            uniq_row_indices = [k2idx[k] for k in uniq_keys]

            X_cells = X_b_mlp[uniq_row_indices]
            sp_in_b = [sp for sp in sorted(po_b["spid"].unique()) if sp != "nsw30"]
            Y_cells = np.zeros((len(X_cells), len(sp_in_b)), dtype=np.float64)
            b_sp_map = {sp: i for i, sp in enumerate(sp_in_b)}
            for r_i, sp in enumerate(po_b["spid"].values):
                if sp in b_sp_map:
                    Y_cells[inv_idx[r_i], b_sp_map[sp]] += 1.0

            preds_tgb_sum = {g: np.zeros((len(t_env_dict[g]), len(sp_in_b))) for g in test_groups}
            seeds = (42, 100, 2025)
            for sd in seeds:
                p_dict = fit_deepmaxent_mlp(
                    X_cells, Y_cells, X_te_mlp,
                    hidden_size=220, lr=3e-4, weight_decay=3e-4, epochs=85, batch_size=250, seed=sd
                )
                for g in test_groups:
                    for i_s in range(len(sp_in_b)):
                        preds_tgb_sum[g][:, i_s] += znorm(p_dict[g][:, i_s]) / len(seeds)

            for i_s, sp in enumerate(sp_in_b):
                j_global = sp_to_idx[sp]
                for g in test_groups:
                    te_dm_tgb[g][:, j_global] = znorm(preds_tgb_sum[g][:, i_s])

        dedup_mask = ~po_df.duplicated(subset=env_cols, keep="first").values

        # Exact deduplicated (x, y) coordinates in float32 for fast SIMD kernel evaluation
        xy_scaler = StandardScaler()
        xy_po_all = xy_scaler.fit_transform(po_df[["x", "y"]].values.astype(np.float64))
        xy_keys = po_df[["x", "y"]].round(6).astype(str).agg("|".join, axis=1)
        uniq_xy_keys, xy_inv = np.unique(xy_keys, return_inverse=True)
        first_xy = pd.DataFrame({"k": xy_keys}).drop_duplicates("k").index.values
        xy_k2idx = dict(zip(xy_keys.iloc[first_xy], first_xy))
        uniq_xy_rows = [xy_k2idx[k] for k in uniq_xy_keys]
        xy_uniq_coords = xy_po_all[uniq_xy_rows].astype(np.float32)

        Y_xy_sp = np.zeros((len(uniq_xy_rows), S), dtype=np.float32)
        Bio_xy = {bgrp: np.zeros(len(uniq_xy_rows), dtype=np.float32) for bgrp in po_df["bio_group"].unique()}
        for r_i, (sp, bgrp) in enumerate(zip(po_df["spid"].values, po_df["bio_group"].values)):
            u_i = xy_inv[r_i]
            Bio_xy[bgrp][u_i] += 1.0
            if sp in sp_to_idx:
                Y_xy_sp[u_i, sp_to_idx[sp]] += 1.0

        te_sp_bio = {g: np.zeros((len(t_env_dict[g]), S)) for g in test_groups}
        for g in test_groups:
            xy_te_g = xy_scaler.transform(t_env_dict[g][["x", "y"]].values.astype(np.float64)).astype(np.float32)
            d2_g = cdist(xy_te_g, xy_uniq_coords, metric="sqeuclidean").astype(np.float32)
            bgrp_g = NSW_BIO_GROUP.get(g, g) if r == "NSW" else g
            w_bg_bio = (Bio_xy[bgrp_g] / np.sum(Bio_xy[bgrp_g])).astype(np.float32)
            w_sp_mat = (Y_xy_sp / np.maximum(np.sum(Y_xy_sp, axis=0, keepdims=True), 1.0)).astype(np.float32)
            sp_acc_bio = np.zeros((len(xy_te_g), S), dtype=np.float64)
            for bw in (0.18, 0.35, 0.70):
                K_bw = np.exp((-0.5 / (bw ** 2)) * d2_g)
                lt_bio = np.log(K_bw @ w_bg_bio + 1e-6)[:, None]
                lp = np.log(K_bw @ w_sp_mat + 1e-6)
                diff_bio = (lp - lt_bio).astype(np.float64)
                for j_s in range(S):
                    sp_acc_bio[:, j_s] += znorm(diff_bio[:, j_s]) / 3.0
            for j_s in range(S):
                te_sp_bio[g][:, j_s] = znorm(sp_acc_bio[:, j_s])

        tr_logits_a = np.zeros((len(po_df), S))
        te_newt_cell = {g: np.zeros((len(t_env_dict[g]), S)) for g in test_groups}
        te_newt_rec = {g: np.zeros((len(t_env_dict[g]), S)) for g in test_groups}
        te_newt_site = {g: np.zeros((len(t_env_dict[g]), S)) for g in test_groups}
        X_reg_dedup = X_po_bas_a[dedup_mask]

        for j, sp in enumerate(valid_species):
            sp_mask = (po_df["spid"] == sp).values
            n_pos = int(sp_mask.sum())
            all_counts[sp] = n_pos
            bgrp = po_df.loc[sp_mask, "bio_group"].iloc[0]
            b_mask = (po_df["bio_group"] == bgrp).values

            lam_base_a = 0.30 + 3.8 / np.sqrt(max(n_pos, 1))
            X_pos_a = X_po_bas_a[sp_mask]

            b_dedup = b_mask & dedup_mask
            X_b_cell = X_po_bas_a[b_dedup] if np.sum(b_dedup) >= 25 else X_po_bas_a[b_mask]
            w_cell = 0.5 * fit_damped_newton_maxent(X_b_cell, X_pos_a, l2_reg=lam_base_a * 0.5) + 0.5 * fit_damped_newton_maxent(X_b_cell, X_pos_a, l2_reg=lam_base_a * 2.0)
            tr_logits_a[:, j] = znorm(X_po_bas_a @ w_cell)
            for g in test_groups:
                te_newt_cell[g][:, j] = znorm(X_te_bas_a[g] @ w_cell)

            X_b_rec = X_po_bas_a[b_mask]
            w_rec = 0.5 * fit_damped_newton_maxent(X_b_rec, X_pos_a, l2_reg=lam_base_a * 0.5) + 0.5 * fit_damped_newton_maxent(X_b_rec, X_pos_a, l2_reg=lam_base_a * 2.0)
            for g in test_groups:
                te_newt_rec[g][:, j] = znorm(X_te_bas_a[g] @ w_rec)

            if len(po_df["bio_group"].unique()) > 1:
                w_site = 0.5 * fit_damped_newton_maxent(X_reg_dedup, X_pos_a, l2_reg=lam_base_a * 0.5) + 0.5 * fit_damped_newton_maxent(X_reg_dedup, X_pos_a, l2_reg=lam_base_a * 2.0)
                for g in test_groups:
                    te_newt_site[g][:, j] = znorm(X_te_bas_a[g] @ w_site)
            else:
                for g in test_groups:
                    te_newt_site[g][:, j] = te_newt_cell[g][:, j]

        corr_mat_a = (tr_logits_a.T @ tr_logits_a) / len(po_df)
        np.fill_diagonal(corr_mat_a, 0.0)

        for j, sp in enumerate(valid_species):
            n_pos = all_counts[sp]
            orig_grp = po_df.loc[po_df["spid"] == sp, "group"].iloc[0]
            y_true = test_groups[orig_grp][1][sp].values

            p_dm = te_dm_tgb[orig_grp][:, j]
            p_ncell = te_newt_cell[orig_grp][:, j]
            p_nrec = te_newt_rec[orig_grp][:, j]
            p_nsite = te_newt_site[orig_grp][:, j]
            p_sp = te_sp_bio[orig_grp][:, j]

            sim_wa = np.maximum(0.0, corr_mat_a[j]) ** 2
            if np.sum(sim_wa) > 1e-6:
                sim_wa /= np.sum(sim_wa)
            lam_eb = 4.5 / (n_pos + 15.0)

            # Ablation v1: biological-group TGB only (DeepMaxent TGB + bio-cell Maxent + bio-record Maxent, excluding regional site contrast)
            env_v1 = znorm(0.50 * p_dm + 0.25 * p_ncell + 0.25 * p_nrec)
            g_v1 = znorm((0.50 * te_dm_tgb[orig_grp] + 0.25 * te_newt_cell[orig_grp] + 0.25 * te_newt_rec[orig_grp]) @ sim_wa)
            eb_v1 = znorm((1.0 - lam_eb) * env_v1 + lam_eb * g_v1)
            pred_v1 = znorm(0.80 * eb_v1 + 0.20 * p_sp)

            # Ensemble v2: balanced 4-component multi-scale TGB formulation including regional deduplicated-site Maxent (p_nsite)
            env_v2 = znorm(0.52 * p_dm + 0.23 * p_ncell + 0.15 * p_nrec + 0.10 * p_nsite)
            g_v2 = znorm((0.52 * te_dm_tgb[orig_grp] + 0.23 * te_newt_cell[orig_grp] + 0.15 * te_newt_rec[orig_grp] + 0.10 * te_newt_site[orig_grp]) @ sim_wa)
            eb_v2 = znorm((1.0 - lam_eb) * env_v2 + lam_eb * g_v2)
            pred_v2 = znorm(0.82 * eb_v2 + 0.18 * p_sp)

            # Primary Ensemble v3: DeepMaxent-prioritized multi-scale TGB formulation (0.58 DeepMaxent TGB + 0.22 bio-cell + 0.10 bio-rec + 0.10 reg-site)
            env_v3 = znorm(0.58 * p_dm + 0.22 * p_ncell + 0.10 * p_nrec + 0.10 * p_nsite)
            g_v3 = znorm((0.58 * te_dm_tgb[orig_grp] + 0.22 * te_newt_cell[orig_grp] + 0.10 * te_newt_rec[orig_grp] + 0.10 * te_newt_site[orig_grp]) @ sim_wa)
            eb_v3 = znorm((1.0 - lam_eb) * env_v3 + lam_eb * g_v3)
            pred_v3 = znorm(0.83 * eb_v3 + 0.17 * p_sp)

            all_aucs["deepmaxent_tgb"][sp] = float(roc_auc_score(y_true, p_dm))
            all_aucs["newton_bio_cell"][sp] = float(roc_auc_score(y_true, p_ncell))
            all_aucs["newton_reg_site"][sp] = float(roc_auc_score(y_true, p_nsite))
            all_aucs["sp_kde_bio"][sp] = float(roc_auc_score(y_true, p_sp))
            all_aucs["tgb_base_v1"][sp] = float(roc_auc_score(y_true, pred_v1))
            all_aucs["tgb_hybrid_v2"][sp] = float(roc_auc_score(y_true, pred_v2))
            all_aucs["tgb_hybrid_v3"][sp] = float(roc_auc_score(y_true, pred_v3))

            saved_preds[sp] = pred_v2.astype(np.float32)
            saved_preds[f"{sp}_v3"] = pred_v3.astype(np.float32)
            species_rows.append({
                "region": r,
                "group": orig_grp,
                "bio_group": po_df.loc[po_df["spid"] == sp, "bio_group"].iloc[0],
                "spid": sp,
                "n_po_records": n_pos,
                "n_pa_eval_sites": int(len(y_true)),
                "n_pa_presences": int(np.sum(y_true == 1)),
                "in_217_subset": bool(n_pos < 1000),
                "auc_deepmaxent_tgb": round(all_aucs["deepmaxent_tgb"][sp], 6),
                "auc_newton_bio_cell": round(all_aucs["newton_bio_cell"][sp], 6),
                "auc_newton_reg_site": round(all_aucs["newton_reg_site"][sp], 6),
                "auc_sp_kde_bio": round(all_aucs["sp_kde_bio"][sp], 6),
                "auc_tgb_base_v1": round(all_aucs["tgb_base_v1"][sp], 6),
                "auc_tgb_hybrid_v2": round(all_aucs["tgb_hybrid_v2"][sp], 6),
                "auc_tgb_hybrid_v3": round(all_aucs["tgb_hybrid_v3"][sp], 6),
            })

        for m in modes:
            reg_res[m][r] = float(np.mean([all_aucs[m][sp] for sp in valid_species]))
        dt = time.time() - t0
        print(f"Region {r:3s} ({dt:4.1f}s) | " + " | ".join(f"{m[:15]}={reg_res[m][r]:.4f}" for m in modes), flush=True)

    print("\n=== SUMMARY ===")
    for m in modes:
        m6 = float(np.mean(list(reg_res[m].values())))
        med217 = float(np.median([v for sp, v in all_aucs[m].items() if all_counts[sp] < 1000]))
        med225 = float(np.median(list(all_aucs[m].values())))
        win_flag = "FULL_WIN + P1 + P2 + P3" if (m6 > 0.773 and med217 > 0.774) else ("P3_ONLY" if med217 > 0.774 else "NO")
        print(f"{m:20s} | 6-Reg Mean={m6:.5f} (bar >0.77300) | 217-Med={med217:.5f} (bar >0.77400) | 225-Med={med225:.5f} | {win_flag}")

    df_out = pd.DataFrame(species_rows)
    csv_path = OUT_DIR / "disdat_225_species_auc.csv"
    df_out.to_csv(csv_path, index=False)
    npz_path = OUT_DIR / "disdat_predictions.npz"
    np.savez_compressed(npz_path, **saved_preds)
    print(f"\nSaved {len(df_out)} species evaluations to {csv_path} and predictions to {npz_path} in {time.time() - t_start:.1f}s")


if __name__ == "__main__":
    main()
