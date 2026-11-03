#!/usr/bin/env python3
"""Self-contained nested staircase combining builder for C(68, 14, 5) -> 16,543 blocks
(before prune.c seed=1 reduces it to 15,675 blocks).

Usage:
  python3 how-we-built-it/fetch_ingredients.py   # downloads the La Jolla ingredients (sha256-checked)
  python3 how-we-built-it/build_68_14_5.py [out_staircase.txt]
"""
import csv
import hashlib
import heapq
import itertools
import os
import sys
from math import comb
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ING = os.path.join(HERE, "ingredients")


def _expected_sha256():
    with open(os.path.join(HERE, "INGREDIENTS.tsv"), encoding="utf-8") as f:
        return {row["file"]: row["sha256"] for row in csv.DictReader(f, delimiter="\t")}


EXPECTED = _expected_sha256()


def load_ing(v, k, t):
    """Read a La Jolla ingredient downloaded by fetch_ingredients.py, after checking its sha256."""
    name = f"C_{v}_{k}_{t}.txt"
    path = os.path.join(ING, name)
    if not os.path.exists(path):
        sys.exit(f"missing {path}: run `python3 how-we-built-it/fetch_ingredients.py` first")
    with open(path, "rb") as f:
        data = f.read()
    if hashlib.sha256(data).hexdigest() != EXPECTED[name]:
        sys.exit(f"{name}: sha256 does not match INGREDIENTS.tsv")
    return [frozenset(int(x) - 1 for x in line.split()) for line in data.decode().splitlines() if line.strip()]


def triv_t1(v, k):
    out = []
    for s in range(0, v, k):
        blk = set(range(s, min(s + k, v)))
        x = 0
        while len(blk) < k:
            blk.add(x)
            x += 1
        out.append(frozenset(blk))
    return out


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
    out_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "staircase_68_14_5.txt")
    v1, v2, V, K, T = 18, 50, 68, 14, 5
    chains = [
        (0, 0, 0, [frozenset()], load_ing(50, 14, 5)),
        (1, 1, 2, triv_t1(18, 2), load_ing(50, 12, 4)),
        (2, 3, 6, load_ing(18, 6, 3), load_ing(50, 8, 3)),
        (4, 4, 12, load_ing(18, 12, 4), triv_t1(50, 2)),
        (5, 5, 14, load_ing(18, 14, 5), [frozenset()]),
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
    print(f"STAIR (68,14,5) v1=18 built={len(D)} file={out_path}")


if __name__ == "__main__":
    main()
