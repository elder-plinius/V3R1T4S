#!/opt/homebrew/bin/python3
import os, sys, time, json, hashlib, subprocess
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import rankdata
from pyteomics import electrochem, mass, parser
from sklearn import ensemble, feature_extraction, preprocessing
from sklearn.metrics import roc_auc_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORK_DIR = BASE_DIR
OUT_SCORES_DIR = os.path.join(WORK_DIR, "clss_tcr_scores")
os.makedirs(OUT_SCORES_DIR, exist_ok=True)

# BLOSUM62 table
AA_LIST = "ACDEFGHIKLMNPQRSTVWY"
AA_TO_IDX = {a: i for i, a in enumerate(AA_LIST)}
ORDER_NCBI = "ARNDCQEGHILKMFPSTWYV"
BLOSUM62_ROWS = {
    'A': [ 4,-1,-2,-2, 0,-1,-1, 0,-2,-1,-1,-1,-1,-2,-1, 1, 0,-3,-2, 0],
    'R': [-1, 5, 0,-2,-3, 1, 0,-2, 0,-3,-2, 2,-1,-3,-2,-1,-1,-3,-2,-3],
    'N': [-2, 0, 6, 1,-3, 0, 0, 0, 1,-3,-3, 0,-2,-3,-2, 1, 0,-4,-2,-3],
    'D': [-2,-2, 1, 6,-3, 0, 2,-1,-1,-3,-4,-1,-3,-3,-1, 0,-1,-4,-3,-3],
    'C': [ 0,-3,-3,-3, 9,-3,-4,-3,-3,-1,-1,-3,-1,-2,-3,-1,-1,-2,-2,-1],
    'Q': [-1, 1, 0, 0,-3, 5, 2,-2, 0,-3,-2, 1, 0,-3,-1, 0,-1,-2,-1,-2],
    'E': [-1, 0, 0, 2,-4, 2, 5,-2, 0,-3,-3, 1,-2,-3,-1, 0,-1,-3,-2,-2],
    'G': [ 0,-2, 0,-1,-3,-2,-2, 6,-2,-4,-4,-2,-3,-3,-2, 0,-2,-2,-3,-3],
    'H': [-2, 0, 1,-1,-3, 0, 0,-2, 8,-3,-3,-1,-2,-1,-2,-1,-2,-2, 2,-3],
    'I': [-1,-3,-3,-3,-1,-3,-3,-4,-3, 4, 2,-3, 1, 0,-3,-2,-1,-3,-1, 3],
    'L': [-1,-2,-3,-4,-1,-2,-3,-4,-3, 2, 4,-2, 2, 0,-3,-2,-1,-2,-1, 1],
    'K': [-1, 2, 0,-1,-3, 1, 1,-2,-1,-3,-2, 5,-1,-3,-1, 0,-1,-3,-2,-2],
    'M': [-1,-1,-2,-3,-1, 0,-2,-3,-2, 1, 2,-1, 5, 0,-2,-1,-1,-1,-1, 1],
    'F': [-2,-3,-3,-3,-2,-3,-3,-3,-1, 0, 0,-3, 0, 6,-4,-2,-2, 1, 3,-1],
    'P': [-1,-2,-2,-1,-3,-1,-1,-2,-2,-3,-3,-1,-2,-4, 7,-1,-1,-4,-3,-2],
    'S': [ 1,-1, 1, 0,-1, 0, 0, 0,-1,-2,-2, 0,-1,-2,-1, 4, 1,-3,-2,-2],
    'T': [ 0,-1, 0,-1,-1,-1,-1,-2,-2,-1,-1,-1,-1,-2,-1, 1, 5,-2,-2, 0],
    'W': [-3,-3,-4,-4,-2,-2,-3,-2,-2,-3,-2,-3,-1, 1,-4,-3,-2,11, 2,-3],
    'Y': [-2,-2,-2,-3,-2,-1,-2,-3, 2,-1,-1,-2,-1, 3,-3,-2,-2, 2, 7,-1],
    'V': [ 0,-3,-3,-3,-1,-2,-2,-3,-3, 3, 1,-2, 1,-1,-2,-2, 0,-3,-1, 4],
}
B62 = np.zeros((20, 20), dtype=np.float32)
for a, row in BLOSUM62_ROWS.items():
    i = AA_TO_IDX[a]
    for b, val in zip(ORDER_NCBI, row):
        j = AA_TO_IDX[b]
        B62[i, j] = val
