#!/usr/bin/env python3
"""Evaluator lens: Method B = direct 3D Cartesian midpoint integration of Eq. (3) (not the reduced 1D form);
Method A' = independent scipy 1D quadrature + minimisation over sigma (log grid of 601 + golden section).
Units: lengths in m, energy in J via c^4/G. beta passed explicitly."""
import numpy as np
from scipy import integrate, optimize

c = 299792458.0
G = 6.67430e-11
K = c**4 / G
R = 5e-3
USTAR = 0.0299002893428026   # from code/check_bound.py output (also recomputed below)


def ustar():
    g = 1 + 1e-7
    return optimize.brentq(lambda u: (2 - u*u) / (2*np.sqrt(1 - u*u)) - g, 1e-6, 0.5, xtol=1e-16)


def fprime(r, s):
    return s * (1/np.cosh(s*(r+R))**2 - 1/np.cosh(s*(r-R))**2) / (2*np.tanh(s*R))


def T00(x, y, z, s, beta):
    r = np.sqrt(x*x + y*y + z*z)
    rho2 = y*y + z*z
    with np.errstate(invalid='ignore', divide='ignore'):
        q = np.where(r > 0, rho2/(r*r), 0.0)
    return -K/(8*np.pi) * beta**2 * q/4 * fprime(r, s)**2


def E3d(s, beta, n):
    # use axial symmetry only through octant symmetry (T00 even in x, y, z): integrate octant, multiply by 8
    L = R + 30.0/s if s*R > 1 else 30.0/s + R
    h = L/n
    g = (np.arange(n) + 0.5) * h
    tot = 0.0
    for xi in g:  # loop over x slices to bound memory (n^2 per slice)
        Y, Z = np.meshgrid(g, g, indexing='ij')
        tot += T00(xi, Y, Z, s, beta).sum()
    return 8 * tot * h**3


def E1d(s, beta):
    w = 1.0/s
    pts = sorted(set([0.0, max(R - 40*w, 0.0), R, R + 40*w]))
    tot = 0.0
    for a, b in zip(pts[:-1], pts[1:]):
        tot += integrate.quad(lambda r: fprime(r, s)**2 * r*r, a, b, epsabs=0, epsrel=1e-12, limit=400)[0]
    tot += integrate.quad(lambda r: fprime(r, s)**2 * r*r, pts[-1], np.inf, epsabs=0, epsrel=1e-12, limit=400)[0]
    return -K/12 * beta**2 * tot


if __name__ == '__main__':
    u = ustar()
    print('u* (scipy brentq) =', repr(u), ' vs formalist 0.0299002893428026, diff', u - USTAR)
    beta = u
    print('Method B (3D midpoint, octant x8) vs Method A\' (1D quad):')
    for sR in [0.5, 1.0, 2.0, 5.0]:
        s = sR/R
        a = E1d(s, beta)
        row = []
        for n in [100, 200, 400]:
            b = E3d(s, beta, n)
            row.append((n, b, b/a - 1))
        print('  sR=%.1f  A=%.10e' % (sR, a) + ''.join('  n=%d B/A-1=%+.2e' % (n, d) for n, b, d in row))
    # minimisation over sigma
    lg = np.linspace(-3, 3, 601)
    vals = np.array([E1d(10**k/R, beta) for k in lg])
    i = int(np.argmax(vals))  # least negative E = smallest |E| over sigma
    print('log grid 601 pts sR in [1e-3,1e3]: smallest |E| at sR=%.6f E=%.10e (edges: %.3e, %.3e)' % (10**lg[i], vals[i], vals[0], vals[-1]))
    res = optimize.minimize_scalar(lambda k: -E1d(10**k/R, beta), bracket=(lg[i-1], lg[i], lg[i+1]), method='golden', tol=1e-10)
    Emin = -res.fun  # E at the sigma minimising |E|
    bound = -K/48 * beta**2 * R
    print('golden: sR*=%.8f  E_min=%.10e J  (%.6e kg)' % (10**res.x, Emin, Emin/c**2))
    print('closed-form bound=%.10e J; E_min/bound=%.8f; E_min <= bound: %s; bound <= -1e30: %s' % (bound, Emin/bound, Emin <= bound, bound <= -1e30))
    b2 = 4e-4
    print('slide 0.0004c: E_min=%.10e J (%.6e kg), bound=%.10e J, bound <= -1e30: %s' % (Emin*(b2/beta)**2, Emin*(b2/beta)**2/c**2, -K/48*b2**2*R, -K/48*b2**2*R <= -1e30))
    # E_min scaling with R: E_min = -(K/12) beta^2 R * min_x J(x), J dimensionless
    print('E_min per metre of R at u*: %.6e J/m  (so any R >= 1 mm gives <= %.4e J)' % (Emin/R, Emin/R*1e-3))
    print('known negative beta=0:', E1d(1/R, 0.0), ' 3D:', E3d(1/R, 0.0, 50))
