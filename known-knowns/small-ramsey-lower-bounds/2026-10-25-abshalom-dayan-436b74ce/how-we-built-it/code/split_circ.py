"""Circulant split (angle 1 of the run's brief, not shipped): split colour `c` of a two-colour circulant on Z_N into part 1 (K_a-free) and
part 2 (K_b-free), both circulant, by SAT over one variable per distance class of colour c (true = part 1).
Triangle clauses are complete; K_b clauses for b >= 4 (and K_a for a >= 4) are added lazily from an exact clique
search through vertex 0 of the expanded part (vertex-transitive, so any clique maps to one containing 0).
UNSAT is exact for this family (a subset of the full clause set is already UNSAT). SAT is accepted only when the
exact clique search finds no K_a in part 1 and no K_b in part 2.
usage: split_circ.py <source.circ> <colour> <a> <b> <out.circ or -> [max_rounds]
Writes a 3-colour circulant file: colour 1 = part 1, colour 2 = part 2, colour 3 = the other source colour."""
import sys, time
from pysat.solvers import Cadical153
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from circ import load_circ


def cls(N, d):
    d %= N
    return min(d, N - d)


def find_cliques_through0(N, D, k, limit):
    """cliques of size k containing 0 in the circulant with distance-residue set D (symmetric). Exact search;
    returns up to `limit` cliques as vertex lists (0 first)."""
    nb = [0] * N
    for i in range(N):
        m = 0
        for d in D:
            m |= 1 << ((i + d) % N)
        nb[i] = m
    out = []

    def rec(cl, P, need):
        if len(out) >= limit:
            return
        if need == 0:
            out.append(list(cl))
            return
        # bound: popcount
        if bin(P).count('1') < need:
            return
        while P:
            if bin(P).count('1') < need:
                return
            v = (P & -P).bit_length() - 1
            P &= ~(1 << v)
            cl.append(v)
            rec(cl, P & nb[v], need - 1)
            cl.pop()
            if len(out) >= limit:
                return

    rec([0], nb[0], k - 1)
    return out


def has_clique_exact(N, D, k):
    """exact decision via greedy-colouring B&B (through vertex 0)."""
    nb = [0] * N
    for i in range(N):
        m = 0
        for d in D:
            m |= 1 << ((i + d) % N)
        nb[i] = m

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

    return expand(1, nb[0])


def main():
    src, c, a, b, outp = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    max_rounds = int(sys.argv[6]) if len(sys.argv) > 6 else 100000
    N, r, col = load_circ(src)
    S = sorted({cls(N, d) for d in range(1, N) if col[d] == c})
    var = {d: i + 1 for i, d in enumerate(S)}
    print('source', src, 'N', N, 'split colour', c, 'classes', len(S), 'parts K%d-free / K%d-free' % (a, b))
    resid = [d for d in range(1, N) if col[d] == c]
    inS = set(resid)
    tri = set()
    for u in resid:
        for v in resid:
            if u < v and ((v - u) % N) in inS:
                t = frozenset((cls(N, u), cls(N, v), cls(N, v - u)))
                tri.add(t)
    s = Cadical153()
    ncl = 0
    for t in tri:
        lits = [var[d] for d in t]
        if a == 3:
            s.add_clause([-l for l in lits]); ncl += 1
        if b == 3:
            s.add_clause(lits); ncl += 1
    print('triangle class-sets', len(tri), 'initial clauses', ncl)
    t0 = time.time()
    rounds = 0
    while True:
        rounds += 1
        if not s.solve():
            print('RESULT UNSAT (exact for circulant splits of this graph) rounds', rounds, 'seconds %.2f' % (time.time() - t0))
            return
        m = set(l for l in s.get_model() if l > 0)
        P1 = [d for d in S if var[d] in m]
        P2 = [d for d in S if var[d] not in m]
        D1 = sorted({x for d in P1 for x in (d, N - d)})
        D2 = sorted({x for d in P2 for x in (d, N - d)})
        added = 0
        for part, D, k, sign in ((1, D1, a, -1), (2, D2, b, 1)):
            if k == 3:
                continue  # complete clauses already
            for clq in find_cliques_through0(N, D, k, 300):
                lits = sorted({var[cls(N, clq[j] - clq[i])] for i in range(k) for j in range(i + 1, k)})
                s.add_clause([sign * l for l in lits]); added += 1
        if rounds % 20 == 0 or added == 0:
            print('round', rounds, 'added', added, 'seconds %.1f' % (time.time() - t0), flush=True)
        if added == 0:
            ok1 = not has_clique_exact(N, D1, a)
            ok2 = not has_clique_exact(N, D2, b)
            print('exact check part1 K%d-free %s part2 K%d-free %s' % (a, ok1, b, ok2))
            if ok1 and ok2:
                other = [d for d in range(1, N // 2 + 1) if col[d] != c]
                txt = 'circulant %d 3\n1: %s\n2: %s\n3: %s\n' % (N, ' '.join(map(str, P1)), ' '.join(map(str, P2)),
                                                                 ' '.join(map(str, other)))
                print('RESULT SAT\n' + txt)
                if outp != '-':
                    open(outp, 'w').write('# circulant split of %s colour %d into K%d-free + K%d-free; colour 3 = other source colour\n' % (src, c, a, b) + txt)
                return
            print('exact check disagrees with lazy search; abort')
            return
        if rounds >= max_rounds:
            print('RESULT UNDECIDED (round cap)')
            return


if __name__ == '__main__':
    main()
