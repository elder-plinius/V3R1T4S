#!/usr/bin/env python3
"""
Standalone exact DNA density verifier for minimizer-density-record-tables at (w=12, k=4).

Upstream references (pinned commits, fetched live by run_checks.sh and not copied in this package):
- OrensteinLab/Minimizers (Golan, Tziony, Kraus, Orenstein & Shur, Bioinformatics 2025):
  https://github.com/OrensteinLab/Minimizers/blob/7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46/lowest-density/binary/individual-orders/ranks/k4-w12.txt
  https://github.com/OrensteinLab/Minimizers/blob/7b9430fce07a1fcf6b0fe023e9c7c135d6a5bf46/lowest-density/binary/best-orders.csv
- OrensteinLab/GreedyMini (Golan, Tziony, Kraus, Orenstein & Shur, Bioinformatics 2025):
  https://github.com/OrensteinLab/GreedyMini/blob/a67eb90dc278ea78111a76d5813cf2ac7662b0ae/code/density_and_gc.cpp
- OrensteinLab/10-minimizers (Shur, Tziony & Orenstein, WABI 2026):
  https://github.com/OrensteinLab/10-minimizers/blob/916daebd399d15d061e2fd437326aee5cf0e7292/density-measurement-and-plots/greedymini_density.ipynb

Verifies:
1. Binary .gm format and storage cost of object/w12_k4_4ary.gm (2,056 bytes: 8-byte size_t header = 256,
   followed by 256 uint64_t ranks in 0..255), plus exact element-by-element agreement with companion CSV
   rank table object/w12_k4_4ary.csv (4,518 bytes).
2. SHA-256 hashes of object/w12_k4_4ary.gm, object/w12_k4_4ary.csv, fetched k4-w12.txt, fetched w12_k4.gm,
   and fetched k_extension_k16_w12.csv.
3. Exact expected DNA density over all 4^16 = 4,294,967,296 DNA contexts via two independent exact 4-ary
   de Bruijn transfer-matrix DP algorithms (active-set forward/backward de Bruijn DP and full matrix-power DP),
   plus exact bit-plane enumeration for the published binary-projected baselines.
4. Strict improvement by -0.7085% relative over OrensteinLab/Minimizers k4-w12.txt (574,313,157 / 2^32 =
   0.1337177020) and by -2.4076% relative over OrensteinLab/10-minimizers w12_k4.gm (584,312,429 / 2^32 =
   0.1360458389), exceeding the >= 0.5% relative threshold (<= 0.1330491135).
"""

import sys
import os
import ast
import csv
import struct
import hashlib
import numpy as np

EXPECTED_IMP_GM_SHA256 = "956170573df55e04f43e55c20d6bba0b134c9b8054a92f995428dc9df4410ddb"
EXPECTED_IMP_CSV_SHA256 = "72557c44cc3c4b10d4735faeee9d6745f40872674c54118a311e258f775431d1"
EXPECTED_MIN_TXT_SHA256 = "9a8f7447e569399a594588e695a963da59078b34cf4aac23a6fd3d998d06d877"
EXPECTED_PUB_GM_SHA256 = "7c04487e1489e8d37302230424f32522f3c9af537680c6319009fb49ef180131"
EXPECTED_CSV_SHA256 = "88c4f8fcd0ea6d4308f4e1fc716bb901ea78d3c6112b7e70d4af42bb631bf2fa"


def sha256_file(filename):
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def load_gm_vector(filename):
    raw = open(filename, "rb").read()
    if len(raw) < 8:
        raise ValueError(f"File too short: {filename}")
    size = struct.unpack("<Q", raw[:8])[0]
    if len(raw) != 8 + 8 * size:
        raise ValueError(f"Byte length {len(raw)} does not match header size {size} in {filename}")
    return list(struct.unpack(f"<{size}Q", raw[8:]))


