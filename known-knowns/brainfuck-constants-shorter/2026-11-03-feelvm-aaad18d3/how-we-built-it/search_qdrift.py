#!/usr/bin/env python3
"""q-drift drift-fold search (run 2 lens 1).

Family (one outer drifting loop with an inner transfer loop, as in the page's 30-char 45306 entry):

  prefix:  cell0 <- d_0,  cells 1..k <- d_1..d_k          (d_0 = -q terminates the fold at cell 0)
  loop:    [ +^p > +^a [-< +^b >] << +^q ]
  suffix:  > +^s

Recurrence: v_k = d_k + p + a*b;  v_c = (d_c + q + p) + b*(v_{c+1} + a)  for c < k;  result = v_1 + s.
Continuation needs d_c + q != 0 for c = 1..k-1 and d_k != 0; termination needs d_0 + q = 0.

Cost: |d_0| + k + sum|d_c| + |p| + |a| + |q| + b + |s| + 11.

For each (b,k,a,p,q,s) the digits are chosen by an exact DP minimising the digit cost; every cost-survivor is
rebuilt and run in the reference interpreter (unbounded cells, step limit 5e6). Non-soft mode forces q = 0
(negative d_0 or q would create a negative cell), which reduces the family to run 1's affine fold plus the
free d_0 = 0 — so non-soft results should reproduce run 1 (41/28/49), while soft results may improve.
"""
import os, sys
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(RUN, 'code'))
from bfcheck import run

TARGETS = {257: 33, 114514: 92, 97104: 103, 256: 24, 333: 25, 45306: 30}


def digits_dp(X, k, b, cm, ct, nonneg=False):
    """Min digit cost for X = sum_{c=1}^{k} b^(c-1) e_c.
    Position cost: |e_c - cm| for c<k (cm = q+p), |e_k - ct| for the top (ct = p).
    nonneg: e_c >= cm for c<k and e_k >= ct (prefix digits d_c >= 0)."""
    R = 10 ** 9

    @lru_cache(maxsize=None)
    def f(j, x):
        if j == k:
            return (0, ()) if x == 0 else (R, ())
        r = x % b
        top = (j == k - 1)
        best = (R, ())
        for t in (-1, 0, 1):
            e = r + t * b
            if top:
                if nonneg and e < ct:
                    continue
                cost = abs(e - ct)
            else:
                if nonneg and e < cm:
                    continue
                cost = abs(e - cm)
            sub, ds = f(j + 1, (x - e) // b)
            if sub >= R:
                continue
            tot = cost + sub
            if tot < best[0]:
                best = (tot, (e,) + ds)
        return best
    return f(0, X)


def build(d0, ds, b, a, p, q, s):
    prog = '+' * d0 if d0 > 0 else '-' * (-d0)
    for d in ds:
        prog += '>'
        prog += '+' * d if d > 0 else '-' * (-d)
    prog += '['
    prog += '+' * p if p > 0 else '-' * (-p)
    prog += '>'
    prog += '+' * a if a > 0 else '-' * (-a)
    prog += '[-<' + '+' * b + '>]<<'
    prog += '+' * q if q > 0 else '-' * (-q)
    prog += ']>'
    prog += '+' * s if s > 0 else '-' * (-s)
    return prog


def search(n, bar, soft, bmax=14, kmax=12, amax=14, pmax=4, qmax=4, smax=4):
    best = None
    for b in range(2, bmax + 1):
        for k in range(1, kmax + 1):
            base = 11 + b + k
            if base >= bar:
                continue
            for a in range((0 if not soft else -amax), amax + 1):
                C = a * b * ((b ** k - 1) // (b - 1))
                for p in range((0 if not soft else -pmax), pmax + 1):
                    for q in (range(0, 1) if not soft else range(-qmax, qmax + 1)):
                        for s in range((0 if not soft else -smax), smax + 1):
                            total = base + abs(a) + abs(p) + 2 * abs(q) + abs(s)
                            if total >= bar:
                                continue
                            X = n - s - C
                            cost, es = digits_dp(X, k, b, q + p, p, nonneg=not soft)
                            if cost >= 10 ** 9:
                                continue
                            if total + cost >= bar:
                                continue
                            es = list(es)
                            # constraints: d_k = e_k - p != 0 ; d_c + q = e_c - p != 0 (c<k) ; d_0 = -q
                            if es[-1] - p == 0:
                                continue
                            if any(e - p == 0 for e in es[:-1]):
                                continue
                            d0 = -q
                            ds = [e - q - p for e in es[:-1]] + [es[-1] - p]
                            prog = build(d0, ds, b, a, p, q, s)
                            if len(prog) != total + cost:
                                continue
                            st, val = run(prog, wrap=False, limit=5_000_000)
                            if st == 'OK' and val == n:
                                if best is None or len(prog) < best[0]:
                                    best = (len(prog), b, a, p, q, s, d0, ds, prog)
    return best


def main():
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    print('q-drift family: prefix d0..dk + [ +^p > +^a [-<+^b>] << +^q ] > +^s')
    for n, bar in TARGETS.items():
        for mode in ('nonsoft', 'soft'):
            best = search(n, bar, soft=(mode == 'soft'))
            if best:
                L, b, a, p, q, s, d0, ds, prog = best
                print('FOUND %-8s n=%-7d bar=%-4d len=%d b=%d a=%d p=%d q=%d s=%d d0=%d digits=%s'
                      % (mode, n, bar, L, b, a, p, q, s, d0, ds))
                print('     ', prog)
            else:
                print('none  %-8s n=%-7d bar=%s' % (mode, n, bar))


if __name__ == '__main__':
    main()
