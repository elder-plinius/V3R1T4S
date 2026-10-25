#!/usr/bin/env python3
"""
Official 5-Fold Cross-Validation Optimism Gap Audit (p2: iedb-mhci-cv-blind-optimism-gap-shrink)
AND Controlled BD2013 Temporal Contamination Audit (p3: iedb-mhci-bd2013-leakage-quantification).
Single-thread we* (https://github.com/mizopl/we-star) Law M7 implementation.
"""
import json
import time
import numpy as np
import pandas as pd
from scipy.special import softmax
from sklearn.metrics import roc_auc_score

t0 = time.perf_counter()
BASE = "data/benchmark_mhci_reliability"
bd2009 = pd.read_csv(f"{BASE}/binding/bd2009.1/bdata.2009.mhci.public.1.txt", sep="\t")
cv_rnd = pd.read_csv(f"{BASE}/binding/bd2009.1/bdata.2009.mhci.public.1.cv_rnd.txt", sep="\t")
bd2013 = pd.read_csv(f"{BASE}/binding/bd2013.1/bdata.20130222.mhci.public.1.txt", sep="\t")
blind  = pd.read_csv(f"{BASE}/binding/blind.1/bdata.2013.mhci.public.blind.1.txt", sep="\t")

t_net = pd.read_csv(f"{BASE}/features/table_pred_performance/table.cv_features.updated.auc.netmhc.xls", sep="\t")
t_pan = pd.read_csv(f"{BASE}/features/table_pred_performance/table.cv_features.updated.auc.netmhcpan.xls", sep="\t")
t_smm = pd.read_csv(f"{BASE}/features/table_pred_performance/table.cv_features.updated.auc.smmpmbec_cpp.xls", sep="\t")

for df in (bd2009, cv_rnd, bd2013, blind):
    df["allele"] = df["mhc"].str.replace("*", "-", regex=False).str.replace(":", "", regex=False)
    df["mhckey"] = df["allele"] + "-" + df["peptide_length"].astype(str)
    df["y_log"] = np.log10(np.clip(df["meas"].values, 1.0, 100000.0))

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

def solve_censored_mm(X, y_raw, ineq, lam_vec, w_prior=None, sample_w=None, n_iter=12):
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

def znorm(v):
    return (v - v.mean()) / (v.std() + 1e-8)

# Precompute 9-mer supertype pocket priors on BD2009
lam_unif9 = np.concatenate([np.full(180, 15.0), [0.01]])
w9_init = {}
n9_cnt = {}
pos_norms_allele = {}
for al, grp in bd2009[bd2009["peptide_length"] == 9].groupby("allele"):
    X9 = encode_len(grp["sequence"].tolist(), 9)
    w9, _ = solve_censored_mm(X9, grp["y_log"].values, grp["inequality"].values, lam_unif9)
    w9_init[al] = w9
    n9_cnt[al] = len(grp)
    pnorms = np.linalg.norm(w9[:180].reshape(9, 20), axis=1)
    pos_norms_allele[al] = np.clip(pnorms / (pnorms.mean() + 1e-8), 0.65, 2.2)

alleles_9 = sorted(w9_init.keys())
al9_to_idx = {a: i for i, a in enumerate(alleles_9)}

S_pos = np.zeros((9, len(alleles_9), len(alleles_9)), dtype=np.float64)
for p in range(9):
    Wp = np.array([w9_init[a][p*20:(p+1)*20] - w9_init[a][p*20:(p+1)*20].mean() for a in alleles_9])
    Wp_norm = Wp / (np.linalg.norm(Wp, axis=1, keepdims=True) + 1e-8)
    S_pos[p] = np.clip(Wp_norm @ Wp_norm.T, 0.0, 1.0)

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

w9_allele = {}
w9_sup_prior = {}
for i, al in enumerate(alleles_9):
    w_sup = np.zeros(181, dtype=np.float64)
    for p in range(9):
        sp = (0.60 * S_pos[p, i] + 0.40 * S_comb[i]) ** 3.5
        sp[i] = 0.0
        weights = sp * np.sqrt([n9_cnt[a] for a in alleles_9])
        if weights.sum() > 0:
            w_sup[p*20:(p+1)*20] = np.average([w9_init[a][p*20:(p+1)*20] for a in alleles_9], axis=0, weights=weights)
    w_sup[-1] = np.mean([w9_init[a][-1] for a in alleles_9])
    w9_sup_prior[al] = w_sup

    pnorms = pos_norms_allele[al]
    lam_vec = np.concatenate([np.repeat(16.0 / (pnorms ** 1.6), 20), [0.01]])
    grp = bd2009[(bd2009["allele"] == al) & (bd2009["peptide_length"] == 9)]
    X9 = encode_len(grp["sequence"].tolist(), 9)
    w9, _ = solve_censored_mm(X9, grp["y_log"].values, grp["inequality"].values, lam_vec, w_prior=w_sup)
    w9_allele[al] = w9

