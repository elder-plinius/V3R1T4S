import os
os.environ.setdefault("NUMBA_THREADING_LAYER", "workqueue")

import time
import numpy as np
import numba as nb
from scipy.stats import pearsonr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from tdc.benchmark_group import dti_dg_group

POPCNT_U8 = np.array([bin(i).count('1') for i in range(256)], dtype=np.int32)

# BLOSUM-like 6-letter reduced alphabet for remote homology k-mers:
# A: PAGST (small/polar), B: DENQ (acidic/amide), C: KRH (basic), D: ILMV (aliphatic), E: FYW (aromatic), F: C
REDUCED_MAP = {
    'P':'A', 'A':'A', 'G':'A', 'S':'A', 'T':'A',
    'D':'B', 'E':'B', 'N':'B', 'Q':'B',
    'K':'C', 'R':'C', 'H':'C',
    'I':'D', 'L':'D', 'M':'D', 'V':'D',
    'F':'E', 'Y':'E', 'W':'E',
    'C':'F'
}

def reduce_seq(seq):
    return "".join(REDUCED_MAP.get(c, 'A') for c in seq)

@nb.njit(parallel=True, fastmath=True, cache=True)
def sw_banded_similarity(seqs_bytes, seq_lens, top_candidates, band=64):
    """
    Fast banded local/global alignment score normalized by min/sqrt length
    for top candidate target pairs.
    """
    n_prot = len(seq_lens)
    k_cand = top_candidates.shape[1]
    out_scores = np.zeros((n_prot, k_cand), dtype=np.float32)
    for i in nb.prange(n_prot):
        li = seq_lens[i]
        if li == 0:
            continue
        seq_i = seqs_bytes[i, :li]
        for c_idx in range(k_cand):
            j = top_candidates[i, c_idx]
            if j < 0:
                continue
            if i == j:
                out_scores[i, c_idx] = 1.0
                continue
            lj = seq_lens[j]
            if lj == 0:
                continue
            seq_j = seqs_bytes[j, :lj]
            # If lengths differ hugely, use k-mer window match density
            # Compute fast diagonal seed match score (best offset + banded DP)
            # Banded Smith-Waterman around best diagonal offset
            # First find best diagonal offset via 4-mer hashes
            H_prev = np.zeros(lj + 1, dtype=np.int16)
            H_curr = np.zeros(lj + 1, dtype=np.int16)
            max_sc = 0
            # Downsample very long sequences > 1200 to keep SW super fast
            step_i = 1 if li <= 1200 else 2
            step_j = 1 if lj <= 1200 else 2
            eff_li = (li + step_i - 1) // step_i
            eff_lj = (lj + step_j - 1) // step_j
            for ii in range(eff_li):
                ci = seq_i[ii * step_i]
                # Banded range around proportional diagonal
                center_j = (ii * eff_lj) // max(eff_li, 1)
                j_start = max(0, center_j - band)
                j_end = min(eff_lj, center_j + band)
                for jj in range(j_start, j_end):
                    cj = seq_j[jj * step_j]
                    match = 3 if ci == cj else -1
                    v1 = H_prev[jj] + match
                    v2 = H_prev[jj + 1] - 2
                    v3 = H_curr[jj] - 2
                    val = v1
                    if v2 > val:
                        val = v2
                    if v3 > val:
                        val = v3
                    if val < 0:
                        val = 0
                    H_curr[jj + 1] = val
                    if val > max_sc:
                        max_sc = val
                for jj in range(j_start, j_end + 1):
                    H_prev[jj] = H_curr[jj]
                    H_curr[jj] = 0
            denom = 3.0 * np.sqrt(float(eff_li * eff_lj))
            out_scores[i, c_idx] = float(max_sc) / max(denom, 1.0)
    return out_scores


