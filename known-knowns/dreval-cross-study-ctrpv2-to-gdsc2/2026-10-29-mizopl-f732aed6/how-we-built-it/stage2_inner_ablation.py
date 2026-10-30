#!/usr/bin/env python3
"""
Stage 2 Air-Gapped Inner Validation & Ablation on CTRPv2 (LCO, LTO, LDO).
STRICT AIR-GAP RULE (Anti-Trap #1):
  This script ONLY loads CTRPv2 and meta/gene_lists.
  Zero external datasets are referenced or loaded.
"""
import os
import json
import time
import numpy as np
import pandas as pd
from scipy.stats import rankdata, norm, spearmanr
from scipy.linalg import solve
import torch
import torch.nn as nn

os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
os.environ["OPENBLAS_NUM_THREADS"] = "4"
torch.set_num_threads(4)

from drevalpy.datasets.loader import load_ctrpv2

DATA_DIR = "DREVAL_CAMPAIGN/data"


def load_ctrpv2_all_views():
    t0 = time.time()
    ge_inter = pd.read_csv(f"{DATA_DIR}/meta/gene_lists/gene_expression_intersection.csv")["Symbol"].tolist()
    lm_genes_raw = pd.read_csv(f"{DATA_DIR}/meta/gene_lists/landmark_genes.csv")["Symbol"].tolist()
    dt_genes_raw = pd.read_csv(f"{DATA_DIR}/meta/gene_lists/drug_target_genes_all_drugs.csv")["Symbol"].tolist()
    pm_genes_raw = pd.read_csv(f"{DATA_DIR}/meta/gene_lists/gene_list_paccmann_network_prop.csv")["Symbol"].tolist()

    with open(f"{DATA_DIR}/CTRPv2/DIPK_features/gene_list_sel.txt", encoding="gbk") as f:
        bionic_sel = [line.strip() for line in f if line.strip()]
    ppi_df = pd.read_csv(f"{DATA_DIR}/CTRPv2/DIPK_features/human_ppi_features.tsv", index_col=0, sep="\t")
    ge_header = set(pd.read_csv(f"{DATA_DIR}/CTRPv2/gene_expression.csv", nrows=0).columns.tolist())

    valid_bionic_genes = [g for g in bionic_sel if g in ppi_df.index and g in ge_header]
    lm_genes = [g for g in lm_genes_raw if g in ge_header]
    dt_genes = [g for g in dt_genes_raw if g in ge_header]
    pm_genes = [g for g in pm_genes_raw if g in ge_header]

    union_genes = sorted(list(set(ge_inter) | set(valid_bionic_genes) | set(lm_genes) | set(dt_genes) | set(pm_genes)))
    ge_full = pd.read_csv(f"{DATA_DIR}/CTRPv2/gene_expression.csv", usecols=["cell_line_name"] + union_genes)
    ge_full["cell_line_name"] = ge_full["cell_line_name"].astype(str)
    ge_full = ge_full.groupby("cell_line_name", sort=False).mean()

    ge_df = ge_full[ge_inter].astype(np.float32)
    ge_lm_df = ge_full[lm_genes].astype(np.float32)
    ge_dt_df = ge_full[dt_genes].astype(np.float32)

    # BIONIC top-256 PPI pooling (100% rank-invariant within cell line)
    ge_b_vals = ge_full[valid_bionic_genes].values
    ppi_mat = ppi_df.loc[valid_bionic_genes].values.astype(np.float32)
    top256_idx = np.argpartition(-ge_b_vals, kth=min(256, ge_b_vals.shape[1] - 1), axis=1)[:, :256]
    bionic_mat = np.mean(ppi_mat[top256_idx], axis=1)
    bionic_df = pd.DataFrame(bionic_mat, index=ge_full.index)

    pw_df = pd.read_csv(f"{DATA_DIR}/CTRPv2/pathway_features.csv", index_col=0)
    pw_df.index = pw_df.index.astype(str)
    pw_df = pw_df.groupby(level=0, sort=False).mean().astype(np.float32)

    cl_names = pd.read_csv(f"{DATA_DIR}/CTRPv2/cell_line_names.csv", dtype=str).drop_duplicates("cell_line_name")
    cl_to_tissue = dict(zip(cl_names["cell_line_name"], cl_names["tissue"]))

    fp2048 = pd.read_csv(f"{DATA_DIR}/CTRPv2/drug_fingerprints/pubchem_id_to_demorgan_2048_map.csv", index_col=None).T
    fp2048.index = fp2048.index.astype(str)
    has_fp = np.ones(len(fp2048), dtype=bool)
    for idx_i, drug in enumerate(fp2048.index):
        if fp2048.loc[drug].isna().all():
            has_fp[idx_i] = False
            rng = np.random.default_rng(hash(drug) % (2**32))
            fp2048.loc[drug] = rng.integers(0, 2, size=fp2048.shape[1])
    fp2048 = fp2048.astype(np.float32)
    has_fp_series = pd.Series(has_fp, index=fp2048.index)

    cb_df = pd.read_csv(f"{DATA_DIR}/CTRPv2/drug_chemberta_embeddings.csv", dtype={"pubchem_id": str}).set_index("pubchem_id")
    cb_df = cb_df.groupby(level=0, sort=False).mean().astype(np.float32)

    sv_df = pd.read_csv(f"{DATA_DIR}/CTRPv2/drug_smilesvec.csv", dtype={"pubchem_id": str}).set_index("pubchem_id")
    sv_df = sv_df.groupby(level=0, sort=False).mean().astype(np.float32)

    drug_names_df = pd.read_csv(f"{DATA_DIR}/CTRPv2/drug_names.csv", dtype=str)
    pubchem_to_name = dict(zip(drug_names_df["pubchem_id"], drug_names_df["drug_name"]))

    dt_set, lm_set, pm_set = set(dt_genes), set(lm_genes), set(pm_genes)
    gene_weights = np.ones(len(ge_inter), dtype=np.float32)
    for i, g in enumerate(ge_inter):
        if g in dt_set:
            gene_weights[i] += 0.6
        if g in lm_set:
            gene_weights[i] += 0.3
        if g in pm_set:
            gene_weights[i] += 0.15

    print(f"Loaded all CTRPv2 views in {time.time()-t0:.2f}s")
    return {
        "ge_df": ge_df,
        "ge_lm_df": ge_lm_df,
        "ge_dt_df": ge_dt_df,
        "pw_df": pw_df,
        "bionic_df": bionic_df,
        "cl_to_tissue": cl_to_tissue,
        "fp2048": fp2048,
        "has_fp": has_fp_series,
        "cb_df": cb_df,
        "sv_df": sv_df,
        "pubchem_to_name": pubchem_to_name,
        "gene_weights": gene_weights,
    }


