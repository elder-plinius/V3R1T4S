#!/usr/bin/env python3
"""
Modular Pocket-Factorized Pan-Allele Censored-MM Kernel + Adaptive Anchor Discovery +
Wildcard L29 Projection + Multi-Threshold Pairwise Epistasis Ensemble (strictly BD2009).
"""
import time
import numpy as np
import pandas as pd
from scipy.special import softmax, expit
from sklearn.metrics import roc_auc_score
from sklearn.linear_model import LogisticRegression

t0 = time.perf_counter()
BASE = "data/benchmark_mhci_reliability"
bd2009 = pd.read_csv(f"{BASE}/binding/bd2009.1/bdata.2009.mhci.public.1.txt", sep="\t")
blind = pd.read_csv(f"{BASE}/binding/blind.1/bdata.2013.mhci.public.blind.1.txt", sep="\t")
t_net = pd.read_csv(f"{BASE}/features/table_pred_performance/table.cv_features.updated.auc.netmhc.xls", sep="\t")
t_pan = pd.read_csv(f"{BASE}/features/table_pred_performance/table.cv_features.updated.auc.netmhcpan.xls", sep="\t")
t_smm = pd.read_csv(f"{BASE}/features/table_pred_performance/table.cv_features.updated.auc.smmpmbec_cpp.xls", sep="\t")

for df in (bd2009, blind):
    df["allele"] = df["mhc"].str.replace("*", "-", regex=False).str.replace(":", "", regex=False)
    df["mhckey"] = df["allele"] + "-" + df["peptide_length"].astype(str)

AAS = "ACDEFGHIKLMNPQRSTVWY"
AA_TO_IDX = {a: i for i, a in enumerate(AAS)}
BLOSUM62_RAW = {
    "A": [ 4,-1,-2,-2, 0,-1,-1, 0,-2,-1,-1,-1,-1,-2,-1, 1, 0,-3,-2, 0],
    "R": [-1, 5, 0,-2,-3, 1, 0,-2, 0,-3,-2, 2,-1,-3,-2,-1,-1,-3,-2,-3],
    "N": [-2, 0, 6, 1,-3, 0, 0, 0, 1,-3,-3, 0,-2,-3,-2, 1, 0,-4,-2,-3],
    "D": [-2,-2, 1, 6,-3, 0, 2,-1,-1,-3,-4,-1,-3,-3,-1, 0,-1,-4,-3,-3],
    "C": [ 0,-3,-3,-3, 9,-3,-4,-3,-3,-1,-1,-3,-1,-2,-3,-1,-1,-2,-2,-1],
    "Q": [-1, 1, 0, 0,-3, 5, 2,-2, 0,-3,-2, 1, 0,-3,-1, 0,-1,-2,-1,-2],
    "E": [-1, 0, 0, 2,-4, 2, 5,-2, 0,-3,-3, 1,-2,-3,-1, 0,-1,-3,-2,-2],
    "G": [ 0,-2, 0,-1,-3,-2,-2, 6,-2,-4,-4,-2,-3,-3,-2, 0,-2,-2,-3,-3],
    "H": [-2, 0, 1,-1,-3, 0, 0,-2, 8,-3,-3,-1,-2,-1,-2,-1,-2,-2, 2,-3],
    "I": [-1,-3,-3,-3,-1,-3,-3,-4,-3, 4, 2,-3, 1, 0,-3,-2,-1,-3,-1, 3],
    "L": [-1,-2,-3,-4,-1,-2,-3,-4,-3, 2, 4,-2, 2, 0,-3,-2,-1,-2,-1, 1],
    "K": [-1, 2, 0,-1,-3, 1, 1,-2,-1,-3,-2, 5,-1,-3,-1, 0,-1,-3,-2,-2],
    "M": [-1,-1,-2,-3,-1, 0,-2,-3,-2, 1, 2,-1, 5, 0,-2,-1,-1,-1,-1, 1],
    "F": [-2,-3,-3,-3,-2,-3,-3,-3,-1, 0, 0,-3, 0, 6,-4,-2,-2, 1, 3,-1],
    "P": [-1,-2,-2,-1,-3,-1,-1,-2,-2,-3,-3,-1,-2,-4, 7,-1,-1,-4,-3,-2],
    "S": [ 1,-1, 1, 0,-1, 0, 0, 0,-1,-2,-2, 0,-1,-2,-1, 4, 1,-3,-2,-2],
    "T": [ 0,-1, 0,-1,-1,-1,-1,-2,-2,-1,-1,-1,-1,-2,-1, 1, 5,-2,-2, 0],
    "W": [-3,-3,-4,-4,-2,-2,-3,-2,-2,-3,-2,-3,-1, 1,-4,-3,-2,11, 2,-3],
    "Y": [-2,-2,-2,-3,-2,-1,-2,-3, 2,-1,-1,-2,-1, 3,-3,-2,-2, 2, 7,-1],
    "V": [ 0,-3,-3,-3,-1,-2,-2,-3,-3, 3, 1,-2, 1,-1,-2,-2, 0,-3,-1, 4],
}
B62_ORDER = "ARNDCQEGHILKMFPSTWYV"
B62 = np.zeros((20, 20), dtype=np.float64)
for a1, row_vals in BLOSUM62_RAW.items():
    i1 = AA_TO_IDX[a1]
    for a2, val in zip(B62_ORDER, row_vals):
        i2 = AA_TO_IDX[a2]
        B62[i1, i2] = val / 5.0

