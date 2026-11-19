"""CNF for 'KG(n,k)_{s-stab} is C-colourable', exactly as frozen in PREREG.md (stdlib only).
  python3 gen_cnf.py n k s C out.cnf [--no-sym]
Vertices: s-stable k-subsets of [n] (min{j-i, n+i-j} >= s for i<j), sorted tuples in lexicographic order.
x(v,c) = v*C + c + 1. Clauses: at-least-one colour per vertex; for each edge u<v and colour c, (-x(u,c) | -x(v,c));
then units fixing colour j-1 on Q_j = {j, j+t, ..., j+(k-1)t}, t = floor(n/k), for j = 1..min(t, C) (PREREG.v2.md)."""
import itertools, sys

def stable_sets(n, k, s):
    return [A for A in itertools.combinations(range(1, n + 1), k)
            if all(min(j - i, n + i - j) >= s for i, j in itertools.combinations(A, 2))]

def build(n, k, s, C, sym=True):
    V = stable_sets(n, k, s)
    idx = {A: i for i, A in enumerate(V)}
    x = lambda v, c: v * C + c + 1
    cl = [[x(v, c) for c in range(C)] for v in range(len(V))]
    edges = [(u, v) for u in range(len(V)) for v in range(u + 1, len(V)) if not set(V[u]) & set(V[v])]
    for u, v in edges:
        for c in range(C):
            cl.append([-x(u, c), -x(v, c)])
    if sym:
        Q = [tuple(j + t * (n // k) for t in range(k)) for j in range(1, min(n // k, C) + 1)]
        assert all(q in idx for q in Q) and all(not set(a) & set(b) for a, b in itertools.combinations(Q, 2))
        for j, q in enumerate(Q):
            cl.append([x(idx[q], j)])
    return V, edges, cl

if __name__ == '__main__':
    n, k, s, C = map(int, sys.argv[1:5])
    V, E, cl = build(n, k, s, C, sym='--no-sym' not in sys.argv)
    with open(sys.argv[5], 'w') as f:
        f.write('p cnf %d %d\n' % (len(V) * C, len(cl)))
        for c in cl:
            f.write(' '.join(map(str, c)) + ' 0\n')
    print('n=%d k=%d s=%d C=%d vertices=%d edges=%d clauses=%d' % (n, k, s, C, len(V), len(E), len(cl)))
