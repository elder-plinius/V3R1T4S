# Criterion skeptic checker: Decimal prec 50. Run from this folder: python3 check_criterion.py
import re, tarfile, random, math
from decimal import Decimal as D, getcontext
getcontext().prec = 50
rt = {}
for l in open('live/radius.txt'):
    p = l.split()
    if len(p) == 2 and not l.startswith('#'): rt[int(p[0])] = D(p[1])
html = open('live/ssp.html', errors='replace').read()
ht = {int(m.group(1)): D(m.group(2)) for m in re.finditer(r'>\s*(\d+)\s*</strong></a></td>\s*<td>(?:&nbsp;)*\s*([0-9.]+)</td>', html)}
T = D('1e-9')
over = sorted(n for n in rt if n in ht and rt[n] - ht[n] > T)
ties = sorted(n for n in rt if n in ht and T >= abs(rt[n] - ht[n]) > 0)
under = sorted(n for n in rt if n in ht and ht[n] - rt[n] > T)
print('rows radius.txt', len(rt), 'html', len(ht))
print('radius.txt > html by >1e-9:', len(over), 'min N', over[0], 'max N', over[-1])
print('ties (0<|d|<=1e-9):', len(ties), ties[:20]); print('radius.txt below html >1e-9:', under)
tf = tarfile.open('live/ssp_coords.tar.gz')
def rstar(n):
    lines = tf.extractfile('ssp%d.txt' % n).read().decode().split('\n')
    P = [tuple(D(x) for x in l.split()[1:4]) for l in lines if len(l.split()) == 4]
    assert len(P) == n, (n, len(P))
    wall = min(1 - (x*x+y*y+z*z).sqrt() for x, y, z in P)
    f = [tuple(float(c) for c in p) for p in P]
    h = 2.2 * float(wall if wall < 1 else D(1)) if n > 1 else 1
    h = 2 * float(min(rt[n], ht[n])) * 1.01
    g = {}
    for i, (x, y, z) in enumerate(f): g.setdefault((math.floor(x/h), math.floor(y/h), math.floor(z/h)), []).append(i)
    best = None
    for (a, b, c), L in g.items():
        for da in (-1,0,1):
            for db in (-1,0,1):
                for dc in (-1,0,1):
                    for j in g.get((a+da, b+db, c+dc), ()):
                        for i in L:
                            if i < j:
                                d2 = sum((f[i][k]-f[j][k])**2 for k in range(3))
                                if d2 < h*h:
                                    e = sum((P[i][k]-P[j][k])**2 for k in range(3)).sqrt()/2
                                    best = e if best is None or e < best else best
    return min(wall, best), wall, best
random.seed(20261017)
mid = [n for n in over if n not in (1055, 1601, 20000, 50000)]
sample = [1055, 1601, 20000, 50000] + sorted(random.sample(mid, 10))
ok = True
gaps = []
for n in sample:
    r, w, p = rstar(n)
    g = rt[n] - r; hd = abs(ht[n] - r); gaps.append((g, n))
    print(n, 'rtxt', rt[n], 'html', ht[n], 'r*', +r, 'binding', 'wall' if w <= p else 'pair', 'rtxt-r*', '%.3e' % g, '|html-r*|', '%.2e' % hd)
    ok &= g > T and hd <= D('2.8e-12') and n in over
gaps_all = sorted((rt[n]-ht[n], n) for n in over)
print('html-based gap min', '%.3e' % gaps_all[0][0], gaps_all[0][1], 'max', '%.3e' % gaps_all[-1][0], gaps_all[-1][1])
ok &= len(over) == 90 and over[0] == 1055 and over[-1] == 50000 and not under and gaps_all[0][1] == 1601 and gaps_all[-1][1] == 20000
print('PASS' if ok else 'FAIL')
