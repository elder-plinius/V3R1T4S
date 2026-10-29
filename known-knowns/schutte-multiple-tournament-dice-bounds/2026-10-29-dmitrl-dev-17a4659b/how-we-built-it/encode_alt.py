#!/usr/bin/env python3
"""Independent second encoding (self-check) of Definition 2.1/2.2 of arXiv:2604.08790, written separately from
encode_schutte.py in a different style.

Variables a[t][i][j] for every ordered pair i != j ("i beats j in T_t"), with explicit tournament clauses
(exactly one of a[t][i][j], a[t][j][i]). For every k-set U and every (t, v not in U) an auxiliary y with
y -> a[t][v][u] for u in U, and one clause OR y over (t, v) for each U.

Symmetry breaking ('max0'), stated differently from encode_schutte.py's 'global' but with the same content:
vertex 0 of T_0 has the largest out-degree among all (t, v) (totalizer unary counters, cnt(t,v) <= cnt(0,0)),
its out-neighbourhood in T_0 is an initial segment {1..d}, and 0 beats 1..k in T_0.
Sound: relabel a vertex of maximum out-degree (over all tournaments) as vertex 0 of T_0 and its out-neighbours as
1..d; d >= k because some vertex dominates some k-set.
"""
import sys
from itertools import combinations

def encode(m, k, n, sb="max0"):
    nv = 0; cls = []
    def new():
        nonlocal nv; nv += 1; return nv
    a = {}
    for t in range(m):
        for i in range(n):
            for j in range(n):
                if i != j: a[t, i, j] = new()
    for t in range(m):
        for i in range(n):
            for j in range(i + 1, n):
                cls.append([a[t, i, j], a[t, j, i]]); cls.append([-a[t, i, j], -a[t, j, i]])
    for U in combinations(range(n), k):
        ys = []
        for t in range(m):
            for v in range(n):
                if v in U: continue
                y = new(); ys.append(y)
                cls.extend([[-y, a[t, v, u]] for u in U])
        cls.append(ys)
    if sb == "max0":
        for u in range(1, n - 1): cls.append([-a[0, 0, u + 1], a[0, 0, u]])
        for u in range(1, k + 1): cls.append([a[0, 0, u]])
        def totalizer(lits):
            # returns unary outputs o[0..len-1], o[r] <-> at least r+1 of lits are true
            if len(lits) == 1: return [lits[0]]
            h = len(lits) // 2
            A, B = totalizer(lits[:h]), totalizer(lits[h:])
            R = [new() for _ in range(len(A) + len(B))]
            for i in range(len(A) + 1):
                for j in range(len(B) + 1):
                    if i + j >= 1:   # A_i and B_j -> R_{i+j}   (A_0 = B_0 = true)
                        c = [R[i + j - 1]]
                        if i: c.append(-A[i - 1])
                        if j: c.append(-B[j - 1])
                        cls.append(c)
                    if i + j < len(A) + len(B):   # not A_{i+1} and not B_{j+1} -> not R_{i+j+1}
                        c = [-R[i + j]]
                        if i < len(A): c.append(A[i])
                        if j < len(B): c.append(B[j])
                        cls.append(c)
            return R
        cnt = {(t, v): totalizer([a[t, v, u] for u in range(n) if u != v]) for t in range(m) for v in range(n)}
        top = cnt[0, 0]
        for (t, v), c in cnt.items():
            if (t, v) == (0, 0): continue
            for r in range(len(c)): cls.append([-c[r], top[r]])
    return nv, cls, a

if __name__ == "__main__":
    m, k, n = map(int, sys.argv[1:4]); sb = sys.argv[4] if len(sys.argv) > 4 else "max0"; out = sys.argv[5]
    nv, cls, a = encode(m, k, n, sb)
    with open(out, "w") as f:
        f.write(f"c schutte-alt m={m} k={k} n={n} sb={sb}\np cnf {nv} {len(cls)}\n")
        for c in cls: f.write(" ".join(map(str, c)) + " 0\n")
