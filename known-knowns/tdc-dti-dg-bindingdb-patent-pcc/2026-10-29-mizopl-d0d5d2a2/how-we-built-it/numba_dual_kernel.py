#!/usr/bin/env python3
"""
numba_dual_kernel.py
Ultra-fast Apple Silicon (ARM64 LLVM Numba @njit(parallel=True)) engine for:
  1. Same-Target Multi-Fingerprint Tanimoto Kernel (both all-train LOO and Out-of-Patent-Series OOS)
  2. Exact Canonical Ligand, Murcko Scaffold & Generic Framework Target/Global Transfer
  3. Inverted-Index Global Ligand Tanimoto k-NN & Cross-Target Homology Dual Kernel
     (strictly excluding target t_q so Cold/Unseen-Target features have zero target leakage!)
"""
import os
os.environ.setdefault("NUMBA_THREADING_LAYER", "workqueue")
from pathlib import Path
import numba as nb
import numpy as np


@nb.njit(inline="always", cache=True)
def popcnt_u64(x: np.uint64) -> int:
    x = x - ((x >> np.uint64(1)) & np.uint64(0x5555555555555555))
    x = (x & np.uint64(0x3333333333333333)) + ((x >> np.uint64(2)) & np.uint64(0x3333333333333333))
    x = (x + (x >> np.uint64(4))) & np.uint64(0x0F0F0F0F0F0F0F0F)
    return int((x * np.uint64(0x0101010101010101)) >> np.uint64(56))


@nb.njit(inline="always")
def tanimoto_32(a: np.ndarray, b: np.ndarray, pop_a: int, pop_b: int) -> float:
    if pop_a == 0 or pop_b == 0:
        return 0.0
    inter = 0
    for w in range(32):
        inter += popcnt_u64(a[w] & b[w])
    uni = pop_a + pop_b - inter
    return float(inter) / float(uni) if uni > 0 else 0.0


@nb.njit(inline="always")
def tanimoto_16(a: np.ndarray, b: np.ndarray, pop_a: int, pop_b: int) -> float:
    if pop_a == 0 or pop_b == 0:
        return 0.0
    inter = 0
    for w in range(16):
        inter += popcnt_u64(a[w] & b[w])
    uni = pop_a + pop_b - inter
    return float(inter) / float(uni) if uni > 0 else 0.0


@nb.njit(inline="always")
def tanimoto_3(a: np.ndarray, b: np.ndarray, pop_a: int, pop_b: int) -> float:
    if pop_a == 0 or pop_b == 0:
        return 0.0
    inter = (
        popcnt_u64(a[0] & b[0])
        + popcnt_u64(a[1] & b[1])
        + popcnt_u64(a[2] & b[2])
    )
    uni = pop_a + pop_b - inter
    return float(inter) / float(uni) if uni > 0 else 0.0


@nb.njit(parallel=True)
def precompute_popcounts(fp_ecfp4, fp_ecfp6, fp_fcfp4, fp_maccs):
    n_lig = fp_ecfp4.shape[0]
    pop_e4 = np.zeros(n_lig, dtype=np.int32)
    pop_e6 = np.zeros(n_lig, dtype=np.int32)
    pop_f4 = np.zeros(n_lig, dtype=np.int32)
    pop_mc = np.zeros(n_lig, dtype=np.int32)
    for d in nb.prange(n_lig):
        p4 = 0
        for w in range(32):
            p4 += popcnt_u64(fp_ecfp4[d, w])
        p6 = 0
        for w in range(16):
            p6 += popcnt_u64(fp_ecfp6[d, w])
        pf = 0
        for w in range(16):
            pf += popcnt_u64(fp_fcfp4[d, w])
        pm = 0
        for w in range(3):
            pm += popcnt_u64(fp_maccs[d, w])
        pop_e4[d] = p4
        pop_e6[d] = p6
        pop_f4[d] = pf
        pop_mc[d] = pm
    return pop_e4, pop_e6, pop_f4, pop_mc