def build_protein_similarity_matrix(unique_proteins):
    t0 = time.time()
    p_list = [str(s) for s in unique_proteins]
    red_list = [reduce_seq(s) for s in p_list]

    # 1. Exact 3-mer, 4-mer, 5-mer TF-IDF cosine similarity
    v3 = TfidfVectorizer(analyzer='char', ngram_range=(3, 3), sublinear_tf=True)
    X3 = normalize(v3.fit_transform(p_list))
    S3 = (X3 @ X3.T).toarray().astype(np.float32)

    v4 = TfidfVectorizer(analyzer='char', ngram_range=(4, 4), sublinear_tf=True)
    X4 = normalize(v4.fit_transform(p_list))
    S4 = (X4 @ X4.T).toarray().astype(np.float32)

    v5 = TfidfVectorizer(analyzer='char', ngram_range=(5, 5), sublinear_tf=True)
    X5 = normalize(v5.fit_transform(p_list))
    S5 = (X5 @ X5.T).toarray().astype(np.float32)

    # 2. Reduced-alphabet (BLOSUM6) 4-mer & 5-mer TF-IDF cosine similarity for remote homology
    vr = TfidfVectorizer(analyzer='char', ngram_range=(4, 5), sublinear_tf=True)
    Xr = normalize(vr.fit_transform(red_list))
    Sr = (Xr @ Xr.T).toarray().astype(np.float32)

    S_kmer = 0.30 * S3 + 0.30 * S4 + 0.20 * S5 + 0.20 * Sr

    # 3. Banded Smith-Waterman on top 40 candidates per protein
    n_p = len(p_list)
    max_len = max(len(s) for s in p_list)
    seqs_bytes = np.zeros((n_p, max_len), dtype=np.uint8)
    seq_lens = np.zeros(n_p, dtype=np.int32)
    for i, s in enumerate(p_list):
        b = s.encode('ascii', errors='ignore')
        seq_lens[i] = len(b)
        seqs_bytes[i, :len(b)] = np.frombuffer(b, dtype=np.uint8)

    k_top = min(40, n_p)
    top_cands = np.argsort(-S_kmer, axis=1)[:, :k_top].astype(np.int32)
    sw_scores = sw_banded_similarity(seqs_bytes, seq_lens, top_cands, band=80)

    S_sw = np.zeros((n_p, n_p), dtype=np.float32)
    for i in range(n_p):
        for c_idx in range(k_top):
            j = top_cands[i, c_idx]
            S_sw[i, j] = sw_scores[i, c_idx]
    S_sw = 0.5 * (S_sw + S_sw.T)

    S_comb = 0.65 * S_kmer + 0.35 * S_sw
    np.fill_diagonal(S_comb, 1.0)
    print(f"Built 477x477 protein homology matrix in {time.time()-t0:.2f}s")
    return S_comb, S_kmer, S_sw


@nb.njit(fastmath=True, cache=True)
def popcnt_buf(arr_u8, n_rows, n_bytes):
    out = np.empty(n_rows, dtype=np.float32)
    for i in range(n_rows):
        c = 0
        for b in range(n_bytes):
            c += POPCNT_U8[arr_u8[i, b]]
        out[i] = float(c)
    return out


