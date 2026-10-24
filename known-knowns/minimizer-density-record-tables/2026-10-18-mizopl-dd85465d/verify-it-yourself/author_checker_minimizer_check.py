#!/usr/bin/env python3
"""
Standalone exact & empirical DNA density verifier for minimizer-density-record-tables (w=12, k=3).

Verifies:
1. Binary .gm format and storage cost (72 bytes: 8-byte size_t header = 8, followed by 8 uint64_t ranks).
2. Exact expected DNA density via GreedyMini's prob_gc_dna / density_expected_dna algorithm
   (GreedyMini/code/density_and_gc.cpp lines 253-480).
3. Independent exact 4-ary de Bruijn transfer-matrix DP over all 4^15 = 1,073,741,824 DNA windows of length w+k = 15.
4. Empirical DNA density via 10-minimizers's GreedyMiniScheme + random_density_function_dna_includes_tiebreaking
   (10-minimizers/density-measurement-and-plots/greedymini_density.ipynb).
5. Strict improvement by >= 0.5% relative over all methods in OrensteinLab/10-minimizers and OrensteinLab/GreedyMini.
"""

import sys
import os
import struct
import hashlib
import csv
import numpy as np


def load_vector_from_file(filename):
    with open(filename, "rb") as file:
        size_data = file.read(struct.calcsize("P"))
        size = struct.unpack("P", size_data)[0]
        vector_data = file.read(size * struct.calcsize("Q"))
        vector = struct.unpack(f"{size}Q", vector_data)
        return list(vector)


def sha256_file(filename):
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


# Method 1: Exact GreedyMini prob_gc_dna (via SOS-DP exact count of unruined secondary sequences)
def exact_greedymini_prob_gc_dna(w, k, order):
    total_seq = 1 << (w + k)
    seqs = np.arange(total_seq, dtype=np.uint32)
    mask = (1 << k) - 1
    first = seqs >> w
    last = seqs & mask
    pref_ruin = np.zeros(total_seq, dtype=np.uint16)
    suff_ruin = np.zeros(total_seq, dtype=np.uint16)
    for j in range(1, w):
        km_j = (seqs >> (w - j)) & mask
        pref_ruin |= ((km_j < first).astype(np.uint16) << j)
        suff_ruin |= ((km_j <= last).astype(np.uint16) << j)
    both_ruin = pref_ruin & suff_ruin

    ord_arr = np.array(order, dtype=np.int64)
    kmers = np.zeros((total_seq, w + 1), dtype=np.uint16)
    for j in range(w + 1):
        kmers[:, j] = (seqs >> (w - j)) & mask
    w_ranks = ord_arr[kmers]
    min_r = w_ranks.min(axis=1, keepdims=True)
    is_min = (w_ranks == min_r)

    first_min = is_min[:, 0]
    last_min = is_min[:, w]
    mid_min = is_min[:, 1:w].any(axis=1)

    pure_gc = int(np.sum((first_min | last_min) & (~mid_min)))
    spec_mask = (first_min | last_min) & mid_min
    wt = np.zeros(int(np.sum(spec_mask)), dtype=np.uint32)
    spec_is_min = is_min[spec_mask]
    for j in range(w + 1):
        wt |= (spec_is_min[:, j].astype(np.uint32) << j)

    unique_wt, counts = np.unique(wt, return_counts=True)
    spec_expected_gc = 0.0
    for u_wt, cnt in zip(unique_wt, counts):
        has_first = (u_wt & 1) != 0
        has_last = (u_wt & (1 << w)) != 0
        if has_first and has_last:
            not_ruined = int(np.sum((both_ruin & u_wt) == 0))
        elif has_first:
            not_ruined = int(np.sum((pref_ruin & u_wt) == 0))
        else:
            not_ruined = int(np.sum((suff_ruin & u_wt) == 0))
        spec_expected_gc += (not_ruined / float(total_seq)) * int(cnt)

    total_gc = (pure_gc << (w + k)) + int(spec_expected_gc * (1 << (w + k)))
    density = total_gc / float(1 << (2 * (w + k)))
    return total_gc, density


# Method 2: Independent exact 4-ary de Bruijn transfer-matrix DP over all 4^(w+k) DNA windows
def gm_to_4ary_rank(order_bin, k):
    N = 1 << (2 * k)
    keys = []
    for km in range(N):
        bin_km = 0
        for i in range(k):
            nuc = (km >> (2 * (k - 1 - i))) & 0b11
            bin_km = (bin_km << 1) | ((nuc >> 1) & 1)
        keys.append((order_bin[bin_km] << (2 * k)) + km)
    order_idx = sorted(range(N), key=lambda x: keys[x])
    rank_4ary = [0] * N
    for r, idx in enumerate(order_idx):
        rank_4ary[idx] = r
    return rank_4ary


