"""enc2: independent SAT encoder for Schutte's property S_k on sets of m tournaments
(Jeffries, arXiv:2604.08790v1, Definitions 2.1 and 2.2).

Arc variables 1..m*C(n,2): tournament t outer, then pairs (i,j), i<j, lexicographic.
Variable true  <=>  i beats j (arc i->j) in T_t.  Auxiliary variables come after.
Only the standard library and pysat.solvers (in __main__) are used.
"""
import itertools
import random
import sys
import threading
import time


# ---------------------------------------------------------------- arc numbering
def _npairs(n):
    return n * (n - 1) // 2


def _pair_index(n, i, j):
    # i < j; index of (i,j) in lexicographic order of pairs
    return i * (n - 1) - i * (i - 1) // 2 + (j - i - 1)


def arc(m, n, t, i, j):
    """DIMACS literal true iff i beats j in T_t."""
    if not (0 <= t < m and 0 <= i < n and 0 <= j < n) or i == j:
        raise ValueError("bad arc(%r,%r,%r,%r,%r)" % (m, n, t, i, j))
    if i < j:
        return t * _npairs(n) + _pair_index(n, i, j) + 1
    return -(t * _npairs(n) + _pair_index(n, j, i) + 1)


class _Pool:
    def __init__(self, first_free):
        self.top = first_free - 1

    def new(self):
        self.top += 1
        return self.top


# ------------------------------------------------------- hand-written at-most-K
def at_most(lits, K, pool):
    """Clauses forcing at most K of lits true (Sinz sequential counter)."""
    lits = list(lits)
    L = len(lits)
    if K < 0:
        return [[]]
    if K >= L:
        return []
    if K == 0:
        return [[-x] for x in lits]
    # s[i][j-1] : "at least j of lits[0..i] are true" (implied direction only)
    s = [[pool.new() for _ in range(K)] for _ in range(L - 1)]
    cl = []
    cl.append([-lits[0], s[0][0]])
    for j in range(1, K):
        cl.append([-s[0][j]])
    for i in range(1, L - 1):
        cl.append([-lits[i], s[i][0]])
        cl.append([-s[i - 1][0], s[i][0]])
        for j in range(1, K):
            cl.append([-lits[i], -s[i - 1][j - 1], s[i][j]])
            cl.append([-s[i - 1][j], s[i][j]])
        cl.append([-lits[i], -s[i - 1][K - 1]])
    cl.append([-lits[L - 1], -s[L - 2][K - 1]])
    return cl


# ------------------------------------------------------------------- base CNF
def _base(m, k, n):
    pool = _Pool(m * _npairs(n) + 1)
    clauses = []
    if n <= k:
        # Paper, proof of Prop. 2.2: if |V| <= k the set "is not S_k" (no vertex outside
        # a k-set, "if such a set even possible"). We follow that, not the vacuous reading.
        clauses.append([])
        return pool, clauses
    V = range(n)
    for U in itertools.combinations(V, k):
        Uset = set(U)
        options = []
        for t in range(m):
            for u in V:
                if u in Uset:
                    continue  # no loops: u cannot beat itself, so u not in U
                y = pool.new()  # y -> u beats every w in U in T_t
                for w in U:
                    clauses.append([-y, arc(m, n, t, u, w)])
                options.append(y)
        clauses.append(options)  # empty clause if no candidate dominator
    return pool, clauses


def base_cnf(m, k, n):
    pool, clauses = _base(m, k, n)
    return pool.top, clauses


