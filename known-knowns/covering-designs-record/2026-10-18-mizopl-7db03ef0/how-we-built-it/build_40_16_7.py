#!/usr/bin/env python3
"""Self-contained nested staircase combining builder for C(40, 16, 7) -> 8,172 blocks
(before prune.c seed=1 reduces it to 7,251 blocks).

Usage:
  python3 how-we-built-it/build_40_16_7.py [out_staircase.txt]
"""
import heapq
import itertools
import os
import sys
from math import comb
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ING = os.path.join(HERE, "ingredients")


def load_ing(v, k, t):
    path = os.path.join(ING, f"C_{v}_{k}_{t}.txt")
    with open(path, encoding="utf-8") as f:
        return [frozenset(int(x) - 1 for x in line.split()) for line in f if line.strip()]


def ranks(blocks, s):
    out = []
    for b in blocks:
        bl = sorted(b)
        if s == 0:
            out.append(np.zeros(1, dtype=np.int64))
            continue
        rs = [sum(comb(c[i], i + 1) for i in range(s)) for c in itertools.combinations(bl, s)]
        out.append(np.array(rs, dtype=np.int64))
    return out


def greedy_sub(blocks, n, s):
    if s == 0:
        return blocks[:1]
    N = comb(n, s)
    cov = np.zeros(N, dtype=bool)
    R = ranks(blocks, s)
    h = [(-len(np.unique(r)), i) for i, r in enumerate(R)]
    heapq.heapify(h)
    chosen = []
    left = N
    while left > 0 and h:
        g, i = heapq.heappop(h)
        gain = int((~cov[R[i]]).sum())
        if h and gain < -h[0][0]:
            heapq.heappush(h, (-gain, i))
            continue
        if gain == 0:
            break
        cov[R[i]] = True
        left -= gain
        chosen.append(blocks[i])
    assert left == 0, "greedy subset failed to cover"
    return chosen


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "staircase_40_16_7.txt")
    v1, v2, V, K, T = 16, 24, 40, 16, 7
    chains = [
        (0, 0, 0, [frozenset()], load_ing(24, 16, 7)),
        (1, 2, 4, load_ing(16, 4, 2), load_ing(24, 12, 6)),
        (3, 4, 8, load_ing(16, 8, 4), load_ing(24, 8, 4)),
        (5, 6, 12, load_ing(16, 12, 6), load_ing(24, 4, 2)),
        (7, 7, 16, [frozenset(range(16))], [frozenset()]),
    ]
    out = set()
    for p, q, k1, Aq, Bp in chains:
        A = {q: Aq}
        for i in range(q - 1, p - 1, -1):
            A[i] = greedy_sub(A[i + 1], v1, i)
        B = {p: Bp}
        for i in range(p + 1, q + 1):
            B[i] = greedy_sub(B[i - 1], v2, T - i)
        for i in range(p, q + 1):
            for a in A[i]:
                for b in B[i]:
                    out.add(frozenset(set(a) | {v1 + y for y in b}))
    D = sorted(sorted(b) for b in out)
    with open(out_path, "w", encoding="utf-8") as f:
        for b in D:
            f.write(" ".join(str(x + 1) for x in b) + "\n")
    print(f"STAIR (40,16,7) v1=16 built={len(D)} file={out_path}")


if __name__ == "__main__":
    main()