@nb.njit(parallel=True, fastmath=True, cache=True)
def _numba_compute_features(
    fp_ecfp4, fp_ecfp6, fp_fcfp4, fp_maccs,
    pop_e4, pop_e6, pop_f4, pop_mc,
    can_id, scaf_id, gscaf_id,
    prot_sim,
    tr_d_idx, tr_t_idx, tr_year, tr_y, tr_row_id,
    t_offsets, t_indices,
    can_offsets, can_indices,
    scaf_offsets, scaf_indices,
    gscaf_offsets, gscaf_indices,
    top_hom_targets,
    t_smooth_mean, t_rec_mean, t_std_vec, global_mean, max_year_tr,
    # Global unique training ligand index + rare-bit inverted index:
    utr_d_idx, utr_mean_y, utr_mean_resid, utr_t_rep,
    bit_offsets, bit_utr_indices, bit_doc_freq,
    q_d_idx, q_t_idx, q_year, q_row_id,
):
    n_q = q_d_idx.shape[0]
    out = np.zeros((n_q, 44), dtype=np.float32)

    for i in nb.prange(n_q):
        dq = q_d_idx[i]
        tq = q_t_idx[i]
        yr_q = q_year[i]
        rid_q = q_row_id[i]

        q_e4 = fp_ecfp4[dq]
        q_e6 = fp_ecfp6[dq]
        q_f4 = fp_fcfp4[dq]
        q_mc = fp_maccs[dq]
        pq_e4 = pop_e4[dq]
        pq_e6 = pop_e6[dq]
        pq_f4 = pop_f4[dq]
        pq_mc = pop_mc[dq]
        c_q = can_id[dq]
        s_q = scaf_id[dq]
        gs_q = gscaf_id[dq]

        # 1. Homology target prior (strictly from t' != tq)
        hom_t_num = 0.0
        hom_t_den = 0.0
        max_prot_sim = 0.0
        for k_h in range(top_hom_targets.shape[1]):
            tp = top_hom_targets[tq, k_h]
            if tp < 0:
                break
            sp = prot_sim[tq, tp]
            if sp > max_prot_sim:
                max_prot_sim = sp
            w = float(sp * sp * sp * sp)
            hom_t_num += w * t_smooth_mean[tp]
            hom_t_den += w
        hom_prior_y = float((hom_t_num + 0.03 * global_mean) / (hom_t_den + 0.03)) if hom_t_den > 1e-9 else global_mean

        # 2. Same-target bucket scan
        t_start = t_offsets[tq]
        t_end = t_offsets[tq + 1]
        n_same = 0
        sum_y_same = 0.0
        sum_y_rec = 0.0
        sum_w_rec = 0.0

        max_e4 = 0.0
        max_f4 = 0.0
        max_mc = 0.0
        max_comb = 0.0
        top1_y = hom_prior_y

        w2_sum = 0.0; wy2_sum = 0.0
        w6_sum = 0.0; wy6_sum = 0.0; wy6_sq_sum = 0.0
        w12_sum = 0.0; wy12_sum = 0.0
        w6r_sum = 0.0; wy6r_sum = 0.0
        cnt_gt_05 = 0; cnt_gt_07 = 0

        oos_max_comb = 0.0
        oos_top1_y = hom_prior_y
        oos_w2 = 0.0; oos_wy2 = 0.0
        oos_w6 = 0.0; oos_wy6 = 0.0
        oos_w12 = 0.0; oos_wy12 = 0.0

        past_n = 0
        past_sum_y = 0.0
        past_max_comb = 0.0
        past_w6 = 0.0; past_wy6 = 0.0

        for idx_p in range(t_start, t_end):
            j = t_indices[idx_p]
            if tr_row_id[j] == rid_q:
                continue
            dj = tr_d_idx[j]
            yj = float(tr_y[j])
            yr_j = tr_year[j]

            n_same += 1
            sum_y_same += yj
            wr = np.exp(0.45 * float(yr_j - max_year_tr))
            sum_y_rec += wr * yj
            sum_w_rec += wr

            s_e4 = tanimoto_32(q_e4, fp_ecfp4[dj], pq_e4, pop_e4[dj])
            s_e6 = tanimoto_16(q_e6, fp_ecfp6[dj], pq_e6, pop_e6[dj])
            s_f4 = tanimoto_16(q_f4, fp_fcfp4[dj], pq_f4, pop_f4[dj])
            s_mc = tanimoto_3(q_mc, fp_maccs[dj], pq_mc, pop_mc[dj])

            if s_e4 > max_e4: max_e4 = s_e4
            if s_f4 > max_f4: max_f4 = s_f4
            if s_mc > max_mc: max_mc = s_mc

            sc = 0.50 * s_e4 + 0.25 * s_e6 + 0.25 * s_f4
            if sc > max_comb:
                max_comb = sc
                top1_y = yj
            if sc >= 0.50: cnt_gt_05 += 1
            if sc >= 0.70: cnt_gt_07 += 1

            sc2 = sc * sc
            sc6 = sc2 * sc2 * sc2
            sc12 = sc6 * sc6

            w2_sum += sc2;   wy2_sum += sc2 * yj
            w6_sum += sc6;   wy6_sum += sc6 * yj; wy6_sq_sum += sc6 * yj * yj
            w12_sum += sc12; wy12_sum += sc12 * yj

            w6r = sc6 * wr
            w6r_sum += w6r;  wy6r_sum += w6r * yj

            same_patent_series = (yr_j == yr_q) and ((s_q >= 0 and scaf_id[dj] == s_q) or sc >= 0.75)
            if not same_patent_series:
                if sc > oos_max_comb:
                    oos_max_comb = sc
                    oos_top1_y = yj
                oos_w2 += sc2;   oos_wy2 += sc2 * yj
                oos_w6 += sc6;   oos_wy6 += sc6 * yj
                oos_w12 += sc12; oos_wy12 += sc12 * yj

            if yr_j < yr_q:
                past_n += 1
                past_sum_y += yj
                if sc > past_max_comb:
                    past_max_comb = sc
                past_w6 += sc6
                past_wy6 += sc6 * yj

        t_mean_i = float((sum_y_same + 5.0 * global_mean) / (n_same + 5.0)) if n_same > 0 else global_mean
        t_rec_i = float((sum_y_rec + 2.0 * global_mean) / (sum_w_rec + 2.0)) if n_same > 0 else global_mean
        t_std_i = float(t_std_vec[tq]) if n_same > 0 else 2.5

        knn_p2 = float((wy2_sum + 0.15 * t_mean_i) / (w2_sum + 0.15))
        knn_p6 = float((wy6_sum + 0.02 * t_mean_i) / (w6_sum + 0.02))
        knn_p12 = float((wy12_sum + 0.003 * t_mean_i) / (w12_sum + 0.003))
        knn_p6_rec = float((wy6r_sum + 0.02 * t_rec_i) / (w6r_sum + 0.02))
        if n_same == 0:
            top1_y = global_mean
            oos_top1_y = global_mean

        knn_std = 2.0
        if w6_sum > 1e-4:
            mean6 = wy6_sum / w6_sum
            var6 = (wy6_sq_sum / w6_sum) - mean6 * mean6
            knn_std = float(np.sqrt(max(0.0, var6)))

        oos_knn_p2 = float((oos_wy2 + 0.15 * t_mean_i) / (oos_w2 + 0.15))
        oos_knn_p6 = float((oos_wy6 + 0.02 * t_mean_i) / (oos_w6 + 0.02))
        oos_knn_p12 = float((oos_wy12 + 0.003 * t_mean_i) / (oos_w12 + 0.003))

        past_t_mean = float((past_sum_y + 5.0 * t_mean_i) / (past_n + 5.0))
        past_knn_p6 = float((past_wy6 + 0.02 * past_t_mean) / (past_w6 + 0.02))

        # 3. Exact canonical ligand & Murcko scaffold matches
        exact_pair_cnt = 0
        exact_pair_sum = 0.0
        global_can_cnt = 0
        global_can_sum = 0.0
        global_can_resid_sum = 0.0

        if c_q >= 0 and c_q + 1 < can_offsets.shape[0]:
            for idx_c in range(can_offsets[c_q], can_offsets[c_q + 1]):
                j = can_indices[idx_c]
                if tr_row_id[j] == rid_q:
                    continue
                tj = tr_t_idx[j]
                yj = float(tr_y[j])
                if tj == tq:
                    exact_pair_cnt += 1
                    exact_pair_sum += yj
                else:
                    global_can_cnt += 1
                    global_can_sum += yj
                    global_can_resid_sum += (yj - t_smooth_mean[tj])

        exact_pair_y = float(exact_pair_sum / exact_pair_cnt) if exact_pair_cnt > 0 else oos_knn_p6
        global_can_y = float((global_can_sum + 2.0 * global_mean) / (global_can_cnt + 2.0))
        global_can_resid = float(global_can_resid_sum / (global_can_cnt + 2.0))

        same_t_scaf_cnt = 0
        same_t_scaf_sum = 0.0
        global_scaf_cnt = 0
        global_scaf_sum = 0.0
        global_scaf_resid_sum = 0.0
        if s_q >= 0 and s_q + 1 < scaf_offsets.shape[0]:
            for idx_s in range(scaf_offsets[s_q], scaf_offsets[s_q + 1]):
                j = scaf_indices[idx_s]
                if tr_row_id[j] == rid_q:
                    continue
                tj = tr_t_idx[j]
                yj = float(tr_y[j])
                if tj == tq:
                    if yr_q != tr_year[j]:
                        same_t_scaf_cnt += 1
                        same_t_scaf_sum += yj
                else:
                    global_scaf_cnt += 1
                    global_scaf_sum += yj
                    global_scaf_resid_sum += (yj - t_smooth_mean[tj])

        same_t_scaf_y = float((same_t_scaf_sum + 2.0 * t_mean_i) / (same_t_scaf_cnt + 2.0))
        global_scaf_y = float((global_scaf_sum + 3.0 * global_mean) / (global_scaf_cnt + 3.0))
        global_scaf_resid = float(global_scaf_resid_sum / (global_scaf_cnt + 3.0))

        same_t_gscaf_cnt = 0
        same_t_gscaf_sum = 0.0
        if gs_q >= 0 and gs_q + 1 < gscaf_offsets.shape[0]:
            for idx_gs in range(gscaf_offsets[gs_q], gscaf_offsets[gs_q + 1]):
                j = gscaf_indices[idx_gs]
                if tr_row_id[j] == rid_q:
                    continue
                if tr_t_idx[j] == tq and yr_q != tr_year[j]:
                    same_t_gscaf_cnt += 1
                    same_t_gscaf_sum += float(tr_y[j])
        same_t_gscaf_y = float((same_t_gscaf_sum + 3.0 * t_mean_i) / (same_t_gscaf_cnt + 3.0))

        # 4 & 5 Unified: Rare-Bit Inverted Index Scan for both Global Ligand k-NN AND Cross-Target Dual Kernel
        rare_bits = np.full(8, -1, dtype=np.int32)
        rare_freqs = np.full(8, 99999999, dtype=np.int32)
        for w in range(32):
            word = q_e4[w]
            base_b = w * 64
            while word != np.uint64(0):
                tz = 0
                tmp = word
                while (tmp & np.uint64(1)) == np.uint64(0):
                    tz += 1
                    tmp >>= np.uint64(1)
                b_idx = base_b + tz
                df = bit_doc_freq[b_idx]
                if 0 < df < rare_freqs[7]:
                    pos = 7
                    while pos > 0 and df < rare_freqs[pos - 1]:
                        rare_freqs[pos] = rare_freqs[pos - 1]
                        rare_bits[pos] = rare_bits[pos - 1]
                        pos -= 1
                    rare_freqs[pos] = df
                    rare_bits[pos] = b_idx
                word &= (word - np.uint64(1))

        hom_max_dual = 0.0
        hom_max_lig = 0.0
        hd_w4 = 0.0; hd_wy4 = 0.0
        hd_w8 = 0.0; hd_wy8 = 0.0
        hd_wr6 = 0.0; hd_wres6 = 0.0

        glob_max_sim = 0.0
        glob_w4 = 0.0; glob_wy4 = 0.0
        glob_w8 = 0.0; glob_wres8 = 0.0

        for rb_i in range(8):
            b_idx = rare_bits[rb_i]
            if b_idx < 0:
                break
            b_start = bit_offsets[b_idx]
            b_end = bit_offsets[b_idx + 1]
            if b_end - b_start > 300:
                b_end = b_start + 300
            for idx_u in range(b_start, b_end):
                u = bit_utr_indices[idx_u]
                dj = utr_d_idx[u]
                if dj == dq:
                    continue
                p_dj = pop_e4[dj]
                mn_p = pq_e4 if pq_e4 < p_dj else p_dj
                mx_p = pq_e4 if pq_e4 > p_dj else p_dj
                if mx_p == 0 or mn_p * 3 < mx_p:
                    continue
                s_e4 = tanimoto_32(q_e4, fp_ecfp4[dj], pq_e4, p_dj)
                if s_e4 < 0.28:
                    continue
                s_f4 = tanimoto_16(q_f4, fp_fcfp4[dj], pq_f4, pop_f4[dj])
                sc = 0.65 * s_e4 + 0.35 * s_f4
                if sc > glob_max_sim:
                    glob_max_sim = sc
                sc2 = sc * sc
                sc4 = sc2 * sc2
                sc6 = sc4 * sc2
                sc8 = sc4 * sc4

                ym = float(utr_mean_y[u])
                yres = float(utr_mean_resid[u])
                glob_w4 += sc4; glob_wy4 += sc4 * ym
                glob_w8 += sc8; glob_wres8 += sc8 * yres

                tj = utr_t_rep[u]
                if tj != tq:
                    sp = float(prot_sim[tq, tj])
                    if sc > hom_max_lig:
                        hom_max_lig = sc
                    dual_s = sp * sc
                    if dual_s > hom_max_dual:
                        hom_max_dual = dual_s
                    sp2 = sp * sp
                    sp3 = sp2 * sp
                    w4 = sp2 * sc4
                    w8 = sp3 * sc8
                    wr6 = sp2 * sc6
                    hd_w4 += w4;   hd_wy4 += w4 * ym
                    hd_w8 += w8;   hd_wy8 += w8 * ym
                    hd_wr6 += wr6; hd_wres6 += wr6 * yres

        hom_dual_p4 = float((hd_wy4 + 0.02 * hom_prior_y) / (hd_w4 + 0.02))
        hom_dual_p8 = float((hd_wy8 + 0.002 * hom_prior_y) / (hd_w8 + 0.002))
        hom_dual_resid_p6 = hom_prior_y + float(hd_wres6 / (hd_wr6 + 0.01))

        glob_knn_y4 = float((glob_wy4 + 0.05 * global_mean) / (glob_w4 + 0.05))
        glob_knn_res8 = float(glob_wres8 / (glob_w8 + 0.005))

        # Store 44 features
        out[i, 0]  = np.log1p(float(n_same))
        out[i, 1]  = t_mean_i
        out[i, 2]  = t_std_i
        out[i, 3]  = t_rec_i
        out[i, 4]  = max_e4
        out[i, 5]  = max_f4
        out[i, 6]  = max_mc
        out[i, 7]  = top1_y
        out[i, 8]  = knn_p2
        out[i, 9]  = knn_p6
        out[i, 10] = knn_p12
        out[i, 11] = knn_p6_rec
        out[i, 12] = knn_std
        out[i, 13] = np.log1p(float(cnt_gt_05))
        out[i, 14] = np.log1p(float(cnt_gt_07))

        out[i, 15] = oos_max_comb
        out[i, 16] = oos_knn_p2
        out[i, 17] = oos_knn_p6
        out[i, 18] = oos_knn_p12
        out[i, 19] = oos_top1_y

        out[i, 20] = np.log1p(float(past_n))
        out[i, 21] = past_t_mean
        out[i, 22] = past_max_comb
        out[i, 23] = past_knn_p6

        out[i, 24] = np.log1p(float(exact_pair_cnt))
        out[i, 25] = exact_pair_y
        out[i, 26] = np.log1p(float(same_t_scaf_cnt))
        out[i, 27] = same_t_scaf_y
        out[i, 28] = same_t_gscaf_y
        out[i, 29] = np.log1p(float(global_can_cnt))
        out[i, 30] = global_can_y
        out[i, 31] = global_can_resid
        out[i, 32] = global_scaf_y
        out[i, 33] = global_scaf_resid

        out[i, 34] = max_prot_sim
        out[i, 35] = hom_prior_y
        out[i, 36] = hom_max_dual
        out[i, 37] = hom_max_lig
        out[i, 38] = hom_dual_p4
        out[i, 39] = hom_dual_p8
        out[i, 40] = hom_dual_resid_p6

        out[i, 41] = glob_max_sim
        out[i, 42] = glob_knn_y4
        out[i, 43] = glob_knn_res8

    return out


