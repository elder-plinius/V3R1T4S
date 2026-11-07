#!/usr/bin/env python3
"""
Step 6: Test the 4-Level Matryoshka Functional ANOVA + Universal Kriging Architecture:
  Level 1: Target-Level LOTO Kernel Ridge Regression f_target(t) on unique targets
           (using Pocket-Core Local Alignment S_pocket + S_contain + S_kmer + 586 descriptors)
  Level 2: Universal Ligand Potency Model f_ligand(d) on target-centered residuals (y - y_bar_t)
           Combining:
             (a) Fast Conjugate-Gradient Ridge on all 4,328 ligand features
                 (2048 ECFP4 + 1024 ECFP6 + 1024 FCFP4 + 167 MACCS + 40 RDKit 2D)
             (b) Global Ligand-First Tanimoto Kernel on target-centered residuals
  Level 3: Factored Bilinear Kronecker Interaction Model f_bilin(d, t) = u(d)^T W v(t)
           + Ligand-First Pocket-Homology Cross-Target Tanimoto Kernel
  Level 4: Universal Kriging Multi-View TKRR on the global prior residuals (y - m(d, t))!
"""
import os
os.environ.setdefault("NUMBA_THREADING_LAYER", "workqueue")

import time
from pathlib import Path
import numba as nb
import numpy as np
from scipy.sparse.linalg import LinearOperator, cg
from scipy.stats import pearsonr
from sklearn.preprocessing import StandardScaler, normalize
from tdc.benchmark_group import dti_dg_group