EYE = np.eye(20)
RES = 0.65 * EYE + 0.35 * B62
ZERO20 = np.zeros(20, dtype=np.float64)

def encode_len(seqs, L):
    out = np.empty((len(seqs), 20 * L + 1), dtype=np.float64)
    for i, s in enumerate(seqs):
        for p in range(L):
            ch = s[p]
            out[i, p*20:(p+1)*20] = RES[AA_TO_IDX[ch]] if ch in AA_TO_IDX else ZERO20
        out[i, -1] = 1.0
    return out

def solve_censored_mm(X, y_raw, ineq, lam_vec, w_prior=None, sample_w=None, n_iter=15):
    D = X.shape[1]
    Lam = np.diag(lam_vec)
    Xw = (X * sample_w[:, None]) if sample_w is not None else X
    A_inv = np.linalg.inv(Xw.T @ X + Lam)
    rhs_prior = (Lam @ w_prior) if w_prior is not None else np.zeros(D)
    gt = (ineq == ">")
    lt = (ineq == "<")
    w = A_inv @ (Xw.T @ y_raw + rhs_prior)
    y_work = y_raw.copy()
    for _ in range(n_iter):
        yhat = X @ w
        y_work[gt] = np.maximum(y_raw[gt], yhat[gt])
        y_work[lt] = np.minimum(y_raw[lt], yhat[lt])
        w = A_inv @ (Xw.T @ y_work + rhs_prior)
    return w, y_work

bd2009["y_log"] = np.log10(np.clip(bd2009["meas"].values, 1.0, 100000.0))

# Step 1: Discover Allele-Specific Anchor Profiles and Modular Pocket Similarities on BD2009 9-mers!
lam_unif9 = np.concatenate([np.full(180, 15.0), [0.01]])
w9_init = {}
n9_cnt = {}
pos_norms_allele = {}

for al, grp in bd2009[bd2009["peptide_length"] == 9].groupby("allele"):
    X9 = encode_len(grp["sequence"].tolist(), 9)
    y9 = grp["y_log"].values
    w9, _ = solve_censored_mm(X9, y9, grp["inequality"].values, lam_unif9)
    w9_init[al] = w9
    n9_cnt[al] = len(grp)
    pnorms = np.linalg.norm(w9[:180].reshape(9, 20), axis=1)
    # Normalize so mean position weight is 1.0, clipped to [0.65, 2.2]
    pnorms = np.clip(pnorms / (pnorms.mean() + 1e-8), 0.65, 2.2)
    pos_norms_allele[al] = pnorms

alleles_9 = sorted(w9_init.keys())
al9_to_idx = {a: i for i, a in enumerate(alleles_9)}

# Modular Position-by-Position Pocket Cosine Similarity across all alleles in BD2009!
S_pos = np.zeros((9, len(alleles_9), len(alleles_9)), dtype=np.float64)
for p in range(9):
    Wp = np.array([w9_init[a][p*20:(p+1)*20] - w9_init[a][p*20:(p+1)*20].mean() for a in alleles_9])
    Wp_norm = Wp / (np.linalg.norm(Wp, axis=1, keepdims=True) + 1e-8)
    S_pos[p] = np.clip(Wp_norm @ Wp_norm.T, 0.0, 1.0)