def within_sample_vdw(mat: np.ndarray) -> np.ndarray:
    n, g = mat.shape
    ranks = np.empty_like(mat, dtype=np.float64)
    for i in range(n):
        ranks[i] = rankdata(mat[i], method="average")
    return norm.ppf(ranks / (g + 1.0)).astype(np.float32)


def within_sample_log_zscore(mat: np.ndarray) -> np.ndarray:
    x = mat.astype(np.float64).copy()
    if np.nanmax(x) > 50.0:
        x = np.log2(np.maximum(x, 0.0) + 1.0)
    mu = np.mean(x, axis=1, keepdims=True)
    sd = np.std(x, axis=1, ddof=1, keepdims=True)
    sd = np.where(sd < 1e-8, 1.0, sd)
    return ((x - mu) / sd).astype(np.float32)


def precompute_cell_views(views):
    ge_df = views["ge_df"]
    cl_ids = sorted(list(set(ge_df.index) & set(views["cl_to_tissue"].keys())))
    ge_mat = ge_df.loc[cl_ids].values
    vdw_mat = within_sample_vdw(ge_mat)
    logz_mat = within_sample_log_zscore(ge_mat)

    lm_mat = views["ge_lm_df"].loc[cl_ids].values
    lm_vdw = within_sample_vdw(lm_mat)
    lm_logz = within_sample_log_zscore(lm_mat)

    dt_mat = views["ge_dt_df"].loc[cl_ids].values
    dt_vdw = within_sample_vdw(dt_mat)
    dt_logz = within_sample_log_zscore(dt_mat)

    pw_mat = views["pw_df"].reindex(cl_ids).fillna(0.0).values
    pw_vdw = within_sample_vdw(pw_mat)
    bionic_mat = views["bionic_df"].reindex(cl_ids).fillna(0.0).values
    return {
        "cl_ids": cl_ids,
        "cl_to_idx": {c: i for i, c in enumerate(cl_ids)},
        "vdw": vdw_mat,
        "logz": logz_mat,
        "lm_vdw": lm_vdw,
        "lm_logz": lm_logz,
        "dt_vdw": dt_vdw,
        "dt_logz": dt_logz,
        "pw_vdw": pw_vdw,
        "pw_raw": pw_mat,
        "bionic": bionic_mat,
        "gene_weights": views["gene_weights"],
    }


def precompute_drug_views(views):
    fp_df = views["fp2048"]
    drug_ids = sorted(list(fp_df.index))
    fp_mat = fp_df.loc[drug_ids].values.astype(np.float32)
    has_fp = views["has_fp"].loc[drug_ids].values

    dot = fp_mat @ fp_mat.T
    norms = np.sum(fp_mat, axis=1, keepdims=True)
    denom = norms + norms.T - dot
    tanimoto = np.where(denom > 0, dot / np.maximum(denom, 1e-8), 0.0).astype(np.float32)
    invalid_mask = ~has_fp
    tanimoto[invalid_mask, :] = 0.0
    tanimoto[:, invalid_mask] = 0.0
    np.fill_diagonal(tanimoto, 1.0)

    cb_df = views["cb_df"]
    has_cb = np.array([d in cb_df.index for d in drug_ids], dtype=bool)
    cb_mat = cb_df.reindex(drug_ids).fillna(0.0).values.astype(np.float32)
    cb_norm = cb_mat / np.maximum(np.linalg.norm(cb_mat, axis=1, keepdims=True), 1e-8)
    cb_sim = np.clip(((cb_norm @ cb_norm.T) + 1.0) * 0.5, 0.0, 1.0).astype(np.float32)
    cb_sim[~has_cb, :] = 0.0
    cb_sim[:, ~has_cb] = 0.0
    np.fill_diagonal(cb_sim, 1.0)

    sv_df = views["sv_df"]
    has_sv = np.array([d in sv_df.index for d in drug_ids], dtype=bool)
    sv_mat = sv_df.reindex(drug_ids).fillna(0.0).values.astype(np.float32)
    sv_norm = sv_mat / np.maximum(np.linalg.norm(sv_mat, axis=1, keepdims=True), 1e-8)
    sv_sim = np.clip(((sv_norm @ sv_norm.T) + 1.0) * 0.5, 0.0, 1.0).astype(np.float32)
    sv_sim[~has_sv, :] = 0.0
    sv_sim[:, ~has_sv] = 0.0
    np.fill_diagonal(sv_sim, 1.0)

    K_drug = 0.50 * tanimoto + 0.30 * cb_sim + 0.20 * sv_sim

    drug_feat_concat = np.concatenate([
        fp_mat,
        cb_norm,
        sv_norm,
        has_fp[:, None].astype(np.float32),
        has_cb[:, None].astype(np.float32),
    ], axis=1)

    return {
        "drug_ids": drug_ids,
        "drug_to_idx": {d: i for i, d in enumerate(drug_ids)},
        "fp_mat": fp_mat,
        "cb_mat": cb_mat,
        "sv_mat": sv_mat,
        "drug_feat_concat": drug_feat_concat,
        "has_fp": has_fp,
        "has_cb": has_cb,
        "has_sv": has_sv,
        "tanimoto": tanimoto,
        "cb_sim": cb_sim,
        "sv_sim": sv_sim,
        "K_drug": K_drug,
    }


