#!/usr/bin/env python3
"""
Lens 2: Model-Space Supertype Ensemble + Training-Time Cross-Allele Matrix Completion +
Exon-2 (N-pocket) / Exon-3 (C-pocket) Modular Split + Exact Dual Kernel Censored-MM (MM-Tobit)
+ Pairwise Anchor Potts Epistasis (strictly BD2009-trained).
Single-thread we* (https://github.com/mizopl/we-star) Law M7 implementation.
"""
import time
import numpy as np
import pandas as pd
from scipy.special import softmax, expit
from scipy.stats import binomtest
from sklearn.metrics import roc_auc_score

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

bd2009["y_log"] = np.log10(np.clip(bd2009["meas"].values, 1.0, 100000.0))

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
RES = 0.68 * EYE + 0.32 * B62
MEAN_RES = RES.mean(axis=0)

def encode_len(seqs, L):
    out = np.empty((len(seqs), 20 * L + 1), dtype=np.float64)
    for i, s in enumerate(seqs):
        for p in range(L):
            ch = s[p]
            out[i, p*20:(p+1)*20] = RES[AA_TO_IDX[ch]] if ch in AA_TO_IDX else MEAN_RES
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

# Canonical serological supertype / family prior hierarchy (Sidney et al. 2008, pre-2009)
SUPERTYPE_MAP = {
    "HLA-A-6801": "HLA-A-03", "HLA-A-1101": "HLA-A-03", "HLA-A-3101": "HLA-A-03", "HLA-A-3301": "HLA-A-03",
    "HLA-A-6802": "HLA-A-02", "HLA-A-6901": "HLA-A-02",
    "HLA-A-2301": "HLA-A-24", "HLA-A-2402": "HLA-A-24",
    "HLA-A-2501": "HLA-A-26", "HLA-A-2601": "HLA-A-26", "HLA-A-2602": "HLA-A-26", "HLA-A-2603": "HLA-A-26",
    "HLA-B-1517": "HLA-B-58", "HLA-B-5701": "HLA-B-58", "HLA-B-5801": "HLA-B-58",
    "HLA-B-3801": "HLA-B-39", "HLA-B-3901": "HLA-B-39", "HLA-B-1509": "HLA-B-39",
    "HLA-B-4001": "HLA-B-44", "HLA-B-4002": "HLA-B-44", "HLA-B-4402": "HLA-B-44", "HLA-B-4403": "HLA-B-44", "HLA-B-4501": "HLA-B-44", "HLA-B-1801": "HLA-B-44",
    "HLA-B-0702": "HLA-B-07", "HLA-B-3501": "HLA-B-07", "HLA-B-5101": "HLA-B-07", "HLA-B-5301": "HLA-B-07", "HLA-B-5401": "HLA-B-07",
}
def get_allele_hierarchy(allele):
    if allele in SUPERTYPE_MAP:
        fam = SUPERTYPE_MAP[allele]
        return fam[:5], fam
    if allele.startswith("HLA-"):
        parts = allele.split("-")
        locus = f"HLA-{parts[1]}"
        fam = f"HLA-{parts[1]}-{parts[2][:2]}" if len(parts) > 2 else locus
        return locus, fam
    elif allele.startswith("Mamu-"):
        return "Mamu", allele[:7]
    elif allele.startswith("H-2-"):
        return "H-2", allele[:5]
    return allele.split("-")[0], allele

# Step 1: Fit hierarchical 9-mer Censored MM models so small alleles (HLA-A-2603, HLA-B-3801, etc.)
# have clean, de-noised anchor motifs!
lam9_std = np.concatenate([np.repeat([12.0, 4.0, 12.0, 30.0, 32.0, 30.0, 20.0, 24.0, 4.0], 20), [0.01]])
df9 = bd2009[bd2009["peptide_length"] == 9].reset_index(drop=True)
X9_df = encode_len(df9["sequence"].tolist(), 9)

w9_fam = {}
for fam in set(get_allele_hierarchy(a)[1] for a in df9["allele"].unique()):
    mask = (df9["allele"].apply(lambda a: get_allele_hierarchy(a)[1] == fam)).values
    if mask.sum() > 0:
        w_f, _ = solve_censored_mm(X9_df[mask], df9.loc[mask, "y_log"].values, df9.loc[mask, "inequality"].values, lam9_std * 1.5)
        w9_fam[fam] = w_f

