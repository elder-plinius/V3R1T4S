#!/usr/bin/env python3
"""Independent coverage + labeling verifier for super edge-magic certificates (adapted from run 2026-11-02-1526).
Trees are regenerated WITHOUT networkx: start from K2 and, for each order, attach a leaf to every vertex of every
tree of the previous order, deduplicating by an AHU canonical code rooted at the centre (min over both centres).
Counts are compared with A000055 from data/b000055.txt. Every certificate line (n;edges;labels;...) must be a tree
whose canonical code is in the regenerated set, every regenerated tree must appear exactly once, and every labeling
must pass check_sem.check (labels a bijection onto {1..n}, the q edge sums f(u)+f(v) exactly q consecutive integers)."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_sem import check, parse

def centres(adj):
    n = len(adj); deg = [len(a) for a in adj]; leaves = [v for v in range(n) if deg[v] <= 1]; rem = n
    removed = [False]*n
    while rem > 2:
        nl = []
        for v in leaves:
            removed[v] = True; rem -= 1
            for w in adj[v]:
                if not removed[w]:
                    deg[w] -= 1
                    if deg[w] == 1: nl.append(w)
        leaves = nl
    return [v for v in range(n) if not removed[v]]

def code(adj, r, p=-1):
    return "(" + "".join(sorted(code(adj, w, r) for w in adj[r] if w != p)) + ")"

def canon(adj):
    return min(code(adj, c) for c in centres(adj))

def adj_of(n, edges):
    a = [[] for _ in range(n)]
    for u, v in edges: a[u].append(v); a[v].append(u)
    return a

def is_tree(n, edges):
    if len(edges) != n-1: return False
    a = adj_of(n, edges); seen = {0}; st = [0]
    while st:
        u = st.pop()
        for w in a[u]:
            if w not in seen: seen.add(w); st.append(w)
    return len(seen) == n

def decode(c):
    """canonical code -> edge list"""
    edges = []; stack = []; k = 0
    for ch in c:
        if ch == "(":
            if stack: edges.append((stack[-1], k))
            stack.append(k); k += 1
        else: stack.pop()
    return k, edges

def generate(N):
    level = {canon(adj_of(2, [(0, 1)]))}
    out = {2: level}
    for n in range(3, N+1):
        nxt = set()
        for c in level:
            m, edges = decode(c)
            for v in range(m):
                e2 = edges + [(v, m)]
                nxt.add(canon(adj_of(n, e2)))
        out[n] = nxt; level = nxt
    return out

if __name__ == "__main__":
    bfile, certs = sys.argv[1], sys.argv[2:]
    A = {int(l.split()[0]): int(l.split()[1]) for l in open(bfile) if l.strip() and not l.startswith("#")}
    sys.setrecursionlimit(10000)
    byn = {}
    for cf in certs:
        for line in open(cf):
            if line.strip(): byn.setdefault(int(line.split(";")[0]), []).append((cf, line))
    gen = generate(max(byn))
    allok = True
    for n in sorted(byn):
        ref = gen[n]; seen = {}; fails = 0; nolab = 0
        for cf, line in byn[n]:
            nn, edges, labels_s = line.strip().split(";")[:3]
            nn = int(nn); edges = [tuple(map(int, x.split("-"))) for x in edges.split(",")]
            if not is_tree(nn, edges): fails += 1; continue
            c = canon(adj_of(nn, edges)); seen[c] = seen.get(c, 0)+1
            if not labels_s: nolab += 1; continue
            ok, why = check(nn, edges, list(map(int, labels_s.split(","))))
            if not ok: fails += 1
        dup = sum(1 for v in seen.values() if v > 1); missing = len(ref - set(seen)); extra = len(set(seen) - ref)
        good = len(ref) == A[n] and not missing and not extra and not dup and not fails and not nolab
        allok &= good
        print("n=%d regenerated=%d A000055=%d cert_lines=%d distinct=%d missing=%d extra=%d dup=%d unlabeled=%d label_failures=%d -> %s"
              % (n, len(ref), A[n], len(byn[n]), len(seen), missing, extra, dup, nolab, fails, "PASS" if good else "FAIL"))
    print("OVERALL:", "PASS" if allok else "FAIL")