def build_cell_kernel_and_features(cell_cache, train_cl_idx, all_cl_idx, tissues_all, train_tissues_set):
    gw = cell_cache["gene_weights"][None, :]

    def std_view(mat, weight=None):
        tr = mat[train_cl_idx]
        mu = np.mean(tr, axis=0, keepdims=True)
        sd = np.std(tr, axis=0, keepdims=True)
        sd = np.where(sd < 1e-6, 1.0, sd)
        z = (mat[all_cl_idx] - mu) / sd
        if weight is not None:
            z = z * weight
        norms = np.maximum(np.linalg.norm(z, axis=1, keepdims=True), 1e-8)
        z_cos = z / norms
        z_lin = z / np.sqrt(z.shape[1])
        return z_cos.astype(np.float32), z_lin.astype(np.float32)

    vdw_cos, vdw_lin = std_view(cell_cache["vdw"], gw)
    logz_cos, logz_lin = std_view(cell_cache["logz"], gw)
    lm_cos, lm_lin = std_view(0.55 * cell_cache["lm_vdw"] + 0.45 * cell_cache["lm_logz"])
    dt_cos, dt_lin = std_view(0.55 * cell_cache["dt_vdw"] + 0.45 * cell_cache["dt_logz"])
    pw_cos, pw_lin = std_view(cell_cache["pw_vdw"])
    bio_cos, bio_lin = std_view(cell_cache["bionic"])

    t_list = sorted(list(train_tissues_set))
    t_to_i = {t: i for i, t in enumerate(t_list)}
    T_mat = np.zeros((len(all_cl_idx), len(t_list)), dtype=np.float32)
    for row_i, t in enumerate(tissues_all):
        if t in t_to_i:
            T_mat[row_i, t_to_i[t]] = 1.0

    pos_map = {orig_i: p for p, orig_i in enumerate(all_cl_idx)}
    tr_pos = np.array([pos_map[i] for i in train_cl_idx], dtype=np.int64)

    def k_pair(c_mat, l_mat):
        return 0.60 * (c_mat @ c_mat[tr_pos].T) + 0.40 * (l_mat @ l_mat[tr_pos].T)

    K_vdw = k_pair(vdw_cos, vdw_lin)
    K_logz = k_pair(logz_cos, logz_lin)
    K_lm = k_pair(lm_cos, lm_lin)
    K_dt = k_pair(dt_cos, dt_lin)
    K_pw = k_pair(pw_cos, pw_lin)
    K_bio = k_pair(bio_cos, bio_lin)
    K_tis = T_mat @ T_mat[tr_pos].T

    Z_comb = np.concatenate([
        0.45 * vdw_cos,
        0.35 * logz_cos,
        0.35 * lm_cos,
        0.35 * dt_cos,
        0.35 * pw_cos,
        0.25 * bio_cos,
    ], axis=1)
    sq_norms_all = np.sum(Z_comb ** 2, axis=1, keepdims=True)
    sq_norms_tr = np.sum(Z_comb[tr_pos] ** 2, axis=1, keepdims=True).T
    dist2 = np.maximum(sq_norms_all + sq_norms_tr - 2.0 * (Z_comb @ Z_comb[tr_pos].T), 0.0)
    median_d2 = float(np.median(dist2[tr_pos])) if len(tr_pos) > 1 else 1.0
    K_rbf = np.exp(-dist2 / max(median_d2, 1e-4)).astype(np.float32)

    X_cell_nn = np.concatenate([
        vdw_lin,
        lm_lin,
        dt_lin,
        pw_lin,
        bio_lin,
        0.25 * T_mat,
    ], axis=1).astype(np.float32)

    return {
        "K_vdw": K_vdw,
        "K_logz": K_logz,
        "K_lm": K_lm,
        "K_dt": K_dt,
        "K_pw": K_pw,
        "K_bio": K_bio,
        "K_tis": K_tis,
        "K_rbf": K_rbf,
        "X_cell_nn": X_cell_nn,
        "tr_pos": tr_pos,
    }


class _FullMatrixBilinearNet(nn.Module):
    """Fast Full-Matrix Residual Two-Tower Bilinear Network over Multi-View Cell & Drug Representations."""

    def __init__(self, cell_dim: int, drug_dim: int, n_drugs: int, hidden_dim: int = 256, emb_dim: int = 128, dropout: float = 0.25):
        super().__init__()
        self.c_in = nn.Linear(cell_dim, hidden_dim)
        self.c_ln1 = nn.LayerNorm(hidden_dim)
        self.c_fc1 = nn.Linear(hidden_dim, hidden_dim)
        self.c_ln2 = nn.LayerNorm(hidden_dim)
        self.c_out = nn.Linear(hidden_dim, emb_dim)
        self.c_skip = nn.Linear(cell_dim, emb_dim)
        self.c_bias = nn.Linear(emb_dim, 1)

        self.d_in = nn.Linear(drug_dim, hidden_dim)
        self.d_ln1 = nn.LayerNorm(hidden_dim)
        self.d_fc1 = nn.Linear(hidden_dim, hidden_dim)
        self.d_ln2 = nn.LayerNorm(hidden_dim)
        self.d_out = nn.Linear(hidden_dim, emb_dim)
        self.d_skip = nn.Linear(drug_dim, emb_dim)
        self.d_id_emb = nn.Embedding(n_drugs, emb_dim)
        nn.init.normal_(self.d_id_emb.weight, std=0.02)
        self.d_bias = nn.Linear(emb_dim, 1)

        self.drop = nn.Dropout(dropout)
        self.act = nn.GELU()
        self.scale = nn.Parameter(torch.tensor(float(1.0 / np.sqrt(emb_dim)), dtype=torch.float32))

    def encode_cells(self, x_c: torch.Tensor) -> torch.Tensor:
        h0 = self.act(self.c_ln1(self.c_in(x_c)))
        h = self.drop(self.act(self.c_ln2(self.c_fc1(self.drop(h0))))) + h0
        return self.c_out(h) + self.c_skip(x_c)

    def encode_drugs(self, x_d: torch.Tensor, use_id_emb: bool = True) -> torch.Tensor:
        h0 = self.act(self.d_ln1(self.d_in(x_d)))
        h = self.drop(self.act(self.d_ln2(self.d_fc1(self.drop(h0))))) + h0
        z_d = self.d_out(h) + self.d_skip(x_d)
        if use_id_emb:
            z_d = z_d + self.d_id_emb.weight
        return z_d

    def forward_matrix(self, x_c: torch.Tensor, x_d: torch.Tensor, use_id_emb: bool = True) -> torch.Tensor:
        z_c = self.encode_cells(x_c)
        z_d = self.encode_drugs(x_d, use_id_emb=use_id_emb)
        return (z_c @ z_d.T) * self.scale + self.c_bias(z_c) + self.d_bias(z_d).T


