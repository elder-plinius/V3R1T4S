#!/usr/bin/env python3
"""Deterministic search over the affine drift-fold family for Brainfuck constants.

Family (one outer loop, drifting pointer):
    prefix: cells 1..k <- d_1..d_k, d_1 least significant
    loop:   [ +^p > +^a [-< +^b >] << ]
    suffix: >
Recurrence during the loop (cell i, i=k..1):
    v_i <- d_i + p + b*(v_{i+1} + a),   v_{k+1} = 0
Value: n = v_1.  Cost: k + sum|d_i| + |p| + |a| + b + 11.

Two modes:
  * signed: digits d_i may be negative (page's "(soft)" for n > 255)
  * nonsoft: d_i, a, p >= 0 (all cell values stay non-negative)

The digit choice for each (a,b,k,p) is solved exactly by a signed-digit DP
(minimising sum|d_i|), then every survivor is rebuilt and run in the reference
interpreter code/bfcheck.py.  Deterministic and reproducible.
"""
import json, os, sys
from functools import lru_cache

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, os.path.join(RUN, 'code'))
from bfcheck import run

TARGETS = {257: 33, 114514: 92, 97104: None, 256: 24, 333: 25, 45306: 30}
TABLE_114514_PRINT = 58  # the 58-char entry prints bytes; 92 leaves the value


def min_digits_signed(X, k, b):
    @lru_cache(None)
    def f(j, x):
        if j == k:
            return (0, ()) if x == 0 else (None, ())
        r = x % b
        best = None
        for s in (-1, 0, 1):
            d = r + s * b
            sub, ds = f(j + 1, (x - d) // b)
            if sub is None:
                continue
            c = abs(d) + sub
            if best is None or c < best[0]:
                best = (c, (d,) + ds)
        return best if best is not None else (None, ())
    return f(0, X)


def build(ds, b, a, p):
    s = ''
    for d in ds:
        s += '>'
        s += '+' * d if d > 0 else '-' * (-d)
    body = ('+' * p if p > 0 else '-' * (-p) if p < 0 else '')
    abody = ('+' * a if a > 0 else '-' * (-a) if a < 0 else '')
    s += '[' + body + '>' + abody + '[-<' + '+' * b + '>]<<]'
    s += '>'
    return s


def search_signed(n, table, bmax=12, kmax=10, amax=10):
    cands = []
    for b in range(2, bmax + 1):
        for k in range(1, kmax + 1):
            for a in range(-amax, amax + 1):
                for p in range(-amax, amax + 1):
                    C = (p + a * b) * ((b ** k - 1) // (b - 1))
                    cd, ds = min_digits_signed(n - C, k, b)
                    if cd is None or not ds or ds[-1] == 0:
                        continue
                    total = k + cd + abs(p) + abs(a) + b + 11
                    if table is not None and total >= table:
                        continue
                    prog = build(ds, b, a, p)
                    if len(prog) == total:
                        cands.append((total, b, a, p, list(ds), prog))
    for cand in sorted(cands)[:300]:
        st, val = run(cand[5], wrap=False, limit=5_000_000)
        if st == 'OK' and val == n:
            return cand
    return None


def search_nonsoft(n, table, bmax=40, kmax=12, aop=25):
    cands = []
    for b in range(2, bmax + 1):
        for k in range(1, kmax + 1):
            for a in range(0, aop + 1):
                for p in range(0, aop + 1):
                    C = a * b * ((b ** k - 1) // (b - 1))
                    X = n - C
                    if X < 0:
                        continue
                    es = []
                    t = X
                    for _ in range(k):
                        es.append(t % b)
                        t //= b
                    if t != 0 or es[-1] == 0 or any(e - p < 0 for e in es):
                        continue
                    total = k + sum(es) + p + a + b + 11
                    if table is not None and total >= table:
                        continue
                    prog = build([e - p for e in es], b, a, p)
                    if len(prog) == total:
                        cands.append((total, b, a, p, es, prog))
    for cand in sorted(cands)[:300]:
        st, val = run(cand[5], wrap=False, limit=5_000_000)
        if st == 'OK' and val == n:
            return cand
    return None


def main():
    try:
        sys.stdout.reconfigure(line_buffering=True)
    except Exception:
        pass
    print('family: prefix digits + [ +^p > +^a [-< +^b >] << ] + >')
    print('reference interpreter: code/bfcheck.py, unbounded cells, step limit 1e7')
    for n, table in TARGETS.items():
        for label, fn in (('signed', search_signed), ('nonsoft', search_nonsoft)):
            best = fn(n, table)
            if best:
                total, b, a, p, ds, prog = best
                print('FOUND %-10s n=%-7d table=%-5s len=%d b=%d a=%d p=%d digits=%s'
                      % (label, n, table, total, b, a, p, ds))
                print('    ', prog)
            else:
                print('none  %-10s n=%-7d table=%s' % (label, n, table))


if __name__ == '__main__':
    main()
