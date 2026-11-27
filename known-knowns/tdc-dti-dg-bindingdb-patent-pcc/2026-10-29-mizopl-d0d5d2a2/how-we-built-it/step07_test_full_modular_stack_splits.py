#!/usr/bin/env python3
"""
Step 7 (v3 — Complete Multi-RHS Universal Kriging TKRR + Analytical Centered Cold Specialist):
  1. Solves 5 Multi-View TKRR predictors per target in a SINGLE vectorized factorization:
     - `pred_same_k1` (Linear Tanimoto K1)
     - `pred_same_k2` (Quadratic Tanimoto K2 = K1^2)
     - `pred_same_mix` (Polynomial 0.4 K1 + 0.4 K2 + 0.2 K4)
     - `pred_same_rec` (Recency-weighted Polynomial TKRR)
     - `pred_same_uk` (Universal Kriging Polynomial TKRR on residuals of 4328D Centered Ligand + Bilinear prior)
     + `tau_same` (Exact Schur-complement RKHS leverage)
  2. Seen-Target Specialist: retains both Centered and Uncentered 4328D Ligand Ridge + Factored Bilinear
     features alongside DualTanimotoKernelEngine + 5-head TKRR, trained on Expanding-Window Forward-Time OOF
     via RidgeCV + LightGBM (L2 & Huber).
  3. Unseen-Target Specialist: strictly analytical RKHS + Ridge combination of Pocket-LOTO-KRR (`f_target_krr`),
     4328D Centered Ligand Ridge (`q_lig_res_300`, `q_lig_res_900`), Centered Factored Bilinear (`q_bilin_res`),
     and Centered Cross-Target Canonical/Scaffold/Tanimoto/Pocket-Homology Residuals (no tree splits on target IDs,
     no uncentered Raw-Y target-offset confounding).
"""
import os
os.environ["NUMBA_THREADING_LAYER"] = "workqueue"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["OPENBLAS_NUM_THREADS"] = "1"

import time
from pathlib import Path
import numba as nb
import numpy as np
from scipy.sparse.linalg import LinearOperator, cg
from scipy.stats import pearsonr
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler, normalize
from tdc.benchmark_group import dti_dg_group

from numba_dual_kernel import DualTanimotoKernelEngine
from step05b_test_homology_tkrr import (
    popcnt_buf,
    multiview_tanimoto_sym,
    multiview_tanimoto_cross,
)
from step06_test_universal_kriging_and_unseen import (
    unpack_bits_u8_to_f32,
    fast_bilinear_matvec_numba,
    fast_bilinear_rhs_numba,
)

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"