# ==============================================================================
# PART 1: p2 — 5-Fold Cross-Validation Optimism Gap Audit on cv_rnd
# ==============================================================================
# Why does NetMHCpan suffer a +0.034553 (0.917601 vs 0.883048) optimism gap between
# cv_rnd and blind? Because random 5-fold CV splits each dataset independently while
# leaving identical/homologous peptides on sister alleles unmasked in the pan-allele
# training pool, AND uses low ridge regularization that memorizes within-assay series.
# Under our Cross-Allele Peptide-Group De-Leaked 5-fold CV protocol (where fold k holds
# out all peptides in fold k across sister alleles too, and uses de-confounded supertype
# regularization), we compute the exact 5-fold out-of-fold AUC across all 87 datasets!
rng = np.random.default_rng(42)
cv_aucs_debiased = []
cv_aucs_standard = []

for idx, row in t_pan.iterrows():
    k = row["mhckey"]
    al, plen_s = k.rsplit("-", 1)
    L = int(plen_s)
    i_al = al9_to_idx[al]
    sub_cv = cv_rnd[cv_rnd["mhckey"] == k].reset_index(drop=True)
    y_true_cv = (sub_cv["meas"].values < 500.0).astype(int)
    folds = sub_cv["cv"].values

    pnorms9 = pos_norms_allele[al]
    if L == 9:
        pnormsL = pnorms9
    else:
        pnormsL = np.ones(L)
        pnormsL[:3] = pnorms9[:3]
        pnormsL[-1] = pnorms9[-1]
        pnormsL[-2] = pnorms9[-2]
        pnormsL[3:-2] = np.mean(pnorms9[3:7])

    lamL = np.concatenate([np.repeat(18.0 / (pnormsL ** 1.6), 20), [0.01]])
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

    X_all = encode_len(sub_cv["sequence"].tolist(), L)
    pwL = np.repeat(np.sqrt(pnormsL), 20)
    F_all = X_all[:, :-1] * pwL[None, :]
    F_all = F_all / (np.linalg.norm(F_all, axis=1, keepdims=True) + 1e-8)

    # Same-length neighbor pool in BD2009 (excluding target allele)
    sub_nbr_all = bd2009[(bd2009["peptide_length"] == L) & (bd2009["allele"] != al)].reset_index(drop=True)
    sims_n = sub_nbr_all["allele"].map(lambda x: S_comb[i_al, al9_to_idx[x]] if x in al9_to_idx else 0.0).values
    idx_n = np.where(sims_n > 0.62)[0]
    if len(idx_n) > 1000:
        idx_n = idx_n[np.argsort(-sims_n[idx_n], kind="mergesort")[:1000]]
    sub_nbr = sub_nbr_all.iloc[idx_n].reset_index(drop=True)
    sims_nbr = sims_n[idx_n]
    X_nbr = encode_len(sub_nbr["sequence"].tolist(), L)
    F_nbr = X_nbr[:, :-1] * pwL[None, :]
    F_nbr = F_nbr / (np.linalg.norm(F_nbr, axis=1, keepdims=True) + 1e-8)
    nbr_seqs = sub_nbr["sequence"].values

    oof_debiased = np.zeros(len(sub_cv), dtype=np.float64)
    oof_standard = np.zeros(len(sub_cv), dtype=np.float64)

    for f_id in range(5):
        te_mask = (folds == f_id)
        tr_mask = ~te_mask
        if te_mask.sum() == 0:
            continue
        te_seqs_set = set(sub_cv.loc[te_mask, "sequence"].tolist())
        # De-leaked neighbor mask: exclude any sister-allele row whose sequence is in the held-out fold!
        nbr_keep = np.array([s not in te_seqs_set for s in nbr_seqs], dtype=bool)

        # 1. De-biased OOF linear + kernel prediction (generalization-matched regularization)
        w_lin, _ = solve_censored_mm(
            X_all[tr_mask], sub_cv.loc[tr_mask, "y_log"].values, sub_cv.loc[tr_mask, "inequality"].values,
            lamL * 1.35, w_prior=w_prior
        )
        p_lin = -(X_all[te_mask] @ w_lin)

        F_tr_fold = np.vstack([F_all[tr_mask], F_nbr[nbr_keep]])
        y_tr_fold = np.concatenate([sub_cv.loc[tr_mask, "y_log"].values, sub_nbr.loc[nbr_keep, "y_log"].values])
        in_tr_fold = np.concatenate([sub_cv.loc[tr_mask, "inequality"].values, sub_nbr.loc[nbr_keep, "inequality"].values])
        sw_fold = np.ones(len(F_tr_fold), dtype=np.float64)
        n_self_tr = int(tr_mask.sum())
        if nbr_keep.sum() > 0:
            base_w = 0.45 * (600.0 / (n_self_tr + 600.0)) + 0.15
            sw_fold[n_self_tr:] = base_w * (sims_nbr[nbr_keep] ** 3.5)

        M_f = min(400, len(F_tr_fold))
        lm_f = np.linspace(0, len(F_tr_fold) - 1, M_f, dtype=int)
        B_f = F_tr_fold[lm_f]
        G_mm = B_f @ B_f.T
        K_mm = 0.5 * ((G_mm + 0.5) ** 3) + 0.5 * np.exp(1.5 * (G_mm - 1.0))
        Uf, Sf, _ = np.linalg.svd(K_mm + 1e-5 * np.eye(M_f))
        proj_f = Uf * (1.0 / np.sqrt(Sf))[None, :]
        K_nm = 0.5 * (((F_tr_fold @ B_f.T) + 0.5) ** 3) + 0.5 * np.exp(1.5 * ((F_tr_fold @ B_f.T) - 1.0))
        K_te = 0.5 * (((F_all[te_mask] @ B_f.T) + 0.5) ** 3) + 0.5 * np.exp(1.5 * ((F_all[te_mask] @ B_f.T) - 1.0))
        Z_tr_f = np.hstack([K_nm @ proj_f, np.ones((len(F_tr_fold), 1))])
        Z_te_f = np.hstack([K_te @ proj_f, np.ones((int(te_mask.sum()), 1))])

        lam_zf = np.full(Z_tr_f.shape[1], 1.65); lam_zf[-1] = 0.01
        w_zf, _ = solve_censored_mm(Z_tr_f, y_tr_fold, in_tr_fold, lam_zf, sample_w=sw_fold)
        p_nl = -(Z_te_f @ w_zf)
        oof_debiased[te_mask] = 0.42 * znorm(p_lin) + 0.58 * znorm(p_nl)

        # Also evaluate un-masked standard CV (without sister-allele sequence masking and with tighter lambda)
        F_tr_std = np.vstack([F_all[tr_mask], F_nbr])
        y_tr_std = np.concatenate([sub_cv.loc[tr_mask, "y_log"].values, sub_nbr["y_log"].values])
        in_tr_std = np.concatenate([sub_cv.loc[tr_mask, "inequality"].values, sub_nbr["inequality"].values])
        sw_std = np.ones(len(F_tr_std), dtype=np.float64)
        if len(F_nbr) > 0:
            sw_std[n_self_tr:] = 0.45 * (sims_nbr ** 3.5)
        K_nm_s = 0.5 * (((F_tr_std @ B_f.T) + 0.5) ** 3) + 0.5 * np.exp(1.5 * ((F_tr_std @ B_f.T) - 1.0))
        Z_tr_s = np.hstack([K_nm_s @ proj_f, np.ones((len(F_tr_std), 1))])
        lam_zs = np.full(Z_tr_s.shape[1], 0.95); lam_zs[-1] = 0.01
        w_zs, _ = solve_censored_mm(Z_tr_s, y_tr_std, in_tr_std, lam_zs, sample_w=sw_std)
        p_nl_s = -(Z_te_f @ w_zs)
        oof_standard[te_mask] = 0.35 * znorm(p_lin) + 0.65 * znorm(p_nl_s)

    cv_aucs_debiased.append(float(roc_auc_score(y_true_cv, oof_debiased)))
    cv_aucs_standard.append(float(roc_auc_score(y_true_cv, oof_standard)))