w9_init = {}
n9_cnt = {}
pos_norms_allele = {}
for al, grp in df9.groupby("allele"):
    _, fam = get_allele_hierarchy(al)
    prior_f = w9_fam.get(fam, np.zeros(181))
    X9 = encode_len(grp["sequence"].tolist(), 9)
    y9 = grp["y_log"].values
    w9, _ = solve_censored_mm(X9, y9, grp["inequality"].values, lam9_std, w_prior=prior_f)
    w9_init[al] = w9
    n9_cnt[al] = len(grp)
    pnorms = np.linalg.norm(w9[:180].reshape(9, 20), axis=1)
    pnorms = np.clip(pnorms / (pnorms.mean() + 1e-8), 0.65, 2.2)
    pos_norms_allele[al] = pnorms

alleles_9 = sorted(w9_init.keys())
al9_to_idx = {a: i for i, a in enumerate(alleles_9)}

# Compute Modular Position-by-Position Pocket Similarity S_pos[9, n_al, n_al], N-pocket S_N, and C-pocket S_C
S_pos = np.zeros((9, len(alleles_9), len(alleles_9)), dtype=np.float64)
for p in range(9):
    Wp = np.array([w9_init[a][p*20:(p+1)*20] - w9_init[a][p*20:(p+1)*20].mean() for a in alleles_9])
    Wp_norm = Wp / (np.linalg.norm(Wp, axis=1, keepdims=True) + 1e-8)
    S_pos[p] = np.clip(Wp_norm @ Wp_norm.T, 0.0, 1.0)

S_N = 0.20 * S_pos[0] + 0.55 * S_pos[1] + 0.25 * S_pos[2]
S_C = 0.15 * S_pos[6] + 0.15 * S_pos[7] + 0.70 * S_pos[8]
S_anc_global = 0.45 * S_N + 0.10 * S_pos[4] + 0.45 * S_C

pivot_bd = bd2009.pivot_table(index="sequence", columns="allele", values="y_log", aggfunc="mean")
val_mat = pivot_bd.reindex(columns=alleles_9).values
valid_mask = ~np.isnan(val_mat)
val_zero = np.where(valid_mask, val_mat - np.nanmean(val_mat, axis=0, keepdims=True), 0.0)
cov_num = val_zero.T @ val_zero
cnt_mat = valid_mask.astype(np.float64).T @ valid_mask.astype(np.float64)
var_vec = np.sum(val_zero ** 2, axis=0) / np.maximum(1.0, np.sum(valid_mask, axis=0))
corr_raw = cov_num / (np.sqrt(np.outer(var_vec, var_vec)) * cnt_mat + 1e-8)
shrink_w = cnt_mat / (cnt_mat + 18.0)
S_comb = np.clip(0.60 * S_anc_global + 0.40 * (shrink_w * corr_raw + (1.0 - shrink_w) * S_anc_global), 0.0, 1.0)
np.fill_diagonal(S_comb, 1.0)

# Solve Modular Pocket-Factorized Linear 9-mer models
w9_allele = {}
w9_sup_prior = {}
for i, al in enumerate(alleles_9):
    _, fam = get_allele_hierarchy(al)
    w_sup = np.zeros(181, dtype=np.float64)
    for p in range(9):
        sp = (0.60 * S_pos[p, i] + 0.40 * S_comb[i]) ** 3.5
        sp[i] = 0.0
        weights = sp * np.sqrt([n9_cnt[a] for a in alleles_9])
        if weights.sum() > 0:
            w_sup[p*20:(p+1)*20] = np.average([w9_init[a][p*20:(p+1)*20] for a in alleles_9], axis=0, weights=weights)
    w_sup[-1] = np.mean([w9_init[a][-1] for a in alleles_9])
    if fam in w9_fam:
        w_sup = 0.65 * w_sup + 0.35 * w9_fam[fam]
    w9_sup_prior[al] = w_sup

    pnorms = pos_norms_allele[al]
    lam_adaptive = 15.0 / (pnorms ** 1.6)
    lam_vec = np.concatenate([np.repeat(lam_adaptive, 20), [0.01]])
    grp = df9[df9["allele"] == al]
    X9 = encode_len(grp["sequence"].tolist(), 9)
    w9, _ = solve_censored_mm(X9, grp["y_log"].values, grp["inequality"].values, lam_vec, w_prior=w_sup)
    w9_allele[al] = w9

