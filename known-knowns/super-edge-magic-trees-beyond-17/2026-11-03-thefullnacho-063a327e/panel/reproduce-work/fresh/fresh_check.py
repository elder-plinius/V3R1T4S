#!/usr/bin/env python3
"""Fresh REPRODUCE checker, written from the definition only.
Definition: a graph with p vertices and q edges is super edge-magic iff there is a bijection
f: V -> {1..p} whose q edge sums f(u)+f(v) are q consecutive integers.
For each line 'n;u-v,...;l0,...,l(n-1)[;...]': check tree (n-1 distinct edges, no loops, connected),
labels a permutation of 1..n, edge sums = {s, s+1, ..., s+n-2}. Canonical form: centre(s) by leaf
peeling, AHU parenthesis code rooted at centre (bicentre: rooted at the central edge, min of both orientations).
Counts distinct canonical forms and compares with A000055(n) computed here by Otter's formula."""
import sys
from collections import deque

def rooted_counts(N):
    # A000081: a(1)=1, a(n+1) = (1/n) sum_{k=1..n} (sum_{d|k} d a(d)) a(n-k+1)
    a = [0]*(N+2); a[1] = 1
    for n in range(1, N+1):
        s = 0
        for k in range(1, n+1):
            sd = sum(d*a[d] for d in range(1, k+1) if k % d == 0)
            s += sd*a[n-k+1]
        a[n+1] = s//n
    return a

def free_trees(n):
    a = rooted_counts(n+1)
    # Otter: t(n) = a(n) - sum_{i<j, i+j=n} a(i)a(j) - [n even] C(a(n/2),2)... standard form:
    # t(n) = a(n) - (sum_{k=0..n} a(k)a(n-k) - [n even] a(n/2)) / 2
    s = sum(a[k]*a[n-k] for k in range(0, n+1))
    if n % 2 == 0:
        s -= a[n//2]
    return a[n] - s//2

def code(adj, root, parent):
    # iterative AHU
    order = []; stack = [(root, parent)]; par = {root: parent}
    while stack:
        v, p = stack.pop(); order.append(v)
        for w in adj[v]:
            if w != p:
                par[w] = v; stack.append((w, v))
    c = {}
    for v in reversed(order):
        kids = sorted(c[w] for w in adj[v] if w != par[v])
        c[v] = "(" + "".join(kids) + ")"
    return c[root]

def canon(n, adj):
    deg = [len(x) for x in adj]
    leaves = [v for v in range(n) if deg[v] <= 1]
    remaining = n; removed = [False]*n
    while remaining > 2:
        nxt = []
        for v in leaves:
            removed[v] = True; remaining -= 1
            for w in adj[v]:
                if not removed[w]:
                    deg[w] -= 1
                    if deg[w] == 1: nxt.append(w)
        leaves = nxt
    centres = [v for v in range(n) if not removed[v]]
    if len(centres) == 1:
        return "C" + code(adj, centres[0], -1)
    a, b = centres
    x, y = code(adj, a, b), code(adj, b, a)
    return "E" + min(x, y) + max(x, y)

def check(path, n):
    stats = dict(lines=0, bad_parse=0, wrong_n=0, not_tree=0, bad_labels=0, bad_sums=0, dup=0)
    seen = set()
    with open(path) as fh:
        for ln in fh:
            ln = ln.strip()
            if not ln: continue
            stats['lines'] += 1
            try:
                f = ln.split(';')
                m = int(f[0])
                edges = [tuple(int(t) for t in e.split('-')) for e in f[1].split(',')]
                lab = [int(t) for t in f[2].split(',')]
                assert all(len(e) == 2 for e in edges)
            except Exception:
                stats['bad_parse'] += 1; continue
            if m != n or len(lab) != n:
                stats['wrong_n'] += 1; continue
            adj = [[] for _ in range(n)]; es = set(); ok = len(edges) == n-1
            for u, v in edges:
                if not (0 <= u < n and 0 <= v < n) or u == v or (min(u,v), max(u,v)) in es:
                    ok = False; break
                es.add((min(u,v), max(u,v))); adj[u].append(v); adj[v].append(u)
            if ok:
                vis = [False]*n; vis[0] = True; dq = deque([0]); cnt = 1
                while dq:
                    v = dq.popleft()
                    for w in adj[v]:
                        if not vis[w]: vis[w] = True; cnt += 1; dq.append(w)
                ok = cnt == n
            if not ok:
                stats['not_tree'] += 1; continue
            if sorted(lab) != list(range(1, n+1)):
                stats['bad_labels'] += 1; continue
            sums = sorted(lab[u]+lab[v] for u, v in edges)
            if sums != list(range(sums[0], sums[0]+n-1)):
                stats['bad_sums'] += 1; continue
            c = canon(n, adj)
            if c in seen: stats['dup'] += 1
            else: seen.add(c)
    exp = free_trees(n)
    good = all(stats[k] == 0 for k in stats if k != 'lines') and len(seen) == exp == stats['lines']
    print(f"n={n} " + " ".join(f"{k}={v}" for k, v in stats.items()) + f" distinct={len(seen)} expected_A000055={exp} -> {'PASS' if good else 'FAIL'}", flush=True)
    return good

if __name__ == '__main__':
    if sys.argv[1] == 'counts':
        for n in range(1, 21): print(n, free_trees(n))
        sys.exit(0)
    if sys.argv[1] == 'calib':
        import tempfile, os
        d = tempfile.mkdtemp()
        cases = {
          'pos': "4;0-1,1-2,2-3;1,3,2,4\n4;0-1,0-2,0-3;1,2,3,4\n",          # P4 sums 4,5,6; K13 sums 3,4,5
          'badsum': "4;0-1,1-2,2-3;1,2,3,4\n4;0-1,0-2,0-3;1,2,3,4\n",       # P4 sums 3,5,7
          'dup': "4;0-1,1-2,2-3;1,3,2,4\n4;3-2,2-0,0-1;4,3,2,1\n",          # second is P4 relabelled (sums 4,5,6? check)
          'cycle': "4;0-1,1-2,2-0;1,2,3,4\n4;0-1,0-2,0-3;1,2,3,4\n",
          'badlab': "4;0-1,1-2,2-3;1,3,3,4\n4;0-1,0-2,0-3;1,2,3,4\n",
        }
        for k, s in cases.items():
            p = os.path.join(d, k); open(p, 'w').write(s); print(k, end=': '); check(p, 4)
        sys.exit(0)
    n = int(sys.argv[1]); sys.exit(0 if check(sys.argv[2], n) else 1)