@nb.njit(parallel=True, fastmath=True, cache=True)
def multiview_tanimoto_sym(u8_1, p1, u8_2, p2, u8_3, p3, u8_4, p4, w1, w2, w3, w4):
    """
    Computes weighted multi-view Tanimoto similarity matrix S and S^2 for m molecules.
    """
    m = u8_1.shape[0]
    b1 = u8_1.shape[1]
    b2 = u8_2.shape[1]
    b3 = u8_3.shape[1]
    b4 = u8_4.shape[1]
    K1 = np.empty((m, m), dtype=np.float32)
    K2 = np.empty((m, m), dtype=np.float32)
    for i in nb.prange(m):
        K1[i, i] = 1.0
        K2[i, i] = 1.0
        for j in range(i + 1, m):
            c1 = 0
            for b in range(b1):
                c1 += POPCNT_U8[u8_1[i, b] & u8_1[j, b]]
            d1 = p1[i] + p1[j] - c1
            s1 = c1 / d1 if d1 > 0 else 0.0

            c2 = 0
            for b in range(b2):
                c2 += POPCNT_U8[u8_2[i, b] & u8_2[j, b]]
            d2 = p2[i] + p2[j] - c2
            s2 = c2 / d2 if d2 > 0 else 0.0

            c3 = 0
            for b in range(b3):
                c3 += POPCNT_U8[u8_3[i, b] & u8_3[j, b]]
            d3 = p3[i] + p3[j] - c3
            s3 = c3 / d3 if d3 > 0 else 0.0

            c4 = 0
            for b in range(b4):
                c4 += POPCNT_U8[u8_4[i, b] & u8_4[j, b]]
            d4 = p4[i] + p4[j] - c4
            s4 = c4 / d4 if d4 > 0 else 0.0

            s = w1 * s1 + w2 * s2 + w3 * s3 + w4 * s4
            s_sq = w1 * (s1 * s1) + w2 * (s2 * s2) + w3 * (s3 * s3) + w4 * (s4 * s4)
            K1[i, j] = s
            K1[j, i] = s
            K2[i, j] = s_sq
            K2[j, i] = s_sq
    return K1, K2


@nb.njit(parallel=True, fastmath=True, cache=True)
def multiview_tanimoto_cross(
    q_u8_1, q_p1, q_u8_2, q_p2, q_u8_3, q_p3, q_u8_4, q_p4,
    r_u8_1, r_p1, r_u8_2, r_p2, r_u8_3, r_p3, r_u8_4, r_p4,
    w1, w2, w3, w4
):
    nq = q_u8_1.shape[0]
    nr = r_u8_1.shape[0]
    b1 = q_u8_1.shape[1]
    b2 = q_u8_2.shape[1]
    b3 = q_u8_3.shape[1]
    b4 = q_u8_4.shape[1]
    K1 = np.empty((nq, nr), dtype=np.float32)
    K2 = np.empty((nq, nr), dtype=np.float32)
    max_s1 = np.zeros(nq, dtype=np.float32)
    for i in nb.prange(nq):
        ms = 0.0
        for j in range(nr):
            c1 = 0
            for b in range(b1):
                c1 += POPCNT_U8[q_u8_1[i, b] & r_u8_1[j, b]]
            d1 = q_p1[i] + r_p1[j] - c1
            s1 = c1 / d1 if d1 > 0 else 0.0
            if s1 > ms:
                ms = s1

            c2 = 0
            for b in range(b2):
                c2 += POPCNT_U8[q_u8_2[i, b] & r_u8_2[j, b]]
            d2 = q_p2[i] + r_p2[j] - c2
            s2 = c2 / d2 if d2 > 0 else 0.0

            c3 = 0
            for b in range(b3):
                c3 += POPCNT_U8[q_u8_3[i, b] & r_u8_3[j, b]]
            d3 = q_p3[i] + r_p3[j] - c3
            s3 = c3 / d3 if d3 > 0 else 0.0

            c4 = 0
            for b in range(b4):
                c4 += POPCNT_U8[q_u8_4[i, b] & r_u8_4[j, b]]
            d4 = q_p4[i] + r_p4[j] - c4
            s4 = c4 / d4 if d4 > 0 else 0.0

            s = w1 * s1 + w2 * s2 + w3 * s3 + w4 * s4
            s_sq = w1 * (s1 * s1) + w2 * (s2 * s2) + w3 * (s3 * s3) + w4 * (s4 * s4)
            K1[i, j] = s
            K2[i, j] = s_sq
        max_s1[i] = ms
    return K1, K2, max_s1


