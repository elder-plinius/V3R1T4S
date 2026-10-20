"""
ddlib: core kernels for warm-start vertex insertion on degree-diameter record graphs.

Graph representation: adj int32[n, Delta] (padded with -1), deg int32[n].
Cost = number of UNORDERED vertex pairs at distance > D (computed exactly with numba bitset APSP).
"""
import re
import numpy as np
from numba import njit


# ------------------------------------------------------------------------------------------- loading
def load_graph(path):
    """Load an edge list ("u v" per line; lines starting with '#' or '%' are comments). Returns (N, E[m,2] int64).

    Same semantics as the checker parser the search used: each edge is normalised to (min, max), the edge list is
    SORTED by (u, v) and duplicates are rejected, and the labels that occur are relabelled to 0..N-1 in increasing
    order (the identity for a 0-based edge list). The sorted order matters: it fixes the adjacency order seen by the
    randomised search, so a chain started from a file is reproducible.
    """
    rows = []
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            s = line.strip()
            if not s or s[0] in '#%':
                continue
            toks = [t for t in re.split(r'[\s,;:]+', s) if t != '']
            rows.append([int(t) for t in toks])
    if not rows or any(len(r) != 2 for r in rows):
        raise ValueError(f"{path}: expected an edge list with two integers per line")
    e = np.array(rows, dtype=np.int64)
    if len(rows) < len(np.unique(e)) - 1:
        raise ValueError(f"{path}: fewer edges than N-1, not an edge list of a connected graph")
    loops = int((e[:, 0] == e[:, 1]).sum())
    u = np.minimum(e[:, 0], e[:, 1]); v = np.maximum(e[:, 0], e[:, 1])
    n_lab = int(max(u.max(), v.max())) + 1
    uk, cnt = np.unique(u * n_lab + v, return_counts=True)
    multi = int((cnt > 1).sum())
    if loops or multi:
        raise ValueError(f"{path}: loops={loops} multi={multi}")
    edges = np.stack([uk // n_lab, uk % n_lab], axis=1)
    lab = np.unique(e)
    E = np.searchsorted(lab, edges).astype(np.int64)
    return len(lab), E


def load_edges_file_order(path):
    """Load an edge list keeping the FILE order of the lines (used to resume from a saved state exactly as the search
    held it in memory). Returns (N, E[m,2] int64) with each row sorted; labels must be 0..N-1."""
    E = []
    with open(path) as f:
        for line in f:
            s = line.strip()
            if not s or s[0] in '#%':
                continue
            a, b = s.split()[:2]
            E.append((int(a), int(b)))
    E = np.array(E, np.int64)
    n = int(E.max()) + 1
    E = np.sort(E, 1)
    key = E[:, 0] * n + E[:, 1]
    assert len(np.unique(key)) == len(key), 'repeated edge'
    assert (E[:, 0] != E[:, 1]).all(), 'loop'
    assert len(np.unique(E.ravel())) == n, 'label gap'
    return n, E


def edges_to_adj(n, E, Delta):
    adj = -np.ones((n, Delta), dtype=np.int32)
    deg = np.zeros(n, dtype=np.int32)
    for a, b in E:
        a = int(a); b = int(b)
        if deg[a] >= Delta or deg[b] >= Delta:
            raise ValueError("degree overflow")
        adj[a, deg[a]] = b; deg[a] += 1
        adj[b, deg[b]] = a; deg[b] += 1
    return adj, deg


def adj_to_edges(adj, deg):
    E = []
    for v in range(adj.shape[0]):
        for j in range(deg[v]):
            u = int(adj[v, j])
            if v < u:
                E.append((v, u))
    return np.array(E, dtype=np.int64)


def write_edges(path, E, header=None):
    with open(path, 'w') as f:
        if header:
            for line in header.strip().split('\n'):
                f.write('# ' + line + '\n')
        for a, b in E:
            f.write(f"{int(a)} {int(b)}\n")


# ------------------------------------------------------------------------------------------- kernels
@njit(inline='always')
def popcount64(x):
    x = x - ((x >> np.uint64(1)) & np.uint64(0x5555555555555555))
    x = (x & np.uint64(0x3333333333333333)) + ((x >> np.uint64(2)) & np.uint64(0x3333333333333333))
    x = (x + (x >> np.uint64(4))) & np.uint64(0x0F0F0F0F0F0F0F0F)
    return (x * np.uint64(0x0101010101010101)) >> np.uint64(56)


@njit(cache=True)
def reach_sets(adj, deg, n, D, W, R, Rn):
    """R, Rn: uint64[nmax, W] scratch. On return R holds B_D(v) bitsets (rows 0..n-1). Returns R (may be swapped)."""
    for v in range(n):
        for w in range(W):
            R[v, w] = 0
        R[v, v >> 6] |= np.uint64(1) << np.uint64(v & 63)
    for step in range(D):
        for v in range(n):
            for w in range(W):
                Rn[v, w] = R[v, w]
            for j in range(deg[v]):
                u = adj[v, j]
                for w in range(W):
                    Rn[v, w] |= R[u, w]
        R, Rn = Rn, R
    return R


@njit(cache=True)
def bad_pairs(adj, deg, n, D, W, R, Rn, defic):
    """Exact number of unordered pairs at distance > D. defic[v] = # vertices not within D of v."""
    for v in range(n):
        for w in range(W):
            R[v, w] = 0
        R[v, v >> 6] |= np.uint64(1) << np.uint64(v & 63)
    for step in range(D - 1):
        for v in range(n):
            for w in range(W):
                Rn[v, w] = R[v, w]
            for j in range(deg[v]):
                u = adj[v, j]
                for w in range(W):
                    Rn[v, w] |= R[u, w]
        R, Rn = Rn, R
    # last step: only count
    total = 0
    for v in range(n):
        c = 0
        for w in range(W):
            x = R[v, w]
            for j in range(deg[v]):
                x |= R[adj[v, j], w]
            c += popcount64(x)
        defic[v] = n - c
        total += n - c
    return total // 2


@njit(cache=True)
def bfs_dist(adj, deg, n, s, dist, queue):
    for v in range(n):
        dist[v] = -1
    dist[s] = 0
    queue[0] = s
    h = 0; t = 1
    while h < t:
        v = queue[h]; h += 1
        for j in range(deg[v]):
            u = adj[v, j]
            if dist[u] < 0:
                dist[u] = dist[v] + 1
                queue[t] = u; t += 1
    return t


@njit(cache=True)
def has_edge(adj, deg, a, b):
    for j in range(deg[a]):
        if adj[a, j] == b:
            return True
    return False


@njit(cache=True)
def add_edge(adj, deg, a, b):
    adj[a, deg[a]] = b; deg[a] += 1
    adj[b, deg[b]] = a; deg[b] += 1


@njit(cache=True)
def _rm_half(adj, deg, a, b):
    d = deg[a]
    for j in range(d):
        if adj[a, j] == b:
            adj[a, j] = adj[a, d - 1]
            adj[a, d - 1] = -1
            deg[a] = d - 1
            return True
    return False


@njit(cache=True)
def rm_edge(adj, deg, a, b):
    _rm_half(adj, deg, a, b)
    _rm_half(adj, deg, b, a)


def exact_cost(adj, deg, n, D):
    W = (n + 63) // 64
    R = np.zeros((n, W), dtype=np.uint64); Rn = np.zeros_like(R)
    defic = np.zeros(n, dtype=np.int64)
    c = bad_pairs(adj, deg, n, D, W, R, Rn, defic)
    return c, defic
