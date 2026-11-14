#!/usr/bin/env python3
"""Lens 2 (smuggler, GAM shape compression) on 522_pm10, all 30 splits.
Fixed procedure per PREREG.md (2026-11-13): backfitting on train only, 8
rounds, binned-mean smoother (20 quantile bins, 3 passes of [1,2,1]/4
smoothing, linear interpolation). Compression: 60-point quantile grid per
feature, greedy stepwise up to 3 terms from the per-feature library (linear,
square, Abs, sqrt|.|, log(1+|.|), hinges at train quartiles, sin/cos for the
two cyclic features only), stop at grid-MSE gain < 0.001. Joint OLS refit of
all coefficients on full train; full-precision coefficients. Writes
output/results.json + output/expressions.txt. Scoring of the final
expressions goes through the checker (score_expr, raw).
"""
import sys, json, time
sys.path.insert(0, 'code')
import numpy as np
import pyarrow.feather as f
from check_srbench import load_data, split, r2, parse_expr, score_expr, FEATURES
sys.path.insert(0, 'data')
from symbolic_utils import complexity as srbench_complexity

N_BINS = 20
N_ROUNDS = 8
N_GRID = 60
MAX_TERMS_PER_SHAPE = 3
CYCLIC = {'hour_of_day': 24.0, 'day': 365.25}


def smooth(v):
    v = np.asarray(v, dtype=float)
    for _ in range(3):
        vp = np.pad(v, (1, 1), mode='edge')
        v = 0.25 * vp[:-2] + 0.5 * vp[1:-1] + 0.25 * vp[2:]
    return v


def fit_shape(x, resid):
    """Binned-mean smoother of resid vs x. Returns (centers, values)."""
    qs = np.linspace(0, 100, N_BINS + 1)
    edges = np.unique(np.quantile(x, qs / 100.0))
    if len(edges) < 3:
        return np.array([x.min(), x.max()]), np.array([resid.mean(), resid.mean()])
    centers = 0.5 * (edges[:-1] + edges[1:])
    idx = np.clip(np.searchsorted(edges, x, side='right') - 1, 0, len(centers) - 1)
    vals = np.zeros(len(centers))
    for b in range(len(centers)):
        m = idx == b
        vals[b] = resid[m].mean() if m.any() else np.nan
    ok = np.isfinite(vals)
    if not ok.any():
        vals[:] = 0.0
    elif not ok.all():
        vals = np.interp(centers, centers[ok], vals[ok])
    vals = smooth(vals)
    return centers, vals


def shape_predict(centers, vals, x):
    return np.interp(x, centers, vals)


def backfit(Xtr, ytr):
    """8 rounds of backfitting. Returns the fitted shapes (centers, values)
    per feature, refit once on the final partial residuals so centers/vals
    match the returned shapes exactly."""
    n, p = Xtr.shape
    f = [np.zeros(n) for _ in range(p)]
    total = np.zeros(n)
    for _ in range(N_ROUNDS):
        for j in range(p):
            resid = ytr - (total - f[j])
            centers, vals = fit_shape(Xtr[:, j], resid)
            fj = shape_predict(centers, vals, Xtr[:, j])
            fj = fj - fj.mean()
            total = total - f[j] + fj
            f[j] = fj
    shapes = []
    for j in range(p):
        resid = ytr - (total - f[j])
        shapes.append(fit_shape(Xtr[:, j], resid))
    return shapes


def lib_terms(x, name, q25, q75):
    """Per-feature compression library: (string, values-on-x). Quartiles are
    passed in (computed once from train) so grid/train/test strings match."""
    terms = [
        (f'({name})', x.copy()),
        (f'({name})**2', x ** 2),
        (f'Abs({name})', np.abs(x)),
        (f'sqrt(Abs({name}))', np.sqrt(np.abs(x))),
        (f'log(1+Abs({name}))', np.log1p(np.abs(x))),
        (f'Max(0, {name} - {q25!r})', np.maximum(0.0, x - q25)),
        (f'Max(0, {name} - {q75!r})', np.maximum(0.0, x - q75)),
        (f'Max(0, {q25!r} - {name})', np.maximum(0.0, q25 - x)),
        (f'Max(0, {q75!r} - {name})', np.maximum(0.0, q75 - x)),
    ]
    if name in CYCLIC:
        P = CYCLIC[name]
        terms.append((f'sin(2*pi*{name}/{P!r})', np.sin(2 * np.pi * x / P)))
        terms.append((f'cos(2*pi*{name}/{P!r})', np.cos(2 * np.pi * x / P)))
    return terms


