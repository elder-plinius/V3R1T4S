#!/usr/bin/env python3
"""Direct stepper for outer-totalistic CA on a graph (independent of otA.c / otB.go).
Usage: ostepper.py GRAPH6 B S START   e.g.  ostepper.py 'FBjng' 0,1,3 2,4,5 1
B, S: comma lists ('' or '-' for empty). START: integer, bit v = state of vertex v (graph6 vertex order).
Rule: OFF node with c ON neighbours turns ON iff c in B; ON node stays ON iff c in S.
Prints transient length and cycle length (states remembered in a dict)."""
import sys

def g6_edges(s):
    data = [ord(ch) - 63 for ch in s]
    n = data[0]
    bitstr = ''.join(format(x, '06b') for x in data[1:])
    edges, k = [], 0
    for j in range(1, n):
        for i in range(j):
            if bitstr[k] == '1':
                edges.append((i, j))
            k += 1
    return n, edges

def parse(x):
    return set() if x in ('', '-') else {int(t) for t in x.split(',')}

def main():
    g, B, S, start = sys.argv[1], parse(sys.argv[2]), parse(sys.argv[3]), int(sys.argv[4])
    n, edges = g6_edges(g)
    nbrs = [[] for _ in range(n)]
    for i, j in edges:
        nbrs[i].append(j); nbrs[j].append(i)
    state = tuple((start >> v) & 1 for v in range(n))
    seen, t = {}, 0
    while state not in seen:
        seen[state] = t
        new = []
        for v in range(n):
            c = sum(state[u] for u in nbrs[v])
            new.append(1 if (c in S if state[v] else c in B) else 0)
        state = tuple(new); t += 1
    print(f"graph6={g} n={n} edges={len(edges)} degrees={sorted(len(x) for x in nbrs)} B={sorted(B)} S={sorted(S)} "
          f"start={start} transient={seen[state]} cycle_length={t - seen[state]}")

main()
