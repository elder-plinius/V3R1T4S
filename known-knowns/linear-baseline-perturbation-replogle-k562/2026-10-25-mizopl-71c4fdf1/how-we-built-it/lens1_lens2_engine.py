#!/usr/bin/env python3
"""
Lens 1 + Lens 2 Dual-Lens Perturbation Predictor for `linear-baseline-perturbation-replogle-k562`.
Strictly adheres to the zero-leakage split firewall:
  - All means, baselines, cis-attenuation laws, SVD subspaces, co-expression kernels,
    and resolvent weights are fitted 100% on `train` perturbations of each split.
"""
import os
import json
import pickle
import time
import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.sparse.linalg import svds

DATA_DIR = "../data"
GEARS_DIR = os.path.join(DATA_DIR, "gears_pert_data")


def load_cached_dataset(dataset_name):
    cache_path = os.path.join(DATA_DIR, f"{dataset_name}_pseudobulk.npz")
    d = np.load(cache_path, allow_pickle=True)
    gene_names = d["gene_names"].astype(str)
    uniq_conds = d["uniq_conds"].astype(str)
    clean_conds = d["clean_conds"].astype(str)
    X_mean = d["X_mean"].astype(np.float64)
    counts = d["counts"].astype(np.float64)
    splits_dict = json.loads(str(d["splits_json"]))
    return gene_names, uniq_conds, clean_conds, X_mean, counts, splits_dict


def build_go_idf_features(pert_universe):
    """
    Build IDF-weighted Gene Ontology indicator matrix and Jaccard similarity
    from GEARS's bundled `gene2go_all.pkl` (no expression leakage of any kind).
    """
    with open(os.path.join(GEARS_DIR, "gene2go_all.pkl"), "rb") as f:
        gene2go = pickle.load(f)

    genes = sorted(list(pert_universe))
    g2idx = {g: i for i, g in enumerate(genes)}

    go_terms = sorted(list({t for g in genes if g in gene2go for t in gene2go[g]}))
    t2idx = {t: j for j, t in enumerate(go_terms)}

    rows, cols = [], []
    for i, g in enumerate(genes):
        for t in gene2go.get(g, []):
            rows.append(i)
            cols.append(t2idx[t])

    M = sp.csr_matrix(
        (np.ones(len(rows), dtype=np.float64), (rows, cols)),
        shape=(len(genes), len(go_terms)),
    )
    # IDF weight: log((1 + N) / (1 + df))
    df = np.array(M.sum(axis=0)).flatten()
    idf = np.log((1.0 + len(genes)) / (1.0 + df))
    M_idf = M @ sp.diags(idf)

    # L2 normalize rows of M_idf for cosine similarity
    norms = np.sqrt(np.array(M_idf.power(2).sum(axis=1)).flatten())
    norms[norms < 1e-12] = 1.0
    M_idf_norm = sp.diags(1.0 / norms) @ M_idf

    # Dense cosine similarity matrix among pert_universe
    S_go_idf = (M_idf_norm @ M_idf_norm.T).toarray()
    np.fill_diagonal(S_go_idf, 1.0)

    # Also compute exact binary GO intersection and Jaccard
    inter = (M @ M.T).toarray()
    deg = np.array(M.sum(axis=1)).flatten()
    union = deg[:, None] + deg[None, :] - inter
    union[union < 1.0] = 1.0
    S_go_jaccard = inter / union
    np.fill_diagonal(S_go_jaccard, 1.0)

    return genes, g2idx, S_go_idf, S_go_jaccard
