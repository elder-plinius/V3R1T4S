#!/usr/bin/env python3
"""Exact solver for "Risk or Safety" (Jehn, arXiv:2603.01002), EXTENDER lens, run 2026-10-15-0312.

Written from the definition in BRIEF.md only.  Standard library only; every quantity is a
fractions.Fraction and every action is decided by an exact comparison (no floats anywhere).

Coordinates (angle 2 of the brief): Q(a, i, j) = probability that the player to move wins when
they have a open points, still need i banked points (i = n - b) and the opponent needs j (j = n - c).
Then P_n(a, b, c) = Q(a, n - b, n - c) for every n, so one table with 1 <= i, j <= N answers all n <= N.

Equations (BRIEF.md, rewritten with i = n - b, j = n - c):
    Q(a, i, j) = 1                                              if a >= i
    Q(0, i, j) = 1/2 (1 - Q(0, j, i)) + 1/2 Q(1, i, j)          (forced toss)
    Q(a, i, j) = max(cont, stop) for 1 <= a < i,
        cont = 1/2 (1 - Q(0, j, i)) + 1/2 Q(a + 1, i, j)
        stop = 1 - Q(0, j, i - a)

Component method (angle 1): the unordered pair {i, j} is one strongly connected component; it only
depends on components with a smaller i + j (stop values Q(0, j, i - a), Q(0, i, j - a)).  Inside a
component the cyclic unknowns are x = Q(0, i, j) and y = Q(0, j, i).  For a fixed y the mover's
best response is a backward recursion a = i-1 .. 1 with exact comparisons, and along it every
Q(a, i, j) is an affine function alpha + beta * y.  Hence F(y) = Q(0, i, j) and G(x) = Q(0, j, i)
are piecewise-affine, decreasing, with slopes in [-(1 - 2^-i), -1/2] and [-(1 - 2^-j), -1/2];
h(x) = x - F(G(x)) is strictly increasing with h(0) < 0 < h(1).  We find its unique root exactly by
a safeguarded Newton iteration (= policy iteration: the Newton step is the exact 2x2 solve for
the current pair of policies), with an exact bisection fallback, so termination is guaranteed.
At the root both sides' policies are exact best responses, i.e. every Bellman equation holds.

Usage:
    python3 solver.py N CERTDIR NMIN NMAX VALUESFILE [--b-dir DATA_DIR]
Writes CERTDIR/n<k>.json for NMIN <= k <= NMAX, the values table, and logs to stdout.
"""
import json
import os
import sys
import time
from fractions import Fraction

HALF = Fraction(1, 2)
ONE = Fraction(1)
ZERO = Fraction(0)


def side_eval(m, stopvals, z):
    """Best response of the side that needs m points when the other side's 0-open value is z.

    stopvals[a] (1 <= a < m) is the exact constant 1 - Q(0, opp, m - a).
    Returns (alpha0, beta0, vals, acts, ties):
      Q(0) = alpha0 + beta0 * z under the chosen (best-response) policy,
      vals[a] exact value at this z (a = 0 .. m-1), acts[a] in {'toss','stop'} for a >= 1,
      ties = list of a with cont == stop exactly (action recorded as 'toss').
    """
    na, nb, nv = ONE, ZERO, ONE  # Q(m) = 1: affine coefficients in z, and value
    vals = [None] * m
    acts = [None] * m
    ties = []
    omz = ONE - z
    for a in range(m - 1, 0, -1):
        cv = HALF * omz + HALF * nv
        sv = stopvals[a]
        if cv > sv:
            acts[a] = 'toss'
            na, nb, nv = HALF + HALF * na, -HALF + HALF * nb, cv
        elif cv < sv:
            acts[a] = 'stop'
            na, nb, nv = sv, ZERO, sv
        else:
            ties.append(a)
            acts[a] = 'toss'
            na, nb, nv = HALF + HALF * na, -HALF + HALF * nb, cv
        vals[a] = nv
    alpha0 = HALF + HALF * na
    beta0 = -HALF + HALF * nb
    vals[0] = HALF * omz + HALF * nv
    acts[0] = 'toss'
    return alpha0, beta0, vals, acts, ties


