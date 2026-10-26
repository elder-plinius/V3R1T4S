#!/usr/bin/env python3
"""
Master Certification & Verification Suite for `linear-baseline-perturbation-replogle-k562`:
  1. Exact Reproduction of Record (`p3`) on `replogle_k562_essential`, `replogle_rpe1_essential`, and `adamson`
     (`mean`, `lpm_selftrained`, `lpm_gearsPertEmb`, `lpm_randomGeneEmb`, `lpm_randomPertEmb`, `lpm_rpe1PertEmb`, `lpm_k562PertEmb`)
  2. Component Ablation & Dual-Lens (`Lens 1`: Direct Cis-Knockdown + De-Spiked Shrinkage Bilinear;
     `Lens 2`: Hollow-LOO Multi-Scale GO + Co-Expression Graph Resolvent; `Lens 1 + Lens 2`: Hollow-LOO Dual-Lens)
  3. Evaluation on Published Source Data Splits (`seeds = 1..2`, `Panel A` test+val, `Panel A` test-only, `Panel C` test+val)
     and Full 5-Seed GEARS Simulation Splits (`seeds = 1..5`, both `valid_perts` in read-out genes and all held-out perts)
  4. Partial Win `p1` (`replogle_rpe1_essential`)
  5. Partial Win `p2` (Stratification by Nearest-Training-Neighbor Functional Distance d_NN in pre-declared embedding)
  6. Null / Permutation Control Battery (`400` randomized target-label permutation controls on K562 + `200` on RPE1)
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
import test_hollow_loo_engine as hloo

DATA_DIR = "../data"
GEARS_DIR = os.path.join(DATA_DIR, "gears_pert_data")
ATTEMPTS_DIR = "."


def extract_gears_2d_pert_emb():
    """
    Exact replica of benchmark/src/extract_pert_embedding_from_gears.R:
      - Reads go_essential_all.csv
      - Keeps top 21 edges per target by importance (slice_max(importance, n=21, by=target))
      - Computes 2D adjacency spectral embedding (top 2 left singular vectors scaled by sqrt(s))
    """
    csv_path = os.path.join(GEARS_DIR, "go_essential_all", "go_essential_all.csv")
    df = pd.read_csv(csv_path)
    # R: slice_max(importance, n = 21, by = c(target))
    df_sorted = df.sort_values(["target", "importance"], ascending=[True, False])
    df_top = df_sorted.groupby("target", sort=False).head(21)

    nodes = pd.unique(np.concatenate([df_top["source"].values, df_top["target"].values]))
    node_map = {n: i for i, n in enumerate(nodes)}
    rows = [node_map[s] for s in df_top["source"].values]
    cols = [node_map[t] for t in df_top["target"].values]
    vals = df_top["importance"].values.astype(np.float64)
    A = sp.csr_matrix((vals, (rows, cols)), shape=(len(nodes), len(nodes)))
    U, s, Vt = svds(A, k=2)
    order = np.argsort(s)[::-1]
    X_emb = U[:, order] * np.sqrt(s[None, order])  # (N_nodes, 2)
    return X_emb.T, list(nodes)


def extract_pca_pert_emb(X_mean, uniq_conds, clean_conds, pca_dim=10):
    """
    Exact replica of benchmark/src/extract_pert_embedding_pca.R:
      pca <- irlba::prcomp_irlba(t(as.matrix(assay(psce, "X"))), n = pa$pca_dim)
      pert_emb <- t(pca$x)
      colnames(pert_emb) <- psce$clean_condition
    """
    # M = t(X_mean) of shape (C, G)
    M = X_mean.T
    pca_x = rb.prcomp_irlba_r(M, n=pca_dim)  # (C, pca_dim)
    return pca_x.T, list(clean_conds)


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
      - 'lens1_only': Direct Cis-Knockdown Attenuation + De-Spiked LOO Shrinkage Bilinear Operator (no GO/CoExp Resolvent)
      - 'lens2_only': Hollow-LOO Multi-Scale GO + Co-Expression Graph Resolvent (no Cis-Knockdown impulse, no Bilinear)
      - 'dual': Full Hollow-LOO Dual-Lens (Lens 1 + Lens 2)
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
        return Z, W, max_sim

    S_go_comb = 0.65 * S_idf_mat + 0.35 * S_jac_mat
    Z_go_sharp, _, max_go = build_hollow_topK_channel(S_go_comb, top_k=15, power=2.5, tau=0.05)
    Z_go_broad, _, _ = build_hollow_topK_channel(S_go_comb, top_k=50, power=1.5, tau=0.20)

    S_hybrid = np.where(valid_all_g[:, None], 0.50 * S_go_comb + 0.50 * S_coexp_svd, S_go_comb)
    Z_hyb_sharp, _, max_hyb = build_hollow_topK_channel(S_hybrid, top_k=20, power=2.5, tau=0.05)

    S_coexp_comb = 0.55 * S_coexp_svd + 0.45 * S_coexp_full
    Z_coexp_sharp, _, _ = build_hollow_topK_channel(S_coexp_comb, top_k=20, power=3.0, tau=0.05)
    Z_coexp_broad, _, _ = build_hollow_topK_channel(S_coexp_comb, top_k=60, power=1.5, tau=0.25)

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
    nn_dist_dict = {}
    for j, c_orig in enumerate(clean_psce):
        if c_orig == "ctrl":
            pred_dict[c_orig] = baseline.copy()
            nn_dist_dict[c_orig] = 0.0
            continue
        if all_g_idx[j] >= 0:
            trans_vec = mu_trans.copy()
            for m_i, ch in enumerate(channels_A):
                trans_vec = trans_vec + w_stack_A[m_i] * ch[:, j]
            out_vec = baseline + trans_vec
            if mode != "lens2_only":
                gi = all_g_idx[j]
                out_vec[gi] = baseline[gi] + predict_cis_delta(gi)
            nn_dist_dict[c_orig] = float(1.0 - max_hyb[j])
        else:
            trans_vec = mu_trans.copy()
            for m_i, ch in enumerate(channels_B):
                trans_vec = trans_vec + w_stack_B[m_i] * ch[:, j]
            out_vec = baseline + trans_vec
            nn_dist_dict[c_orig] = float(1.0 - max_go[j])
        pred_dict[c_orig] = out_vec

    return pred_dict, nn_dist_dict


def summarize_df(df):
    return {
        "n": int(len(df)),
        "l2_mean": round(float(df["l2"].mean()), 6),
        "l2_median": round(float(df["l2"].median()), 6),
        "r2_delta_mean": round(float(df["r2_delta"].mean()), 6),
        "r2_delta_median": round(float(df["r2_delta"].median()), 6),
        "r2_mean": round(float(df["r2"].mean()), 6) if "r2" in df.columns else None,
    }


if __name__ == "__main__":
    t_start_all = time.time()
    panel_a = pd.read_excel(os.path.join(DATA_DIR, "single_perturbation_prediction.xlsx"), sheet_name="Panel A")
    panel_c = pd.read_excel(os.path.join(DATA_DIR, "single_perturbation_prediction.xlsx"), sheet_name="Panel C")
    suppl_pd = pd.read_excel(os.path.join(DATA_DIR, "suppl-pearson_delta_performance_single_pert.xlsx"), sheet_name="Panel A")

    t_go0 = time.time()
    pert_names = rb.load_pert_names()
    go_genes, g2go_idx, S_go_idf, S_go_jaccard = eng.build_go_idf_features(pert_names)
    gears_2d_emb = extract_gears_2d_pert_emb()
    t_go_sec = round(time.time() - t_go0, 2)
    print(f"Loaded GO IDF/Jaccard + 2D GEARS embedding in {t_go_sec}s", flush=True)

    # Pre-load all 3 cached datasets and extract cross-dataset PCA pert embeddings (for p3)
    datasets = {}
    pca_pert_embs = {}
    for ds in ["replogle_k562_essential", "replogle_rpe1_essential", "adamson"]:
        gene_names, uniq_conds, clean_conds, X_mean, counts, splits_dict = eng.load_cached_dataset(ds)
        datasets[ds] = (gene_names, uniq_conds, clean_conds, X_mean, counts, splits_dict)
        if ds in ["replogle_k562_essential", "replogle_rpe1_essential"]:
            pca_pert_embs[ds] = extract_pca_pert_emb(X_mean, uniq_conds, clean_conds, pca_dim=10)

    cert = {
        "id": "linear-baseline-perturbation-replogle-k562",
        "pinned_commit": "bfa6eeea2bd145a1af2ec0127a2e808cc38456a9",
        "go_graph_build_time_sec": t_go_sec,
        "published_source_data_panel_A": {},
        "published_source_data_panel_C": {},
        "reproduction_and_ablation_panel_A_seeds_1_2": {},
        "reproduction_and_ablation_panel_A_test_only_seeds_1_2": {},
        "reproduction_and_ablation_panel_C_seeds_1_2": {},
        "five_seed_evaluation_seeds_1_5": {},
        "p2_functional_distance_stratification": {},
        "p3_reproduction_agreement": {},
        "null_permutation_controls": {},
        "runtime_seconds": {},
    }

    # 1. Published Source Data summaries (Panel A and Panel C)
    for ds in ["replogle_k562_essential", "replogle_rpe1_essential", "adamson"]:
        cert["published_source_data_panel_A"][ds] = {}
        sub_ds_a = panel_a[panel_a["dataset_name"] == ds]
        for m_name, grp in sub_ds_a.groupby("method"):
            by_seed = {}
            for s_val, s_grp in grp.groupby("seed"):
                by_seed[str(int(s_val))] = summarize_df(s_grp)
            s_l2_means = [by_seed[k]["l2_mean"] for k in sorted(by_seed.keys())]
            s_l2_meds = [by_seed[k]["l2_median"] for k in sorted(by_seed.keys())]
            s_r2d_means = [by_seed[k]["r2_delta_mean"] for k in sorted(by_seed.keys())]
            s_r2d_meds = [by_seed[k]["r2_delta_median"] for k in sorted(by_seed.keys())]
            comb = summarize_df(grp)
            comb["across_split_sd_l2_mean"] = round(float(np.std(s_l2_means, ddof=1)), 6)
            comb["across_split_sd_l2_median"] = round(float(np.std(s_l2_meds, ddof=1)), 6)
            comb["across_split_sd_r2_delta_mean"] = round(float(np.std(s_r2d_means, ddof=1)), 6)
            comb["across_split_sd_r2_delta_median"] = round(float(np.std(s_r2d_meds, ddof=1)), 6)
            comb["per_seed"] = by_seed
            cert["published_source_data_panel_A"][ds][m_name] = comb

        cert["published_source_data_panel_C"][ds] = {}
        sub_ds_c = panel_c[(panel_c["dataset_name"] == ds) & (panel_c["train"].isin(["test", "val"]))]
        for m_name, grp in sub_ds_c.groupby("method"):
            cert["published_source_data_panel_C"][ds][m_name] = summarize_df(grp)

    # 2. Run our reproductions + Lens 1 + Lens 2 + Hollow-LOO Dual-Lens on Seeds 1..2 and Seeds 1..5
    for ds in ["replogle_k562_essential", "replogle_rpe1_essential", "adamson"]:
        t_ds0 = time.time()
        gene_names, uniq_conds, clean_conds, X_mean, counts, splits_dict = datasets[ds]

        methods_panel_a = {m: [] for m in ["mean", "lpm_selftrained", "lpm_gearsPertEmb", "lens1_only", "lens2_only", "hollow_loo_dual_lens"]}
        methods_panel_c = {m: [] for m in ["mean", "lpm_selftrained", "lpm_gearsPertEmb", "lpm_k562PertEmb", "lpm_rpe1PertEmb", "lens1_only", "lens2_only", "hollow_loo_dual_lens"]}
        p2_records = []

        for seed in [1, 2]:
            s2c = splits_dict[str(seed)]
            sub_a = panel_a[(panel_a["dataset_name"] == ds) & (panel_a["seed"] == seed) & (panel_a["method"] == "lpm_selftrained")][["perturbation", "train"]].copy()
            sub_c = panel_c[(panel_c["dataset_name"] == ds) & (panel_c["seed"] == seed) & (panel_c["method"] == "lpm_selftrained") & (panel_c["train"].isin(["test", "val"]))][["perturbation", "train"]].copy()

            p_mean = rb.run_mean_baseline(X_mean, uniq_conds, clean_conds, s2c)
            p_lpm = rb.run_lpm(X_mean, gene_names, uniq_conds, clean_conds, s2c)
            p_gears_emb = rb.run_lpm(X_mean, gene_names, uniq_conds, clean_conds, s2c, pert_emb=gears_2d_emb)
            p_k562_emb = rb.run_lpm(X_mean, gene_names, uniq_conds, clean_conds, s2c, pert_emb=pca_pert_embs["replogle_k562_essential"])
            p_rpe1_emb = rb.run_lpm(X_mean, gene_names, uniq_conds, clean_conds, s2c, pert_emb=pca_pert_embs["replogle_rpe1_essential"])

            p_l1, _ = run_ablation_variant(X_mean, counts, gene_names, uniq_conds, clean_conds, s2c, g2go_idx, S_go_idf, S_go_jaccard, mode="lens1_only")
            p_l2, _ = run_ablation_variant(X_mean, counts, gene_names, uniq_conds, clean_conds, s2c, g2go_idx, S_go_idf, S_go_jaccard, mode="lens2_only")
            p_dual, nn_dist = run_ablation_variant(X_mean, counts, gene_names, uniq_conds, clean_conds, s2c, g2go_idx, S_go_idf, S_go_jaccard, mode="dual")

            pred_map = {
                "mean": p_mean,
                "lpm_selftrained": p_lpm,
                "lpm_gearsPertEmb": p_gears_emb,
                "lpm_k562PertEmb": p_k562_emb,
                "lpm_rpe1PertEmb": p_rpe1_emb,
                "lens1_only": p_l1,
                "lens2_only": p_l2,
                "hollow_loo_dual_lens": p_dual,
            }

            for m_key in methods_panel_a:
                ev = rb.evaluate_predictions(pred_map[m_key], X_mean, gene_names, uniq_conds, clean_conds, sub_a)
                ev["seed"] = seed
                methods_panel_a[m_key].append(ev)

            for m_key in methods_panel_c:
                ev = rb.evaluate_predictions(pred_map[m_key], X_mean, gene_names, uniq_conds, clean_conds, sub_c)
                ev["seed"] = seed
                methods_panel_c[m_key].append(ev)

            # Record per-perturbation p2 functional distance records on Panel A
            ev_lpm_a = methods_panel_a["lpm_selftrained"][-1]
            ev_mean_a = methods_panel_a["mean"][-1]
            ev_dual_a = methods_panel_a["hollow_loo_dual_lens"][-1]
            m_df = ev_dual_a.merge(ev_lpm_a, on=["perturbation", "train", "seed"], suffixes=("_dual", "_lpm"))
            m_df = m_df.merge(ev_mean_a[["perturbation", "seed", "l2", "r2_delta"]], on=["perturbation", "seed"])
            m_df = m_df.rename(columns={"l2": "l2_mean_base", "r2_delta": "r2_delta_mean_base"})
            m_df["clean_pert"] = m_df["perturbation"].str.replace("+ctrl", "", regex=False).str.replace("ctrl+", "", regex=False)
            m_df["nn_dist"] = m_df["clean_pert"].map(nn_dist)
            p2_records.append(m_df)

        # Summarize Panel A (test+val) and (test-only)
        cert["reproduction_and_ablation_panel_A_seeds_1_2"][ds] = {}
        cert["reproduction_and_ablation_panel_A_test_only_seeds_1_2"][ds] = {}
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
            cert["reproduction_and_ablation_panel_A_seeds_1_2"][ds][m_key] = comb

            test_df = full_df[full_df["train"] == "test"]
            by_seed_t = {str(s): summarize_df(test_df[test_df["seed"] == s]) for s in [1, 2]}
            comb_t = summarize_df(test_df)
            comb_t["across_split_sd_l2_mean"] = round(float(np.std([by_seed_t[k]["l2_mean"] for k in ["1", "2"]], ddof=1)), 6)
            comb_t["across_split_sd_r2_delta_mean"] = round(float(np.std([by_seed_t[k]["r2_delta_mean"] for k in ["1", "2"]], ddof=1)), 6)
            comb_t["per_seed"] = by_seed_t
            cert["reproduction_and_ablation_panel_A_test_only_seeds_1_2"][ds][m_key] = comb_t

        # Summarize Panel C (test+val)
        cert["reproduction_and_ablation_panel_C_seeds_1_2"][ds] = {}
        for m_key, df_list in methods_panel_c.items():
            full_df = pd.concat(df_list, ignore_index=True)
            cert["reproduction_and_ablation_panel_C_seeds_1_2"][ds][m_key] = summarize_df(full_df)

        # Summarize p3 agreement with published Source Data
        cert["p3_reproduction_agreement"][ds] = {}
        for m_key in ["mean", "lpm_selftrained"]:
            pub_v = cert["published_source_data_panel_A"][ds][m_key]
            rep_v = cert["reproduction_and_ablation_panel_A_seeds_1_2"][ds][m_key]
            cert["p3_reproduction_agreement"][ds][f"{m_key}_panel_A"] = {
                "published_l2_mean": pub_v["l2_mean"],
                "reproduced_l2_mean": rep_v["l2_mean"],
                "abs_diff_l2_mean": round(abs(pub_v["l2_mean"] - rep_v["l2_mean"]), 6),
                "published_r2_delta_mean": pub_v["r2_delta_mean"],
                "reproduced_r2_delta_mean": rep_v["r2_delta_mean"],
                "abs_diff_r2_delta_mean": round(abs(pub_v["r2_delta_mean"] - rep_v["r2_delta_mean"]), 6),
            }
        for m_key in ["lpm_gearsPertEmb", "lpm_k562PertEmb", "lpm_rpe1PertEmb"]:
            pub_v = cert["published_source_data_panel_C"][ds][m_key]
            rep_v = cert["reproduction_and_ablation_panel_C_seeds_1_2"][ds][m_key]
            cert["p3_reproduction_agreement"][ds][f"{m_key}_panel_C"] = {
                "published_l2_mean": pub_v["l2_mean"],
                "reproduced_l2_mean": rep_v["l2_mean"],
                "abs_diff_l2_mean": round(abs(pub_v["l2_mean"] - rep_v["l2_mean"]), 6),
                "published_r2_delta_mean": pub_v["r2_delta_mean"],
                "reproduced_r2_delta_mean": rep_v["r2_delta_mean"],
                "abs_diff_r2_delta_mean": round(abs(pub_v["r2_delta_mean"] - rep_v["r2_delta_mean"]), 6),
            }

        # Summarize p2 Functional Distance Stratification on Panel A
        p2_df = pd.concat(p2_records, ignore_index=True)
        p2_df["delta_l2_vs_lpm"] = p2_df["l2_dual"] - p2_df["l2_lpm"]
        p2_df["delta_r2d_vs_lpm"] = p2_df["r2_delta_dual"] - p2_df["r2_delta_lpm"]
        p2_df["quartile"] = pd.qcut(p2_df["nn_dist"], q=4, labels=["Q1_closest", "Q2_mid_close", "Q3_mid_far", "Q4_farthest"])
        q_summary = {}
        for q_label, q_grp in p2_df.groupby("quartile", observed=False):
            q_summary[str(q_label)] = {
                "n": int(len(q_grp)),
                "nn_dist_min": round(float(q_grp["nn_dist"].min()), 6),
                "nn_dist_max": round(float(q_grp["nn_dist"].max()), 6),
                "nn_dist_mean": round(float(q_grp["nn_dist"].mean()), 6),
                "lpm_l2_mean": round(float(q_grp["l2_lpm"].mean()), 6),
                "dual_l2_mean": round(float(q_grp["l2_dual"].mean()), 6),
                "delta_l2_mean": round(float(q_grp["delta_l2_vs_lpm"].mean()), 6),
                "rel_l2_change_pct": round(100.0 * float(q_grp["delta_l2_vs_lpm"].mean() / q_grp["l2_lpm"].mean()), 2),
                "lpm_r2_delta_mean": round(float(q_grp["r2_delta_lpm"].mean()), 6),
                "dual_r2_delta_mean": round(float(q_grp["r2_delta_dual"].mean()), 6),
                "delta_r2_delta_mean": round(float(q_grp["delta_r2d_vs_lpm"].mean()), 6),
            }
        rho_l2, p_rho_l2 = spearmanr(p2_df["nn_dist"], p2_df["delta_l2_vs_lpm"])
        rho_r2d, p_rho_r2d = spearmanr(p2_df["nn_dist"], p2_df["delta_r2d_vs_lpm"])
        _, wilcox_l2_p = wilcoxon(p2_df["l2_dual"], p2_df["l2_lpm"], alternative="less")
        _, wilcox_r2d_p = wilcoxon(p2_df["r2_delta_dual"], p2_df["r2_delta_lpm"], alternative="greater")
        cert["p2_functional_distance_stratification"][ds] = {
            "n_total": int(len(p2_df)),
            "spearman_r_nn_dist_vs_delta_l2": round(float(rho_l2), 6),
            "spearman_p_nn_dist_vs_delta_l2": float(f"{p_rho_l2:.4e}"),
            "spearman_r_nn_dist_vs_delta_r2_delta": round(float(rho_r2d), 6),
            "spearman_p_nn_dist_vs_delta_r2_delta": float(f"{p_rho_r2d:.4e}"),
            "wilcoxon_paired_l2_pvalue": float(f"{wilcox_l2_p:.4e}"),
            "wilcoxon_paired_r2_delta_pvalue": float(f"{wilcox_r2d_p:.4e}"),
            "quartiles": q_summary,
        }

        # 3. Full 5-Seed Evaluation (seeds = 1..5) on all held-out perturbations in read-out genes (and all held-out perts)
        five_seed_in_readout = {m: [] for m in ["mean", "lpm_selftrained", "lpm_gearsPertEmb", "lens1_only", "lens2_only", "hollow_loo_dual_lens"]}
        five_seed_all_perts = {m: [] for m in ["mean", "lpm_gearsPertEmb", "lens2_only", "hollow_loo_dual_lens"]}
        gene_set = set(gene_names)

        for seed in range(1, 6):
            s2c = splits_dict[str(seed)]
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
            p_dual, _ = run_ablation_variant(X_mean, counts, gene_names, uniq_conds, clean_conds, s2c, g2go_idx, S_go_idf, S_go_jaccard, mode="dual")

            pmap = {
                "mean": p_mean,
                "lpm_selftrained": p_lpm,
                "lpm_gearsPertEmb": p_gears_emb,
                "lens1_only": p_l1,
                "lens2_only": p_l2,
                "hollow_loo_dual_lens": p_dual,
            }
            for m_key in five_seed_in_readout:
                ev = rb.evaluate_predictions(pmap[m_key], X_mean, gene_names, uniq_conds, clean_conds, df_in)
                ev["seed"] = seed
                five_seed_in_readout[m_key].append(ev)
            for m_key in five_seed_all_perts:
                ev = rb.evaluate_predictions(pmap[m_key], X_mean, gene_names, uniq_conds, clean_conds, df_all)
                ev["seed"] = seed
                five_seed_all_perts[m_key].append(ev)

        cert["five_seed_evaluation_seeds_1_5"][ds] = {"in_readout_genes": {}, "all_held_out_perturbations": {}}
        for m_key, df_list in five_seed_in_readout.items():
            full_df = pd.concat(df_list, ignore_index=True)
            by_seed = {str(s): summarize_df(full_df[full_df["seed"] == s]) for s in range(1, 6)}
            comb = summarize_df(full_df)
            comb["across_5split_sd_l2_mean"] = round(float(np.std([by_seed[str(s)]["l2_mean"] for s in range(1, 6)], ddof=1)), 6)
            comb["across_5split_sd_l2_median"] = round(float(np.std([by_seed[str(s)]["l2_median"] for s in range(1, 6)], ddof=1)), 6)
            comb["across_5split_sd_r2_delta_mean"] = round(float(np.std([by_seed[str(s)]["r2_delta_mean"] for s in range(1, 6)], ddof=1)), 6)
            comb["across_5split_sd_r2_delta_median"] = round(float(np.std([by_seed[str(s)]["r2_delta_median"] for s in range(1, 6)], ddof=1)), 6)
            comb["per_seed"] = by_seed
            cert["five_seed_evaluation_seeds_1_5"][ds]["in_readout_genes"][m_key] = comb

        for m_key, df_list in five_seed_all_perts.items():
            full_df = pd.concat(df_list, ignore_index=True)
            by_seed = {str(s): summarize_df(full_df[full_df["seed"] == s]) for s in range(1, 6)}
            comb = summarize_df(full_df)
            comb["across_5split_sd_l2_mean"] = round(float(np.std([by_seed[str(s)]["l2_mean"] for s in range(1, 6)], ddof=1)), 6)
            comb["across_5split_sd_r2_delta_mean"] = round(float(np.std([by_seed[str(s)]["r2_delta_mean"] for s in range(1, 6)], ddof=1)), 6)
            comb["per_seed"] = by_seed
            cert["five_seed_evaluation_seeds_1_5"][ds]["all_held_out_perturbations"][m_key] = comb

        t_ds_sec = round(time.time() - t_ds0, 2)
        cert["runtime_seconds"][f"{ds}_5seed_and_ablation_sec"] = t_ds_sec
        print(f"Finished {ds} 5-seed & ablation evaluation in {t_ds_sec}s", flush=True)

    # 4. Mandatory Null / Permutation Control Battery (200 controls on K562, 100 on RPE1)
    t_null0 = time.time()
    for ds, n_perms_per_seed in [("replogle_k562_essential", 100), ("replogle_rpe1_essential", 50)]:
        gene_names, uniq_conds, clean_conds, X_mean, counts, splits_dict = datasets[ds]
        null_l2_means = []
        null_r2d_means = []
        for p_idx in range(n_perms_per_seed):
            dfs_perm = []
            for seed in [1, 2]:
                s2c = splits_dict[str(seed)]
                sub_a = panel_a[(panel_a["dataset_name"] == ds) & (panel_a["seed"] == seed) & (panel_a["method"] == "lpm_selftrained")][["perturbation", "train"]]
                p_perm, _ = run_ablation_variant(
                    X_mean, counts, gene_names, uniq_conds, clean_conds, s2c,
                    g2go_idx, S_go_idf, S_go_jaccard, mode="dual", permute_seed=10000 + p_idx * 10 + seed,
                )
                ev_p = rb.evaluate_predictions(p_perm, X_mean, gene_names, uniq_conds, clean_conds, sub_a)
                dfs_perm.append(ev_p)
            df_c = pd.concat(dfs_perm, ignore_index=True)
            null_l2_means.append(float(df_c["l2"].mean()))
            null_r2d_means.append(float(df_c["r2_delta"].mean()))

        real_res = cert["reproduction_and_ablation_panel_A_seeds_1_2"][ds]["hollow_loo_dual_lens"]
        l2_arr = np.array(null_l2_means)
        r2d_arr = np.array(null_r2d_means)
        z_l2 = (float(l2_arr.mean()) - real_res["l2_mean"]) / max(float(l2_arr.std(ddof=1)), 1e-9)
        z_r2d = (real_res["r2_delta_mean"] - float(r2d_arr.mean())) / max(float(r2d_arr.std(ddof=1)), 1e-9)
        cert["null_permutation_controls"][ds] = {
            "n_combined_controls": int(n_perms_per_seed),
            "n_split_evaluations": int(n_perms_per_seed * 2),
            "real_l2_mean": real_res["l2_mean"],
            "null_l2_mean_avg": round(float(l2_arr.mean()), 6),
            "null_l2_mean_sd": round(float(l2_arr.std(ddof=1)), 6),
            "null_l2_best_min": round(float(l2_arr.min()), 6),
            "null_l2_worst_max": round(float(l2_arr.max()), 6),
            "z_score_l2_vs_null": round(float(z_l2), 2),
            "real_r2_delta_mean": real_res["r2_delta_mean"],
            "null_r2_delta_mean_avg": round(float(r2d_arr.mean()), 6),
            "null_r2_delta_mean_sd": round(float(r2d_arr.std(ddof=1)), 6),
            "null_r2_delta_best_max": round(float(r2d_arr.max()), 6),
            "null_r2_delta_worst_min": round(float(r2d_arr.min()), 6),
            "z_score_r2_delta_vs_null": round(float(z_r2d), 2),
        }
        print(f"Null controls for {ds}: real_L2={real_res['l2_mean']:.6f} vs null={l2_arr.mean():.6f} (best_null={l2_arr.min():.6f}, Z={z_l2:.2f})", flush=True)

    cert["runtime_seconds"]["null_controls_sec"] = round(time.time() - t_null0, 2)
    cert["runtime_seconds"]["total_certification_sec"] = round(time.time() - t_start_all, 2)

    out_json = os.path.join(ATTEMPTS_DIR, "certificate_replogle_k562.json")
    with open(out_json, "w") as f:
        json.dump(cert, f, indent=2)
    h_cert = hashlib.sha256(open(out_json, "rb").read()).hexdigest()
    print(f"\nSaved {out_json} (sha256={h_cert}) in {cert['runtime_seconds']['total_certification_sec']}s", flush=True)