# Also fit Exon-2 (N-pocket: pos 0..4) and Exon-3 (C-pocket: pos 4..9) Censored-MM models per allele!
def enc_sub9(seqs, start, end):
    L = end - start
    out = np.zeros((len(seqs), 20 * L + 1))
    for i, s in enumerate(seqs):
        for p, ch in enumerate(s[start:end]):
            out[i, p*20:(p+1)*20] = RES[AA_TO_IDX[ch]] if ch in AA_TO_IDX else MEAN_RES
        out[i, -1] = 1.0
    return out

wN_raw, wC_raw = {}, {}
lam_N = np.concatenate([np.repeat([10.0, 4.0, 10.0, 25.0], 20), [0.01]])
lam_C = np.concatenate([np.repeat([25.0, 25.0, 18.0, 20.0, 4.0], 20), [0.01]])
for al in alleles_9:
    grp = df9[df9["allele"] == al]
    s_list = grp["sequence"].tolist()
    y9 = grp["y_log"].values
    in9 = grp["inequality"].values
    wN_raw[al], _ = solve_censored_mm(enc_sub9(s_list, 0, 4), y9, in9, lam_N)
    wC_raw[al], _ = solve_censored_mm(enc_sub9(s_list, 4, 9), y9, in9, lam_C)

wN_ens, wC_ens = {}, {}
for i, al in enumerate(alleles_9):
    sn = (S_N[i] ** 4.0).copy(); sn[i] = 0.0
    sc = (S_C[i] ** 4.0).copy(); sc[i] = 0.0
    wn_w = sn * np.sqrt([n9_cnt[a] for a in alleles_9])
    wc_w = sc * np.sqrt([n9_cnt[a] for a in alleles_9])
    self_share = n9_cnt[al] / (n9_cnt[al] + 450.0)
    wN_nbr = np.average([wN_raw[a] for a in alleles_9], axis=0, weights=wn_w) if wn_w.sum() > 0 else wN_raw[al]
    wC_nbr = np.average([wC_raw[a] for a in alleles_9], axis=0, weights=wc_w) if wc_w.sum() > 0 else wC_raw[al]
    wN_ens[al] = self_share * wN_raw[al] + (1.0 - self_share) * wN_nbr
    wC_ens[al] = self_share * wC_raw[al] + (1.0 - self_share) * wC_nbr

# Step 2: Fit Dedicated Exact Dual Kernel 9-mer Models per Allele (for Model-Space Supertype Transfer!)
# Plus Supertype-Pooled Nystrom 9-mer Models!
rng = np.random.default_rng(42)
target_alleles = sorted(t_pan["mhckey"].apply(lambda x: x.rsplit("-", 1)[0]).unique())
exact_dual_9mer = {}
nonlinear_9mer_models = {}

for al in alleles_9:
    grp = df9[df9["allele"] == al]
    if len(grp) < 50:
        continue
    # Subsample at most 3000 rows for speed on huge alleles
    if len(grp) > 3000:
        idx_sub = rng.choice(len(grp), size=3000, replace=False)
        grp = grp.iloc[idx_sub]
    pw9 = np.repeat(np.sqrt(pos_norms_allele[al]), 20)
    X = encode_len(grp["sequence"].tolist(), 9)[:, :180] * pw9[None, :]
    X = X / (np.linalg.norm(X, axis=1, keepdims=True) + 1e-8)
    G = X @ X.T
    K = 0.5 * ((G + 0.5) ** 3) + 0.5 * np.exp(1.5 * (G - 1.0))
    K_inv = np.linalg.inv(K + 0.90 * np.eye(len(grp)))
    P = K @ K_inv
    y = grp["y_log"].values
    gt = (grp["inequality"].values == ">")
    lt = (grp["inequality"].values == "<")
    yw = y.copy()
    for _ in range(12):
        yh = P @ yw
        yw[gt] = np.maximum(y[gt], yh[gt])
        yw[lt] = np.minimum(y[lt], yh[lt])
    exact_dual_9mer[al] = (pw9, X, K_inv @ yw)

