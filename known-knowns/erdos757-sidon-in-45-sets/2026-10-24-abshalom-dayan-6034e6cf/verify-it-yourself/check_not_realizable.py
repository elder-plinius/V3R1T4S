"""Exact check (Python standard library only) that H in object/H.json is not the A.P.-hypergraph H(A) of any weak
Sidon set A, hence (Proposition 2.2 of arXiv:2602.23282) of no (4,5)-set. Definitions from arXiv:2602.23282 (v2):
  weak Sidon       all sums x + y with x, y in A and x < y are distinct;
  Definition 1.7   the edges of H(A) are exactly the triples of A that form a 3-term arithmetic progression.
Argument, for S = {1, 2, 3, 4, 95, 97, 98, 99}:
  1. If H = H(A) under a bijection x: V(H) -> A, the induced subhypergraph H[S] is H(x(S)), because a 3-AP among
     points of x(S) is a 3-AP of A, hence an edge of H inside S, and conversely.
  2. Each edge e of H[S] is a 3-AP, so some vertex mu(e) of e is its middle: 2 x_mu(e) = sum of the other two.
     Distinct edges have distinct middles: if e != f had the same middle m, then x_u + x_v = x_u' + x_v' = 2 x_m with
     {u, v} != {u', v'}, two equal sums of two distinct elements, which a weak Sidon set does not allow.
  3. For every assignment mu with distinct middles, the linear system 2 x_mu(e) = x_u + x_v (one row per edge) is
     solved exactly over the rationals. If its solution space has dimension 2, it is {alpha v + beta 1} for one
     vector v; alpha != 0 because the points are distinct, and an affine map with alpha != 0 keeps both equalities
     and 3-APs, so x(S) has distinct points and exactly the edges of H[S] as 3-APs if and only if v does.
  4. The script checks that every such mu gives dimension 2 and a vector v with two equal entries or with a 3-AP on
     a triple that is not an edge. Then no mu is possible, so H is not H(A) for any weak Sidon set A.
Control: the same routine on H(A_base), the paper's 14-point set, must find the true middles realizable with v an
affine image of A_base, and every assignment it calls realizable must have H(v) equal to the hypergraph.
Usage: python3 check_not_realizable.py H.json   (last line PASS, exit 0; or FAIL, exit 1)"""
import sys, json, itertools
from fractions import Fraction

PIECE = [1, 2, 3, 4, 95, 97, 98, 99]
PIECE_EDGES = {(1, 2, 4), (1, 3, 98), (3, 4, 95), (2, 95, 97), (3, 97, 99), (2, 98, 99)}

def nullspace(rows, ncols):
    M = [[Fraction(a) for a in r] for r in rows]; piv = []; r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(M)) if M[i][c] != 0), None)
        if p is None: continue
        M[r], M[p] = M[p], M[r]; pv = M[r][c]; M[r] = [a / pv for a in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c] != 0:
                f = M[i][c]; M[i] = [a - f * b for a, b in zip(M[i], M[r])]
        piv.append(c); r += 1
    basis = []
    for f in (c for c in range(ncols) if c not in piv):
        v = [Fraction(0)] * ncols; v[f] = Fraction(1)
        for i, c in enumerate(piv): v[c] = -M[i][f]
        basis.append(v)
    return basis

def ap_triples(vals):
    return {frozenset(t) for t in itertools.combinations(range(len(vals)), 3)
            if (lambda s: s[0] + s[2] == 2 * s[1])(sorted(vals[i] for i in t))}

def classify(V, E, mids):
    """Returns (verdict, v): 'coincide', 'extra_ap', 'realizable', or 'dim<d>' when the dimension is not 2."""
    idx = {u: i for i, u in enumerate(V)}; rows = []
    for e, m in zip(E, mids):
        row = [0] * len(V)
        for u in e: row[idx[u]] += -2 if u == m else 1
        rows.append(row)
    B = nullspace(rows, len(V))
    if len(B) != 2: return "dim%d" % len(B), None
    v = next(b for b in B if len(set(b)) > 1)      # the all-ones vector is always a solution; take the other one
    if len(set(v)) < len(v): return "coincide", v
    edges = {frozenset(idx[u] for u in e) for e in E}
    if ap_triples(v) != edges: return "extra_ap", v
    return "realizable", v

def distinct_middle_assignments(E):
    def rec(i, used, mids):
        if i == len(E): yield list(mids); return
        for m in E[i]:
            if m not in used: yield from rec(i + 1, used | {m}, mids + [m])
    yield from rec(0, frozenset(), [])

def survey(V, E):
    counts = {}; real = []
    for mids in distinct_middle_assignments(E):
        verdict, v = classify(V, E, mids)
        counts[verdict] = counts.get(verdict, 0) + 1
        if verdict == "realizable": real.append(v)
    return counts, real

def main():
    ok = True
    A = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
    Aset = set(A)
    E0 = [(a, b, 2 * b - a) for a, b in itertools.combinations(A, 2) if 2 * b - a in Aset]
    verdict, v = classify(A, E0, [e[1] for e in E0])
    affine = verdict == "realizable" and all((A[i] - A[0]) * (v[1] - v[0]) == (v[i] - v[0]) * (A[1] - A[0]) for i in range(len(A)))
    counts0, real0 = survey(A, E0)
    consistent = all(ap_triples(w) == {frozenset(A.index(u) for u in e) for e in E0} for w in real0)
    cal = affine and counts0.get("realizable", 0) > 0 and consistent
    print("control A_base: m", len(E0), "true middles", verdict, "affine image of A_base", affine,
          "assignments", counts0, "OK" if cal else "BAD")
    ok &= cal
    d = json.load(open(sys.argv[1]))
    E = sorted(tuple(sorted(e)) for e in d["edges"] if set(e) <= set(PIECE))
    piece_ok = set(E) == PIECE_EDGES
    print("object: induced edges on", PIECE, E, "as stated" if piece_ok else "NOT as stated")
    ok &= piece_ok
    counts, real = survey(PIECE, E)
    total = sum(counts.values())
    bad = set(counts) - {"coincide", "extra_ap"}
    print("object: distinct-middle assignments", total, counts)
    ok &= total > 0 and not bad and not real
    print("not H(A) for any weak Sidon set A:", ok)
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

main()
