#!/usr/bin/env python3
"""CNF for Definition 2.2 of arXiv:2604.08790: m tournaments on V = {0..n-1} such that every k-subset U
is dominated, in at least one tournament t, by one vertex v outside U (v -> u in T_t for every u in U).

Variables
  e(t,i,j), i < j : true iff i -> j in tournament t (false iff j -> i); every assignment is a tournament tuple.
  d(t,v,U)        : "v dominates U in T_t"; only the direction d -> (v -> u) is needed.
Clauses
  for every k-subset U: OR_{t, v not in U} d(t,v,U)
  for every t, U, v not in U, u in U: (not d(t,v,U)) or lit(v -> u in T_t)
The formula is satisfiable iff an S_k set of m tournaments of order n exists (Definition 2.2).

Symmetry breaking (option --sb, default 'none'):
  'dom0': unit clauses 0 -> u in T_0 for u = 1..k. Sound: in any solution some k-set (say {1..k} after
          relabelling) is dominated by some vertex in some tournament; relabel that vertex as 0 and that tournament
          as T_0. Vertex relabelling and tournament reordering map solutions to solutions.
  'maxdeg D': vertex 0 in T_0 has out-neighbourhood exactly {1..D}, and every vertex in every tournament has
          out-degree <= D (sequential-counter at-most-D). Sound for the case "maximum out-degree over all
          tournaments and vertices equals D": relabel the vertex attaining it as 0, its tournament as T_0, and its
          out-neighbours as 1..D. Running every D from k to n-1 covers all solutions (D >= k is forced because
          some vertex dominates a k-set).
  'global': one CNF covering every maximum out-degree D at once. (a) The out-neighbourhood of vertex 0 in T_0 is an
          initial segment {1..d}: (0 -> u+1) implies (0 -> u). (c) 0 -> u for u = 1..k. (b) For every D in k..n-1, if
          d = D (that is, 0 -> D and not 0 -> D+1) then every vertex of every tournament has out-degree <= D
          (sequential counters whose overflow clauses carry the extra literals "not (0 -> D)" and "(0 -> D+1)").
          Sound by the same relabelling as 'maxdeg': take a vertex of maximum out-degree D* >= k over all tournaments,
          make it vertex 0 of T_0 with out-neighbours 1..D*; then (a), (b) and (c) hold.
  'gsort': 'global' plus degree sorting inside the two blocks fixed by vertex 0 of T_0: for consecutive u, u+1 both in
          {1..d} or both in {d+1..n-1} (d = out-degree of 0 in T_0), out-degree of u in T_0 >= out-degree of u+1 in T_0.
          Exact unary degree counters (sequential counters with both implication directions) give the comparison.
          Sound: relabelling inside {1..d} and inside {d+1..n-1} fixes vertex 0, T_0 and the set {1..d}, so it keeps
          (a), (b), (c); every solution can be sorted that way. For m >= 3 also: (0 -> 1 in T_1) or not (0 -> 1 in T_2)
          (swap T_1 and T_2 otherwise; the swap keeps every other constraint).
  'global2': 'global' plus, for the case d = n-1 (vertex 0 beats everyone in T_0, literal 0 -> n-1), the same device
          one level down on V' = {1..n-1} and T_1..T_(m-1): vertex 1 of T_1 has out-neighbourhood {2..d'+1} inside V'
          (an initial segment), 1 -> u for u = 2..k (so d' >= k-1), and if d' = D' then every vertex of V' has
          out-degree <= D' inside V' in every T_t, t >= 1. Every nested clause carries the literal not(0 -> n-1).
          Sound: when 0 beats everyone in T_0, the k-sets containing 0 can only be dominated in T_1..T_(m-1), so some
          (t >= 1, v in V') dominates a (k-1)-subset of V' inside V' (out-degree >= k-1 there); relabel V' so that a
          maximiser of the out-degree inside V' over t >= 1 is vertex 1 of T_1 with out-neighbours 2..d'+1 (permuting
          T_1..T_(m-1)). This fixes vertex 0 and leaves (a), (b), (c) true, because 0 still beats everyone in T_0 and
          the bounds of (b) are void for d = n-1.
  'global3': 'global2' plus a second level for d < n-1, with w = d+1 (the first in-neighbour of 0 in T_0): the
          out-neighbourhood of w in T_0 is an initial segment of {1..d} and an initial segment of {d+2..n-1}; and for
          m >= 3, (0 -> 1 in T_1) or not (0 -> 1 in T_2) when d < n-1. All clauses carry the literals that make them
          conditional on d = D (the same pair as in 'global').
          Sound: permuting {1..d} and permuting {d+2..n-1} fixes vertex 0, the set {1..d} and the vertex w = d+1, so
          it keeps (a), (b), (c); choose these permutations to put w's out-neighbours first in each block. For d < n-1
          the nested clauses of 'global2' are void and T_1, T_2 play symmetric roles, so swapping them is allowed.
"""
import argparse, sys
from itertools import combinations

