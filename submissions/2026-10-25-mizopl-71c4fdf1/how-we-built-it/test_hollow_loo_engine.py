#!/usr/bin/env python3
"""
Test the Hollow / Leave-One-Out (LOO) Multi-Channel Resolvent + Shrinkage Bilinear + Cis-Attenuation Engine
strictly fitted on `train` perturbations of each split.
"""
import os
import json
import time
import numpy as np
import pandas as pd
import reproduce_baselines as rb
import lens1_lens2_engine as eng

DATA_DIR = "../data"
GEARS_DIR = os.path.join(DATA_DIR, "gears_pert_data")

panel_a = pd.read_excel(os.path.join(DATA_DIR, "single_perturbation_prediction.xlsx"), sheet_name="Panel A")
panel_c = pd.read_excel(os.path.join(DATA_DIR, "single_perturbation_prediction.xlsx"), sheet_name="Panel C")

pert_names = rb.load_pert_names()
go_genes, g2go_idx, S_go_idf, S_go_jaccard = eng.build_go_idf_features(pert_names)


def fit_predict_hollow_loo_dual_lens(
    X_mean,
    counts,
    gene_names,
    uniq_conds,
    clean_conds,
    set2conditions,
    g2go_idx,
    S_go_idf,
    S_go_jaccard,
):
    """
    100% Zero-Leakage Hollow / Leave-One-Out (LOO) Dual-Lens Predictor:
      - Fitted exclusively on `set2conditions['train']`
      - Every hyper-weight (channel stacking weights, shrinkage scales, cis-attenuation coefficients)
        is learned in closed form via Leave-One-Out (hollow) cross-validation on `train`!
    """
    valid_set = set()
    cond_to_split = {}
    for sp_name, clist in set2conditions.items():
        for c in clist:
            valid_set.add(c)
            cond_to_split[c] = sp_name
    if "ctrl" not in valid_set:
        valid_set.add("ctrl")
        cond_to_split["ctrl"] = "train"

    keep_mask = np.array([c in valid_set for c in uniq_conds])
    X_psce = X_mean[:, keep_mask]
    counts_psce = counts[keep_mask]
    conds_psce = uniq_conds[keep_mask]
    clean_psce = clean_conds[keep_mask]
    splits_psce = np.array([cond_to_split[c] for c in conds_psce])

    ctrl_idx = np.where(conds_psce == "ctrl")[0][0]
    baseline = X_psce[:, ctrl_idx]
    change_psce = X_psce - baseline[:, None]

    # Top 1000 expressed genes in ctrl (used to weight the LOO stacking regression on train)
    top1000_idx = np.argsort(-baseline, kind="mergesort")[:1000]

    train_mask = splits_psce == "train"
    train_change = change_psce[:, train_mask].copy()
    train_X = X_psce[:, train_mask].copy()
    train_clean = clean_psce[train_mask]
    train_counts = counts_psce[train_mask]

    # Map gene_name -> first read-out index (matching R's match())
    gene_first = {}
    for idx, g in enumerate(gene_names):
        if g not in gene_first:
            gene_first[g] = idx

    # -------------------------------------------------------------------------
    # 1. Direct Cis-Knockdown Attenuation Law (Lens 1a)
    # -------------------------------------------------------------------------
    P_tr = train_change.shape[1]
    row_sum = train_change.sum(axis=1)
    row_cnt = np.full(len(gene_names), P_tr, dtype=np.float64)

    cis_train_g_idx = []
    cis_train_p_idx = []
    cis_obs_delta = []
    cis_obs_counts = []

    for j, p_gene in enumerate(train_clean):
        if p_gene != "ctrl" and p_gene in gene_first:
            gi = gene_first[p_gene]
            val = train_change[gi, j]
            row_sum[gi] -= val
            row_cnt[gi] -= 1.0
            cis_train_g_idx.append(gi)
            cis_train_p_idx.append(j)
            cis_obs_delta.append(val)
            cis_obs_counts.append(train_counts[j])

    mu_trans = row_sum / np.maximum(row_cnt, 1.0)

    # De-spike diagonal cis-knockdown entries in training matrix
    Y_trans_train = train_change.copy()
    for gi, pj in zip(cis_train_g_idx, cis_train_p_idx):
        Y_trans_train[gi, pj] = mu_trans[gi]

    R_trans_train = Y_trans_train - mu_trans[:, None]
    std_trans = np.sqrt(np.mean(R_trans_train ** 2, axis=1) + 1e-8)

    # Fit weighted ridge regression for Cis-Knockdown delta on training pairs
    cis_g = np.array(cis_train_g_idx, dtype=np.int32)
    cis_y = np.array(cis_obs_delta, dtype=np.float64)
    cis_w = np.array(cis_obs_counts, dtype=np.float64)
    cis_w = cis_w / (cis_w + 20.0)

    b_cis = baseline[cis_g]
    m_cis = mu_trans[cis_g]
    s_cis = std_trans[cis_g]

    X_cis_design = np.column_stack([
        np.ones_like(b_cis),
        b_cis,
        b_cis ** 2,
        np.log1p(np.maximum(b_cis, 0.0)),
        m_cis,
        s_cis,
    ])
    W_cis = np.diag(cis_w)
    reg_cis = 2.0 * np.eye(X_cis_design.shape[1])
    reg_cis[0, 0] = 0.0
    w_cis = np.linalg.solve(X_cis_design.T @ W_cis @ X_cis_design + reg_cis, X_cis_design.T @ W_cis @ cis_y)

    def predict_cis_delta(gi):
        bg = baseline[gi]
        mg = mu_trans[gi]
        sg = std_trans[gi]
        feat = np.array([1.0, bg, bg ** 2, np.log1p(max(bg, 0.0)), mg, sg])
        pred_d = float(feat @ w_cis)
        return float(np.clip(pred_d, -bg, 0.0))

    # -------------------------------------------------------------------------
    # 2. Build Training Co-Regulation & Functional Similarity Kernels
    # -------------------------------------------------------------------------
    non_ctrl_tr_idx = [j for j, c in enumerate(train_clean) if c != "ctrl"]
    tr_pert_genes = [train_clean[j] for j in non_ctrl_tr_idx]
    Y_tr_nc = R_trans_train[:, non_ctrl_tr_idx]  # shape (G, N_tr)
    tr_nc_counts = train_counts[non_ctrl_tr_idx]
    rel_w = tr_nc_counts / (tr_nc_counts + 30.0)  # reliability weight per training perturbation

    N_all = len(clean_psce)
    N_tr = len(tr_pert_genes)
    tr_nc_global_idx = np.where(train_mask)[0][non_ctrl_tr_idx]

    # Map clean_psce and tr_pert_genes into GO index and read-out gene index
    all_go_idx = np.array([g2go_idx.get(c, -1) for c in clean_psce], dtype=np.int32)
    tr_go_idx = np.array([g2go_idx.get(c, -1) for c in tr_pert_genes], dtype=np.int32)

    all_g_idx = np.array([gene_first.get(c, -1) for c in clean_psce], dtype=np.int32)
    tr_g_idx = np.array([gene_first.get(c, -1) for c in tr_pert_genes], dtype=np.int32)

    # (a) GO IDF cosine similarity & GO Jaccard similarity (vectorized)
    valid_all_go = all_go_idx >= 0
    valid_tr_go = tr_go_idx >= 0
    S_idf_mat = np.zeros((N_all, N_tr), dtype=np.float64)
    S_jac_mat = np.zeros((N_all, N_tr), dtype=np.float64)
    ix_all_go = np.where(valid_all_go)[0]
    ix_tr_go = np.where(valid_tr_go)[0]
    S_idf_mat[np.ix_(ix_all_go, ix_tr_go)] = S_go_idf[np.ix_(all_go_idx[ix_all_go], tr_go_idx[ix_tr_go])]
    S_jac_mat[np.ix_(ix_all_go, ix_tr_go)] = S_go_jaccard[np.ix_(all_go_idx[ix_all_go], tr_go_idx[ix_tr_go])]

    # (b) Training Read-Out Co-Regulation similarities (full-rank Pearson & SVD rank-32 cosine)
    # Row-standardize R_trans_train across non-ctrl training perturbations
    R_nc = Y_tr_nc - Y_tr_nc.mean(axis=1, keepdims=True)
    R_nc_norms = np.linalg.norm(R_nc, axis=1, keepdims=True)
    R_nc_norms[R_nc_norms < 1e-8] = 1.0
    R_nc_unit = R_nc / R_nc_norms  # (G, N_tr)

    # SVD rank-32 of R_nc_unit
    U_r, s_r, _ = np.linalg.svd(R_nc_unit, full_matrices=False)
    k_svd = min(32, U_r.shape[1])
    E_svd = U_r[:, :k_svd] * np.sqrt(s_r[None, :k_svd])
    E_norms = np.linalg.norm(E_svd, axis=1, keepdims=True)
    E_norms[E_norms < 1e-8] = 1.0
    E_svd_unit = E_svd / E_norms

    valid_all_g = all_g_idx >= 0
    valid_tr_g = tr_g_idx >= 0
    ix_all_g = np.where(valid_all_g)[0]
    ix_tr_g = np.where(valid_tr_g)[0]

    S_coexp_full = np.zeros((N_all, N_tr), dtype=np.float64)
    S_coexp_svd = np.zeros((N_all, N_tr), dtype=np.float64)
    S_coexp_full[np.ix_(ix_all_g, ix_tr_g)] = np.clip(
        R_nc_unit[all_g_idx[ix_all_g], :] @ R_nc_unit[tr_g_idx[ix_tr_g], :].T, 0.0, 1.0
    )
    S_coexp_svd[np.ix_(ix_all_g, ix_tr_g)] = np.clip(
        E_svd_unit[all_g_idx[ix_all_g], :] @ E_svd_unit[tr_g_idx[ix_tr_g], :].T, 0.0, 1.0
    )

    # Mask self-matches on training perturbations (Hollow / Leave-One-Out mask!)
    hollow_mask = np.ones((N_all, N_tr), dtype=bool)
    for j_tr, glob_i in enumerate(tr_nc_global_idx):
        hollow_mask[glob_i, j_tr] = False
    # Also mask if same gene name appears
    for i_all, c_all in enumerate(clean_psce):
        if splits_psce[i_all] == "train":
            for j_tr, c_tr in enumerate(tr_pert_genes):
                if c_all == c_tr:
                    hollow_mask[i_all, j_tr] = False

    def build_hollow_topK_channel(S_raw, top_k=25, power=2.0, tau=0.15):
        """
        For each row i in 0..N_all-1:
          - Zero out self-matches via hollow_mask
          - Keep only top_k largest positive similarities
          - Raise to `power`, multiply by reliability `rel_w`
          - Normalize by (sum_weights + tau) so isolated genes shrink smoothly to 0
        Returns predicted trans residual matrix Z of shape (G, N_all) and max-sim vector.
        """
        S = np.where(hollow_mask, np.maximum(S_raw, 0.0), 0.0)
        max_sim = S.max(axis=1)
        W = np.zeros_like(S)
        for i in range(N_all):
            row = S[i, :]
            pos = np.where(row > 0.0)[0]
            if len(pos) == 0:
                continue
            if len(pos) > top_k:
                top_idx = pos[np.argpartition(row[pos], -top_k)[-top_k:]]
            else:
                top_idx = pos
            w_vals = (row[top_idx] ** power) * rel_w[top_idx]
            W[i, top_idx] = w_vals / (w_vals.sum() + tau)
        Z = Y_tr_nc @ W.T  # shape (G, N_all)
        return Z, W, max_sim

    # Construct multi-scale hollow channels:
    # Channel 1: Sharp GO IDF+Jaccard Top-15 (pathway-specific complexes)
    S_go_comb = 0.65 * S_idf_mat + 0.35 * S_jac_mat
    Z_go_sharp, W_go_sharp, max_go = build_hollow_topK_channel(S_go_comb, top_k=15, power=2.5, tau=0.05)

    # Channel 2: Broad GO IDF+Jaccard Top-50 (broader functional modules)
    Z_go_broad, W_go_broad, _ = build_hollow_topK_channel(S_go_comb, top_k=50, power=1.5, tau=0.20)

    # Channel 3:Hollow Graph Resolvent on Top-30 GO + Co-Expression graph
    S_hybrid = np.where(valid_all_g[:, None], 0.50 * S_go_comb + 0.50 * S_coexp_svd, S_go_comb)
    Z_hyb_sharp, _, max_hyb = build_hollow_topK_channel(S_hybrid, top_k=20, power=2.5, tau=0.05)

    # Channel 4: Pure Empirical Co-Expression Top-20 (for target genes in read-out set)
    S_coexp_comb = 0.55 * S_coexp_svd + 0.45 * S_coexp_full
    Z_coexp_sharp, _, _ = build_hollow_topK_channel(S_coexp_comb, top_k=20, power=3.0, tau=0.05)
    Z_coexp_broad, _, _ = build_hollow_topK_channel(S_coexp_comb, top_k=60, power=1.5, tau=0.25)

    # Channel 5: Lens 1 — Leave-One-Out De-Spiked Bilinear Operator (with Exact Hat-Matrix LOO on train!)
    X_trans_train = baseline[:, None] + Y_trans_train
    M_c = X_trans_train - X_trans_train.mean(axis=0, keepdims=True)
    U, s, _ = np.linalg.svd(M_c, full_matrices=False)
    k_pca = min(20, U.shape[1])
    pca_x = U[:, :k_pca] * s[None, :k_pca]  # (G, k_pca)

    # Normalize row norms of B so high-expression genes don't explode
    pca_norms = np.linalg.norm(pca_x, axis=1, keepdims=True)
    med_norm = np.median(pca_norms)
    pca_x_reg = pca_x * (med_norm / np.maximum(pca_norms, med_norm * 0.5))

    B_all = np.zeros((k_pca, N_all), dtype=np.float64)
    for j in range(N_all):
        if all_g_idx[j] >= 0:
            B_all[:, j] = pca_x_reg[all_g_idx[j], :]

    tr_has_g = [j_tr for j_tr in range(N_tr) if tr_g_idx[j_tr] >= 0]
    tr_has_g_glob = tr_nc_global_idx[tr_has_g]
    B_tr = B_all[:, tr_has_g_glob]  # (k_pca, N_tr_g)
    Y_tr_g = Y_tr_nc[:, tr_has_g]   # (G, N_tr_g)

    # Relative ridge proportional to mean eigenvalue
    lam_A = 0.05 * float(np.mean( np.sum(pca_x ** 2, axis=0) ))
    lam_B = 0.25 * float(np.mean( np.sum(B_tr ** 2, axis=1) ))
    P_A = pca_x @ np.linalg.solve(pca_x.T @ pca_x + lam_A * np.eye(k_pca), pca_x.T)  # (G, G)
    G_B = np.linalg.solve(B_tr @ B_tr.T + lam_B * np.eye(k_pca), B_tr)  # (k_pca, N_tr_g)

    # Hat matrix on B_tr: H_B = B_tr.T @ G_B of shape (N_tr_g, N_tr_g)
    H_B = B_tr.T @ G_B
    Y_proj = P_A @ Y_tr_g  # (G, N_tr_g)
    Z_bilin_all = Y_proj @ (G_B.T @ B_all)  # (G, N_all)

    # Replace training columns in Z_bilin_all with exact Leave-One-Out bilinear prediction!
    diag_H = np.clip(np.diag(H_B), 0.0, 0.95)
    Z_bilin_tr_in = Y_proj @ H_B
    Z_bilin_tr_loo = (Z_bilin_tr_in - Y_proj * diag_H[None, :]) / (1.0 - diag_H[None, :])
    Z_bilin_all[:, tr_has_g_glob] = Z_bilin_tr_loo

    # -------------------------------------------------------------------------
    # 3. Closed-Form Leave-One-Out (LOO) Stacking on Training Perturbations
    #    Everything here uses ONLY `Y_tr_nc` (training perturbations)!
    #    We fit separate stacking weights for:
    #      Regime A: Perturbations whose target gene IS in read-out `gene_names`
    #      Regime B: Perturbations whose target gene is NOT in read-out `gene_names`
    # -------------------------------------------------------------------------
    Y_target = Y_tr_nc[top1000_idx, :]  # (1000, N_tr)

    # Regime A: target gene in read-out `gene_names`
    idx_A = [j_tr for j_tr in range(N_tr) if tr_g_idx[j_tr] >= 0]
    glob_A = tr_nc_global_idx[idx_A]
    channels_A = [Z_go_sharp, Z_go_broad, Z_hyb_sharp, Z_coexp_sharp, Z_coexp_broad, Z_bilin_all]
    M_A = len(channels_A)
    X_stack_A = np.column_stack([
        ch[np.ix_(top1000_idx, glob_A)].reshape(-1) for ch in channels_A
    ])
    y_stack_A = Y_target[:, idx_A].reshape(-1)
    # Non-negative ridge least squares via coordinate/projected solve
    gram_A = X_stack_A.T @ X_stack_A + 1e-2 * np.trace(X_stack_A.T @ X_stack_A) * np.eye(M_A)
    rhs_A = X_stack_A.T @ y_stack_A
    w_stack_A = np.linalg.solve(gram_A, rhs_A)
    w_stack_A = np.maximum(w_stack_A, 0.0)

    # Regime B: target gene NOT in read-out `gene_names` (only GO channels available)
    channels_B = [Z_go_sharp, Z_go_broad]
    M_B = len(channels_B)
    X_stack_B = np.column_stack([
        ch[np.ix_(top1000_idx, tr_nc_global_idx)].reshape(-1) for ch in channels_B
    ])
    y_stack_B = Y_target.reshape(-1)
    gram_B = X_stack_B.T @ X_stack_B + 1e-2 * np.trace(X_stack_B.T @ X_stack_B) * np.eye(M_B)
    rhs_B = X_stack_B.T @ y_stack_B
    w_stack_B = np.linalg.solve(gram_B, rhs_B)
    w_stack_B = np.maximum(w_stack_B, 0.0)

    # Assemble final predictions
    pred_dict = {}
    nn_dist_dict = {}
    for j, c in enumerate(clean_psce):
        if c == "ctrl":
            pred_dict[c] = baseline.copy()
            nn_dist_dict[c] = 0.0
            continue
        if all_g_idx[j] >= 0:
            trans_vec = mu_trans.copy()
            for m_i, ch in enumerate(channels_A):
                trans_vec = trans_vec + w_stack_A[m_i] * ch[:, j]
            out_vec = baseline + trans_vec
            gi = all_g_idx[j]
            out_vec[gi] = baseline[gi] + predict_cis_delta(gi)
            nn_dist_dict[c] = float(1.0 - max_hyb[j])
        else:
            trans_vec = mu_trans.copy()
            for m_i, ch in enumerate(channels_B):
                trans_vec = trans_vec + w_stack_B[m_i] * ch[:, j]
            out_vec = baseline + trans_vec
            nn_dist_dict[c] = float(1.0 - max_go[j])
        pred_dict[c] = out_vec

    return pred_dict, nn_dist_dict, w_stack_A, w_stack_B


