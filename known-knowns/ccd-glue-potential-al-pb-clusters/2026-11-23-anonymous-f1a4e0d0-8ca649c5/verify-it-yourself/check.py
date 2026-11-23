"""Standalone check of one Pb glue cluster (Lim-Ong-Ercolessi glue potential, piecewise polynomials parsed from lead.f).
E = sum_{i<j} phi(r_ij) + sum_i U(sum_{j!=i} rho(r_ij)), eV and Angstrom. Checks, from the bank criterion:
 calibration (ten random posted files plus N = 121 against the table cells, 1e-6 eV), the object's energy at least 1e-4 eV
 below the table cell, a 30-digit (mpmath) Newton polish to gradient norm < 1e-10, a double-precision Hessian with exactly
 6 |lambda| < 1e-6 and no negative eigenvalue, and the polished posted structure at least 1e-4 eV higher.
Needs numpy, scipy, mpmath. Usage: check.py CACHE_DIR PACKAGE_DIR"""
import sys, os, re, csv, math, random
import numpy as np, mpmath as mp
from scipy.optimize import minimize
cache, pkg = sys.argv[1], sys.argv[2]; mp.mp.dps = 30
def fnum(s): return s.replace('D', 'E').replace('d', 'E')
blk = open(os.path.join(cache, 'lead.f')).read().split('SUBROUTINE')[0]
lines = [l for l in blk.splitlines() if l.strip() and not l.lstrip().startswith('*')]
text = ' '.join(l[6:] if len(l) > 5 and l[5] not in ' 0' else l for l in lines)
S = {}
for names, vals in re.findall(r'DATA\s+([A-Z0-9_,\s]+?)\s*/([^/]*)/', text):
    ns = [n.strip() for n in names.split(',')]; vs = [fnum(v.strip()) for v in vals.replace('$', ' ').split(',')]
    assert len(ns) == len(vs), (ns, vs); S.update(zip(ns, vs))
def consts(conv): return {k: conv(v) for k, v in S.items()}
def poly(cs, x):  # value and derivative
    v = 0; d = 0
    for c in reversed(cs): d = d * x + v; v = v * x + c
    return v, d
def make(g, zero):
    def rho(r):
        if r >= g['RRC']: return zero, zero
        if r >= g['RRB']: return poly([zero, zero, g['R2III'], g['R3III']], r - g['RRC'])
        if r >= g['RRD']: return poly([g['RHOD'], g['R1II'], g['R2II'], g['R3II']], r - g['RRD'])
        return poly([g['RHOD'], g['R1I'], g['R2I'], g['R3I']], r - g['RRD'])
    def U(n):
        if n > g['DB']: return poly([g['UB'], zero, g['B2III'], g['B3III']], n - g['DB'])
        if n > g['DSW']: return poly([g['UB'], zero, g['B2II'], g['B3II'], g['B4II']], n - g['DB'])
        return poly([g['B0I'], g['B1I'], g['B2I'], g['B3I'], g['B4I']], n - g['DSW'])
    def phi(r):
        if r >= g['RC']: return zero, zero
        if r >= g['A']: return poly([zero, zero, zero, g['A3III'], g['A4III'], g['A5III']], r - g['RC'])
        if r >= g['D']: return poly([g['A0II'], g['A1II'], g['A2II'], g['A3II'], g['A4II'], g['A5II'], g['A6II']], r - g['D'])
        return poly([g['A0I'], g['A1I'], g['A2I'], g['A3I'], g['A4I']], r - g['D'])
    rc = max(g['RC'], g['RRC'])
    def eg(X, sqrt):
        n = len(X); pairs = []; dens = [zero] * n; E = zero
        for i in range(n):
            for j in range(i + 1, n):
                d = [X[i][k] - X[j][k] for k in range(3)]; r = sqrt(d[0]*d[0] + d[1]*d[1] + d[2]*d[2])
                if r >= rc: continue
                p, dp = phi(r); q, dq = rho(r); E += p; dens[i] += q; dens[j] += q; pairs.append((i, j, d, r, dp, dq))
        Ud = [U(z) for z in dens]; E += sum(u for u, _ in Ud); G = [[zero] * 3 for _ in range(n)]
        for i, j, d, r, dp, dq in pairs:
            f = (dp + (Ud[i][1] + Ud[j][1]) * dq) / r
            for k in range(3): G[i][k] += f * d[k]; G[j][k] -= f * d[k]
        return E, G
    return eg
