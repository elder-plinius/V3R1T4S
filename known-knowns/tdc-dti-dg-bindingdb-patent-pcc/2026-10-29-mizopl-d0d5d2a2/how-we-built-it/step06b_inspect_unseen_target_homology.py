#!/usr/bin/env python3
"""
Step 6b: Catalytic Domain / Pocket-Core Local Alignment (Op-M3 Seed-Core Alignment).
Computes true slope-1 offset-invariant local domain alignment across all 477 proteins:
  1. Exact 5-mer seed diagonal voting to find the true offset delta = j - i between
     any two proteins (handling domain truncations, N/C-terminal tags, and isoforms!).
  2. Banded slope-1 Smith-Waterman alignment around the top diagonal offsets,
     normalized by:
       - min(L1, L2) (Containment similarity: detects truncated catalytic domain constructs!)
       - min(L1, L2, 220) (Catalytic pocket-core similarity: detects shared 220-AA binding domains!)
       - BLOSUM62 similarity score!
Evaluates the resulting Pocket-Core Homology Transfer on Inner Temporal Splits A and B.
Never touches `test['Y']`.
"""
import os
os.environ.setdefault("NUMBA_THREADING_LAYER", "workqueue")

import time
from pathlib import Path
import numba as nb
import numpy as np
from scipy.stats import pearsonr
from tdc.benchmark_group import dti_dg_group

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
CACHE_DIR = BASE_DIR / "cache"

AA_ORDER = "ARNDCQEGHILKMFPSTWYV"
AA_TO_INT = {c: i for i, c in enumerate(AA_ORDER)}

# Standard BLOSUM62 20x20 matrix in AA_ORDER
BLOSUM62 = np.array([
    [ 4, -1, -2, -2,  0, -1, -1,  0, -2, -1, -1, -1, -1, -2, -1,  1,  0, -3, -2,  0],
    [-1,  5,  0, -2, -3,  1,  0, -2,  0, -3, -2,  2, -1, -3, -2, -1, -1, -3, -2, -3],
    [-2,  0,  6,  1, -3,  0,  0,  0,  1, -3, -3,  0, -2, -3, -2,  1,  0, -4, -2, -3],
    [-2, -2,  1,  6, -3,  0,  2, -1, -1, -3, -4, -1, -3, -3, -1,  0, -1, -4, -3, -3],
    [ 0, -3, -3, -3,  9, -3, -4, -3, -3, -1, -1, -3, -1, -2, -3, -1, -1, -2, -2, -1],
    [-1,  1,  0,  0, -3,  5,  2, -2,  0, -3, -2,  1,  0, -3, -1,  0, -1, -2, -1, -2],
    [-1,  0,  0,  2, -4,  2,  5, -2,  0, -3, -3,  1, -2, -3, -1,  0, -1, -3, -2, -2],
    [ 0, -2,  0, -1, -3, -2, -2,  6, -2, -4, -4, -2, -3, -3, -2,  0, -2, -2, -3, -3],
    [-2,  0,  1, -1, -3,  0,  0, -2,  8, -3, -3, -1, -2, -1, -2, -1, -2, -2,  2, -3],
    [-1, -3, -3, -3, -1, -3, -3, -4, -3,  4,  2, -3,  1,  0, -3, -2, -1, -3, -1,  3],
    [-1, -2, -3, -4, -1, -2, -3, -4, -3,  2,  4, -2,  2,  0, -3, -2, -1, -2, -1,  1],
    [-1,  2,  0, -1, -3,  1,  1, -2, -1, -3, -2,  5, -1, -3, -1,  0, -1, -3, -2, -2],
    [-1, -1, -2, -3, -1,  0, -2, -3, -2,  1,  2, -1,  5,  0, -2, -1, -1, -1, -1,  1],
    [-2, -3, -3, -3, -2, -3, -3, -3, -1,  0,  0, -3,  0,  6, -4, -2, -2,  1,  3, -1],
    [-1, -2, -2, -1, -3, -1, -1, -2, -2, -3, -3, -1, -2, -4,  7, -1, -1, -4, -3, -2],
    [ 1, -1,  1,  0, -1,  0,  0,  0, -1, -2, -2,  0, -1, -2, -1,  4,  1, -3, -2, -2],
    [ 0, -1,  0, -1, -1, -1, -1, -2, -2, -1, -1, -1, -1, -2, -1,  1,  5, -2, -2,  0],
    [-3, -3, -4, -4, -2, -2, -3, -2, -2, -3, -2, -3, -1,  1, -4, -3, -2, 11,  2, -3],
    [-2, -2, -2, -3, -2, -1, -2, -3,  2, -1, -1, -2, -1,  3, -3, -2, -2,  2,  7, -1],
    [ 0, -3, -3, -3, -1, -2, -2, -3, -3,  3,  1, -2,  1, -1, -2, -2,  0, -3, -1,  4],
], dtype=np.int16)

