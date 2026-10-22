"""Independent exact check of a one-point extension optimum with an integer program (scipy.optimize.milp = HiGHS).
Max-coverage formulation (operations research import): sub-domain F = full domain of the M-assignment in.npy;
items = (order of F, slot of the new alternative x = M); binary y[p,o] (one option o per pair p = {a,b}, triple
{a,b,x}); z[i] in [0,1] with z[i] <= sum_{o allowed for item i on pair p} y[p,o] for every pair p; maximise sum z.
Usage: python milp_ext.py M in.npy OPTS TIMELIMIT"""
import sys, itertools, time
from math import comb
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from scipy.sparse import coo_matrix
M = int(sys.argv[1]); cond = np.load(sys.argv[2]); opts = [0, 2, 3, 5, 6, 8] if sys.argv[3] == 'pp6' else list(range(9)); tl = float(sys.argv[4])
def tidx(a, b, c): return comb(c, 3) + comb(b, 2) + a
def ok(order):
    pos = {v: i for i, v in enumerate(order)}
    for a, b, c in itertools.combinations(range(M), 3):
        code = int(cond[tidx(a, b, c)]); s, p = divmod(code, 3); m = (a, b, c)[s]
        if sum(pos[o] < pos[m] for o in (a, b, c) if o != m) == p: return False
    return True
# enumerate F by DFS with prefix checks
F = []
def dfs(pre, rest):
    if not rest: F.append(tuple(pre)); return
    for e in sorted(rest):
        good = True
        for u, v in itertools.combinations(pre, 2):
            a, b, c = sorted((u, v, e)); code = int(cond[tidx(a, b, c)]); s, p = divmod(code, 3); m = (a, b, c)[s]
            rk = {u: 0, v: 1, e: 2}[m]
            if rk == p: good = False; break
        if good: dfs(pre + [e], rest - {e})
dfs([], set(range(M)))
x = M; pairs = list(itertools.combinations(range(M), 2)); NP, NO = len(pairs), len(opts)
items = [(f, k) for f in F for k in range(M + 1)]; NI = len(items)
print('M', M, 'subdomain', len(F), 'items', NI, 'pairs', NP, 'opts', NO, flush=True)
nv = NP * NO + NI
rows, cols, vals = [], [], []; r = 0
for i, (f, k) in enumerate(items):
    order = list(f[:k]) + [x] + list(f[k:]); pos = {v: q for q, v in enumerate(order)}
    for p, (a, b) in enumerate(pairs):
        tri = sorted((a, b, x))
        rows.append(r); cols.append(NP * NO + i); vals.append(1.0)
        for oi, code in enumerate(opts):
            s, q = divmod(code, 3); m = tri[s]
            if sum(pos[o] < pos[m] for o in tri if o != m) != q: rows.append(r); cols.append(p * NO + oi); vals.append(-1.0)
        r += 1
for p in range(NP):  # one option per pair
    for oi in range(NO): rows.append(r); cols.append(p * NO + oi); vals.append(1.0)
    r += 1
A = coo_matrix((vals, (rows, cols)), shape=(r, nv)).tocsr()
lb = np.r_[np.full(NI * NP, -np.inf), np.ones(NP)]; ub = np.r_[np.zeros(NI * NP), np.ones(NP)]
c = np.r_[np.zeros(NP * NO), -np.ones(NI)]
integ = np.r_[np.ones(NP * NO), np.zeros(NI)]
t0 = time.time()
res = milp(c, constraints=LinearConstraint(A, lb, ub), integrality=integ, bounds=Bounds(0, 1), options={'time_limit': tl, 'disp': False, 'mip_rel_gap': 0})
print('status', res.status, res.message, 'time %.1fs' % (time.time() - t0))
if res.x is not None:
    print('objective', -res.fun, 'dual bound', getattr(res, 'mip_dual_bound', None), 'gap', getattr(res, 'mip_gap', None))