egf = make(consts(float), 0.0); egm = make(consts(mp.mpf), mp.mpf(0))
def E64(X): return egf(X, math.sqrt)[0]
def fg(x): E, G = egf(x.reshape(-1, 3).tolist(), math.sqrt); return E, np.array(G).ravel()
def load(p): return [[float(v) for v in l.split()] for l in open(p) if l.strip()]
tab = {int(r['N']): float(r['E_table_eV']) for r in csv.DictReader(open(os.path.join(pkg, 'the-record-we-beat', 'table_values.csv')))}
bad = []
# 1. calibration
random.seed(2026); sample = sorted(random.sample([n for n in tab if n not in (116, 121)], 10)) + [121]
for n in sample:
    d = E64(load(os.path.join(cache, 'Pb_points', str(n)))) - tab[n]
    print(f'calibration N={n}: E_posted - E_table = {d:.2e}')
    if abs(d) > 1e-6: bad.append(f'calibration {n}')
# 2. object energy and 30-digit polish
X = load(os.path.join(pkg, 'object', 'Pb_121.txt')); N = len(X)
CLAIMED = -198.47902916627225  # the claimed energy of these exact coordinates (eV)
import hashlib
want = next(csv.DictReader(open(os.path.join(pkg, 'INDEX.csv'))))['sha256']
got = hashlib.sha256(open(os.path.join(pkg, 'object', 'Pb_121.txt'), 'rb').read()).hexdigest()
print('object sha256 matches INDEX.csv' if got == want else 'object sha256 MISMATCH: ' + got)
if got != want: bad.append('object sha256')
E0, G0 = egf(X, math.sqrt); g0 = math.sqrt(sum(c * c for row in G0 for c in row))
print(f'object as given: E = {E0:.11f} eV (claimed {CLAIMED}), float64 |grad| = {g0:.2e}')
if abs(E0 - CLAIMED) > 1e-9 or g0 > 1e-6: bad.append('object file does not match the claimed minimum')
if N != 121: bad.append('object has %d atoms' % N)
x = np.array(X).ravel()
def hessian(x, h=1e-5):
    H = np.zeros((len(x), len(x)))
    for k in range(len(x)):
        e = np.zeros(len(x)); e[k] = h; H[:, k] = (fg(x + e)[1] - fg(x - e)[1]) / (2 * h)
    return (H + H.T) / 2
H = hessian(x); w, V = np.linalg.eigh(H)
Xm = [[mp.mpf(repr(v)) for v in row] for row in X]
for it in range(4):
    Em, Gm = egm(Xm, mp.sqrt); gn = mp.sqrt(sum(c * c for row in Gm for c in row))
    print(f'mpmath iteration {it}: E = {mp.nstr(Em, 25)}  |grad| = {mp.nstr(gn, 5)}')
    if gn < mp.mpf('1e-20'): break
    g = np.array([float(c) for row in Gm for c in row]); keep = np.abs(w) > 1e-6
    step = V[:, keep] @ ((V[:, keep].T @ g) / w[keep])
    Xm = [[Xm[i][k] - mp.mpf(float(step[3 * i + k])) for k in range(3)] for i in range(N)]
if not gn < mp.mpf('1e-10'): bad.append('gradient norm %s' % mp.nstr(gn, 5))
Eobj = float(Em); xp = np.array([[float(v) for v in row] for row in Xm]).ravel()
w = np.linalg.eigvalsh(hessian(xp)); nz = int((np.abs(w) < 1e-6).sum()); neg = int((w < -1e-6).sum())
print(f'object: E = {Eobj:.10f} eV; table N=121 {tab[121]}; margin {Eobj - tab[121]:.6f} eV')
print(f'Hessian: near-zero modes {nz}, negative {neg}, lowest nonzero {w[np.abs(w) >= 1e-6].min():.4f}')
if not Eobj <= tab[121] - 1e-4: bad.append('margin vs table')
if nz != 6 or neg: bad.append('Hessian')
# 3. distinct basin: polish the posted 121 structure
r = minimize(fg, np.array(load(os.path.join(cache, 'Pb_points', '121'))).ravel(), jac=True, method='L-BFGS-B', options={'gtol': 1e-9, 'ftol': 1e-15, 'maxiter': 5000})
print(f'posted N=121 polished: {r.fun:.10f} eV; object lower by {r.fun - Eobj:.6f} eV')
if not r.fun - Eobj >= 1e-4: bad.append('distinct basin')
print('problems:', bad); print('PASS' if not bad else 'FAIL'); sys.exit(0 if not bad else 1)