# Global allele similarity combining anchor pocket similarity + empirical peptide co-binding in BD2009
S_anc_global = (
    0.12 * S_pos[0] + 0.32 * S_pos[1] + 0.14 * S_pos[2] +
    0.06 * S_pos[4] + 0.04 * S_pos[6] + 0.32 * S_pos[8]
)
pivot_bd = bd2009.pivot_table(index="sequence", columns="allele", values="y_log", aggfunc="mean")
val_mat = pivot_bd.reindex(columns=alleles_9).values
valid_mask = ~np.isnan(val_mat)
val_zero = np.where(valid_mask, val_mat - np.nanmean(val_mat, axis=0, keepdims=True), 0.0)
cov_num = val_zero.T @ val_zero
cnt_mat = valid_mask.astype(np.float64).T @ valid_mask.astype(np.float64)
var_vec = np.sum(val_zero ** 2, axis=0) / np.maximum(1.0, np.sum(valid_mask, axis=0))
corr_raw = cov_num / (np.sqrt(np.outer(var_vec, var_vec)) * cnt_mat + 1e-8)
shrink_w = cnt_mat / (cnt_mat + 18.0)
S_comb = np.clip(0.55 * S_anc_global + 0.45 * (shrink_w * corr_raw + (1.0 - shrink_w) * S_anc_global), 0.0, 1.0)
np.fill_diagonal(S_comb, 1.0)

# Construct Modular Pocket-Factorized Supertype Prior w9_sup_prior[al] and solve adaptive Censored-MM 9-mer models
w9_allele = {}
w9_sup_prior = {}
y9_censor_by_allele = {}
for i, al in enumerate(alleles_9):
    w_sup = np.zeros(181, dtype=np.float64)
    for p in range(9):
        # Combine position-p specific pocket similarity and global allele similarity
        sp = (0.60 * S_pos[p, i] + 0.40 * S_comb[i]) ** 3.5
        sp[i] = 0.0
        weights = sp * np.sqrt([n9_cnt[a] for a in alleles_9])
        if weights.sum() > 0:
            w_sup[p*20:(p+1)*20] = np.average([w9_init[a][p*20:(p+1)*20] for a in alleles_9], axis=0, weights=weights)
    w_sup[-1] = np.mean([w9_init[a][-1] for a in alleles_9])
    w9_sup_prior[al] = w_sup

    # Adaptive per-position lambda: inversely proportional to discovered anchor norm!
    pnorms = pos_norms_allele[al]
    lam_adaptive = 16.0 / (pnorms ** 1.6)
    lam_vec = np.concatenate([np.repeat(lam_adaptive, 20), [0.01]])

    grp = bd2009[(bd2009["allele"] == al) & (bd2009["peptide_length"] == 9)]
    X9 = encode_len(grp["sequence"].tolist(), 9)
    y9 = grp["y_log"].values
    w9, y9_cens = solve_censored_mm(X9, y9, grp["inequality"].values, lam_vec, w_prior=w_sup)
    w9_allele[al] = w9
    y9_censor_by_allele[al] = y9_cens

# Step 2: Fit Supertype-Pooled Nonlinear 9-mer Censored-MM Kernel Models for all 51 target alleles!
df9_all = bd2009[bd2009["peptide_length"] == 9].reset_index(drop=True)
X9_raw_all = encode_len(df9_all["sequence"].tolist(), 9)[:, :180]

rng = np.random.default_rng(42)
target_alleles = sorted(t_pan["mhckey"].apply(lambda x: x.rsplit("-", 1)[0]).unique())
nonlinear_9mer_models = {}