class Solver:
    def __init__(self, N):
        self.N = N
        self.Q = {}      # (a, i, j) -> Fraction, 0 <= a < i
        self.act = {}    # (a, i, j) -> 'toss' / 'stop'
        self.ties = []   # (a, i, j) with cont == stop exactly
        self.iters = {}  # (i, j) -> number of h evaluations
        self.bisections = 0

    def q0(self, i, j):
        return self.Q[(0, i, j)]

    def stopvals(self, m, opp):
        # stop at a: bank a points -> opponent to move needing opp, we need m - a
        sv = [None] * m
        for a in range(1, m):
            sv[a] = ONE - self.q0(opp, m - a)
        return sv

    def solve_component(self, i, j):
        """Solve component {i, j} with i <= j exactly."""
        if i == j:
            sA = self.stopvals(i, i)

            def h(x):
                pA, qA, _, _, _ = side_eval(i, sA, x)
                fx = pA + qA * x
                newton = pA / (ONE - qA)
                return x - fx, newton
        else:
            sA = self.stopvals(i, j)
            sB = self.stopvals(j, i)

            def h(x):
                pB, qB, _, _, _ = side_eval(j, sB, x)
                y = pB + qB * x
                pA, qA, _, _, _ = side_eval(i, sA, y)
                fy = pA + qA * y
                newton = (pA + qA * pB) / (ONE - qA * qB)
                return x - fy, newton

        lo, hi = ZERO, ONE
        x = HALF
        seen = set()
        nev = 0
        while True:
            nev += 1
            if nev > 10000:
                raise RuntimeError('no convergence in component %r' % ((i, j),))
            hv, newton = h(x)
            if hv == 0:
                break
            if hv < 0:
                lo = x
            else:
                hi = x
            seen.add(x)
            if lo < newton < hi and newton not in seen:
                x = newton
            else:
                self.bisections += 1
                x = (lo + hi) / 2
        self.iters[(i, j)] = nev
        # x is the exact root; store final values/actions with exact best responses
        if i == j:
            _, _, vals, acts, ties = side_eval(i, sA, x)
            assert vals[0] == x
            self._store(i, i, vals, acts, ties)
        else:
            pB, qB, valsB, actsB, tiesB = side_eval(j, sB, x)
            y = valsB[0]
            assert y == pB + qB * x
            _, _, valsA, actsA, tiesA = side_eval(i, sA, y)
            assert valsA[0] == x
            self._store(i, j, valsA, actsA, tiesA)
            self._store(j, i, valsB, actsB, tiesB)

    def _store(self, i, j, vals, acts, ties):
        for a in range(i):
            self.Q[(a, i, j)] = vals[a]
            self.act[(a, i, j)] = acts[a]
        for a in ties:
            self.ties.append((a, i, j))

    def solve(self, log=None):
        N = self.N
        t0 = time.time()
        for s in range(2, 2 * N + 1):
            for i in range(max(1, s - N), min(N, s - 1) + 1):
                j = s - i
                if i > j:
                    continue
                self.solve_component(i, j)
            if log is not None and s <= N + 1 and s >= 2:
                pass
        return time.time() - t0


def fstr(q):
    return '%d/%d' % (q.numerator, q.denominator)


def write_cert(sol, n, path):
    table = []
    for b in range(n):
        for c in range(n):
            for a in range(n - b):
                key = (a, n - b, n - c)
                table.append([a, b, c, fstr(sol.Q[key]), sol.act[key]])
    obj = {"n": n, "P000": fstr(sol.Q[(0, n, n)]), "table": table}
    with open(path, 'w') as f:
        json.dump(obj, f, separators=(',', ':'))
    return len(table)