def exact_4ary_debruijn_dp(w, k, rank_4ary):
    N = 1 << (2 * k)
    mask = N - 1
    r_of = np.array(rank_4ary, dtype=np.int64)
    assert len(np.unique(r_of)) == N

    fwd = np.zeros((N, 4), dtype=np.int32)
    bwd = np.zeros((N, 4), dtype=np.int32)
    for u in range(N):
        for b in range(4):
            fwd[u, b] = ((u << 2) & mask) | b
            bwd[u, b] = (u >> 2) | (b << (2 * (k - 1)))

    total_pref_gc = 0
    total_suff_gc = 0
    for u0 in range(N):
        r0 = r_of[u0]
        allowed_pref = (r_of >= r0)
        dp = np.zeros(N, dtype=np.int64)
        dp[u0] = 1
        for _ in range(w):
            nxt = dp[bwd[:, 0]] + dp[bwd[:, 1]] + dp[bwd[:, 2]] + dp[bwd[:, 3]]
            dp = np.where(allowed_pref, nxt, 0)
        total_pref_gc += int(np.sum(dp))

        allowed_suff = (r_of > r0)
        dp = np.zeros(N, dtype=np.int64)
        dp[u0] = 1
        for _ in range(w):
            nxt = dp[fwd[:, 0]] + dp[fwd[:, 1]] + dp[fwd[:, 2]] + dp[fwd[:, 3]]
            dp = np.where(allowed_suff, nxt, 0)
        total_suff_gc += int(np.sum(dp))

    total_gc = total_pref_gc + total_suff_gc
    return total_gc, total_gc / float(1 << (2 * (w + k)))


# Method 3: 10-minimizers empirical sampling function (verbatim logic from greedymini_density.ipynb)
def hash_kmer(k, kmer, seed):
    kmer_seed_sum = kmer + seed
    kmer_as_bytes = kmer_seed_sum.to_bytes(2 * k, byteorder="big")
    hashed_kmer = hashlib.sha256(kmer_as_bytes).digest()
    return int.from_bytes(hashed_kmer, byteorder="big")


def get_kmer_id_dna(k, kmer, seed):
    hashed_kmer = hash_kmer(k, kmer, seed) % (4 ** k)
    return (4 ** k) * hashed_kmer + kmer


def sample_10minimizers_density(w, k, order_bin, n_samples=1_000_000, seed=0):
    k_mask = (1 << (2 * k)) - 1
    total_nucleotides = n_samples + w + k - 1
    rng = np.random.default_rng(seed)
    nucleotides = rng.integers(0, 4, size=total_nucleotides, dtype=np.uint32)

    shift_8k = 8 * k
    lut_rank = []
    for km in range(1 << (2 * k)):
        bin_kmer = 0
        for i in range(k):
            nuc = (km >> (2 * (k - 1 - i))) & 0b11
            bit = (nuc >> 1) & 1
            bin_kmer = (bin_kmer << 1) | bit
        fn_val = (order_bin[bin_kmer] << (2 * k)) + km
        lut_rank.append((fn_val << shift_8k) + get_kmer_id_dna(k, km, seed))

    n_kmers = total_nucleotides - k + 1
    kmers = []
    kmer = 0
    for pos in range(k):
        kmer = (kmer << 2) | int(nucleotides[pos])
    kmers.append(kmer & k_mask)
    for i in range(1, n_kmers):
        kmer = ((kmer << 2) | int(nucleotides[i + k - 1])) & k_mask
        kmers.append(kmer)
    ranks = [lut_rank[km] for km in kmers]

    sampled_positions = 0
    last_sampled = -1
    for t in range(n_samples):
        window = ranks[t : t + w]
        min_pos = t + window.index(min(window))
        if min_pos != last_sampled:
            sampled_positions += 1
            last_sampled = min_pos

    return sampled_positions / n_kmers