def train_and_predict_neural_bilinear(
    X_cell_all: np.ndarray,
    tr_pos: np.ndarray,
    X_drug_tr: np.ndarray,
    R_target: np.ndarray,
    M_obs: np.ndarray,
    n_ensemble: int = 5,
    epochs: int = 115,
    lr: float = 1.5e-3,
    seed: int = 42,
) -> np.ndarray:
    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    x_c_all_t = torch.tensor(X_cell_all, dtype=torch.float32, device=device)
    x_c_tr_t = x_c_all_t[tr_pos]
    x_d_tr_t = torch.tensor(X_drug_tr, dtype=torch.float32, device=device)
    r_t = torch.tensor(np.nan_to_num(R_target, nan=0.0), dtype=torch.float32, device=device)
    m_t = torch.tensor(M_obs.astype(np.float32), dtype=torch.float32, device=device)
    m_sum = torch.sum(m_t)

    n_tr_cl, n_tr_dr = R_target.shape
    preds_accum = np.zeros((len(X_cell_all), n_tr_dr), dtype=np.float32)

    for m_idx in range(n_ensemble):
        torch.manual_seed(seed + 101 * m_idx)
        net = _FullMatrixBilinearNet(
            cell_dim=X_cell_all.shape[1],
            drug_dim=X_drug_tr.shape[1],
            n_drugs=n_tr_dr,
            hidden_dim=256,
            emb_dim=128,
            dropout=0.25,
        ).to(device)
        opt = torch.optim.AdamW(net.parameters(), lr=lr, weight_decay=2e-4)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=epochs, eta_min=1e-4)

        net.train()
        for _ep in range(epochs):
            opt.zero_grad()
            pred_mat = net.forward_matrix(x_c_tr_t, x_d_tr_t, use_id_emb=True)
            loss = torch.sum(((pred_mat - r_t) ** 2) * m_t) / m_sum
            loss.backward()
            torch.nn.utils.clip_grad_norm_(net.parameters(), 2.0)
            opt.step()
            sched.step()

        net.eval()
        with torch.no_grad():
            p_all = net.forward_matrix(x_c_all_t, x_d_tr_t, use_id_emb=True).cpu().numpy()
        preds_accum += p_all / n_ensemble

    return preds_accum


