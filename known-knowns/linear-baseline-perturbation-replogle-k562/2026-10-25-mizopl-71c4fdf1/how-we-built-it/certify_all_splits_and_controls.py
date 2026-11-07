#!/usr/bin/env python3
"""
Master Certification & Plain-Text Prediction Export Suite for
`linear-baseline-perturbation-replogle-k562` (Partial Progress `p2` Only):
  1. Re-runs `mean`, `lpm_selftrained` (`K = 10` PCA, lambda = 0.1), `lpm_gearsPertEmb`,
     and the Hollow-LOO Dual-Lens (`lens1_only`, `lens2_only`, `hollow_loo_dual_lens`)
     models strictly on the training split (`train`) of each GEARS simulation fold on
     `replogle_k562_essential` (`seeds = 1..2` Panel A `n = 262`, and `seeds = 1..5` `n = 677`).
  2. Exports plain-text per-perturbation predictions (keyed by perturbation ID, each once per split)
     for `hollow_loo_dual_lens` and `lpm_selftrained` (along with observed top-1,000 gene expression
     and `ctrl`), together with each perturbation's nearest training perturbation ID and functional
     distance (`nn_dist_hybrid`, `nn_dist_go_only`, `nn_dist_go_idf`).
  3. Certifies Partial Progress `p2` across:
     - Pre-registered hybrid GO + training co-expression distance (`nn_dist_hybrid`) under both
       standard equiprobable quartiles (`q = [0.25, 0.50, 0.75]`) and training-set-only leave-one-out
       (`train-LOO`) quartile cut points;
     - Pure static 2023 `gene2go_all.pkl` Gene Ontology distance (`nn_dist_go_only` and `nn_dist_go_idf`,
       zero expression data of any kind) under both standard equiprobable quartiles (`q = [0.25, 0.50, 0.75]`)
       and training-set-only `train-LOO` quartile cut points;
     - Both the `seeds = 1..2` Panel A benchmark splits (`n = 262`) and all 5 GEARS simulation splits
       (`seeds = 1..5`, `n = 677`).
  4. Runs 200 randomized target-label permutation controls (`100` per split on `seeds = 1, 2`) on K562.
"""
import os
import json
import time
import hashlib
import numpy as np
import pandas as pd
from scipy.stats import spearmanr, wilcoxon
from scipy.sparse.linalg import svds
import scipy.sparse as sp

import reproduce_baselines as rb
import lens1_lens2_engine as eng

DATA_DIR = os.environ.get("REPLOGLE_DATA_DIR", "../data")
GEARS_DIR = os.path.join(DATA_DIR, "gears_pert_data")
OBJECT_DIR = os.environ.get(
    "REPLOGLE_OBJECT_DIR",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "object")),
)

rb.DATA_DIR = DATA_DIR
rb.GEARS_DIR = GEARS_DIR
eng.DATA_DIR = DATA_DIR
eng.GEARS_DIR = GEARS_DIR


def extract_gears_2d_pert_emb():
    """
    Exact replica of benchmark/src/extract_pert_embedding_from_gears.R:
      - Reads go_essential_all.csv
      - Keeps top 21 edges per target by importance (slice_max(importance, n=21, by=target))
      - Computes 2D adjacency spectral embedding (top 2 left singular vectors scaled by sqrt(s))
    """
    csv_path = os.path.join(GEARS_DIR, "go_essential_all", "go_essential_all.csv")
    df = pd.read_csv(csv_path)
    df_sorted = df.sort_values(["target", "importance"], ascending=[True, False])
    df_top = df_sorted.groupby("target", sort=False).head(21)

    nodes = pd.unique(np.concatenate([df_top["source"].values, df_top["target"].values]))
    node_map = {n: i for i, n in enumerate(nodes)}
    rows = [node_map[s] for s in df_top["source"].values]
    cols = [node_map[t] for t in df_top["target"].values]
    vals = df_top["importance"].values.astype(np.float64)
    A = sp.csr_matrix((vals, (rows, cols)), shape=(len(nodes), len(nodes)))
    U, s, _ = svds(A, k=2)
    order = np.argsort(s)[::-1]
    X_emb = U[:, order] * np.sqrt(s[None, order])
    return X_emb.T, list(nodes)