def compress_shape(grid_x, grid_y, name, q25, q75):
    """Greedy stepwise fit of grid_y on the per-feature library (<=3 terms).
    Returns (selected term strings, final grid MSE, base grid MSE)."""
    terms = lib_terms(grid_x, name, q25, q75)
    sel, sel_vals = [], []
    base_mse = float(np.mean((grid_y - grid_y.mean()) ** 2))
    cur_mse = base_mse
    for _ in range(MAX_TERMS_PER_SHAPE):
        best_k, best_mse = None, cur_mse
        for k, (ts, tv) in enumerate(terms):
            if k in sel:
                continue
            M = np.column_stack(sel_vals + [tv]) if sel_vals else tv[:, None]
            A = np.column_stack([np.ones_like(grid_y), M])
            coef, *_ = np.linalg.lstsq(A, grid_y, rcond=None)
            mse = float(np.mean((grid_y - A @ coef) ** 2))
            if mse < best_mse:
                best_k, best_mse = k, mse
        if best_k is None or (cur_mse - best_mse) < 0.001 * base_mse:
            break
        sel.append(best_k)
        sel_vals.append(terms[best_k][1])
        cur_mse = best_mse
    return [terms[k][0] for k in sel], cur_mse, base_mse


def run_split(seed, X, y):
    Xtr, ytr, Xte, yte = split(seed, X, y)
    shapes = backfit(Xtr, ytr)
    all_terms = []  # (string, train-values, test-values)
    comp_info = []
    for j, name in enumerate(FEATURES):
        centers, vals = shapes[j]
        q25, q75 = np.quantile(Xtr[:, j], [0.25, 0.75])
        grid_x = np.unique(np.quantile(Xtr[:, j], np.linspace(0, 1, N_GRID)))
        grid_y = shape_predict(centers, vals, grid_x)
        sel, mse, base = compress_shape(grid_x, grid_y, name, float(q25), float(q75))
        comp_info.append((name, len(sel), mse, base))
        lib_tr = dict(lib_terms(Xtr[:, j], name, float(q25), float(q75)))
        lib_te = dict(lib_terms(Xte[:, j], name, float(q25), float(q75)))
        for ts in sel:
            all_terms.append((ts, lib_tr[ts], lib_te[ts]))
    if not all_terms:
        expr_str = f'{float(ytr.mean())!r}'
        test_r2, cx = score_expr(expr_str, seed, X, y, scale_x=False)
        return test_r2, cx, 0, expr_str, comp_info
    Mtr = np.column_stack([np.ones(len(ytr))] + [v for _, v, _ in all_terms])
    Mte = np.column_stack([np.ones(len(yte))] + [v for _, _, v in all_terms])
    coef, *_ = np.linalg.lstsq(Mtr, ytr, rcond=None)
    coef = [float(v) for v in coef]  # plain floats: numpy repr (np.float64(...)) breaks sympy parsing
    expr = ' + '.join(f'{c!r}*({s})' for c, (s, _, _) in zip(coef[1:], all_terms))
    expr_str = f'{coef[0]!r} + {expr}' if expr else f'{coef[0]!r}'
    test_r2, cx = score_expr(expr_str, seed, X, y, scale_x=False)
    yhat = Mte @ coef
    dm_r2 = r2(yte, yhat)
    if abs(dm_r2 - test_r2) > 1e-9:
        print(f'  WARNING seed {seed}: design R2 {dm_r2:.6f} != checker R2 {test_r2:.6f}')
    return test_r2, cx, len(all_terms), expr_str, comp_info


def main():
    t0 = time.time()
    X, y, _ = load_data()
    df = f.read_feather('data/results.feather')
    seeds = sorted(df[df['dataset'] == '522_pm10']['random_state'].unique().tolist())
    print('seeds:', len(seeds), flush=True)
    out = []
    for s in seeds:
        tr2, cx, nterms, expr, comp = run_split(s, X, y)
        out.append({'seed': s, 'test_r2': tr2, 'complexity': cx,
                    'n_terms': nterms, 'expr': expr,
                    'compression': [(c[0], c[1], c[2], c[3]) for c in comp]})
        print(f'seed {s}: R2={tr2:.4f} cx={cx} terms={nterms}', flush=True)
    med_r2 = float(np.median([o['test_r2'] for o in out]))
    med_cx = float(np.median([o['complexity'] for o in out]))
    print(f'MEDIAN R2={med_r2:.4f} (bar 0.3009) MEDIAN CX={med_cx:.0f} (bar 4996.5; p2 bar R2>0.1758 cx<=20)')
    print(f'elapsed {time.time()-t0:.0f}s')
    with open('attempts/smuggler/output/results.json', 'w') as fh:
        json.dump({'median_r2': med_r2, 'median_complexity': med_cx, 'per_split': out}, fh, indent=1)
    with open('attempts/smuggler/output/expressions.txt', 'w') as fh:
        for o in out:
            fh.write(f"seed {o['seed']} R2={o['test_r2']:.4f} cx={o['complexity']} terms={o['n_terms']}: {o['expr']}\n")


if __name__ == '__main__':
    main()