for al in target_alleles:
    i_al = al9_to_idx[al]
    pw9 = np.repeat(np.sqrt(pos_norms_allele[al]), 20)
    mask_self = (df9["allele"] == al).values
    idx_self = np.where(mask_self)[0]
    sims_vec = df9["allele"].map(lambda x: S_comb[i_al, al9_to_idx.get(x, i_al)]).values
    mask_nbr = (~mask_self) & (sims_vec > 0.60)
    idx_nbr = np.where(mask_nbr)[0]
    if len(idx_nbr) > 2200:
        idx_nbr = idx_nbr[np.argsort(-sims_vec[idx_nbr], kind="mergesort")[:2200]]
    idx_tr = np.concatenate([idx_self, idx_nbr])
    F_tr = X9_df[idx_tr, :180] * pw9[None, :]
    F_tr = F_tr / (np.linalg.norm(F_tr, axis=1, keepdims=True) + 1e-8)
    sw = np.ones(len(idx_tr), dtype=np.float64)
    if len(idx_nbr) > 0:
        base_nbr_w = 0.50 * (800.0 / (len(idx_self) + 800.0)) + 0.15
        sw[len(idx_self):] = base_nbr_w * (sims_vec[idx_nbr] ** 3.0)
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
    lam_z = np.full(Z_tr.shape[1], 1.1); lam_z[-1] = 0.01
    wz, _ = solve_censored_mm(Z_tr, df9.iloc[idx_tr]["y_log"].values, df9.iloc[idx_tr]["inequality"].values, lam_z, sample_w=sw)
    nonlinear_9mer_models[al] = (pw9, F_L, proj_M, wz)

print(f"Trained Exact Dual & Supertype-Pooled 9-mer models in {time.perf_counter()-t0:.2f}s")

def candidate_9mer_cores_stretch(seq):
    """Canonical stretch/bulge cores (preserving unit amino acid scale at all 9 positions)."""
    L = len(seq)
    if L == 9:
        return [seq]
    elif L == 8:
        return [seq[:d] + seq[d] + seq[d:] for d in range(2, 7)]
    elif L == 10:
        return [seq[:d] + seq[d+1:] for d in range(1, 9)]
    elif L == 11:
        return [seq[:d] + seq[d+2:] for d in range(1, 9)]
    elif L > 11:
        step = L - 9
        return [seq[:d] + seq[d+step:] for d in range(1, L - step)]
    return [seq[:9]]

def candidate_9mer_cores_wildcard8(seq):
    """Lundegaard et al. (2008) L29 wildcard insertion cores for 8-mers."""
    return [seq[:d] + "X" + seq[d:] for d in range(1, 8)]

all_seqs = sorted(set(bd2009["sequence"]).union(set(blind["sequence"])))
seq_cores_X = {s: encode_len(candidate_9mer_cores_stretch(s), 9) for s in all_seqs}
seq_cores_wild8 = {s: encode_len(candidate_9mer_cores_wildcard8(s), 9) for s in all_seqs if len(s) == 8}

