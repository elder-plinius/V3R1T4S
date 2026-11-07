"""CEGAR search for an abstract block whose 2-point self-similar chain has growth <= c = C/D per n0-2 new vertices.
Block: vertices 0..n0-1 in label order; edges (i,j,k), i<j<k, middle j; at most one edge per middle (Lemma 2.4),
linear (Lemma 2.5); F7-free (Lemma 5.2) by lazy cuts. Anchors u=0, w=n0-1 (never middles) are glued onto the
out-pair (p,q) of the previous copy. Cut linearity: not both an edge through {p,q} and one through {0,n0-1}.
Transfer matrix M[s][t] = max |I minus {0,n0-1}| over independent I with s = state(0,n0-1), t = state(p,q).
Chain growth = max cycle mean of M <= c  iff  exists integer psi with D*M[s][t] <= C + psi[t] - psi[s].
psi is a CP-SAT variable; every violating independent set I yields the cut: I contains an edge OR the psi inequality.
Usage: cegar.py n0 C D p q timelimit_total [maxm]"""
import sys, time, itertools
from ortools.sat.python import cp_model

def f7_find(n, edges):
    es = set(tuple(sorted(e)) for e in edges)
    inc = {v: [e for e in es if v in e] for v in range(n)}
    for c in range(n):
        for e1, e2, e3 in itertools.combinations(inc[c], 3):
            r = [tuple(x for x in e if x != c) for e in (e1, e2, e3)]
            for a in (0, 1):
                for b in (0, 1):
                    x = tuple(sorted((r[0][0], r[1][a], r[2][b]))); y = tuple(sorted((r[0][1], r[1][1 - a], r[2][1 - b])))
                    if x in es and y in es:
                        return [e1, e2, e3, x, y]
    return None

def indep_table(n, edges, p, q):
    em = [(1 << a) | (1 << b) | (1 << c) for a, b, c in edges]
    best = {}
    full = (1 << n) - 1
    u, w = 0, n - 1
    for I in range(1 << n):
        ok = True
        for e in em:
            if I & e == e:
                ok = False; break
        if not ok:
            continue
        s = 2 * ((I >> u) & 1) + ((I >> w) & 1); t = 2 * ((I >> p) & 1) + ((I >> q) & 1)
        v = bin(I).count("1") - ((I >> u) & 1) - ((I >> w) & 1)
        if (s, t) not in best or v > best[(s, t)][0]:
            best[(s, t)] = (v, [I])
        elif v == best[(s, t)][0] and len(best[(s, t)][1]) < 40:
            best[(s, t)][1].append(I)
    return best

def karp(M):
    from fractions import Fraction
    NEG = None
    D = [[0] * 4]
    for k in range(1, 5):
        row = []
        for v in range(4):
            b = None
            for uu in range(4):
                if D[k - 1][uu] is not None and M[uu][v] is not None:
                    x = D[k - 1][uu] + M[uu][v]
                    b = x if b is None or x > b else b
            row.append(b)
        D.append(row)
    best = None
    for v in range(4):
        if D[4][v] is None:
            continue
        mn = None
        for k in range(4):
            if D[k][v] is None:
                continue
            val = Fraction(D[4][v] - D[k][v], 4 - k)
            mn = val if mn is None or val < mn else mn
        if mn is not None and (best is None or mn > best):
            best = mn
    return best

def main():
    n0, C, D, p, q, TL = map(int, sys.argv[1:7]); maxm = int(sys.argv[7]) if len(sys.argv) > 7 else n0 - 2
    t0 = time.time()
    md = cp_model.CpModel()
    trip = [(i, j, k) for j in range(1, n0 - 1) for i in range(j) for k in range(j + 1, n0)]
    x = {e: md.NewBoolVar("x%d_%d_%d" % e) for e in trip}
    for j in range(1, n0 - 1):
        md.Add(sum(x[e] for e in trip if e[1] == j) <= 1)
    for a, b in itertools.combinations(range(n0), 2):
        md.Add(sum(x[e] for e in trip if a in e and b in e) <= 1)
    md.Add(sum(x[e] for e in trip if p in e and q in e) + sum(x[e] for e in trip if 0 in e and n0 - 1 in e) <= 1)
    md.Add(sum(x.values()) <= maxm)
    psi = [md.NewIntVar(-4 * D, 4 * D, "psi%d" % s) for s in range(4)]
    md.Add(psi[0] == 0)
    it = 0; ncuts = 0
    while True:
        it += 1
        left = TL - (time.time() - t0)
        if left <= 1:
            print("RESULT TIMEOUT iters", it, "cuts", ncuts, flush=True); return
        sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = left; sol.parameters.num_workers = 2
        st = sol.Solve(md)
        if st == cp_model.INFEASIBLE:
            print("RESULT INFEASIBLE iters", it, "cuts", ncuts, "time %.1f" % (time.time() - t0), flush=True); return
        if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
            print("RESULT", sol.StatusName(st), "iters", it, "cuts", ncuts, flush=True); return
        edges = [e for e in trip if sol.Value(x[e])]
        f7 = f7_find(n0, edges)
        if f7:
            md.Add(sum(x[tuple(sorted(e))] for e in f7) <= 4); ncuts += 1; continue
        tab = indep_table(n0, edges, p, q)
        M = [[tab[(s, t)][0] if (s, t) in tab else None for t in range(4)] for s in range(4)]
        g = karp(M)
        from fractions import Fraction
        if g is not None and g <= Fraction(C, D):
            print("RESULT FOUND n0", n0, "p q", p, q, "m", len(edges), "g", g, "ratio", g / (n0 - 2), "edges", edges, "M", M,
                  "iters", it, "time %.1f" % (time.time() - t0), flush=True); return
        # add cuts for every (s,t) entry: I contains an edge OR D*v <= C + psi[t]-psi[s]
        added = 0
        for (s, t), (v, Is) in tab.items():
            for I in Is:
                inside = [x[e] for e in trip if all((I >> z) & 1 for z in e)]
                b = md.NewBoolVar("")
                md.Add(D * v <= C + psi[t] - psi[s]).OnlyEnforceIf(b.Not())
                if inside:
                    md.AddBoolOr(inside).OnlyEnforceIf(b)
                else:
                    md.Add(b == 0)
                added += 1
        ncuts += added
        if it % 20 == 0:
            print("iter", it, "m", len(edges), "g", g, "cuts", ncuts, "t %.0f" % (time.time() - t0), flush=True)

main()
