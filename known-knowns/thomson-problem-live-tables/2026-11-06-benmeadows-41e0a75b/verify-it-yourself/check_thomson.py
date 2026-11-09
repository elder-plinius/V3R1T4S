#!/usr/bin/env python3
"""Check a Thomson configuration against its claimed energy and a table value, from the definition.
usage: check_thomson.py <points file: x,y,z per line> <claimed E*> <table minimum> [<expected sha256 of the file>]

Standard library: checks the file's sha256 when one is given, parses the points (>= 20 significant digits each), normalises them in Decimal at 50 digits,
computes E* = sum_{i<j} 1/|x_i - x_j|, and requires |E* - claimed| < 1e-12 and table - E* >= 1e-6.
With numpy installed it also checks the tangent gradient (|grad| < 1e-9 in float64) and that the float64 Hessian on
the product of spheres has 2N - 3 positive eigenvalues once the three rotation modes are set aside.
The last line printed is PASS or FAIL."""
import sys
from decimal import Decimal, getcontext

getcontext().prec = 50


def sig_digits(tok):
    t = tok.lstrip('+-').lower().split('e')[0].replace('.', '').lstrip('0')
    return len(t)


def main():
    path, claimed, table = sys.argv[1], Decimal(sys.argv[2]), Decimal(sys.argv[3])
    ok = True
    if len(sys.argv) > 4:
        import hashlib
        h = hashlib.sha256(open(path, 'rb').read()).hexdigest()
        print('sha256', h)
        if h != sys.argv[4]:
            print('FAIL: the file is not the claimed object (sha256 differs)'); ok = False
    rows = [l.strip().split(',') for l in open(path) if l.strip()]
    if any(len(r) != 3 for r in rows):
        print('FAIL: every line must hold three comma-separated numbers'); ok = False
    toks = [t for r in rows for t in r]
    mind = min(sig_digits(t) for t in toks)
    print('points:', len(rows), ' fewest significant digits in a coordinate:', mind)
    if mind < 20:
        print('FAIL: a coordinate has fewer than 20 significant digits'); ok = False
    P = []
    for r in rows:
        v = [Decimal(t) for t in r]
        n = (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]).sqrt()
        P.append([c / n for c in v])
    if len({tuple(p) for p in P}) != len(P):
        print('FAIL: repeated points'); ok = False
    E = Decimal(0)
    N = len(P)
    for i in range(N):
        a = P[i]
        for j in range(i):
            b = P[j]
            d2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
            E += 1 / d2.sqrt()
    print('E* =', +E)
    print('claimed E* =', claimed, ' difference =', +(E - claimed))
    if abs(E - claimed) >= Decimal('1e-12'):
        print('FAIL: computed energy differs from the claimed energy by 1e-12 or more'); ok = False
    print('table minimum - E* =', +(table - E))
    if table - E < Decimal('1e-6'):
        print('FAIL: not below the table minimum by 1e-6'); ok = False
    try:
        import numpy as np
    except ImportError:
        print('numpy not installed: gradient and Hessian checks skipped (energy checks above still apply)')
        np = None
    if np is not None:
        X = np.array([[float(c) for c in p] for p in P])
        D = X[:, None] - X[None]; r = np.linalg.norm(D, axis=2); np.fill_diagonal(r, np.inf)
        F = np.sum(D / r[..., None] ** 3, axis=1)              # minus the energy gradient of each point
        G = -F + np.sum(F * X, 1, keepdims=True) * X           # tangent part of the gradient
        print('float64 tangent gradient norm: %.3e' % np.linalg.norm(G))
        if np.linalg.norm(G) >= 1e-9:
            print('FAIL: tangent gradient is not zero to float64 accuracy'); ok = False
        H = np.zeros((3 * N, 3 * N))
        for i in range(N):
            d = D[i]; ri = r[i]
            blk = 3 * d[:, :, None] * d[:, None, :] / ri[:, None, None] ** 5 - np.eye(3)[None] / ri[:, None, None] ** 3
            blk[i] = 0
            for j in range(N):
                if j != i:
                    H[3 * i:3 * i + 3, 3 * j:3 * j + 3] = -blk[j]
            H[3 * i:3 * i + 3, 3 * i:3 * i + 3] = blk.sum(0) + np.dot(F[i], X[i]) * np.eye(3)  # sphere curvature term
        B = np.zeros((3 * N, 2 * N))
        for i in range(N):
            n = X[i]; a = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
            t1 = np.cross(n, a); t1 /= np.linalg.norm(t1); t2 = np.cross(n, t1)
            B[3 * i:3 * i + 3, 2 * i] = t1; B[3 * i:3 * i + 3, 2 * i + 1] = t2
        w = np.linalg.eigvalsh(B.T @ H @ B)
        pos = int((w > 1e-6).sum()); zero = int((np.abs(w) <= 1e-6).sum()); neg = int((w < -1e-6).sum())
        print('tangent Hessian: %d positive (need %d), %d zero (rotations, expect 3), %d negative; lowest %s'
              % (pos, 2 * N - 3, zero, neg, ['%.6f' % x for x in w[:6]]))
        if pos != 2 * N - 3 or neg:
            print('FAIL: not a strict local minimum'); ok = False
    print('PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