def read_bfile(path):
    d = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            k, v = line.split()
            d[int(k)] = int(v)
    return d


def main():
    args = sys.argv[1:]
    bdir = None
    if '--b-dir' in args:
        k = args.index('--b-dir')
        bdir = args[k + 1]
        del args[k:k + 2]
    N = int(args[0])
    certdir = args[1]
    nmin, nmax = int(args[2]), int(args[3])
    valuesfile = args[4]
    os.makedirs(certdir, exist_ok=True)
    print('solver: N = %d (points-needed table 1 <= i, j <= N), certs n = %d..%d' % (N, nmin, nmax))
    sys.stdout.flush()
    sol = Solver(N)
    tsolve = sol.solve()
    print('exact solve time: %.2f s; components: %d; h-evaluations: total %d, max %d; bisection steps: %d'
          % (tsolve, len(sol.iters), sum(sol.iters.values()), max(sol.iters.values()), sol.bisections))
    hist = {}
    for v in sol.iters.values():
        hist[v] = hist.get(v, 0) + 1
    print('histogram of h-evaluations per component: %s' % sorted(hist.items()))
    print('exact ties (cont == stop) found: %d' % len(sol.ties))
    for t in sorted(sol.ties):
        print('  tie at (a, i, j) = %r' % (t,))
    # values table
    with open(valuesfile, 'w') as f:
        for n in range(1, N + 1):
            f.write('%d %s\n' % (n, fstr(sol.Q[(0, n, n)])))
    print('wrote values table %s' % valuesfile)
    # OEIS comparison
    if bdir is not None:
        nums = read_bfile(os.path.join(bdir, 'b387261.txt'))
        dens = read_bfile(os.path.join(bdir, 'b387262.txt'))
        allok = True
        for n in sorted(nums):
            if n > N:
                continue
            q = sol.Q[(0, n, n)]
            ok = (q.numerator == nums[n] and q.denominator == dens[n]
                  and Fraction(nums[n], dens[n]) == q)
            allok &= ok
            print('OEIS n=%2d: %s  mine=%s  oeis=%d/%d' % (n, 'MATCH' if ok else 'MISMATCH', fstr(q), nums[n], dens[n]))
        print('OEIS comparison n<=15: %s' % ('ALL MATCH' if allok else 'MISMATCH FOUND'))
        # Table 1 / A394776 comparison
        tpath = os.path.join(bdir, 'b394776.txt')
        if os.path.exists(tpath):
            tb = read_bfile(tpath)
            mism = 0
            checked = 0
            tie_on_path = 0
            for i in range(1, min(N, 20) + 1):
                for j in range(1, min(N, 20) + 1):
                    k = None
                    tie_seen = False
                    for a in range(1, i):
                        if (a, i, j) in set(sol.ties):
                            tie_seen = True
                        if sol.act[(a, i, j)] == 'stop':
                            k = a
                            break
                    if k is None:
                        k = i
                    if tie_seen:
                        tie_on_path += 1
                    idx = (j - 1) ** 2 + i if i < j else i * i - j + 1
                    checked += 1
                    if tb.get(idx) != k:
                        mism += 1
                        print('A394776 MISMATCH at i=%d j=%d (index %d): mine %d, b-file %r' % (i, j, idx, k, tb.get(idx)))
            print('A394776 / Table 1 comparison: %d (i,j) pairs checked, %d mismatches, %d with an exact tie on path'
                  % (checked, mism, tie_on_path))
    # certificates
    t1 = time.time()
    for n in range(nmin, nmax + 1):
        path = os.path.join(certdir, 'n%d.json' % n)
        cnt = write_cert(sol, n, path)
        assert cnt == n * n * (n + 1) // 2
        print('wrote %s (%d positions, %d bytes) P000 = %s' % (path, cnt, os.path.getsize(path), fstr(sol.Q[(0, n, n)])))
    print('certificate writing time: %.2f s' % (time.time() - t1))


if __name__ == '__main__':
    main()