def get_peptide_groove_features(seqs, al):
    w9 = w9_allele[al]
    pw9, F_L9, proj_M9, wz9 = nonlinear_9mer_models[al]
    N = len(seqs)
    X_best = np.empty((N, 180), dtype=np.float64)
    X_soft = np.empty((N, 180), dtype=np.float64)
    X_term = np.empty((N, 120), dtype=np.float64)
    s_feats = np.empty((N, 8), dtype=np.float64)

    wN = wN_ens[al]
    wC = wC_ens[al]

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
        # Exon-2 (N-pocket) + Exon-3 (C-pocket) modular split score on best core
        best_core_x = Xc[best_i]
        xn_vec = np.append(best_core_x[:80], 1.0)
        xc_vec = np.append(best_core_x[80:180], 1.0)
        s_feats[i, 5] = float(xn_vec @ wN + xc_vec @ wC)
        # If L == 8, also compute wildcard L29 mean score
        if len(s) == 8:
            Xw = seq_cores_wild8[s]
            Fw = Xw[:, :180] * pw9[None, :]
            Fw = Fw / (np.linalg.norm(Fw, axis=1, keepdims=True) + 1e-8)
            Gw = Fw @ F_L9.T
            Kw = 0.5 * ((Gw + 0.5) ** 3) + 0.5 * np.exp(1.6 * (Gw - 1.0))
            nl_w = (Kw @ proj_M9) @ wz9[:-1] + wz9[-1]
            s_feats[i, 6] = float(np.mean(nl_w))
            s_feats[i, 7] = float(np.min(nl_w))
        else:
            s_feats[i, 6] = s_feats[i, 4]
            s_feats[i, 7] = s_feats[i, 2]
    return X_best, X_soft, X_term, s_feats

def eval_model_space_supertype_9mer(seqs, al):
    """
    Evaluate Exact Dual Kernel 9-mer models of top supertype neighbor alleles on seqs
    (via each peptide's candidate 9-mer cores) — 100% pure sequence f(allele, seq)!
    """
    i_al = al9_to_idx[al]
    sims = S_comb[i_al].copy()
    # Select top 5 alleles (including self) with sims >= 0.55
    top_indices = np.argsort(-sims)[:5]
    ens_pred = np.zeros(len(seqs), dtype=np.float64)
    total_w = 0.0
    for idx_n in top_indices:
        al_n = alleles_9[idx_n]
        sim_val = sims[idx_n]
        if sim_val < 0.52 or al_n not in exact_dual_9mer:
            continue
        w_n = 1.0 if al_n == al else (sim_val ** 3.5) * (500.0 / (n9_cnt[al] + 500.0) + 0.20)
        pw_n, X_tr_n, alpha_n = exact_dual_9mer[al_n]
        preds_n = np.empty(len(seqs), dtype=np.float64)
        for i, s in enumerate(seqs):
            Xc = seq_cores_X[s][:, :180] * pw_n[None, :]
            Xc = Xc / (np.linalg.norm(Xc, axis=1, keepdims=True) + 1e-8)
            G = Xc @ X_tr_n.T
            K = 0.5 * ((G + 0.5) ** 3) + 0.5 * np.exp(1.5 * (G - 1.0))
            ic50s = K @ alpha_n
            preds_n[i] = -(0.55 * np.min(ic50s) + 0.45 * np.mean(ic50s))
        if preds_n.std() > 1e-8:
            preds_n = (preds_n - preds_n.mean()) / preds_n.std()
        ens_pred += w_n * preds_n
        total_w += w_n
    return ens_pred / (total_w + 1e-8)

# Precompute Multi-Length Super-Groove caches for ALL 51 target alleles
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

print(f"Precomputed 51 Multi-Length caches in {time.perf_counter()-t0:.2f}s")

seq_bd_lookup = {}
for s, al, ylog, ineq, plen in zip(bd2009["sequence"], bd2009["allele"], bd2009["y_log"], bd2009["inequality"], bd2009["peptide_length"]):
    if al not in al9_to_idx:
        continue
    score = 2.69897 - ylog
    if ineq == ">" and ylog >= 2.69897:
        score = min(score, -1.0)
    seq_bd_lookup.setdefault(s, []).append((al9_to_idx[al], score, plen))

aucs_seq = []
aucs_full = []
clean_cache = {}

