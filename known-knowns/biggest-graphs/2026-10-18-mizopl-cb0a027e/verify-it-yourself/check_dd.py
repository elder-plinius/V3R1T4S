#!/usr/bin/env python3
"""check_dd.py EDGES --delta DELTA --diameter D [--expect-n N]
Standalone checker for the degree-diameter problem, written from the definition.

The object is an edge list: one line per edge, two 0-indexed vertex numbers. The graph must be simple (no loops, no
repeated edges), have maximum degree <= DELTA, be connected, and have diameter <= D: every pair of vertices joined by
a path of at most D edges. The checker runs a breadth-first search from EVERY vertex (all ordered pairs), reports the
exact diameter, the degree histogram, and the Moore bound 1 + DELTA * sum_{i<D} (DELTA - 1)^i, which no graph exceeds.
Standard library only. Last line: "PASS ..." or "FAIL ...".
"""
import sys
from collections import Counter, deque


def main():
    args = sys.argv[1:]
    path = args[0]
    delta = int(args[args.index("--delta") + 1])
    dmax = int(args[args.index("--diameter") + 1])
    expect = int(args[args.index("--expect-n") + 1]) if "--expect-n" in args else None
    edges = []
    try:
        for line in open(path):
            if line.strip():
                a, b = line.split()
                edges.append((int(a), int(b)))
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL could not read the edge list: {exc}")
        return 1
    n = 1 + max(max(e) for e in edges)
    adj = [set() for _ in range(n)]
    for a, b in edges:
        if a == b or a < 0 or b < 0:
            print(f"FAIL loop or negative vertex in edge ({a}, {b})")
            return 1
        if b in adj[a]:
            print(f"FAIL repeated edge ({a}, {b})")
            return 1
        adj[a].add(b)
        adj[b].add(a)
    degs = [len(s) for s in adj]
    hist = sorted(Counter(degs).items())
    if min(degs) == 0:
        print("FAIL an isolated vertex (or a gap in the vertex numbering)")
        return 1
    diam = 0
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        q = deque([s])
        while q:
            u = q.popleft()
            for w in adj[u]:
                if dist[w] < 0:
                    dist[w] = dist[u] + 1
                    q.append(w)
        if min(dist) < 0:
            print("FAIL the graph is disconnected")
            return 1
        diam = max(diam, max(dist))
    moore = 1 + delta * sum((delta - 1) ** i for i in range(dmax))
    print(f"N={n} edges={len(edges)} degree histogram={hist} max degree={max(degs)} exact diameter={diam} "
          f"(BFS from all {n} vertices) Moore bound={moore}")
    if max(degs) > delta:
        print(f"FAIL maximum degree {max(degs)} > {delta}")
        return 1
    if diam > dmax:
        print(f"FAIL diameter {diam} > {dmax}")
        return 1
    if n > moore:
        print("FAIL more vertices than the Moore bound (impossible: the checker or the input is wrong)")
        return 1
    if expect is not None and n != expect:
        print(f"FAIL N={n} != expected {expect}")
        return 1
    print(f"PASS (Delta,D)=({delta},{dmax}) N={n} max_degree={max(degs)} diameter={diam}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