if __name__ == "__main__":
    for ds in ["replogle_k562_essential", "replogle_rpe1_essential", "adamson"]:
        gene_names, uniq_conds, clean_conds, X_mean, counts, splits_dict = eng.load_cached_dataset(ds)
        print(f"\n==================== {ds} ====================")
        all_lpm, all_dual = [], []
        for seed in [1, 2]:
            s2c = splits_dict[str(seed)]
            sub_a = panel_a[(panel_a["dataset_name"] == ds) & (panel_a["seed"] == seed) & (panel_a["method"] == "lpm_selftrained")]
            pred_lpm = rb.run_lpm(X_mean, gene_names, uniq_conds, clean_conds, s2c)
            eval_lpm = rb.evaluate_predictions(pred_lpm, X_mean, gene_names, uniq_conds, clean_conds, sub_a[["perturbation", "train"]])
            eval_lpm["seed"] = seed

            pred_dual, nn_dist, wA, wB = fit_predict_hollow_loo_dual_lens(
                X_mean, counts, gene_names, uniq_conds, clean_conds, s2c,
                g2go_idx, S_go_idf, S_go_jaccard,
            )
            eval_dual = rb.evaluate_predictions(pred_dual, X_mean, gene_names, uniq_conds, clean_conds, sub_a[["perturbation", "train"]])
            eval_dual["seed"] = seed

            all_lpm.append(eval_lpm)
            all_dual.append(eval_dual)

            print(f"  Seed {seed} (n={len(sub_a)}) | wA={np.round(wA, 3)}:")
            print(f"    lpm_selftrained: L2_mean={eval_lpm['l2'].mean():.6f}, L2_med={eval_lpm['l2'].median():.6f} | r2_delta_mean={eval_lpm['r2_delta'].mean():.6f}, r2_delta_med={eval_lpm['r2_delta'].median():.6f}")
            print(f"    Hollow-LOO Dual: L2_mean={eval_dual['l2'].mean():.6f}, L2_med={eval_dual['l2'].median():.6f} | r2_delta_mean={eval_dual['r2_delta'].mean():.6f}, r2_delta_med={eval_dual['r2_delta'].median():.6f}")

        df_lpm = pd.concat(all_lpm, ignore_index=True)
        df_dual = pd.concat(all_dual, ignore_index=True)
        pct_l2 = 100.0 * (df_dual["l2"].mean() - df_lpm["l2"].mean()) / df_lpm["l2"].mean()
        pct_med = 100.0 * (df_dual["l2"].median() - df_lpm["l2"].median()) / df_lpm["l2"].median()
        pct_r2d = 100.0 * (df_dual["r2_delta"].mean() - df_lpm["r2_delta"].mean()) / df_lpm["r2_delta"].mean()
        print(f"  >>> COMBINED {ds} (n={len(df_dual)}):")
        print(f"      L2_mean:      {df_lpm['l2'].mean():.6f} -> {df_dual['l2'].mean():.6f} ({pct_l2:+.2f}%)")
        print(f"      L2_median:    {df_lpm['l2'].median():.6f} -> {df_dual['l2'].median():.6f} ({pct_med:+.2f}%)")
        print(f"      r2_delta_mean:{df_lpm['r2_delta'].mean():.6f} -> {df_dual['r2_delta'].mean():.6f} ({pct_r2d:+.2f}%)")
        print(f"      r2_delta_med: {df_lpm['r2_delta'].median():.6f} -> {df_dual['r2_delta'].median():.6f}")
