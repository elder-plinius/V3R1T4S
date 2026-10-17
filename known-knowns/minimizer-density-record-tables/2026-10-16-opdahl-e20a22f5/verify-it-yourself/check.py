#!/usr/bin/env python3
"""Check the claim in this package: one minimizer order for (w=12, k=3).

The composition comes from the published notebook greedymini_density.ipynb.

  Cell 2, random_density_function_dna_includes_tiebreaking:

      shift_8k = 8 * k
      ranks = [(function(km, w, k, seed) << shift_8k) + get_kmer_id_dna(k, km, seed) for km in kmers]

  Cell 4, GreedyMiniScheme.get_minimizer -> _fn:

      return (rank_train << (2 * k)) + kmer

The composed rank is:

      (((order[bin_kmer] << (2*k)) + kmer) << (8*k)) + get_kmer_id_dna(k, km, seed)

bin_kmer is the high bit of each 2-bit base: bit = (nuc >> 1) & 1. For k=3, the bits are 5, 3 and 1.

This file needs numpy. Run the check from the package folder:

      sh verify-it-yourself/run_checks.sh
"""
import hashlib, json, struct, sys
import numpy as np

W = 12
K = 3
N_SAMPLES = 2000000
SEEDS = (0, 1, 2)
EXPECTED_CLAIMED = 0.136644513466
EXPECTED_GREEDYMINI = 0.138882166707
SMALLEST_TABLE = 0.138389448
MARGIN_REQUIRED = 0.005


def load_gm(path):
    """Read a GreedyMini order file. The file holds a size header and uint64 values."""
    raw = open(path, "rb").read()
    n = struct.unpack("P", raw[:struct.calcsize("P")])[0]
    return list(struct.unpack("%dQ" % n, raw[struct.calcsize("P"):]))


def get_kmer_id_dna(k, kmer, seed):
    """Give the tiebreak value of a k-mer. This function comes from the notebook."""
    h = hashlib.sha256((kmer + seed).to_bytes(2 * k, byteorder="big")).digest()
    return (4 ** k) * (int.from_bytes(h, "big") % (4 ** k)) + kmer


def density(order, n_samples, seed):
    """Measure the density of one order on one random sequence.

    Do these steps:
    1. Make the sequence.
    2. Find the k-mer at each position.
    3. Give a rank to each k-mer.
    4. Find the smallest rank in each window.
    5. Divide the number of new positions by the number of k-mers.
    """
    total = n_samples + W + K - 1
    nuc = np.random.default_rng(seed).integers(0, 4, size=total, dtype=np.uint32)
    n_kmers = total - K + 1
    km = np.zeros(n_kmers, dtype=np.int64)
    cur = 0
    for p in range(K):
        cur = (cur << 2) | int(nuc[p])
    km[0] = cur
    for i in range(1, n_kmers):
        cur = ((cur << 2) | int(nuc[i + K - 1])) & ((1 << (2 * K)) - 1)
        km[i] = cur
    bin_kmer = (((km >> 5) & 1) << 2) | (((km >> 3) & 1) << 1) | ((km >> 1) & 1)
    tb = np.array([get_kmer_id_dna(K, int(x), seed) for x in km], dtype=np.int64)
    inner = (np.array(order, dtype=np.int64)[bin_kmer] << (2 * K)) + km
    rank = (inner << (8 * K)) + tb
    win = np.lib.stride_tricks.sliding_window_view(rank, W)
    mn = win.argmin(axis=1) + np.arange(len(win))
    return (1 + int(np.count_nonzero(np.diff(mn)))) / n_kmers


def main():
    ok = True
    order = [int(x) for x in open("object/order.txt").read().split()]

    if sorted(order) != list(range(8)):
        print("FAIL: object/order.txt is not a permutation of 0 to 7: %r" % (order,))
        ok = False

    obj = json.load(open("object/order.json"))
    if obj.get("order") != order:
        print("FAIL: object/order.txt and object/order.json do not agree")
        ok = False
    if float(obj.get("claimed_mean_density", 0.0)) != EXPECTED_CLAIMED:
        print("FAIL: object/order.json holds a different claimed density")
        ok = False
    if float(obj.get("smallest_listed_table_value", 0.0)) != SMALLEST_TABLE:
        print("FAIL: object/order.json holds a different table value")
        ok = False

    if ok:
        gm = load_gm("verify-it-yourself/w12_k3.gm")
        c = float(np.mean([density(order, N_SAMPLES, s) for s in SEEDS]))
        g = float(np.mean([density(gm, N_SAMPLES, s) for s in SEEDS]))
        margin = (SMALLEST_TABLE - c) / SMALLEST_TABLE
        print("n_samples        = %d, seeds %s" % (N_SAMPLES, list(SEEDS)))
        print("claimed order    = %r" % (order,))
        print("claimed density  = %.12f   (expected %.12f)" % (c, EXPECTED_CLAIMED))
        print("GreedyMini       = %.12f   (expected %.12f)" % (g, EXPECTED_GREEDYMINI))
        print("smallest listed  = %.9f" % SMALLEST_TABLE)
        print("margin           = %.4f%% (required >= 0.5%%)" % (margin * 100))
        if abs(c - EXPECTED_CLAIMED) > 1e-9:
            print("FAIL: the claimed density does not agree with the recorded value")
            ok = False
        if abs(g - EXPECTED_GREEDYMINI) > 1e-9:
            print("FAIL: the GreedyMini density does not agree with the recorded value")
            ok = False
        if margin < MARGIN_REQUIRED:
            print("FAIL: the margin is below the required 0.5%%")
            ok = False

    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
