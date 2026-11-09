#!/usr/bin/env python3
"""Independent certificate verifier (EXTENDER lens, run 2026-10-15-0312).

Written from the equations in BRIEF.md, in the ORIGINAL (a, b, c) coordinates, without importing
or reusing the solver.  It does not use fractions.Fraction: every rational is a pair of Python ints
(num, den) and every equation / comparison is decided by exact integer cross-multiplication.

For a certificate {"n": n, "P000": "p/q", "table": [[a, b, c, "num/den", "toss"|"stop"], ...]} it checks
  (1) the table lists every position 0 <= b < n, 0 <= c < n, 0 <= a < n - b exactly once (n^2 (n+1)/2 rows),
      with integer coordinates and nothing else;
  (2) each value is a string "num/den" of decimal digits, den > 0, gcd(num, den) = 1 (reduced), 0 <= value <= 1;
  (3) a = 0 rows have action "toss" and satisfy P(0,b,c) = 1/2 (1 - P(0,c,b)) + 1/2 P(1,b,c);
  (4) a >= 1 rows have action "toss" or "stop" and satisfy P(a,b,c) = max(cont, stop) with
      cont = 1/2 (1 - P(0,c,b)) + 1/2 P(a+1,b,c),  stop = 1 - P(0,c,a+b),
      and the claimed action attains the max;  P(x,y,z) = 1 whenever x + y >= n;
  (5) the "P000" field equals the table value at (0,0,0);
  (6) optionally (--oeis DIR) P(0,0,0) equals A387261(n)/A387262(n) from the b-files when n is listed there.
Prints one line per certificate and a final summary line.

Usage: python3 -I my_verify.py [--oeis DATA_DIR] cert1.json [cert2.json ...]
"""
import json
import math
import re
import sys

FRAC_RE = re.compile(r'^([0-9]+)/([0-9]+)$')


def parse_value(s):
    if not isinstance(s, str):
        raise ValueError('value is not a string: %r' % (s,))
    m = FRAC_RE.match(s)
    if not m:
        raise ValueError('value not of the form num/den: %r' % (s,))
    num, den = int(m.group(1)), int(m.group(2))
    if den <= 0:
        raise ValueError('non-positive denominator: %r' % (s,))
    if math.gcd(num, den) != 1:
        raise ValueError('fraction not reduced: %r' % (s,))
    if num > den:
        raise ValueError('value exceeds 1: %r' % (s,))
    return (num, den)


# exact rational helpers on (num, den) pairs, den > 0, not necessarily reduced
def r_sub(x, y):
    return (x[0] * y[1] - y[0] * x[1], x[1] * y[1])


def r_add(x, y):
    return (x[0] * y[1] + y[0] * x[1], x[1] * y[1])


def r_half(x):
    return (x[0], 2 * x[1])


def r_cmp(x, y):
    d = x[0] * y[1] - y[0] * x[1]
    return (d > 0) - (d < 0)


ONE = (1, 1)


def verify(path, oeis=None):
    with open(path) as f:
        cert = json.load(f)
    n = cert['n']
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError('bad n')
    table = cert['table']
    expected = n * n * (n + 1) // 2
    if len(table) != expected:
        raise ValueError('table has %d rows, expected %d' % (len(table), expected))
    val = {}
    act = {}
    for row in table:
        if not isinstance(row, list) or len(row) != 5:
            raise ValueError('bad row %r' % (row,))
        a, b, c, s, ac = row
        for t in (a, b, c):
            if not isinstance(t, int) or isinstance(t, bool):
                raise ValueError('non-integer coordinate in %r' % (row,))
        if not (0 <= b < n and 0 <= c < n and 0 <= a < n - b):
            raise ValueError('position out of range %r' % (row,))
        if (a, b, c) in val:
            raise ValueError('duplicate position %r' % ((a, b, c),))
        if ac not in ('toss', 'stop'):
            raise ValueError('bad action %r' % (row,))
        if a == 0 and ac != 'toss':
            raise ValueError('a = 0 must toss: %r' % (row,))
        val[(a, b, c)] = parse_value(s)
        act[(a, b, c)] = ac
    if len(val) != expected:
        raise ValueError('missing positions')

    def P(a, b, c):
        if a + b >= n:
            return ONE
        return val[(a, b, c)]

    ties = 0
    nstop = 0
    for (a, b, c), v in val.items():
        opp = P(0, c, b)
        cont = r_half(r_add(r_sub(ONE, opp), P(a + 1, b, c)))
        if a == 0:
            if r_cmp(v, cont) != 0:
                raise ValueError('forced-toss equation fails at %r' % ((a, b, c),))
            continue
        stop = r_sub(ONE, P(0, c, a + b))
        k = r_cmp(cont, stop)
        best = cont if k >= 0 else stop
        if r_cmp(v, best) != 0:
            raise ValueError('Bellman max fails at %r' % ((a, b, c),))
        chosen = cont if act[(a, b, c)] == 'toss' else stop
        if r_cmp(chosen, v) != 0:
            raise ValueError('claimed action %s does not attain the max at %r' % (act[(a, b, c)], (a, b, c)))
        if k == 0:
            ties += 1
        if act[(a, b, c)] == 'stop':
            nstop += 1
    p000 = parse_value(cert['P000'])
    if r_cmp(p000, val[(0, 0, 0)]) != 0:
        raise ValueError('P000 field differs from table value at (0,0,0)')
    oeis_status = 'n/a'
    if oeis is not None and n in oeis:
        oeis_status = 'OEIS-MATCH' if oeis[n] == val[(0, 0, 0)] else 'OEIS-MISMATCH'
        if oeis_status == 'OEIS-MISMATCH':
            raise ValueError('P(0,0,0) differs from OEIS b-files')
    return n, len(val), ties, nstop, val[(0, 0, 0)], oeis_status


def read_b(path):
    d = {}
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                k, v = line.split()
                d[int(k)] = int(v)
    return d


def main():
    args = sys.argv[1:]
    oeis = None
    if args and args[0] == '--oeis':
        num = read_b(args[1] + '/b387261.txt')
        den = read_b(args[1] + '/b387262.txt')
        oeis = {k: (num[k], den[k]) for k in num}
        args = args[2:]
    npass = 0
    nfail = 0
    for path in args:
        try:
            n, cnt, ties, nstop, p, st = verify(path, oeis)
            npass += 1
            print('PASS %s n=%d positions=%d stop_actions=%d exact_ties=%d %s P(0,0,0)=%d/%d'
                  % (path, n, cnt, nstop, ties, st, p[0], p[1]))
        except Exception as e:  # report and continue
            nfail += 1
            print('FAIL %s: %s' % (path, e))
        sys.stdout.flush()
    print('my_verify summary: %d passed, %d failed, of %d certificates' % (npass, nfail, npass + nfail))
    sys.exit(0 if nfail == 0 else 1)


if __name__ == '__main__':
    main()
