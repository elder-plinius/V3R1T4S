"""Independent exact check (no SAT solver): is KG(n,k)_{s-stab} C-colourable?  python3 exact_colour.py n k s C
DSATUR branch and bound written from the definition: pick the uncoloured vertex with the most distinct neighbour
colours (ties: most uncoloured neighbours), try its feasible colours, never opening more than one new colour at a
time (colour-permutation symmetry, so the search stays exhaustive up to renaming colours). Bitsets as Python ints."""
import itertools, sys, time
sys.setrecursionlimit(10000)
n, k, s, C = map(int, sys.argv[1:5])
V = [A for A in itertools.combinations(range(1, n + 1), k) if all(min(j - i, n + i - j) >= s for i, j in itertools.combinations(A, 2))]
N = len(V)
adj = [0] * N
for u in range(N):
    for v in range(u + 1, N):
        if not set(V[u]) & set(V[v]):
            adj[u] |= 1 << v; adj[v] |= 1 << u
colour = [-1] * N
forb = [0] * N            # bitmask of colours used by neighbours
nodes = 0
def solve(ncol, left):
    global nodes
    nodes += 1
    if not left:
        return True
    best, bs, bd = -1, -1, -1
    m = left
    while m:
        v = (m & -m).bit_length() - 1; m &= m - 1
        sat = bin(forb[v]).count('1')
        if sat > bs or (sat == bs and bin(adj[v] & left).count('1') > bd):
            best, bs, bd = v, sat, bin(adj[v] & left).count('1')
    v = best
    for c in range(min(ncol + 1, C)):
        if forb[v] >> c & 1:
            continue
        changed = []
        nb = adj[v] & left
        ok = True
        while nb:
            u = (nb & -nb).bit_length() - 1; nb &= nb - 1
            if not forb[u] >> c & 1:
                forb[u] |= 1 << c; changed.append(u)
                if forb[u] == (1 << C) - 1:
                    ok = False
        colour[v] = c
        if ok and solve(max(ncol, c + 1), left & ~(1 << v)):
            return True
        colour[v] = -1
        for u in changed:
            forb[u] &= ~(1 << c)
    return False
t = time.time()
res = solve(0, (1 << N) - 1)
if res:
    assert all(colour[u] != colour[v] for u in range(N) for v in range(N) if adj[u] >> v & 1)
print('n=%d k=%d s=%d C=%d vertices=%d: %s, nodes %d, %.2f s' % (n, k, s, C, N, 'COLOURABLE' if res else 'NOT colourable', nodes, time.time() - t))