def fit_and_predict_schur_bilinear(
    train_ds,
    pred_ds,
    cell_cache,
    drug_cache,
    cl_to_tissue,
    hpams,
    naive_params_override=None,
):
    cl_to_idx = cell_cache["cl_to_idx"]
    drug_to_idx = drug_cache["drug_to_idx"]

    # 1. Exact NaiveMeanEffectsPredictor parameters
    if naive_params_override is not None:
        mu_global, ti_effects, cl_effects, dr_effects = naive_params_override
    else:
        df_tr_full = pd.DataFrame({
            "cl": train_ds.cell_line_ids,
            "dr": train_ds.drug_ids,
            "y": train_ds.response.astype(np.float64),
        })
        df_tr_full["ti"] = df_tr_full["cl"].map(lambda c: cl_to_tissue.get(c, "Unknown"))
        mu_global = float(df_tr_full["y"].mean())
        cl_means = df_tr_full.groupby("cl")["y"].mean().to_dict()
        ti_means = df_tr_full.groupby("ti")["y"].mean().to_dict()
        dr_means = df_tr_full.groupby("dr")["y"].mean().to_dict()
        ti_effects = {t: m - mu_global for t, m in ti_means.items()}
        cl_effects = {c: m - ti_means[cl_to_tissue.get(c, "Unknown")] for c, m in cl_means.items()}
        dr_effects = {d: m - mu_global for d, m in dr_means.items()}

    # 2. Aggregate replicate (cell_line, drug) pairs in train_ds by mean
    df_tr = pd.DataFrame({
        "cl": train_ds.cell_line_ids,
        "dr": train_ds.drug_ids,
        "y": train_ds.response.astype(np.float64),
    })
    df_tr = df_tr[df_tr["cl"].isin(cl_to_idx) & df_tr["dr"].isin(drug_to_idx)]
    df_agg = df_tr.groupby(["cl", "dr"], sort=False)["y"].mean().reset_index()

    uniq_tr_cl = sorted(df_agg["cl"].unique().tolist())
    uniq_tr_dr = sorted(df_agg["dr"].unique().tolist())
    tr_cl_idx = np.array([cl_to_idx[c] for c in uniq_tr_cl], dtype=np.int64)
    tr_dr_idx = np.array([drug_to_idx[d] for d in uniq_tr_dr], dtype=np.int64)

    n_tr_cl = len(uniq_tr_cl)
    n_tr_dr = len(uniq_tr_dr)
    local_cl_map = {c: i for i, c in enumerate(uniq_tr_cl)}
    local_dr_map = {d: j for j, d in enumerate(uniq_tr_dr)}

    Y_mat = np.full((n_tr_cl, n_tr_dr), np.nan, dtype=np.float32)
    rows_i = df_agg["cl"].map(local_cl_map).values
    cols_j = df_agg["dr"].map(local_dr_map).values
    Y_mat[rows_i, cols_j] = df_agg["y"].values.astype(np.float32)
    M_obs = ~np.isnan(Y_mat)

    tr_cl_tissues = [cl_to_tissue.get(c, "Unknown") for c in uniq_tr_cl]
    alpha_vec = np.array([ti_effects.get(t, 0.0) for t in tr_cl_tissues], dtype=np.float32)[:, None]
    beta_vec = np.array([cl_effects.get(c, 0.0) for c in uniq_tr_cl], dtype=np.float32)[:, None]
    gamma_vec = np.array([dr_effects.get(d, 0.0) for d in uniq_tr_dr], dtype=np.float32)[None, :]

    # Empirical-Bayes Tissue x Drug residual offset delta_{t, d}
    R_lco_obs = Y_mat - (mu_global + alpha_vec + gamma_vec)
    R_int_obs = R_lco_obs - beta_vec

    lam_td = float(hpams.get("lam_td", 10.0))
    unique_tissues = sorted(list(set(tr_cl_tissues)))
    t_to_row = {t: i for i, t in enumerate(unique_tissues)}
    Delta_table = np.zeros((len(unique_tissues), n_tr_dr), dtype=np.float32)
    tr_tissues_arr = np.array(tr_cl_tissues)
    for t_i, t in enumerate(unique_tissues):
        t_mask = (tr_tissues_arr == t)
        cnt = np.sum(M_obs[t_mask, :], axis=0)
        s_r = np.nansum(R_int_obs[t_mask, :], axis=0)
        Delta_table[t_i, :] = s_r / (cnt + lam_td)

    tr_ti_idx = np.array([t_to_row[t] for t in tr_cl_tissues], dtype=np.int64)
    Delta_mat = Delta_table[tr_ti_idx, :]

    # 3. Multi-view subspace kernels
    uniq_pred_cl = sorted(list(set(pred_ds.cell_line_ids) & set(cl_to_idx.keys())))
    all_cl = sorted(list(set(uniq_tr_cl) | set(uniq_pred_cl)))
    all_cl_idx = np.array([cl_to_idx[c] for c in all_cl], dtype=np.int64)
    all_cl_tissues = [cl_to_tissue.get(c, "Unknown") for c in all_cl]

    ck = build_cell_kernel_and_features(
        cell_cache=cell_cache,
        train_cl_idx=tr_cl_idx,
        all_cl_idx=all_cl_idx,
        tissues_all=all_cl_tissues,
        train_tissues_set=set(tr_cl_tissues),
    )
    K_all_tr = (
        float(hpams.get("w_vdw", 0.22)) * ck["K_vdw"]
        + float(hpams.get("w_logz", 0.16)) * ck["K_logz"]
        + float(hpams.get("w_lm", 0.16)) * ck["K_lm"]
        + float(hpams.get("w_dt", 0.16)) * ck["K_dt"]
        + float(hpams.get("w_pw", 0.14)) * ck["K_pw"]
        + float(hpams.get("w_bio", 0.06)) * ck["K_bio"]
        + float(hpams.get("w_rbf", 0.10)) * ck["K_rbf"]
        + float(hpams.get("w_tis", 0.06)) * ck["K_tis"]
    )
    tr_pos = ck["tr_pos"]
    K_tr_tr = K_all_tr[tr_pos]

    # 4. Head 1A: Exact Per-Drug Observed-Cell Multi-Subspace Kernel Ridge (zero missingness dampening!)
    w_delta = float(hpams.get("w_delta", 0.58))
    R_tis_target = Y_mat - (mu_global + alpha_vec + gamma_vec + w_delta * Delta_mat)

    lam_exact_base = float(hpams.get("lam_exact_base", 8.0))
    Pred_exact_tis = np.zeros((len(all_cl), n_tr_dr), dtype=np.float32)
    for j in range(n_tr_dr):
        obs_i = np.where(M_obs[:, j])[0]
        if len(obs_i) < 5:
            continue
        lam_j = lam_exact_base * (len(obs_i) / 600.0)
        K_sub = K_tr_tr[np.ix_(obs_i, obs_i)] + lam_j * np.eye(len(obs_i), dtype=np.float32)
        w_j = solve(K_sub, R_tis_target[obs_i, j], assume_a="pos")
        Pred_exact_tis[:, j] = K_all_tr[:, obs_i] @ w_j

    # Head 1B: SVD Low-Rank Denoised Matrix Completion + Global Ridge
    A_cell = K_tr_tr + 14.0 * np.eye(n_tr_cl, dtype=np.float32)
    w_beta = solve(K_tr_tr + 18.0 * np.eye(n_tr_cl, dtype=np.float32), beta_vec[:, 0], assume_a="pos")
    beta_pred_all = K_all_tr @ w_beta

    R_tis_comp = np.where(M_obs, R_tis_target, Pred_exact_tis[tr_pos])
    u_svd, s_svd, vt_svd = np.linalg.svd(R_tis_comp - beta_vec, full_matrices=False)
    rank_k = int(hpams.get("svd_rank", 28))
    s_shrunk = np.maximum(s_svd[:rank_k] - float(hpams.get("svd_shrink", 3.5)), 0.0)
    R_svd = (u_svd[:, :rank_k] * s_shrunk[None, :]) @ vt_svd[:rank_k, :] + beta_vec
    Pred_svd_tis = K_all_tr @ solve(A_cell, R_svd, assume_a="pos")

    # Head 1C: Lineage Compass (top-20 transcriptomic/pathway softmax kernel) for unseen tissue transfer (LTO)
    S_lin = 0.45 * ck["K_vdw"] + 0.35 * ck["K_pw"] + 0.20 * ck["K_bio"]
    logits = S_lin / float(hpams.get("lineage_temp", 0.06))
    top_k = min(int(hpams.get("lineage_topk", 20)), n_tr_cl)
    thresh = np.partition(logits, -top_k, axis=1)[:, -top_k : -top_k + 1]
    logits = np.where(logits >= thresh, logits - np.max(logits, axis=1, keepdims=True), -1e9)
    W_lin = np.exp(logits)
    W_lin = W_lin / np.sum(W_lin, axis=1, keepdims=True)
    Lineage_offset_all = W_lin @ (alpha_vec + w_delta * Delta_mat)

    # 5. Head 2: Full-Matrix Residual Two-Tower Bilinear Neural Ensemble (on MPS/CPU)
    X_drug_tr = drug_cache["drug_feat_concat"][tr_dr_idx]
    Pred_nn_tis = train_and_predict_neural_bilinear(
        X_cell_all=ck["X_cell_nn"],
        tr_pos=tr_pos,
        X_drug_tr=X_drug_tr,
        R_target=R_tis_target,
        M_obs=M_obs,
        n_ensemble=int(hpams.get("nn_ensemble", 5)),
        epochs=int(hpams.get("nn_epochs", 115)),
        lr=float(hpams.get("nn_lr", 1.5e-3)),
    )

    # Combine Head 1A (Exact Per-Drug KRR), Head 1B (SVD Low-Rank KRR), and Head 2 (Neural Bilinear)
    # with their variance-calibrated MMSE weights
    Pred_all_tis = (
        0.54 * Pred_exact_tis
        + 0.14 * Pred_svd_tis
        + 0.40 * Pred_nn_tis
    )

    # 6. Head 3: Unseen-Drug Chemical & Schur Response Transfer (LDO & Cross-Study Unshared Drugs)
    all_cl_pos = {c: i for i, c in enumerate(all_cl)}
    seen_tr_cl_set = set(uniq_tr_cl)
    seen_tr_dr_set = set(uniq_tr_dr)

    uniq_pred_dr = sorted(list(set(pred_ds.drug_ids) & set(drug_to_idx.keys())))
    unseen_pred_dr = [d for d in uniq_pred_dr if d not in seen_tr_dr_set]

    unseen_dr_gamma = {}
    unseen_dr_pred_all = {}
    if unseen_pred_dr:
        K_dr_tr = drug_cache["K_drug"][np.ix_(tr_dr_idx, tr_dr_idx)]
        lam_drug = float(hpams.get("lam_drug", 2.0))
        chem_pow_ldo = float(hpams.get("chem_pow_ldo", 2.0))
        K_d_tr = np.power(np.maximum(K_dr_tr, 0.0), chem_pow_ldo)
        A_drug = K_d_tr + lam_drug * np.eye(n_tr_dr, dtype=np.float32)

        R_int_comp = R_tis_comp - beta_vec
        Pred_int_all = Pred_all_tis - beta_pred_all[:, None]

        for d_star in unseen_pred_dr:
            d_idx = drug_to_idx[d_star]
            k_vec = np.power(np.maximum(drug_cache["K_drug"][d_idx, tr_dr_idx], 0.0), chem_pow_ldo)
            if np.max(k_vec) < 1e-6:
                unseen_dr_gamma[d_star] = 0.0
                unseen_dr_pred_all[d_star] = np.zeros(len(all_cl), dtype=np.float32)
                continue
            w_krr = solve(A_drug, k_vec, assume_a="pos")
            k_top = k_vec.copy()
            if len(k_top) > 25:
                thresh_d = np.partition(k_top, -25)[-25]
                k_top = np.where(k_top >= thresh_d, k_top, 0.0)
            w_nw = k_top / max(float(np.sum(k_top)), 1e-6)
            w_d = 0.55 * w_krr + 0.45 * w_nw

            unseen_dr_gamma[d_star] = float(gamma_vec[0, :] @ w_d)
            pred_vec = Pred_int_all @ w_d
            pred_vec[tr_pos] = 0.72 * (R_int_comp @ w_d) + 0.28 * pred_vec[tr_pos]
            unseen_dr_pred_all[d_star] = pred_vec

    # 7. Vectorized Prediction Assembly with Bayes-MMSE Calibration
    pred_cl = pred_ds.cell_line_ids
    pred_dr = pred_ds.drug_ids
    pred_ti = np.array([cl_to_tissue.get(c, "Unknown") for c in pred_cl])

    eff_ti_arr = np.array([ti_effects.get(t, 0.0) for t in pred_ti], dtype=np.float64)
    eff_cl_arr = np.array([cl_effects.get(c, 0.0) for c in pred_cl], dtype=np.float64)
    eff_dr_arr = np.array([dr_effects.get(d, 0.0) for d in pred_dr], dtype=np.float64)
    y_naive_arr = mu_global + eff_ti_arr + eff_cl_arr + eff_dr_arr

    pos_c_arr = np.array([all_cl_pos.get(c, -1) for c in pred_cl], dtype=np.int64)
    j_dr_arr = np.array([local_dr_map.get(d, -1) for d in pred_dr], dtype=np.int64)
    ti_row_arr = np.array([t_to_row.get(t, -1) for t in pred_ti], dtype=np.int64)
    in_tr_cl = np.array([c in seen_tr_cl_set for c in pred_cl], dtype=bool)
    in_tr_ti = ti_row_arr >= 0
    in_tr_dr = j_dr_arr >= 0
    valid_c = pos_c_arr >= 0

    preds = y_naive_arr.copy()

    # Case A: Seen drug, unseen cell line, seen tissue (LCO / Ex Vivo shared drugs)
    mask_lco = valid_c & in_tr_dr & (~in_tr_cl) & in_tr_ti
    if np.any(mask_lco):
        pc = pos_c_arr[mask_lco]
        jd = j_dr_arr[mask_lco]
        tr_i = ti_row_arr[mask_lco]
        res = Pred_all_tis[pc, jd] + w_delta * Delta_table[tr_i, jd]
        preds[mask_lco] = (mu_global + eff_ti_arr[mask_lco] + eff_dr_arr[mask_lco]) + res

    # Case B: Seen drug, unseen cell line, unseen tissue (LTO)
    mask_lto = valid_c & in_tr_dr & (~in_tr_cl) & (~in_tr_ti)
    if np.any(mask_lto):
        pc = pos_c_arr[mask_lto]
        jd = j_dr_arr[mask_lto]
        res = 0.88 * Lineage_offset_all[pc, jd] + 0.96 * Pred_all_tis[pc, jd]
        preds[mask_lto] = (mu_global + eff_dr_arr[mask_lto]) + res

    # Case C: Seen drug, seen cell line (LPO)
    mask_lpo = valid_c & in_tr_dr & in_tr_cl
    if np.any(mask_lpo):
        pc = pos_c_arr[mask_lpo]
        jd = j_dr_arr[mask_lpo]
        tr_i = np.maximum(ti_row_arr[mask_lpo], 0)
        res = Pred_all_tis[pc, jd] - beta_pred_all[pc] + w_delta * Delta_table[tr_i, jd]
        preds[mask_lpo] = y_naive_arr[mask_lpo] + res

    # Case D: Unseen drug (LDO or Cross-Study unshared drugs)
    beta_shrink_ldo = float(hpams.get("beta_shrink_ldo", 0.85))
    mask_ldo = valid_c & (~in_tr_dr)
    if np.any(mask_ldo):
        idx_ldo = np.where(mask_ldo)[0]
        for idx_r in idx_ldo:
            d = pred_dr[idx_r]
            pc = pos_c_arr[idx_r]
            g_tr = unseen_dr_gamma.get(d, 0.0)
            i_tr = float(unseen_dr_pred_all[d][pc]) if d in unseen_dr_pred_all else 0.0
            if in_tr_cl[idx_r]:
                preds[idx_r] = y_naive_arr[idx_r] + beta_shrink_ldo * (g_tr + i_tr)
            elif in_tr_ti[idx_r]:
                preds[idx_r] = (mu_global + eff_ti_arr[idx_r]) + beta_shrink_ldo * (g_tr + beta_pred_all[pc] + i_tr)
            else:
                preds[idx_r] = mu_global + beta_shrink_ldo * (g_tr + beta_pred_all[pc] + i_tr)

    return preds


