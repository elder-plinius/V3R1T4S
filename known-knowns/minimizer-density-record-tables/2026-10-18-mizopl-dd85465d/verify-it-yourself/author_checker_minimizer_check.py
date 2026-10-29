#!/usr/bin/env python3
"""
Standalone exact DNA density verifier for minimizer-density-record-tables (w=12, k=3).

Upstream references (pinned commits, not copied in this package):
- OrensteinLab/GreedyMini (Golan, Tziony, Kraus, Orenstein & Shur, Bioinformatics 2025):
  https://github.com/OrensteinLab/GreedyMini/blob/a67eb90dc278ea78111a76d5813cf2ac7662b0ae/code/density_and_gc.cpp
- OrensteinLab/10-minimizers (Shur, Tziony & Orenstein, WABI 2026):
  https://github.com/OrensteinLab/10-minimizers/blob/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/greedymini_density.ipynb

Verifies:
1. Binary .gm format and storage cost (72 bytes: 8-byte size_t header = 8, followed by 8 uint64_t ranks),
   plus exact agreement with companion CSV table object/w12_k3_improved.csv.
2. SHA-256 hashes of object/w12_k3_improved.gm, fetched w12_k3.gm, and fetched k_extension_k16_w12.csv.
3. Exact expected DNA density via high-bit / low-bit bit-plane enumeration over all 4^15 = 1,073,741,824 DNA contexts.
4. Independent exact 4-ary de Bruijn transfer-matrix DP over all 4^15 = 1,073,741,824 DNA contexts of length w+k = 15.
5. Strict improvement by >= 0.5% relative over all methods in k_extension_k16_w12.csv and w12_k3.gm.
"""

import sys
import os
import struct
import hashlib
import csv
import numpy as np

EXPECTED_IMP_SHA256 = "dd85465d87f23d688778ff35175ed19e4c9f00e71cad28b535d7a9d73294f302"
EXPECTED_PUB_SHA256 = "c592519b57ad8104860b7e1559b28c2d37ef329db82298b151a65e056ce27f1d"
EXPECTED_CSV_SHA256 = "88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa"


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


# Method 1: Exact high-bit / low-bit bit-plane enumeration of gamechanger DNA contexts
def exact_bitplane_prob_gc_dna(w, k, order):
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
    spec_gc_windows = 0
    for u_wt, cnt in zip(unique_wt, counts):
        has_first = (u_wt & 1) != 0
        has_last = (u_wt & (1 << w)) != 0
        if has_first and has_last:
            not_ruined = int(np.sum((both_ruin & u_wt) == 0))
        elif has_first:
            not_ruined = int(np.sum((pref_ruin & u_wt) == 0))
        else:
            not_ruined = int(np.sum((suff_ruin & u_wt) == 0))
        spec_gc_windows += not_ruined * int(cnt)

    total_gc = (pure_gc << (w + k)) + spec_gc_windows
    density = total_gc / float(1 << (2 * (w + k)))
    return total_gc, density


# Method 2: Independent exact 4-ary de Bruijn transfer-matrix DP over all 4^(w+k) DNA windows
def gm_to_4ary_rank(order_bin, k):
    N = 1 << (2 * k)
    keys = []
    for km in range(N):
        bin_km = 0
        low_km = 0
        for i in range(k):
            nuc = (km >> (2 * (k - 1 - i))) & 0b11
            bin_km = (bin_km << 1) | ((nuc >> 1) & 1)
            low_km = (low_km << 1) | (nuc & 1)
        keys.append((order_bin[bin_km], low_km))
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


def main():
    claim_dir = os.path.dirname(os.path.abspath(__file__))
    imp_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(claim_dir, "w12_k3_improved.gm")
    pub_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(claim_dir, "published_w12_k3.gm")
    csv_path = sys.argv[3] if len(sys.argv) > 3 else os.path.join(claim_dir, "k_extension_k16_w12.csv")

    w, k = 12, 3
    imp_sha = sha256_file(imp_path)
    pub_sha = sha256_file(pub_path)
    csv_sha = sha256_file(csv_path)
    assert imp_sha == EXPECTED_IMP_SHA256, f"w12_k3_improved.gm sha256 mismatch: {imp_sha}"
    assert pub_sha == EXPECTED_PUB_SHA256, f"published_w12_k3.gm sha256 mismatch: {pub_sha}"
    assert csv_sha == EXPECTED_CSV_SHA256, f"k_extension_k16_w12.csv sha256 mismatch: {csv_sha}"

    imp_order = load_vector_from_file(imp_path)
    pub_order = load_vector_from_file(pub_path)

    imp_bytes = os.path.getsize(imp_path)
    pub_bytes = os.path.getsize(pub_path)
    csv_bytes = os.path.getsize(csv_path)
    assert imp_bytes == 72 and pub_bytes == 72 and csv_bytes == 1644
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

    print(f"w12_k3_improved.gm sha256  : {imp_sha} ({imp_bytes} bytes)")
    print(f"published_w12_k3.gm sha256 : {pub_sha} ({pub_bytes} bytes)")
    print(f"k_extension_k16_w12.csv sha: {csv_sha} ({csv_bytes} bytes)")
    print(f"Improved order (8 uint64s) : {imp_order}")
    print(f"Published order (8 uint64s): {pub_order}")

    imp_gc_1, imp_den_1 = exact_bitplane_prob_gc_dna(w, k, imp_order)
    pub_gc_1, pub_den_1 = exact_bitplane_prob_gc_dna(w, k, pub_order)

    imp_gc_2, imp_den_2 = exact_4ary_debruijn_dp(w, k, gm_to_4ary_rank(imp_order, k))
    assert imp_gc_1 == imp_gc_2, f"Mismatch between Method 1 ({imp_gc_1}) and Method 2 ({imp_gc_2})"

    print("\n--- Exact Expected DNA Density (over all 4^15 = 1,073,741,824 DNA windows) ---")
    print(f"Published w12_k3.gm (bit-plane exact)        : {pub_gc_1} / 2^30 = {pub_den_1:.10f}")
    print(f"Improved  w12_k3_improved.gm (bit-plane)     : {imp_gc_1} / 2^30 = {imp_den_1:.10f}")
    print(f"Improved  w12_k3_improved.gm (4-ary DP)      : {imp_gc_2} / 2^30 = {imp_den_2:.10f}")

    table_vals = {}
    with open(csv_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            val_str = row["3"].strip()
            if val_str and val_str.lower() != "nan":
                table_vals[row["method"].strip()] = float(val_str)

    min_table_method = min(table_vals, key=table_vals.get)
    min_table_val = table_vals[min_table_method]
    smallest_listed = min(pub_den_1, min_table_val)
    rel_improvement = (smallest_listed - imp_den_1) / smallest_listed * 100.0
    rel_vs_gm = (pub_den_1 - imp_den_1) / pub_den_1 * 100.0

    print("\n--- Comparison vs All Listed Methods at (w=12, k=3) ---")
    for m, v in sorted(table_vals.items(), key=lambda x: x[1]):
        rel_m = (v - imp_den_1) / v * 100.0
        print(f"  {m:20s}: {v:.9f}  (our order improves by -{rel_m:.4f}%)")
    print(f"Smallest listed value   : {smallest_listed:.10f} ({min_table_method})")
    print(f"Published GreedyMini .gm: {pub_den_1:.10f} (-{rel_vs_gm:.6f}%)")
    print(f"Our exact DNA density   : {imp_den_1:.10f}")
    print(f"Relative reduction vs smallest listed: -{rel_improvement:.6f}% (required >= 0.500000%)")

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