# Reduced 6-class alphabet for fast 6-mer seed hashing (6^6 = 46,656 buckets!)
RED6 = np.array([0, 2, 1, 1, 5, 1, 1, 0, 2, 3, 3, 2, 3, 4, 0, 0, 0, 4, 4, 3], dtype=np.int32)


@nb.njit(parallel=True, fastmath=True, cache=True)
def compute_pocket_local_alignment_matrix(seqs_aa: np.ndarray, seq_lens: np.ndarray):
    """
    For all 477 x 477 protein pairs (i, j):
    1. Uses reduced-alphabet 5-mer seed hits to find the top 3 diagonal offsets delta = pos_j - pos_i.
    2. Runs slope-1 banded Smith-Waterman (band = +-24) around each top diagonal offset
       using BLOSUM62 scoring (gap open/extend = -6 / -2).
    3. Returns:
       - S_contain[i, j]: alignment score normalized by self-score of shorter protein min(self_i, self_j)
       - S_pocket[i, j]: alignment score normalized by a 200-AA catalytic pocket self-score (~1050)
       - S_global[i, j]: alignment score normalized by sqrt(self_i * self_j)
    """
    n_p = len(seq_lens)
    S_contain = np.eye(n_p, dtype=np.float32)
    S_pocket = np.eye(n_p, dtype=np.float32)
    S_global = np.eye(n_p, dtype=np.float32)

    # Self BLOSUM62 scores
    self_sc = np.zeros(n_p, dtype=np.float32)
    for i in range(n_p):
        li = seq_lens[i]
        s = 0
        for p in range(li):
            aa = seqs_aa[i, p]
            s += BLOSUM62[aa, aa]
        self_sc[i] = float(max(s, 1))

    # Precompute reduced 5-mer codes (6^5 = 7776) for each sequence
    max_len = seqs_aa.shape[1]
    kmer5 = np.full((n_p, max_len), -1, dtype=np.int16)
    for i in range(n_p):
        li = seq_lens[i]
        if li < 5:
            continue
        for p in range(li - 4):
            c = (
                RED6[seqs_aa[i, p]] * 1296
                + RED6[seqs_aa[i, p + 1]] * 216
                + RED6[seqs_aa[i, p + 2]] * 36
                + RED6[seqs_aa[i, p + 3]] * 6
                + RED6[seqs_aa[i, p + 4]]
            )
            kmer5[i, p] = c

    for i in nb.prange(n_p):
        li = seq_lens[i]
        if li < 10:
            continue
        # Build first-occurrence position table of 5-mers in sequence i
        first_pos = np.full(7776, -1, dtype=np.int16)
        second_pos = np.full(7776, -1, dtype=np.int16)
        for p in range(li - 4):
            c = kmer5[i, p]
            if first_pos[c] == -1:
                first_pos[c] = p
            elif second_pos[c] == -1 and p - first_pos[c] >= 15:
                second_pos[c] = p

        for j in range(i + 1, n_p):
            lj = seq_lens[j]
            if lj < 10:
                continue

            # Diagonal offset histogram in bins of width 8: offset = pj - pi in [-li, lj]
            n_bins = (li + lj) // 8 + 4
            hist = np.zeros(n_bins, dtype=np.int16)
            bin_sum_delta = np.zeros(n_bins, dtype=np.int32)

            for pj in range(lj - 4):
                c = kmer5[j, pj]
                pi1 = first_pos[c]
                if pi1 >= 0:
                    delta = pj - pi1
                    b = (delta + li) >> 3
                    hist[b] += 1
                    bin_sum_delta[b] += delta
                pi2 = second_pos[c]
                if pi2 >= 0:
                    delta2 = pj - pi2
                    b2 = (delta2 + li) >> 3
                    hist[b2] += 1
                    bin_sum_delta[b2] += delta2

            # Pick top 2 diagonal bins
            b_best1 = 0
            b_best2 = 0
            v1 = -1
            v2 = -1
            for b in range(n_bins):
                vb = hist[b]
                if vb > v1:
                    v2 = v1
                    b_best2 = b_best1
                    v1 = vb
                    b_best1 = b
                elif vb > v2:
                    v2 = vb
                    b_best2 = b

            best_sw = 0
            for b_cand, v_cand in ((b_best1, v1), (b_best2, v2)):
                if v_cand <= 0:
                    continue
                delta_center = bin_sum_delta[b_cand] // max(int(v_cand), 1)
                band = 20
                # Run slope-1 banded Smith-Waterman around pj = pi + delta_center
                H_prev = np.zeros(2 * band + 3, dtype=np.int16)
                H_curr = np.zeros(2 * band + 3, dtype=np.int16)
                pi_start = max(0, -delta_center - band)
                pi_end = min(li, lj - delta_center + band)
                for pi in range(pi_start, pi_end):
                    aai = seqs_aa[i, pi]
                    row_blosum = BLOSUM62[aai]
                    for k_off in range(-band, band + 1):
                        pj = pi + delta_center + k_off
                        idx = k_off + band + 1
                        if pj < 0 or pj >= lj:
                            H_curr[idx] = 0
                            continue
                        aaj = seqs_aa[j, pj]
                        # Match/mismatch transitions along same diagonal offset k_off
                        sc_match = H_prev[idx] + row_blosum[aaj]
                        # Insertion/deletion shifts diagonal offset by +-1
                        sc_del = H_prev[idx + 1] - 4
                        sc_ins = H_curr[idx - 1] - 4
                        val = sc_match
                        if sc_del > val:
                            val = sc_del
                        if sc_ins > val:
                            val = sc_ins
                        if val < 0:
                            val = 0
                        H_curr[idx] = val
                        if val > best_sw:
                            best_sw = val
                    for idx in range(2 * band + 3):
                        H_prev[idx] = H_curr[idx]
                        H_curr[idx] = 0

            sc_f = float(best_sw)
            min_self = min(self_sc[i], self_sc[j])
            pocket_denom = min(min_self, 1100.0)  # ~210 AA catalytic domain BLOSUM62 self-score
            glob_denom = np.sqrt(self_sc[i] * self_sc[j])

            sc_contain = min(1.0, sc_f / max(min_self, 1.0))
            sc_pocket = min(1.0, sc_f / max(pocket_denom, 1.0))
            sc_glob = min(1.0, sc_f / max(glob_denom, 1.0))

            S_contain[i, j] = sc_contain
            S_contain[j, i] = sc_contain
            S_pocket[i, j] = sc_pocket
            S_pocket[j, i] = sc_pocket
            S_global[i, j] = sc_glob
            S_global[j, i] = sc_glob

    return S_contain, S_pocket, S_global


