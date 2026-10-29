"""Exact multicolour Ramsey colouring checker, two independent methods per colour.

usage: python mcheck.py <colouring file> k_1 k_2 ... k_r
A valid file proves R(k_1, ..., k_r) >= N+1: every edge of K_N has exactly one colour c in 1..r and colour c has
no clique K_{k_c}.

File formats (lines starting with '#' are ignored):
  matrix:    first line "matrix N r", then N lines of N characters; character j of line i is the colour (1..r) of
             edge {i,j}, '0' on the diagonal.
  circulant: first line "circulant N r", then r lines "c: d d d ..." listing the distances of colour c
             (edge {i,j} has the colour of the distance (j-i) mod N, a distance d and N-d are the same distance;
             every distance 1..N-1 must get exactly one colour, consistently for d and N-d).
Method A: bitset branch-and-bound clique search with a greedy-colouring bound on the expanded graph of each colour.
Method B: SAT (pysat CaDiCaL 1.5.3): "is there a K_{k_c} in colour c?" with pairwise exclusion of non-edges and a
  totalizer cardinality >= k_c; must be UNSAT.
Exit 0 only if both methods agree that no colour contains its forbidden clique.
"""
import sys, hashlib


def load(path):
    lines = [l.strip() for l in open(path) if l.strip() and not l.lstrip().startswith('#')]
    head = lines[0].split()
    kind, N, r = head[0], int(head[1]), int(head[2])
    C = [[0] * N for _ in range(N)]
    if kind == 'circulant':
        col = {}
        for l in lines[1:1 + r]:
            c, ds = l.split(':', 1)
            c = int(c)
            assert 1 <= c <= r, "colour out of range"
            for d in map(int, ds.split()):
                d %= N
                assert d != 0, "distance 0"
                for e in (d, N - d):
                    assert col.get(e, c) == c, "distance %d has two colours" % e
                    col[e] = c
        missing = [d for d in range(1, N) if d not in col]
        assert not missing, "uncoloured distances %s" % missing[:10]
        for i in range(N):
            for j in range(N):
                if i != j:
                    C[i][j] = col[(j - i) % N]
    elif kind == 'matrix':
        rows = lines[1:1 + N]
        assert len(rows) == N, "expected %d matrix rows" % N
        for i, row in enumerate(rows):
            assert len(row) == N, "row %d has length %d" % (i, len(row))
            C[i] = [int(ch) for ch in row]
    else:
        raise SystemExit("unknown format " + kind)
    return C, r


def validate(C, r):
    N = len(C)
    for i in range(N):
        assert C[i][i] == 0, "nonzero diagonal at %d" % i
        for j in range(N):
            if i != j:
                assert 1 <= C[i][j] <= r, "edge %d-%d colour %d out of range" % (i, j, C[i][j])
                assert C[i][j] == C[j][i], "not symmetric at %d-%d" % (i, j)


def colour_graph(C, c):
    N = len(C)
    return [[1 if (i != j and C[i][j] == c) else 0 for j in range(N)] for i in range(N)]


def has_clique_bb(A, k):
    """True iff the graph has a clique of size >= k (exact branch and bound)."""
    N = len(A)
    if k <= 1:
        return N >= k
    nb = [sum(1 << j for j in range(N) if A[i][j]) for i in range(N)]
    sys.setrecursionlimit(10000)

    def colour_order(P):
        order, col, U = [], 0, P
        while U:
            col += 1
            Q = U
            while Q:
                v = (Q & -Q).bit_length() - 1
                Q &= ~(1 << v)
                Q &= ~nb[v]
                U &= ~(1 << v)
                order.append((v, col))
        return order

    def expand(size, P):
        for v, c in reversed(colour_order(P)):
            if size + c < k:
                return False
            if size + 1 >= k:
                return True
            if expand(size + 1, P & nb[v]):
                return True
            P &= ~(1 << v)
        return False

    return expand(0, (1 << N) - 1)


def has_clique_sat(A, k):
    from pysat.solvers import Cadical153
    from pysat.card import CardEnc, EncType
    N = len(A)
    if k > N:
        return False
    cl = [[-(i + 1), -(j + 1)] for i in range(N) for j in range(i + 1, N) if not A[i][j]]
    card = CardEnc.atleast(lits=list(range(1, N + 1)), bound=k, top_id=N, encoding=EncType.totalizer)
    with Cadical153(bootstrap_with=cl + card.clauses) as s:
        return s.solve()


def main():
    path, ks = sys.argv[1], [int(x) for x in sys.argv[2:]]
    C, r = load(path)
    assert len(ks) == r, "need %d clique sizes, got %d" % (r, len(ks))
    validate(C, r)
    N = len(C)
    canon = "\n".join("".join(map(str, row)) for row in C).encode()
    print("colouring", path, "N", N, "colours", r, "matrix sha256", hashlib.sha256(canon).hexdigest())
    ok = True
    for c in range(1, r + 1):
        A = colour_graph(C, c)
        deg = sorted(set(sum(row) for row in A))
        a = has_clique_bb(A, ks[c - 1])
        b = has_clique_sat(A, ks[c - 1])
        print("colour %d: edges %d, degrees %s, K_%d by B&B: %s, by SAT: %s" % (
            c, sum(map(sum, A)) // 2, deg if len(deg) <= 6 else (deg[0], '..', deg[-1]), ks[c - 1], a, b))
        if a != b:
            print("VERDICT: METHODS DISAGREE")
            sys.exit(2)
        ok = ok and not a
    if ok:
        print("VERDICT: valid (%s)-colouring of K_%d, proves R(%s) >= %d" % (
            ",".join(map(str, ks)), N, ",".join(map(str, ks)), N + 1))
        sys.exit(0)
    print("VERDICT: NOT a valid (%s)-colouring" % ",".join(map(str, ks)))
    sys.exit(1)


if __name__ == '__main__':
    main()