def run_ablation_variant(
    X_mean,
    counts,
    gene_names,
    uniq_conds,
    clean_conds,
    set2conditions,
    g2go_idx,
    S_go_idf,
    S_go_jaccard,
    mode="dual",
    permute_seed=None,
):
    """
    Modes:
      - 'lens1_only': Direct Cis-Knockdown Attenuation + De-Spiked LOO Shrinkage Bilinear Operator
      - 'lens2_only': Hollow-LOO Multi-Scale GO + Co-Expression Graph Resolvent
      - 'dual': Full Hollow-LOO Dual-Lens (Lens 1 + Lens 2)
    Returns:
      pred_dict, dist_info
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
    top1000_idx = np.argsort(-baseline, kind="mergesort")[:1000]

    train_mask = splits_psce == "train"
    train_change = change_psce[:, train_mask].copy()
    train_clean = clean_psce[train_mask]
    train_conds = conds_psce[train_mask]
    train_counts = counts_psce[train_mask]

    gene_first = {}
    for idx, g in enumerate(gene_names):
        if g not in gene_first:
            gene_first[g] = idx

    query_clean_psce = clean_psce.copy()
    if permute_seed is not None:
        rng = np.random.default_rng(permute_seed)
        held_idx = np.where(~train_mask)[0]
        query_clean_psce[held_idx] = rng.permutation(query_clean_psce[held_idx])

    P_tr = train_change.shape[1]
    row_sum = train_change.sum(axis=1)
    row_cnt = np.full(len(gene_names), P_tr, dtype=np.float64)

    cis_train_g_idx, cis_train_p_idx, cis_obs_delta, cis_obs_counts = [], [], [], []
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
    Y_trans_train = train_change.copy()
    for gi, pj in zip(cis_train_g_idx, cis_train_p_idx):
        Y_trans_train[gi, pj] = mu_trans[gi]

    R_trans_train = Y_trans_train - mu_trans[:, None]
    std_trans = np.sqrt(np.mean(R_trans_train ** 2, axis=1) + 1e-8)

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
        return float(np.clip(float(feat @ w_cis), -bg, 0.0))

    non_ctrl_tr_idx = [j for j, c in enumerate(train_clean) if c != "ctrl"]
    tr_pert_genes = [train_clean[j] for j in non_ctrl_tr_idx]
    tr_pert_conds = [train_conds[j] for j in non_ctrl_tr_idx]
    Y_tr_nc = R_trans_train[:, non_ctrl_tr_idx]
    tr_nc_counts = train_counts[non_ctrl_tr_idx]
    rel_w = tr_nc_counts / (tr_nc_counts + 30.0)

    N_all = len(query_clean_psce)
    N_tr = len(tr_pert_genes)
    tr_nc_global_idx = np.where(train_mask)[0][non_ctrl_tr_idx]

    all_go_idx = np.array([g2go_idx.get(c, -1) for c in query_clean_psce], dtype=np.int32)
    tr_go_idx = np.array([g2go_idx.get(c, -1) for c in tr_pert_genes], dtype=np.int32)
    all_g_idx = np.array([gene_first.get(c, -1) for c in query_clean_psce], dtype=np.int32)
    tr_g_idx = np.array([gene_first.get(c, -1) for c in tr_pert_genes], dtype=np.int32)

    # Lens 1 Bilinear Channel
    X_trans_train = baseline[:, None] + Y_trans_train
    M_c = X_trans_train - X_trans_train.mean(axis=0, keepdims=True)
    U, s, _ = np.linalg.svd(M_c, full_matrices=False)
    k_pca = min(20, U.shape[1])
    pca_x = U[:, :k_pca] * s[None, :k_pca]

    pca_norms = np.linalg.norm(pca_x, axis=1, keepdims=True)
    med_norm = np.median(pca_norms)
    pca_x_reg = pca_x * (med_norm / np.maximum(pca_norms, med_norm * 0.5))

    B_all = np.zeros((k_pca, N_all), dtype=np.float64)
    for j in range(N_all):
        if all_g_idx[j] >= 0:
            B_all[:, j] = pca_x_reg[all_g_idx[j], :]

    idx_A = [j_tr for j_tr in range(N_tr) if tr_g_idx[j_tr] >= 0]
    glob_A = tr_nc_global_idx[idx_A]
    B_tr = B_all[:, glob_A]
    Y_tr_g = Y_tr_nc[:, idx_A]

    lam_A = 0.05 * float(np.mean(np.sum(pca_x ** 2, axis=0)))
    lam_B = 0.25 * float(np.mean(np.sum(B_tr ** 2, axis=1)))
    P_A = pca_x @ np.linalg.solve(pca_x.T @ pca_x + lam_A * np.eye(k_pca), pca_x.T)
    G_B = np.linalg.solve(B_tr @ B_tr.T + lam_B * np.eye(k_pca), B_tr)

    H_B = B_tr.T @ G_B
    Y_proj = P_A @ Y_tr_g
    Z_bilin_all = Y_proj @ (G_B.T @ B_all)

    diag_H = np.clip(np.diag(H_B), 0.0, 0.95)
    Z_bilin_tr_in = Y_proj @ H_B
    Z_bilin_tr_loo = (Z_bilin_tr_in - Y_proj * diag_H[None, :]) / (1.0 - diag_H[None, :])
    Z_bilin_all[:, glob_A] = Z_bilin_tr_loo

    if mode == "lens1_only":
        pred_dict = {}
        for j, c_orig in enumerate(clean_psce):
            if c_orig == "ctrl":
                pred_dict[c_orig] = baseline.copy()
                continue
            out_vec = baseline + mu_trans + Z_bilin_all[:, j]
            if all_g_idx[j] >= 0:
                gi = all_g_idx[j]
                out_vec[gi] = baseline[gi] + predict_cis_delta(gi)
            pred_dict[c_orig] = out_vec
        return pred_dict, {}

    # Lens 2 Hollow Graph Resolvent Channels
    valid_all_go = all_go_idx >= 0
    valid_tr_go = tr_go_idx >= 0
    S_idf_mat = np.zeros((N_all, N_tr), dtype=np.float64)
    S_jac_mat = np.zeros((N_all, N_tr), dtype=np.float64)
    ix_all_go = np.where(valid_all_go)[0]
    ix_tr_go = np.where(valid_tr_go)[0]
    S_idf_mat[np.ix_(ix_all_go, ix_tr_go)] = S_go_idf[np.ix_(all_go_idx[ix_all_go], tr_go_idx[ix_tr_go])]
    S_jac_mat[np.ix_(ix_all_go, ix_tr_go)] = S_go_jaccard[np.ix_(all_go_idx[ix_all_go], tr_go_idx[ix_tr_go])]

    R_nc = Y_tr_nc - Y_tr_nc.mean(axis=1, keepdims=True)
    R_nc_unit = R_nc / np.maximum(np.linalg.norm(R_nc, axis=1, keepdims=True), 1e-8)

    U_r, s_r, _ = np.linalg.svd(R_nc_unit, full_matrices=False)
    k_svd = min(32, U_r.shape[1])
    E_svd = U_r[:, :k_svd] * np.sqrt(s_r[None, :k_svd])
    E_svd_unit = E_svd / np.maximum(np.linalg.norm(E_svd, axis=1, keepdims=True), 1e-8)

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

    hollow_mask = np.ones((N_all, N_tr), dtype=bool)
    for j_tr, glob_i in enumerate(tr_nc_global_idx):
        hollow_mask[glob_i, j_tr] = False
    for i_all, c_all in enumerate(query_clean_psce):
        if splits_psce[i_all] == "train":
            for j_tr, c_tr in enumerate(tr_pert_genes):
                if c_all == c_tr:
                    hollow_mask[i_all, j_tr] = False

    def build_hollow_topK_channel(S_raw, top_k=25, power=2.0, tau=0.15):
        S = np.where(hollow_mask, np.maximum(S_raw, 0.0), 0.0)
        max_sim = S.max(axis=1)
        argmax_tr = np.argmax(S, axis=1)
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
        Z = Y_tr_nc @ W.T
        return Z, W, max_sim, argmax_tr

    S_go_comb = 0.65 * S_idf_mat + 0.35 * S_jac_mat
    Z_go_sharp, _, max_go, argmax_go = build_hollow_topK_channel(S_go_comb, top_k=15, power=2.5, tau=0.05)
    Z_go_broad, _, _, _ = build_hollow_topK_channel(S_go_comb, top_k=50, power=1.5, tau=0.20)

    S_idf_masked = np.where(hollow_mask, np.maximum(S_idf_mat, 0.0), 0.0)
    max_go_idf = S_idf_masked.max(axis=1)
    argmax_go_idf = np.argmax(S_idf_masked, axis=1)

    S_hybrid = np.where(valid_all_g[:, None], 0.50 * S_go_comb + 0.50 * S_coexp_svd, S_go_comb)
    Z_hyb_sharp, _, max_hyb, argmax_hyb = build_hollow_topK_channel(S_hybrid, top_k=20, power=2.5, tau=0.05)

    S_coexp_comb = 0.55 * S_coexp_svd + 0.45 * S_coexp_full
    Z_coexp_sharp, _, _, _ = build_hollow_topK_channel(S_coexp_comb, top_k=20, power=3.0, tau=0.05)
    Z_coexp_broad, _, _, _ = build_hollow_topK_channel(S_coexp_comb, top_k=60, power=1.5, tau=0.25)

    Y_target = Y_tr_nc[top1000_idx, :]
    if mode == "lens2_only":
        channels_A = [Z_go_sharp, Z_go_broad, Z_hyb_sharp, Z_coexp_sharp, Z_coexp_broad]
    else:
        channels_A = [Z_go_sharp, Z_go_broad, Z_hyb_sharp, Z_coexp_sharp, Z_coexp_broad, Z_bilin_all]

    M_A = len(channels_A)
    X_stack_A = np.column_stack([
        ch[np.ix_(top1000_idx, glob_A)].reshape(-1) for ch in channels_A
    ])
    y_stack_A = Y_target[:, idx_A].reshape(-1)
    gram_A = X_stack_A.T @ X_stack_A + 1e-2 * np.trace(X_stack_A.T @ X_stack_A) * np.eye(M_A)
    w_stack_A = np.maximum(np.linalg.solve(gram_A, X_stack_A.T @ y_stack_A), 0.0)

    channels_B = [Z_go_sharp, Z_go_broad]
    M_B = len(channels_B)
    X_stack_B = np.column_stack([
        ch[np.ix_(top1000_idx, tr_nc_global_idx)].reshape(-1) for ch in channels_B
    ])
    y_stack_B = Y_target.reshape(-1)
    gram_B = X_stack_B.T @ X_stack_B + 1e-2 * np.trace(X_stack_B.T @ X_stack_B) * np.eye(M_B)
    w_stack_B = np.maximum(np.linalg.solve(gram_B, X_stack_B.T @ y_stack_B), 0.0)

    pred_dict = {}
    nn_dist_hyb_dict = {}
    nn_train_hyb_dict = {}
    nn_dist_go_dict = {}
    nn_train_go_dict = {}
    nn_dist_idf_dict = {}
    nn_train_idf_dict = {}

    for j, c_orig in enumerate(clean_psce):
        if c_orig == "ctrl":
            pred_dict[c_orig] = baseline.copy()
            nn_dist_hyb_dict[c_orig] = 0.0
            nn_train_hyb_dict[c_orig] = "ctrl"
            nn_dist_go_dict[c_orig] = 0.0
            nn_train_go_dict[c_orig] = "ctrl"
            nn_dist_idf_dict[c_orig] = 0.0
            nn_train_idf_dict[c_orig] = "ctrl"
            continue
        if all_g_idx[j] >= 0:
            trans_vec = mu_trans.copy()
            for m_i, ch in enumerate(channels_A):
                trans_vec = trans_vec + w_stack_A[m_i] * ch[:, j]
            out_vec = baseline + trans_vec
            if mode != "lens2_only":
                gi = all_g_idx[j]
                out_vec[gi] = baseline[gi] + predict_cis_delta(gi)
            nn_dist_hyb_dict[c_orig] = float(1.0 - max_hyb[j])
            nn_train_hyb_dict[c_orig] = str(tr_pert_conds[int(argmax_hyb[j])])
        else:
            trans_vec = mu_trans.copy()
            for m_i, ch in enumerate(channels_B):
                trans_vec = trans_vec + w_stack_B[m_i] * ch[:, j]
            out_vec = baseline + trans_vec
            nn_dist_hyb_dict[c_orig] = float(1.0 - max_go[j])
            nn_train_hyb_dict[c_orig] = str(tr_pert_conds[int(argmax_go[j])])

        nn_dist_go_dict[c_orig] = float(1.0 - max_go[j])
        nn_train_go_dict[c_orig] = str(tr_pert_conds[int(argmax_go[j])])
        nn_dist_idf_dict[c_orig] = float(1.0 - max_go_idf[j])
        nn_train_idf_dict[c_orig] = str(tr_pert_conds[int(argmax_go_idf[j])])
        pred_dict[c_orig] = out_vec

    # Compute train-only LOO quartile cut points strictly on in-readout training perturbations
    tr_hyb_loo_vals = [1.0 - float(max_hyb[g_i]) for g_i in glob_A]
    tr_go_loo_vals = [1.0 - float(max_go[g_i]) for g_i in glob_A]
    tr_idf_loo_vals = [1.0 - float(max_go_idf[g_i]) for g_i in glob_A]

    dist_info = {
        "nn_dist": nn_dist_hyb_dict,
        "nn_train_pert": nn_train_hyb_dict,
        "nn_dist_go_only": nn_dist_go_dict,
        "nn_train_pert_go_only": nn_train_go_dict,
        "nn_dist_go_idf": nn_dist_idf_dict,
        "nn_train_pert_go_idf": nn_train_idf_dict,
        "train_loo_cutpoints_hybrid": [round(float(x), 6) for x in np.quantile(tr_hyb_loo_vals, [0.25, 0.50, 0.75])],
        "train_loo_cutpoints_go_only": [round(float(x), 6) for x in np.quantile(tr_go_loo_vals, [0.25, 0.50, 0.75])],
        "train_loo_cutpoints_go_idf": [round(float(x), 6) for x in np.quantile(tr_idf_loo_vals, [0.25, 0.50, 0.75])],
    }
    return pred_dict, dist_info


def summarize_df(df):
    return {
        "n": int(len(df)),
        "l2_mean": round(float(df["l2"].mean()), 6),
        "l2_median": round(float(df["l2"].median()), 6),
        "r2_delta_mean": round(float(df["r2_delta"].mean()), 6),
        "r2_delta_median": round(float(df["r2_delta"].median()), 6),
        "r2_mean": round(float(df["r2"].mean()), 6) if "r2" in df.columns else None,
    }


def summarize_p2_stratification(df, dist_col, q_col, cutpoints_list=None):
    q_summary = {}
    for q_label in ["Q1_closest", "Q2_mid_close", "Q3_mid_far", "Q4_farthest"]:
        q_grp = df[df[q_col] == q_label]
        q_summary[q_label] = {
            "n": int(len(q_grp)),
            "nn_dist_min": round(float(q_grp[dist_col].min()), 6),
            "nn_dist_max": round(float(q_grp[dist_col].max()), 6),
            "nn_dist_mean": round(float(q_grp[dist_col].mean()), 6),
            "lpm_l2_mean": round(float(q_grp["l2_lpm"].mean()), 6),
            "dual_l2_mean": round(float(q_grp["l2_dual"].mean()), 6),
            "delta_l2_mean": round(float(q_grp["delta_l2_vs_lpm"].mean()), 6),
            "rel_l2_change_pct": round(100.0 * float(q_grp["delta_l2_vs_lpm"].mean() / q_grp["l2_lpm"].mean()), 2),
            "lpm_r2_delta_mean": round(float(q_grp["r2_delta_lpm"].mean()), 6),
            "dual_r2_delta_mean": round(float(q_grp["r2_delta_dual"].mean()), 6),
            "delta_r2_delta_mean": round(float(q_grp["delta_r2d_vs_lpm"].mean()), 6),
        }
    rho_l2, p_rho_l2 = spearmanr(df[dist_col], df["delta_l2_vs_lpm"])
    rho_r2d, p_rho_r2d = spearmanr(df[dist_col], df["delta_r2d_vs_lpm"])
    _, wilcox_l2_p = wilcoxon(df["l2_dual"], df["l2_lpm"], alternative="less")
    _, wilcox_r2d_p = wilcoxon(df["r2_delta_dual"], df["r2_delta_lpm"], alternative="greater")
    out = {
        "n_total": int(len(df)),
        "distance_column": dist_col,
        "quartile_column": q_col,
        "spearman_r_nn_dist_vs_delta_l2": round(float(rho_l2), 6),
        "spearman_p_nn_dist_vs_delta_l2": float(f"{p_rho_l2:.4e}"),
        "spearman_r_nn_dist_vs_delta_r2_delta": round(float(rho_r2d), 6),
        "spearman_p_nn_dist_vs_delta_r2_delta": float(f"{p_rho_r2d:.4e}"),
        "wilcoxon_paired_l2_pvalue": float(f"{wilcox_l2_p:.4e}"),
        "wilcoxon_paired_r2_delta_pvalue": float(f"{wilcox_r2d_p:.4e}"),
        "quartiles": q_summary,
    }
    if cutpoints_list is not None:
        out["quartile_cutpoints_q25_q50_q75"] = [round(float(x), 6) for x in cutpoints_list]
    return out


def assign_cutpoint_quartiles(vals, cuts):
    out = []
    for v in vals:
        if v <= cuts[0]:
            out.append("Q1_closest")
        elif v <= cuts[1]:
            out.append("Q2_mid_close")
        elif v <= cuts[2]:
            out.append("Q3_mid_far")
        else:
            out.append("Q4_farthest")
    return out


def fmt_num(v):
    s = f"{v:.4f}"
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s if s != "-0" else "0"


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


if __name__ == "__main__":
    t_start_all = time.time()
    os.makedirs(OBJECT_DIR, exist_ok=True)
    panel_a = pd.read_excel(os.path.join(DATA_DIR, "single_perturbation_prediction.xlsx"), sheet_name="Panel A")

    t_go0 = time.time()
    pert_names = rb.load_pert_names()
    go_genes, g2go_idx, S_go_idf, S_go_jaccard = eng.build_go_idf_features(pert_names)
    gears_2d_emb = extract_gears_2d_pert_emb()
    t_go_sec = round(time.time() - t_go0, 2)
    print(f"Loaded GO IDF/Jaccard + 2D GEARS embedding in {t_go_sec}s", flush=True)

    ds = "replogle_k562_essential"
    gene_names, uniq_conds, clean_conds, X_mean, counts, splits_dict = eng.load_cached_dataset(ds)
    gene_set = set(gene_names)
    clean_to_idx = {c: i for i, c in enumerate(clean_conds)}

    ctrl_idx = np.where(uniq_conds == "ctrl")[0][0]
    baseline = X_mean[:, ctrl_idx]
    top1000_idx = np.argsort(-baseline, kind="mergesort")[:1000]
    top1000_genes = list(gene_names[top1000_idx])

    methods_panel_a = {m: [] for m in ["mean", "lpm_selftrained", "lpm_gearsPertEmb", "lens1_only", "lens2_only", "hollow_loo_dual_lens"]}
    five_seed_in_readout = {m: [] for m in ["mean", "lpm_selftrained", "lpm_gearsPertEmb", "lens1_only", "lens2_only", "hollow_loo_dual_lens"]}
    five_seed_all_perts = {m: [] for m in ["mean", "lpm_gearsPertEmb", "lens2_only", "hollow_loo_dual_lens"]}

    all_5seed_p2_records = []
    train_loo_cutpoints_by_seed = {}
    plain_text_files_manifest = {}

    t_ds0 = time.time()
    for seed in range(1, 6):
        s2c = splits_dict[str(seed)]
        panel_a_seed_perts = set()
        if seed in [1, 2]:
            sub_a = panel_a[
                (panel_a["dataset_name"] == ds)
                & (panel_a["seed"] == seed)
                & (panel_a["method"] == "lpm_selftrained")
            ][["perturbation", "train"]].copy()
            panel_a_seed_perts = set(sub_a["perturbation"].values)

        held_rows_in = []
        held_rows_all = []
        for sp_name in ["test", "val"]:
            for c in s2c.get(sp_name, []):
                if c == "ctrl":
                    continue
                clean_c = c.replace("+ctrl", "").replace("ctrl+", "")
                held_rows_all.append({"perturbation": c, "train": sp_name})
                if clean_c in gene_set:
                    held_rows_in.append({"perturbation": c, "train": sp_name})
        df_in = pd.DataFrame(held_rows_in)
        df_all = pd.DataFrame(held_rows_all)

        p_mean = rb.run_mean_baseline(X_mean, uniq_conds, clean_conds, s2c)
        p_lpm = rb.run_lpm(X_mean, gene_names, uniq_conds, clean_conds, s2c)
        p_gears_emb = rb.run_lpm(X_mean, gene_names, uniq_conds, clean_conds, s2c, pert_emb=gears_2d_emb)
        p_l1, _ = run_ablation_variant(X_mean, counts, gene_names, uniq_conds, clean_conds, s2c, g2go_idx, S_go_idf, S_go_jaccard, mode="lens1_only")
        p_l2, _ = run_ablation_variant(X_mean, counts, gene_names, uniq_conds, clean_conds, s2c, g2go_idx, S_go_idf, S_go_jaccard, mode="lens2_only")
        p_dual, dist_info = run_ablation_variant(X_mean, counts, gene_names, uniq_conds, clean_conds, s2c, g2go_idx, S_go_idf, S_go_jaccard, mode="dual")

        train_loo_cutpoints_by_seed[str(seed)] = {
            "hybrid": dist_info["train_loo_cutpoints_hybrid"],
            "go_only": dist_info["train_loo_cutpoints_go_only"],
            "go_idf": dist_info["train_loo_cutpoints_go_idf"],
        }

        pmap = {
            "mean": p_mean,
            "lpm_selftrained": p_lpm,
            "lpm_gearsPertEmb": p_gears_emb,
            "lens1_only": p_l1,
            "lens2_only": p_l2,
            "hollow_loo_dual_lens": p_dual,
        }

        if seed in [1, 2]:
            for m_key in methods_panel_a:
                ev_a = rb.evaluate_predictions(pmap[m_key], X_mean, gene_names, uniq_conds, clean_conds, sub_a)
                ev_a["seed"] = seed
                methods_panel_a[m_key].append(ev_a)

        for m_key in five_seed_in_readout:
            ev_in = rb.evaluate_predictions(pmap[m_key], X_mean, gene_names, uniq_conds, clean_conds, df_in)
            ev_in["seed"] = seed
            five_seed_in_readout[m_key].append(ev_in)

        for m_key in five_seed_all_perts:
            ev_all = rb.evaluate_predictions(pmap[m_key], X_mean, gene_names, uniq_conds, clean_conds, df_all)
            ev_all["seed"] = seed
            five_seed_all_perts[m_key].append(ev_all)

        # Build per-perturbation records for this seed (all held-out in-readout perturbations)
        ev_lpm_in = five_seed_in_readout["lpm_selftrained"][-1]
        ev_dual_in = five_seed_in_readout["hollow_loo_dual_lens"][-1]
        ev_mean_in = five_seed_in_readout["mean"][-1]

        m_df = ev_dual_in.merge(ev_lpm_in, on=["perturbation", "train", "seed"], suffixes=("_dual", "_lpm"))
        m_df = m_df.merge(
            ev_mean_in[["perturbation", "seed", "l2", "r2_delta"]],
            on=["perturbation", "seed"],
        ).rename(columns={"l2": "l2_mean_base", "r2_delta": "r2_delta_mean_base"})
        m_df["in_panel_a"] = m_df["perturbation"].apply(lambda p: 1 if p in panel_a_seed_perts else 0)
        m_df["clean_pert"] = m_df["perturbation"].str.replace("+ctrl", "", regex=False).str.replace("ctrl+", "", regex=False)

        m_df["nearest_train_pert"] = m_df["clean_pert"].map(dist_info["nn_train_pert"])
        m_df["nn_dist"] = m_df["clean_pert"].map(dist_info["nn_dist"])
        m_df["nearest_train_pert_go_only"] = m_df["clean_pert"].map(dist_info["nn_train_pert_go_only"])
        m_df["nn_dist_go_only"] = m_df["clean_pert"].map(dist_info["nn_dist_go_only"])
        m_df["nearest_train_pert_go_idf"] = m_df["clean_pert"].map(dist_info["nn_train_pert_go_idf"])
        m_df["nn_dist_go_idf"] = m_df["clean_pert"].map(dist_info["nn_dist_go_idf"])

        m_df["quartile_hybrid_train_loo"] = assign_cutpoint_quartiles(
            m_df["nn_dist"].values, dist_info["train_loo_cutpoints_hybrid"]
        )
        m_df["quartile_go_only_train_loo"] = assign_cutpoint_quartiles(
            m_df["nn_dist_go_only"].values, dist_info["train_loo_cutpoints_go_only"]
        )
        m_df["quartile_go_idf_train_loo"] = assign_cutpoint_quartiles(
            m_df["nn_dist_go_idf"].values, dist_info["train_loo_cutpoints_go_idf"]
        )
        all_5seed_p2_records.append(m_df)

        # Export plain-text per-perturbation prediction TSVs for this split (keyed by perturbation ID, each once)
        pred_header = "\t".join(
            [
                "perturbation",
                "split",
                "in_panel_a",
                "nearest_train_pert",
                "nn_dist",
                "nearest_train_pert_go_only",
                "nn_dist_go_only",
            ]
            + top1000_genes
        )
        obs_header = "\t".join(["perturbation", "split"] + top1000_genes)

        dual_lines = [pred_header]
        lpm_lines = [pred_header]
        obs_lines = [obs_header]

        # First row of observed TSV is ctrl baseline over top1000_genes
        ctrl_top = baseline[top1000_idx]
        obs_lines.append("\t".join(["ctrl", "train"] + [fmt_num(v) for v in ctrl_top]))

        for _, row in m_df.iterrows():
            p_id = row["perturbation"]
            cp = row["clean_pert"]
            sp_lbl = row["train"]
            in_pa = str(int(row["in_panel_a"]))
            nn_tr_h = str(row["nearest_train_pert"])
            nn_d_h = f"{float(row['nn_dist']):.6f}"
            nn_tr_go = str(row["nearest_train_pert_go_only"])
            nn_d_go = f"{float(row['nn_dist_go_only']):.6f}"

            vec_dual = p_dual[cp][top1000_idx]
            vec_lpm = p_lpm[cp][top1000_idx]
            vec_obs = X_mean[top1000_idx, clean_to_idx[cp]]

            dual_lines.append(
                "\t".join([p_id, sp_lbl, in_pa, nn_tr_h, nn_d_h, nn_tr_go, nn_d_go] + [fmt_num(v) for v in vec_dual])
            )
            lpm_lines.append(
                "\t".join([p_id, sp_lbl, in_pa, nn_tr_h, nn_d_h, nn_tr_go, nn_d_go] + [fmt_num(v) for v in vec_lpm])
            )
            obs_lines.append("\t".join([p_id, sp_lbl] + [fmt_num(v) for v in vec_obs]))

        for fname, lines_list in [
            (f"k562_seed{seed}_dual_predictions.tsv", dual_lines),
            (f"k562_seed{seed}_lpm_predictions.tsv", lpm_lines),
            (f"k562_seed{seed}_observed_top1000.tsv", obs_lines),
        ]:
            fpath = os.path.join(OBJECT_DIR, fname)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write("\n".join(lines_list) + "\n")
            plain_text_files_manifest[fname] = {
                "rows_excluding_header": len(lines_list) - 1,
                "columns": len(lines_list[0].split("\t")),
                "bytes": os.path.getsize(fpath),
                "sha256": sha256_file(fpath),
            }

    # Combine all 5 seeds (n = 677) and Panel A seeds 1..2 (n = 262)
    full_p2_df = pd.concat(all_5seed_p2_records, ignore_index=True)
    full_p2_df["delta_l2_vs_lpm"] = full_p2_df["l2_dual"] - full_p2_df["l2_lpm"]
    full_p2_df["delta_r2d_vs_lpm"] = full_p2_df["r2_delta_dual"] - full_p2_df["r2_delta_lpm"]

    full_p2_df["quartile_hybrid_5seed"] = pd.qcut(
        full_p2_df["nn_dist"], q=4, labels=["Q1_closest", "Q2_mid_close", "Q3_mid_far", "Q4_farthest"]
    ).astype(str)
    full_p2_df["quartile_go_only_5seed"] = pd.qcut(
        full_p2_df["nn_dist_go_only"], q=4, labels=["Q1_closest", "Q2_mid_close", "Q3_mid_far", "Q4_farthest"]
    ).astype(str)
    full_p2_df["quartile_go_idf_5seed"] = pd.qcut(
        full_p2_df["nn_dist_go_idf"], q=4, labels=["Q1_closest", "Q2_mid_close", "Q3_mid_far", "Q4_farthest"]
    ).astype(str)

    pa_mask = full_p2_df["in_panel_a"] == 1
    pa_df = full_p2_df[pa_mask].copy()
    pa_df["quartile_hybrid_panel_a"] = pd.qcut(
        pa_df["nn_dist"], q=4, labels=["Q1_closest", "Q2_mid_close", "Q3_mid_far", "Q4_farthest"]
    ).astype(str)
    pa_df["quartile_go_only_panel_a"] = pd.qcut(
        pa_df["nn_dist_go_only"], q=4, labels=["Q1_closest", "Q2_mid_close", "Q3_mid_far", "Q4_farthest"]
    ).astype(str)
    pa_df["quartile_go_idf_panel_a"] = pd.qcut(
        pa_df["nn_dist_go_idf"], q=4, labels=["Q1_closest", "Q2_mid_close", "Q3_mid_far", "Q4_farthest"]
    ).astype(str)

    full_p2_df["quartile_hybrid_panel_a"] = "NA"
    full_p2_df.loc[pa_mask, "quartile_hybrid_panel_a"] = pa_df["quartile_hybrid_panel_a"]
    full_p2_df["quartile_go_only_panel_a"] = "NA"
    full_p2_df.loc[pa_mask, "quartile_go_only_panel_a"] = pa_df["quartile_go_only_panel_a"]
    full_p2_df["quartile_go_idf_panel_a"] = "NA"
    full_p2_df.loc[pa_mask, "quartile_go_idf_panel_a"] = pa_df["quartile_go_idf_panel_a"]

    # Export plain-text per-perturbation metrics table (all 677 held-out perturbations across seeds 1..5)
    metrics_cols = [
        "seed",
        "perturbation",
        "train",
        "in_panel_a",
        "nearest_train_pert",
        "nn_dist",
        "quartile_hybrid_panel_a",
        "quartile_hybrid_5seed",
        "quartile_hybrid_train_loo",
        "nearest_train_pert_go_only",
        "nn_dist_go_only",
        "quartile_go_only_panel_a",
        "quartile_go_only_5seed",
        "quartile_go_only_train_loo",
        "nearest_train_pert_go_idf",
        "nn_dist_go_idf",
        "quartile_go_idf_panel_a",
        "quartile_go_idf_5seed",
        "quartile_go_idf_train_loo",
        "l2_lpm",
        "l2_dual",
        "delta_l2_vs_lpm",
        "r2_delta_lpm",
        "r2_delta_dual",
        "delta_r2d_vs_lpm",
        "l2_mean_base",
        "r2_delta_mean_base",
        "r2_lpm",
        "r2_dual",
    ]
    out_metrics_df = full_p2_df[metrics_cols].copy()
    for fcol in [
        "nn_dist",
        "nn_dist_go_only",
        "nn_dist_go_idf",
        "l2_lpm",
        "l2_dual",
        "delta_l2_vs_lpm",
        "r2_delta_lpm",
        "r2_delta_dual",
        "delta_r2d_vs_lpm",
        "l2_mean_base",
        "r2_delta_mean_base",
        "r2_lpm",
        "r2_dual",
    ]:
        out_metrics_df[fcol] = out_metrics_df[fcol].map(lambda x: f"{float(x):.6f}")

    metrics_tsv_path = os.path.join(OBJECT_DIR, "k562_p2_per_perturbation_metrics.tsv")
    out_metrics_df.to_csv(metrics_tsv_path, sep="\t", index=False)
    plain_text_files_manifest["k562_p2_per_perturbation_metrics.tsv"] = {
        "rows_excluding_header": int(len(out_metrics_df)),
        "columns": int(len(metrics_cols)),
        "bytes": os.path.getsize(metrics_tsv_path),
        "sha256": sha256_file(metrics_tsv_path),
    }

    # Re-load rounded TSV so certificate summary matches plain-text TSV to 6 decimal places
    full_p2_df = pd.read_csv(metrics_tsv_path, sep="\t")
    pa_df = full_p2_df[full_p2_df["in_panel_a"] == 1].copy()

    # Summarize Panel A (test+val) and (test-only) on K562
    repro_panel_a = {ds: {}}
    repro_panel_a_test_only = {ds: {}}
    for m_key, df_list in methods_panel_a.items():
        full_df = pd.concat(df_list, ignore_index=True)
        by_seed = {str(s): summarize_df(full_df[full_df["seed"] == s]) for s in [1, 2]}
        s_l2_m = [by_seed[k]["l2_mean"] for k in ["1", "2"]]
        s_l2_med = [by_seed[k]["l2_median"] for k in ["1", "2"]]
        s_r2d_m = [by_seed[k]["r2_delta_mean"] for k in ["1", "2"]]
        s_r2d_med = [by_seed[k]["r2_delta_median"] for k in ["1", "2"]]
        comb = summarize_df(full_df)
        comb["across_split_sd_l2_mean"] = round(float(np.std(s_l2_m, ddof=1)), 6)
        comb["across_split_sd_l2_median"] = round(float(np.std(s_l2_med, ddof=1)), 6)
        comb["across_split_sd_r2_delta_mean"] = round(float(np.std(s_r2d_m, ddof=1)), 6)
        comb["across_split_sd_r2_delta_median"] = round(float(np.std(s_r2d_med, ddof=1)), 6)
        comb["per_seed"] = by_seed
        repro_panel_a[ds][m_key] = comb

        test_df = full_df[full_df["train"] == "test"]
        by_seed_t = {str(s): summarize_df(test_df[test_df["seed"] == s]) for s in [1, 2]}
        comb_t = summarize_df(test_df)
        comb_t["across_split_sd_l2_mean"] = round(float(np.std([by_seed_t[k]["l2_mean"] for k in ["1", "2"]], ddof=1)), 6)
        comb_t["across_split_sd_r2_delta_mean"] = round(float(np.std([by_seed_t[k]["r2_delta_mean"] for k in ["1", "2"]], ddof=1)), 6)
        comb_t["per_seed"] = by_seed_t
        repro_panel_a_test_only[ds][m_key] = comb_t

    five_seed_summary = {ds: {"in_readout_genes": {}, "all_held_out_perturbations": {}}}
    for m_key, df_list in five_seed_in_readout.items():
        full_df = pd.concat(df_list, ignore_index=True)
        by_seed = {str(s): summarize_df(full_df[full_df["seed"] == s]) for s in range(1, 6)}
        comb = summarize_df(full_df)
        comb["across_5split_sd_l2_mean"] = round(float(np.std([by_seed[str(s)]["l2_mean"] for s in range(1, 6)], ddof=1)), 6)
        comb["across_5split_sd_l2_median"] = round(float(np.std([by_seed[str(s)]["l2_median"] for s in range(1, 6)], ddof=1)), 6)
        comb["across_5split_sd_r2_delta_mean"] = round(float(np.std([by_seed[str(s)]["r2_delta_mean"] for s in range(1, 6)], ddof=1)), 6)
        comb["across_5split_sd_r2_delta_median"] = round(float(np.std([by_seed[str(s)]["r2_delta_median"] for s in range(1, 6)], ddof=1)), 6)
        comb["per_seed"] = by_seed
        five_seed_summary[ds]["in_readout_genes"][m_key] = comb

    for m_key, df_list in five_seed_all_perts.items():
        full_df = pd.concat(df_list, ignore_index=True)
        by_seed = {str(s): summarize_df(full_df[full_df["seed"] == s]) for s in range(1, 6)}
        comb = summarize_df(full_df)
        comb["across_5split_sd_l2_mean"] = round(float(np.std([by_seed[str(s)]["l2_mean"] for s in range(1, 6)], ddof=1)), 6)
        comb["across_5split_sd_r2_delta_mean"] = round(float(np.std([by_seed[str(s)]["r2_delta_mean"] for s in range(1, 6)], ddof=1)), 6)
        comb["per_seed"] = by_seed
        five_seed_summary[ds]["all_held_out_perturbations"][m_key] = comb

    t_ds_sec = round(time.time() - t_ds0, 2)
    print(f"Finished {ds} 5-seed & plain-text export in {t_ds_sec}s", flush=True)

    # Mandatory Null / Permutation Control Battery (200 controls on K562: 100 per seed on seeds 1, 2)
    t_null0 = time.time()
    null_l2_means = []
    null_r2d_means = []
    for perm_i in range(100):
        perm_dfs = []
        for seed in [1, 2]:
            s2c = splits_dict[str(seed)]
            sub_a = panel_a[
                (panel_a["dataset_name"] == ds)
                & (panel_a["seed"] == seed)
                & (panel_a["method"] == "lpm_selftrained")
            ][["perturbation", "train"]].copy()
            p_null, _ = run_ablation_variant(
                X_mean,
                counts,
                gene_names,
                uniq_conds,
                clean_conds,
                s2c,
                g2go_idx,
                S_go_idf,
                S_go_jaccard,
                mode="dual",
                permute_seed=10000 + perm_i * 10 + seed,
            )
            ev_null = rb.evaluate_predictions(p_null, X_mean, gene_names, uniq_conds, clean_conds, sub_a)
            perm_dfs.append(ev_null)
        df_perm = pd.concat(perm_dfs, ignore_index=True)
        null_l2_means.append(float(df_perm["l2"].mean()))
        null_r2d_means.append(float(df_perm["r2_delta"].mean()))

    real_l2 = repro_panel_a[ds]["hollow_loo_dual_lens"]["l2_mean"]
    real_r2d = repro_panel_a[ds]["hollow_loo_dual_lens"]["r2_delta_mean"]
    mean_base_l2 = repro_panel_a[ds]["mean"]["l2_mean"]
    mean_base_r2d = repro_panel_a[ds]["mean"]["r2_delta_mean"]

    null_l2_arr = np.array(null_l2_means)
    null_r2d_arr = np.array(null_r2d_means)
    z_l2 = (real_l2 - float(null_l2_arr.mean())) / max(float(null_l2_arr.std(ddof=1)), 1e-12)
    z_r2d = (real_r2d - float(null_r2d_arr.mean())) / max(float(null_r2d_arr.std(ddof=1)), 1e-12)
    emp_p_l2 = (1 + int(np.sum(null_l2_arr <= real_l2))) / (len(null_l2_arr) + 1)
    emp_p_r2d = (1 + int(np.sum(null_r2d_arr >= real_r2d))) / (len(null_r2d_arr) + 1)

    t_null_sec = round(time.time() - t_null0, 2)

    p2_strat_dict = {
        ds: summarize_p2_stratification(
            pa_df,
            "nn_dist",
            "quartile_hybrid_panel_a",
            np.quantile(pa_df["nn_dist"].values, [0.25, 0.50, 0.75]),
        ),
        "replogle_k562_essential_train_loo_cutpoints_hybrid_seeds_1_2": summarize_p2_stratification(
            pa_df,
            "nn_dist",
            "quartile_hybrid_train_loo",
        ),
        "replogle_k562_essential_pure_go_2023_seeds_1_2": summarize_p2_stratification(
            pa_df,
            "nn_dist_go_only",
            "quartile_go_only_panel_a",
            np.quantile(pa_df["nn_dist_go_only"].values, [0.25, 0.50, 0.75]),
        ),
        "replogle_k562_essential_pure_go_2023_train_loo_cutpoints_seeds_1_2": summarize_p2_stratification(
            pa_df,
            "nn_dist_go_only",
            "quartile_go_only_train_loo",
        ),
        "replogle_k562_essential_pure_go_idf_2023_seeds_1_2": summarize_p2_stratification(
            pa_df,
            "nn_dist_go_idf",
            "quartile_go_idf_panel_a",
            np.quantile(pa_df["nn_dist_go_idf"].values, [0.25, 0.50, 0.75]),
        ),
        "replogle_k562_essential_pure_go_idf_2023_train_loo_cutpoints_seeds_1_2": summarize_p2_stratification(
            pa_df,
            "nn_dist_go_idf",
            "quartile_go_idf_train_loo",
        ),
        "replogle_k562_essential_five_seed_hybrid_seeds_1_5": summarize_p2_stratification(
            full_p2_df,
            "nn_dist",
            "quartile_hybrid_5seed",
            np.quantile(full_p2_df["nn_dist"].values, [0.25, 0.50, 0.75]),
        ),
        "replogle_k562_essential_five_seed_pure_go_2023_seeds_1_5": summarize_p2_stratification(
            full_p2_df,
            "nn_dist_go_only",
            "quartile_go_only_5seed",
            np.quantile(full_p2_df["nn_dist_go_only"].values, [0.25, 0.50, 0.75]),
        ),
        "train_loo_cutpoints_by_seed": train_loo_cutpoints_by_seed,
    }

    cert = {
        "id": "linear-baseline-perturbation-replogle-k562",
        "claim_scope": "PARTIAL_PROGRESS (p2 only)",
        "pinned_commit": "bfa6eeea2bd145a1af2ec0127a2e808cc38456a9",
        "go_graph_build_time_sec": t_go_sec,
        "published_source_data_links_and_sha256": {
            "single_perturbation_prediction_xlsx": {
                "url": "https://github.com/const-ae/linear_perturbation_prediction-Paper/raw/bfa6eeea2bd145a1af2ec0127a2e808cc38456a9/source_data/single_perturbation_prediction.xlsx",
                "bytes": 565586,
                "sha256": "09c6c198aff4e8a827064183f9cff13eb6f33e56f1689940527304bf78957efe",
            },
            "suppl_pearson_delta_performance_single_pert_xlsx": {
                "url": "https://github.com/const-ae/linear_perturbation_prediction-Paper/raw/bfa6eeea2bd145a1af2ec0127a2e808cc38456a9/source_data/suppl-pearson_delta_performance_single_pert.xlsx",
                "bytes": 569165,
                "sha256": "61658661412f385356a383c3ed506f4454c6db79b28c272151bb15a725b0faaa",
            },
            "gene2go_all_pkl": {
                "url": "https://dataverse.harvard.edu/api/access/datafile/6153417",
                "bytes": 9462558,
                "sha256": "f145c5e84a53048d87942a417d870a4f2d8db50200b96e492b358c13aba8c771",
            },
            "essential_all_data_pert_genes_pkl": {
                "url": "https://dataverse.harvard.edu/api/access/datafile/6934320",
                "bytes": 558811,
                "sha256": "46c3dfe354d8ad5c0da22c69f3d0ca451987b1a61ed9d984279b22b9565ff8d7",
            },
            "go_essential_all_tar_gz": {
                "url": "https://dataverse.harvard.edu/api/access/datafile/6934319",
                "bytes": 60654049,
                "sha256": "3d2ee2ebbcdf3ca2ca8fd8fb0d3bbf0a63db9dd2ff9fc7587abbd57a55b78998",
            },
            "replogle_k562_essential_perturb_processed_h5ad": {
                "url": "https://dataverse.harvard.edu/api/access/datafile/7458695",
                "bytes": 692000190,
                "sha256": "550fde89ac85c258c9fd517638fe34fb42c0e748c9305fe6355761a2bb754170",
            },
        },
        "dated_preregistration_and_embedding_provenance": {
            "prereg_file": "how-we-built-it/PREREG.md",
            "prereg_timestamp_utc": "2026-10-25T22:10:00Z",
            "initial_git_commit": "853db39",
            "initial_git_commit_date_utc": "2026-10-25",
            "static_go_dictionary_source": "Harvard Dataverse datafile/6153417 (gene2go_all.pkl, published May 2023 in Roohani et al., Nature Biotechnology 2024)",
            "static_go_dictionary_sha256": "f145c5e84a53048d87942a417d870a4f2d8db50200b96e492b358c13aba8c771",
            "quartile_definition": "Standard equiprobable quartiles q = [0.25, 0.50, 0.75] (pd.qcut(nn_dist, q=4)) and training-set-only leave-one-out quantiles np.quantile(train_loo_nn_dist, [0.25, 0.50, 0.75]); neither uses any held-out expression target y_test or test score.",
        },
        "reproduction_and_ablation_panel_A_seeds_1_2": repro_panel_a,
        "reproduction_and_ablation_panel_A_test_only_seeds_1_2": repro_panel_a_test_only,
        "five_seed_evaluation_seeds_1_5": five_seed_summary,
        "p2_functional_distance_stratification": p2_strat_dict,
        "null_permutation_controls": {
            ds: {
                "n_permutations_per_seed": 100,
                "total_split_evaluations": 200,
                "real_l2_mean": real_l2,
                "null_l2_mean_avg": round(float(null_l2_arr.mean()), 6),
                "null_l2_mean_sd": round(float(null_l2_arr.std(ddof=1)), 6),
                "null_l2_mean_min": round(float(null_l2_arr.min()), 6),
                "null_l2_mean_max": round(float(null_l2_arr.max()), 6),
                "mean_baseline_l2": mean_base_l2,
                "z_score_l2": round(float(z_l2), 2),
                "empirical_p_l2": round(float(emp_p_l2), 6),
                "real_r2_delta_mean": real_r2d,
                "null_r2_delta_mean_avg": round(float(null_r2d_arr.mean()), 6),
                "null_r2_delta_mean_sd": round(float(null_r2d_arr.std(ddof=1)), 6),
                "null_r2_delta_mean_min": round(float(null_r2d_arr.min()), 6),
                "null_r2_delta_mean_max": round(float(null_r2d_arr.max()), 6),
                "mean_baseline_r2_delta": mean_base_r2d,
                "z_score_r2_delta": round(float(z_r2d), 2),
                "empirical_p_r2_delta": round(float(emp_p_r2d), 6),
            }
        },
        "plain_text_prediction_files": plain_text_files_manifest,
        "runtime_seconds": {
            "replogle_k562_essential_5seed_and_export_sec": t_ds_sec,
            "null_permutation_battery_sec": t_null_sec,
            "total_wall_clock_sec": round(time.time() - t_start_all, 2),
        },
    }

    out_json_path = os.path.join(OBJECT_DIR, "certificate_replogle_k562.json")
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2)
        f.write("\n")
    print(f"Wrote {out_json_path} and {len(plain_text_files_manifest)} plain-text TSVs in {OBJECT_DIR}", flush=True)
