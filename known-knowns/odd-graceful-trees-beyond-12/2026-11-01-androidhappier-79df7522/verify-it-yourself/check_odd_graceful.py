#!/usr/bin/env python3
"""Standalone checker for odd-graceful tree certificates (Python 3 standard library only).

Definition (Gnanajothi 1991, as quoted in Gallian's Dynamic Survey DS6, Section 3.6): a graph with q edges is
odd-graceful if there is an injection f from V to {0, 1, ..., 2q-1} such that the edge labels |f(x)-f(y)| are
exactly {1, 3, 5, ..., 2q-1}. A tree on n vertices has q = n-1 edges.

Certificate format (gzip or plain text), one tree per line:
    p_1 p_2 ... p_{n-1} | f(0) f(1) ... f(n-1)
p_i is the parent of vertex i (0 <= p_i < i, so the edges i--p_i always form a tree on vertices 0..n-1), and f(v)
is the label of vertex v.

For order n the checker verifies, for every line: exact token counts, 0 <= p_i < i, labels pairwise distinct in
[0, 2n-3], and the n-1 edge differences equal {1, 3, ..., 2n-3} exactly. It computes a canonical form of each tree
(AHU code rooted at the centre, minimum over the one or two centres), rejects any duplicate tree, and requires
the number of lines = the number of distinct trees = t(n), the number of unlabeled trees on n vertices, computed
here from Otter's formula (OEIS A000055). n distinct isomorphism classes out of t(n) possible means every
unlabeled tree on n vertices appears exactly once.

Usage: check_odd_graceful.py n certfile      (exit 0 and a line ending PASS, or exit 1 and FAIL)
"""
import gzip
import sys


def rooted_counts(N):
    # A000081: r[1] = 1, r[n+1] = (1/n) sum_{k=1..n} (sum_{d|k} d r[d]) r[n-k+1]
    r = [0] * (N + 2)
    r[1] = 1
    for n in range(1, N):
        s = 0
        for k in range(1, n + 1):
            s += sum(d * r[d] for d in range(1, k + 1) if k % d == 0) * r[n - k + 1]
        r[n + 1] = s // n
    return r


def free_trees(n):
    # Otter: t(n) = r(n) - (1/2) sum_{i+j=n} r(i) r(j) + [n even] (1/2) r(n/2)
    r = rooted_counts(n + 1)
    s = sum(r[i] * r[n - i] for i in range(1, n))
    x = 2 * r[n] - s + (r[n // 2] if n % 2 == 0 else 0)
    assert x % 2 == 0
    return x // 2


def canon(par, n):
    adj = [[] for _ in range(n)]
    for i in range(1, n):
        p = par[i - 1]
        adj[i].append(p)
        adj[p].append(i)
    deg = [len(a) for a in adj]
    alive = [True] * n
    leaves = [v for v in range(n) if deg[v] <= 1]
    rem = n
    while rem > 2:
        nxt = []
        for v in leaves:
            alive[v] = False
            rem -= 1
            for w in adj[v]:
                if alive[w]:
                    deg[w] -= 1
                    if deg[w] == 1:
                        nxt.append(w)
        leaves = nxt
    best = None
    for c in range(n):
        if not alive[c]:
            continue
        # iterative post-order AHU encoding rooted at c
        order, parent = [c], {c: -1}
        k = 0
        while k < len(order):
            u = order[k]
            k += 1
            for w in adj[u]:
                if w != parent[u]:
                    parent[w] = u
                    order.append(w)
        code = {}
        for u in reversed(order):
            code[u] = "(" + "".join(sorted(code[w] for w in adj[u] if w != parent[u])) + ")"
        if best is None or code[c] < best:
            best = code[c]
    return best


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    n = int(sys.argv[1])
    path = sys.argv[2]
    opener = gzip.open if path.endswith(".gz") else open
    top = 2 * n - 3
    want = list(range(1, top + 1, 2))
    seen = set()
    lines = 0
    bad = None
    with opener(path, "rt") as f:
        for line in f:
            lines += 1
            try:
                a, b = line.split("|")
                par = [int(x) for x in a.split()]
                lab = [int(x) for x in b.split()]
            except ValueError:
                bad = "line %d: cannot parse" % lines
                break
            if len(par) != n - 1 or len(lab) != n:
                bad = "line %d: wrong number of entries" % lines
                break
            if any(not (0 <= par[i - 1] < i) for i in range(1, n)):
                bad = "line %d: parent array is not a tree on 0..n-1" % lines
                break
            if len(set(lab)) != n or min(lab) < 0 or max(lab) > top:
                bad = "line %d: labels not distinct in [0, %d]" % (lines, top)
                break
            if sorted(abs(lab[i] - lab[par[i - 1]]) for i in range(1, n)) != want:
                bad = "line %d: edge differences are not {1, 3, ..., %d}" % (lines, top)
                break
            c = canon(par, n)
            if c in seen:
                bad = "line %d: duplicate tree" % lines
                break
            seen.add(c)
    t = free_trees(n)
    if bad is None and not (lines == len(seen) == t):
        bad = "lines %d, distinct trees %d, but A000055(%d) = %d" % (lines, len(seen), n, t)
    if bad:
        print("order %d: %s FAIL" % (n, bad))
        sys.exit(1)
    print("order %d: %d lines, %d distinct odd-gracefully labelled trees, A000055(%d) = %d (Otter) PASS"
          % (n, lines, len(seen), n, t))


if __name__ == "__main__":
    main()
