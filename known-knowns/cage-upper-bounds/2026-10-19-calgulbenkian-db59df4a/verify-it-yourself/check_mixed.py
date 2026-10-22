#!/usr/bin/env python3
"""Checker for a regular mixed graph with z in-arcs, z out-arcs and r edges at every vertex
(standard library only).

Usage: python3 check_mixed.py OBJECT_JSON [--neg]
OBJECT_JSON: N, M (N = 2M), z, r, g, generators S, A0, A1, and the explicit lists edges and arcs.
Vertex (side, x) has number side*M + (x mod M). The generators define the graph as
  edges (0,x)-(1,x+s) for s in S;  arcs (0,x)->(1,x+a) for a in A0 and (1,x)->(0,x-a) for a in A1.
The checker rebuilds the graph from the generators and compares it with the stored lists,
then checks the stored lists: no loops, no repeated link between a vertex pair (so no digon
and no parallel edge/arc), every vertex has exactly z in-arcs, z out-arcs and r edges.

CYCLE CONVENTION (open question for the panel). The checker reports the girth under two
conventions, and the claim depends on which is meant:
  FORWARD-ARC convention: a cycle may traverse an edge in either direction and an arc only
  from its tail to its head (a directed arc is never traversed backwards); cycle vertices
  are distinct. Shortest such cycle length is computed exactly by depth-first search from
  every vertex up to length 5 (so girth >= 6 means none of length 2,3,4,5 exists).
  DIRECTION-BLIND convention: forget arc directions (every arc is an undirected adjacency);
  girth of the underlying simple graph by breadth-first search from every vertex.
--neg changes the head of one arc (negative control: must fail).
The last output line is a JSON object.
"""
import sys, json
from collections import deque


def main():
    d = json.load(open(sys.argv[1]))
    N, z, r, g, M = d["N"], d["z"], d["r"], d["g"], d["M"]
    S, A0, A1 = d["S"], d["A0"], d["A1"]
    E = {frozenset((0 * M + x, M + (x + s) % M)) for x in range(M) for s in S}
    A = set()
    for x in range(M):
        for a in A0: A.add((x, M + (x + a) % M))
        for a in A1: A.add((M + x, (x - a) % M))
    arcs = [tuple(a) for a in d["arcs"]]
    edges = [frozenset(e) for e in d["edges"]]
    if "--neg" in sys.argv:
        arcs[0] = (arcs[0][0], (arcs[0][1] + 1) % N)
    res = {"file": sys.argv[1].split("/")[-1], "N": N, "z": z, "r": r, "g": g,
           "n_edges": len(set(edges)), "n_arcs": len(set(arcs))}
    if "--neg" in sys.argv: res["negative_control"] = "head of arc 0 changed"
    res["order_is_2M"] = (N == 2 * M)
    res["stored_lists_equal_graph_rebuilt_from_generators"] = (set(edges) == E and set(arcs) == A and
        len(edges) == len(set(edges)) and len(arcs) == len(set(arcs)))
    res["no_loops"] = all(len(e) == 2 for e in edges) and all(u != v for u, v in arcs)
    pairs = [tuple(sorted(e)) for e in edges] + [tuple(sorted(a)) for a in arcs]
    res["no_repeated_link_between_a_vertex_pair"] = (len(pairs) == len(set(pairs)))
    ind = [0] * N; out = [0] * N; ed = [0] * N
    for u, v in arcs: out[u] += 1; ind[v] += 1
    for e in edges:
        for u in e: ed[u] += 1
    res["regular_z_in_z_out_r_edges"] = all(ind[v] == z and out[v] == z and ed[v] == r for v in range(N))
    mv = [[] for _ in range(N)]
    for e in edges:
        u, v = tuple(e); mv[u].append(v); mv[v].append(u)
    for u, v in arcs: mv[u].append(v)
    best = [None]

    def dfs(root, path):
        u = path[-1]
        for w in mv[u]:
            if w == root:
                L = len(path)
                if L >= 3 and (best[0] is None or L < best[0]): best[0] = L
                continue
            if w in path or len(path) >= 5: continue
            path.append(w); dfs(root, path); path.pop()
    for root in range(N): dfs(root, [root])
    res["shortest_cycle_up_to_5_forward_arc_convention"] = best[0]
    res["girth_at_least_6_forward_arc_convention"] = (best[0] is None and res["no_repeated_link_between_a_vertex_pair"])
    und = [set() for _ in range(N)]
    for u, v in arcs: und[u].add(v); und[v].add(u)
    for e in edges:
        u, v = tuple(e); und[u].add(v); und[v].add(u)
    gir = 10 ** 9
    for s in range(N):
        dist = {s: 0}; par = {s: -1}; q = deque([s])
        while q:
            u = q.popleft()
            for w in und[u]:
                if w not in dist: dist[w] = dist[u] + 1; par[w] = u; q.append(w)
                elif par[u] != w: gir = min(gir, dist[u] + dist[w] + 1)
    res["girth_direction_blind_convention"] = gir
    res["VALID_under_forward_arc_convention"] = bool(res["order_is_2M"] and res["stored_lists_equal_graph_rebuilt_from_generators"]
        and res["no_loops"] and res["regular_z_in_z_out_r_edges"] and res["girth_at_least_6_forward_arc_convention"])
    print(json.dumps(res))
    return 0


sys.exit(main())