B62_POS = np.maximum(0.0, B62 + 4.0)
B62_POS_SQRT = np.linalg.cholesky(B62_POS + 0.5 * np.eye(20))

def loop_profile_emb(seqs, max_len=24):
    N = len(seqs)
    flank = min(8, max_len // 2)
    out = np.zeros((N, max_len + 2 * flank, 20), dtype=np.float32)
    mid = max_len // 2
    for idx, s in enumerate(seqs):
        s = str(s)
        L = len(s)
        start = max(0, mid - L // 2)
        for k, ch in enumerate(s):
            pos = start + k
            if 0 <= pos < max_len and ch in AA_TO_IDX:
                out[idx, pos] = B62_POS_SQRT[AA_TO_IDX[ch]]
        for k in range(min(L, flank)):
            ch_n = s[k]
            if ch_n in AA_TO_IDX:
                out[idx, max_len + k] = B62_POS_SQRT[AA_TO_IDX[ch_n]]
            ch_c = s[L - 1 - k]
            if ch_c in AA_TO_IDX:
                out[idx, max_len + flank + k] = B62_POS_SQRT[AA_TO_IDX[ch_c]]
    flat = out.reshape(N, -1)
    norms = np.linalg.norm(flat, axis=1, keepdims=True) + 1e-12
    return flat / norms

def extract_chain_kmer_dicts(df, chain='A'):
    recs = []
    v_col = 'TRAV' if chain == 'A' else 'TRBV'
    j_col = 'TRAJ' if chain == 'A' else 'TRBJ'
    c1_col = 'A1' if chain == 'A' else 'B1'
    c2_col = 'A2' if chain == 'A' else 'B2'
    c3_col = 'TRA_CDR3' if chain == 'A' else 'TRB_CDR3'
    for row in df.itertuples(index=False):
        d = {}
        v_str = str(getattr(row, v_col))
        j_str = str(getattr(row, j_col))
        v_strip = v_str.split('*')[0]
        j_strip = j_str.split('*')[0]
        v_fam = v_strip.split('-')[0]
        j_fam = j_strip.split('-')[0]
        d[f"V_exact={v_str}"] = 1.2
        d[f"V_gene={v_strip}"] = 1.5
        d[f"V_fam={v_fam}"] = 1.0
        d[f"J_exact={j_str}"] = 1.0
        d[f"J_gene={j_strip}"] = 1.2
        d[f"J_fam={j_fam}"] = 0.8
        d[f"VJ={v_strip}+{j_strip}"] = 1.5

        seq = str(getattr(row, c3_col))
        L = len(seq)
        d[f"L={L}"] = 1.2
        d[f"L_bin={L // 2}"] = 0.6
        core = seq[3:-2] if L > 5 else seq
        for k in (1, 2, 3, 4):
            w = 0.6 if k == 1 else (1.0 if k == 2 else (1.4 if k == 3 else 1.2))
            for i in range(L - k + 1):
                km = seq[i:i+k]
                d[f"k{k}_{km}"] = d.get(f"k{k}_{km}", 0.0) + w
        for k in (2, 3):
            for i in range(len(core) - k + 1):
                km = core[i:i+k]
                d[f"core_{km}"] = d.get(f"core_{km}", 0.0) + 1.4
        for gap in (1, 2):
            for i in range(len(core) - gap - 1):
                gkm = f"{core[i]}.{gap}.{core[i+gap+1]}"
                d[f"gap_{gkm}"] = d.get(f"gap_{gkm}", 0.0) + 0.9
        mid = L // 2
        for i, ch in enumerate(seq):
            rel = i - mid
            d[f"p_{rel}_{ch}"] = 1.2
            if i + 1 < L:
                d[f"p2_{rel}_{seq[i:i+2]}"] = 1.2
        for k in range(min(4, L)):
            d[f"N_{k}_{seq[k]}"] = 1.0
            d[f"C_{k}_{seq[L-1-k]}"] = 1.0
        for loop_name, loop_seq in [('c1', str(getattr(row, c1_col))), ('c2', str(getattr(row, c2_col)))]:
            for k in (2, 3):
                for i in range(len(loop_seq) - k + 1):
                    km = loop_seq[i:i+k]
                    d[f"{loop_name}_{km}"] = d.get(f"{loop_name}_{km}", 0.0) + 0.5
        recs.append(d)
    return recs

basicity = {'A': 206.4, 'B': 210.7, 'C': 206.2, 'D': 208.6, 'E': 215.6, 'F': 212.1, 'G': 202.7,
            'H': 223.7, 'I': 210.8, 'K': 221.8, 'L': 209.6, 'M': 213.3, 'N': 212.8, 'P': 214.4,
            'Q': 214.2, 'R': 237.0, 'S': 207.6, 'T': 211.7, 'V': 208.7, 'W': 216.1, 'X': 210.2,
            'Y': 213.1, 'Z': 214.9}
hydrophobicity = {'A': 0.16, 'B': -3.14, 'C': 2.50, 'D': -2.49, 'E': -1.50, 'F': 5.00, 'G': -3.31,
                  'H': -4.63, 'I': 4.41, 'K': -5.00, 'L': 4.76, 'M': 3.23, 'N': -3.79, 'P': -4.92,
                  'Q': -2.76, 'R': -2.77, 'S': -2.85, 'T': -1.08, 'V': 3.02, 'W': 4.88, 'X': 4.59,
                  'Y': 2.00, 'Z': -2.13}
helicity = {'A': 1.24, 'B': 0.92, 'C': 0.79, 'D': 0.89, 'E': 0.85, 'F': 1.26, 'G': 1.15, 'H': 0.97,
            'I': 1.29, 'K': 0.88, 'L': 1.28, 'M': 1.22, 'N': 0.94, 'P': 0.57, 'Q': 0.96, 'R': 0.95,
            'S': 1.00, 'T': 1.09, 'V': 1.27, 'W': 1.07, 'X': 1.29, 'Y': 1.11, 'Z': 0.91}
mutation_stability = {'A': 13, 'C': 52, 'D': 11, 'E': 12, 'F': 32, 'G': 27, 'H': 15, 'I': 10,
                      'K': 24, 'L': 34, 'M':  6, 'N':  6, 'P': 20, 'Q': 10, 'R': 17, 'S': 10,
                      'T': 11, 'V': 17, 'W': 55, 'Y': 31}
physchem_properties = {'basicity': basicity, 'hydrophobicity': hydrophobicity,
                       'helicity': helicity, 'mutation stability': mutation_stability}
aa_pI_cache = {aa: electrochem.pI(aa) for aa in mutation_stability.keys()}
seq_mass_cache, seq_pI_cache = {}, {}
def cached_mass(seq):
    if seq not in seq_mass_cache:
        seq_mass_cache[seq] = mass.fast_mass(seq)
    return seq_mass_cache[seq]
def cached_pI(seq):
    if seq not in seq_pI_cache:
        seq_pI_cache[seq] = electrochem.pI(seq)
    return seq_pI_cache[seq]
def gene_to_family(gene):
    gene_str = str(gene)
    return gene_str if gene_str == 'unresolved' else gene_str.split('-')[0].zfill(2)
def encode_gene(gene):
    gene_str = str(gene)
    return '-'.join(g.zfill(2) for g in gene_str.split('-')) if '-' in gene_str else gene_str
def convert_gene_df(data):
    data = data.copy()
    for gene in [g for g in data.columns.values if g in ['TRBV','TRBJ','TRAV','TRAJ']]:
        data[gene] = data[gene].str.replace(r'\*0\d', '', regex=True).apply(encode_gene)
        data[gene + '_family'] = data[gene].apply(gene_to_family)
    return data

def compute_tcrex_dicts(df, chain='A'):
    v_col = 'TRAV' if chain == 'A' else 'TRBV'
    j_col = 'TRAJ' if chain == 'A' else 'TRBJ'
    vf_col = v_col + '_family'
    jf_col = j_col + '_family'
    c3_col = 'TRA_CDR3' if chain == 'A' else 'TRB_CDR3'
    recs = []
    for row in df.itertuples(index=False):
        seq = str(getattr(row, c3_col))
        L = len(seq)
        d = {
            f"V_gene={getattr(row, v_col)}": 1.0,
            f"J_gene={getattr(row, j_col)}": 1.0,
            f"V_family={getattr(row, vf_col)}": 1.0,
            f"J_family={getattr(row, jf_col)}": 1.0,
            "length": float(L),
            "mass": float(cached_mass(seq)),
            "pI": float(cached_pI(seq)),
        }
        for aa, cnt in parser.amino_acid_composition(seq).items():
            d[f"{aa} count"] = float(cnt)
        for prop_name, prop_lookup in physchem_properties.items():
            d[f"average {prop_name}"] = float(np.mean([prop_lookup[aa] for aa in seq]))
        start_pos = -1 * (L // 2)
        pos_range = list(range(start_pos, start_pos + L)) if L % 2 == 1 else list(range(start_pos, 0)) + list(range(1, start_pos + L + 1))
        for pos, aa in zip(pos_range, seq):
            d[f"pos_{pos}_{aa}"] = 1.0
            d[f"pos_{pos}_basicity"] = float(basicity[aa])
            d[f"pos_{pos}_hydrophobicity"] = float(hydrophobicity[aa])
            d[f"pos_{pos}_helicity"] = float(helicity[aa])
            d[f"pos_{pos}_mutation_stability"] = float(mutation_stability[aa])
            d[f"pos_{pos}_pI"] = float(aa_pI_cache[aa])
        recs.append(d)
    return recs

def build_chain_featurizer(tr_df, chain='A'):
    dv_kmer = feature_extraction.DictVectorizer(sparse=True)
    X_tr = dv_kmer.fit_transform(extract_chain_kmer_dicts(tr_df, chain))
    tr_n = np.sqrt(X_tr.multiply(X_tr).sum(axis=1)).A1 + 1e-12
    c1_col = 'A1' if chain == 'A' else 'B1'
    c2_col = 'A2' if chain == 'A' else 'B2'
    c3_col = 'TRA_CDR3' if chain == 'A' else 'TRB_CDR3'
    emb_tr = np.hstack([
        loop_profile_emb(tr_df[c3_col], 22) * np.sqrt(3.0),
        loop_profile_emb(tr_df[c1_col], 10) * 1.0,
        loop_profile_emb(tr_df[c2_col], 10) * 1.0,
    ])
    emb_tr /= (np.linalg.norm(emb_tr, axis=1, keepdims=True) + 1e-12)
    K_kmer_tr = (X_tr @ X_tr.T).toarray() / np.outer(tr_n, tr_n)
    K_b62_tr = emb_tr @ emb_tr.T
    K_tr = 0.25 * K_kmer_tr + 0.30 * (K_kmer_tr ** 2) + 0.15 * (K_kmer_tr ** 4) + 0.15 * K_b62_tr + 0.15 * (K_b62_tr ** 3)

    def transform_kernel(te_df):
        X_te = dv_kmer.transform(extract_chain_kmer_dicts(te_df, chain))
        te_n = np.sqrt(X_te.multiply(X_te).sum(axis=1)).A1 + 1e-12
        K_kmer_te = (X_te @ X_tr.T).toarray() / np.outer(te_n, tr_n)
        emb_te = np.hstack([
            loop_profile_emb(te_df[c3_col], 22) * np.sqrt(3.0),
            loop_profile_emb(te_df[c1_col], 10) * 1.0,
            loop_profile_emb(te_df[c2_col], 10) * 1.0,
        ])
        emb_te /= (np.linalg.norm(emb_te, axis=1, keepdims=True) + 1e-12)
        K_b62_te = emb_te @ emb_tr.T
        return 0.25 * K_kmer_te + 0.30 * (K_kmer_te ** 2) + 0.15 * (K_kmer_te ** 4) + 0.15 * K_b62_te + 0.15 * (K_b62_te ** 3)

    return K_tr, transform_kernel

pub_micro = pd.read_csv(os.path.join(BASE_DIR, "evaluation/microaucs.csv"), index_col=0)
pub_rank = pd.read_csv(os.path.join(BASE_DIR, "evaluation/epitoperank.csv"), index_col=0)
epitopes = [c for c in pub_micro.columns if c not in ("Unnamed: 1", "_Average", "ab", "cdr", "cluster")]

t0 = time.time()
global_te_raw = pd.read_csv(os.path.join(BASE_DIR, "test_set/testSet_Global.txt"), sep="\t")
global_te_df = convert_gene_df(global_te_raw[global_te_raw["TRB_CDR3"] != "TRB_CDR3"].reset_index(drop=True))
global_rows = []

for ep in epitopes:
    tr_df = convert_gene_df(pd.read_csv(os.path.join(BASE_DIR, f"training_data/{ep}.txt"), sep="\t"))
    te_df = convert_gene_df(pd.read_csv(os.path.join(BASE_DIR, f"test_set/{ep}.txt"), sep="\t"))
    y_tr = (tr_df["Label"].values == 1).astype(int)
    n_tr = len(y_tr)

    K_A_tr, tf_K_A = build_chain_featurizer(tr_df, 'A')
    K_B_tr, tf_K_B = build_chain_featurizer(tr_df, 'B')
    K_AB_tr = 0.40 * K_A_tr + 0.40 * K_B_tr + 0.20 * (K_A_tr * K_B_tr)

    dv_A = feature_extraction.DictVectorizer(sparse=False)
    X_A_tr = dv_A.fit_transform(compute_tcrex_dicts(tr_df, 'A'))
    dv_B = feature_extraction.DictVectorizer(sparse=False)
    X_B_tr = dv_B.fit_transform(compute_tcrex_dicts(tr_df, 'B'))
    X_AB_tr = np.hstack([X_A_tr, X_B_tr])

    # Fit KRR, CSLS-KNN, and RF+ET models on training_data/{ep}.txt
    oof_preds = np.zeros((n_tr, 9), dtype=np.float64)
    krr_alphas, csls_states, tree_models = [], [], []

    pos_m = (y_tr == 1)
    neg_m = (y_tr == 0)
    kp = min(3, pos_m.sum() - 1)
    kn = min(5, neg_m.sum() - 1)
    k_bg = min(10, n_tr - 1)

    for c_idx, K_tr_c in enumerate([K_A_tr, K_B_tr, K_AB_tr]):
        A_inv = np.linalg.inv(K_tr_c + 0.4 * np.eye(n_tr))
        alpha = A_inv @ y_tr
        oof_preds[:, c_idx] = y_tr - alpha / np.diag(A_inv)
        krr_alphas.append(alpha)

        K_sharp_tr = (K_tr_c ** 3).copy()
        np.fill_diagonal(K_sharp_tr, -1.0)
        mu_tr = np.sort(K_sharp_tr, axis=1)[:, -k_bg:].mean(axis=1)
        S_tr = K_sharp_tr - 0.5 * (mu_tr[:, None] + mu_tr[None, :])
        np.fill_diagonal(S_tr, -1e9)
        oof_preds[:, 3 + c_idx] = np.sort(S_tr[:, pos_m], axis=1)[:, -kp:].mean(axis=1) - 0.5 * np.sort(S_tr[:, neg_m], axis=1)[:, -kn:].mean(axis=1)
        csls_states.append((mu_tr, pos_m, neg_m, kp, kn, k_bg))

    for c_idx, X_tr_c in enumerate([X_A_tr, X_B_tr, X_AB_tr]):
        rf = ensemble.RandomForestClassifier(300, random_state=0, class_weight='balanced', oob_score=True, n_jobs=-1)
        et = ensemble.ExtraTreesClassifier(300, random_state=0, class_weight='balanced', bootstrap=True, oob_score=True, n_jobs=-1)
        rf.fit(X_tr_c, y_tr)
        et.fit(X_tr_c, y_tr)
        oof_preds[:, 6 + c_idx] = 0.65 * rf.oob_decision_function_[:, 1] + 0.35 * et.oob_decision_function_[:, 1]
        tree_models.append((rf, et))

    oof_aucs = np.array([roc_auc_score(y_tr, oof_preds[:, j]) for j in range(9)])
    excess = np.maximum(0.0, oof_aucs - 0.52)
    weights = (excess ** 4)
    if weights.sum() == 0:
        weights = np.ones(9)
    weights /= weights.sum()

    # Compute OOF mean & std per expert on training_data/{ep}.txt ONLY (strictly pointwise inductive, no upper-tail clipping)
    oof_means = oof_preds.mean(axis=0)
    oof_stds = oof_preds.std(axis=0) + 1e-12

    def transform_oof_calibrated(mat):
        z = (mat - oof_means[None, :]) / oof_stds[None, :]
        return 0.5 * z + 0.5 * np.tanh(0.6 * z) * 1.7320508

    oof_combined = transform_oof_calibrated(oof_preds) @ weights
    oof_neg_mean = float(oof_combined[y_tr == 0].mean())
    oof_comb_std = float(oof_combined.std() + 1e-12)

    def predict_df(target_df):
        K_A_te = tf_K_A(target_df)
        K_B_te = tf_K_B(target_df)
        K_AB_te = 0.40 * K_A_te + 0.40 * K_B_te + 0.20 * (K_A_te * K_B_te)
        X_A_te = dv_A.transform(compute_tcrex_dicts(target_df, 'A'))
        X_B_te = dv_B.transform(compute_tcrex_dicts(target_df, 'B'))
        X_AB_te = np.hstack([X_A_te, X_B_te])

        preds = np.zeros((len(target_df), 9), dtype=np.float64)
        for c_idx, K_te_c in enumerate([K_A_te, K_B_te, K_AB_te]):
            preds[:, c_idx] = K_te_c @ krr_alphas[c_idx]
            mu_tr, pm, nm, kp_c, kn_c, k_bg_c = csls_states[c_idx]
            K_sharp_te = K_te_c ** 3
            mu_te = np.sort(K_sharp_te, axis=1)[:, -k_bg_c:].mean(axis=1)
            S_te = K_sharp_te - 0.5 * (mu_te[:, None] + mu_tr[None, :])
            preds[:, 3 + c_idx] = np.sort(S_te[:, pm], axis=1)[:, -kp_c:].mean(axis=1) - 0.5 * np.sort(S_te[:, nm], axis=1)[:, -kn_c:].mean(axis=1)
        for c_idx, X_te_c in enumerate([X_A_te, X_B_te, X_AB_te]):
            rf, et = tree_models[c_idx]
            preds[:, 6 + c_idx] = 0.65 * rf.predict_proba(X_te_c)[:, 1] + 0.35 * et.predict_proba(X_te_c)[:, 1]

        raw_s = transform_oof_calibrated(preds) @ weights
        return (raw_s - oof_neg_mean) / oof_comb_std

    # Task 1: per-epitope score (strictly pointwise inductive)
    te_out = te_df[["TRA_CDR3", "TRB_CDR3"]].copy()
    te_out["score"] = predict_df(te_df)
    te_out.to_csv(os.path.join(OUT_SCORES_DIR, f"{ep}.txt"), sep="\t", index=False)

    # Task 2: global test set score for this epitope (identical function!)
    g_out = global_te_df[["TRA_CDR3", "TRB_CDR3"]].copy()
    g_out["epitope"] = ep
    g_out["score"] = predict_df(global_te_df)
    global_rows.append(g_out)

pd.concat(global_rows, ignore_index=True).to_csv(os.path.join(OUT_SCORES_DIR, "testSet_Global.txt"), sep="\t", index=False)
stats_file = os.path.join(WORK_DIR, "clss_tcr_stats.txt")
subprocess.run([sys.executable, os.path.join(BASE_DIR, "evaluation/evaluate.py"), "-i", OUT_SCORES_DIR, "-t", os.path.join(BASE_DIR, "true_set"), "-o", stats_file], check=True, stdout=subprocess.DEVNULL)

st = pd.read_csv(stats_file, sep="\t", index_col=0)
print(f"Finished full Task 1 + Task 2 evaluation in {time.time()-t0:.1f}s!")
print(st)
print(f"\n_Average MicroAUC: {st.loc['_Average', 'MicroAUC']:.6f} vs live max {pub_micro['_Average'].max():.6f} (diff = {st.loc['_Average', 'MicroAUC'] - pub_micro['_Average'].max():+.6f})")
print(f"_Average Rank:     {st.loc['_Average', 'Average Rank']:.6f} vs live best {pub_rank['_Average'].min():.6f} (diff = {st.loc['_Average', 'Average Rank'] - pub_rank['_Average'].min():+.6f})")