def fit_predict_pocket_loto_krr_v3(
    tr_p: np.ndarray,
    tr_y: np.ndarray,
    S_prot: np.ndarray,
    S_kmer: np.ndarray,
    S_sw: np.ndarray,
    S_contain: np.ndarray,
    S_pocket: np.ndarray,
    prot_feats_norm: np.ndarray,
    global_mean: float,
):
    S_desc = np.clip(prot_feats_norm @ prot_feats_norm.T, -1.0, 1.0)
    S_desc_rbf = np.exp(-1.0 * np.maximum(0.0, 2.0 - 2.0 * S_desc)).astype(np.float32)

    K_all = (
        0.30 * S_pocket
        + 0.20 * (S_pocket ** 2)
        + 0.15 * S_contain
        + 0.15 * S_kmer
        + 0.10 * S_sw
        + 0.10 * S_desc_rbf
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
    shrink_n = 10.0
    emp_target_mean[uniq_t] = (
        (cnts * t_means + shrink_n * f_target_loto_u) / (cnts + shrink_n)
    ).astype(np.float32)

    return f_target_krr, f_target_loto, emp_target_mean, best_loto_pcc


def fit_predict_5head_tkrr_and_homology(
    tr_d: np.ndarray,
    tr_p: np.ndarray,
    tr_y: np.ndarray,
    tr_yr: np.ndarray,
    m_tr_prior: np.ndarray,
    m_q_prior: np.ndarray,
    q_d: np.ndarray,
    q_p: np.ndarray,
    S_pocket: np.ndarray,
    u8_1: np.ndarray, p1: np.ndarray,
    u8_2: np.ndarray, p2: np.ndarray,
    u8_3: np.ndarray, p3: np.ndarray,
    u8_4: np.ndarray, p4: np.ndarray,
    global_mean: float,
    w=(0.45, 0.20, 0.25, 0.10),
    top_k_hom: int = 3,
):
    """
    Fits 5 Multi-View TKRR heads per target (K1, K2, Mix, RecencyMix, UniversalKrigingMix)
    plus Schur-complement leverage `tau_same` and Pocket-Homology TKRR transfer (`top_k_hom=3`).
    """
    n_targets = S_pocket.shape[0]
    n_q = len(q_d)
    w1, w2, w3, w4 = w
    max_yr = float(np.max(tr_yr))

    order_tr = np.argsort(tr_p, kind="mergesort")
    p_tr_s = tr_p[order_tr]
    t_starts = np.searchsorted(p_tr_s, np.arange(n_targets), side="left")
    t_ends = np.searchsorted(p_tr_s, np.arange(n_targets), side="right")

    bank = [None] * n_targets
    for t in range(n_targets):
        rs, re = t_starts[t], t_ends[t]
        n_tr = re - rs
        if n_tr == 0:
            continue
        rows = order_tr[rs:re]
        r_d = tr_d[rows]
        r_y = tr_y[rows]
        r_yr = tr_yr[rows]
        r_uk_res = (r_y - m_tr_prior[rows]).astype(np.float32)

        uniq_d, inv = np.unique(r_d, return_inverse=True)
        m = len(uniq_d)
        cnts = np.bincount(inv).astype(np.float32)
        sqrt_cnts = np.sqrt(cnts)
        mean_y = (np.bincount(inv, weights=r_y) / cnts).astype(np.float32)
        mean_uk_res = (np.bincount(inv, weights=r_uk_res) / cnts).astype(np.float32)

        rw_row = np.exp(0.40 * (r_yr - max_yr)).astype(np.float32)
        rw_u = (np.bincount(inv, weights=rw_row) / cnts).astype(np.float32)
        rw_u = rw_u / max(float(np.mean(rw_u)), 1e-6)

        t_mean = float((np.sum(r_y) + 8.0 * global_mean) / (n_tr + 8.0))
        t_rec_mean = float((np.sum(r_y * rw_row) + 4.0 * global_mean) / (np.sum(rw_row) + 4.0))

        yc_std = (mean_y - t_mean).astype(np.float32)
        yc_rec = (mean_y - t_rec_mean).astype(np.float32)

        r1, rp1 = u8_1[uniq_d], p1[uniq_d]
        r2, rp2 = u8_2[uniq_d], p2[uniq_d]
        r3, rp3 = u8_3[uniq_d], p3[uniq_d]
        r4, rp4 = u8_4[uniq_d], p4[uniq_d]

        K1, K2 = multiview_tanimoto_sym(r1, rp1, r2, rp2, r3, rp3, r4, rp4, w1, w2, w3, w4)
        K4 = K2 * K2
        K_mix = 0.40 * K1 + 0.40 * K2 + 0.20 * K4

        idx_d = np.arange(m)
        G1 = K1.copy()
        G1[idx_d, idx_d] += 0.25 / sqrt_cnts
        alpha_k1 = np.linalg.solve(G1, yc_std)

        G2 = K2.copy()
        G2[idx_d, idx_d] += 0.15 / sqrt_cnts
        alpha_k2 = np.linalg.solve(G2, yc_std)

        G_mix = K_mix.copy()
        G_mix[idx_d, idx_d] += 0.12 / sqrt_cnts
        L_mix = np.linalg.cholesky(G_mix)
        # Solve both standard Mix and Universal-Kriging Mix using the SAME Cholesky factor L_mix!
        Y_both = np.column_stack([yc_std, mean_uk_res])
        V_both = np.linalg.solve(L_mix, Y_both)
        Alpha_both = np.linalg.solve(L_mix.T, V_both)
        alpha_mix = Alpha_both[:, 0]
        alpha_uk = Alpha_both[:, 1]

        G_rec = K_mix.copy()
        G_rec[idx_d, idx_d] += 0.12 / (sqrt_cnts * (0.65 + 0.35 * rw_u))
        alpha_rec = np.linalg.solve(G_rec, yc_rec)

        bank[t] = {
            "r1": r1, "rp1": rp1,
            "r2": r2, "rp2": rp2,
            "r3": r3, "rp3": rp3,
            "r4": r4, "rp4": rp4,
            "t_mean": t_mean,
            "t_rec_mean": t_rec_mean,
            "alpha_k1": alpha_k1,
            "alpha_k2": alpha_k2,
            "alpha_mix": alpha_mix,
            "alpha_uk": alpha_uk,
            "alpha_rec": alpha_rec,
            "L_mix": L_mix,
        }

    pred_same_k1 = np.full(n_q, global_mean, dtype=np.float32)
    pred_same_k2 = np.full(n_q, global_mean, dtype=np.float32)
    pred_same_mix = np.full(n_q, global_mean, dtype=np.float32)
    pred_same_rec = np.full(n_q, global_mean, dtype=np.float32)
    pred_same_uk = m_q_prior.copy().astype(np.float32)
    tau_same = np.zeros(n_q, dtype=np.float32)
    max_s_same = np.zeros(n_q, dtype=np.float32)

    pred_hom_abs = np.full(n_q, global_mean, dtype=np.float32)
    pred_hom_res = np.zeros(n_q, dtype=np.float32)
    tau_hom = np.zeros(n_q, dtype=np.float32)
    max_s_hom = np.zeros(n_q, dtype=np.float32)
    hom_top_sim = np.zeros(n_q, dtype=np.float32)

    q_order = np.argsort(q_p, kind="mergesort")
    qp_s = q_p[q_order]
    qd_s = q_d[q_order]
    q_starts = np.searchsorted(qp_s, np.arange(n_targets), side="left")
    q_ends = np.searchsorted(qp_s, np.arange(n_targets), side="right")

    trained_indices = np.array([t for t in range(n_targets) if bank[t] is not None], dtype=np.int32)

    for t in range(n_targets):
        qs, qe = q_starts[t], q_ends[t]
        if qe == qs:
            continue
        q_idx = q_order[qs:qe]
        qt_d = qd_s[qs:qe]
        uniq_q, q_inv = np.unique(qt_d, return_inverse=True)

        q1, qp1 = u8_1[uniq_q], p1[uniq_q]
        q2, qp2 = u8_2[uniq_q], p2[uniq_q]
        q3, qp3 = u8_3[uniq_q], p3[uniq_q]
        q4, qp4 = u8_4[uniq_q], p4[uniq_q]

        bt = bank[t]
        if bt is not None:
            K1, K2, ms1 = multiview_tanimoto_cross(
                q1, qp1, q2, qp2, q3, qp3, q4, qp4,
                bt["r1"], bt["rp1"], bt["r2"], bt["rp2"], bt["r3"], bt["rp3"], bt["r4"], bt["rp4"],
                w1, w2, w3, w4
            )
            K4 = K2 * K2
            K_mix = 0.40 * K1 + 0.40 * K2 + 0.20 * K4

            u_k1 = bt["t_mean"] + K1 @ bt["alpha_k1"]
            u_k2 = bt["t_mean"] + K2 @ bt["alpha_k2"]
            u_mix = bt["t_mean"] + K_mix @ bt["alpha_mix"]
            u_rec = bt["t_rec_mean"] + K_mix @ bt["alpha_rec"]
            u_uk_delta = K_mix @ bt["alpha_uk"]

            V = np.linalg.solve(bt["L_mix"], K_mix.T)
            u_tau = np.clip(np.sum(V * V, axis=0), 0.0, 1.0)

            pred_same_k1[q_idx] = u_k1[q_inv]
            pred_same_k2[q_idx] = u_k2[q_inv]
            pred_same_mix[q_idx] = u_mix[q_inv]
            pred_same_rec[q_idx] = u_rec[q_inv]
            pred_same_uk[q_idx] = m_q_prior[q_idx] + u_uk_delta[q_inv]
            tau_same[q_idx] = u_tau[q_inv]
            max_s_same[q_idx] = ms1[q_inv]

        # Pocket-Homology TKRR across top_k_hom trained targets t' != t
        if len(trained_indices) > 0:
            sims_t = S_pocket[t, trained_indices].copy()
            for idx_pos, tp in enumerate(trained_indices):
                if tp == t:
                    sims_t[idx_pos] = -1.0
            top_pos = np.argsort(-sims_t)[:top_k_hom]
            top_prot_s = float(max(sims_t[top_pos[0]], 0.0)) if len(top_pos) > 0 else 0.0

            nq_u = len(uniq_q)
            num_abs = np.zeros(nq_u, dtype=np.float32)
            num_res = np.zeros(nq_u, dtype=np.float32)
            den_w = np.zeros(nq_u, dtype=np.float32)
            best_tau_h = np.zeros(nq_u, dtype=np.float32)
            best_ms_h = np.zeros(nq_u, dtype=np.float32)

            for pos in top_pos:
                s_prot = float(sims_t[pos])
                if s_prot <= 0.08:
                    continue
                tp = trained_indices[pos]
                btp = bank[tp]
                K1_h, K2_h, ms1_h = multiview_tanimoto_cross(
                    q1, qp1, q2, qp2, q3, qp3, q4, qp4,
                    btp["r1"], btp["rp1"], btp["r2"], btp["rp2"], btp["r3"], btp["rp3"], btp["r4"], btp["rp4"],
                    w1, w2, w3, w4
                )
                K4_h = K2_h * K2_h
                K_mix_h = 0.40 * K1_h + 0.40 * K2_h + 0.20 * K4_h
                res_h = K_mix_h @ btp["alpha_mix"]
                abs_h = btp["t_mean"] + res_h

                w_prot = s_prot ** 4
                w_lig = (ms1_h ** 3) + 0.5 * np.max(K4_h, axis=1)
                num_abs += (w_prot * (0.01 + w_lig)) * abs_h
                num_res += (w_prot * w_lig) * res_h
                den_w += (w_prot * (0.01 + w_lig))

                best_tau_h = np.maximum(best_tau_h, s_prot * ms1_h)
                best_ms_h = np.maximum(best_ms_h, ms1_h)

            u_hom_abs = np.where(den_w > 1e-8, num_abs / np.maximum(den_w, 1e-8), global_mean)
            u_hom_res = np.where(den_w > 1e-8, num_res / np.maximum(den_w + 0.02, 1e-8), 0.0)

            pred_hom_abs[q_idx] = u_hom_abs[q_inv]
            pred_hom_res[q_idx] = u_hom_res[q_inv]
            tau_hom[q_idx] = best_tau_h[q_inv]
            max_s_hom[q_idx] = best_ms_h[q_inv]
            hom_top_sim[q_idx] = top_prot_s

    return np.column_stack([
        pred_same_k1,    # 0 (col 44)
        pred_same_k2,    # 1 (col 45)
        pred_same_mix,   # 2 (col 46)
        pred_same_rec,   # 3 (col 47)
        pred_same_uk,    # 4 (col 48)
        tau_same,        # 5 (col 49)
        max_s_same,      # 6 (col 50)
        pred_hom_abs,    # 7 (col 51)
        pred_hom_res,    # 8 (col 52)
        tau_hom,         # 9 (col 53)
        max_s_hom,       # 10 (col 54)
        hom_top_sim,     # 11 (col 55)
    ]).astype(np.float32)


class UnifiedDTIDGFeatureEngine:
    def __init__(self, cache_dir: Path):
        t0 = time.time()
        prot_npz = np.load(cache_dir / "protein_features.npz", allow_pickle=True)
        lig_npz = np.load(cache_dir / "ligand_features.npz", allow_pickle=True)
        hom_npz = np.load(cache_dir / "protein_homology.npz", allow_pickle=True)

        self.targets = list(prot_npz["targets"])
        self.smiles = list(lig_npz["smiles"])
        self.n_prots = len(self.targets)
        self.n_drugs = len(self.smiles)

        self.S_prot = hom_npz["S_prot"].astype(np.float32)
        self.S_kmer = hom_npz["S_kmer"].astype(np.float32)
        self.S_sw = hom_npz["S_sw"].astype(np.float32)
        self.S_pocket = hom_npz["S_pocket"].astype(np.float32)
        self.S_contain = hom_npz["S_contain"].astype(np.float32)

        raw_prot_x = np.nan_to_num(prot_npz["prot_feats"].astype(np.float32), 0.0)
        prot_x_std = np.clip(StandardScaler().fit_transform(raw_prot_x), -5.0, 5.0).astype(np.float32)
        self.prot_feats_norm = normalize(prot_x_std).astype(np.float32)

        S_blend = 0.55 * self.S_pocket + 0.45 * self.S_prot
        eigvals, eigvecs = np.linalg.eigh(S_blend.astype(np.float64))
        top64 = np.argsort(-eigvals)[:64]
        V_kpca = (eigvecs[:, top64] * np.sqrt(np.maximum(eigvals[top64], 1e-6))).astype(np.float32)
        Up, Sp, _ = np.linalg.svd(self.prot_feats_norm, full_matrices=False)
        V_svd = (Up[:, :48] * Sp[:48]).astype(np.float32)
        self.V_prot_all = np.hstack([V_kpca, V_svd]).astype(np.float32)  # (477, 112)
        self.V_prot_16 = np.hstack([V_kpca[:, :8], V_svd[:, :8]]).astype(np.float32)

        self.u8_1 = lig_npz["fp_ecfp4"].view(np.uint8)
        self.p1 = popcnt_buf(self.u8_1, self.u8_1.shape[0], self.u8_1.shape[1])
        self.u8_2 = lig_npz["fp_ecfp6"].view(np.uint8)
        self.p2 = popcnt_buf(self.u8_2, self.u8_2.shape[0], self.u8_2.shape[1])
        self.u8_3 = lig_npz["fp_fcfp4"].view(np.uint8)
        self.p3 = popcnt_buf(self.u8_3, self.u8_3.shape[0], self.u8_3.shape[1])
        self.u8_4 = lig_npz["fp_maccs"].view(np.uint8)
        self.p4 = popcnt_buf(self.u8_4, self.u8_4.shape[0], self.u8_4.shape[1])

        X_e4 = unpack_bits_u8_to_f32(self.u8_1) * 0.25
        X_e6 = unpack_bits_u8_to_f32(self.u8_2) * 0.25
        X_f4 = unpack_bits_u8_to_f32(self.u8_3) * 0.30
        X_mc = unpack_bits_u8_to_f32(self.u8_4) * 0.45
        mol_desc = np.nan_to_num(lig_npz["mol_desc"].astype(np.float32), 0.0)
        self.mol_desc_std = np.clip(StandardScaler().fit_transform(mol_desc), -5.0, 5.0).astype(np.float32)

        self.X_lig_all = np.hstack([X_e4, X_e6, X_f4, X_mc, self.mol_desc_std * 0.35]).astype(np.float32)
        rng = np.random.default_rng(42)
        proj_mat = rng.standard_normal((self.X_lig_all.shape[1], 192), dtype=np.float32) / np.sqrt(192.0)
        self.U_lig_232 = np.hstack([self.X_lig_all @ proj_mat, self.mol_desc_std * 0.35]).astype(np.float32)
        self.U_lig_16 = np.hstack([self.U_lig_232[:, :8], self.mol_desc_std[:, :8]]).astype(np.float32)

        self.dual_engine = DualTanimotoKernelEngine(cache_dir, self.S_pocket)
        print(f"Initialized UnifiedDTIDGFeatureEngine in {time.time()-t0:.2f}s", flush=True)

    def extract_all_features(
        self,
        tr_d: np.ndarray,
        tr_p: np.ndarray,
        tr_yr: np.ndarray,
        tr_y: np.ndarray,
        tr_rid: np.ndarray,
        q_d: np.ndarray,
        q_p: np.ndarray,
        q_yr: np.ndarray,
        q_rid: np.ndarray,
    ) -> np.ndarray:
        g_mean = float(np.mean(tr_y))

        # 1. DualTanimotoKernelEngine (cols 0..43)
        f_dual = self.dual_engine.compute(
            tr_d, tr_p, tr_yr, tr_y, tr_rid,
            q_d, q_p, q_yr, q_rid
        )

        # 2. Level 1 Pocket-LOTO-KRR
        f_target_krr, f_target_loto, emp_target_mean, _ = fit_predict_pocket_loto_krr_v3(
            tr_p, tr_y, self.S_prot, self.S_kmer, self.S_sw, self.S_contain, self.S_pocket,
            self.prot_feats_norm, g_mean
        )
        seen_t_set = set(tr_p.tolist())
        q_seen_flag = np.array([1.0 if p in seen_t_set else 0.0 for p in q_p], dtype=np.float32)

        # 3. Level 2 Exact 4,328D Ligand CG Ridge (Centered AND Uncentered Raw-Y)
        tr_y_res = (tr_y - emp_target_mean[tr_p]).astype(np.float32)
        tr_y_raw_c = (tr_y - g_mean).astype(np.float32)

        uniq_d, inv_d = np.unique(tr_d, return_inverse=True)
        cnt_d = np.bincount(inv_d).astype(np.float32)
        mean_res_d = (np.bincount(inv_d, weights=tr_y_res) / cnt_d).astype(np.float32)
        mean_raw_d = (np.bincount(inv_d, weights=tr_y_raw_c) / cnt_d).astype(np.float32)
        w_d = np.sqrt(cnt_d)
        X_u = self.X_lig_all[uniq_d]
        d_lig = self.X_lig_all.shape[1]

        def matvec_lig(v):
            v32 = v.astype(np.float32)
            return (X_u.T @ (w_d * (X_u @ v32)) + 300.0 * v32).astype(np.float64)

        A_lig = LinearOperator((d_lig, d_lig), matvec=matvec_lig, dtype=np.float64)
        w_lig_res, _ = cg(A_lig, (X_u.T @ (w_d * mean_res_d)).astype(np.float64), maxiter=25, rtol=1e-3)
        w_lig_raw, _ = cg(A_lig, (X_u.T @ (w_d * mean_raw_d)).astype(np.float64), maxiter=25, rtol=1e-3)

        q_lig_res = (self.X_lig_all[q_d] @ w_lig_res.astype(np.float32)).astype(np.float32)
        q_lig_raw = g_mean + (self.X_lig_all[q_d] @ w_lig_raw.astype(np.float32)).astype(np.float32)
        tr_lig_res = (self.X_lig_all[tr_d] @ w_lig_res.astype(np.float32)).astype(np.float32)

        # 4. Level 3 Factored Bilinear Kronecker Ridge (Centered AND Uncentered Raw-Y)
        double_res = (tr_y_res - 0.75 * tr_lig_res).astype(np.float32)
        d_u = self.U_lig_232.shape[1]
        d_v = self.V_prot_all.shape[1]

        p_order = np.argsort(tr_p, kind="mergesort")
        p_sorted = tr_p[p_order]
        U_sorted = np.ascontiguousarray(self.U_lig_232[tr_d[p_order]])
        r_res_sorted = np.ascontiguousarray(double_res[p_order])
        r_raw_sorted = np.ascontiguousarray(tr_y_raw_c[p_order])
        p_starts = np.searchsorted(p_sorted, np.arange(self.n_prots), side="left").astype(np.int32)
        p_ends = np.searchsorted(p_sorted, np.arange(self.n_prots), side="right").astype(np.int32)

        def matvec_bilin(w_flat):
            W = w_flat.reshape(d_u, d_v).astype(np.float32)
            M = np.ascontiguousarray(W @ self.V_prot_all.T)
            G_mat = fast_bilinear_matvec_numba(M, U_sorted, p_starts, p_ends)
            grad = G_mat @ self.V_prot_all + 1200.0 * W
            return grad.ravel().astype(np.float64)

        A_bilin = LinearOperator((d_u * d_v, d_u * d_v), matvec=matvec_bilin, dtype=np.float64)

        G_rhs_res = fast_bilinear_rhs_numba(U_sorted, r_res_sorted, p_starts, p_ends, self.n_prots)
        w_bilin_res, _ = cg(A_bilin, (G_rhs_res @ self.V_prot_all).ravel().astype(np.float64), maxiter=18, rtol=2e-3)
        M_bilin_res = w_bilin_res.reshape(d_u, d_v).astype(np.float32) @ self.V_prot_all.T
        q_bilin_res = np.sum(self.U_lig_232[q_d] * M_bilin_res[:, q_p].T, axis=1).astype(np.float32)
        tr_bilin_res = np.sum(self.U_lig_232[tr_d] * M_bilin_res[:, tr_p].T, axis=1).astype(np.float32)

        G_rhs_raw = fast_bilinear_rhs_numba(U_sorted, r_raw_sorted, p_starts, p_ends, self.n_prots)
        w_bilin_raw, _ = cg(A_bilin, (G_rhs_raw @ self.V_prot_all).ravel().astype(np.float64), maxiter=18, rtol=2e-3)
        M_bilin_raw = w_bilin_raw.reshape(d_u, d_v).astype(np.float32) @ self.V_prot_all.T
        q_bilin_raw = g_mean + np.sum(self.U_lig_232[q_d] * M_bilin_raw[:, q_p].T, axis=1).astype(np.float32)

        # Prior mean functions for Universal Kriging
        m_tr_prior = (emp_target_mean[tr_p] + 0.45 * tr_lig_res + 0.30 * tr_bilin_res).astype(np.float32)
        m_q_prior = (emp_target_mean[q_p] + 0.55 * q_lig_res + 0.35 * q_bilin_res).astype(np.float32)

        # 5. 5-Head Multi-View TKRR + Pocket-Homology TKRR (cols 44..55)
        f_tkrr = fit_predict_5head_tkrr_and_homology(
            tr_d, tr_p, tr_y, tr_yr, m_tr_prior, m_q_prior,
            q_d, q_p, self.S_pocket,
            self.u8_1, self.p1, self.u8_2, self.p2, self.u8_3, self.p3, self.u8_4, self.p4,
            g_mean, top_k_hom=3
        )

        # Pure Analytical Target-Centered Unseen-Target Predictor (NO tree splits, NO uncentered Raw-Y!)
        unseen_analytical_1 = (
            f_target_loto[q_p]
            + 0.58 * q_lig_res
            + 0.22 * q_bilin_res
            + 0.12 * f_dual[:, 31]   # global_can_resid
            + 0.08 * f_dual[:, 43]   # glob_knn_res8
            + 0.12 * f_tkrr[:, 8]    # pred_hom_res
        ).astype(np.float32)

        f_l1_l3 = np.column_stack([
            f_target_loto[q_p],      # 56
            emp_target_mean[q_p],    # 57
            q_seen_flag,             # 58
            q_lig_res,               # 59
            q_lig_raw,               # 60
            q_bilin_res,             # 61
            q_bilin_raw,             # 62
            m_q_prior,               # 63
            unseen_analytical_1,     # 64
        ]).astype(np.float32)

        f_coords = np.hstack([
            self.U_lig_16[q_d],      # 65..80
            self.V_prot_16[q_p],     # 81..96
        ]).astype(np.float32)

        return np.hstack([f_dual, f_tkrr, f_l1_l3, f_coords]).astype(np.float32)


def build_temporal_oof_v3(
    engine: UnifiedDTIDGFeatureEngine,
    tr_d: np.ndarray,
    tr_p: np.ndarray,
    tr_yr: np.ndarray,
    tr_y: np.ndarray,
    tr_rid: np.ndarray,
):
    years = sorted(np.unique(tr_yr).tolist())
    oof_temp_X = []
    oof_temp_y = []
    oof_temp_yr = []

    for yr in years[1:]:
        hist_mask = tr_yr < yr
        curr_mask = tr_yr == yr
        if np.sum(hist_mask) < 500 or np.sum(curr_mask) < 100:
            continue
        t_f = time.time()
        X_yr = engine.extract_all_features(
            tr_d[hist_mask], tr_p[hist_mask], tr_yr[hist_mask], tr_y[hist_mask], tr_rid[hist_mask],
            tr_d[curr_mask], tr_p[curr_mask], tr_yr[curr_mask], tr_rid[curr_mask],
        )
        oof_temp_X.append(X_yr)
        oof_temp_y.append(tr_y[curr_mask])
        oof_temp_yr.append(tr_yr[curr_mask])
        print(f"  Fold Year < {yr} -> {yr} ({np.sum(curr_mask)} rows) extracted in {time.time()-t_f:.2f}s", flush=True)

    return np.vstack(oof_temp_X), np.concatenate(oof_temp_y), np.concatenate(oof_temp_yr)


def fit_predict_two_regime_ensemble_v3(
    X_temp: np.ndarray,
    y_temp: np.ndarray,
    yr_temp: np.ndarray,
    X_va: np.ndarray,
    seed: int = 42,
):
    import lightgbm as lgb

    seen_temp_mask = X_temp[:, 58] > 0.5
    X_seen_tr = np.nan_to_num(X_temp[seen_temp_mask], 0.0)
    y_seen_tr = y_temp[seen_temp_mask]
    yr_seen_tr = yr_temp[seen_temp_mask]
    w_seen = np.exp(0.25 * (yr_seen_tr - np.max(yr_seen_tr))).astype(np.float32)

    seen_lin_cols = [
        1, 3, 8, 9, 10, 11, 17, 18, 25, 27, 28, 30, 31, 32, 33, 38, 40, 42, 43,
        44, 45, 46, 47, 48, 51, 52, 56, 57, 59, 60, 61, 62, 63, 64
    ]
    scaler_seen = StandardScaler()
    Xs_lin = scaler_seen.fit_transform(X_seen_tr[:, seen_lin_cols])
    ridge_seen = RidgeCV(alphas=np.logspace(1, 5, 25))
    ridge_seen.fit(Xs_lin, y_seen_tr, sample_weight=w_seen)

    lgb_seen_1 = lgb.LGBMRegressor(
        objective="regression",
        n_estimators=550,
        learning_rate=0.025,
        num_leaves=31,
        max_depth=6,
        min_child_samples=60,
        subsample=0.8,
        colsample_bytree=0.75,
        reg_alpha=5.0,
        reg_lambda=25.0,
        random_state=seed,
        n_jobs=1,
        verbose=-1,
    )
    lgb_seen_1.fit(X_seen_tr, y_seen_tr, sample_weight=w_seen)

    lgb_seen_2 = lgb.LGBMRegressor(
        objective="huber",
        alpha=1.35,
        n_estimators=550,
        learning_rate=0.025,
        num_leaves=23,
        max_depth=5,
        min_child_samples=80,
        subsample=0.8,
        colsample_bytree=0.70,
        reg_alpha=8.0,
        reg_lambda=40.0,
        random_state=seed + 100,
        n_jobs=1,
        verbose=-1,
    )
    lgb_seen_2.fit(X_seen_tr, y_seen_tr, sample_weight=w_seen)

    # Predict on validation/test X_va
    X_va_clean = np.nan_to_num(X_va, 0.0)

    pred_seen_ridge = ridge_seen.predict(scaler_seen.transform(X_va_clean[:, seen_lin_cols]))
    pred_seen_lgb1 = lgb_seen_1.predict(X_va_clean)
    pred_seen_lgb2 = lgb_seen_2.predict(X_va_clean)
    # 5-Head TKRR blend (K2 + Mix + RecencyMix + UniversalKrigingMix)
    pred_seen_tkrr = (
        0.20 * X_va_clean[:, 45]  # K2
        + 0.30 * X_va_clean[:, 46]  # Mix
        + 0.20 * X_va_clean[:, 47]  # Rec
        + 0.30 * X_va_clean[:, 48]  # UK
    )
    pred_seen = 0.25 * pred_seen_ridge + 0.30 * pred_seen_lgb1 + 0.20 * pred_seen_lgb2 + 0.25 * pred_seen_tkrr

    # Pure Analytical Target-Centered Unseen-Target Specialist (col 64)
    # No GBDT tree splits on target IDs, no uncentered Raw-Y!
    pred_cold = X_va_clean[:, 64]

    log_n_same = X_va_clean[:, 0]
    tau_same = X_va_clean[:, 49]
    seen_flag = X_va_clean[:, 58]

    w_seen_gate = np.where(
        seen_flag > 0.5,
        np.clip(0.82 + 0.10 * np.tanh(log_n_same / 3.0) + 0.08 * tau_same, 0.82, 0.99),
        0.0
    )
    pred_final = w_seen_gate * pred_seen + (1.0 - w_seen_gate) * pred_cold
    return pred_final, pred_seen, pred_cold, pred_seen_ridge, pred_seen_tkrr


def main():
    group = dti_dg_group(path=str(DATA_DIR))
    bm = group.get("BindingDB_Patent")
    tv = bm["train_val"].copy()

    engine = UnifiedDTIDGFeatureEngine(CACHE_DIR)
    t_to_idx = {t: i for i, t in enumerate(engine.targets)}
    d_to_idx = {s: i for i, s in enumerate(engine.smiles)}

    tv_p = tv["Target"].map(t_to_idx).values.astype(np.int32)
    tv_d = tv["Drug"].map(d_to_idx).values.astype(np.int32)
    tv_y = tv["Y"].values.astype(np.float32)
    tv_yr = tv["Year"].values.astype(np.int32)
    tv_rid = np.arange(len(tv), dtype=np.int32)

    for name, cut_yr in [
        ("Inner Temporal A (2013-2016 -> 2017-2018)", 2016),
        ("Inner Temporal B (2013-2017 -> 2018)", 2017),
    ]:
        t0 = time.time()
        tr_mask = tv_yr <= cut_yr
        va_mask = tv_yr > cut_yr

        tr_d, tr_p, tr_yr, tr_y, tr_rid = tv_d[tr_mask], tv_p[tr_mask], tv_yr[tr_mask], tv_y[tr_mask], tv_rid[tr_mask]
        va_d, va_p, va_yr, va_y, va_rid = tv_d[va_mask], tv_p[va_mask], tv_yr[va_mask], tv_y[va_mask], tv_rid[va_mask]

        print(f"\n--- Running {name} ---", flush=True)
        X_temp, y_temp, yr_temp = build_temporal_oof_v3(
            engine, tr_d, tr_p, tr_yr, tr_y, tr_rid
        )
        t_v = time.time()
        X_va = engine.extract_all_features(
            tr_d, tr_p, tr_yr, tr_y, tr_rid,
            va_d, va_p, va_yr, va_rid
        )
        print(f"  Validation features ({len(va_y)} rows) extracted in {time.time()-t_v:.2f}s", flush=True)

        pred_final, pred_seen, pred_cold, pred_seen_ridge, pred_seen_tkrr = fit_predict_two_regime_ensemble_v3(
            X_temp, y_temp, yr_temp, X_va, seed=42
        )
        dt = time.time() - t0

        seen_targets = set(tr_p.tolist())
        seen_mask = np.array([p in seen_targets for p in va_p], dtype=bool)
        unseen_mask = ~seen_mask

        print(f"=== {name} (solved in {dt:.2f}s) ===", flush=True)
        for lbl, vec in [
            ("Base: 5-Head MultiView-TKRR", pred_seen_tkrr),
            ("Cold-Specialist (Analytical Centered)", pred_cold),
            ("Seen-Specialist Ridge", pred_seen_ridge),
            ("Seen-Specialist Full (R+LGB+5TKRR)", pred_seen),
            ("Two-Regime Schur-Gated Ensemble", pred_final),
        ]:
            p_all = pearsonr(va_y, vec)[0]
            p_seen = pearsonr(va_y[seen_mask], vec[seen_mask])[0]
            p_unseen = pearsonr(va_y[unseen_mask], vec[unseen_mask])[0]
            print(f"  {lbl:36s}: All PCC = {p_all:.5f} | Seen PCC = {p_seen:.5f} | Unseen PCC = {p_unseen:.5f}", flush=True)


if __name__ == "__main__":
    main()
