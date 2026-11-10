#!/usr/bin/env python3
"""Lens 1 (constructor): dictionary sparse regression on 1028_SWD, all 30 splits.
Fixed procedure per PREREG.md. Writes output/results.json + output/expressions.txt."""
import sys, json
sys.path.insert(0, 'code')
import numpy as np
import sympy as sp
from check_srbench import load_data, split, r2, parse_expr
sys.path.insert(0, 'data')
from symbolic_utils import complexity as srbench_complexity

TRANSFORMS = [
    ('x', lambda x: x),
    ('x2', lambda x: x ** 2),
    ('x3', lambda x: x ** 3),
    ('inv', lambda x: 1.0 / x),
    ('sqrt', lambda x: np.sqrt(x)),
    ('log', lambda x: np.log(x)),
    ('xm2', lambda x: x - 2.0),
    ('xm2sq', lambda x: (x - 2.0) ** 2),
    ('hinge_hi', lambda x: np.maximum(0.0, x - 2.0)),
    ('hinge_lo', lambda x: np.maximum(0.0, 2.0 - x)),
]
EXPR = {
    'x': 'x_{i}', 'x2': 'x_{i}**2', 'x3': 'x_{i}**3', 'inv': '1/x_{i}',
    'sqrt': 'sqrt(x_{i})', 'log': 'log(x_{i})', 'xm2': '(x_{i}-2)',
    'xm2sq': '(x_{i}-2)**2', 'hinge_hi': 'Max(0,x_{i}-2)', 'hinge_lo': 'Max(0,2-x_{i})',
}
MAX_TERMS = 12
MIN_GAIN = 0.001


def build_library(X):
    """Return (names, matrix) of the 146-term dictionary for rows X."""
    n, p = X.shape
    names, cols = [], []
    for j in range(p):
        for tname, tf in TRANSFORMS:
            names.append((tname, j))
            cols.append(tf(X[:, j].astype(float)))
    for i in range(p):
        for j in range(i + 1, p):
            names.append(('prod', (i, j)))
            cols.append(X[:, i].astype(float) * X[:, j].astype(float))
    M = np.column_stack([np.ones(n)] + cols)
    names = [('const', None)] + names
    return names, M


def term_expr(name, coef):
    if name[0] == 'const':
        return sp.Float(round(coef, 4))
    if name[0] == 'prod':
        i, j = name[1]
        return sp.Float(round(coef, 4)) * sp.Symbol(f'x_{i+1}') * sp.Symbol(f'x_{j+1}')
    tname, j = name
    s = EXPR[tname].replace('x_{i}', f'x_{j+1}')
    return sp.Float(round(coef, 4)) * sp.sympify(s)


def run_split(seed, X, y):
    Xtr, ytr, Xte, yte = split(seed, X, y)
    names, Mtr = build_library(Xtr)
    _, Mte = build_library(Xte)
    # inner validation split of train (seed 0)
    rng = np.random.RandomState(0)
    perm = rng.permutation(len(ytr))
    n_val = len(ytr) // 5
    vi, ti = perm[:n_val], perm[n_val:]
    sel = [0]
    best_val = r2(ytr[vi], np.full(n_val, ytr[ti].mean()))
    while len(sel) < MAX_TERMS + 1:
        best_gain, best_k = 0.0, None
        for k in range(1, Mtr.shape[1]):
            if k in sel:
                continue
            cols = sel + [k]
            coef, *_ = np.linalg.lstsq(Mtr[ti][:, cols], ytr[ti], rcond=None)
            pred = Mtr[vi][:, cols] @ coef
            val = r2(ytr[vi], pred)
            gain = val - best_val
            if gain > best_gain:
                best_gain, best_k = gain, k
        if best_k is None or best_gain < MIN_GAIN:
            break
        sel.append(best_k)
        coef, *_ = np.linalg.lstsq(Mtr[ti][:, sel], ytr[ti], rcond=None)
        best_val = r2(ytr[vi], Mtr[vi][:, sel] @ coef)
    coef, *_ = np.linalg.lstsq(Mtr[:, sel], ytr, rcond=None)
    yhat = Mte[:, sel] @ coef
    test_r2 = r2(yte, yhat)
    expr = sum((term_expr(names[k], c) for k, c in zip(sel, coef)), sp.Integer(0))
    cx = int(srbench_complexity(expr))
    return test_r2, cx, len(sel) - 1, str(expr)


def main():
    X, y, _ = load_data()
    import pyarrow.feather as f
    df = f.read_feather('data/results.feather')
    seeds = sorted(df[df['dataset'] == '1028_SWD']['random_state'].unique().tolist())
    print('seeds:', len(seeds))
    out = []
    for s in seeds:
        tr2, cx, nterms, expr = run_split(s, X, y)
        out.append({'seed': s, 'test_r2': tr2, 'complexity': cx, 'n_terms': nterms, 'expr': expr})
        print(f"seed {s}: R2={tr2:.4f} cx={cx} terms={nterms}")
    med_r2 = float(np.median([o['test_r2'] for o in out]))
    med_cx = float(np.median([o['complexity'] for o in out]))
    print(f"MEDIAN R2={med_r2:.4f} (bar 0.3800) MEDIAN CX={med_cx:.0f} (bar 3270; p2 bar R2>0.2430 cx<=20)")
    with open('attempts/constructor/output/results.json', 'w') as fh:
        json.dump({'median_r2': med_r2, 'median_complexity': med_cx, 'per_split': out}, fh, indent=1)
    with open('attempts/constructor/output/expressions.txt', 'w') as fh:
        for o in out:
            fh.write(f"seed {o['seed']} R2={o['test_r2']:.4f} cx={o['complexity']}: {o['expr']}\n")


if __name__ == '__main__':
    main()
