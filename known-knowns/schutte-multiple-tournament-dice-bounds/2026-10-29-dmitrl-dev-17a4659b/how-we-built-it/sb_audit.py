#!/usr/bin/env python3
"""Randomised soundness test of the added (symmetry-breaking) clauses of a Schutte CNF (needs python-sat).

For random tournament tuples, apply the relabelling of the soundness argument (encode_schutte.py docstring:
'global3'): a vertex of maximum out-degree becomes vertex 0 of T_0 with out-neighbours 1..d; if d < n-1, the vertex
w = d+1 is an in-neighbour of 0 and its out-neighbours come first inside {1..d} and inside {d+2..n-1}; for m >= 3 swap
T_1, T_2 if (0 -> 1 in T_2) and not (0 -> 1 in T_1); if d = n-1, a maximiser (t' >= 1, v') of the out-degree inside
V' = {1..n-1} becomes vertex 1 of T_1 with out-neighbours 2..d'+1 inside V'. Then fix the edge variables and ask a
SAT solver whether the added clauses (all clauses that are not domination or defining clauses) can be satisfied.
Every canonical tuple must give SAT (soundness of the clauses as implemented); random relabellings are a control
that should often give UNSAT (the clauses are not vacuous).
usage: sb_audit.py cnf m k n trials seed"""
import sys, random
from itertools import combinations
from collections import defaultdict
from pysat.solvers import Solver

def load(path, m, k, n):
    pairs = list(combinations(range(n), 2)); P = len(pairs); E = m * P
    clauses = [list(map(int, l.split()))[:-1] for l in open(path) if l.strip() and not l.startswith(("c", "p"))]
    occ = defaultdict(list)
    for ci, c in enumerate(clauses):
        for l in c: occ[abs(l)].append(ci)
    big = {ci for ci, c in enumerate(clauses) if all(l > E for l in c) and len(c) == m * (n - k)}
    base = set(big)
    for ci in big:
        for d in clauses[ci]:
            base.update(cj for cj in occ[d])
    added = [c for ci, c in enumerate(clauses) if ci not in base]
    idx = {p: i for i, p in enumerate(pairs)}
    def var(t, i, j): return 1 + t * P + idx[(i, j)]
    return added, var

def units(T, m, n, var):
    out = []
    for t in range(m):
        for i in range(n):
            for j in range(i + 1, n):
                out.append(var(t, i, j) if T[t][i][j] else -var(t, i, j))
    return out

def relabel(T, perm, order):
    """perm[old] = new label; order = list of old tournament indices in new order."""
    n = len(perm); inv = [0] * n
    for old, new in enumerate(perm): inv[new] = old
    return [[[T[o][inv[a]][inv[b]] if a != b else 0 for b in range(n)] for a in range(n)] for o in order]

def canonical(T, m, n, rng):
    deg = [(sum(T[t][v]), t, v) for t in range(m) for v in range(n)]
    D = max(d for d, _, _ in deg); cands = [(t, v) for d, t, v in deg if d == D]; ts, vs = rng.choice(cands)
    order = [ts] + [t for t in range(m) if t != ts]
    O = [u for u in range(n) if u != vs and T[ts][vs][u]]; I = [u for u in range(n) if u != vs and not T[ts][vs][u]]
    rng.shuffle(O); rng.shuffle(I)
    if I:
        w = I[0]; Ir = I[1:]
        O = [u for u in O if T[ts][w][u]] + [u for u in O if not T[ts][w][u]]
        Ir = [u for u in Ir if T[ts][w][u]] + [u for u in Ir if not T[ts][w][u]]
        newlist = [vs] + O + [w] + Ir
    else:
        newlist = [vs] + O
    perm = [0] * n
    for new, old in enumerate(newlist): perm[old] = new
    T2 = relabel(T, perm, order)
    if D < n - 1 and m >= 3 and T2[2][0][1] and not T2[1][0][1]:
        T2[1], T2[2] = T2[2], T2[1]
    if D == n - 1 and m >= 2:
        Vp = list(range(1, n))
        deg2 = [(sum(T2[t][v][u] for u in Vp if u != v), t, v) for t in range(1, m) for v in Vp]
        D2 = max(d for d, _, _ in deg2); c2 = [(t, v) for d, t, v in deg2 if d == D2]; t2, v2 = rng.choice(c2)
        order2 = [0, t2] + [t for t in range(1, m) if t != t2]
        O2 = [u for u in Vp if u != v2 and T2[t2][v2][u]]; R2 = [u for u in Vp if u != v2 and not T2[t2][v2][u]]
        rng.shuffle(O2); rng.shuffle(R2)
        newlist2 = [0, v2] + O2 + R2
        perm2 = [0] * n
        for new, old in enumerate(newlist2): perm2[old] = new
        T2 = relabel(T2, perm2, order2)
    return T2

def random_tuple(m, n, rng, king=False):
    T = []
    for t in range(m):
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if rng.random() < 0.5: A[i][j] = 1
                else: A[j][i] = 1
        T.append(A)
    if king:  # force a vertex that beats everyone in some tournament (exercises the d = n-1 branch)
        t, v = rng.randrange(m), rng.randrange(n)
        for u in range(n):
            if u != v: T[t][v][u], T[t][u][v] = 1, 0
    return T

def main(path, m, k, n, trials, seed):
    rng = random.Random(seed); added, var = load(path, m, k, n)
    ok = 0; ctrl_unsat = 0; bad = 0
    with Solver(name="cadical195", bootstrap_with=added) as S:
        for i in range(trials):
            T = random_tuple(m, n, rng, king=(i % 3 == 0))
            C = canonical(T, m, n, rng)
            if S.solve(assumptions=units(C, m, n, var)): ok += 1
            else: bad += 1
            perm = list(range(n)); rng.shuffle(perm)
            R = relabel(T, perm, rng.sample(range(m), m))
            if not S.solve(assumptions=units(R, m, n, var)): ctrl_unsat += 1
    print(f"{path}: {len(added)} added clauses; canonical tuples accepted {ok}/{trials}; "
          f"random relabellings rejected {ctrl_unsat}/{trials}")
    print("SB AUDIT OK" if bad == 0 else "SB AUDIT FAIL"); return 0 if bad == 0 else 1

if __name__ == "__main__":
    a = sys.argv; sys.exit(main(a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]), int(a[6])))