# Physicochemical 5D descriptor for pairwise anchor epistasis
PHYS5_RAW = {
    "A": [ 1.8, 0.31,  0.0, 0.0, 0.0], "R": [-4.5, 1.01,  1.0, 1.0, 0.0],
    "N": [-3.5, 0.56,  0.0, 1.0, 0.0], "D": [-3.5, 0.54, -1.0, 1.0, 0.0],
    "C": [ 2.5, 0.55,  0.0, 0.0, 0.0], "Q": [-3.5, 0.72,  0.0, 1.0, 0.0],
    "E": [-3.5, 0.68, -1.0, 1.0, 0.0], "G": [-0.4, 0.00,  0.0, 0.0, 0.0],
    "H": [-3.2, 0.79,  0.5, 1.0, 0.5], "I": [ 4.5, 0.85,  0.0, 0.0, 0.0],
    "L": [ 3.8, 0.85,  0.0, 0.0, 0.0], "K": [-3.9, 0.89,  1.0, 1.0, 0.0],
    "M": [ 1.9, 0.83,  0.0, 0.0, 0.0], "F": [ 2.8, 0.99,  0.0, 0.0, 1.0],
    "P": [-1.6, 0.46,  0.0, 0.0, 0.0], "S": [-0.8, 0.38,  0.0, 0.5, 0.0],
    "T": [-0.7, 0.53,  0.0, 0.5, 0.0], "W": [-0.9, 1.25,  0.0, 0.0, 1.0],
    "Y": [-1.3, 1.00,  0.0, 0.5, 1.0], "V": [ 4.2, 0.68,  0.0, 0.0, 0.0],
}
PHYS5 = np.zeros((20, 5), dtype=np.float64)
for i_a, a_ch in enumerate(AAS):
    PHYS5[i_a] = np.array(PHYS5_RAW[a_ch], dtype=np.float64)
PHYS5 = (PHYS5 - PHYS5.mean(axis=0)) / (PHYS5.std(axis=0) + 1e-8)
CHEM_EMB = np.hstack([B62, 0.35 * PHYS5])
CHEM_EMB /= (np.linalg.norm(CHEM_EMB, axis=1, keepdims=True) + 1e-8)

def encode_chem_epistasis_len(seqs, L, pnormsL):
    n = len(seqs)
    pw = np.sqrt(pnormsL)
    X_pos = np.zeros((n, 25 * L), dtype=np.float64)
    X_pairs = np.zeros((n, 4 * 25), dtype=np.float64)
    pair_defs = [(0, 1), (1, 2), (1, L - 1), (L - 2, L - 1)]
    for r, s in enumerate(seqs):
        idxs = [AA_TO_IDX.get(ch, 0) for ch in s]
        for p, idx_c in enumerate(idxs):
            X_pos[r, p * 25 : (p + 1) * 25] = CHEM_EMB[idx_c] * pw[p]
        for k_p, (p1, p2) in enumerate(pair_defs):
            X_pairs[r, k_p * 25 : (k_p + 1) * 25] = np.outer(PHYS5[idxs[p1]], PHYS5[idxs[p2]]).ravel()
    X_pos /= (np.linalg.norm(X_pos, axis=1, keepdims=True) + 1e-8)
    X_pairs /= (np.linalg.norm(X_pairs, axis=1, keepdims=True) + 1e-8)
    return np.hstack([0.80 * X_pos, 0.20 * X_pairs])

