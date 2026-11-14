"""Independent cross-check of the pricing050 Lagrangian bound with mpmath.iv (directed-rounding intervals).
Different code path from cert_arb.py: breadth-first bisection with a global per-variable bound, Taylor-free
monotonicity test: on a cell where phi' enclosure excludes 0, min is at an endpoint (evaluated as point interval)."""
import json, sys
from mpmath import iv, mpf
iv.dps = 40
M = json.load(open(sys.argv[1])); lam = {l.split()[0]: l.split()[1] for l in open(sys.argv[2]) if l.strip()}
T = {v: [] for v in M['vars']}
for r in M['rows']:
    for t in r['terms']:
        T[t['var']].append((iv.mpf(lam[r['name']]) * iv.mpf(t['a']), iv.mpf(t['b']), t['p']))
C = {v: -iv.mpf(s) for v, s in M['cost_in_e1'].items()}
def phi(v, X):
    s = C.get(v, iv.mpf(0)) * X
    for la, b, p in T[v]: s = s - la * X * iv.exp(-(b * X ** p))
    return s
def dphi(v, X):
    s = C.get(v, iv.mpf(0))
    for la, b, p in T[v]: s = s - la * iv.exp(-(b * X ** p)) * (1 - b * p * X ** p)
    return s
def cell_lower(v, lo, hi):
    X = iv.mpf([lo, hi]); D = dphi(v, X)
    if D.a > 0: return phi(v, iv.mpf(lo)).a          # increasing: min at lo
    if D.b < 0: return phi(v, iv.mpf(hi)).a          # decreasing: min at hi
    m = (lo + hi) / 2
    return max(phi(v, X).a, (phi(v, iv.mpf(m)) + D * (X - m)).a)
total = iv.mpf(0)
for r in M['rows']: total = total + iv.mpf(lam[r['name']]) * (-iv.mpf(r['rhs']))
lows = []
for v in M['vars']:
    cells = [(mpf(0), mpf(10))]; done = []
    up = min(phi(v, iv.mpf(mpf(k) / 50)).b for k in range(501))
    for depth in range(40):
        nxt = []
        for lo, hi in cells:
            lb = cell_lower(v, lo, hi)
            if lb >= up - mpf('1e-8') or depth == 39: done.append(lb)
            else:
                m = (lo + hi) / 2; nxt += [(lo, m), (m, hi)]
                up = min(up, phi(v, iv.mpf(m)).b)
        cells = nxt
        if not cells: break
    assert not cells
    mv = min(done); lows.append(mv); total = total + iv.mpf(mv)
LB = total.a
print('mpmath.iv LB on min c.x:', LB)
print('U = -LB:', -LB)
bar = mpf('-1813.829078') + mpf('1e-6') * mpf('1813.829078')
print('bar:', bar, ' S1 cross-check', 'PASS' if -LB <= bar else 'FAIL')