def fit_target_tkrr_bank(
    tr_d, tr_p, tr_y, tr_yr,
    u8_1, p1, u8_2, p2, u8_3, p3, u8_4, p4,
    n_targets, global_mean,
    w=(0.45, 0.20, 0.25, 0.10),
    lam1=0.25, lam2=0.12
):
    """
    Fits a bank of Multi-View Tanimoto Kernel Ridge Regression models for every
    target t present in the training set.
    Stores dual weights alpha and Cholesky factor L so any query molecule can be
    evaluated on EITHER its own target t OR its top homologous targets t'!
    """
    order = np.argsort(tr_p, kind='mergesort')
    p_sorted = tr_p[order]
    d_sorted = tr_d[order]
    y_sorted = tr_y[order]
    yr_sorted = tr_yr[order]

    t_starts = np.searchsorted(p_sorted, np.arange(n_targets), side='left')
    t_ends = np.searchsorted(p_sorted, np.arange(n_targets), side='right')

    bank = [None] * n_targets
    w1, w2, w3, w4 = w

    for t in range(n_targets):
        rs, re = t_starts[t], t_ends[t]
        n_tr = re - rs
        if n_tr == 0:
            continue
        r_d = d_sorted[rs:re]
        r_y = y_sorted[rs:re]
        r_yr = yr_sorted[rs:re]

        # Dedup by ligand index within target
        uniq_d, inv = np.unique(r_d, return_inverse=True)
        m = len(uniq_d)
        cnts = np.bincount(inv).astype(np.float32)
        mean_y = (np.bincount(inv, weights=r_y) / cnts).astype(np.float32)

        # Target baseline with empirical Bayes shrinkage
        t_mean = float(np.mean(r_y))
        t_mean_shrunk = (n_tr * t_mean + 10.0 * global_mean) / (n_tr + 10.0)
        yc = mean_y - t_mean_shrunk

        r1 = u8_1[uniq_d]
        rp1 = p1[uniq_d]
        r2 = u8_2[uniq_d]
        rp2 = p2[uniq_d]
        r3 = u8_3[uniq_d]
        rp3 = p3[uniq_d]
        r4 = u8_4[uniq_d]
        rp4 = p4[uniq_d]

        K1, K2 = multiview_tanimoto_sym(r1, rp1, r2, rp2, r3, rp3, r4, rp4, w1, w2, w3, w4)
        K4 = K2 * K2
        K_mix = 0.40 * K1 + 0.40 * K2 + 0.20 * K4

        diag_reg1 = (lam1 / np.sqrt(cnts)).astype(np.float32)
        diag_reg2 = (lam2 / np.sqrt(cnts)).astype(np.float32)

        G1 = K1.copy()
        G1[np.arange(m), np.arange(m)] += diag_reg1
        alpha1 = np.linalg.solve(G1, yc)

        G_mix = K_mix.copy()
        G_mix[np.arange(m), np.arange(m)] += diag_reg2
        L_mix = np.linalg.cholesky(G_mix)
        v_y = np.linalg.solve(L_mix, yc)
        alpha_mix = np.linalg.solve(L_mix.T, v_y)

        bank[t] = {
            'uniq_d': uniq_d,
            'r1': r1, 'rp1': rp1,
            'r2': r2, 'rp2': rp2,
            'r3': r3, 'rp3': rp3,
            'r4': r4, 'rp4': rp4,
            'yc': yc,
            't_mean': t_mean_shrunk,
            'n_tr': n_tr,
            'm': m,
            'alpha1': alpha1,
            'alpha_mix': alpha_mix,
            'L_mix': L_mix
        }
    return bank