for idx, row in t_pan.iterrows():
    k = row["mhckey"]
    al, plen_s = k.rsplit("-", 1)
    L = int(plen_s)
    i_al = al9_to_idx[al]
    sub_tr = bd2009[bd2009["mhckey"] == k]
    sub_te = blind[blind["mhckey"] == k]
    y_true = (sub_te["meas"].values < 500.0).astype(int)

    pnorms9 = pos_norms_allele[al]
    if L == 9:
        pnormsL = pnorms9
    else:
        pnormsL = np.ones(L)
        pnormsL[:3] = pnorms9[:3]
        pnormsL[-1] = pnorms9[-1]
        pnormsL[-2] = pnorms9[-2]
        pnormsL[3:-2] = np.mean(pnorms9[3:7])

    lamL = np.concatenate([np.repeat(15.0 / (pnormsL ** 1.6), 20), [0.01]])
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

    # Native length-L Nystrom Kernel (with supertype same-length neighbors)
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

    # Pure Chemical/BLOSUM62 + Pairwise Anchor Epistasis Dual Kernel on same-length supertype pool!
    FC_tr = encode_chem_epistasis_len(sub_l_tr["sequence"].tolist(), L, pnormsL)
    FC_te = encode_chem_epistasis_len(sub_te["sequence"].tolist(), L, pnormsL)
    BC_L = FC_tr[lm_L]
    GMMC = BC_L @ BC_L.T
    KMMC = 0.5 * ((GMMC + 0.5) ** 3) + 0.5 * np.exp(1.5 * (GMMC - 1.0))
    UC, SC, _ = np.linalg.svd(KMMC + 1e-5 * np.eye(ML))
    projC = UC * (1.0 / np.sqrt(SC))[None, :]
    KNMC = 0.5 * (((FC_tr @ BC_L.T) + 0.5) ** 3) + 0.5 * np.exp(1.5 * ((FC_tr @ BC_L.T) - 1.0))
    KTEC = 0.5 * (((FC_te @ BC_L.T) + 0.5) ** 3) + 0.5 * np.exp(1.5 * ((FC_te @ BC_L.T) - 1.0))
    ZC_tr = np.hstack([KNMC @ projC, np.ones((len(FC_tr), 1))])
    ZC_te = np.hstack([KTEC @ projC, np.ones((len(FC_te), 1))])
    wzC, _ = solve_censored_mm(ZC_tr, sub_l_tr["y_log"].values, sub_l_tr["inequality"].values, lam_zL, sample_w=sw_L)
    pred_chem_L = -(ZC_te @ wzC)

    # 2. Multi-length Groove Nystrom Kernel + Nonlinear 9-mer projection + Exon-2/Exon-3 split + Model-Space Supertype Ensemble!
    sub_al_all, is_self, nbr_sim_arr, F_L, proj_M, Z_tr, sf_tr = allele_nystrom_cache[al]
    Xb_te, Xs_te, Xt_te, sf_te = get_peptide_groove_features(sub_te["sequence"].tolist(), al)

    def znorm(v):
        return (v - v.mean()) / (v.std() + 1e-8)

    pred_9nl_base = -(0.50 * sf_te[:, 2] + 0.35 * sf_te[:, 3] + 0.15 * sf_te[:, 4])
    pred_exon_split = -sf_te[:, 5]
    pred_wild8 = -(0.60 * sf_te[:, 6] + 0.40 * sf_te[:, 7])
    pred_9nl_proj = -(0.45 * sf_te[:, 2] + 0.30 * sf_te[:, 3] + 0.15 * sf_te[:, 4] + 0.10 * sf_te[:, 5])
    if L == 8:
        pred_9nl_proj = 0.65 * znorm(pred_9nl_proj) + 0.35 * znorm(pred_wild8)

    pred_ms_ens = eval_model_space_supertype_9mer(sub_te["sequence"].tolist(), al)

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

    n_binders_L = int((sub_tr["meas"] < 500.0).sum())
    if L == 9:
        w_native = n_binders_L / (n_binders_L + 35.0)
    else:
        w_native = n_binders_L / (n_binders_L + 85.0)

    pred_native_comb = 0.38 * znorm(pred_lin_L) + 0.62 * znorm(pred_nl_L)
    pred_pan_comb = 0.38 * znorm(pred_groove_krr) + 0.32 * znorm(pred_9nl_proj) + 0.30 * znorm(pred_ms_ens)
    pred_seq_only = w_native * pred_native_comb + (1.0 - w_native * 0.60) * pred_pan_comb
    aucs_seq.append(roc_auc_score(y_true, pred_seq_only))

    # Variant B: Collaborative IRT + Sequence (high-similarity sister alleles in BD2009)
    pred_panel = np.zeros(len(sub_te), dtype=np.float64)
    for i, s in enumerate(sub_te["sequence"]):
        recs = seq_bd_lookup.get(s, [])
        num, den = 0.0, 0.0
        for other_a, sc, other_len in recs:
            if other_a == i_al and other_len == L:
                continue
            sim = S_comb[i_al, other_a]
            if sim > 0.50:
                w = (sim ** 5.0) * (1.0 if other_len == L else 0.7)
                num += w * sc
                den += w
        if den > 0.1:
            pred_panel[i] = num / (den + 1.0)

    pred_full = znorm(pred_seq_only) + 0.20 * pred_panel
    aucs_full.append(roc_auc_score(y_true, pred_full))

    clean_cache[f"{idx}_y"] = y_true
    clean_cache[f"{idx}_lin"] = pred_lin_L
    clean_cache[f"{idx}_nl"] = pred_nl_L
    clean_cache[f"{idx}_chem"] = pred_chem_L
    clean_cache[f"{idx}_groove"] = pred_groove_krr
    clean_cache[f"{idx}_9nl"] = pred_9nl_base
    clean_cache[f"{idx}_exon"] = pred_exon_split
    clean_cache[f"{idx}_wild8"] = pred_wild8
    clean_cache[f"{idx}_ms"] = pred_ms_ens
    clean_cache[f"{idx}_panel"] = pred_panel
    clean_cache[f"{idx}_meta"] = np.array([
        L, len(sub_tr), n_binders_L, len(sub_te),
        float(np.std(X_tr_L @ wL) + 1e-8),
        float(np.std(ZL_tr[:len(idx_l_self)] @ wzL) + 1e-8),
        float(np.std(ZC_tr[:len(idx_l_self)] @ wzC) + 1e-8),
        float(np.std(Z_tr[is_self] @ w_z) + 1e-8),
        float(np.std(0.50 * sf_tr[is_self, 2] + 0.35 * sf_tr[is_self, 3] + 0.15 * sf_tr[is_self, 4]) + 1e-8),
        float(np.std(sf_tr[is_self, 5]) + 1e-8),
    ], dtype=np.float64)

