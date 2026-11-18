#!/usr/bin/env python3
"""Check one Game of Sloanes complex line packing from the definition. Python 3 standard library only.

usage: check_gos.py FILE d n CLAIMED TABLE LOWER_BOUND SHA256 [PENDING]

FILE holds 2*d*n decimal numbers, one or more per line (blank lines and lines starting with '#' are skipped):
the real parts of all n vectors, vector by vector, then the imaginary parts in the same order (the layout of
the CurrentBestPackings/ files of https://github.com/gnikylime/GameofSloanes).
Coherence mu = max over j < k of |<phi_j, phi_k>| / (|phi_j| |phi_k|). Every coordinate is read as an exact
decimal; the maximising pair is chosen with exact integer arithmetic and mu is printed from a 60-digit
Decimal square root.
PASS needs: the sha256 matches; exactly 2*d*n finite numbers, each written with at least 16 significant
digits; no zero vector; |mu - CLAIMED| < 1e-30; TABLE - mu >= 1e-8; mu >= LOWER_BOUND; and, if PENDING is
given (the lowest coherence among the packings in open pull requests to the leaderboard), PENDING - mu >= 1e-7.
The last output line is PASS or FAIL.
"""
import hashlib
import sys
from decimal import Decimal, InvalidOperation, getcontext

getcontext().prec = 120


def fail(msg):
    print(msg)
    print('FAIL')
    sys.exit(1)


def sig_digits(tok):
    mant = tok.lower().split('e')[0].lstrip('+-').replace('.', '').lstrip('0')
    return len(mant)


def main(argv):
    if len(argv) not in (8, 9):
        fail(__doc__.strip().splitlines()[2])
    path, d, n = argv[1], int(argv[2]), int(argv[3])
    claimed, table, lb, want = Decimal(argv[4]), Decimal(argv[5]), Decimal(argv[6]), argv[7].lower()
    pending = Decimal(argv[8]) if len(argv) == 9 else None
    raw = open(path, 'rb').read()
    h = hashlib.sha256(raw).hexdigest()
    print('sha256 %s' % h)
    if h != want:
        fail('sha256 does not match the expected %s' % want)
    toks = []
    for line in raw.decode('ascii').splitlines():
        s = line.strip()
        if s and not s.startswith('#'):
            toks.extend(t for t in s.replace(',', ' ').split() if t)
    if len(toks) != 2 * d * n:
        fail('numbers: %d, expected 2*d*n = %d' % (len(toks), 2 * d * n))
    try:
        vals = [Decimal(t) for t in toks]
    except InvalidOperation:
        fail('a token is not a decimal number')
    if not all(v.is_finite() for v in vals):
        fail('a number is not finite')
    fewest = min(sig_digits(t) for t in toks)
    print('d = %d, n = %d, numbers: %d, fewest significant digits in a coordinate: %d' % (d, n, len(toks), fewest))
    if fewest < 16:
        fail('a coordinate has fewer than 16 significant digits')
    k = max(0, max(-v.as_tuple().exponent for v in vals))
    ints = [int(v.scaleb(k)) for v in vals]
    if any(Decimal(i) != v.scaleb(k) for i, v in zip(ints, vals)):
        fail('internal error: inexact integer scaling')
    re_ = [ints[j * d:(j + 1) * d] for j in range(n)]
    im_ = [ints[d * n + j * d:d * n + (j + 1) * d] for j in range(n)]
    norms = [sum(a * a + b * b for a, b in zip(re_[j], im_[j])) for j in range(n)]
    if min(norms) == 0:
        fail('a vector is zero')
    best = None
    for j in range(n):
        for l in range(j + 1, n):
            pr = sum(a * c + b * e for a, b, c, e in zip(re_[j], im_[j], re_[l], im_[l]))
            pi = sum(a * e - b * c for a, b, c, e in zip(re_[j], im_[j], re_[l], im_[l]))
            num, den = pr * pr + pi * pi, norms[j] * norms[l]
            if best is None or num * best[1] > best[0] * den:
                best = (num, den, j, l)
    num, den, j, l = best
    getcontext().prec = 60
    mu = (Decimal(num) / Decimal(den)).sqrt()
    print('coherence mu = %s' % format(mu.quantize(Decimal(10) ** -40)))
    print('claimed      = %s  difference %.3e' % (argv[4], abs(mu - claimed)))
    print('attaining pair (0-based vectors) (%d, %d)' % (j, l))
    if abs(mu - claimed) >= Decimal('1e-30'):
        fail('computed coherence differs from the claimed value')
    print('leaderboard  = %s  leaderboard - mu = %.6e  (need >= 1e-8)' % (argv[5], table - mu))
    if table - mu < Decimal('1e-8'):
        fail('not at least 1e-8 below the leaderboard value')
    print('lower bound  = %s  mu - lower bound = %.6e  (need >= 0)' % (argv[6], mu - lb))
    if mu < lb:
        fail('below the lower bound: a bug, not a packing')
    if pending is not None:
        print('best pending = %s  pending - mu = %.6e  (need >= 1e-7)' % (argv[8], pending - mu))
        if pending - mu < Decimal('1e-7'):
            fail('not at least 1e-7 below the best packing in an open pull request')
    print('PASS')


if __name__ == '__main__':
    main(sys.argv)
