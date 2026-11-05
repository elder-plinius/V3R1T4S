#!/usr/bin/env python3
"""Higher-beta LogSumExp steps from the polished (25, 651) file.

The 2026-10-21 ladder stopped at beta 1e6 once the hard maximum had fallen
by 1e-10. This run asks whether beta 1e7, 3e7 and 1e8 still move N=651.
"""
import json
import os
import sys
import time

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kernel import LogSumExp


def load(path):
    X = np.loadtxt(path, delimiter=",")
    X = np.ascontiguousarray(X, dtype=np.float64)
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    return X


def maxip(X):
    G = X @ X.T
    np.fill_diagonal(G, -np.inf)
    return float(np.max(G))


def step(pts, beta, maxiter):
    n, d = pts.shape
    loss = LogSumExp(n, d)
    res = minimize(
        loss.value_and_grad,
        pts.ravel(),
        args=(float(beta),),
        method="L-BFGS-B",
        jac=True,
        options={"ftol": 1e-18, "gtol": 1e-14, "maxcor": 15, "maxiter": maxiter, "maxfun": maxiter * 4},
    )
    Y = res.x.reshape(n, d)
    Y /= np.linalg.norm(Y, axis=1, keepdims=True)
    return Y, maxip(Y), int(res.nit)


def main():
    src, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    X = load(src)
    base = maxip(X)
    best, bestc = X.copy(), base
    pts = X.copy()
    trace = []
    t0 = time.perf_counter()
    print("start N=%d d=%d c=%.16e" % (X.shape[0], X.shape[1], base), flush=True)
    for beta, iters in ((1e7, 250), (3e7, 200), (1e8, 120)):
        pts, c, nit = step(pts, beta, iters)
        trace.append({"beta": beta, "c": c, "nit": nit})
        if np.isfinite(c) and c < bestc:
            best, bestc = pts.copy(), c
        print("beta=%.0e c=%.16e drop=%.3e nit=%d" % (beta, c, base - c, nit), flush=True)
        rec = {
            "N": int(X.shape[0]),
            "d": int(X.shape[1]),
            "start": base,
            "best": bestc,
            "drop_from_start": base - bestc,
            "seconds": time.perf_counter() - t0,
            "trace": trace,
        }
        with open(os.path.join(outdir, "continue_651.json"), "w") as f:
            json.dump(rec, f)
        if base - bestc >= 1e-12:
            np.savetxt(os.path.join(outdir, "continue_651.txt"), best, delimiter=",", fmt="%.20e")
    print("DONE drop=%.6e seconds=%.1f" % (base - bestc, time.perf_counter() - t0), flush=True)


if __name__ == "__main__":
    main()
