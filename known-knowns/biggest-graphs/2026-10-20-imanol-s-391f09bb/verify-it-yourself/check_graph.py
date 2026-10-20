#!/usr/bin/env python3
"""Check the (13,4) object from its edge list alone: simple, max degree <= 13, connected,
diameter <= 4. Pure standard library, all-pairs BFS from every vertex.

usage: check_graph.py <edges> [Delta] [D]
"""
import sys
from collections import deque


def load(path):
    edges = []
    with open(path) as f:
        for line in f:
            line = line.split('#')[0].strip()
            if line:
                a, b = map(int, line.split())
                edges.append((a, b))
    return edges


def main():
    path = sys.argv[1]
    Delta = int(sys.argv[2]) if len(sys.argv) > 2 else 13
    D = int(sys.argv[3]) if len(sys.argv) > 3 else 4
    E = load(path)
    n = 1 + max(max(e) for e in E)
    adj = [set() for _ in range(n)]
    for a, b in E:
        assert 0 <= a < n and 0 <= b < n, "vertex out of range"
        assert a != b, "loop"
        assert b not in adj[a], "multi-edge"
        adj[a].add(b); adj[b].add(a)
    deg = [len(x) for x in adj]
    assert max(deg) <= Delta, "max degree %d > %d" % (max(deg), Delta)
    assert min(deg) > 0, "isolated vertex"
    diam = 0
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        q = deque([s])
        seen = 1
        while q:
            u = q.popleft()
            du = dist[u]
            for v in adj[u]:
                if dist[v] < 0:
                    dist[v] = du + 1
                    seen += 1
                    if du + 1 > diam:
                        diam = du + 1
                    q.append(v)
        assert seen == n, "disconnected at source %d" % s
    assert diam <= D, "diameter %d > %d" % (diam, D)
    print("VALID n=%d maxdeg=%d diameter=%d edges=%d" % (n, max(deg), diam, len(E)))


if __name__ == '__main__':
    main()