for al in target_alleles:
    i_al = al9_to_idx[al]
    pw9 = np.repeat(np.sqrt(pos_norms_allele[al]), 20)
    mask_self = (df9_all["allele"] == al).values
    idx_self = np.where(mask_self)[0]

    # Always include top supertype 9-mer neighbors with S_comb > 0.62!
    sims_vec = df9_all["allele"].map(lambda x: S_comb[i_al, al9_to_idx.get(x, i_al)]).values
    mask_nbr = (~mask_self) & (sims_vec > 0.60)
    idx_nbr = np.where(mask_nbr)[0]
    max_nbr = 2200
    if len(idx_nbr) > max_nbr:
        order = np.argsort(-sims_vec[idx_nbr], kind="mergesort")[:max_nbr]
        idx_nbr = idx_nbr[order]

    idx_tr = np.concatenate([idx_self, idx_nbr])
    F_tr = X9_raw_all[idx_tr] * pw9[None, :]
    F_tr = F_tr / (np.linalg.norm(F_tr, axis=1, keepdims=True) + 1e-8)

    sw = np.ones(len(idx_tr), dtype=np.float64)
    if len(idx_nbr) > 0:
        # Adaptive neighbor weight: higher when self sample size is smaller, still 0.25 when self is large!
        base_nbr_w = 0.45 * (800.0 / (len(idx_self) + 800.0)) + 0.15
        sw[len(idx_self):] = base_nbr_w * (sims_vec[idx_nbr] ** 3.5)

    M = min(650, len(F_tr))
    if len(idx_self) >= M:
        lm_idx = rng.choice(len(idx_self), size=M, replace=False)
    else:
        rem = rng.choice(len(F_tr) - len(idx_self), size=M - len(idx_self), replace=False) + len(idx_self)
        lm_idx = np.concatenate([np.arange(len(idx_self)), rem])
    F_L = F_tr[lm_idx]
    G_MM = F_L @ F_L.T
    K_MM = 0.5 * ((G_MM + 0.5) ** 3) + 0.5 * np.exp(1.6 * (G_MM - 1.0))
    U, S, _ = np.linalg.svd(K_MM + 1e-5 * np.eye(M))
    proj_M = U * (1.0 / np.sqrt(S))[None, :]
    G_NM = F_tr @ F_L.T
    K_NM = 0.5 * ((G_NM + 0.5) ** 3) + 0.5 * np.exp(1.6 * (G_NM - 1.0))
    Z_tr = np.hstack([K_NM @ proj_M, np.ones((len(F_tr), 1))])
    lam_z = np.full(Z_tr.shape[1], 1.1)
    lam_z[-1] = 0.01
    wz, _ = solve_censored_mm(Z_tr, df9_all.iloc[idx_tr]["y_log"].values, df9_all.iloc[idx_tr]["inequality"].values, lam_z, sample_w=sw)
    nonlinear_9mer_models[al] = (pw9, F_L, proj_M, wz)

print(f"Trained 51 Supertype-Pooled Nonlinear 9-mer models in {time.perf_counter()-t0:.2f}s")

def candidate_9mer_cores(seq):
    """
    Lundegaard et al. (2008) / Andreatta & Nielsen L29 candidate 9-mer cores:
    - For L=8: insert neutral wildcard 'X' at internal positions d in 1..7 AND stretch insertions at 2..6
    - For L=10: delete 1 residue at internal positions d in 1..8
    - For L=11: delete 2 contiguous residues at internal positions d in 1..8
    """
    L = len(seq)
    if L == 9:
        return [seq]
    elif L == 8:
        cores_x = [seq[:d] + "X" + seq[d:] for d in range(1, 8)]
        cores_dup = [seq[:d] + seq[d] + seq[d:] for d in range(2, 7)]
        return cores_x + cores_dup
    elif L == 10:
        return [seq[:d] + seq[d+1:] for d in range(1, 9)]
    elif L == 11:
        return [seq[:d] + seq[d+2:] for d in range(1, 9)]
    elif L > 11:
        step = L - 9
        return [seq[:d] + seq[d+step:] for d in range(1, L - step)]
    return [seq[:9]]

all_seqs = sorted(set(bd2009["sequence"]).union(set(blind["sequence"])))
seq_cores_X = {s: encode_len(candidate_9mer_cores(s), 9) for s in all_seqs}

