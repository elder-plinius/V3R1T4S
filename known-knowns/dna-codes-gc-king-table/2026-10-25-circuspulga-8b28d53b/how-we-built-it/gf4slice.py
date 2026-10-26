#!/usr/bin/env python3
"""Far import (projective-geometry codes over GF(4)) + per-column letter-map search.
Codes: the [21,3,16] simplex code of PG(2,4) (codeword for a linear form f = values of f at the 21 points), punctured
on a point set S. Distances of the punctured code are checked exactly. A per-column 2-subset T_j of GF(4) is sent to
{C,G}; we search T (6^n choices) for the largest set of codewords with GC-content exactly w = floor(n/2)
(random restarts + first-improvement local search on (count, -sum|GC-w|)). Output: the slice as a DNA code.
Usage: gf4slice.py N SEED RESTARTS OUTFILE     (S = first 21-N points of a fixed point order chosen to keep d max)"""
import sys, itertools, random
def mul(x, y):
    r = 0
    for i in range(2):
        if (y >> i) & 1: r ^= x << i
    if r & 4: r ^= 0b111
    return r
N, seed, restarts, outf = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
# points of PG(2,4): normalised nonzero vectors
pts = [p for p in itertools.product(range(4), repeat=3) if any(p) and p[[i for i in range(3) if p[i]][0]] == 1]
assert len(pts) == 21
def ev(f, p): return mul(f[0], p[0]) ^ mul(f[1], p[1]) ^ mul(f[2], p[2])
forms = list(itertools.product(range(4), repeat=3))
def code_on(points): return [tuple(ev(f, p) for p in points) for f in forms]
def mind(C): return min(sum(a != b for a, b in zip(x, y)) for x, y in itertools.combinations(C, 2))
# choose the deleted set: for 21-N <= 5 points, take points on one line first (keeps d = N - 4 + 1 when a full line
# plus extra points are removed, d = 16 - s otherwise); verify by exact distance computation.
line = [p for p in pts if p[0] == 0]           # the line x0 = 0 (5 points)
rest = [p for p in pts if p[0] != 0]
s = 21 - N
best_set = None
for S in ([line[:s]] if s <= 5 else [line + rest[:s-5]]):
    keep = [p for p in pts if p not in S]
    C = code_on(keep); d = mind(C)
    best_set = (keep, C, d)
keep, C, d = best_set
w = N // 2
print('N=%d deleted=%d words=%d min_distance=%d w=%d' % (N, s, len(C), d, w))
pairs = list(itertools.combinations(range(4), 2))
rng = random.Random(seed)
def evalT(T):
    gcs = [sum(c[j] in T[j] for j in range(N)) for c in C]
    return (sum(g == w for g in gcs), -sum(abs(g - w) for g in gcs))
best = None
for r in range(restarts):
    T = [pairs[rng.randrange(6)] for _ in range(N)]; v = evalT(T); improved = True
    while improved:
        improved = False
        for j in rng.sample(range(N), N):
            for p in pairs:
                if p == T[j]: continue
                old = T[j]; T[j] = p; v2 = evalT(T)
                if v2 > v: v = v2; improved = True
                else: T[j] = old
    if best is None or v > best[0]: best = (v, list(T))
print('restarts=%d best_count=%d' % (restarts, best[0][0]))
T = best[1]; words = []
for c in C:
    if sum(c[j] in T[j] for j in range(N)) != w: continue
    s_ = ''
    for j in range(N):
        gc = [x for x in range(4) if x in T[j]]; at = [x for x in range(4) if x not in T[j]]
        s_ += 'CG'[gc.index(c[j])] if c[j] in T[j] else 'AT'[at.index(c[j])]
    words.append(s_)
open(outf, 'w').write('\n'.join(words) + '\n'); print('written %s size=%d' % (outf, len(words)))
