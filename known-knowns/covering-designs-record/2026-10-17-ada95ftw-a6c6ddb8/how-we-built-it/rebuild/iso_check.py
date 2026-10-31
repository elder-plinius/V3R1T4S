#!/usr/bin/env python3
"""Isomorphism test of two block designs via their point-block incidence graphs (networkx VF2), plus invariants."""
import sys, networkx as nx, itertools
from networkx.algorithms import isomorphism as iso
from collections import Counter
def load(fn): return [frozenset(map(int,l.split())) for l in open(fn) if l.strip()]
def graph(bl):
    g = nx.Graph()
    for p in range(1,21): g.add_node(("p",p), side=0)
    for i,b in enumerate(bl):
        g.add_node(("b",i), side=1)
        for p in b: g.add_edge(("p",p),("b",i))
    return g
def inv(bl):
    inter = Counter(len(a&b) for a,b in itertools.combinations(bl,2))
    mult = Counter()
    for b in bl:
        for t in itertools.combinations(sorted(b),3): mult[t]+=1
    return sorted(inter.items()), sorted(Counter(mult.values()).items())
A, B = load(sys.argv[1]), load(sys.argv[2])
print("invariants A", inv(A)); print("invariants B", inv(B))
gm = iso.GraphMatcher(graph(A), graph(B), node_match=lambda x,y: x["side"]==y["side"])
r = gm.is_isomorphic(); print("isomorphic:", r)
if r:
    m = {k[1]:v[1] for k,v in gm.mapping.items() if k[0]=="p"}
    print("point map A->B:", [m[p] for p in range(1,21)])
    mapped = {frozenset(m[p] for p in b) for b in A}
    print("mapped A equals B exactly:", mapped == set(B))
print("identical as labelled sets:", set(A)==set(B))