def main():
    claim_dir = os.path.dirname(os.path.abspath(__file__))
    imp_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(claim_dir, "w12_k3_improved.gm")
    pub_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(claim_dir, "published_w12_k3.gm")
    csv_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(claim_dir, "k_extension_k16_w12.csv")

    w, k = 12, 3
    imp_order = load_vector_from_file(imp_path)
    pub_order = load_vector_from_file(pub_path)

    imp_bytes = os.path.getsize(imp_path)
    pub_bytes = os.path.getsize(pub_path)
    assert imp_bytes == 72 and pub_bytes == 72
    assert len(imp_order) == 8 and len(pub_order) == 8
    assert sorted(imp_order) == list(range(8)), "w12_k3_improved.gm must be a strict permutation of 0..7"

    imp_csv_path = os.path.splitext(imp_path)[0] + ".csv"
    if os.path.exists(imp_csv_path):
        csv_ranks = {}
        with open(imp_csv_path, "r") as cf:
            reader = csv.DictReader(cf)
            for row in reader:
                km_str = row["k-mer"].strip()
                assert len(km_str) == 3 and all(c in "01" for c in km_str), f"Invalid k-mer in CSV: {km_str}"
                km_idx = int(km_str, 2)
                csv_ranks[km_idx] = int(row["rank"].strip())
        assert len(csv_ranks) == 8, f"CSV must have 8 rows, got {len(csv_ranks)}"
        csv_order = [csv_ranks[i] for i in range(8)]
        assert csv_order == imp_order, f"CSV order {csv_order} != .gm order {imp_order}"

    print(f"w12_k3_improved.gm sha256  : {sha256_file(imp_path)} ({imp_bytes} bytes)")
    print(f"published_w12_k3.gm sha256 : {sha256_file(pub_path)} ({pub_bytes} bytes)")
    print(f"Improved order (8 uint64s) : {imp_order}")
    print(f"Published order (8 uint64s): {pub_order}")

    imp_gc_1, imp_den_1 = exact_greedymini_prob_gc_dna(w, k, imp_order)
    pub_gc_1, pub_den_1 = exact_greedymini_prob_gc_dna(w, k, pub_order)

    imp_gc_2, imp_den_2 = exact_4ary_debruijn_dp(w, k, gm_to_4ary_rank(imp_order, k))
    assert imp_gc_1 == imp_gc_2, f"Mismatch between Method 1 ({imp_gc_1}) and Method 2 ({imp_gc_2})"

    print("\n--- Exact Expected DNA Density (over all 4^15 = 1,073,741,824 DNA windows) ---")
    print(f"Published w12_k3.gm (prob_gc_dna)        : {pub_gc_1} / 2^30 = {pub_den_1:.10f}")
    print(f"Improved  w12_k3_improved.gm (prob_gc_dna): {imp_gc_1} / 2^30 = {imp_den_1:.10f}")
    print(f"Improved  w12_k3_improved.gm (4-ary DP)   : {imp_gc_2} / 2^30 = {imp_den_2:.10f}")

    table_vals = {}
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            val_str = row["3"].strip()
            if val_str and val_str.lower() != "nan":
                table_vals[row["method"].strip()] = float(val_str)

    min_table_method = min(table_vals, key=table_vals.get)
    min_table_val = table_vals[min_table_method]
    best_known = min(pub_den_1, min_table_val)
    rel_improvement = (best_known - imp_den_1) / best_known * 100.0
    rel_vs_gm = (pub_den_1 - imp_den_1) / pub_den_1 * 100.0

    print("\n--- Comparison vs All Published Methods at (w=12, k=3) ---")
    for m, v in sorted(table_vals.items(), key=lambda x: x[1]):
        rel_m = (v - imp_den_1) / v * 100.0
        print(f"  {m:20s}: {v:.9f}  (our order improves by -{rel_m:.4f}%)")
    print(f"Smallest published value: {best_known:.10f} ({min_table_method})")
    print(f"Published GreedyMini .gm: {pub_den_1:.10f} (-{rel_vs_gm:.6f}%)")
    print(f"Our exact DNA density   : {imp_den_1:.10f}")
    print(f"Relative reduction vs best: -{rel_improvement:.6f}% (required >= 0.500000%)")

    emp_pub = sample_10minimizers_density(w, k, pub_order, n_samples=1_000_000, seed=0)
    emp_imp = sample_10minimizers_density(w, k, imp_order, n_samples=1_000_000, seed=0)
    emp_rel = (emp_pub - emp_imp) / emp_pub * 100.0
    print("\n--- Empirical Check (10-minimizers random_density_function_dna_includes_tiebreaking, N=1,000,000, seed=0) ---")
    print(f"  Published w12_k3.gm     : {emp_pub:.6f}")
    print(f"  Improved w12_k3_improved: {emp_imp:.6f} (-{emp_rel:.4f}%)")

    assert imp_gc_1 == 146639789
    assert pub_gc_1 == 149082035
    assert rel_improvement >= 0.5, f"Relative improvement {rel_improvement}% < 0.5%"
    print("\nVERIFICATION: PASS")
    print("PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
        print("FAIL")
        sys.exit(1)