cv_aucs_debiased = np.array(cv_aucs_debiased)
cv_aucs_standard = np.array(cv_aucs_standard)
print(f"Computed 87-dataset 5-fold cv_rnd in {time.perf_counter()-t0:.2f}s:")
print(f"  De-leaked Cross-Allele Group OOF Mean cv_rnd AUC : {cv_aucs_debiased.mean():.6f}")
print(f"  Standard Un-masked OOF Mean cv_rnd AUC           : {cv_aucs_standard.mean():.6f}")
print(f"  Reference NetMHCpan cv_rnd={t_pan['cv_rnd'].mean():.6f}, blind={t_pan['blind'].mean():.6f}, gap={t_pan['cv_rnd'].mean()-t_pan['blind'].mean():.6f}")
print(f"  Reference NetMHC    cv_rnd={t_net['cv_rnd'].mean():.6f}, blind={t_net['blind'].mean():.6f}, gap={t_net['cv_rnd'].mean()-t_net['blind'].mean():.6f}")
print(f"  Reference SMM-PMBEC cv_rnd={t_smm['cv_rnd'].mean():.6f}, blind={t_smm['blind'].mean():.6f}, gap={t_smm['cv_rnd'].mean()-t_smm['blind'].mean():.6f}")

# ==============================================================================
# PART 2: p3 — BD2013 Temporal Contamination Leakage Audit Curve
# ==============================================================================
# We quantify how much apparent Blind AUC a predictor gains when post-2009 IEDB
# measurements (BD2013 / post-2009 corpus) leak into training vs strict BD2009 training.
# Notice:
#   - In bdata.20130222.mhci.public.1.txt, there are 42,038 post-2009 rows not in BD2009.
#   - Furthermore, post-2013 tools trained on the complete 2013 IEDB release (or post-2013
#     dumps used by MHCflurry 2.0, NetMHCpan-3.0/4.0, BigMHC, TransPHLA) include both
#     cross-allele sister measurements AND direct post-2009 measurements!
# We evaluate the EXACT SAME architecture across contamination fractions
# f in [0.00, 0.10, 0.25, 0.50, 0.75, 1.00] under:
#   Regime A (Cross-Allele Post-2009 Leakage Only: 0% target-allele blind rows leaked,
#             only sister-allele post-2009 rows from BD2013 + Blind added to training)
#   Regime B (Full Post-2009 Corpus Leakage: fraction f of post-2009 rows randomly
#             included in the training set, mimicking post-2013 pretrained models).

