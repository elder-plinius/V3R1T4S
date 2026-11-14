"""Rigorous Lagrangian dual bound for pricing050 with python-flint arb ball arithmetic.
LB = sum_k lam_k d_k + sum_i m_i, m_i <= min_{x in [0,10]} phi_i(x), phi_i(x) = c_i x - sum_k lam_k a_ki x exp(-b_ki x^p_ki).
Weak duality: for any feasible x (sum_i a_ki g_ki(x_i) >= d_k, lam >= 0): c.x >= c.x - sum_k lam_k (sum_i a_ki g_ki(x_i) - d_k) >= LB.
So max objvar = -min c.x <= -LB. Interval branch and bound per variable; every leaf's enclosure lower bound is kept;
leaves cover [0,10] exactly (checked). Output: leaves log (JSON) and the bound printed as an arb ball."""
import json, sys
from flint import arb, ctx
ctx.prec = 200
M = json.load(open(sys.argv[1])); lamf = sys.argv[2]; logf = sys.argv[3]
lam = {l.split()[0]: l.split()[1] for l in open(lamf) if l.strip()}
for v in lam.values(): assert arb(v) >= 0
def interval(lo, hi):            # exact rationals lo,hi given as arb points -> ball covering [lo,hi]
    return arb((lo + hi) / 2, (hi - lo) / 2)  # flint rounds outward for rad
terms = {v: [] for v in M['vars']}
for r in M['rows']:
    L = arb(lam[r['name']])
    for t in r['terms']:
        terms[t['var']].append((L * arb(t['a']), arb(t['b']), t['p']))
cost = {v: (-arb(s)) for v, s in M['cost_in_e1'].items()}
def phi(v, X):
    c = cost.get(v, arb(0))
    s = c * X
    for la, b, p in terms[v]:
        s -= la * X * (-(b * X ** p)).exp()
    return s
def dphi(v, X):
    c = cost.get(v, arb(0))
    s = c
    for la, b, p in terms[v]:
        s -= la * (-(b * X ** p)).exp() * (1 - b * p * X ** p)
    return s
def enclose_lower(v, lo, hi):
    X = interval(lo, hi); m = (lo + hi) / 2
    nat = phi(v, X)
    mv = phi(v, arb(m)) + dphi(v, X) * (X - m)
    return max(nat.lower(), mv.lower())   # both are valid enclosures; take the tighter lower end
def solve_var(v, tol=arb('1e-7'), maxleaves=200000):
    from fractions import Fraction
    # upper bound on min from point evaluations
    best_up = min((phi(v, arb(k) / 100).upper() for k in range(0, 1001)))
    stack = [(arb(0), arb(10))]; leaves = []; pruned = 0
    while stack:
        lo, hi = stack.pop()
        lb = enclose_lower(v, lo, hi)
        mid = (lo + hi) / 2
        up = phi(v, mid).upper()
        if up < best_up: best_up = up
        if lb > best_up - tol or (hi - lo) < arb('1e-9'):
            leaves.append((lo, hi, lb)); continue
        stack.append((mid, hi)); stack.append((lo, mid))
        if len(leaves) > maxleaves: raise RuntimeError('too many leaves')
    leaves.sort(key=lambda z: float(z[0].mid()))
    # coverage check: consecutive, exact endpoints (dyadic midpoints, exact in arb)
    assert leaves[0][0] == 0 and leaves[-1][1] == 10
    for a, b in zip(leaves, leaves[1:]): assert a[1] == b[0]
    m = min(z[2] for z in leaves)
    return m, best_up, leaves
total = arb(0)
for r in M['rows']: total += arb(lam[r['name']]) * (-arb(r['rhs']))
log = {}; nleaves = 0
for v in M['vars']:
    m, up, leaves = solve_var(v)
    total += m
    nleaves += len(leaves)
    log[v] = {'lower': m.str(30, radius=False), 'upper_from_points': up.str(30, radius=False), 'leaves': len(leaves),
              'leaf_list': [[a.str(25, radius=False), b.str(25, radius=False), l.str(25, radius=False)] for a, b, l in leaves]}
LB = total.lower()
U = -LB
bar = arb('-1813.829078') + arb('1e-6') * arb('1813.829078')
json.dump({'lambda': lam, 'LB_lower': LB.str(30, radius=False), 'nleaves': nleaves, 'vars': log}, open(logf, 'w'), indent=0)
print('leaves', nleaves)
print('LB (rigorous lower bound on min c.x):', LB.str(25, radius=False))
print('U = -LB (rigorous upper bound on max objvar):', U.str(25, radius=False))
print('bar (best primal + 1e-6*|best|):', bar.str(25))
print('S1 PASS' if U <= bar else 'S1 FAIL', '; margin bar-U =', (bar - U).str(10))