def get_peptide_groove_features(seqs, al):
    w9 = w9_allele[al]
    pw9, F_L9, proj_M9, wz9 = nonlinear_9mer_models[al]
    N = len(seqs)
    X_best = np.empty((N, 180), dtype=np.float64)
    X_soft = np.empty((N, 180), dtype=np.float64)
    X_term = np.empty((N, 120), dtype=np.float64)
    s_feats = np.empty((N, 6), dtype=np.float64)

    for i, s in enumerate(seqs):
        Xc = seq_cores_X[s]
        Fc = Xc[:, :180] * pw9[None, :]
        Fc = Fc / (np.linalg.norm(Fc, axis=1, keepdims=True) + 1e-8)
        lin_ic50 = Xc @ w9
        G_c = Fc @ F_L9.T
        K_c = 0.5 * ((G_c + 0.5) ** 3) + 0.5 * np.exp(1.6 * (G_c - 1.0))
        nl_ic50 = (K_c @ proj_M9) @ wz9[:-1] + wz9[-1]

        comb_ic50 = 0.35 * lin_ic50 + 0.65 * nl_ic50
        best_i = int(np.argmin(comb_ic50))
        probs = softmax(-comb_ic50 * 3.0)
        X_best[i] = Fc[best_i]
        X_soft[i] = probs @ Fc
        t_str = s[:3] + s[-3:]
        for p, ch in enumerate(t_str):
            X_term[i, p*20:(p+1)*20] = RES[AA_TO_IDX.get(ch, 0)]
        s_feats[i, 0] = lin_ic50[best_i]
        s_feats[i, 1] = float(probs @ lin_ic50)
        s_feats[i, 2] = nl_ic50[best_i]
        s_feats[i, 3] = float(probs @ nl_ic50)
        s_feats[i, 4] = float(np.mean(nl_ic50))
        s_feats[i, 5] = float(comb_ic50[best_i])
    return X_best, X_soft, X_term, s_feats

# Build BD2009 Cross-Allele Lookup using Censored-MM standardized affinity scores!
seq_bd_lookup = {}
for s, al, ylog, ineq, plen in zip(bd2009["sequence"], bd2009["allele"], bd2009["y_log"], bd2009["inequality"], bd2009["peptide_length"]):
    if al not in al9_to_idx:
        continue
    score = 2.69897 - ylog
    if ineq == ">" and ylog >= 2.69897:
        score = min(score, -1.0)
    seq_bd_lookup.setdefault(s, []).append((al9_to_idx[al], score, plen))

# Precompute Multi-Length Super-Groove caches for ALL 51 target alleles (ALWAYS pooling top supertype neighbors!)
allele_nystrom_cache = {}
for al in target_alleles:
    i_al = al9_to_idx[al]
    sub_self = bd2009[bd2009["allele"] == al].reset_index(drop=True)
    sims_vec = bd2009["allele"].map(lambda x: S_comb[i_al, al9_to_idx.get(x, i_al)]).values
    mask_nbr = (bd2009["allele"] != al).values & (sims_vec > 0.60)
    sub_nbr = bd2009[mask_nbr].copy()
    if len(sub_nbr) > 1800:
        nbr_sims = sims_vec[mask_nbr]
        top_i = np.argsort(-nbr_sims, kind="mergesort")[:1800]
        sub_nbr = sub_nbr.iloc[top_i]
    sub_al_all = pd.concat([sub_self, sub_nbr], ignore_index=True)
    is_self = np.zeros(len(sub_al_all), dtype=bool)
    is_self[:len(sub_self)] = True
    nbr_sim_arr = sub_al_all["allele"].map(lambda x: S_comb[i_al, al9_to_idx.get(x, i_al)]).values

    Xb_tr, Xs_tr, Xt_tr, sf_tr = get_peptide_groove_features(sub_al_all["sequence"].tolist(), al)
    Xt_norm = Xt_tr / (np.linalg.norm(Xt_tr, axis=1, keepdims=True) + 1e-8)
    F_tr = np.hstack([0.55 * Xb_tr + 0.45 * Xs_tr, 0.55 * Xt_norm])
    F_tr = F_tr / (np.linalg.norm(F_tr, axis=1, keepdims=True) + 1e-8)
    M = min(650, len(F_tr))
    if len(sub_self) >= M:
        lm_idx = rng.choice(len(sub_self), size=M, replace=False)
    else:
        rem = rng.choice(len(F_tr) - len(sub_self), size=M - len(sub_self), replace=False) + len(sub_self)
        lm_idx = np.concatenate([np.arange(len(sub_self)), rem])
    F_L = F_tr[lm_idx]
    G_MM = F_L @ F_L.T
    K_MM = 0.5 * ((G_MM + 0.5) ** 3) + 0.5 * np.exp(1.5 * (G_MM - 1.0))
    U, S, _ = np.linalg.svd(K_MM + 1e-5 * np.eye(M))
    proj_M = U * (1.0 / np.sqrt(S))[None, :]
    G_NM = F_tr @ F_L.T
    K_NM = 0.5 * ((G_NM + 0.5) ** 3) + 0.5 * np.exp(1.5 * (G_NM - 1.0))
    Z_tr = np.hstack([K_NM @ proj_M, np.ones((len(F_tr), 1))])
    allele_nystrom_cache[al] = (sub_al_all, is_self, nbr_sim_arr, F_L, proj_M, Z_tr, sf_tr)

