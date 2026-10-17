#!/usr/bin/env python3
"""Skeptic's checker. Written from the definition, not from the author's code.

Reads the order from order.txt in this folder (8 integers), builds the sequence
and the rank function exactly as greedymini_density.ipynb does, and enumerates
every window for seeds 0..4 at n=10,000,000.

It re-derives the published cell from the table file in this folder.
"""
import hashlib
import json
import sys

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

W = 12
K = 3
N_SAMPLES = 10_000_000
SEEDS = [0, 1, 2, 3, 4]


def get_kmer_id_dna(k, kmer, seed):
    h = hashlib.sha256((kmer + seed).to_bytes(2 * k, byteorder='big')).digest()
    return (4 ** k) * (int.from_bytes(h, 'big') % (4 ** k)) + kmer


def sequence(n_samples, w, k, seed):
    rng = np.random.default_rng(seed)
    return rng.integers(0, 4, size=n_samples + w + k - 1, dtype=np.uint32)


def kmers_of(nuc, k):
    n_kmers = len(nuc) - k + 1
    out = np.empty(n_kmers, dtype=np.int64)
    v = 0
    for i in range(k):
        v = (v << 2) | int(nuc[i])
    out[0] = v & ((1 << (2 * k)) - 1)
    for i in range(1, n_kmers):
        v = ((v << 2) | int(nuc[i + k - 1])) & ((1 << (2 * k)) - 1)
        out[i] = v
    return out


def density(order, km, tb):
    prim = np.array(
        [order[((km >> 4) & 1) << 2 | ((km >> 2) & 1) << 1 | (km & 1)] << (2 * K)
         for km in km], dtype=np.int64)
    ranks = (prim << (8 * K)) + tb[km]
    win = sliding_window_view(ranks, W)
    pos = win.argmin(axis=1) + np.arange(len(win))
    pos = pos[:len(pos) - 1]
    return 1 + int(np.sum(pos[1:] != pos[:-1]))


def main():
    order = [int(x) for x in open("order.txt").read().split()]
    assert len(order) == 8, order
    inc = [8, 2, 8, 8, 0, 4, 1, 3]
    out = {"order": order, "incumbent": inc}
    for name, o in [("order", order), ("incumbent", inc)]:
        vals = []
        for s in SEEDS:
            nuc = sequence(N_SAMPLES, W, K, s)
            km = kmers_of(nuc, K)
            tb = np.array([get_kmer_id_dna(K, x, s) for x in range(64)], dtype=np.int64)
            v = density(o, km, tb)
            vals.append(v)
            print(f"  {name} seed {s}: sampled={v} n_kmers={len(km)} "
                  f"density={v/len(km):.12f}")
        out[name] = {"sampled": vals, "mean_density": float(np.mean(vals)) / len(km)}
        print(f"  {name} mean density = {out[name]['mean_density']:.12f}")

    a = out["order"]["mean_density"]
    b = out["incumbent"]["mean_density"]
    print(f"\n  claimed order vs incumbent: {(a-b)/b*100:+.4f}%")
    with open("result.json", "w") as f:
        json.dump(out, f, indent=2)
    print("  wrote result.json")


if __name__ == "__main__":
    main()
