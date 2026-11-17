#!/usr/bin/env python3
"""Generator G1: all free trees on n vertices via networkx.nonisomorphic_trees (Wright-Richmond-Odlyzko-McKay).
Output: one tree per line, the parent array p[1..n-1] of a BFS from vertex 0 (vertices renumbered in BFS order)."""
import sys, networkx as nx
from collections import deque
n=int(sys.argv[1]); out=sys.stdout; w=out.write
if n==1: w("\n"); sys.exit()
for T in nx.nonisomorphic_trees(n):
    adj=T.adj; order=[0]; idx={0:0}; par=[0]*n; dq=deque([0])
    while dq:
        u=dq.popleft()
        for v in adj[u]:
            if v not in idx:
                idx[v]=len(order); order.append(v); par[idx[v]]=idx[u]; dq.append(v)
    w(" ".join(map(str,par[1:]))+"\n")
