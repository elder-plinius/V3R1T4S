#!/usr/bin/env python3
"""float_vi.py -- third, algorithmically different computation (certifier lens, main session):
Gauss-Seidel value iteration in double precision, in points-needed coordinates (a, i, j):
  i = points the mover still needs, j = points the opponent needs, a = open points of the mover (0 <= a < i).
  V(a,i,j) = 1 if a >= i;  V(0,i,j) = 1/2 (1 - V(0,j,i)) + 1/2 V(1,i,j);
  V(a,i,j) = max( 1/2 (1 - V(0,j,i)) + 1/2 V(a+1,i,j),  1 - V(0,j,i-a) )  for 1 <= a < i.
A387261(n)/A387262(n) = V(0,n,n). Components {i,j} are solved in increasing i+j; inside a component the two
cyclic unknowns V(0,i,j), V(0,j,i) are iterated to machine precision (NUMERICAL; only a cross-check of the exact
certificates, never a decision).
Usage: python3 -I float_vi.py N [values_file]   (values_file lines "n num/den" to compare against)
"""
import sys
from fractions import Fraction

def solve(N):
    V0 = {}  # (i,j) -> V(0,i,j)
    def comp(i, j):
        # returns V(0,i,j), V(0,j,i) by iterating the two-cycle; needs V0 for smaller i+j
        x, y = 0.5, 0.5
        for it in range(10000):
            # given y = V(0,j,i): compute V(a,i,j) for a = i-1 .. 1 then x
            def side(ii, jj, yy):
                nxt = 1.0  # V(ii, ii, jj) = 1
                for a in range(ii - 1, 0, -1):
                    cont = 0.5 * (1 - yy) + 0.5 * nxt
                    stop = 1 - V0[(jj, ii - a)] if (jj, ii - a) in V0 else None
                    if stop is None:
                        raise KeyError((jj, ii - a))
                    nxt = cont if cont >= stop else stop
                return 0.5 * (1 - yy) + 0.5 * nxt
            nx = side(i, j, y)
            ny = side(j, i, nx) if (i, j) != (j, i) else nx
            if (nx == x and ny == y) or (abs(nx - x) <= 1e-15 and abs(ny - y) <= 1e-15):
                x, y = nx, ny
                break
            x, y = nx, ny
        return x, y, it
    maxit = 0
    for s in range(2, 2 * N + 1):
        for i in range(1, N + 1):
            j = s - i
            if j < 1 or j > N or j < i:
                continue
            x, y, it = comp(i, j)
            V0[(i, j)] = x
            V0[(j, i)] = y
            maxit = max(maxit, it)
    return V0, maxit

def main():
    N = int(sys.argv[1])
    V0, maxit = solve(N)
    exact = {}
    if len(sys.argv) > 2:
        for line in open(sys.argv[2]):
            p = line.split()
            if len(p) == 2 and '/' in p[1]:
                exact[int(p[0])] = Fraction(p[1])
    worst = 0.0
    for n in range(1, N + 1):
        v = V0[(n, n)]
        line = "n=%2d  float=%.15f" % (n, v)
        if n in exact:
            d = abs(v - float(exact[n]))
            worst = max(worst, d)
            line += "  exact=%.15f  |diff|=%.1e" % (float(exact[n]), d)
        print(line)
    print("max_two_cycle_iterations=%d" % maxit)
    if exact:
        print("worst_abs_diff=%.3e  agree_to_1e-12=%s" % (worst, "yes" if worst < 1e-12 else "NO"))

if __name__ == "__main__":
    main()
