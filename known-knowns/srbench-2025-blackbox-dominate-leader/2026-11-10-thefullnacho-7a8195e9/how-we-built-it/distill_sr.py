#!/usr/bin/env python3
"""Lens 2 (smuggler): RBF kernel-ridge teacher, dictionary student fit to teacher
predictions. Fixed procedure per PREREG.md. Writes output/results.json."""
import sys, json
sys.path.insert(0, 'code')
sys.path.insert(0, 'attempts/constructor/code')
import numpy as np
import sympy as sp
from check_srbench import load_data, split, r2
from dict_sr import build_library, term_expr, MAX_TERMS, MIN_GAIN
sys.path.insert(0, 'data')
from symbolic_utils import complexity as srbench_complexity

LAMBDA = 1e-3


def teacher_fit_predict(Xtr, ytr, Xev):
    mu, sd = Xtr.mean(0), Xtr.std(0)
    sd[sd == 0] = 1.0
    Ztr = (Xtr - mu) / sd
    Zev = (Xev - mu) / sd
    rng = np.random.RandomState(0)
    idx = rng.choice(len(Ztr), size=min(200, len(Ztr)), replace=False)
    d = np.sqrt(((Ztr[idx, None, :] - Ztr[None, :, :]) ** 2).sum(-1))
    d_med = np.median(d[d > 0])
    gamma = 1.0 / (2.0 * d_med ** 2)
    K = np.exp(-gamma * ((Ztr[:, None, :] - Ztr[None, :, :]) ** 2).sum(-1))
    alpha = np.linalg.solve(K + LAMBDA * len(ytr) * np.eye(len(ytr)), ytr)
    Kev = np.exp(-gamma * ((Zev[:, None, :] - Ztr[None, :, :]) ** 2).sum(-1))
    return Kev @ alpha, gamma


def run_split(seed, X, y):
    Xtr, ytr, Xte, yte = split(seed, X, y)
    ytr_smooth, gamma = teacher_fit_predict(Xtr, ytr, Xtr)
    names, Mtr = build_library(Xtr)
    _, Mte = build_library(Xte)
    rng = np.random.RandomState(0)
    perm = rng.permutation(len(ytr))
    n_val = len(ytr) // 5
    vi, ti = perm[:n_val], perm[n_val:]
    sel = [0]
    best_val = r2(ytr_smooth[vi], np.full(n_val, ytr_smooth[ti].mean()))
    while len(sel) < MAX_TERMS + 1:
        best_gain, best_k = 0.0, None
        for k in range(1, Mtr.shape[1]):
            if k in sel:
                continue
            cols = sel + [k]
            coef, *_ = np.linalg.lstsq(Mtr[ti][:, cols], ytr_smooth[ti], rcond=None)
            val = r2(ytr_smooth[vi], Mtr[vi][:, cols] @ coef)
            if val - best_val > best_gain:
                best_gain, best_k = val - best_val, k
        if best_k is None or best_gain < MIN_GAIN:
            break
        sel.append(best_k)
        coef, *_ = np.linalg.lstsq(Mtr[ti][:, sel], ytr_smooth[ti], rcond=None)
        best_val = r2(ytr_smooth[vi], Mtr[vi][:, sel] @ coef)
    coef, *_ = np.linalg.lstsq(Mtr[:, sel], ytr_smooth, rcond=None)
    yhat = Mte[:, sel] @ coef
    test_r2 = r2(yte, yhat)
    expr = sum((term_expr(names[k], c) for k, c in zip(sel, coef)), sp.Integer(0))
    cx = int(srbench_complexity(expr))
    return test_r2, cx, len(sel) - 1, str(expr), gamma


def main():
    X, y, _ = load_data()
    import pyarrow.feather as f
    df = f.read_feather('data/results.feather')
    seeds = sorted(df[df['dataset'] == '1028_SWD']['random_state'].unique().tolist())
    out = []
    for s in seeds:
        tr2, cx, nterms, expr, gamma = run_split(s, X, y)
        out.append({'seed': s, 'test_r2': tr2, 'complexity': cx, 'n_terms': nterms, 'expr': expr})
        print(f"seed {s}: R2={tr2:.4f} cx={cx} terms={nterms} gamma={gamma:.4f}")
    med_r2 = float(np.median([o['test_r2'] for o in out]))
    med_cx = float(np.median([o['complexity'] for o in out]))
    print(f"MEDIAN R2={med_r2:.4f} (bar 0.3800) MEDIAN CX={med_cx:.0f} (bar 3270; p2 bar R2>0.2430 cx<=20)")
    with open('attempts/smuggler/output/results.json', 'w') as fh:
        json.dump({'median_r2': med_r2, 'median_complexity': med_cx, 'per_split': out}, fh, indent=1)


if __name__ == '__main__':
    main()
