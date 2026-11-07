#!/usr/bin/env python3
"""Independent checker (written before reading claim/checkers/).
Definition checked (CLAIM.md): "every unlabeled tree on n vertices (A000055(n) of them) with a
bijection from its vertices to {1..n} whose n-1 edge sums are consecutive integers".
"""
import sys, lzma, itertools
from array import array

def rooted_counts(N):
    # A000081: a(1)=1, a(n+1) = (1/n) sum_{k=1..n} (sum_{d|k} d a(d)) a(n-k+1)
    a = [0]*(N+1); a[1] = 1
    for n in range(1, N):
        s = 0
        for k in range(1, n+1):
            sd = sum(d*a[d] for d in range(1, k+1) if k % d == 0)
            s += sd * a[n-k+1]
        assert s % n == 0
        a[n+1] = s // n
    return a

def free_count(n, a):
    # Otter: t(n) = r(n) - (sum_{i=1}^{n-1} r(i) r(n-i) - [n even] r(n/2)) / 2
    s = sum(a[i]*a[n-i] for i in range(1, n))
    if n % 2 == 0:
        s -= a[n//2]
    assert s % 2 == 0
    return a[n] - s//2

def canon(n, adj):
    # centers by leaf peeling
    deg = [len(x) for x in adj]
    leaves = [v for v in range(n) if deg[v] <= 1]
    rem = n
    while rem > 2:
        rem -= len(leaves)
        nl = []
        for v in leaves:
            for w in adj[v]:
                deg[w] -= 1
                if deg[w] == 1:
                    nl.append(w)
        leaves = nl
    best = None
    for c in leaves:
        # iterative AHU from root c
        parent = [-1]*n; order = [c]; parent[c] = c
        i = 0
        while i < len(order):
            v = order[i]; i += 1
            for w in adj[v]:
                if parent[w] == -1:
                    parent[w] = v; order.append(w)
        code = [None]*n
        kids = [[] for _ in range(n)]
        for v in reversed(order):
            ks = kids[v]; ks.sort()
            code[v] = "1" + "".join(ks) + "0"
            if v != c:
                kids[parent[v]].append(code[v])
        s = code[c]
        if best is None or s < best:
            best = s
    return int(best, 2)   # fixed length 2n, leading '1' -> unique int

def check_line(line, n):
    f = line.split(";")
    if len(f) < 3: return "fields"
    if int(f[0]) != n: return "n field"
    es = f[1].split(",")
    if len(es) != n-1: return "edge count"
    labs = list(map(int, f[2].split(",")))
    if len(labs) != n: return "label count"
    if sorted(labs) != list(range(1, n+1)): return "labels not bijection onto 1..n"
    adj = [[] for _ in range(n)]
    seen = set(); sums = []
    for e in es:
        u, v = e.split("-"); u = int(u); v = int(v)
        if not (0 <= u < n and 0 <= v < n) or u == v: return "bad vertex"
        k = (min(u,v), max(u,v))
        if k in seen: return "dup edge"
        seen.add(k)
        adj[u].append(v); adj[v].append(u)
        sums.append(labs[u]+labs[v])
    # connectivity (n-1 edges + connected => tree)
    st = [0]; vis = [False]*n; vis[0] = True; c = 1
    while st:
        x = st.pop()
        for y in adj[x]:
            if not vis[y]:
                vis[y] = True; c += 1; st.append(y)
    if c != n: return "not connected"
    ss = sorted(sums)
    if any(ss[i+1] != ss[i]+1 for i in range(len(ss)-1)): return "sums not consecutive"
    return canon(n, adj)

def check_file(path, n, expect):
    op = lzma.open if path.endswith(".xz") else open
    codes = array("Q"); lines = 0; bad = 0; firstbad = None
    with op(path, "rt") as fh:
        for line in fh:
            line = line.strip()
            if not line: continue
            lines += 1
            r = check_line(line, n)
            if isinstance(r, str):
                bad += 1
                if firstbad is None: firstbad = (lines, r)
            else:
                codes.append(r)
    lst = sorted(codes); del codes
    dups = sum(1 for i in range(len(lst)-1) if lst[i] == lst[i+1])
    distinct = len(lst) - dups
    ok = bad == 0 and dups == 0 and lines == expect and distinct == expect
    print(f"n={n} file={path.split('claim/')[-1]} lines={lines} invalid={bad} first_invalid={firstbad} "
          f"iso_duplicates={dups} distinct={distinct} A000055={expect} -> {'OK' if ok else 'FAIL'}", flush=True)
    return ok

def selftest():
    a = rooted_counts(30)
    # brute force: all labelled trees via Pruefer sequences for n<=9, count iso classes
    for n in range(3, 10):
        cls = set()
        for seq in itertools.product(range(n), repeat=n-2):
            deg = [1]*n
            for x in seq: deg[x] += 1
            adj = [[] for _ in range(n)]
            d = deg[:]
            for x in seq:
                leaf = min(i for i in range(n) if d[i] == 1)
                adj[leaf].append(x); adj[x].append(leaf); d[leaf] -= 1; d[x] -= 1
            u, v = [i for i in range(n) if d[i] == 1]
            adj[u].append(v); adj[v].append(u)
            cls.add(canon(n, adj))
        print(f"selftest n={n} brute_classes={len(cls)} otter={free_count(n,a)}", flush=True)
        assert len(cls) == free_count(n, a)

if __name__ == "__main__":
    a = rooted_counts(30)
    if sys.argv[1] == "counts":
        for n in range(1, 26): print(n, free_count(n, a))
    elif sys.argv[1] == "selftest":
        selftest()
    else:
        n = int(sys.argv[1]); ok = check_file(sys.argv[2], n, free_count(n, a))
        sys.exit(0 if ok else 1)