def load_4ary_csv(filename):
    bases = "ACGT"
    ranks = [None] * 256
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            b_str = row["k-mer"].strip()
            dna_str = row["dna_4mer"].strip()
            r_val = int(row["rank"].strip())
            if len(b_str) != 8 or any(c not in "01" for c in b_str):
                raise ValueError(f"Invalid 8-bit k-mer string: {b_str}")
            idx = int(b_str, 2)
            expected_dna = "".join(bases[(idx >> (2 * (3 - j))) & 3] for j in range(4))
            if dna_str != expected_dna:
                raise ValueError(f"Mismatch between k-mer {b_str} and dna_4mer {dna_str}")
            if idx != count:
                raise ValueError(f"Row order corrupted at index {idx} (expected {count})")
            ranks[idx] = r_val
            count += 1
    if count != 256 or any(v is None for v in ranks):
        raise ValueError(f"CSV {filename} does not contain all 256 4-mers")
    if sorted(ranks) != list(range(256)):
        raise ValueError(f"CSV {filename} ranks are not a strict permutation of 0..255")
    return ranks


def gm_bin_to_4ary_rank(order_bin, k):
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


# Method 1: Active-set forward prefix / backward suffix 4-ary de Bruijn DP
def exact_4ary_debruijn_dp_active(w, k, rank_4ary):
    N = 1 << (2 * k)
    mask = N - 1
    r_of = np.array(rank_4ary, dtype=np.int64)
    if len(r_of) != N or sorted(rank_4ary) != list(range(N)):
        raise ValueError("rank_4ary must be a strict permutation of 0..4^k-1")

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
            if not np.any(dp):
                break
        total_pref_gc += int(np.sum(dp))

        allowed_suff = (r_of > r0)
        dp = np.zeros(N, dtype=np.int64)
        dp[u0] = 1
        for _ in range(w):
            nxt = dp[fwd[:, 0]] + dp[fwd[:, 1]] + dp[fwd[:, 2]] + dp[fwd[:, 3]]
            dp = np.where(allowed_suff, nxt, 0)
            if not np.any(dp):
                break
        total_suff_gc += int(np.sum(dp))

    total_gc = total_pref_gc + total_suff_gc
    return total_gc, total_pref_gc, total_suff_gc, total_gc / float(1 << (2 * (w + k)))


# Method 2: Independent transition-matrix power DP over (vertex) restricted to rank thresholds
def exact_4ary_matrix_power_dp(w, k, rank_4ary):
    N = 1 << (2 * k)
    mask = N - 1
    inv = [0] * N
    for u, r in enumerate(rank_4ary):
        inv[r] = u

    adj = np.zeros((N, N), dtype=np.int64)
    for u in range(N):
        for b in range(4):
            v = ((u << 2) & mask) | b
            adj[u, v] += 1

    active = np.ones(N, dtype=np.int64)
    total_gc = 0
    for r in range(N):
        u0 = inv[r]
        # Prefix GC: paths u0 -> u1 -> ... -> uw with u1..uw in S_{>= r}
        vec = adj[u0, :] * active
        for _ in range(w - 1):
            if not np.any(vec):
                break
            vec = (vec @ adj) * active
        total_gc += int(np.sum(vec))

        # Remove u0 so active becomes S_{> r}
        active[u0] = 0

        # Suffix GC: paths u_0 -> ... -> u_{w-1} -> u0 with u_0..u_{w-1} in S_{> r}
        bvec = adj[:, u0] * active
        for _ in range(w - 1):
            if not np.any(bvec):
                break
            bvec = (adj @ bvec) * active
        total_gc += int(np.sum(bvec))

    return total_gc, total_gc / float(1 << (2 * (w + k)))


# Method 3: Exact high-bit / low-bit bit-plane enumeration for binary-projected orders
def exact_bitplane_prob_gc_dna(w, k, order_bin):
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

    ord_arr = np.array(order_bin, dtype=np.int64)
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
    return total_gc, total_gc / float(1 << (2 * (w + k)))


