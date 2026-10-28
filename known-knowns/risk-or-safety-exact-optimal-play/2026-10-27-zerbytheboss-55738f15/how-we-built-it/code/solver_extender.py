#!/usr/bin/env python3
"""Exact solver for "Risk or Safety" (Jehn, arXiv:2603.01002), EXTENDER lens.

Component-wise exact policy iteration with safeguarded Newton-Raphson iteration on the 2x2
strongly connected components, using standard-library fractions.Fraction in exact rational
arithmetic (zero floating point).

Coordinates: Q(a, i, j) = probability that the player to move wins when they have a open points,
still need i banked points (i = n - b) and the opponent needs j (j = n - c).
Then P_n(a, b, c) = Q(a, n - b, n - c) for every n.
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
    """Best response of the side needing m points given opponent's 0-open value z."""
    na, nb, nv = ONE, ZERO, ONE
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
        self.Q = {}      # (a, i, j) -> Fraction
        self.act = {}    # (a, i, j) -> 'toss' | 'stop'
        self.ties = []   # (a, i, j) with cont == stop exactly
        self.iters = {}  # (i, j) -> number of h evaluations
        self.bisections = 0

    def q0(self, i, j):
        return self.Q[(0, i, j)]

    def stopvals(self, m, opp):
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

    def solve(self):
        N = self.N
        t0 = time.time()
        for s in range(2, 2 * N + 1):
            for i in range(max(1, s - N), min(N, s - 1) + 1):
                j = s - i
                if i > j:
                    continue
                self.solve_component(i, j)
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
            ok = (q.numerator == nums[n] and q.denominator == dens[n] and Fraction(nums[n], dens[n]) == q)
            allok &= ok
            print('OEIS n=%2d: %s  mine=%s  oeis=%d/%d' % (n, 'MATCH' if ok else 'MISMATCH', fstr(q), nums[n], dens[n]))
        print('OEIS comparison n<=15: %s' % ('ALL MATCH' if allok else 'MISMATCH FOUND'))

        tpath = os.path.join(bdir, 'b394776.txt')
        if os.path.exists(tpath):
            tb = read_bfile(tpath)
            mism = 0
            checked = 0
            for i in range(1, min(N, 20) + 1):
                for j in range(1, min(N, 20) + 1):
                    k = None
                    for a in range(1, i):
                        if sol.act[(a, i, j)] == 'stop':
                            k = a
                            break
                    if k is None:
                        k = i
                    idx = (j - 1) ** 2 + i if i < j else i * i - j + 1
                    checked += 1
                    if tb.get(idx) != k:
                        mism += 1
            print('A394776 / Table 1 comparison: %d (i,j) pairs checked, %d mismatches' % (checked, mism))

    t1 = time.time()
    for n in range(nmin, nmax + 1):
        path = os.path.join(certdir, 'n%d.json' % n)
        cnt = write_cert(sol, n, path)
        assert cnt == n * n * (n + 1) // 2
        print('wrote %s (%d positions, %d bytes) P000 = %s' % (path, cnt, os.path.getsize(path), fstr(sol.Q[(0, n, n)])))
    print('certificate writing time: %.2f s' % (time.time() - t1))


if __name__ == '__main__':
    main()
