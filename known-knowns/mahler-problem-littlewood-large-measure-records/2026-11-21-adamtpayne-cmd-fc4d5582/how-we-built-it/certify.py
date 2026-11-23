#!/usr/bin/env python3
"""Certify the Mahler measure of a Littlewood polynomial two ways.

Method 1 (rigorous): FLINT/Arb root isolation (fmpz_poly.complex_roots), then the product of
max(1, |root|) in ball arithmetic. A root whose modulus ball contains 1 contributes the ball
[1, upper]; precision is raised until the result's radius is below 1e-25.
Method 2 (independent numerics): mpmath.polyroots at 60 digits.

usage: certify.py '+-++-...'  [compare_value]    (coefficient string, constant term first)
"""
import sys
import flint
import mpmath


def parse(s):
    return [1 if ch == '+' else -1 for ch in s.strip()]


def mahler_arb(coeffs, prec=200):
    while True:
        flint.ctx.prec = prec
        p = flint.fmpz_poly(coeffs)  # coeffs[k] = coefficient of x^k
        M = flint.arb(abs(coeffs[-1]))
        for r, mult in p.complex_roots():
            m = abs(r)
            if m > 1:
                f = m
            elif m < 1:
                f = flint.arb(1)
            else:  # ball contains 1: max(1, |r|) lies in [1, upper]
                up = m.mid() + m.rad()
                f = flint.arb(1).union(flint.arb(up))
            for _ in range(mult):
                M *= f
        if M.rad() < flint.arb('1e-25') or prec > 4000:
            return M
        prec *= 2


def mahler_mpmath(coeffs, dps=60):
    mpmath.mp.dps = dps
    roots = mpmath.polyroots(list(reversed(coeffs)), maxsteps=500, extraprec=400)
    M = mpmath.mpf(abs(coeffs[-1]))
    for r in roots:
        M *= max(mpmath.mpf(1), abs(r))
    return M


if __name__ == "__main__":
    s = sys.argv[1]
    c = parse(s)
    d = len(c) - 1
    M1 = mahler_arb(c)
    M2 = mahler_mpmath(c)
    mid1 = mpmath.mpf(M1.mid().str(40, radius=False))
    print(f"degree {d}")
    print(f"arb ball   : {M1.str(30)}")
    print(f"mpmath 60d : {mpmath.nstr(M2, 30)}")
    print(f"agree to 20 digits: {abs(mid1 - M2) < mpmath.mpf('1e-20') * M2}")
    if len(sys.argv) > 2:
        T = flint.arb(sys.argv[2])
        lo = M1.mid() - M1.rad()
        print(f"table value: {sys.argv[2]}  certified M - table > 1e-9: {bool(lo - T > flint.arb('1e-9'))}  (margin {float((M1 - T).mid()):.3e})")
