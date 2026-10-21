"""Minimal exact certificates: Delsarte D_k plus per-distance rows R_x: a_x <= C(w,x) A(n-w,d,x) (inputs from the live table).
usage: make_certs.py n d w [n d w ...]  -> result/cert_A<n>_<d>_<w>.json"""
import sys, json
cells = [tuple(map(int, sys.argv[i:i + 3])) for i in range(1, len(sys.argv), 3)]
sys.argv = ['x', '../../tools', '../../data/Andw.html']
exec(open('code/lpsweep.py').read().split("if __name__")[0])
from cells2 import parse2
for k, v in parse2('../../data/Andw.html').items():
    if k not in CELLS: CELLS[k] = v
    else:
        a, b = CELLS[k], v; his = [h for h in (a[1], b[1]) if h is not None]
        CELLS[k] = (max(a[0], b[0]), min(his) if his else None, a[2] + ' | ' + b[2])
U.cache_clear()
import numpy as np
from scipy.optimize import linprog
for c in cells:
    n, d, w = c; delta = d // 2; X = list(range(delta, w + 1))
    rows = []; rhs = []; tags = []; inputs = {}
    for k in range(1, w + 1):
        rows.append([-Q(n, w, k, x) for x in X]); rhs.append(Q(n, w, k, 0)); tags.append(f'D{k}')
    for i, x in enumerate(X):
        u = U(n - w, d, x); inputs[f'A({n-w},{d},{x})'] = (u, CELLS.get((n - w, d, min(x, n - w - x)), (0, 0, 'elementary'))[2])
        r = [F(0)] * len(X); r[i] = F(1); rows.append(r); rhs.append(F(comb(w, x) * u)); tags.append(f'R{x}')
    sc = [max(max(abs(v) for v in r), abs(b), F(1)) for r, b in zip(rows, rhs)]
    A = np.array([[float(v / s) for v in r] for r, s in zip(rows, sc)]); b = np.array([float(bb / s) for bb, s in zip(rhs, sc)])
    res = linprog(-np.ones(len(X)), A_ub=A, b_ub=b, bounds=[(0, None)] * len(X), method='highs')
    y = [max(F(v).limit_denominator(10**6), F(0)) / s for v, s in zip(-res.ineqlin.marginals, sc)]
    col = [sum(y[r] * rows[r][i] for r in range(len(rows))) for i in range(len(X))]; mn = min(col)
    if mn < 1: y = [v / mn for v in y]
    col = [sum(y[r] * rows[r][i] for r in range(len(rows))) for i in range(len(X))]
    assert all(t >= 1 for t in col) and all(v >= 0 for v in y)
    val = 1 + sum(y[r] * rhs[r] for r in range(len(rows)))
    act = [i for i in range(len(rows)) if y[i] != 0]
    used = {f'A({n-w},{d},{int(tags[i][1:])})': inputs[f'A({n-w},{d},{int(tags[i][1:])})'][0] for i in act if tags[i][0] == 'R'}
    raw = {k: inputs[k][1] for k in used}
    cert = {'cell': {'n': n, 'd': d, 'w': w}, 'variables': f'a_x for Johnson distance x = {X[0]}..{X[-1]} (Hamming distance 2x); a_0 = 1',
            'constraints': [{'tag': tags[i], 'coeffs': {str(x): str(rows[i][k]) for k, x in enumerate(X)}, 'rhs': str(rhs[i]), 'dual': str(y[i])} for i in act],
            'table_inputs': used, 'table_inputs_as_printed': raw, 'claimed_bound': floor(val), 'certified_value': str(val)}
    json.dump(cert, open(f'result/cert_A{n}_{d}_{w}.json', 'w'), indent=1)
    print(c, 'float', round(1 - res.fun, 4), 'cert', val, round(float(val), 4), 'bound', floor(val), 'table', CELLS[c][2], 'inputs', used, raw, [tags[i] for i in act])