class CNF:
    def __init__(self): self.nv = 0; self.clauses = []
    def new(self): self.nv += 1; return self.nv
    def add(self, c): self.clauses.append(c)

def build(m, k, n, sb="none", D=None):
    F = CNF()
    E = {}
    for t in range(m):
        for i in range(n):
            for j in range(i + 1, n):
                E[t, i, j] = F.new()
    def beats(t, v, u):  # literal for v -> u in T_t
        return E[t, v, u] if v < u else -E[t, u, v]
    for U in combinations(range(n), k):
        Us = set(U); big = []
        for t in range(m):
            for v in range(n):
                if v in Us: continue
                d = F.new(); big.append(d)
                for u in U: F.add([-d, beats(t, v, u)])
        F.add(big)
    if sb == "global3":
        F2 = build(m, k, n, "global2"); F.nv, F.clauses = F2.nv, F2.clauses
        for D in range(k, n - 1):
            cond = [-beats(0, 0, D), beats(0, 0, D + 1)]      # all literals false iff d = D
            w = D + 1
            for u in range(1, D):                              # block {1..D}
                F.add([-beats(0, w, u + 1), beats(0, w, u)] + cond)
            for u in range(D + 2, n - 1):                      # block {D+2..n-1}
                F.add([-beats(0, w, u + 1), beats(0, w, u)] + cond)
        if m >= 3:
            F.add([beats(1, 0, 1), -beats(2, 0, 1), beats(0, 0, n - 1)])
        return F
    if sb == "global2":
        F2 = build(m, k, n, "global"); F.nv, F.clauses = F2.nv, F2.clauses
        if m >= 2 and n - 1 >= k:
            c0 = [-beats(0, 0, n - 1)]
            for u in range(2, n - 1): F.add([-beats(1, 1, u + 1), beats(1, 1, u)] + c0)
            for u in range(2, k + 1): F.add([beats(1, 1, u)] + c0)
            Vp = list(range(1, n))
            for Dp in range(k - 1, n - 2):      # d' = n-2 needs no bound
                c1 = c0 + [-beats(1, 1, Dp + 1), beats(1, 1, Dp + 2)]
                for t in range(1, m):
                    for v in Vp:
                        at_most(F, [beats(t, v, u) for u in Vp if u != v], Dp, c1)
        return F
    if sb == "gsort":
        F2 = build(m, k, n, "global"); F.nv, F.clauses = F2.nv, F2.clauses
        cnts = [exact_counter(F, [beats(0, v, u) for u in range(n) if u != v]) for v in range(n)]
        for u in range(1, n - 1):
            same_block = [beats(0, 0, u + 1)]                 # u+1 in {1..d} implies u in {1..d}
            # case both in {1..d}: 0 -> u+1 ; case both in {d+1..n-1}: not 0 -> u
            for j in range(len(cnts[u + 1])):
                F.add([-beats(0, 0, u + 1), -cnts[u + 1][j], cnts[u][j]])
                F.add([beats(0, 0, u), -cnts[u + 1][j], cnts[u][j]])
        if m >= 3: F.add([beats(1, 0, 1), -beats(2, 0, 1)])
        return F
    if sb == "dom0":
        for u in range(1, k + 1): F.add([beats(0, 0, u)])
    elif sb == "global":
        for u in range(1, n - 1): F.add([-beats(0, 0, u + 1), beats(0, 0, u)])
        for u in range(1, k + 1): F.add([beats(0, 0, u)])
        for D in range(k, n - 1):           # D = n-1 needs no degree bound
            cond = [-beats(0, 0, D), beats(0, 0, D + 1)]
            for t in range(m):
                for v in range(n):
                    lits = [beats(t, v, u) for u in range(n) if u != v]
                    at_most(F, lits, D, cond)
    elif sb == "maxdeg":
        assert D is not None and k <= D <= n - 1
        for u in range(1, n):
            F.add([beats(0, 0, u)] if u <= D else [-beats(0, 0, u)])
        for t in range(m):
            for v in range(n):
                lits = [beats(t, v, u) for u in range(n) if u != v]
                at_most(F, lits, D)
    return F