def build_csr_buckets(keys: np.ndarray, n_buckets: int):
    valid = keys >= 0
    v_keys = keys[valid]
    v_idx = np.nonzero(valid)[0].astype(np.int32)
    order = np.argsort(v_keys, kind="mergesort")
    sorted_k = v_keys[order]
    sorted_idx = v_idx[order]
    counts = np.bincount(sorted_k, minlength=n_buckets).astype(np.int32)
    offsets = np.zeros(n_buckets + 1, dtype=np.int32)
    np.cumsum(counts, out=offsets[1:])
    return offsets, sorted_idx


@nb.njit
def _build_inverted_bit_index(utr_d_idx: np.ndarray, fp_ecfp4: np.ndarray):
    n_u = utr_d_idx.shape[0]
    counts = np.zeros(2048, dtype=np.int32)
    for u in range(n_u):
        d = utr_d_idx[u]
        for w in range(32):
            word = fp_ecfp4[d, w]
            base_b = w * 64
            while word != np.uint64(0):
                tz = 0
                tmp = word
                while (tmp & np.uint64(1)) == np.uint64(0):
                    tz += 1
                    tmp >>= np.uint64(1)
                counts[base_b + tz] += 1
                word &= (word - np.uint64(1))

    offsets = np.zeros(2049, dtype=np.int32)
    for b in range(2048):
        offsets[b + 1] = offsets[b] + counts[b]

    indices = np.zeros(offsets[2048], dtype=np.int32)
    cur = offsets[:-1].copy()
    for u in range(n_u):
        d = utr_d_idx[u]
        for w in range(32):
            word = fp_ecfp4[d, w]
            base_b = w * 64
            while word != np.uint64(0):
                tz = 0
                tmp = word
                while (tmp & np.uint64(1)) == np.uint64(0):
                    tz += 1
                    tmp >>= np.uint64(1)
                b_idx = base_b + tz
                indices[cur[b_idx]] = u
                cur[b_idx] += 1
                word &= (word - np.uint64(1))

    return offsets, indices, counts


