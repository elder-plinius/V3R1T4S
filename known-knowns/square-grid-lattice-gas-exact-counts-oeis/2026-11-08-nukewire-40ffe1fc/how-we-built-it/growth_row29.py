"""growth_row29.py — the row-29 claim's frozen growth test.

Formula = the row-28 arc's PREREG test VERBATIM (see
runs/2026-11-03-0830/attempts/evaluator-first/code/growth_fit.py):
  fit y = ln T(m,n)/(m*n) = lnW - c/(m*n) by least squares on ALL cells of
  published rows 26 and 27; tol = max(1e-5, 3*max residual); a candidate row's
  cells PASS iff |ln T/(m*n) - (lnW - c/(m*n))| <= tol for every cell, and the
  fitted W sits below Finch's 1.9402139258 (the a(28) package's constant).

Modes:
  regression   run the test on the PACKAGED row-28 object; must reproduce the
               arc's recorded result (fitted W = 1.9318762, PASS) before this
               script may be pointed at row-29 values.
  <file.json>  claim mode: {k: T(29,k)} values.
"""
import json
import os
from math import log

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WS = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..', '..'))
BFILE = os.path.join(WS, 'runs', '2026-11-08-1131', 'data', 'b210662.txt')
ROW28 = os.path.join(WS, 'runs', '2026-11-03-0830', 'row28_final.json')
W_FINCH = 1.9402139258          # Finch (quoted from the a(28) package)


def load_published(path):
    vals = [l.split()[1] for l in open(path) if l.strip()]
    tri, i = {}, 0
    for n in range(1, 28):
        for k in range(1, n + 1):
            tri[(n, k)] = int(vals[i])
            i += 1
    return tri


def fit(tri):
    pts = [(26, k, tri[(26, k)]) for k in range(1, 27)] + \
          [(27, k, tri[(27, k)]) for k in range(1, 28)]
    A = np.array([[1.0, -1.0 / (m * n)] for (m, n, _) in pts])
    y = np.array([log(v) / (m * n) for (m, n, v) in pts])
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    lnW, c = coef
    maxres = float(np.max(np.abs(y - A @ coef)))
    return lnW, c, maxres


def run_row(vals, m, lnW, c, tol):
    ok = True
    worst = 0.0
    for k in sorted(vals):
        dev = abs(log(vals[k]) / (m * k) - (lnW - c / (m * k)))
        worst = max(worst, dev)
        ok = ok and dev <= tol
    return ok, worst


def main():
    tri = load_published(BFILE)
    lnW, c, maxres = fit(tri)
    tol = max(1e-5, 3 * maxres)
    W = float(np.exp(lnW))
    print(f"fit on published rows 26-27 (all cells): lnW={lnW:.9f} "
          f"W={W:.7f} c={c:.4f} maxres={maxres:.2e} tol={tol:.2e}")
    print(f"|W - Finch {W_FINCH}| = {abs(W - W_FINCH):.2e} "
          f"(must be below, within 1%: "
          f"{W < W_FINCH and W > W_FINCH * 0.99})")
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "regression":
        row = {int(k): int(v) for k, v in json.load(open(ROW28)).items()}
        ok, worst = run_row(row, 28, lnW, c, tol)
        print(f"regression row-28: worst deviation {worst:.2e} -> "
              f"{'PASS' if ok else 'FAIL'} (arc recorded W=1.9318762 PASS)")
        print("GROWTH_REGRESSION:", "PASS" if ok else "FAIL")
        return 0 if ok else 1
    row = {int(k): int(v) for k, v in json.load(open(mode)).items()}
    ok, worst = run_row(row, 29, lnW, c, tol)
    print(f"row-29 worst deviation {worst:.2e} -> {'PASS' if ok else 'FAIL'}")
    print("GROWTH_ROW29:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