def exact_counter(F, x):
    """Unary counter with both directions: c[j] true iff at least j+1 of the literals x are true."""
    prev = None
    for i, xi in enumerate(x):
        cur = [F.new() for _ in range(i + 1)]
        for j in range(i + 1):
            # cur[j] <-> prev[j] or (xi and prev[j-1]) ; prev[-1] = true, prev[i] = false
            a = prev[j] if (prev is not None and j < i) else None
            b = prev[j - 1] if (prev is not None and j >= 1) else None
            if j == 0:
                if a is None: F.add([-cur[0], xi]); F.add([cur[0], -xi])
                else: F.add([-cur[0], a, xi]); F.add([cur[0], -a]); F.add([cur[0], -xi])
            else:
                if a is None: F.add([-cur[j], b]); F.add([-cur[j], xi]); F.add([cur[j], -b, -xi])
                else:
                    F.add([-cur[j], a, b]); F.add([-cur[j], a, xi]); F.add([cur[j], -a]); F.add([cur[j], -b, -xi])
        prev = cur
    return prev

def at_most(F, x, K, cond=()):
    """Sinz sequential counter: at most K of the literals x are true. With cond (a list of literals), only the
    overflow clauses carry cond, so the bound applies when every literal of cond is false; the register clauses
    only force counter bits upward and can always be satisfied by the exact counts."""
    cond = list(cond)
    n = len(x)
    if K >= n: return
    if K == 0:
        for l in x: F.add([-l] + cond)
        return
    s = [[F.new() for _ in range(K)] for _ in range(n - 1)]
    F.add([-x[0], s[0][0]])
    for j in range(1, K): F.add([-s[0][j]])
    for i in range(1, n - 1):
        F.add([-x[i], s[i][0]]); F.add([-s[i - 1][0], s[i][0]])
        for j in range(1, K):
            F.add([-x[i], -s[i - 1][j - 1], s[i][j]]); F.add([-s[i - 1][j], s[i][j]])
        F.add([-x[i], -s[i - 1][K - 1]] + cond)
    F.add([-x[n - 1], -s[n - 2][K - 1]] + cond)

def decode(model, m, n):
    pos = set(l for l in model if l > 0)
    T = []; idx = 0
    for t in range(m):
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                idx += 1
                if idx in pos: A[i][j] = 1
                else: A[j][i] = 1
        T.append(A)
    return T

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("m", type=int); ap.add_argument("k", type=int); ap.add_argument("n", type=int)
    ap.add_argument("--sb", default="none", choices=["none", "dom0", "maxdeg", "global", "gsort", "global2", "global3"]); ap.add_argument("--D", type=int)
    ap.add_argument("-o", default="-")
    a = ap.parse_args()
    F = build(a.m, a.k, a.n, a.sb, a.D)
    out = sys.stdout if a.o == "-" else open(a.o, "w")
    out.write(f"c schutte m={a.m} k={a.k} n={a.n} sb={a.sb} D={a.D}\np cnf {F.nv} {len(F.clauses)}\n")
    for c in F.clauses: out.write(" ".join(map(str, c)) + " 0\n")