np.savez("./cache_lens2_components_clean.npz", **clean_cache)

aucs_seq = np.array(aucs_seq)
aucs_full = np.array(aucs_full)
ref_net = t_net["blind"].values
ref_pan = t_pan["blind"].values
ref_smm = t_smm["blind"].values

print(f"Done in {time.perf_counter()-t0:.2f}s!")
print(f"87-dataset Pure Sequence Lens-2 Mean Blind AUC: {aucs_seq.mean():.6f} (wins vs NetMHC: {(aucs_seq > ref_net).sum()}/87, vs NetMHCpan: {(aucs_seq > ref_pan).sum()}/87, vs SMM: {(aucs_seq > ref_smm).sum()}/87)")
print(f"87-dataset Full (Seq + BD2009 IRT) Mean Blind AUC: {aucs_full.mean():.6f} (wins vs NetMHC: {(aucs_full > ref_net).sum()}/87, vs NetMHCpan: {(aucs_full > ref_pan).sum()}/87, vs SMM: {(aucs_full > ref_smm).sum()}/87)")
for plen in [8, 9, 10, 11]:
    m = (t_pan["mhckey"].str.endswith(f"-{plen}")).values
    vn = t_net.loc[m, "blind"].mean()
    vp = t_pan.loc[m, "blind"].mean()
    print(f"  Len {plen:2d} (n={m.sum():2d}): SeqOnly={aucs_seq[m].mean():.4f} | Full={aucs_full[m].mean():.4f} | NetMHC={vn:.4f} | NetMHCpan={vp:.4f}")

idx_bl20 = t_pan.sort_values(["size_bl", "mhckey"]).index[:20]
idx_cv20 = t_pan.sort_values(["size_cv", "mhckey"]).index[:20]
print(f"20 smallest by size_bl: SeqOnly={aucs_seq[idx_bl20].mean():.6f} ({aucs_seq[idx_bl20].mean()-ref_net[idx_bl20].mean():+.6f}), Full={aucs_full[idx_bl20].mean():.6f} ({aucs_full[idx_bl20].mean()-ref_net[idx_bl20].mean():+.6f}) vs NetMHC={ref_net[idx_bl20].mean():.6f}, Pan={ref_pan[idx_bl20].mean():.6f}")
print(f"20 smallest by size_cv: SeqOnly={aucs_seq[idx_cv20].mean():.6f} ({aucs_seq[idx_cv20].mean()-ref_net[idx_cv20].mean():+.6f}), Full={aucs_full[idx_cv20].mean():.6f} ({aucs_full[idx_cv20].mean()-ref_net[idx_cv20].mean():+.6f}) vs NetMHC={ref_net[idx_cv20].mean():.6f}, Pan={ref_pan[idx_cv20].mean():.6f}")
