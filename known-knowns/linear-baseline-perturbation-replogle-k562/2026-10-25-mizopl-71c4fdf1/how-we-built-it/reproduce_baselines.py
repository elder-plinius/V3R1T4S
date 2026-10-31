#!/usr/bin/env python3
"""
Exact Python reproduction of Ahlmann-Eltze, Huber & Anders (Nature Methods 2025)
single-perturbation benchmark (`const-ae/linear_perturbation_prediction-Paper`
at commit bfa6eeea2bd145a1af2ec0127a2e808cc38456a9):
  - prepare_perturbation_data.py (GEARS PertData + simulation split)
  - run_ground_truth_for_combinatorial_perturbations.py
  - run_mean_prediction.R
  - run_linear_pretrained_model.R (lpm_selftrained, lpm_gearsPertEmb, lpm_rpe1PertEmb, lpm_k562PertEmb, lpm_randomGeneEmb, lpm_randomPertEmb)
  - single_perturbation_analysis.Rmd (Top-1000 expressed genes L2 and Pearson delta)
"""
import os
import json
import pickle
import time
import numpy as np
import pandas as pd
import anndata as ad
import scipy.sparse as sp
from scipy.sparse.linalg import svds


DATA_DIR = "../data"
GEARS_DIR = os.path.join(DATA_DIR, "gears_pert_data")


def parse_single_pert(i):
    a, b = i.split("+")[0], i.split("+")[1]
    return b if a == "ctrl" else a


def parse_combo_pert(i):
    return i.split("+")[0], i.split("+")[1]


def parse_any_pert(p):
    if ("ctrl" in p) and (p != "ctrl"):
        return [parse_single_pert(p)]
    elif "ctrl" not in p:
        out = parse_combo_pert(p)
        return [out[0], out[1]]
    return []


def filter_pert_in_go(condition, pert_names):
    if condition == "ctrl":
        return True
    cond1 = condition.split("+")[0]
    cond2 = condition.split("+")[1]
    num_ctrl = (cond1 == "ctrl") + (cond2 == "ctrl")
    num_in_perts = (cond1 in pert_names) + (cond2 in pert_names)
    return (num_ctrl + num_in_perts) == 2


def get_genes_from_perts(perts):
    if isinstance(perts, str):
        perts = [perts]
    gene_list = [p.split("+") for p in np.unique(perts)]
    gene_list = [item for sublist in gene_list for item in sublist]
    gene_list = [g for g in gene_list if g != "ctrl"]
    return list(np.unique(gene_list))


def get_perts_from_genes(genes, pert_list, type_="both"):
    single_perts = [p for p in pert_list if ("ctrl" in p) and (p != "ctrl")]
    combo_perts = [p for p in pert_list if "ctrl" not in p]
    perts = []
    if type_ == "single":
        pert_candidate_list = single_perts
    elif type_ == "combo":
        pert_candidate_list = combo_perts
    elif type_ == "both":
        pert_candidate_list = pert_list
    else:
        pert_candidate_list = pert_list
    for p in pert_candidate_list:
        for g in genes:
            if g in parse_any_pert(p):
                perts.append(p)
                break
    return perts


def get_simulation_split(pert_list, train_gene_set_size=0.85, combo_seen2_train_frac=0.85, seed=1):
    unique_pert_genes = get_genes_from_perts(pert_list)
    pert_train = []
    pert_test = []
    np.random.seed(seed=seed)
    train_gene_candidates = np.random.choice(
        unique_pert_genes, int(len(unique_pert_genes) * train_gene_set_size), replace=False
    )
    ood_genes = np.setdiff1d(unique_pert_genes, train_gene_candidates)

    pert_single_train = get_perts_from_genes(train_gene_candidates, pert_list, "single")
    pert_combo = get_perts_from_genes(train_gene_candidates, pert_list, "combo")
    pert_train.extend(pert_single_train)

    combo_seen1 = [
        x for x in pert_combo if len([t for t in x.split("+") if t in train_gene_candidates]) == 1
    ]
    pert_test.extend(combo_seen1)

    pert_combo = np.setdiff1d(pert_combo, combo_seen1)
    np.random.seed(seed=seed)
    pert_combo_train = np.random.choice(
        pert_combo, int(len(pert_combo) * combo_seen2_train_frac), replace=False
    )
    combo_seen2 = np.setdiff1d(pert_combo, pert_combo_train).tolist()
    pert_test.extend(combo_seen2)
    pert_train.extend(pert_combo_train)

    unseen_single = get_perts_from_genes(ood_genes, pert_list, "single")
    combo_ood = get_perts_from_genes(ood_genes, pert_list, "combo")
    pert_test.extend(unseen_single)

    combo_seen0 = [
        x for x in combo_ood if len([t for t in x.split("+") if t in train_gene_candidates]) == 0
    ]
    pert_test.extend(combo_seen0)
    return pert_train, pert_test