class DualTanimotoKernelEngine:
    def __init__(self, cache_dir: Path, prot_sim: np.ndarray):
        lig = np.load(cache_dir / "ligand_features.npz", allow_pickle=True)
        self.smiles = lig["smiles"]
        self.can_id = lig["can_id"].astype(np.int32)
        self.scaf_id = lig["scaf_id"].astype(np.int32)
        self.gscaf_id = lig["gscaf_id"].astype(np.int32)
        self.fp_ecfp4 = lig["fp_ecfp4"]
        self.fp_ecfp6 = lig["fp_ecfp6"]
        self.fp_fcfp4 = lig["fp_fcfp4"]
        self.fp_maccs = lig["fp_maccs"]
        self.mol_desc = lig["mol_desc"]

        self.pop_e4, self.pop_e6, self.pop_f4, self.pop_mc = precompute_popcounts(
            self.fp_ecfp4, self.fp_ecfp6, self.fp_fcfp4, self.fp_maccs
        )
        self.prot_sim = prot_sim.astype(np.float32)
        self.n_lig = len(self.smiles)
        self.n_prot = prot_sim.shape[0]
        self.max_can = int(self.can_id.max()) + 1
        self.max_scaf = int(self.scaf_id.max()) + 1
        self.max_gscaf = int(self.gscaf_id.max()) + 1

    def compute(
        self,
        tr_d_idx: np.ndarray,
        tr_t_idx: np.ndarray,
        tr_year: np.ndarray,
        tr_y: np.ndarray,
        tr_row_id: np.ndarray,
        q_d_idx: np.ndarray,
        q_t_idx: np.ndarray,
        q_year: np.ndarray,
        q_row_id: np.ndarray,
    ) -> np.ndarray:
        tr_d_idx = tr_d_idx.astype(np.int32)
        tr_t_idx = tr_t_idx.astype(np.int32)
        tr_year = tr_year.astype(np.int32)
        tr_y = tr_y.astype(np.float32)
        tr_row_id = tr_row_id.astype(np.int32)

        q_d_idx = q_d_idx.astype(np.int32)
        q_t_idx = q_t_idx.astype(np.int32)
        q_year = q_year.astype(np.int32)
        q_row_id = q_row_id.astype(np.int32)

        max_year_tr = int(tr_year.max())
        global_mean = float(tr_y.mean())

        t_offsets, t_indices = build_csr_buckets(tr_t_idx, self.n_prot)
        can_offsets, can_indices = build_csr_buckets(self.can_id[tr_d_idx], self.max_can)
        scaf_offsets, scaf_indices = build_csr_buckets(self.scaf_id[tr_d_idx], self.max_scaf)
        gscaf_offsets, gscaf_indices = build_csr_buckets(self.gscaf_id[tr_d_idx], self.max_gscaf)

        t_smooth_mean = np.full(self.n_prot, global_mean, dtype=np.float32)
        t_rec_mean = np.full(self.n_prot, global_mean, dtype=np.float32)
        t_std_vec = np.full(self.n_prot, 2.5, dtype=np.float32)
        for t in range(self.n_prot):
            s, e = t_offsets[t], t_offsets[t + 1]
            cnt = e - s
            if cnt > 0:
                rows = t_indices[s:e]
                ys = tr_y[rows]
                yrs = tr_year[rows]
                w_rec = np.exp(0.45 * (yrs - max_year_tr))
                m = float((ys.sum() + 5.0 * global_mean) / (cnt + 5.0))
                t_smooth_mean[t] = m
                t_rec_mean[t] = float(((ys * w_rec).sum() + 2.0 * global_mean) / (w_rec.sum() + 2.0))
                v = np.sum((ys - m) ** 2)
                t_std_vec[t] = float(np.sqrt((v + 5.0 * 6.25) / (cnt + 5.0)))

        has_tr = np.diff(t_offsets) > 0
        top_hom_targets = np.full((self.n_prot, 15), -1, dtype=np.int32)
        for t in range(self.n_prot):
            sims = self.prot_sim[t].copy()
            sims[~has_tr] = -1.0
            sims[t] = -1.0
            top_idx = np.argsort(sims)[::-1][:15]
            k_pos = 0
            for tp in top_idx:
                if sims[tp] > 0.02:
                    top_hom_targets[t, k_pos] = int(tp)
                    k_pos += 1

        tr_resids = tr_y - t_smooth_mean[tr_t_idx]
        order_d = np.argsort(tr_d_idx, kind="mergesort")
        sd = tr_d_idx[order_d]
        sy = tr_y[order_d]
        sres = tr_resids[order_d]
        st = tr_t_idx[order_d]
        uniq_d, idx_start, counts_d = np.unique(sd, return_index=True, return_counts=True)
        utr_d_idx = uniq_d.astype(np.int32)
        utr_mean_y = (np.add.reduceat(sy, idx_start) / counts_d).astype(np.float32)
        utr_mean_resid = (np.add.reduceat(sres, idx_start) / counts_d).astype(np.float32)
        utr_t_rep = st[idx_start].astype(np.int32)

        bit_offsets, bit_utr_indices, bit_doc_freq = _build_inverted_bit_index(utr_d_idx, self.fp_ecfp4)

        return _numba_compute_features(
            self.fp_ecfp4, self.fp_ecfp6, self.fp_fcfp4, self.fp_maccs,
            self.pop_e4, self.pop_e6, self.pop_f4, self.pop_mc,
            self.can_id, self.scaf_id, self.gscaf_id,
            self.prot_sim,
            tr_d_idx, tr_t_idx, tr_year, tr_y, tr_row_id,
            t_offsets, t_indices,
            can_offsets, can_indices,
            scaf_offsets, scaf_indices,
            gscaf_offsets, gscaf_indices,
            top_hom_targets,
            t_smooth_mean, t_rec_mean, t_std_vec, global_mean, max_year_tr,
            utr_d_idx, utr_mean_y, utr_mean_resid, utr_t_rep,
            bit_offsets, bit_utr_indices, bit_doc_freq,
            q_d_idx, q_t_idx, q_year, q_row_id,
        )
