#!/usr/bin/env python3
"""Independent REPRODUCE check (spheres in unit sphere). Usage: indep_check.py DATA_DIR
DATA_DIR holds radius.txt, ssp.html and extracted sspN.txt. Container radius 1 (ssp.html: ratio=1/radius).
Coordinate-supported radius r_c = min( min_ij |ci-cj|/2 , min_i (1-|ci|) ), exact rationals + mpmath dps=50."""
import sys, os, re, math
from fractions import Fraction as F
from mpmath import mp, mpf, sqrt
mp.dps = 50
D = sys.argv[1]
rad = {}
for l in open(os.path.join(D, 'radius.txt')):
    s = l.split()
    if len(s) == 2 and not l.startswith('#'): rad[int(s[0])] = s[1]
html = {}
for m in re.finditer(r'name="ssp(\d+)">.*?</a></td>\s*<td>(?:&nbsp;)*\s*([0-9.]+)</td>', open(os.path.join(D, 'ssp.html')).read()):
    html[int(m.group(1))] = m.group(2)
def coords(n):
    P = []
    for l in open(os.path.join(D, 'ssp%d.txt' % n)):
        s = l.split()
        if l.startswith('#') or len(s) < 4: continue
        P.append(tuple(F(x) for x in s[1:4]))
    return P
def rc(P, rhint):
    fl = [tuple(float(v) for v in p) for p in P]
    h = 2 * rhint * 1.05
    g = {}
    for i, p in enumerate(fl): g.setdefault(tuple(int(math.floor(v / h)) for v in p), []).append(i)
    cand = []
    best = float('inf')
    for k, lst in g.items():
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for j in g.get((k[0]+dx, k[1]+dy, k[2]+dz), ()):
                        for i in lst:
                            if i < j:
                                d = sum((a-b)**2 for a, b in zip(fl[i], fl[j]))
                                if d < (2*rhint*1.001)**2: cand.append((i, j))
    dmin = min(sum((a-b)**2 for a, b in zip(P[i], P[j])) for i, j in cand) if cand else None
    rp = sqrt(mpf(dmin.numerator)/dmin.denominator)/2 if dmin is not None else mpf('inf')
    nm = max(sum(v*v for v in p) for p in P)
    rb = 1 - sqrt(mpf(nm.numerator)/nm.denominator)
    return min(rp, rb), (len(P) == 1 or cand)
rows = []; miss = []
for n in sorted(rad):
    try: P = coords(n)
    except FileNotFoundError: miss.append(n); continue
    if len(P) != n: print('COUNTMISMATCH', n, len(P)); continue
    r, ok = rc(P, float(rad[n]))
    gap = mpf(rad[n]) - r
    hg = mpf(html[n]) - r if n in html else None
    if gap > mpf('1e-12'):
        rows.append((n, gap, hg)); print(n, rad[n], mp.nstr(r, 15), 'gap', mp.nstr(gap, 4), 'html-coord', mp.nstr(hg, 3) if hg is not None else 'NA')
    if gap < -mpf('1e-12'): print('BELOW', n, mp.nstr(gap, 4))
print('# missing coord files', miss)
print('# rows', len(rows))
if rows:
    g = sorted(rows, key=lambda t: t[1]); print('# min', g[0][0], mp.nstr(g[0][1], 4), 'max', g[-1][0], mp.nstr(g[-1][1], 4), 'smallestN', min(t[0] for t in rows), 'maxN', max(t[0] for t in rows))
    hm = max(abs(t[2]) for t in rows if t[2] is not None); print('# max |html-coord|', mp.nstr(hm, 4), 'html missing', sum(t[2] is None for t in rows))
    print('PASS' if len(rows) == 90 and hm < mpf('2.8e-12') else 'FAIL')