def predict_same_and_homology_tkrr(
    bank, S_prot,
    q_d, q_p,
    u8_1, p1, u8_2, p2, u8_3, p3, u8_4, p4,
    global_mean,
    w=(0.45, 0.20, 0.25, 0.10),
    top_k_hom=15
):
    """
    For every query (q_d[i], q_p[i]):
    1. Evaluates Multi-View TKRR on the same target t = q_p[i] (if present in bank),
       plus Schur-complement RKHS leverage tau_same[i] = ||L^{-1} k_t(q)||^2.
    2. Evaluates Homology-Transfer Multi-View TKRR across the top_k_hom most
       homologous training targets t' != t!
    """
    n_q = len(q_d)
    n_targets = S_prot.shape[0]
    w1, w2, w3, w4 = w

    pred_same_k1 = np.full(n_q, global_mean, dtype=np.float32)
    pred_same_mix = np.full(n_q, global_mean, dtype=np.float32)
    tau_same = np.zeros(n_q, dtype=np.float32)
    max_s_same = np.zeros(n_q, dtype=np.float32)

    pred_hom_abs = np.full(n_q, global_mean, dtype=np.float32)
    pred_hom_res = np.zeros(n_q, dtype=np.float32)
    tau_hom = np.zeros(n_q, dtype=np.float32)
    max_s_hom = np.zeros(n_q, dtype=np.float32)
    hom_top_sim = np.zeros(n_q, dtype=np.float32)

    # Group queries by target t
    q_order = np.argsort(q_p, kind='mergesort')
    qp_sorted = q_p[q_order]
    qd_sorted = q_d[q_order]
    q_starts = np.searchsorted(qp_sorted, np.arange(n_targets), side='left')
    q_ends = np.searchsorted(qp_sorted, np.arange(n_targets), side='right')

    # Pre-identify trained targets
    trained_mask = np.array([bank[t] is not None for t in range(n_targets)], dtype=bool)
    trained_indices = np.where(trained_mask)[0]

    for t in range(n_targets):
        qs, qe = q_starts[t], q_ends[t]
        if qe == qs:
            continue
        q_idx = q_order[qs:qe]
        qt_d = qd_sorted[qs:qe]
        uniq_q, q_inv = np.unique(qt_d, return_inverse=True)

        q1 = u8_1[uniq_q]
        qp1 = p1[uniq_q]
        q2 = u8_2[uniq_q]
        qp2 = p2[uniq_q]
        q3 = u8_3[uniq_q]
        qp3 = p3[uniq_q]
        q4 = u8_4[uniq_q]
        qp4 = p4[uniq_q]

        # 1. Same-Target TKRR
        bt = bank[t]
        if bt is not None:
            K1, K2, ms1 = multiview_tanimoto_cross(
                q1, qp1, q2, qp2, q3, qp3, q4, qp4,
                bt['r1'], bt['rp1'], bt['r2'], bt['rp2'], bt['r3'], bt['rp3'], bt['r4'], bt['rp4'],
                w1, w2, w3, w4
            )
            K4 = K2 * K2
            K_mix = 0.40 * K1 + 0.40 * K2 + 0.20 * K4
            u_pred1 = bt['t_mean'] + K1 @ bt['alpha1']
            u_pred_mix = bt['t_mean'] + K_mix @ bt['alpha_mix']

            # Schur-complement leverage tau = ||L^{-1} k||^2
            V = np.linalg.solve(bt['L_mix'], K_mix.T)
            u_tau = np.clip(np.sum(V * V, axis=0), 0.0, 1.0)

            pred_same_k1[q_idx] = u_pred1[q_inv]
            pred_same_mix[q_idx] = u_pred_mix[q_inv]
            tau_same[q_idx] = u_tau[q_inv]
            max_s_same[q_idx] = ms1[q_inv]

        # 2. Homology-Transfer TKRR across top_k_hom trained targets t' != t
        sims_t = S_prot[t, trained_indices].copy()
        for idx_pos, tp in enumerate(trained_indices):
            if tp == t:
                sims_t[idx_pos] = -1.0
        top_pos = np.argsort(-sims_t)[:top_k_hom]

        nq_u = len(uniq_q)
        num_abs = np.zeros(nq_u, dtype=np.float32)
        num_res = np.zeros(nq_u, dtype=np.float32)
        den_w = np.zeros(nq_u, dtype=np.float32)
        best_tau_h = np.zeros(nq_u, dtype=np.float32)
        best_ms_h = np.zeros(nq_u, dtype=np.float32)
        top_prot_s = float(max(sims_t[top_pos[0]], 0.0)) if len(top_pos) > 0 else 0.0

        for pos in top_pos:
            s_prot = float(sims_t[pos])
            if s_prot <= 0.08:
                continue
            tp = trained_indices[pos]
            btp = bank[tp]

            K1_h, K2_h, ms1_h = multiview_tanimoto_cross(
                q1, qp1, q2, qp2, q3, qp3, q4, qp4,
                btp['r1'], btp['rp1'], btp['r2'], btp['rp2'], btp['r3'], btp['rp3'], btp['r4'], btp['rp4'],
                w1, w2, w3, w4
            )
            K4_h = K2_h * K2_h
            K_mix_h = 0.40 * K1_h + 0.40 * K2_h + 0.20 * K4_h
            res_h = K_mix_h @ btp['alpha_mix']
            abs_h = btp['t_mean'] + res_h

            # Weight by protein homology^3 * ligand coverage on homologous target!
            # Notice: when a neighbor target t' has NOT tested any similar ligand (ms1_h < 0.25),
            # its TKRR prediction is just btp['t_mean'] (a target constant).
            # For within-target ranking and cross-target transfer, we weight heavily by ms1_h^3!
            w_prot = (s_prot ** 3)
            w_lig_res = (ms1_h ** 3) + 0.5 * np.max(K4_h, axis=1)
            w_lig_abs = 0.005 + w_lig_res

            num_abs += (w_prot * w_lig_abs) * abs_h
            num_res += (w_prot * w_lig_res) * res_h
            den_w += (w_prot * w_lig_abs)

            cand_tau = s_prot * ms1_h
            best_tau_h = np.maximum(best_tau_h, cand_tau)
            best_ms_h = np.maximum(best_ms_h, ms1_h)

        u_hom_abs = np.where(den_w > 1e-8, num_abs / np.maximum(den_w, 1e-8), global_mean)
        u_hom_res = np.where(den_w > 1e-8, num_res / np.maximum(den_w, 1e-8), 0.0)

        pred_hom_abs[q_idx] = u_hom_abs[q_inv]
        pred_hom_res[q_idx] = u_hom_res[q_inv]
        tau_hom[q_idx] = best_tau_h[q_inv]
        max_s_hom[q_idx] = best_ms_h[q_inv]
        hom_top_sim[q_idx] = top_prot_s

    return {
        'pred_same_k1': pred_same_k1,
        'pred_same_mix': pred_same_mix,
        'tau_same': tau_same,
        'max_s_same': max_s_same,
        'pred_hom_abs': pred_hom_abs,
        'pred_hom_res': pred_hom_res,
        'tau_hom': tau_hom,
        'max_s_hom': max_s_hom,
        'hom_top_sim': hom_top_sim,
    }