l1 = np.load("./cache_lens1_components_clean.npz")
l2 = np.load("./cache_lens2_components_clean.npz")

# Build post-2009 cross-allele lookup & direct post-2009 lookup
bd2009_pairs = set(zip(bd2009["mhckey"], bd2009["sequence"]))
post2009_all = pd.concat([bd2013, blind], ignore_index=True).drop_duplicates(subset=["mhckey", "sequence"])
mask_new = [((mk, sq) not in bd2009_pairs) for mk, sq in zip(post2009_all["mhckey"], post2009_all["sequence"])]
post2009_delta = post2009_all[mask_new].reset_index(drop=True)

print(f"Post-2009 Delta Corpus (BD2013 U Blind \\ BD2009): {len(post2009_delta)} unique (mhckey, sequence) measurements")

fracs = [0.00, 0.10, 0.25, 0.50, 0.75, 1.00]
p3_curve_cross_allele = {}
p3_curve_full_post2013 = {}

# Precompute clean f=0.00 baseline score per dataset (Adaptive Scarcity Lens 1 + Lens 2)
clean_seq_scores = {}
clean_full_scores = {}
for i in range(87):
    meta = l2[f"{i}_meta"]
    L, n_tr, n_bind, n_te = meta[:4]
    scarcity = 500.0 / (n_tr + 500.0)
    lin = (1.0 - 0.65 * scarcity) * znorm(l1[f"{i}_lin"]) + (0.65 * scarcity) * znorm(l2[f"{i}_lin"])
    nl  = (1.0 - 0.65 * scarcity) * znorm(l1[f"{i}_nl"])  + (0.65 * scarcity) * znorm(l2[f"{i}_nl"])
    gr  = (1.0 - 0.65 * scarcity) * znorm(l1[f"{i}_groove"]) + (0.65 * scarcity) * znorm(l2[f"{i}_groove"])
    p9  = (1.0 - 0.65 * scarcity) * znorm(l1[f"{i}_9nl"]) + (0.65 * scarcity) * (0.85 * znorm(l2[f"{i}_9nl"]) + 0.15 * znorm(l2[f"{i}_exon"]))
    chem2 = znorm(l2[f"{i}_chem"])
    ms2   = znorm(l2[f"{i}_ms"])

    w_native = n_bind / (n_bind + (35.0 if L == 9 else 85.0))
    w_chem_eff = 0.16 * scarcity
    pred_native = (0.38 * (1.0 - w_chem_eff)) * lin + (0.62 * (1.0 - w_chem_eff)) * nl + w_chem_eff * chem2
    w_ms = 0.35 * scarcity if L in (9, 10) else (0.15 * 0.35 * scarcity)
    pred_pan = (0.50 * (1.0 - w_ms)) * gr + (0.50 * (1.0 - w_ms)) * p9 + w_ms * ms2
    pred_seq = w_native * pred_native + (1.0 - w_native * 0.60) * pred_pan
    clean_seq_scores[i] = pred_seq
    panel = 0.55 * l1[f"{i}_panel"] + 0.45 * l2[f"{i}_panel"]
    clean_full_scores[i] = znorm(pred_seq) + 0.22 * panel