def cube_cnf(m, k, n, d, a, b):
    assert 0 <= a <= d and 0 <= b <= n - 1 - d and a + b <= d
    pool, clauses = _base(m, k, n)
    # (i) out-degree <= d in every tournament
    for t in range(m):
        for v in range(n):
            clauses += at_most([arc(m, n, t, v, w) for w in range(n) if w != v], d, pool)
    # (ii) T_1: vertex 0 beats exactly 1..d
    for w in range(1, n):
        lit = arc(m, n, 0, 0, w)
        clauses.append([lit] if w <= d else [-lit])
    # (iii) T_2: vertex 0 beats exactly {1..a} u {d+1..d+b}
    if m >= 2:
        wins = set(range(1, a + 1)) | set(range(d + 1, d + b + 1))
        for w in range(1, n):
            lit = arc(m, n, 1, 0, w)
            clauses.append([lit] if w in wins else [-lit])
    # (iv) T_3: vertex 0 beats at most a+b others
    if m >= 3:
        clauses += at_most([arc(m, n, 2, 0, w) for w in range(1, n)], a + b, pool)
    return pool.top, clauses


# --------------------------------------------------------------- decode/check
def decode(model, m, n):
    pos = set(l for l in model if l > 0)
    mats = []
    for t in range(m):
        A = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                v = arc(m, n, t, i, j)
                if v in pos:
                    A[i][j] = 1
                else:
                    A[j][i] = 1
        mats.append(A)
    return mats


def has_Sk(mats, k):
    """Brute force Definition 2.1: every k-set U has some T_i and u with u -> U in T_i."""
    n = len(mats[0])
    for A in mats:  # sanity: each matrix is a tournament
        for i in range(n):
            assert A[i][i] == 0
            for j in range(i + 1, n):
                assert A[i][j] + A[j][i] == 1
    for U in itertools.combinations(range(n), k):
        found = False
        for A in mats:
            for u in range(n):
                if all(A[u][w] == 1 for w in U):  # A[u][u]==0 so u in U fails
                    found = True
                    break
            if found:
                break
        if not found:
            return False
    return True


# ----------------------------------------------------------------- self-test
def _solve(clauses, assumptions=(), limit=None):
    from pysat.solvers import Solver
    with Solver(name="cadical195", bootstrap_with=clauses) as s:
        if limit is None:
            r = s.solve(assumptions=list(assumptions))
        else:
            timer = threading.Timer(limit, s.interrupt)
            timer.start()
            r = s.solve_limited(assumptions=list(assumptions), expect_interrupt=True)
            timer.cancel()
        return r, (s.get_model() if r else None)


def _arc_lits_of(mats, m, n):
    lits = []
    for t in range(m):
        for i in range(n):
            for j in range(i + 1, n):
                v = arc(m, n, t, i, j)
                lits.append(v if mats[t][i][j] else -v)
    return lits


def _selftest_atmost(out):
    ok = True
    from pysat.solvers import Solver
    for L in range(1, 7):
        for K in range(0, L + 1):
            pool = _Pool(L + 1)
            cl = at_most(range(1, L + 1), K, pool)
            with Solver(name="cadical195", bootstrap_with=cl) as s:
                for bits in itertools.product([0, 1], repeat=L):
                    as_ = [(i + 1) if bits[i] else -(i + 1) for i in range(L)]
                    if s.solve(assumptions=as_) != (sum(bits) <= K):
                        ok = False
    out("at_most exhaustive check L<=6: %s" % ("ok" if ok else "MISMATCH"))
    return ok


def _selftest_arc(out):
    ok = True
    for m, n in [(1, 2), (2, 5), (3, 6)]:
        seen = set()
        for t in range(m):
            for i in range(n):
                for j in range(n):
                    if i != j:
                        if arc(m, n, t, i, j) != -arc(m, n, t, j, i):
                            ok = False
                        if i < j:
                            seen.add(arc(m, n, t, i, j))
        if seen != set(range(1, m * _npairs(n) + 1)):
            ok = False
    if arc(2, 4, 1, 0, 1) != 7 or arc(2, 4, 0, 2, 3) != 6 or arc(2, 4, 1, 3, 2) != -12:
        ok = False
    out("arc numbering check: %s" % ("ok" if ok else "MISMATCH"))
    return ok