def compute_gears_set2conditions(adata, pert_names, seed=1, train_gene_set_size=0.75, combo_seen2_train_frac=0.75):
    """Exact replica of GEARS PertData.load() + PertData.prepare_split(split='simulation', seed=seed)."""
    obs_cond = adata.obs["condition"].astype(str)
    mask = obs_cond.apply(lambda x: filter_pert_in_go(x, pert_names)).values
    filtered_conds = obs_cond.values[mask]
    # Preserve order of unique conditions in filtered adata.obs['condition']
    _, idx = np.unique(filtered_conds, return_index=True)
    unique_conds_in_order = filtered_conds[np.sort(idx)]
    unique_perts = [p for p in unique_conds_in_order if p != "ctrl"]

    np.random.seed(seed=seed)
    train, test = get_simulation_split(
        unique_perts, train_gene_set_size, combo_seen2_train_frac, seed
    )
    train, val = get_simulation_split(train, 0.9, 0.9, seed)
    train.append("ctrl")

    map_dict = {x: "train" for x in train}
    map_dict.update({x: "val" for x in val})
    map_dict.update({x: "test" for x in test})
    map_dict.update({"ctrl": "train"})

    # Group filtered conditions by split in order of appearance in adata.obs
    df_obs = pd.DataFrame({"condition": filtered_conds})
    df_obs["split"] = df_obs["condition"].map(map_dict)
    set2conditions = {}
    for sp_name, grp in df_obs.groupby("split", sort=False):
        set2conditions[sp_name] = grp["condition"].unique().tolist()
    return set2conditions, map_dict


def load_pert_names():
    with open(os.path.join(GEARS_DIR, "gene2go_all.pkl"), "rb") as f:
        gene2go = pickle.load(f)
    with open(os.path.join(GEARS_DIR, "essential_all_data_pert_genes.pkl"), "rb") as f:
        essential_genes = pickle.load(f)
    gene2go = {i: gene2go[i] for i in essential_genes if i in gene2go}
    return set(np.unique(list(gene2go.keys())))


def load_dataset_pseudobulk(dataset_name):
    """Load h5ad and compute exact condition-level pseudobulk matrix (genes x conditions)."""
    h5_path = os.path.join(GEARS_DIR, dataset_name, "perturb_processed.h5ad")
    adata = ad.read_h5ad(h5_path)
    gene_names = adata.var["gene_name"].astype(str).values
    conds = adata.obs["condition"].astype(str).values

    # Unique conditions
    uniq_conds = pd.unique(conds)
    G = len(gene_names)
    C = len(uniq_conds)

    # Efficient sparse/dense group mean
    cond_to_idx = {c: i for i, c in enumerate(uniq_conds)}
    codes = np.array([cond_to_idx[c] for c in conds], dtype=np.int32)
    counts = np.bincount(codes, minlength=C).astype(np.float64)

    # Indicator matrix S of shape (N_cells, C)
    S = sp.csr_matrix(
        (np.ones(len(codes), dtype=np.float64), (np.arange(len(codes)), codes)),
        shape=(len(codes), C),
    )
    X_sum = (adata.X.T @ S).toarray() if sp.issparse(adata.X) else (adata.X.T @ S)
    X_mean = X_sum / counts[None, :]  # shape (G, C)

    clean_conds = np.array([c.replace("+ctrl", "").replace("ctrl+", "") if c != "ctrl" else "ctrl" for c in uniq_conds])
    return adata, gene_names, uniq_conds, clean_conds, X_mean, counts