for f in fracs:
    rng_f = np.random.default_rng(2026 + int(f * 100))
    if f == 0.0:
        sub_leak = post2009_delta.iloc[:0]
    elif f == 1.0:
        sub_leak = post2009_delta
    else:
        n_pick = int(round(f * len(post2009_delta)))
        idx_pick = rng_f.choice(len(post2009_delta), size=n_pick, replace=False)
        sub_leak = post2009_delta.iloc[idx_pick]

    # Build leaked lookup table
    leak_lookup = {}
    for s, al, ylog, ineq, plen in zip(sub_leak["sequence"], sub_leak["allele"], sub_leak["y_log"], sub_leak["inequality"], sub_leak["peptide_length"]):
        if al not in al9_to_idx:
            continue
        score = 2.69897 - ylog
        if ineq == ">" and ylog >= 2.69897:
            score = min(score, -1.0)
        leak_lookup.setdefault(s, []).append((al9_to_idx[al], score, int(plen)))

    aucs_cross = []
    aucs_direct = []
    for idx, row in t_pan.iterrows():
        k = row["mhckey"]
        al, plen_s = k.rsplit("-", 1)
        L = int(plen_s)
        i_al = al9_to_idx[al]
        sub_te = blind[blind["mhckey"] == k]
        y_true = l1[f"{idx}_y"]
        base_sc = znorm(clean_full_scores[idx])

        if f == 0.0:
            aucs_cross.append(float(roc_auc_score(y_true, base_sc)))
            aucs_direct.append(float(roc_auc_score(y_true, base_sc)))
            continue

        # Regime A: Cross-allele post-2009 sister leakage only (other_a != i_al)
        cross_adj = np.zeros(len(sub_te), dtype=np.float64)
        # Regime B: Full post-2009 corpus leakage (including direct target-allele training rows when leaked)
        direct_adj = np.zeros(len(sub_te), dtype=np.float64)

        # Also refit target-allele linear + kernel with leaked target-allele rows for Regime B
        sub_tr_orig = bd2009[bd2009["mhckey"] == k]
        sub_tr_leak_self = sub_leak[sub_leak["mhckey"] == k]
        if len(sub_tr_leak_self) > 0:
            sub_tr_comb = pd.concat([sub_tr_orig, sub_tr_leak_self], ignore_index=True)
            pnorms9 = pos_norms_allele[al]
            pnormsL = pnorms9 if L == 9 else np.concatenate([pnorms9[:3], np.full(L-5, np.mean(pnorms9[3:7])), pnorms9[-2:]])
            lamL = np.concatenate([np.repeat(12.0 / (pnormsL ** 1.6), 20), [0.01]])
            X_tr_c = encode_len(sub_tr_comb["sequence"].tolist(), L)
            X_te_c = encode_len(sub_te["sequence"].tolist(), L)
            w_c, _ = solve_censored_mm(X_tr_c, sub_tr_comb["y_log"].values, sub_tr_comb["inequality"].values, lamL)
            p_lin_leak = znorm(-(X_te_c @ w_c))
        else:
            p_lin_leak = base_sc

        for i_s, s in enumerate(sub_te["sequence"]):
            recs = leak_lookup.get(s, [])
            if not recs:
                continue
            num_c, den_c = 0.0, 0.0
            num_d, den_d = 0.0, 0.0
            for other_a, sc, other_len in recs:
                if other_a == i_al and other_len == L:
                    num_d += 4.0 * sc
                    den_d += 4.0
                else:
                    sim = S_comb[i_al, other_a]
                    if sim > 0.45:
                        w = (sim ** 4.0) * (1.0 if other_len == L else 0.7)
                        num_c += w * sc
                        den_c += w
                        num_d += w * sc
                        den_d += w
            if den_c > 0.05:
                cross_adj[i_s] = num_c / (den_c + 1.0)
            if den_d > 0.05:
                direct_adj[i_s] = num_d / (den_d + 0.5)

        pred_cross = base_sc + 0.25 * cross_adj
        pred_direct = 0.75 * base_sc + 0.25 * p_lin_leak + 0.85 * direct_adj
        aucs_cross.append(float(roc_auc_score(y_true, pred_cross)))
        aucs_direct.append(float(roc_auc_score(y_true, pred_direct)))

    p3_curve_cross_allele[f"{f:.2f}"] = {
        "mean_blind_auc": float(np.mean(aucs_cross)),
        "delta_vs_clean": float(np.mean(aucs_cross) - np.mean(p3_curve_cross_allele["0.00"]["per_dataset"] if "0.00" in p3_curve_cross_allele else aucs_cross)),
        "wins_vs_netmhc": int((np.array(aucs_cross) > t_net["blind"].values).sum()),
        "wins_vs_netmhcpan": int((np.array(aucs_cross) > t_pan["blind"].values).sum()),
        "per_dataset": aucs_cross,
    }
    p3_curve_full_post2013[f"{f:.2f}"] = {
        "mean_blind_auc": float(np.mean(aucs_direct)),
        "delta_vs_clean": float(np.mean(aucs_direct) - np.mean(p3_curve_full_post2013["0.00"]["per_dataset"] if "0.00" in p3_curve_full_post2013 else aucs_direct)),
        "wins_vs_netmhc": int((np.array(aucs_direct) > t_net["blind"].values).sum()),
        "wins_vs_netmhcpan": int((np.array(aucs_direct) > t_pan["blind"].values).sum()),
        "per_dataset": aucs_direct,
    }
    print(f"  Leakage f={f:4.2f} | Cross-Allele Post-2009 Only: {np.mean(aucs_cross):.6f} ({p3_curve_cross_allele[f'{f:.2f}']['delta_vs_clean']:+.6f}) | Full Post-2013 Corpus: {np.mean(aucs_direct):.6f} ({p3_curve_full_post2013[f'{f:.2f}']['delta_vs_clean']:+.6f}, wins={p3_curve_full_post2013[f'{f:.2f}']['wins_vs_netmhc']}/87)")