print(f"Precomputed 51 Supertype-Pooled Multi-Length caches in {time.perf_counter()-t0:.2f}s")

aucs_seq = []
aucs_full = []
l1_cache = {}

for idx, row in t_pan.iterrows():
    k = row["mhckey"]
    al, plen_s = k.rsplit("-", 1)
    L = int(plen_s)
    i_al = al9_to_idx[al]
    sub_tr = bd2009[bd2009["mhckey"] == k]
    sub_te = blind[blind["mhckey"] == k]
    y_true = (sub_te["meas"].values < 500.0).astype(int)

    # 1. Native length-L linear & nonlinear Censored MM (with supertype-pooled same-length prior!)
    pnorms9 = pos_norms_allele[al]
    if L == 9:
        pnormsL = pnorms9
    else:
        pnormsL = np.ones(L)
        pnormsL[:3] = pnorms9[:3]
        pnormsL[-1] = pnorms9[-1]
        pnormsL[-2] = pnorms9[-2]
        pnormsL[3:-2] = np.mean(pnorms9[3:7])

    lamL = np.concatenate([np.repeat(16.0 / (pnormsL ** 1.6), 20), [0.01]])
    w_prior = np.zeros(20 * L + 1)
    w9 = w9_allele[al]
    w_prior[-1] = w9[-1]
    if L == 9:
        w_prior = w9_sup_prior[al].copy()
    else:
        w_prior[:60] = w9[:60]
        w_prior[-21:-1] = w9[160:180]
        mid_mean = w9[60:160].reshape(5, 20).mean(axis=0)
        for p in range(3, L - 1):
            w_prior[p*20:(p+1)*20] = mid_mean

    X_tr_L = encode_len(sub_tr["sequence"].tolist(), L)
    X_te_L = encode_len(sub_te["sequence"].tolist(), L)
    y_raw_L = sub_tr["y_log"].values
    wL, _ = solve_censored_mm(X_tr_L, y_raw_L, sub_tr["inequality"].values, lamL, w_prior=w_prior)
    pred_lin_L = -(X_te_L @ wL)

    # Native length-L Nystrom Kernel (pooling same-length supertype neighbors!)
    sub_len_all = bd2009[bd2009["peptide_length"] == L].reset_index(drop=True)
    mask_l_self = (sub_len_all["allele"] == al).values
    idx_l_self = np.where(mask_l_self)[0]
    sims_l = sub_len_all["allele"].map(lambda x: S_comb[i_al, al9_to_idx.get(x, i_al)]).values
    idx_l_nbr = np.where((~mask_l_self) & (sims_l > 0.60))[0]
    if len(idx_l_nbr) > 1500:
        idx_l_nbr = idx_l_nbr[np.argsort(-sims_l[idx_l_nbr], kind="mergesort")[:1500]]
    idx_l_tr = np.concatenate([idx_l_self, idx_l_nbr])
    sub_l_tr = sub_len_all.iloc[idx_l_tr]
    XL_pool = encode_len(sub_l_tr["sequence"].tolist(), L)
    pwL = np.repeat(np.sqrt(pnormsL), 20)
    FL_tr = XL_pool[:, :-1] * pwL[None, :]
    FL_te = X_te_L[:, :-1] * pwL[None, :]
    FL_tr = FL_tr / (np.linalg.norm(FL_tr, axis=1, keepdims=True) + 1e-8)
    FL_te = FL_te / (np.linalg.norm(FL_te, axis=1, keepdims=True) + 1e-8)
    ML = min(500, len(FL_tr))
    if len(idx_l_self) >= ML:
        lm_L = rng.choice(len(idx_l_self), size=ML, replace=False)
    else:
        rem = rng.choice(len(FL_tr) - len(idx_l_self), size=ML - len(idx_l_self), replace=False) + len(idx_l_self)
        lm_L = np.concatenate([np.arange(len(idx_l_self)), rem])
    B_L = FL_tr[lm_L]
    GMM_L = B_L @ B_L.T
    KMM_L = 0.5 * ((GMM_L + 0.5) ** 3) + 0.5 * np.exp(1.5 * (GMM_L - 1.0))
    UL, SL, _ = np.linalg.svd(KMM_L + 1e-5 * np.eye(ML))
    projL = UL * (1.0 / np.sqrt(SL))[None, :]
    KNM_L = 0.5 * (((FL_tr @ B_L.T) + 0.5) ** 3) + 0.5 * np.exp(1.5 * ((FL_tr @ B_L.T) - 1.0))
    KTE_L = 0.5 * (((FL_te @ B_L.T) + 0.5) ** 3) + 0.5 * np.exp(1.5 * ((FL_te @ B_L.T) - 1.0))
    ZL_tr = np.hstack([KNM_L @ projL, np.ones((len(FL_tr), 1))])
    ZL_te = np.hstack([KTE_L @ projL, np.ones((len(FL_te), 1))])
    sw_L = np.ones(len(idx_l_tr))
    if len(idx_l_nbr) > 0:
        base_w = 0.45 * (600.0 / (len(idx_l_self) + 600.0)) + 0.15
        sw_L[len(idx_l_self):] = base_w * (sims_l[idx_l_nbr] ** 3.5)
    lam_zL = np.full(ZL_tr.shape[1], 1.15); lam_zL[-1] = 0.01
    wzL, _ = solve_censored_mm(ZL_tr, sub_l_tr["y_log"].values, sub_l_tr["inequality"].values, lam_zL, sample_w=sw_L)
    pred_nl_L = -(ZL_te @ wzL)

    # 2. Multi-length Groove Nystrom Kernel + Nonlinear 9-mer L29 core projection
    sub_al_all, is_self, nbr_sim_arr, F_L, proj_M, Z_tr, sf_tr = allele_nystrom_cache[al]
    Xb_te, Xs_te, Xt_te, sf_te = get_peptide_groove_features(sub_te["sequence"].tolist(), al)

    pred_9nl_proj = -(0.50 * sf_te[:, 2] + 0.35 * sf_te[:, 3] + 0.15 * sf_te[:, 4])

    Xt_te_norm = Xt_te / (np.linalg.norm(Xt_te, axis=1, keepdims=True) + 1e-8)
    F_te = np.hstack([0.55 * Xb_te + 0.45 * Xs_te, 0.55 * Xt_te_norm])
    F_te = F_te / (np.linalg.norm(F_te, axis=1, keepdims=True) + 1e-8)
    G_te = F_te @ F_L.T
    K_te = 0.5 * ((G_te + 0.5) ** 3) + 0.5 * np.exp(1.5 * (G_te - 1.0))
    Z_te = np.hstack([K_te @ proj_M, np.ones((len(F_te), 1))])

    same_len_tr = (sub_al_all["peptide_length"].values == L).astype(np.float64)
    sample_w = np.where(is_self, np.where(same_len_tr > 0.5, 1.0, 0.55), 0.28 * (nbr_sim_arr ** 3.5))
    lam_z = np.full(Z_tr.shape[1], 1.15); lam_z[-1] = 0.01
    w_z, _ = solve_censored_mm(Z_tr, sub_al_all["y_log"].values, sub_al_all["inequality"].values, lam_z, sample_w=sample_w)
    pred_groove_krr = -(Z_te @ w_z)

    def znorm(v):
        return (v - v.mean()) / (v.std() + 1e-8)

    # Weight native length-L model by NUMBER OF BINDERS in sub_tr (effective positive sample size!)
    n_binders_L = int((sub_tr["meas"] < 500.0).sum())
    if L == 9:
        w_native = n_binders_L / (n_binders_L + 35.0)
    else:
        w_native = n_binders_L / (n_binders_L + 85.0)

    pred_native_comb = 0.38 * znorm(pred_lin_L) + 0.62 * znorm(pred_nl_L)
    pred_pan_comb = 0.50 * znorm(pred_groove_krr) + 0.50 * znorm(pred_9nl_proj)
    pred_seq_only = w_native * pred_native_comb + (1.0 - w_native * 0.60) * pred_pan_comb
    aucs_seq.append(roc_auc_score(y_true, pred_seq_only))

    # 3. Calibrated BD2009 Cross-Allele Kronecker Panel Lookup
    pred_panel = np.zeros(len(sub_te), dtype=np.float64)
    for i, s in enumerate(sub_te["sequence"]):
        recs = seq_bd_lookup.get(s, [])
        num, den = 0.0, 0.0
        for other_a, sc, other_len in recs:
            if other_a == i_al and other_len == L:
                continue
            sim = S_comb[i_al, other_a]
            if sim > 0.45:
                w = (sim ** 4.0) * (1.0 if other_len == L else 0.7)
                num += w * sc
                den += w
        if den > 0.1:
            pred_panel[i] = num / (den + 1.2)

    pred_full = znorm(pred_seq_only) + 0.22 * pred_panel
    aucs_full.append(roc_auc_score(y_true, pred_full))
    l1_cache[f"{idx}_y"] = y_true
    l1_cache[f"{idx}_lin"] = pred_lin_L
    l1_cache[f"{idx}_nl"] = pred_nl_L
    l1_cache[f"{idx}_groove"] = pred_groove_krr
    l1_cache[f"{idx}_9nl"] = pred_9nl_proj
    l1_cache[f"{idx}_panel"] = pred_panel
    l1_cache[f"{idx}_seq"] = pred_seq_only
    l1_cache[f"{idx}_full"] = pred_full

