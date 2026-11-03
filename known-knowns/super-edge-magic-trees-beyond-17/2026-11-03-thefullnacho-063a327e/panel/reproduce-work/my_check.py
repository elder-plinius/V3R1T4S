#!/usr/bin/env python3
# REPRODUCE skeptic's own checker, written from the definition quoted in panel/reproduce.md.
# Different methods from the package checker: union-find tree test, set-based label/sum test,
# centroid-rooted AHU with integer class ids. Usage: my_check.py N EXPECTED_COUNT FILE
import sys
n_exp, count_exp, path = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
ids = {}
def find(p, x):
    while p[x] != x: p[x] = p[p[x]]; x = p[x]
    return x
def centroids(n, adj):
    # iterative subtree sizes from root 0
    order = [0]; par = [-1]*n; seen = [False]*n; seen[0] = True
    for u in order:
        for w in adj[u]:
            if not seen[w]: seen[w] = True; par[w] = u; order.append(w)
    size = [1]*n
    for u in reversed(order):
        if par[u] >= 0: size[par[u]] += size[u]
    res = []
    for u in range(n):
        m = n - size[u]
        for w in adj[u]:
            if w != par[u]: m = max(m, size[w])
        if 2*m <= n: res.append(u)
    return res
def rooted_id(adj, r):
    order = [r]; par = {r: -1}
    for u in order:
        for w in adj[u]:
            if w != par[u]: par[w] = u; order.append(w)
    kids = {u: [] for u in order}
    cid = {}
    for u in reversed(order):
        key = tuple(sorted(kids[u]))
        if key not in ids: ids[key] = len(ids)
        cid[u] = ids[key]
        if par[u] >= 0: kids[par[u]].append(cid[u])
    return cid[r]
stats = dict(lines=0, bad_parse=0, wrong_n=0, not_tree=0, bad_labels=0, bad_sums=0, dup=0)
canon = set()
for line in open(path):
    if not line.strip(): continue
    stats["lines"] += 1
    try:
        f = line.rstrip("\n").split(";")
        n = int(f[0]); E = [tuple(int(y) for y in x.split("-")) for x in f[1].split(",")]
        L = [int(y) for y in f[2].split(",")]
        assert all(len(e) == 2 for e in E)
    except Exception:
        stats["bad_parse"] += 1; continue
    if n != n_exp: stats["wrong_n"] += 1; continue
    p = list(range(n)); ok = len(E) == n-1
    for u, v in E:
        if not (0 <= u < n and 0 <= v < n) or u == v: ok = False; break
        a, b = find(p, u), find(p, v)
        if a == b: ok = False; break
        p[a] = b
    if not ok: stats["not_tree"] += 1; continue
    if len(L) != n or set(L) != set(range(1, n+1)): stats["bad_labels"] += 1; continue
    S = [L[u]+L[v] for u, v in E]
    if len(set(S)) != n-1 or max(S)-min(S) != n-2: stats["bad_sums"] += 1; continue
    adj = [[] for _ in range(n)]
    for u, v in E: adj[u].append(v); adj[v].append(u)
    key = min(rooted_id(adj, c) for c in centroids(n, adj))
    if key in canon: stats["dup"] += 1
    canon.add(key)
good = stats["lines"] == count_exp == len(canon) and not any(stats[k] for k in stats if k != "lines")
print("n=%d %s distinct=%d expected=%d -> %s" % (n_exp, " ".join("%s=%d" % kv for kv in stats.items()), len(canon), count_exp, "PASS" if good else "FAIL"))