def main():
    pkg_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    imp_gm_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(pkg_root, "object", "w12_k4_4ary.gm")
    imp_csv_path = sys.argv[2] if len(sys.argv) > 2 else os.path.join(pkg_root, "object", "w12_k4_4ary.csv")
    min_txt_path = sys.argv[3] if len(sys.argv) > 3 else None
    pub_gm_path = sys.argv[4] if len(sys.argv) > 4 else None
    table_csv_path = sys.argv[5] if len(sys.argv) > 5 else None

    w, k = 12, 4
    imp_gm_sha = sha256_file(imp_gm_path)
    imp_csv_sha = sha256_file(imp_csv_path)
    assert imp_gm_sha == EXPECTED_IMP_GM_SHA256, f"w12_k4_4ary.gm sha256 mismatch: {imp_gm_sha}"
    assert imp_csv_sha == EXPECTED_IMP_CSV_SHA256, f"w12_k4_4ary.csv sha256 mismatch: {imp_csv_sha}"

    gm_ranks = load_gm_vector(imp_gm_path)
    csv_ranks = load_4ary_csv(imp_csv_path)
    assert len(gm_ranks) == 256 and sorted(gm_ranks) == list(range(256)), "w12_k4_4ary.gm not a 256-permutation"
    assert gm_ranks == csv_ranks, "Mismatch between object/w12_k4_4ary.gm and object/w12_k4_4ary.csv"

    imp_gm_bytes = os.path.getsize(imp_gm_path)
    imp_csv_bytes = os.path.getsize(imp_csv_path)
    assert imp_gm_bytes == 2056 and imp_csv_bytes == 4518

    print(f"object/w12_k4_4ary.gm  sha256 : {imp_gm_sha} ({imp_gm_bytes} bytes)")
    print(f"object/w12_k4_4ary.csv sha256 : {imp_csv_sha} ({imp_csv_bytes} bytes)")

    # Verify our 256-entry 4-ary DNA order with both independent exact 4-ary de Bruijn DP methods
    imp_gc_1, imp_pref_gc, imp_suff_gc, imp_den_1 = exact_4ary_debruijn_dp_active(w, k, gm_ranks)
    imp_gc_2, imp_den_2 = exact_4ary_matrix_power_dp(w, k, csv_ranks)
    assert imp_gc_1 == imp_gc_2 == 570244411, f"Exact count mismatch: {imp_gc_1} vs {imp_gc_2}"

    # Verify OrensteinLab/Minimizers k4-w12.txt (UHS-7 order [3, 16, 2, 16, 16, 4, 1, 0, 16, 16, 16, 16, 16, 16, 5, 6])
    if min_txt_path and os.path.exists(min_txt_path):
        min_txt_sha = sha256_file(min_txt_path)
        assert min_txt_sha == EXPECTED_MIN_TXT_SHA256, f"k4-w12.txt sha256 mismatch: {min_txt_sha}"
        min_order = ast.literal_eval(open(min_txt_path, "r", encoding="utf-8").read().strip())
        print(f"OrensteinLab/Minimizers k4-w12.txt sha256 : {min_txt_sha} ({os.path.getsize(min_txt_path)} bytes)")
    else:
        min_order = [3, 16, 2, 16, 16, 4, 1, 0, 16, 16, 16, 16, 16, 16, 5, 6]

    min_gc_bp, min_den_bp = exact_bitplane_prob_gc_dna(w, k, min_order)
    min_gc_dp, _, _, min_den_dp = exact_4ary_debruijn_dp_active(w, k, gm_bin_to_4ary_rank(min_order, k))
    assert min_gc_bp == min_gc_dp == 574313157

    # Verify OrensteinLab/10-minimizers w12_k4.gm ([6, 1, 16, 16, 16, 16, 16, 0, 16, 2, 4, 3, 16, 16, 5, 16])
    if pub_gm_path and os.path.exists(pub_gm_path):
        pub_gm_sha = sha256_file(pub_gm_path)
        assert pub_gm_sha == EXPECTED_PUB_GM_SHA256, f"published_w12_k4.gm sha256 mismatch: {pub_gm_sha}"
        pub_order = load_gm_vector(pub_gm_path)
        print(f"OrensteinLab/10-minimizers w12_k4.gm sha256: {pub_gm_sha} ({os.path.getsize(pub_gm_path)} bytes)")
    else:
        pub_order = [6, 1, 16, 16, 16, 16, 16, 0, 16, 2, 4, 3, 16, 16, 5, 16]

    pub_gc_bp, pub_den_bp = exact_bitplane_prob_gc_dna(w, k, pub_order)
    pub_gc_dp, _, _, pub_den_dp = exact_4ary_debruijn_dp_active(w, k, gm_bin_to_4ary_rank(pub_order, k))
    assert pub_gc_bp == pub_gc_dp == 584312429

    print("\n--- Exact Expected DNA Density (over all 4^16 = 4,294,967,296 DNA windows) ---")
    print(f"OrensteinLab/10-minimizers w12_k4.gm          : {pub_gc_bp} / 2^32 = {pub_den_bp:.10f}")
    print(f"OrensteinLab/Minimizers    k4-w12.txt         : {min_gc_bp} / 2^32 = {min_den_bp:.10f}")
    print(f"Claimed 4-ary DNA order    w12_k4_4ary (DP 1) : {imp_gc_1} / 2^32 = {imp_den_1:.10f} (pref={imp_pref_gc}, suff={imp_suff_gc})")
    print(f"Claimed 4-ary DNA order    w12_k4_4ary (DP 2) : {imp_gc_2} / 2^32 = {imp_den_2:.10f}")

    rel_vs_minimizers = (min_den_bp - imp_den_1) / min_den_bp * 100.0
    rel_vs_10min = (pub_den_bp - imp_den_1) / pub_den_bp * 100.0

    if table_csv_path and os.path.exists(table_csv_path):
        csv_sha = sha256_file(table_csv_path)
        assert csv_sha == EXPECTED_CSV_SHA256, f"k_extension_k16_w12.csv sha256 mismatch: {csv_sha}"
        assert os.path.getsize(table_csv_path) == 1644
        print(f"k_extension_k16_w12.csv sha256               : {csv_sha} (1644 bytes)")
        table_vals = {}
        with open(table_csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                val_str = row["4"].strip()
                if val_str and val_str.lower() != "nan":
                    table_vals[row["method"].strip()] = float(val_str)
        print("\n--- Comparison vs All Listed Methods at (w=12, k=4) ---")
        print(f"  {'Minimizers (k4-w12)':20s}: {min_den_bp:.10f}  (our order improves by -{rel_vs_minimizers:.4f}%)")
        for m, v in sorted(table_vals.items(), key=lambda x: x[1]):
            rel_m = (v - imp_den_1) / v * 100.0
            print(f"  {m:20s}: {v:.9f}   (our order improves by -{rel_m:.4f}%)")

    print(f"\nSmallest published DNA density (k4-w12.txt) : {min_den_bp:.10f} (574,313,157 / 2^32)")
    print(f"Required <= 0.5% relative threshold         : 0.1330491135 (571,441,591 / 2^32)")
    print(f"Our exact DNA density (w12_k4_4ary.gm)      : {imp_den_1:.10f} (570,244,411 / 2^32)")
    print(f"Relative reduction vs OrensteinLab/Minimizers: -{rel_vs_minimizers:.4f}% (required >= 0.5000%)")
    print(f"Relative reduction vs OrensteinLab/10-minim. : -{rel_vs_10min:.4f}% (required >= 0.5000%)")

    assert imp_gc_1 <= 571441591
    assert rel_vs_minimizers >= 0.5, f"Relative improvement {rel_vs_minimizers}% < 0.5%"
    print("\nVERIFICATION: PASS")
    print("PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}")
        print("FAIL")
        sys.exit(1)
