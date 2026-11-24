#!/usr/bin/env python3
"""Find the smallest Y on the grid k/1000 that cert_arb certifies (bisection on k, then confirm k passes and k-1 fails)."""
import sys, io, contextlib
from cert_arb import certify
def ok(k, c, dens, prec):
    Y = f"{k//1000}.{k%1000:03d}"
    with contextlib.redirect_stdout(io.StringIO()):
        r, _ = certify(Y, c, dens, prec, verbose=False)
    return r
def smallest(c, dens, prec, lo=25000, hi=36000):
    assert ok(hi, c, dens, prec) and not ok(lo, c, dens, prec)
    while hi - lo > 1:
        mid = (lo + hi)//2
        if ok(mid, c, dens, prec): hi = mid
        else: lo = mid
    return hi
if __name__ == '__main__':
    for c in ['51.34', '54.004', '53.989', '57.54']:
        for dens in ['thm11', 'thm12', 'thm13', 'kln']:
            r = [smallest(c, dens, p) for p in (128, 256)]
            k = r[0]
            print(f"c={c:7s} dens={dens:6s} Y_cert(prec128)={k/1000:.3f} Y_cert(prec256)={r[1]/1000:.3f} agree={r[0]==r[1]}")
            sys.stdout.flush()