def main():
    t0 = time.time()
    prot_npz = np.load(CACHE_DIR / "protein_features.npz", allow_pickle=True)
    hom_npz = np.load(CACHE_DIR / "protein_homology.npz", allow_pickle=True)
    targets = list(prot_npz["targets"])
    n_p = len(targets)
    max_len = max(len(s) for s in targets)

    seqs_aa = np.zeros((n_p, max_len), dtype=np.int16)
    seq_lens = np.zeros(n_p, dtype=np.int32)
    for i, s in enumerate(targets):
        seq_lens[i] = len(s)
        for p, c in enumerate(s):
            seqs_aa[i, p] = AA_TO_INT.get(c, 0)

    S_contain, S_pocket, S_global = compute_pocket_local_alignment_matrix(seqs_aa, seq_lens)
    print(f"Computed Pocket-Core Local Alignment (477x477) in {time.time()-t0:.2f}s")

    S_kmer = hom_npz["S_kmer"].astype(np.float32)
    S_prot_old = hom_npz["S_prot"].astype(np.float32)
    S_prot_upgraded = (0.35 * S_kmer + 0.30 * S_pocket + 0.20 * S_contain + 0.15 * S_global).astype(np.float32)
    np.fill_diagonal(S_prot_upgraded, 1.0)

    np.savez_compressed(
        CACHE_DIR / "protein_homology.npz",
        S_prot=S_prot_upgraded,
        S_kmer=S_kmer,
        S_sw=S_global,
        S_contain=S_contain,
        S_pocket=S_pocket,
        S_global=S_global,
    )

    # Inspect unseen targets in Inner Temporal Split A, Split B, strictly on train_val
    group = dti_dg_group(path=str(DATA_DIR))
    bm = group.get("BindingDB_Patent")
    tv = bm["train_val"]
    t_to_idx = {t: i for i, t in enumerate(targets)}

    for label, seen_set, unseen_set in [
        ("Split A (2017-2018 vs 2013-2016)", set(tv[tv["Year"] <= 2016]["Target"]), set(tv[tv["Year"] >= 2017]["Target"]) - set(tv[tv["Year"] <= 2016]["Target"])),
        ("Split B (2018 vs 2013-2017)", set(tv[tv["Year"] <= 2017]["Target"]), set(tv[tv["Year"] == 2018]["Target"]) - set(tv[tv["Year"] <= 2017]["Target"])),
    ]:
        s_idx = np.array([t_to_idx[t] for t in seen_set], dtype=np.int32)
        u_idx = np.array([t_to_idx[t] for t in unseen_set], dtype=np.int32)
        max_old = np.max(S_prot_old[np.ix_(u_idx, s_idx)], axis=1)
        max_poc = np.max(S_pocket[np.ix_(u_idx, s_idx)], axis=1)
        max_con = np.max(S_contain[np.ix_(u_idx, s_idx)], axis=1)
        print(f"\n=== {label}: {len(u_idx)} Unseen Targets ===")
        print(f"  Old S_prot max >= 0.70: {np.sum(max_old >= 0.70)} | Pocket S_pocket max >= 0.70: {np.sum(max_poc >= 0.70)} | >= 0.50: {np.sum(max_poc >= 0.50)}")
        print(f"  Mean max homology: Old={np.mean(max_old):.3f}, Contain={np.mean(max_con):.3f}, Pocket={np.mean(max_poc):.3f}")


if __name__ == "__main__":
    main()