def main():
    group = dti_dg_group(path="data/")
    benchmark = group.get("BindingDB_Patent")
    train_val = benchmark["train_val"]

    prot_npz = np.load("cache/protein_features.npz", allow_pickle=True)
    lig_npz = np.load("cache/ligand_features.npz", allow_pickle=True)

    unique_proteins = prot_npz["targets"]
    unique_drugs = lig_npz["smiles"]

    S_prot, S_kmer, S_sw = build_protein_similarity_matrix(unique_proteins)
    # Save S_prot for downstream scripts
    np.savez_compressed("cache/protein_homology.npz", S_prot=S_prot, S_kmer=S_kmer, S_sw=S_sw)

    prot_to_id = {s: i for i, s in enumerate(unique_proteins)}
    drug_to_id = {s: i for i, s in enumerate(unique_drugs)}

    tv_p = np.array([prot_to_id[s] for s in train_val["Target"].values], dtype=np.int32)
    tv_d = np.array([drug_to_id[s] for s in train_val["Drug"].values], dtype=np.int32)
    tv_y = train_val["Y"].values.astype(np.float32)
    tv_yr = train_val["Year"].values.astype(np.int32)

    u8_1 = lig_npz["fp_ecfp4"].view(np.uint8)
    p1 = popcnt_buf(u8_1, u8_1.shape[0], u8_1.shape[1])
    u8_2 = lig_npz["fp_ecfp6"].view(np.uint8)
    p2 = popcnt_buf(u8_2, u8_2.shape[0], u8_2.shape[1])
    u8_3 = lig_npz["fp_fcfp4"].view(np.uint8)
    p3 = popcnt_buf(u8_3, u8_3.shape[0], u8_3.shape[1])
    u8_4 = lig_npz["fp_maccs"].view(np.uint8)
    p4 = popcnt_buf(u8_4, u8_4.shape[0], u8_4.shape[1])

    for name, cut_yr in [
        ("Inner Temporal A (2013-2016 -> 2017-2018)", 2016),
        ("Inner Temporal B (2013-2017 -> 2018)", 2017),
    ]:
        tr_mask = tv_yr <= cut_yr
        va_mask = tv_yr > cut_yr
        tr_idx = np.where(tr_mask)[0]
        va_idx = np.where(va_mask)[0]

        t0 = time.time()
        g_mean = float(np.mean(tv_y[tr_idx]))
        bank = fit_target_tkrr_bank(
            tv_d[tr_idx], tv_p[tr_idx], tv_y[tr_idx], tv_yr[tr_idx],
            u8_1, p1, u8_2, p2, u8_3, p3, u8_4, p4,
            len(unique_proteins), g_mean
        )
        out = predict_same_and_homology_tkrr(
            bank, S_prot,
            tv_d[va_idx], tv_p[va_idx],
            u8_1, p1, u8_2, p2, u8_3, p3, u8_4, p4,
            g_mean
        )
        dt = time.time() - t0

        va_y = tv_y[va_idx]
        seen_targets = set(tv_p[tr_idx].tolist())
        seen_mask = np.array([p in seen_targets for p in tv_p[va_idx]], dtype=bool)
        unseen_mask = ~seen_mask

        # Schur-gated blend of Same-Target TKRR and Homology-Transfer TKRR
        tau = out['tau_same']
        # When tau_same is high, trust Same-Target TKRR; when low or 0 (unseen target), blend in Homology TKRR!
        schur_blend = np.where(
            seen_mask,
            (0.75 + 0.20 * tau) * out['pred_same_mix'] + (0.25 - 0.20 * tau) * (out['pred_same_mix'] + 0.6 * out['pred_hom_res']),
            0.55 * out['pred_hom_abs'] + 0.45 * (g_mean + out['pred_hom_res'])
        )

        print(f"\n=== {name} (solved in {dt:.2f}s) ===")
        for k_name, vec in [
            ("MultiView-TKRR-K1", out['pred_same_k1']),
            ("MultiView-TKRR-Mix", out['pred_same_mix']),
            ("Homology-TKRR-Abs", out['pred_hom_abs']),
            ("Homology-TKRR-Res", g_mean + out['pred_hom_res']),
            ("Schur-Coupled-TKRR", schur_blend),
        ]:
            pcc_all = pearsonr(va_y, vec)[0]
            pcc_seen = pearsonr(va_y[seen_mask], vec[seen_mask])[0]
            pcc_unseen = pearsonr(va_y[unseen_mask], vec[unseen_mask])[0]
            print(f"  {k_name:20s}: All PCC = {pcc_all:.5f} | Seen PCC = {pcc_seen:.5f} | Unseen PCC = {pcc_unseen:.5f}")


if __name__ == "__main__":
    main()