out_json = {
    "p2_cv_blind_optimism_gap": {
        "cv_rnd_mean_debiased": float(cv_aucs_debiased.mean()),
        "cv_rnd_mean_standard": float(cv_aucs_standard.mean()),
        "cv_rnd_per_dataset_debiased": cv_aucs_debiased.tolist(),
        "cv_rnd_per_dataset_standard": cv_aucs_standard.tolist(),
        "references": {
            "NetMHCpan_updated_table": {
                "cv_rnd": float(t_pan["cv_rnd"].mean()),
                "blind": float(t_pan["blind"].mean()),
                "gap": float(t_pan["cv_rnd"].mean() - t_pan["blind"].mean()),
            },
            "NetMHCpan_paper_text": {
                "cv_rnd": 0.9150,
                "blind": 0.8833,
                "gap": 0.0317,
            },
            "NetMHC_updated_table": {
                "cv_rnd": float(t_net["cv_rnd"].mean()),
                "blind": float(t_net["blind"].mean()),
                "gap": float(t_net["cv_rnd"].mean() - t_net["blind"].mean()),
            },
            "SMM_PMBEC_updated_table": {
                "cv_rnd": float(t_smm["cv_rnd"].mean()),
                "blind": float(t_smm["blind"].mean()),
                "gap": float(t_smm["cv_rnd"].mean() - t_smm["blind"].mean()),
            },
        },
    },
    "p3_bd2013_leakage_quantification": {
        "post2009_delta_unique_measurements": int(len(post2009_delta)),
        "regime_a_cross_allele_only": p3_curve_cross_allele,
        "regime_b_full_post2013_corpus": p3_curve_full_post2013,
    },
}

with open("./cache_p2_p3_audit_results.json", "w") as f_out:
    json.dump(out_json, f_out, indent=2)
print(f"Saved ./cache_p2_p3_audit_results.json in {time.perf_counter()-t0:.2f}s!")
