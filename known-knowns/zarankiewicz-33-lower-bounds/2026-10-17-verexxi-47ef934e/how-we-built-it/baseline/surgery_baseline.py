#!/usr/bin/env python3
"""Trivial-derivation baseline for z(m,n;3,3): what do cheap edits of PUBLIC witness matrices give?

For a target shape m x n and each public base matrix (wit/):
  1. delete minimum-weight rows / columns until the shape is at most m x n (ties broken at random),
  2. greedily add every 1 that keeps the matrix K33-free (random order),
  3. add missing rows / columns one at a time, each the exact maximum-weight admissible line (branch and bound),
     randomly dropping one 1 of the new line in 20 percent of the cases,
  4. greedily saturate again.
Every output is re-verified K33-free before it is counted. This is the "end-trim / one-line append / padding"
family of derivations; it is NOT an exhaustive search over derivations, so a value it does not reach is evidence,
not proof, that a matrix is not derivable.

Standard library only (Python 3.8+).
usage:  python surgery_baseline.py M N --runs R --seed S [--max-seconds T] [--save FILE]
  --runs R         surgery runs per base matrix (deterministic given --seed when --max-seconds is not hit)
  --max-seconds T  hard wall-clock cap for the whole script (default 3600)
  --save FILE      write the best matrix found (0/1 rows) to FILE
"""
import argparse, json, os, random, sys, time
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
W = os.path.join(HERE, "wit")


def pc(x):
    return bin(x).count("1")


def load_csv(fn):
    return [[int(x) for x in l.strip().split(",")] for l in open(fn) if l.strip()]


def load_txt(fn):
    return [[int(c) for c in l.strip()] for l in open(fn) if l.strip()]


def load_blocks(fn, m=13):
    d = json.load(open(fn))
    bl = d["blocks"]
    n = len(bl)
    M = [[0] * n for _ in range(m)]
    for j, b in enumerate(bl):
        for r in b:
            M[r][j] = 1
    return M


def build(M):
    m = len(M); n = len(M[0]); rm = [0] * m; cm = [0] * n
    for i in range(m):
        for j in range(n):
            if M[i][j]:
                rm[i] |= 1 << j; cm[j] |= 1 << i
    return rm, cm


def k33free(M):
    rm, _ = build(M)
    return all(pc(rm[a] & rm[b] & rm[c]) < 3 for a, b, c in combinations(range(len(M)), 3))


def ones(M):
    return sum(map(sum, M))


def saturate(M, rng):
    m = len(M); n = len(M[0]); rm, cm = build(M)
    cells = [(i, j) for i in range(m) for j in range(n) if not M[i][j]]
    rng.shuffle(cells)
    added = True
    while added:
        added = False
        for (i, j) in cells:
            if M[i][j]:
                continue
            cols = [c for c in range(n) if (rm[i] >> c) & 1]
            ok = True
            for c, d in combinations(cols, 2):
                if pc(cm[j] & cm[c] & cm[d] & ~(1 << i)) >= 2:
                    ok = False; break
            if ok:
                M[i][j] = 1; rm[i] |= 1 << j; cm[j] |= 1 << i; added = True
    return M


def best_line(masks, rng):
    """masks[a]: bitmask over the other dimension for item a. Max set S with no triple in S having >= 2 common coordinates."""
    k = len(masks); order = list(range(k)); rng.shuffle(order)
    badpair = [[0] * k for _ in range(k)]
    for a, b, c in combinations(range(k), 3):
        if pc(masks[a] & masks[b] & masks[c]) >= 2:
            badpair[a][b] |= 1 << c; badpair[b][a] |= 1 << c
            badpair[a][c] |= 1 << b; badpair[c][a] |= 1 << b
            badpair[b][c] |= 1 << a; badpair[c][b] |= 1 << a
    best = [0, 0]

    def rec(S, Sl, cand, size):
        if size > best[0]:
            best[0] = size; best[1] = S
        rem = pc(cand)
        if size + rem <= best[0]:
            return
        c2 = cand
        while c2:
            r = (c2 & -c2).bit_length() - 1; c2 &= c2 - 1
            v = order[r]
            ok = True
            for a in Sl:
                if badpair[v][a] & S:
                    ok = False; break
            if ok:
                rec(S | (1 << v), Sl + [v], c2, size + 1)
            if size + pc(c2) <= best[0]:
                break
    rec(0, [], (1 << k) - 1, 0)
    return best[1]


