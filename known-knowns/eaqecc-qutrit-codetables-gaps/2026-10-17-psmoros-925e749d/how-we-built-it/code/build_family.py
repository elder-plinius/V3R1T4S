#!/usr/bin/env python3
"""Explicit [[n,1,n-1;c]]_3 construction with an X-type radical (lens small-cases, run 2026-10-17-1119).

C = R + <u,v>,  R = {(rho,0): rho in R0},  R0 = span(y_1..y_T) with y_t supported on Y_t inside class Z_t,
u = (ux, g1), v = (vx, g2).  The 2-dim Z-code Zs = <g1,g2> has column P_t on class Z_t (P_t = the T<=4 points of PG(1,3)).
The codeword of Zs vanishing on Z_t is a_t.(g1,g2); its X partner x0_t = a_t.(ux,vx) must, on Z_t, be nonzero off Y_t and
give pairwise distinct lambda_i = -x0_i/y_i on Y_t.  Then every word of C \\ R has at most one zero: d >= n-1.
dim R = T (number of classes), so c = n-1-T.  Output: S = C^perp (symplectic), one generator per line, X part then Z part.
Usage: build_family.py SIZES OUTFILE   SIZES like 3:3,2:2,2:2,2:2  (|Z_t|:|Y_t| per class, T<=4 classes)
"""
import sys, itertools, random
pass  # eacheck.py sits in this folder
import numpy as np
from eacheck import nullspace, rank, symp

P = [(1, 0), (0, 1), (1, 1), (1, 2)]
A = [(0, 1), (1, 0), (1, 2), (1, 1)]   # a_t . P_t = 0 (mod 3)
inv = {1: 1, 2: 2}

def build(sizes, seed=0):
    rnd = random.Random(seed)
    T = len(sizes)
    n = sum(z for z, y in sizes)
    pos = 0
    g1 = [0] * n; g2 = [0] * n
    R0 = []
    target = {}
    classes = []
    for t, (zs, ys) in enumerate(sizes):
        Z = list(range(pos, pos + zs)); pos += zs
        Y = Z[:ys]
        classes.append((Z, Y))
        for i in Z:
            g1[i], g2[i] = P[t]
        y = [0] * n
        if ys == 2:
            y[Y[0]], y[Y[1]] = 1, 2
        elif ys == 3:
            y[Y[0]], y[Y[1]], y[Y[2]] = 1, 1, 1
        else:
            raise SystemExit('|Y_t| must be 2 or 3')
        R0.append(y)
    # choose x0 on each Z_t and solve ux, vx with a_t.(ux,vx) = x0 on Z_t; retry everything until <u,v> != 0
    for attempt in range(100000):
        target = {}
        for t, (Z, Y) in enumerate(classes):
            y = R0[t]
            while True:
                x0 = {i: (rnd.randrange(3) if i in Y else rnd.randrange(1, 3)) for i in Z}
                lam = [(-x0[i] * inv[y[i]]) % 3 for i in Y]
                if len(set(lam)) == len(lam):
                    break
            target[t] = x0
        ux = [0] * n; vx = [0] * n
        for t, (Z, Y) in enumerate(classes):
            a1, a2 = A[t]
            for i in Z:
                if a1:
                    vx[i] = rnd.randrange(3)
                    ux[i] = ((target[t][i] - a2 * vx[i]) * inv[a1]) % 3
                else:
                    ux[i] = rnd.randrange(3)
                    vx[i] = (target[t][i] * inv[a2]) % 3
        form = (sum(ux[i] * g2[i] for i in range(n)) - sum(g1[i] * vx[i] for i in range(n))) % 3
        if form:
            break
    else:
        raise SystemExit('no nondegenerate choice found')
    Crows = [y + [0] * n for y in R0] + [ux + g1, vx + g2]
    return n, T, np.array(Crows, dtype=np.int64) % 3

if __name__ == '__main__':
    sizes = [tuple(map(int, s.split(':'))) for s in sys.argv[1].split(',')]
    n, T, C = build(sizes)
    J = symp(n)
    S = nullspace((C @ J) % 3)   # S = {w : C J w^T = 0} = C^perp (symplectic)
    assert rank(C) == T + 2, 'C rank'
    with open(sys.argv[2], 'w') as f:
        f.write('# S = C^perp for sizes %s ; n=%d, dim R=%d, expect [[%d,1,%d;%d]]\n' % (sys.argv[1], n, T, n, n - 1, n - 1 - T))
        for row in S:
            f.write(' '.join(map(str, row)) + '\n')
    with open(sys.argv[2] + '.C', 'w') as f:
        for row in C:
            f.write(' '.join(map(str, row)) + '\n')
    print('n', n, 'T', T, 'rows(S)', S.shape[0], 'expected [[%d,1,%d;%d]]' % (n, n - 1, n - 1 - T))