def _check_cube(mats, m, n, d, a, b):
    for A in mats:
        for v in range(n):
            if sum(A[v]) > d:
                return False
    if mats[0][0] != [0] + [1 if 1 <= w <= d else 0 for w in range(1, n)]:
        return False
    if m >= 2:
        wins = set(range(1, a + 1)) | set(range(d + 1, d + b + 1))
        if mats[1][0] != [0] + [1 if w in wins else 0 for w in range(1, n)]:
            return False
    if m >= 3 and sum(mats[2][0]) > a + b:
        return False
    return True


def main():
    rng = random.Random(20261103)
    allok = True
    lines = []

    def out(s):
        print(s, flush=True)
        lines.append(s)

    allok &= _selftest_arc(out)
    allok &= _selftest_atmost(out)

    def run_case(m, k, n, limit=None, flips=6):
        nonlocal allok
        nv, cl = base_cnf(m, k, n)
        t0 = time.time()
        r, model = _solve(cl, limit=limit)
        dt = time.time() - t0
        tag = {True: "SAT", False: "UNSAT", None: "TIMEOUT"}[r]
        extra = ""
        if r:
            mats = decode(model, m, n)
            if not has_Sk(mats, k):
                allok = False
                extra += " has_Sk=FALSE(FAIL)"
            else:
                extra += " has_Sk=True"
            mism = 0
            for _ in range(flips):
                fm = [[row[:] for row in A] for A in mats]
                nf = rng.randint(1, 3)
                for _ in range(nf):
                    t = rng.randrange(m)
                    i, j = rng.sample(range(n), 2)
                    fm[t][i][j], fm[t][j][i] = fm[t][j][i], fm[t][i][j]
                units = [[l] for l in _arc_lits_of(fm, m, n)]
                r2, _ = _solve(cl + units)
                if bool(r2) != has_Sk(fm, k):
                    mism += 1
            if mism:
                allok = False
            extra += " flips=%d mismatches=%d" % (flips, mism)
        out("base m=%d k=%d n=%-2d vars=%-6d clauses=%-7d %-7s %7.2fs%s"
            % (m, k, n, nv, len(cl), tag, dt, extra))
        return r, dt

    for (m, k, n) in [(2, 3, 2), (2, 3, 3)]:  # n <= k: paper says not S_k
        run_case(m, k, n)
    for (m, k, n) in [(1, 1, 2), (1, 1, 3), (1, 2, 6), (1, 2, 7)]:
        run_case(m, k, n)
    for n in range(3, 8):
        run_case(2, 2, n)
    budget = 60.0
    used = 0.0
    n = 4
    while used < budget and n <= 30:
        r, dt = run_case(2, 3, n, limit=max(1.0, budget - used))
        used += dt
        if r is None:
            out("  (2,3,n) loop stopped: time budget of ~%ds used" % budget)
            break
        n += 1
    for n in (9, 10):
        r, dt = run_case(2, 4, n, limit=1200)
        if r is None:
            out("  (2,4,%d) stopped after 1200 s" % n)

    # cube sanity: models of cube_cnf satisfy (i)-(iv) and S_k
    for (m, k, n, d, a, b) in [(1, 2, 7, 3, 0, 0), (2, 2, 6, 3, 1, 1), (2, 2, 7, 4, 2, 2),
                               (3, 2, 6, 3, 1, 2), (3, 3, 9, 5, 2, 2), (2, 3, 10, 6, 3, 2)]:
        nv, cl = cube_cnf(m, k, n, d, a, b)
        t0 = time.time()
        r, model = _solve(cl, limit=60)
        dt = time.time() - t0
        tag = {True: "SAT", False: "UNSAT", None: "TIMEOUT"}[r]
        extra = ""
        if r:
            mats = decode(model, m, n)
            good = has_Sk(mats, k) and _check_cube(mats, m, n, d, a, b)
            if not good:
                allok = False
            extra = " model checks (S_k + cube i-iv): %s" % ("ok" if good else "FAIL")
        out("cube m=%d k=%d n=%-2d d=%d a=%d b=%d vars=%-6d %-7s %7.2fs%s"
            % (m, k, n, d, a, b, nv, tag, dt, extra))

    out("PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
