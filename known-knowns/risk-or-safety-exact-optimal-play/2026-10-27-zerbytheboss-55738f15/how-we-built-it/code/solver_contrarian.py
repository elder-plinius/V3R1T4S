#!/usr/bin/env python3
"""needs_minimax_solver.py -- CONTRARIAN lens.

Exact solver for "Risk or Safety" in points-needed coordinates, written from the definition.
ALGORITHM: pure-turn-plan exact minimax (no policy iteration, no value iteration).
Inside component {i, j}, turn plans k = 1..i give affine lines:
    L_k(y) = (1 - 2^-k)(1 - y) + 2^-k s_k
Opponent plans m = 1..j give:
    M_m(x) = (1 - 2^-m)(1 - x) + 2^-m t_m
Solving x = T(x) gives the unique fixed point:
    x* = min_m max_k x_km,  x_km = (A_k + B_k C_m) / (1 - B_k D_m)
and for i == j: x* = max_k A_k / (1 - B_k).
"""
import sys
import json
import time
import os
from fractions import Fraction as Fr

one = Fr(1)
half = Fr(1, 2)


def solve(N):
    P0 = {}          # (i, j) -> P(0, i, j)
    PA = {}          # (a, i, j) -> P(a, i, j), 0 <= a < i
    ACT = {}         # (a, i, j) -> (cont, stop) exact pair for a >= 1
    PLANS = {}       # (i, j) -> sorted list of optimal k

    def lines(i, j):
        out = []
        for k in range(1, i + 1):
            p = Fr(1, 2 ** k)
            s = one if k == i else one - P0[(j, i - k)]
            out.append((k, (one - p) + p * s, -(one - p)))
        return out

    for S in range(2, 2 * N + 1):
        for i in range(max(1, S - N), min(N, S - 1) + 1):
            j = S - i
            if j < i:
                continue
            L = lines(i, j)
            if i == j:
                x = max(A / (one - B) for (_, A, B) in L)
                y = x
            else:
                M = lines(j, i)
                best_over_m = []
                for (_, C, D) in M:
                    r = max((A + B * C) / (one - B * D) for (_, A, B) in L)
                    best_over_m.append(r)
                x = min(best_over_m)
                y = max(C + D * x for (_, C, D) in M)
                y2 = min(max((C + D * A) / (one - D * B) for (_, C, D) in M) for (_, A, B) in L)
                assert y2 == y, ("y mismatch", i, j)

            assert x == max(A + B * y for (_, A, B) in L), ("F(y) != x", i, j)
            if i != j:
                assert y == max(C + D * x for (_, C, D) in lines(j, i)), ("G(x) != y", i, j)
            P0[(i, j)] = x
            P0[(j, i)] = y

            for (u, v, xu, yv, LL) in ((i, j, x, y, L), (j, i, y, x, None if i == j else lines(j, i))):
                if LL is None:
                    LL = L
                PLANS[(u, v)] = [k for (k, A, B) in LL if A + B * yv == xu]

            for (u, v) in ((i, j), (j, i)):
                yy = P0[(v, u)]
                tail = (one - yy) / 2
                V = {u: one}
                for a in range(u - 1, 0, -1):
                    cont = tail + V[a + 1] / 2
                    stop = one - P0[(v, u - a)]
                    V[a] = cont if cont >= stop else stop
                    ACT[(a, u, v)] = (cont, stop)
                    PA[(a, u, v)] = V[a]
                x0 = tail + V[1] / 2
                assert x0 == P0[(u, v)], ("forced-toss identity fails", u, v)
                PA[(0, u, v)] = x0
    return P0, PA, ACT, PLANS


def fstr(q):
    return '%d/%d' % (q.numerator, q.denominator)


def write_cert(PA, ACT, n, path):
    table = []
    for b in range(n):
        for c in range(n):
            for a in range(n - b):
                key = (a, n - b, n - c)
                val = PA[key]
                if a == 0:
                    action = "toss"
                else:
                    cont, stop = ACT[key]
                    action = "toss" if cont >= stop else "stop"
                table.append([a, b, c, fstr(val), action])
    obj = {"n": n, "P000": fstr(PA[(0, n, n)]), "table": table}
    with open(path, 'w') as f:
        json.dump(obj, f, separators=(',', ':'))
    return len(table)


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 45
    values_path = sys.argv[2] if len(sys.argv) > 2 else "values_contrarian.txt"
    t0 = time.time()
    P0, PA, ACT, PLANS = solve(N)
    t1 = time.time()
    print("solve N=%d done in %.2f s; components=%d positions(a,i,j)=%d" % (N, t1 - t0, N * (N + 1) // 2, len(PA)))

    with open(values_path, "w") as f:
        for n in range(1, N + 1):
            v = P0[(n, n)]
            f.write("%d %s\n" % (n, fstr(v)))
    print("wrote values table to %s" % values_path)


if __name__ == '__main__':
    main()
