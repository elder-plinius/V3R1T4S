"""Second exact check of the R(3,3,15) join object that does not use the block argument of verify_join.py.
usage: check_rot.py <matrix file> <n_circ>   (run with the venv python: needs python-sat)
1. sigma: i -> (i + 1) mod n_circ for i < n_circ, i -> i otherwise, is checked to be an automorphism of the colouring
   (colour(sigma i, sigma j) = colour(i, j) for every pair). So any clique that contains a vertex below n_circ can be
   rotated to one containing vertex 0.
2. Cliques inside the extra vertices (n_circ..N-1) are checked by brute force over all their subsets.
3. A K_k in colour c that meets 0..n_circ-1 exists iff the colour-c neighbourhood of 0 has a K_{k-1}: decided by
   CaDiCaL 1.9.5 (sequential-counter cardinality) and, separately, by a bitset branch and bound with a greedy
   colouring bound written here.
Forbidden sizes: 3, 3, 15. Last line: PASS or FAIL."""
import sys, time, itertools
from pysat.solvers import Cadical195
from pysat.card import CardEnc, EncType

path, NC = sys.argv[1], int(sys.argv[2])
rows = [l.strip() for l in open(path) if l.strip() and not l.startswith('#')]
assert rows[0].split()[0] == 'matrix'
N = int(rows[0].split()[1])
C = [[int(ch) for ch in r] for r in rows[1:1 + N]]
assert len(C) == N and all(len(r) == N for r in C)
assert all(C[i][i] == 0 for i in range(N)) and all(C[i][j] == C[j][i] in (1, 2, 3) for i in range(N) for j in range(N) if i != j)
sig = [(i + 1) % NC if i < NC else i for i in range(N)]
bad = sum(1 for i in range(N) for j in range(N) if i != j and C[sig[i]][sig[j]] != C[i][j])
print('automorphism check of the rotation of 0..%d (extra vertices fixed): %d mismatching pairs' % (NC - 1, bad))
ok = bad == 0
K = {1: 3, 2: 3, 3: 15}
extra = list(range(NC, N))
for c, k in K.items():
    small = max((len(S) for r in range(1, len(extra) + 1) for S in itertools.combinations(extra, r)
                 if all(C[a][b] == c for a, b in itertools.combinations(S, 2))), default=0)
    nb = [j for j in range(N) if j != 0 and C[0][j] == c]
    adj = {v: sum(1 << i for i, u in enumerate(nb) if u != v and C[v][u] == c) for v in nb}
    bits = [adj[v] for v in nb]
    # branch and bound for the clique number of the neighbourhood of 0
    best = [0]

    def expand(P, size):
        if P == 0:
            best[0] = max(best[0], size)
            return
        # greedy colouring bound
        order, cols, U, col = [], [], P, 0
        while U:
            col += 1
            Q = U
            while Q:
                v = (Q & -Q).bit_length() - 1
                Q &= ~bits[v] & ~(1 << v)
                U &= ~(1 << v)
                order.append(v); cols.append(col)
                Q &= U
        for idx in range(len(order) - 1, -1, -1):
            if size + cols[idx] <= best[0]:
                return
            v = order[idx]
            expand(P & bits[v], size + 1)
            P &= ~(1 << v)

    t0 = time.time()
    expand((1 << len(nb)) - 1, 0)
    t1 = time.time()
    n = len(nb)
    cl = [[-(i + 1), -(j + 1)] for i in range(n) for j in range(i + 1, n) if not (bits[i] >> j) & 1]
    card = CardEnc.atleast(lits=list(range(1, n + 1)), bound=k - 1, top_id=n, encoding=EncType.seqcounter)
    with Cadical195(bootstrap_with=cl + card.clauses) as s:
        sat = s.solve()
    t2 = time.time()
    w = best[0] + 1
    print('colour %d: degree of 0 = %d; clique number through 0 = %d (B&B, %.1f s); K_%d in the neighbourhood of 0: %s '
          '(CaDiCaL, %.1f s); largest clique inside the extra vertices: %d'
          % (c, n, w, t1 - t0, k - 1, 'SAT' if sat else 'UNSAT', t2 - t1, small))
    if sat or w >= k or small >= k:
        ok = False
print('N %d: forbidden 3, 3, 15 %s' % (N, 'absent' if ok else 'NOT shown absent'))
print('proves R(3,3,15) >= %d' % (N + 1) if ok else 'no proof')
print('PASS' if ok else 'FAIL')
