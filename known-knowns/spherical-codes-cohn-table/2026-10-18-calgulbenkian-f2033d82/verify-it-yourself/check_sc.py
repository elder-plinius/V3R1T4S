"""Spherical-code checker against saved rows of Henry Cohn's table (spherical-codes.org). Standard library only.
Usage: python3 -I check_sc.py index_rows.html plain_rows.csv FILE...
FILE is named {d}x{N}.txt: N lines, d comma-separated coordinates each.
For every FILE: normalise each vector to unit length at 50 significant digits (decimal module), compute the maximum
pairwise inner product c* over ALL N(N-1)/2 pairs, compare with the 12-decimal /plain cosine, and read the saved index
row for a proven-optimal mark and for the text 'needs more optimization'."""
import re, sys, os
from decimal import Decimal, getcontext
getcontext().prec = 50

idx = open(sys.argv[1]).read()
plain = {}
for l in open(sys.argv[2]):
    p = l.strip().split(',')
    if len(p) >= 3 and p[0].isdigit():
        plain[(int(p[0]), int(p[1]))] = p[2]
rows = {}
for m in re.finditer(r'<tr>\s*<td>(\d+)</td>\s*<td><a href="/data/(\d+)/(\d+)">\d+</a>(.*?)</td>\s*<td>([0-9.]+)</td>\s*<td>(.*?)</td>\s*</tr>', idx, re.S):
    d, N = int(m.group(2)), int(m.group(3))
    rows[(d, N)] = dict(star='&ast;' in m.group(4) or '*' in m.group(4), cos=m.group(5),
                        label='needs more optimization' in m.group(6),
                        ref=re.sub('<.*?>', '', m.group(6)).strip()[:80])
for f in sys.argv[3:]:
    d, N = map(int, os.path.basename(f)[:-4].split('x'))
    V = [[Decimal(x) for x in l.strip().split(',')] for l in open(f) if l.strip()]
    assert len(V) == N and all(len(v) == d for v in V), 'shape'
    U = []
    for v in V:
        s = sum((y * y for y in v), Decimal(0)).sqrt()
        U.append([x / s for x in v])
    cs = None
    for i in range(N):
        a = U[i]
        for j in range(i + 1, N):
            b = U[j]
            ip = sum((x * y for x, y in zip(a, b)), Decimal(0))
            if cs is None or ip > cs:
                cs = ip
    r = rows.get((d, N))
    t = Decimal(plain[(d, N)])
    gain = t - cs
    print('(%d,%d) c*=%s table=%s gain=%s star=%s needs_opt=%s ref=%s index_cos=%s %s' % (
        d, N, format(cs, '.20g'), plain[(d, N)], format(gain, '.6g').replace('E', 'e'),
        r and r['star'], r and r['label'], r and r['ref'], r and r['cos'],
        'OK' if gain >= Decimal('1e-10') else 'NO'))