def prcomp_irlba_r(M, n=10):
    """
    Exact match to R's `irlba::prcomp_irlba(M, n = n)` where M has shape (n_obs, n_vars).
    In R, prcomp(M, center=TRUE, scale.=FALSE) centers each COLUMN of M,
    and returns `pca$x = M_centered @ V[:, :n]` of shape (n_obs, n).
    """
    M_centered = M - M.mean(axis=0, keepdims=True)
    U, s, Vt = svds(M_centered.astype(np.float64), k=n)
    order = np.argsort(s)[::-1]
    U = U[:, order]
    s = s[order]
    return U * s[None, :]


def run_lpm(X_mean, gene_names, uniq_conds, clean_conds, set2conditions, gene_emb=None, pert_emb=None, pca_dim=10, ridge_penalty=0.1):
    """
    Exact replica of benchmark/src/run_linear_pretrained_model.R.
    Returns dict mapping clean_condition -> predicted expression vector of length G.
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
    conds_psce = uniq_conds[keep_mask]
    clean_psce = clean_conds[keep_mask]
    splits_psce = np.array([cond_to_split[c] for c in conds_psce])

    ctrl_idx = np.where(conds_psce == "ctrl")[0][0]
    baseline = X_psce[:, ctrl_idx]
    change_psce = X_psce - baseline[:, None]

    train_mask = splits_psce == "train"
    train_X = X_psce[:, train_mask]
    train_change = change_psce[:, train_mask]
    train_clean = clean_psce[train_mask]

    # PCA on assay(train_data, "X") of shape (G, P_train)
    if gene_emb is None or pert_embedding_is_train(pert_emb):
        pca_x = prcomp_irlba_r(train_X, n=pca_dim)  # shape (G, pca_dim)

    if gene_emb is None:
        G_mat = pca_x  # (G, pca_dim)
        G_rows = list(gene_names)
    else:
        G_mat, G_rows = gene_emb[0], list(gene_emb[1])

    if pert_emb is None:
        P_mat = pca_x.T  # (pca_dim, G)
        P_cols = list(gene_names)
    else:
        P_mat, P_cols = pert_emb[0].copy(), list(pert_emb[1])

    if "ctrl" not in P_cols:
        P_mat = np.hstack([P_mat, np.zeros((P_mat.shape[0], 1), dtype=np.float64)])
        P_cols = P_cols + ["ctrl"]

    # R: pert_matches <- match(colnames(pert_emb), train_data$clean_condition)
    train_clean_first = {}
    for idx, c in enumerate(train_clean):
        if c not in train_clean_first:
            train_clean_first[c] = idx

    pert_keep_cols = []
    pert_matches = []
    for j, col_name in enumerate(P_cols):
        if col_name in train_clean_first:
            pert_keep_cols.append(j)
            pert_matches.append(train_clean_first[col_name])

    # R: gene_matches <- match(rownames(gene_emb), rownames(train_data))
    gene_first = {}
    for idx, g in enumerate(gene_names):
        if g not in gene_first:
            gene_first[g] = idx

    gene_keep_rows = []
    gene_matches = []
    for i, row_name in enumerate(G_rows):
        if row_name in gene_first:
            gene_keep_rows.append(i)
            gene_matches.append(gene_first[row_name])

    gene_emb_sub = G_mat[gene_keep_rows, :]
    pert_emb_training = P_mat[:, pert_keep_cols]
    Y = train_change[np.ix_(gene_matches, pert_matches)]

    # solve_y_axb: center is rowMeans(Y) on the matched submatrix!
    center = Y.mean(axis=1)  # shape (G_matched,)
    Y_c = Y - center[:, None]

    d_A = gene_emb_sub.shape[1]
    d_B = pert_emb_training.shape[0]
    lhs_A = np.linalg.solve(gene_emb_sub.T @ gene_emb_sub + np.eye(d_A) * ridge_penalty, gene_emb_sub.T)
    rhs_B = np.linalg.solve(pert_emb_training @ pert_emb_training.T + np.eye(d_B) * ridge_penalty, pert_emb_training).T
    K = lhs_A @ Y_c @ rhs_B

    # R: pert_matches_all <- match(psce$clean_condition, colnames(pert_emb))
    p_col_first = {}
    for j, col_name in enumerate(P_cols):
        if col_name not in p_col_first:
            p_col_first[col_name] = j

    B_all = np.full((d_B, len(clean_psce)), np.nan, dtype=np.float64)
    for j, p in enumerate(clean_psce):
        if p in p_col_first:
            B_all[:, j] = P_mat[:, p_col_first[p]]

    baseline_sub = baseline[gene_matches]
    pred_sub = baseline_sub[:, None] + center[:, None] + (gene_emb_sub @ K @ B_all)

    # Map back to full gene_names length G
    # Note: for genes matched in gene_matches, we store their prediction
    pred_full_mat = np.full((len(gene_names), len(clean_psce)), np.nan, dtype=np.float64)
    # In R, rownames(pred) <- rownames(psce)[na.omit(gene_matches)]
    for row_idx_in_sub, orig_g_idx in enumerate(gene_matches):
        pred_full_mat[orig_g_idx, :] = pred_sub[row_idx_in_sub, :]

    return {clean_psce[j]: pred_full_mat[:, j] for j in range(len(clean_psce))}


def pert_embedding_is_train(pert_emb):
    return pert_emb is None


def run_mean_baseline(X_mean, uniq_conds, clean_conds, set2conditions):
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
    conds_psce = uniq_conds[keep_mask]
    clean_psce = clean_conds[keep_mask]
    splits_psce = np.array([cond_to_split[c] for c in conds_psce])

    mean_across_training = X_psce[:, splits_psce == "train"].mean(axis=1)
    return {clean_psce[j]: mean_across_training.copy() for j in range(len(clean_psce))}


def evaluate_predictions(pred_dict, X_mean, gene_names, uniq_conds, clean_conds, valid_perts_df):
    """
    Exact replica of single_perturbation_analysis.Rmd lines 138-200:
      - Rank genes by descending ctrl expression with ties='first'
      - Keep expr_rank <= 1000
      - Compute r2, r2_delta, l2 per perturbation
    """
    ctrl_idx = np.where(uniq_conds == "ctrl")[0][0]
    baseline = X_mean[:, ctrl_idx]

    # R: rank(desc(observed), ties = "first")
    # In Python, stable argsort of -baseline gives exact ties="first" order!
    order = np.argsort(-baseline, kind="mergesort")
    top1000_idx = order[:1000]

    b_top = baseline[top1000_idx]
    clean_to_idx = {c: i for i, c in enumerate(clean_conds)}

    rows = []
    for _, row in valid_perts_df.iterrows():
        pert = row["perturbation"]  # e.g. "AAAS+ctrl"
        clean_p = pert.replace("+ctrl", "").replace("ctrl+", "")
        if clean_p not in pred_dict or clean_p not in clean_to_idx:
            continue
        pred_full = pred_dict[clean_p]
        obs_full = X_mean[:, clean_to_idx[clean_p]]

        p_top = pred_full[top1000_idx]
        o_top = obs_full[top1000_idx]
        valid_g = ~(np.isnan(p_top) | np.isnan(o_top) | np.isnan(b_top))
        if valid_g.sum() == 0:
            continue
        p_v = p_top[valid_g]
        o_v = o_top[valid_g]
        b_v = b_top[valid_g]

        l2 = float(np.sqrt(np.sum((p_v - o_v) ** 2)))
        r2 = float(np.corrcoef(p_v, o_v)[0, 1])
        dp = p_v - b_v
        do = o_v - b_v
        if np.std(dp) < 1e-12 or np.std(do) < 1e-12:
            r2_delta = 0.0
        else:
            r2_delta = float(np.corrcoef(dp, do)[0, 1])
        rows.append({
            "perturbation": pert,
            "train": row["train"],
            "l2": l2,
            "r2": r2,
            "r2_delta": r2_delta,
        })
    return pd.DataFrame(rows)


if __name__ == "__main__":
    pert_names = load_pert_names()
    print("Loaded pert_names:", len(pert_names), flush=True)

    panel_a = pd.read_excel(os.path.join(DATA_DIR, "single_perturbation_prediction.xlsx"), sheet_name="Panel A")
    panel_c = pd.read_excel(os.path.join(DATA_DIR, "single_perturbation_prediction.xlsx"), sheet_name="Panel C")

    for ds in ["replogle_k562_essential", "replogle_rpe1_essential", "adamson"]:
        t0 = time.time()
        cache_path = os.path.join(DATA_DIR, f"{ds}_pseudobulk.npz")
        if os.path.exists(cache_path):
            d = np.load(cache_path, allow_pickle=True)
            gene_names = d["gene_names"].astype(str)
            uniq_conds = d["uniq_conds"].astype(str)
            clean_conds = d["clean_conds"].astype(str)
            X_mean = d["X_mean"].astype(np.float64)
            counts = d["counts"].astype(np.float64)
            splits_dict = json.loads(str(d["splits_json"]))
        else:
            adata, gene_names, uniq_conds, clean_conds, X_mean, counts = load_dataset_pseudobulk(ds)
            splits_dict = {}
            for seed in range(1, 6):
                s2c, _ = compute_gears_set2conditions(adata, pert_names, seed=seed)
                splits_dict[str(seed)] = s2c
            np.savez_compressed(
                cache_path,
                gene_names=gene_names,
                uniq_conds=uniq_conds,
                clean_conds=clean_conds,
                X_mean=X_mean,
                counts=counts,
                splits_json=json.dumps(splits_dict),
            )
        print(f"\n=== {ds} loaded in {time.time()-t0:.2f}s: G={len(gene_names)}, C={len(uniq_conds)} ===", flush=True)

        for seed in [1, 2]:
            s2c = splits_dict[str(seed)]
            sub_a = panel_a[(panel_a["dataset_name"] == ds) & (panel_a["seed"] == seed) & (panel_a["method"] == "lpm_selftrained")]
            pred_mean = run_mean_baseline(X_mean, uniq_conds, clean_conds, s2c)
            pred_lpm = run_lpm(X_mean, gene_names, uniq_conds, clean_conds, s2c)

            eval_mean = evaluate_predictions(pred_mean, X_mean, gene_names, uniq_conds, clean_conds, sub_a[["perturbation", "train"]])
            eval_lpm = evaluate_predictions(pred_lpm, X_mean, gene_names, uniq_conds, clean_conds, sub_a[["perturbation", "train"]])

            pub_mean = panel_a[(panel_a["dataset_name"] == ds) & (panel_a["seed"] == seed) & (panel_a["method"] == "mean")]
            pub_lpm = sub_a

            m_mean = eval_mean.merge(pub_mean, on=["perturbation", "train"], suffixes=("_repro", "_pub"))
            m_lpm = eval_lpm.merge(pub_lpm, on=["perturbation", "train"], suffixes=("_repro", "_pub"))

            print(f"  Seed {seed} (n={len(m_lpm)}):")
            print(f"    MEAN L2: repro={m_mean['l2_repro'].mean():.6f} vs pub={m_mean['l2_pub'].mean():.6f} (max_diff={np.abs(m_mean['l2_repro']-m_mean['l2_pub']).max():.2e})")
            print(f"    LPM  L2: repro={m_lpm['l2_repro'].mean():.6f} vs pub={m_lpm['l2_pub'].mean():.6f} (max_diff={np.abs(m_lpm['l2_repro']-m_lpm['l2_pub']).max():.2e})")
            print(f"    LPM  r2_delta: repro={m_lpm['r2_delta_repro'].mean():.6f} vs pub={m_lpm['r2_delta_pub'].mean():.6f} (max_diff={np.abs(m_lpm['r2_delta_repro']-m_lpm['r2_delta_pub']).max():.2e})", flush=True)

