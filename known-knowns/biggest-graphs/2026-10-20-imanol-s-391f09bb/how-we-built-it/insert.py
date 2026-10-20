"""
Warm-start insertion of k new vertices into a valid (Delta, D) graph (the starting state of each annealing run).

strategy 'slack' (the one used for (13,4)): each new vertex is joined greedily to old vertices that still have free
degree, choosing at each step the vertex whose (D-1)-ball covers most of what is not yet covered; if the new vertex
still has >= 2 free slots, an old edge (a, b) is subdivided through it (edge chosen among 600 random candidates by the
same coverage gain); finally leftover free slots are joined pairwise. strategy 'subdiv' skips the slack step.
The result usually has a few dozen to a few hundred pairs at distance > D; sa2.sa2_run then repairs it.
"""
import numpy as np
from ddlib import reach_sets, rm_edge, add_edge, has_edge, edges_to_adj


def popcnt_rows(X):
    return np.unpackbits(X.view(np.uint8), axis=-1).sum(axis=-1)


def reach_bits(adj, deg, n, r):
    W = (n + 63) // 64
    R = np.zeros((n, W), np.uint64); Rn = np.zeros_like(R)
    return reach_sets(adj, deg, n, r, W, R, Rn).copy()


def initial_insert(N, E, Delta, D, k, strategy, rng):
    if strategy not in ('slack', 'subdiv'):
        raise ValueError("strategy must be 'slack' or 'subdiv'")
    n = N + k
    adj, deg = edges_to_adj(n, E, Delta)   # new vertices N..n-1 isolated
    # bitsets of (D-1)-balls in the ORIGINAL graph (approximate guide only)
    Rb = reach_bits(adj, deg, n, D - 1)
    Eset = set((int(min(a, b)), int(max(a, b))) for a, b in E)
    used = set()          # vertices whose edges we already cut (keep cuts vertex-disjoint)
    newv = list(range(N, n))
    for z in newv:
        cov = np.zeros(Rb.shape[1], np.uint64)
        slots = Delta
        # slack: attach to deficient old vertices first (greedy coverage)
        if strategy == 'slack':
            while slots > 0:
                defs = [v for v in range(N) if deg[v] < Delta and not has_edge(adj, deg, z, v) and v not in used]
                if not defs:
                    break
                gains = popcnt_rows(Rb[defs] & ~cov[None, :])
                i = int(np.argmax(gains))
                v = defs[i]
                add_edge(adj, deg, z, v); cov |= Rb[v]; slots -= 1
        while slots >= 2:
            Elist = list(Eset)
            cand = [Elist[i] for i in rng.choice(len(Elist), size=min(600, len(Elist)), replace=False)]
            best = None; bg = -1
            for (a, b) in cand:
                if a in used or b in used or a >= N or b >= N:
                    continue
                g = int(popcnt_rows(((Rb[a] | Rb[b]) & ~cov)[None, :])[0])
                if g > bg:
                    bg = g; best = (a, b)
            a, b = best
            used.add(a); used.add(b)
            rm_edge(adj, deg, a, b); Eset.discard((a, b))
            add_edge(adj, deg, z, a); add_edge(adj, deg, z, b)
            cov |= Rb[a] | Rb[b]
            slots -= 2
    # odd leftovers: join new vertices with free slots pairwise, else any deficient vertex
    for _ in range(3):
        free = [v for v in range(n) if deg[v] < Delta]
        rng.shuffle(free)
        for i in range(len(free)):
            for j in range(i + 1, len(free)):
                p, q = free[i], free[j]
                if deg[p] < Delta and deg[q] < Delta and not has_edge(adj, deg, p, q) and (p >= N or q >= N):
                    add_edge(adj, deg, p, q)
    return n, adj, deg


def verify_independent(n, E, Delta, D):
    """Independent check with scipy BFS (not the numba kernel). Returns (diameter, max degree, min degree)."""
    import scipy.sparse as sp
    import scipy.sparse.csgraph as cg
    E = np.asarray(E)
    assert (E[:, 0] != E[:, 1]).all()
    key = np.minimum(E[:, 0], E[:, 1]) * n + np.maximum(E[:, 0], E[:, 1])
    assert len(np.unique(key)) == len(key), "multi-edge"
    A = sp.coo_matrix((np.ones(2 * len(E)), (np.r_[E[:, 0], E[:, 1]], np.r_[E[:, 1], E[:, 0]])), shape=(n, n)).tocsr()
    degs = np.diff(A.indptr)
    assert degs.max() <= Delta, "degree"
    dist = cg.shortest_path(A, unweighted=True, directed=False)
    assert np.isfinite(dist).all(), "disconnected"
    return int(dist.max()), int(degs.max()), int(degs.min())
