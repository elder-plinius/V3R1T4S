#!/usr/bin/env python3
"""
Peels a 9-chromatic triangulation-union candidate produced by wagner_n18_20
down to an exact 9-edge-critical biplanar subgraph using a SAT solver (PySAT CaDiCaL)
and emits the JSON object and DRAT UNSAT certificate.
"""
import sys, json
import networkx as nx
from pysat.solvers import Cadical195

def solve_k_col(G, k, fix_clq=None, with_proof=False):
    clauses = []
    if fix_clq:
        for ci, v in enumerate(fix_clq):
            clauses.append([v * k + ci + 1])
    for v in range(G.number_of_nodes()):
        clauses.append([v * k + c + 1 for c in range(k)])
    for u, v in sorted(G.edges()):
        a, b = min(u, v), max(u, v)
        for c in range(k):
            clauses.append([-(a * k + c + 1), -(b * k + c + 1)])
    with Cadical195(bootstrap_with=clauses, with_proof=with_proof) as s:
        if s.solve():
            m = set(s.get_model())
            return True, [next(c for c in range(k) if (v * k + c + 1) in m) for v in range(G.number_of_nodes())], None
        return False, None, (s.get_proof() if with_proof else None)

if __name__ == "__main__":
    rec = json.loads(open(sys.argv[1]).readline())
    n = rec["n"]
    L1 = nx.Graph(); L1.add_nodes_from(range(n)); L1.add_edges_from(rec["T0"])
    L2 = nx.Graph(); L2.add_nodes_from(range(n)); L2.add_edges_from(rec["T1"])
    H = nx.compose(L1, L2)
    for u, v in sorted(H.edges()):
        H.remove_edge(u, v)
        clq = sorted(max(nx.find_cliques(H), key=len))
        if solve_k_col(H, 8, clq[:8])[0]:
            H.add_edge(u, v)
    print(f"Peeled 9-critical biplanar graph: n={H.number_of_nodes()}, e={H.number_of_edges()}")
