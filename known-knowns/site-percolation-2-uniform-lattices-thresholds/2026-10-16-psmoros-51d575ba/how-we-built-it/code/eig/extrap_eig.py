#!/usr/bin/env python3
"""PREREG rule 4 extrapolation of root sequences p(n).

Usage: extrap.py FILE.tsv [FILE.tsv ...]   (lines from eseq.py: LAT MODE W=n root=... ; FAILED lines ignored)
  or   extrap.py --seq NAME n1:p1 n2:p2 ...

For each lattice (and mode) with >= 4 consecutive sizes:
  E1 = exact three-point fit p = pc + a n^-D on the last three sizes;
  E2 = the same on the three sizes before the last;
  E3 = Bulirsch-Stoer (BST) extrapolation with exponent w = D(E1) on the last four sizes (top approximant),
       algorithm of Henkel & Schuetz / Monroe as used in arXiv 1401.7847 sec 4.1 (stated in NOTES before use);
  sigma_B = max(|E1-E2|, |E1-E3|); if the last four values are not monotone with monotone shrinking steps,
  sigma_B = max |p(n) - p(n')| over the last three sizes (PREREG rule 4).
All arithmetic in Decimal with 50 digits.
"""
import sys, re
from decimal import Decimal as D, getcontext
getcontext().prec = 50


def powm(n, e):
    return (D(n).ln() * (-e)).exp()


def fit3(ns, ps):
    (n1, n2, n3), (p1, p2, p3) = ns, ps
    r = (p1 - p2) / (p2 - p3)

    def g(e):
        return (powm(n1, e) - powm(n2, e)) / (powm(n2, e) - powm(n3, e)) - r
    lo, hi = D('0.001'), D('40')
    glo = g(lo)
    if (glo > 0) == (g(hi) > 0):
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        gm = g(mid)
        if (gm > 0) == (glo > 0):
            lo, glo = mid, gm
        else:
            hi = mid
    e = (lo + hi) / 2
    a = (p1 - p2) / (powm(n1, e) - powm(n2, e))
    return p3 - a * powm(n3, e), e, a


def bst(ns, ps, w):
    m = len(ps)
    h = [D(1) / D(n) for n in ns]
    prev = [D(0)] * (m + 1)     # T^(k-2)
    cur = list(ps)              # T^(k-1)
    for k in range(1, m):
        nxt = []
        for i in range(m - k):
            dif = cur[i + 1] - cur[i]
            den2 = cur[i + 1] - prev[i + 1]
            ratio = (h[i] / h[i + k]) ** w if False else ((h[i] / h[i + k]).ln() * w).exp()
            if den2 == 0:
                fac = ratio - 1
            else:
                fac = ratio * (1 - dif / den2) - 1
            nxt.append(cur[i + 1] + dif / fac)
        prev, cur = cur, nxt
    return cur[0]


def analyse(name, seq):
    seq = sorted(seq)
    ns = [n for n, _ in seq]
    ps = [p for _, p in seq]
    print('==', name)
    for i, (n, p) in enumerate(seq):
        dd = ('  diff %+.6e' % float(p - ps[i - 1])) if i else ''
        print('  n=%-3d p=%s%s' % (n, p, dd))
    if len(seq) < 4:
        print('  fewer than 4 sizes: no rule-4 estimate')
        return None
    consecutive = all(ns[i + 1] - ns[i] == ns[1] - ns[0] for i in range(len(ns) - 1))
    l4 = ps[-4:]
    steps = [l4[i + 1] - l4[i] for i in range(3)]
    mono = all(s > 0 for s in steps) or all(s < 0 for s in steps)
    shrink = abs(steps[2]) < abs(steps[1]) < abs(steps[0])
    f1 = fit3(ns[-3:], ps[-3:])
    f2 = fit3(ns[-4:-1], ps[-4:-1])
    if f1 is None or f2 is None or not (mono and shrink):
        sig = max(abs(a - b) for a in ps[-3:] for b in ps[-3:])
        print('  not monotone/smoothly converging over last 4 (mono=%s shrink=%s fit1=%s fit2=%s)' % (mono, shrink, f1 is not None, f2 is not None))
        print('  RULE4 p_B = %s (last value) sigma_B = %.3e (max spread of last 3)' % (ps[-1], float(sig)))
        return ps[-1], sig
    E1, D1, a1 = f1
    E2, D2, a2 = f2
    E3 = bst(ns[-4:], ps[-4:], D1)
    sig = max(abs(E1 - E2), abs(E1 - E3))
    print('  E1 = %.15f (D=%.4f, a=%.4e) on n=%s' % (E1, D1, a1, ns[-3:]))
    print('  E2 = %.15f (D=%.4f, a=%.4e) on n=%s' % (E2, D2, a2, ns[-4:-1]))
    print('  E3 = %.15f (BST w=D1 on n=%s)' % (E3, ns[-4:]))
    print('  consecutive sizes: %s' % consecutive)
    print('  RULE4 p_B = E1 = %.15f sigma_B = %.3e' % (E1, float(sig)))
    return E1, sig


if __name__ == '__main__':
    if sys.argv[1] == '--seq':
        name = sys.argv[2]
        seq = [(int(a.split(':')[0]), D(a.split(':')[1])) for a in sys.argv[3:]]
        analyse(name, seq)
        sys.exit()
    data = {}
    for path in sys.argv[1:]:
        for line in open(path):
            f = line.rstrip('\n').split('\t')
            if len(f) < 4 or not f[3].startswith('root='):
                continue
            n = int(f[2].split('=')[1])
            data.setdefault((f[0], f[1]), {})[n] = D(f[3].split('=')[1])
    for (lat, mode), s in sorted(data.items()):
        analyse('%s %s' % (lat, mode), list(s.items()))
