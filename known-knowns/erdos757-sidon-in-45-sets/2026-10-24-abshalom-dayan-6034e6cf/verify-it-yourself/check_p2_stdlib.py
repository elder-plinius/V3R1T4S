"""Standalone checker (Python standard library only) for an abstract hypergraph offered as partial win p2 of
erdos757-sidon-in-45-sets. Written from the definitions in arXiv:2602.23282 (v2):
  Definition 1.7  the A.P.-hypergraph is 3-uniform on the ordered set a_1 < ... < a_n;
  Lemma 2.4       the midpoint map is injective and never hits a_1 or a_n (so m <= n - 2);
  Lemma 2.5       linear: two distinct edges share at most one vertex;
  Lemma 5.2       no subhypergraph isomorphic to F7 = {012, 034, 056, 135, 246}.
For an abstract H the vertex labels 0..n-1 play the order, so the middle of an edge is its median label.
alpha(H) is computed exactly by a frontier dynamic program over a greedy vertex order (exact for any order).
Calibration: the A.P.-hypergraph of the paper's 14-point set A_base must pass every property with alpha = 8.
Usage: python3 check_p2_stdlib.py H.json [claimed_alpha]   (last line PASS, exit 0; or FAIL, exit 1)"""
import sys, json, itertools
from fractions import Fraction

F7 = [(0, 1, 2), (0, 3, 4), (0, 5, 6), (1, 3, 5), (2, 4, 6)]

def properties(n, E):
    r = {}
    r["three_uniform"] = all(len(e) == 3 and len(set(e)) == 3 and all(isinstance(v, int) and 0 <= v < n for v in e) for e in E)
    S = [tuple(sorted(e)) for e in E]
    r["edges_distinct"] = len(set(S)) == len(S)
    pairs = {}
    for e in S:
        for pr in itertools.combinations(e, 2):
            pairs[pr] = pairs.get(pr, 0) + 1
    r["linear"] = all(c <= 1 for c in pairs.values())
    mids = [e[1] for e in S]
    r["middles_distinct"] = len(set(mids)) == len(mids)
    r["middles_not_first_or_last"] = all(0 < x < n - 1 for x in mids)
    r["m_at_most_n_minus_2"] = len(S) <= n - 2
    if all(r.values()):
        r["f7_free"] = f7_embedding(n, S) is None   # only searched on linear inputs with distinct middles
    else:
        r["f7_free"] = None
    return r, S

def f7_embedding(n, S):
    es = set(S); inc = [[] for _ in range(n)]
    for e in S:
        for v in e: inc[v].append(e)
    def rec(i, phi, used):
        if i == len(F7): return dict(phi)
        f = F7[i]; img = [phi.get(v) for v in f]
        if all(x is not None for x in img):
            return rec(i + 1, phi, used) if tuple(sorted(img)) in es else None
        known = [x for x in img if x is not None]
        cands = S if not known else inc[known[0]]
        for e in cands:
            for perm in itertools.permutations(e):
                ok = True; new = {}
                for v, h in zip(f, perm):
                    if v in phi:
                        if phi[v] != h: ok = False; break
                    elif h in used or h in new.values(): ok = False; break
                    else: new[v] = h
                if ok:
                    phi2 = dict(phi); phi2.update(new)
                    res = rec(i + 1, phi2, used | set(new.values()))
                    if res: return res
        return None
    return rec(0, {}, set())

def alpha_exact(n, S):
    inc = [[] for _ in range(n)]
    for e in S:
        for v in e: inc[v].append(e)
    decided = set(); frontier = []
    states = {frozenset(): 0}
    remaining = set(range(n))
    while remaining:
        # greedy: next vertex that keeps the frontier smallest
        def cost(v):
            d2 = decided | {v}
            fr = [u for u in set(frontier) | {v} if any(w not in d2 for e in inc[u] for w in e)]
            return (len(fr), v)
        v = min(remaining, key=cost)
        remaining.discard(v); decided.add(v)
        new = {}
        for ch, val in states.items():
            new[ch] = max(new.get(ch, -1), val)                       # v excluded
            ok = all(not (all(w in ch for w in e if w != v)) for e in inc[v])
            if ok:
                c2 = ch | {v}
                new[c2] = max(new.get(c2, -1), val + 1)               # v included
        frontier = [u for u in set(frontier) | {v} if any(w not in decided for e in inc[u] for w in e)]
        fs = set(frontier)
        states = {}
        for ch, val in new.items():
            k = frozenset(x for x in ch if x in fs)
            if val > states.get(k, -1): states[k] = val
    return max(states.values())

def ap_hypergraph(A):
    A = sorted(A); idx = {a: i for i, a in enumerate(A)}
    return len(A), [(idx[a], idx[b], idx[2 * b - a]) for a, b in itertools.combinations(A, 2) if 2 * b - a in idx]

def main():
    ok = True
    A_base = [0, 136, 200, 243, 246, 249, 272, 286, 298, 323, 400, 528, 596, 1056]
    n0, E0 = ap_hypergraph(A_base)
    r0, S0 = properties(n0, E0); a0 = alpha_exact(n0, S0)
    cal = all(r0.values()) and a0 == 8
    print("calibration A_base: n", n0, "m", len(S0), r0, "alpha", a0, "OK" if cal else "BAD")
    ok &= cal
    d = json.load(open(sys.argv[1])); n = d["n"]; E = [tuple(e) for e in d["edges"]]
    r, S = properties(n, E)
    print("object: n", n, "m", len(S), r)
    ok &= all(r.values())
    if not ok:
        print("FAIL"); sys.exit(1)
    a = alpha_exact(n, S)
    claimed = int(sys.argv[2]) if len(sys.argv) > 2 else None
    ratio = Fraction(a, n)
    print("alpha", a, "claimed", claimed, "ratio", ratio, "below 5/9:", ratio < Fraction(5, 9), "below 4/7:", ratio < Fraction(4, 7),
          "at least 9/17:", ratio >= Fraction(9, 17))
    if claimed is not None: ok &= (a == claimed)
    ok &= ratio < Fraction(5, 9) and ratio >= Fraction(9, 17)
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)

main()