def fast_naive_mean_effects(tr_ds, te_ds, cl_to_tissue):
    df_tr = pd.DataFrame({
        "cl": tr_ds.cell_line_ids,
        "dr": tr_ds.drug_ids,
        "y": tr_ds.response.astype(np.float64),
    })
    df_tr["ti"] = df_tr["cl"].map(lambda c: cl_to_tissue.get(c, "Unknown"))
    mu = float(df_tr["y"].mean())
    cl_means = df_tr.groupby("cl")["y"].mean().to_dict()
    ti_means = df_tr.groupby("ti")["y"].mean().to_dict()
    dr_means = df_tr.groupby("dr")["y"].mean().to_dict()
    ti_eff = {t: m - mu for t, m in ti_means.items()}
    cl_eff = {c: m - ti_means[cl_to_tissue.get(c, "Unknown")] for c, m in cl_means.items()}
    dr_eff = {d: m - mu for d, m in dr_means.items()}

    te_ti = pd.Series(te_ds.cell_line_ids).map(lambda c: cl_to_tissue.get(c, "Unknown"))
    preds = (
        mu
        + te_ti.map(ti_eff).fillna(0.0).values
        + pd.Series(te_ds.cell_line_ids).map(cl_eff).fillna(0.0).values
        + pd.Series(te_ds.drug_ids).map(dr_eff).fillna(0.0).values
    )
    return preds, (mu, ti_eff, cl_eff, dr_eff)


