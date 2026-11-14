#!/usr/bin/env python3
"""Checker for srbench-2025-black-box-dominate-leader / 522_pm10.

Split reproduction: EXACTLY sklearn's train_test_split(X, y, train_size=0.75,
test_size=0.25, random_state=seed). NOTE (PREREG.v2, 2026-11-10): a plain
numpy RandomState(seed).permutation is NOT equivalent — sklearn's indices
differ. Always use sklearn here.
R2 is computed on raw test y. Complexity is SRBench's symbolic_utils.complexity.
Recorded expressions use feature NAMES (cars_per_hour, ...) — parse_expr maps
them to x_1..x_7.
"""
import gzip, re, sys
import numpy as np
import sympy as sp
from sklearn.model_selection import train_test_split as _sk_tts

sys.path.insert(0, 'data')
from symbolic_utils import complexity as srbench_complexity

N = 500
N_TRAIN = 375
FEATURES = ['cars_per_hour', 'temperature_at_2m', 'wind_speed',
            'temperature_diff_2m_25m', 'wind_direction', 'hour_of_day', 'day']
NF = len(FEATURES)


def load_data(path='data/522_pm10.tsv.gz'):
    with gzip.open(path, 'rt') as f:
        header = f.readline().strip().split('\t')
        arr = np.loadtxt(f, delimiter='\t')
    X = arr[:, :-1]
    y = arr[:, -1]
    return X, y, header[:-1]


def split(seed, X, y):
    idx = np.arange(len(y))
    tr_i, te_i = _sk_tts(idx, train_size=0.75, test_size=0.25, random_state=seed)
    return X[tr_i], y[tr_i], X[te_i], y[te_i]


def r2(y, yhat):
    y = np.asarray(y, dtype=float)
    yhat = np.asarray(yhat, dtype=float)
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - y.mean()) ** 2))
    return 1.0 - ss_res / ss_tot


def parse_expr(expr_str):
    """Translate SRBench expression notation to sympy: ^ -> **, |...| -> Abs(...).
    Variables may be named x_1..x_7, In1..In7, or the PMLB feature names."""
    s = expr_str.strip()
    s = re.sub(r'\|([^|]+)\|', r'Abs(\1)', s)
    s = s.replace('^', '**')
    # feature names -> x_i (longest first, word-boundary safe)
    for i, name in enumerate(FEATURES):
        s = re.sub(r'\b' + re.escape(name) + r'\b', f'x_{i+1}', s)
    syms = {f'x_{i}': sp.Symbol(f'x_{i}') for i in range(1, NF + 1)}
    syms.update({f'In{i}': sp.Symbol(f'x_{i}') for i in range(1, NF + 1)})
    syms.update({'sqrt': sp.sqrt, 'log': sp.log, 'exp': sp.exp, 'Exp': sp.exp,
                 'sin': sp.sin, 'cos': sp.cos, 'tanh': sp.tanh, 'Tanh': sp.tanh,
                 'Sin': sp.sin, 'Cos': sp.cos, 'Tan': sp.tan, 'Log': sp.log,
                 'Sqrt': sp.sqrt, 'Abs': sp.Abs, 'Min': sp.Min, 'Max': sp.Max, 'pi': sp.pi})
    return sp.sympify(s, locals=syms)


def eval_expr(expr, X):
    """Evaluate a parsed sympy expression on rows X (columns x_1..x_7)."""
    syms = [sp.Symbol(f'x_{i}') for i in range(1, NF + 1)]
    fn = sp.lambdify(syms, expr, modules='numpy')
    cols = [X[:, i] for i in range(NF)]
    out = fn(*cols)
    return np.asarray(out, dtype=float)


def score_expr(expr_str, seed, X, y, scale_x=False):
    """Score one recorded expression on one seed's split. scale_x standardizes X
    (fit on train) before evaluating, matching scale_x runs."""
    Xtr, ytr, Xte, yte = split(seed, X, y)
    if scale_x:
        mu, sd = Xtr.mean(0), Xtr.std(0)
        sd[sd == 0] = 1.0
        Xte = (Xte - mu) / sd
    expr = parse_expr(expr_str)
    yhat = eval_expr(expr, Xte)
    return r2(yte, yhat), int(srbench_complexity(expr))


def score_expr_y_scaled(expr_str, seed, X, y, scale_x=False):
    """Same, but the expression outputs standardized y (scale_y runs): compare
    against standardized test y. R2 is affine-invariant, so this equals the
    recorded r2_test when the convention matches."""
    Xtr, ytr, Xte, yte = split(seed, X, y)
    if scale_x:
        mu, sd = Xtr.mean(0), Xtr.std(0)
        sd[sd == 0] = 1.0
        Xte = (Xte - mu) / sd
    ym, ys = ytr.mean(), ytr.std()
    yte_s = (yte - ym) / ys
    expr = parse_expr(expr_str)
    yhat = eval_expr(expr, Xte)
    return r2(yte_s, yhat), int(srbench_complexity(expr))


def constant_mean_r2(seed, X, y):
    Xtr, ytr, Xte, yte = split(seed, X, y)
    return r2(yte, np.full_like(yte, ytr.mean()))


if __name__ == '__main__':
    X, y, names = load_data()
    print('data', X.shape, 'features', names)
    print('constant-mean R2 on seed 769:', round(constant_mean_r2(769, X, y), 6))