np.savez("./cache_lens1_components_clean.npz", **l1_cache)

aucs_seq = np.array(aucs_seq)
aucs_full = np.array(aucs_full)
ref_net = t_net["blind"].values
ref_pan = t_pan["blind"].values
ref_smm = t_smm["blind"].values

print(f"Done in {time.perf_counter()-t0:.2f}s!")
print(f"87-dataset Pure Sequence Modular-Pan Mean Blind AUC: {aucs_seq.mean():.6f} (wins vs NetMHC: {(aucs_seq > ref_net).sum()}/87, vs NetMHCpan: {(aucs_seq > ref_pan).sum()}/87)")
print(f"87-dataset Full (Seq + BD2009 Panel) Mean Blind AUC: {aucs_full.mean():.6f} (wins vs NetMHC: {(aucs_full > ref_net).sum()}/87, vs NetMHCpan: {(aucs_full > ref_pan).sum()}/87)")
for plen in [8, 9, 10, 11]:
    m = (t_pan["mhckey"].str.endswith(f"-{plen}")).values
    vn = t_net.loc[m, "blind"].mean()
    vp = t_pan.loc[m, "blind"].mean()
    print(f"  Len {plen:2d} (n={m.sum():2d}): SeqOnly={aucs_seq[m].mean():.4f} | Full={aucs_full[m].mean():.4f} | NetMHC={vn:.4f} | NetMHCpan={vp:.4f}")

idx_bl20 = t_pan.sort_values(["size_bl", "mhckey"]).index[:20]
idx_cv20 = t_pan.sort_values(["size_cv", "mhckey"]).index[:20]
print(f"20 smallest by size_bl: Ours={aucs_full[idx_bl20].mean():.6f} vs NetMHC={ref_net[idx_bl20].mean():.6f} ({aucs_full[idx_bl20].mean()-ref_net[idx_bl20].mean():+.6f}), Pan={ref_pan[idx_bl20].mean():.6f}")
print(f"20 smallest by size_cv: Ours={aucs_full[idx_cv20].mean():.6f} vs NetMHC={ref_net[idx_cv20].mean():.6f} ({aucs_full[idx_cv20].mean()-ref_net[idx_cv20].mean():+.6f}), Pan={ref_pan[idx_cv20].mean():.6f}")