def run_cv_evaluation(views, cell_cache, drug_cache, mode="LCO", n_splits=10, eval_split="test", hpams=None, random_state=42):
    t0 = time.time()
    hpams = hpams or {}
    ds = load_ctrpv2(path_data=DATA_DIR)
    ds.remove_nan_responses()
    if mode == "LCO" and random_state == 42 and os.path.exists(f"{DATA_DIR}/splits"):
        ds.load_splits(f"{DATA_DIR}/splits")
    elif random_state != 42:
        from sklearn.model_selection import GroupKFold, train_test_split
        from drevalpy.datasets.dataset import DrugResponseDataset
        group_ids = ds.drug_ids if mode == "LDO" else (ds.cell_line_ids if mode == "LCO" else ds.tissue)
        gkf = GroupKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
        cv_sets = []
        for train_indices, test_indices in gkf.split(ds.response, groups=group_ids):
            unique_train_groups = np.unique(group_ids[train_indices])
            train_groups, val_groups = train_test_split(
                unique_train_groups, test_size=0.1, shuffle=True, random_state=random_state
            )
            tr_idx = np.where(np.isin(group_ids, train_groups))[0]
            va_idx = np.where(np.isin(group_ids, val_groups))[0]
            cv_sets.append({
                "train": DrugResponseDataset(
                    cell_line_ids=ds.cell_line_ids[tr_idx],
                    drug_ids=ds.drug_ids[tr_idx],
                    response=ds.response[tr_idx],
                    tissues=ds.tissue[tr_idx] if ds.tissue is not None else None,
                    dataset_name=ds.dataset_name,
                ),
                "validation": DrugResponseDataset(
                    cell_line_ids=ds.cell_line_ids[va_idx],
                    drug_ids=ds.drug_ids[va_idx],
                    response=ds.response[va_idx],
                    tissues=ds.tissue[va_idx] if ds.tissue is not None else None,
                    dataset_name=ds.dataset_name,
                ),
                "test": DrugResponseDataset(
                    cell_line_ids=ds.cell_line_ids[test_indices],
                    drug_ids=ds.drug_ids[test_indices],
                    response=ds.response[test_indices],
                    tissues=ds.tissue[test_indices] if ds.tissue is not None else None,
                    dataset_name=ds.dataset_name,
                ),
            })
        ds._cv_splits = cv_sets
    else:
        ds.split_dataset(
            n_cv_splits=n_splits,
            mode=mode,
            split_validation=True,
            split_early_stopping=False,
            validation_ratio=0.1,
            random_state=random_state,
        )

    cl_keep = np.array(cell_cache["cl_ids"])
    dr_keep = np.array(drug_cache["drug_ids"])

    fold_metrics = []
    for fold_i, split in enumerate(ds.cv_splits):
        if eval_split == "validation":
            tr_raw = split["train"].copy()
            te_raw = split["validation"].copy()
        else:
            tr_raw = split["train"].copy()
            tr_raw.add_rows(split["validation"].copy())
            tr_raw.shuffle(random_state=42)
            te_raw = split["test"].copy()

        naive_preds, _ = fast_naive_mean_effects(tr_raw, te_raw, views["cl_to_tissue"])
        naive_df = pd.DataFrame({
            "cell_line_name": te_raw.cell_line_ids,
            "pubchem_id": te_raw.drug_ids,
            "y_pred": naive_preds,
        })
        naive_df["drug_name"] = naive_df["pubchem_id"].map(views["pubchem_to_name"])

        tr_ds = tr_raw.copy()
        te_ds = te_raw.copy()
        tr_ds.reduce_to(cell_line_ids=cl_keep, drug_ids=dr_keep)
        te_ds.reduce_to(cell_line_ids=cl_keep, drug_ids=dr_keep)

        preds = fit_and_predict_schur_bilinear(
            train_ds=tr_ds,
            pred_ds=te_ds,
            cell_cache=cell_cache,
            drug_cache=drug_cache,
            cl_to_tissue=views["cl_to_tissue"],
            hpams=hpams,
        )

        mse_raw = float(np.mean((te_ds.response - preds) ** 2))
        df = pd.DataFrame({
            "cell_line_name": te_ds.cell_line_ids,
            "pubchem_id": te_ds.drug_ids,
            "y_true": te_ds.response,
            "y_pred": preds,
        })
        df["drug_name"] = df["pubchem_id"].map(views["pubchem_to_name"])
        merged = df.merge(
            naive_df[["drug_name", "cell_line_name", "y_pred"]],
            on=["drug_name", "cell_line_name"],
            suffixes=("", "_naive"),
        )
        yt = merged["y_true"].values - merged["y_pred_naive"].values
        yp = merged["y_pred"].values - merged["y_pred_naive"].values
        ss_res = np.sum((yt - yp) ** 2)
        ss_tot = np.sum((yt - np.mean(yt)) ** 2)
        r2_norm = float(1.0 - ss_res / ss_tot)
        pcc_norm = float(np.corrcoef(yt, yp)[0, 1]) if np.std(yp) > 1e-12 else 0.0
        scc_norm = float(spearmanr(yt, yp).statistic)
        te_tissues = sorted(list(set(te_ds.tissue))) if te_ds.tissue is not None else []
        fold_metrics.append({
            "fold": fold_i,
            "R2_norm": r2_norm,
            "Pearson_norm": pcc_norm,
            "Spearman_norm": scc_norm,
            "MSE": mse_raw,
            "tissues": te_tissues,
        })

    r2s = [m["R2_norm"] for m in fold_metrics]
    pccs = [m["Pearson_norm"] for m in fold_metrics]
    sccs = [m["Spearman_norm"] for m in fold_metrics]
    mses = [m["MSE"] for m in fold_metrics]
    summary = {
        "mode": mode,
        "eval_split": eval_split,
        "random_state": random_state,
        "R2_norm_mean": float(np.mean(r2s)),
        "R2_norm_std": float(np.std(r2s, ddof=1)),
        "Pearson_norm_mean": float(np.mean(pccs)),
        "Pearson_norm_std": float(np.std(pccs, ddof=1)),
        "Spearman_norm_mean": float(np.mean(sccs)),
        "Spearman_norm_std": float(np.std(sccs, ddof=1)),
        "MSE_mean": float(np.mean(mses)),
        "MSE_std": float(np.std(mses, ddof=1)),
        "folds": fold_metrics,
    }
    print(
        f"[{mode} | {eval_split} | seed={random_state} | {time.time()-t0:.1f}s] "
        f"Mean R2_norm = {summary['R2_norm_mean']:.5f} ± {summary['R2_norm_std']:.5f} | "
        f"Pearson_norm = {summary['Pearson_norm_mean']:.5f} ± {summary['Pearson_norm_std']:.5f} | "
        f"Spearman_norm = {summary['Spearman_norm_mean']:.5f} ± {summary['Spearman_norm_std']:.5f} | "
        f"MSE = {summary['MSE_mean']:.5f}"
    )
    if mode == "LTO":
        for m in fold_metrics:
            if "Blood" in m["tissues"] or "Breast" in m["tissues"]:
                print(
                    f"  -> LTO Fold {m['fold']} ({m['tissues']}): "
                    f"R2_norm={m['R2_norm']:.5f}, Pearson_norm={m['Pearson_norm']:.5f}, Spearman_norm={m['Spearman_norm']:.5f}"
                )
    return summary


if __name__ == "__main__":
    t_start = time.time()
    views = load_ctrpv2_all_views()
    cell_cache = precompute_cell_views(views)
    drug_cache = precompute_drug_views(views)
    print(f"Precomputed cell & drug caches in {time.time()-t_start:.2f}s")

    results = {}
    for mode in ["LCO", "LTO", "LDO"]:
        results[f"{mode}_validation"] = run_cv_evaluation(views, cell_cache, drug_cache, mode=mode, eval_split="validation")
        results[f"{mode}_test"] = run_cv_evaluation(views, cell_cache, drug_cache, mode=mode, eval_split="test")

    # Second independent split generation for LDO (per dreval-ldo-beat-naive-mean-effects target card)
    results["LDO_test_seed1337"] = run_cv_evaluation(views, cell_cache, drug_cache, mode="LDO", eval_split="test", random_state=1337)

    out_path = "DREVAL_CAMPAIGN/certificates/stage2_ctrpv2_inner_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved Stage 2 CTRPv2 inner validation results to {out_path}")