def add_line(M, axis, rng, drop=0.2):
    m = len(M); n = len(M[0]); rm, cm = build(M)
    if axis == 0:   # add a column; items are rows
        S = best_line(rm, rng)
        rows = [r for r in range(m) if (S >> r) & 1]
        if rows and rng.random() < drop:
            rows.pop(rng.randrange(len(rows)))
        for r in range(m):
            M[r].append(1 if r in rows else 0)
    else:           # add a row; items are columns
        S = best_line(cm, rng)
        cols = [c for c in range(n) if (S >> c) & 1]
        if cols and rng.random() < drop:
            cols.pop(rng.randrange(len(cols)))
        M.append([1 if c in cols else 0 for c in range(n)])
    return M


def delete_to(M, m, n, rng):
    M = [r[:] for r in M]
    while len(M) > m:
        w = [sum(r) for r in M]; mn = min(w)
        cands = [i for i, x in enumerate(w) if x <= mn + (1 if rng.random() < 0.3 else 0)]
        M.pop(rng.choice(cands))
    while len(M[0]) > n:
        w = [sum(M[i][j] for i in range(len(M))) for j in range(len(M[0]))]; mn = min(w)
        cands = [j for j, x in enumerate(w) if x <= mn + (1 if rng.random() < 0.3 else 0)]
        j = rng.choice(cands)
        for r in M:
            r.pop(j)
    return M


def surgery(B, m, n, rng):
    M = delete_to(B, m, n, rng)
    saturate(M, rng)
    while len(M) < m or len(M[0]) < n:
        need = []
        if len(M[0]) < n: need.append(0)
        if len(M) < m: need.append(1)
        add_line(M, rng.choice(need), rng)
    saturate(M, rng)
    return M


BASE_FILES = [
    ("Afr 12x19 (114)", "z12_19_114_witness_verified.csv", load_csv),
    ("Afr 12x22 (132)", "z12_22_132_witness_verified.csv", load_csv),
    ("Afr 13x18 (116)", "z13_18_116_witness.csv", load_csv),
    ("Afr 13x22 (137)", "z13_22_137_blocks.json", load_blocks),
    ("Afr 14x17 (118)", "z14_17_118_witness.csv", load_csv),
    ("Afr 14x18 (124)", "z14_18_124_witness.csv", load_csv),
    ("Afr 15x17 (126)", "z15_17_126_witness.csv", load_csv),
    ("Afr 15x18 (132)", "z15_18_132_witness.csv", load_csv),
    ("Afr 16x17 (132)", "z16_17_132_witness_seed201.csv", load_csv),
    ("Sau 13x19 (118)", "sau_13x19_118.txt", load_txt),
    ("Sau 14x19 (126)", "sau_14x19_126.txt", load_txt),
    ("Sau 16x18 (136)", "sau_16x18_136.txt", load_txt),
]


def bases():
    return {name: ld(os.path.join(W, fn)) for name, fn, ld in BASE_FILES}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int)
    ap.add_argument("n", type=int)
    ap.add_argument("--runs", type=int, default=300)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--max-seconds", type=float, default=3600.0)
    ap.add_argument("--save")
    a = ap.parse_args()
    t_start = time.time()
    B = bases()
    print("target %d x %d, %d runs per base, seed %d, cap %.0f s" % (a.m, a.n, a.runs, a.seed, a.max_seconds))
    for k, M in B.items():
        print("  base %-18s %2dx%-2d ones %3d K33-free %s" % (k, len(M), len(M[0]), ones(M), k33free(M)))
    best = (0, None, None); total = 0; hist = {}; capped = False
    for bi, (name, M0) in enumerate(B.items()):
        rng = random.Random(a.seed * 1000 + bi)
        bb = 0; done = 0
        for _ in range(a.runs):
            if time.time() - t_start > a.max_seconds:
                capped = True; break
            M = surgery(M0, a.m, a.n, rng)
            assert len(M) == a.m and len(M[0]) == a.n and k33free(M), "invalid surgery output"
            o = ones(M); done += 1
            hist[o] = hist.get(o, 0) + 1
            if o > bb: bb = o
            if o > best[0]: best = (o, name, [r[:] for r in M])
        total += done
        print("  base %-18s runs %5d best %d" % (name, done, bb)); sys.stdout.flush()
        if capped: break
    print("histogram of ones (top 5): %s" % sorted(hist.items())[-5:])
    print("total runs %d, wall %.0f s, capped %s" % (total, time.time() - t_start, capped))
    print("BEST %d from [%s] (re-verified K33-free: %s)" % (best[0], best[1], k33free(best[2])))
    if a.save:
        with open(a.save, "w", newline="\n") as f:
            f.write("\n".join("".join(map(str, r)) for r in best[2]) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
