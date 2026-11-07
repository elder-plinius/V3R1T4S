#!/usr/bin/env python3
"""Criterion-skeptic's own checker, written from the definition without reading the
author's canonical-form code paths. For one certificate file of order n:
  - every line: n field == N, exactly N-1 edges, endpoints in 0..N-1, connected (BFS) => tree
  - labels: exactly N ints, multiset == {1..N}
  - edge sums: sorted == m, m+1, ..., m+N-2  (N-1 consecutive integers, hence distinct)
  - canonical form: centre by leaf peeling; AHU parenthesis string; bicentral -> edge-rooted
    form "B" + min/max of the two half codes
  - distinct canonical forms == lines == A000055(N), where A000055 is computed here from
    the Euler transform for rooted trees (A000081) and Otter's dissimilarity formula.
Also reports min edge sum distribution (k = magic constant info) for sanity.
"""
import sys, lzma

def a81(N):
    r = [0, 1] + [0] * N
    for n in range(1, N + 1):
        s = 0
        for k in range(1, n + 1):
            s += sum(d * r[d] for d in range(1, k + 1) if k % d == 0) * r[n - k + 1]
        r[n + 1] = s // n
    return r

def a55(n):
    r = a81(n)
    s = sum(r[i] * r[n - i] for i in range(1, n))
    if n % 2 == 0:
        s -= r[n // 2]
    return r[n] - s // 2

def code(adj, root, par):
    # iterative AHU
    order = []; stack = [(root, par)]; parent = {root: par}
    while stack:
        v, p = stack.pop(); order.append(v)
        for w in adj[v]:
            if w != p:
                parent[w] = v; stack.append((w, v))
    c = {}
    for v in reversed(order):
        kids = sorted(c.pop(w) for w in adj[v] if w != parent[v])
        c[v] = "(" + "".join(kids) + ")"
    return c[root]

def main():
    path, N = sys.argv[1], int(sys.argv[2])
    op = lzma.open if path.endswith(".xz") else open
    seen = set(); lines = bad = 0; firstbad = None
    with op(path, "rt") as f:
        for raw in f:
            if not raw.strip():
                continue
            lines += 1
            try:
                fs = raw.rstrip("\n").split(";")
                assert int(fs[0]) == N
                E = []
                for e in fs[1].split(","):
                    u, v = e.split("-"); u = int(u); v = int(v)
                    assert 0 <= u < N and 0 <= v < N and u != v
                    E.append((u, v))
                assert len(E) == N - 1
                L = [int(x) for x in fs[2].split(",")]
                assert len(L) == N and sorted(L) == list(range(1, N + 1))
                adj = [[] for _ in range(N)]
                for u, v in E:
                    adj[u].append(v); adj[v].append(u)
                vis = [False] * N; vis[0] = True; st = [0]; cnt = 1
                while st:
                    x = st.pop()
                    for y in adj[x]:
                        if not vis[y]:
                            vis[y] = True; cnt += 1; st.append(y)
                assert cnt == N
                S = sorted(L[u] + L[v] for u, v in E)
                assert S == list(range(S[0], S[0] + N - 1))
                # centre by leaf peeling
                deg = [len(a) for a in adj]; rem = N; layer = [v for v in range(N) if deg[v] == 1]
                gone = [False] * N
                while rem > 2:
                    nxt = []
                    for v in layer:
                        gone[v] = True; rem -= 1
                        for w in adj[v]:
                            if not gone[w]:
                                deg[w] -= 1
                                if deg[w] == 1:
                                    nxt.append(w)
                    layer = nxt
                cs = [v for v in range(N) if not gone[v]]
                if len(cs) == 1:
                    k = "U" + code(adj, cs[0], -1)
                else:
                    a, b = cs
                    ca, cb = code(adj, a, b), code(adj, b, a)
                    k = "B" + min(ca, cb) + "|" + max(ca, cb)
            except AssertionError:
                bad += 1; firstbad = firstbad or lines; continue
            seen.add(k)
    A = a55(N)
    ok = bad == 0 and lines == len(seen) == A
    print(f"n={N} lines={lines} distinct={len(seen)} A000055={A} bad={bad} firstbad={firstbad} -> {'PASS' if ok else 'FAIL'}")

main()
