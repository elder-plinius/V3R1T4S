#!/usr/bin/env python3
"""Standard-library check of a Thomson configuration (no numpy, no mpmath).

Reads N lines "x y z", normalises each point with Python's decimal module at 40 significant digits, and computes
E = sum_{i<j} 1/|x_i - x_j| and the 2-norm of the tangent gradient (g_i - (x_i.g_i) x_i).

Usage: verify_stdlib.py <points-file> [--bar B] [--expect E] [--others f1 f2 ...]
  --bar B       require E <= B - 1e-6
  --expect E    require |E - expected| < 1e-12
  --others ...  energies of other (already polished) configurations; require each >= E + 1e-6
Prints one line per check and a last line PASS or FAIL. The Hessian test needs linear algebra and is not here.
"""
import sys
from decimal import Decimal, getcontext

getcontext().prec = 40


def load(path):
    pts = []
    for line in open(path):
        p = line.split()
        if len(p) < 3:
            continue
        try:
            v = [Decimal(s) for s in p[-3:]]
        except Exception:
            continue
        n = (v[0] * v[0] + v[1] * v[1] + v[2] * v[2]).sqrt()
        pts.append([v[0] / n, v[1] / n, v[2] / n])
    return pts


def energy_grad(pts):
    N = len(pts)
    E = Decimal(0)
    G = [[Decimal(0)] * 3 for _ in range(N)]
    for i in range(N):
        xi = pts[i]
        gi = G[i]
        for j in range(i + 1, N):
            xj = pts[j]
            dx = xi[0] - xj[0]; dy = xi[1] - xj[1]; dz = xi[2] - xj[2]
            r2 = dx * dx + dy * dy + dz * dz
            r = r2.sqrt()
            E += 1 / r
            k = 1 / (r2 * r)
            fx = dx * k; fy = dy * k; fz = dz * k
            gi[0] -= fx; gi[1] -= fy; gi[2] -= fz
            gj = G[j]
            gj[0] += fx; gj[1] += fy; gj[2] += fz
    s = Decimal(0)
    for x, g in zip(pts, G):
        lam = x[0] * g[0] + x[1] * g[1] + x[2] * g[2]
        for a in range(3):
            t = g[a] - lam * x[a]
            s += t * t
    return E, s.sqrt()


def main(argv):
    path = argv[1]
    bar = expect = None
    others = []
    i = 2
    while i < len(argv):
        if argv[i] == '--bar':
            bar = Decimal(argv[i + 1]); i += 2
        elif argv[i] == '--expect':
            expect = Decimal(argv[i + 1]); i += 2
        elif argv[i] == '--others':
            others = argv[i + 1:]; break
        else:
            i += 1
    pts = load(path)
    E, g = energy_grad(pts)
    ok = True
    print('N = %d' % len(pts))
    print('E = %s' % format(E, '.25f'))
    print('tangent gradient norm = %s' % format(g, '.3e'))
    if g >= Decimal('1e-20'):
        ok = False; print('FAIL: gradient norm not < 1e-20')
    if expect is not None:
        d = abs(E - expect)
        print('|E - expected| = %s' % format(d, '.3e'))
        if d >= Decimal('1e-12'):
            ok = False; print('FAIL: energy differs from the expected value')
    if bar is not None:
        m = bar - E
        print('bar - E = %s (need >= 1e-6)' % format(m, '.10f'))
        if m < Decimal('1e-6'):
            ok = False; print('FAIL: not below the bar by 1e-6')
    for f in others:
        Eo, go = energy_grad(load(f))
        print('other %s: E = %s, |g| = %s, E_other - E = %s (need >= 1e-6)' % (
            f.split('/')[-1], format(Eo, '.20f'), format(go, '.3e'), format(Eo - E, '.10f')))
        if Eo - E < Decimal('1e-6'):
            ok = False; print('FAIL: other configuration not above E by 1e-6')
    print('PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main(sys.argv))