from step05b_test_homology_tkrr import (
    POPCNT_U8,
    popcnt_buf,
    multiview_tanimoto_sym,
    multiview_tanimoto_cross,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"


@nb.njit(parallel=True, fastmath=True, cache=True)
def unpack_bits_u8_to_f32(u8_arr: np.ndarray) -> np.ndarray:
    """Unpacks (N, B) uint8 array into (N, 8*B) float32 0/1 array."""
    n, n_bytes = u8_arr.shape
    out = np.empty((n, n_bytes * 8), dtype=np.float32)
    for i in nb.prange(n):
        for b in range(n_bytes):
            v = u8_arr[i, b]
            base = b * 8
            out[i, base + 0] = float((v >> 0) & 1)
            out[i, base + 1] = float((v >> 1) & 1)
            out[i, base + 2] = float((v >> 2) & 1)
            out[i, base + 3] = float((v >> 3) & 1)
            out[i, base + 4] = float((v >> 4) & 1)
            out[i, base + 5] = float((v >> 5) & 1)
            out[i, base + 6] = float((v >> 6) & 1)
            out[i, base + 7] = float((v >> 7) & 1)
    return out


@nb.njit(parallel=True, fastmath=True, cache=True)
def fast_bilinear_matvec_numba(
    M: np.ndarray,
    U_sorted: np.ndarray,
    p_starts: np.ndarray,
    p_ends: np.ndarray,
) -> np.ndarray:
    """
    Computes G_mat[:, p] = sum_{i in target p} U_sorted[i] * (U_sorted[i] @ M[:, p])
    in parallel over the 477 targets! Takes < 2 milliseconds!
    """
    d_u, n_prots = M.shape
    G_mat = np.zeros((d_u, n_prots), dtype=np.float32)
    for p in nb.prange(n_prots):
        s = p_starts[p]
        e = p_ends[p]
        if e == s:
            continue
        mp = M[:, p]
        acc = np.zeros(d_u, dtype=np.float32)
        for i in range(s, e):
            u_row = U_sorted[i]
            dot = 0.0
            for k in range(d_u):
                dot += u_row[k] * mp[k]
            for k in range(d_u):
                acc[k] += u_row[k] * dot
        G_mat[:, p] = acc
    return G_mat


@nb.njit(parallel=True, fastmath=True, cache=True)
def fast_bilinear_rhs_numba(
    U_sorted: np.ndarray,
    r_sorted: np.ndarray,
    p_starts: np.ndarray,
    p_ends: np.ndarray,
    n_prots: int,
) -> np.ndarray:
    d_u = U_sorted.shape[1]
    G_rhs = np.zeros((d_u, n_prots), dtype=np.float32)
    for p in nb.prange(n_prots):
        s = p_starts[p]
        e = p_ends[p]
        if e == s:
            continue
        acc = np.zeros(d_u, dtype=np.float32)
        for i in range(s, e):
            ri = r_sorted[i]
            u_row = U_sorted[i]
            for k in range(d_u):
                acc[k] += u_row[k] * ri
        G_rhs[:, p] = acc
    return G_rhs


@nb.njit(parallel=True, fastmath=True, cache=True)
def ligand_first_homology_tanimoto_kernel(
    q_d: np.ndarray,
    q_p: np.ndarray,
    tr_d: np.ndarray,
    tr_p: np.ndarray,
    tr_y: np.ndarray,
    tr_y_res: np.ndarray,
    u8_1: np.ndarray,
    p1: np.ndarray,
    u8_3: np.ndarray,
    p3: np.ndarray,
    S_pocket: np.ndarray,
    global_mean: float,
):
    """
    Ligand-First Cross-Target Tanimoto + Pocket-Homology Kernel (Op-M3 + Op-M5):
    Uses popcount pruning (`min(pa, pb) < 0.25 * max(pa, pb)`) to skip 90%+ of pairs in O(1),
    then evaluates ECFP4 + FCFP4 Tanimoto coupled with Pocket-Core homology S_pocket[qp, tp]!
    """
    nq = len(q_d)
    ntr = len(tr_d)
    b1 = u8_1.shape[1]
    b3 = u8_3.shape[1]

    out_lig_res = np.zeros(nq, dtype=np.float32)
    out_hom_res = np.zeros(nq, dtype=np.float32)
    out_hom_abs = np.full(nq, global_mean, dtype=np.float32)
    out_max_sim_other = np.zeros(nq, dtype=np.float32)
    out_max_hom_sim = np.zeros(nq, dtype=np.float32)

    for i in nb.prange(nq):
        qd_i = q_d[i]
        qp_i = q_p[i]
        q1_vec = u8_1[qd_i]
        qp1_val = p1[qd_i]
        q3_vec = u8_3[qd_i]
        qp3_val = p3[qd_i]
        min_p1 = 0.25 * qp1_val
        max_p1 = 4.0 * qp1_val

        num_lig_res = 0.0
        den_lig_res = 0.0

        num_hom_res = 0.0
        num_hom_abs = 0.0
        den_hom = 0.0

        max_s_other = 0.0
        max_sh = 0.0

        for j in range(ntr):
            tp_j = tr_p[j]
            if tp_j == qp_i:
                continue
            td_j = tr_d[j]
            if td_j == qd_i:
                s1 = 1.0
                s3 = 1.0
            else:
                pj_val = p1[td_j]
                if pj_val < min_p1 or pj_val > max_p1:
                    continue
                c1 = 0
                for b in range(b1):
                    c1 += POPCNT_U8[q1_vec[b] & u8_1[td_j, b]]
                d1 = qp1_val + pj_val - c1
                s1 = c1 / d1 if d1 > 0 else 0.0
                if s1 < 0.25:
                    continue
                c3 = 0
                for b in range(b3):
                    c3 += POPCNT_U8[q3_vec[b] & u8_3[td_j, b]]
                d3 = qp3_val + p3[td_j] - c3
                s3 = c3 / d3 if d3 > 0 else 0.0

            s_lig = 0.65 * s1 + 0.35 * s3
            if s_lig > max_s_other:
                max_s_other = s_lig

            s2 = s_lig * s_lig
            s6 = s2 * s2 * s2
            num_lig_res += s6 * tr_y_res[j]
            den_lig_res += s6

            s_poc = S_pocket[qp_i, tp_j]
            if s_poc > 0.15:
                sh = s_lig * s_poc
                if sh > max_sh:
                    max_sh = sh
                w_hom = s6 * (s_poc * s_poc * s_poc * s_poc)
                num_hom_res += w_hom * tr_y_res[j]
                num_hom_abs += w_hom * tr_y[j]
                den_hom += w_hom

        if den_lig_res > 1e-12:
            out_lig_res[i] = num_lig_res / den_lig_res
        if den_hom > 1e-12:
            out_hom_res[i] = num_hom_res / den_hom
            out_hom_abs[i] = num_hom_abs / den_hom
        out_max_sim_other[i] = max_s_other
        out_max_hom_sim[i] = max_sh

    return out_lig_res, out_hom_res, out_hom_abs, out_max_sim_other, out_max_hom_sim


def fit_predict_level1_target_loto_krr(
    tr_p: np.ndarray,
    tr_y: np.ndarray,
    S_prot: np.ndarray,
    S_kmer: np.ndarray,
    S_pocket: np.ndarray,
    S_contain: np.ndarray,
    prot_feats_norm: np.ndarray,
    global_mean: float,
):
    """
    Level 1: Fits a Target-Level Multi-Kernel Ridge Regression on the UNIQUE targets
    in `tr_p`, tuned via exact Leave-One-Target-Out (LOTO) cross-validation!
    """
    S_desc = np.clip(prot_feats_norm @ prot_feats_norm.T, -1.0, 1.0)
    S_desc_rbf = np.exp(-1.0 * np.maximum(0.0, 2.0 - 2.0 * S_desc)).astype(np.float32)

    # Combined protein kernel including Pocket-Core and Containment alignment
    K_all = (
        0.25 * S_kmer
        + 0.30 * (S_pocket ** 2)
        + 0.20 * (S_contain ** 2)
        + 0.10 * S_prot
        + 0.15 * S_desc_rbf
    ).astype(np.float64)
    np.fill_diagonal(K_all, 1.0)

    uniq_t, inv = np.unique(tr_p, return_inverse=True)
    cnts = np.bincount(inv).astype(np.float64)
    t_means = np.bincount(inv, weights=tr_y.astype(np.float64)) / cnts

    w_t = np.log1p(cnts)
    w_t = w_t / np.mean(w_t)

    K_uu = K_all[np.ix_(uniq_t, uniq_t)]
    yc = t_means - global_mean

    best_lam = 1.0
    best_loto_pcc = -1.0
    for lam in [0.1, 0.25, 0.5, 1.0, 2.0, 4.0]:
        G = K_uu + np.diag(lam / w_t)
        G_inv = np.linalg.inv(G)
        alpha = G_inv @ yc
        y_loto = global_mean + yc - (alpha / np.diag(G_inv))
        mask_10 = cnts >= 10
        pcc = pearsonr(t_means[mask_10], y_loto[mask_10])[0]
        if pcc > best_loto_pcc:
            best_loto_pcc = pcc
            best_lam = lam

    G_best = K_uu + np.diag(best_lam / w_t)
    alpha_best = np.linalg.solve(G_best, yc)
    f_target_krr = (global_mean + K_all[:, uniq_t] @ alpha_best).astype(np.float32)

    G_inv_best = np.linalg.inv(G_best)
    f_target_loto_u = (global_mean + yc - (alpha_best / np.diag(G_inv_best))).astype(np.float32)
    f_target_loto = f_target_krr.copy()
    f_target_loto[uniq_t] = f_target_loto_u

    emp_target_mean = f_target_krr.copy()
    shrink_n = 12.0
    emp_target_mean[uniq_t] = (
        (cnts * t_means + shrink_n * f_target_loto_u) / (cnts + shrink_n)
    ).astype(np.float32)

    return f_target_krr, f_target_loto, emp_target_mean, best_loto_pcc


def main():
    group = dti_dg_group(path=str(DATA_DIR))
    bm = group.get("BindingDB_Patent")
    tv = bm["train_val"].copy()

    prot_npz = np.load(CACHE_DIR / "protein_features.npz", allow_pickle=True)
    lig_npz = np.load(CACHE_DIR / "ligand_features.npz", allow_pickle=True)
    hom_npz = np.load(CACHE_DIR / "protein_homology.npz", allow_pickle=True)

    all_targets = list(prot_npz["targets"])
    t_to_idx = {t: i for i, t in enumerate(all_targets)}
    all_smiles = list(lig_npz["smiles"])
    d_to_idx = {s: i for i, s in enumerate(all_smiles)}

    tv_p = tv["Target"].map(t_to_idx).values.astype(np.int32)
    tv_d = tv["Drug"].map(d_to_idx).values.astype(np.int32)
    tv_y = tv["Y"].values.astype(np.float32)
    tv_yr = tv["Year"].values.astype(np.int32)

    S_prot = hom_npz["S_prot"].astype(np.float32)
    S_kmer = hom_npz["S_kmer"].astype(np.float32)
    S_pocket = hom_npz["S_pocket"].astype(np.float32)
    S_contain = hom_npz["S_contain"].astype(np.float32)

    raw_prot_x = np.nan_to_num(prot_npz["prot_feats"].astype(np.float32), 0.0)
    prot_x_std = np.clip(StandardScaler().fit_transform(raw_prot_x), -5.0, 5.0).astype(np.float32)
    prot_feats_norm = normalize(prot_x_std).astype(np.float32)

    eigvals, eigvecs = np.linalg.eigh(S_prot.astype(np.float64))
    top64_idx = np.argsort(-eigvals)[:64]
    V_kpca = (eigvecs[:, top64_idx] * np.sqrt(np.maximum(eigvals[top64_idx], 1e-6))).astype(np.float32)
    Up, Sp, _ = np.linalg.svd(prot_feats_norm, full_matrices=False)
    V_desc_svd = (Up[:, :48] * Sp[:48]).astype(np.float32)
    V_prot_all = np.hstack([V_kpca, V_desc_svd]).astype(np.float32)

    t0 = time.time()
    u8_1 = lig_npz["fp_ecfp4"].view(np.uint8)
    p1 = popcnt_buf(u8_1, u8_1.shape[0], u8_1.shape[1])
    u8_2 = lig_npz["fp_ecfp6"].view(np.uint8)
    p2 = popcnt_buf(u8_2, u8_2.shape[0], u8_2.shape[1])
    u8_3 = lig_npz["fp_fcfp4"].view(np.uint8)
    p3 = popcnt_buf(u8_3, u8_3.shape[0], u8_3.shape[1])
    u8_4 = lig_npz["fp_maccs"].view(np.uint8)
    p4 = popcnt_buf(u8_4, u8_4.shape[0], u8_4.shape[1])

    X_e4 = unpack_bits_u8_to_f32(u8_1) * 0.25
    X_e6 = unpack_bits_u8_to_f32(u8_2) * 0.25
    X_f4 = unpack_bits_u8_to_f32(u8_3) * 0.30
    X_mc = unpack_bits_u8_to_f32(u8_4) * 0.45
    mol_desc = np.nan_to_num(lig_npz["mol_desc"].astype(np.float32), 0.0)
    mol_desc_std = np.clip(StandardScaler().fit_transform(mol_desc), -5.0, 5.0).astype(np.float32) * 0.35

    X_lig_all = np.hstack([X_e4, X_e6, X_f4, X_mc, mol_desc_std]).astype(np.float32)
    rng = np.random.default_rng(42)
    proj_mat = rng.standard_normal((X_lig_all.shape[1], 192), dtype=np.float32) / np.sqrt(192.0)
    U_lig_all = np.hstack([X_lig_all @ proj_mat, mol_desc_std]).astype(np.float32)
    print(f"Prepared features in {time.time()-t0:.2f}s")

    for name, cut_yr in [
        ("Inner Temporal A (2013-2016 -> 2017-2018)", 2016),
        ("Inner Temporal B (2013-2017 -> 2018)", 2017),
    ]:
        t_split = time.time()
        tr_idx = np.where(tv_yr <= cut_yr)[0]
        va_idx = np.where(tv_yr > cut_yr)[0]

        tr_d, tr_p, tr_y = tv_d[tr_idx], tv_p[tr_idx], tv_y[tr_idx]
        va_d, va_p, va_y = tv_d[va_idx], tv_p[va_idx], tv_y[va_idx]
        g_mean = float(np.mean(tr_y))

        seen_targets = set(tr_p.tolist())
        seen_mask = np.array([p in seen_targets for p in va_p], dtype=bool)
        unseen_mask = ~seen_mask

        # Level 1: Target LOTO-KRR
        f_target_krr, f_target_loto, emp_target_mean, loto_pcc = fit_predict_level1_target_loto_krr(
            tr_p, tr_y, S_prot, S_kmer, S_pocket, S_contain, prot_feats_norm, g_mean
        )
        tr_y_res = tr_y - emp_target_mean[tr_p]

        # Level 2: Universal Ligand Potency Ridge on unique training drugs
        uniq_d, inv_d = np.unique(tr_d, return_inverse=True)
        cnt_d = np.bincount(inv_d).astype(np.float32)
        mean_res_d = (np.bincount(inv_d, weights=tr_y_res) / cnt_d).astype(np.float32)
        w_d = np.sqrt(cnt_d)
        X_u = X_lig_all[uniq_d]
        d_lig = X_lig_all.shape[1]

        def matvec_lig(v):
            v32 = v.astype(np.float32)
            return (X_u.T @ (w_d * (X_u @ v32)) + 300.0 * v32).astype(np.float64)

        rhs_lig = (X_u.T @ (w_d * mean_res_d)).astype(np.float64)
        w_lig, _ = cg(LinearOperator((d_lig, d_lig), matvec=matvec_lig, dtype=np.float64), rhs_lig, maxiter=30, rtol=1e-4)
        f_ligand_all = (X_lig_all @ w_lig.astype(np.float32)).astype(np.float32)
        double_res = tr_y_res - 0.75 * f_ligand_all[tr_d]

        # Level 3a: Fast Numba-accelerated Factored Bilinear Kronecker Ridge
        d_u = U_lig_all.shape[1]
        d_v = V_prot_all.shape[1]
        n_prots = len(all_targets)

        p_order = np.argsort(tr_p, kind='mergesort')
        p_sorted = tr_p[p_order]
        U_sorted = np.ascontiguousarray(U_lig_all[tr_d[p_order]])
        r_sorted = np.ascontiguousarray(double_res[p_order])
        p_starts = np.searchsorted(p_sorted, np.arange(n_prots), side='left').astype(np.int32)
        p_ends = np.searchsorted(p_sorted, np.arange(n_prots), side='right').astype(np.int32)

        def matvec_bilin(w_flat):
            W = w_flat.reshape(d_u, d_v).astype(np.float32)
            M = np.ascontiguousarray(W @ V_prot_all.T)
            G_mat = fast_bilinear_matvec_numba(M, U_sorted, p_starts, p_ends)
            grad = G_mat @ V_prot_all + 1200.0 * W
            return grad.ravel().astype(np.float64)

        G_rhs = fast_bilinear_rhs_numba(U_sorted, r_sorted, p_starts, p_ends, n_prots)
        rhs_bilin = (G_rhs @ V_prot_all).ravel().astype(np.float64)
        w_bilin, _ = cg(LinearOperator((d_u * d_v, d_u * d_v), matvec=matvec_bilin, dtype=np.float64), rhs_bilin, maxiter=25, rtol=1e-3)
        M_bilin = w_bilin.reshape(d_u, d_v).astype(np.float32) @ V_prot_all.T

        f_bilin_tr = np.sum(U_lig_all[tr_d] * M_bilin[:, tr_p].T, axis=1)
        f_bilin_va = np.sum(U_lig_all[va_d] * M_bilin[:, va_p].T, axis=1)

        # Level 3b: Deduplicated Ligand-First Cross-Target Tanimoto + Pocket-Homology Kernel
        pair_key_tr = tr_p.astype(np.int64) * 200000 + tr_d.astype(np.int64)
        _, uniq_tr_idx, tr_inv = np.unique(pair_key_tr, return_index=True, return_inverse=True)
        tr_pair_cnts = np.bincount(tr_inv).astype(np.float32)
        u_tr_d = tr_d[uniq_tr_idx]
        u_tr_p = tr_p[uniq_tr_idx]
        u_tr_y = (np.bincount(tr_inv, weights=tr_y) / tr_pair_cnts).astype(np.float32)
        u_tr_res = (np.bincount(tr_inv, weights=tr_y_res) / tr_pair_cnts).astype(np.float32)

        pair_key_va = va_p.astype(np.int64) * 200000 + va_d.astype(np.int64)
        _, uniq_va_idx, va_inv = np.unique(pair_key_va, return_index=True, return_inverse=True)
        u_va_d = va_d[uniq_va_idx]
        u_va_p = va_p[uniq_va_idx]

        u_lig_res, u_hom_res, u_hom_abs, u_max_s_other, u_max_sh = ligand_first_homology_tanimoto_kernel(
            u_va_d, u_va_p, u_tr_d, u_tr_p, u_tr_y, u_tr_res,
            u8_1, p1, u8_3, p3, S_pocket, g_mean
        )
        va_lig_res = u_lig_res[va_inv]
        va_hom_res = u_hom_res[va_inv]
        va_hom_abs = u_hom_abs[va_inv]
        va_max_sh = u_max_sh[va_inv]

        # Combine Levels 1 + 2 + 3 into Global Prior Mean Function m(d, t)
        m_va = (
            emp_target_mean[va_p]
            + 0.55 * f_ligand_all[va_d]
            + 0.45 * va_lig_res
            + 0.40 * f_bilin_va
            + 0.35 * va_hom_res
        )
        sh_gate = np.clip(va_max_sh * 1.3, 0.0, 0.70)
        m_va_unseen_enhanced = np.where(
            seen_mask,
            m_va,
            (1.0 - sh_gate) * m_va + sh_gate * va_hom_abs
        )

        # Level 4: Universal Kriging Multi-View TKRR on (y - m_prior(d, t))!
        m_tr = emp_target_mean[tr_p] + 0.45 * f_ligand_all[tr_d] + 0.30 * f_bilin_tr
        uk_pred = m_va_unseen_enhanced.copy()
        w1, w2, w3, w4 = 0.45, 0.20, 0.25, 0.10

        order_va = np.argsort(va_p, kind='mergesort')
        p_va_s = va_p[order_va]
        v_starts = np.searchsorted(p_va_s, np.arange(n_prots), side='left')
        v_ends = np.searchsorted(p_va_s, np.arange(n_prots), side='right')

        for t in range(n_prots):
            rs, re = p_starts[t], p_ends[t]
            vs, ve = v_starts[t], v_ends[t]
            if re == rs or ve == vs:
                continue
            tr_rows = p_order[rs:re]
            va_rows = order_va[vs:ve]

            r_d = tr_d[tr_rows]
            r_res_uk = (tr_y[tr_rows] - m_tr[tr_rows]).astype(np.float32)

            uniq_td, inv_td = np.unique(r_d, return_inverse=True)
            cnt_td = np.bincount(inv_td).astype(np.float32)
            yc_uk = (np.bincount(inv_td, weights=r_res_uk) / cnt_td).astype(np.float32)

            K1, K2 = multiview_tanimoto_sym(
                u8_1[uniq_td], p1[uniq_td],
                u8_2[uniq_td], p2[uniq_td],
                u8_3[uniq_td], p3[uniq_td],
                u8_4[uniq_td], p4[uniq_td],
                w1, w2, w3, w4
            )
            K4 = K2 * K2
            K_mix = 0.40 * K1 + 0.40 * K2 + 0.20 * K4
            G_mix = K_mix.copy()
            G_mix[np.arange(len(uniq_td)), np.arange(len(uniq_td))] += 0.14 / np.sqrt(cnt_td)
            alpha_uk = np.linalg.solve(G_mix, yc_uk)

            q_d_sub = va_d[va_rows]
            uniq_qd, inv_qd = np.unique(q_d_sub, return_inverse=True)
            K1_q, K2_q, _ = multiview_tanimoto_cross(
                u8_1[uniq_qd], p1[uniq_qd],
                u8_2[uniq_qd], p2[uniq_qd],
                u8_3[uniq_qd], p3[uniq_qd],
                u8_4[uniq_qd], p4[uniq_qd],
                u8_1[uniq_td], p1[uniq_td],
                u8_2[uniq_td], p2[uniq_td],
                u8_3[uniq_td], p3[uniq_td],
                u8_4[uniq_td], p4[uniq_td],
                w1, w2, w3, w4
            )
            K4_q = K2_q * K2_q
            K_mix_q = 0.40 * K1_q + 0.40 * K2_q + 0.20 * K4_q
            u_delta = K_mix_q @ alpha_uk
            uk_pred[va_rows] = m_va_unseen_enhanced[va_rows] + u_delta[inv_qd]

        dt = time.time() - t_split
        print(f"\n=== {name} (LOTO Target PCC={loto_pcc:.4f}, solved in {dt:.2f}s) ===")
        for label, pred_vec in [
            ("L1: Target-LOTO-KRR only", emp_target_mean[va_p]),
            ("L1+L2: + Global Ligand Ridge", emp_target_mean[va_p] + 0.65 * f_ligand_all[va_d]),
            ("L1+L2+L3a: + Factored Bilinear", emp_target_mean[va_p] + 0.60 * f_ligand_all[va_d] + 0.45 * f_bilin_va),
            ("L1+L2+L3b: + Pocket-Homology Kernel", m_va_unseen_enhanced),
            ("L1..L4: Universal Kriging TKRR", uk_pred),
        ]:
            p_all = pearsonr(va_y, pred_vec)[0]
            p_seen = pearsonr(va_y[seen_mask], pred_vec[seen_mask])[0]
            p_unseen = pearsonr(va_y[unseen_mask], pred_vec[unseen_mask])[0]
            print(f"  {label:35s}: All PCC = {p_all:.5f} | Seen PCC = {p_seen:.5f} | Unseen PCC = {p_unseen:.5f}")


if __name__ == "__main__":
    main()
