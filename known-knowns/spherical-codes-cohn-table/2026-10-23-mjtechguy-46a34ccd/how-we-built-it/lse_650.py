#!/usr/bin/env python3
"""LogSumExp ladder (L-BFGS-B, float64) on the (25, 650) deletion file. Keeps the best hard maximum seen and writes it
atomically to <outdir>/lse_650.txt with lse_status.json. Usage: lse_650.py <in.txt> <outdir> <seconds>"""
import json, os, sys, time
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kernel import LogSumExp

def maxip(X):
    G = X @ X.T; np.fill_diagonal(G, -np.inf); return float(np.max(G))

def main():
    src, outdir, tl = sys.argv[1], sys.argv[2], float(sys.argv[3])
    X = np.loadtxt(src, delimiter=","); X /= np.linalg.norm(X, axis=1, keepdims=True)
    base = maxip(X); best, bestc = X.copy(), base; t0 = time.time(); trace = []
    print("start c=%.16e" % base, flush=True)
    for beta, iters in ((3e5, 300), (1e6, 300), (3e6, 300), (1e7, 250), (3e7, 200), (1e8, 150), (3e8, 120)):
        if time.time() - t0 > tl: break
        pts = best.copy()
        loss = LogSumExp(*pts.shape)
        res = minimize(loss.value_and_grad, pts.ravel(), args=(beta,), method="L-BFGS-B", jac=True,
                       options={"ftol": 1e-18, "gtol": 1e-14, "maxcor": 15, "maxiter": iters, "maxfun": iters * 4})
        Y = res.x.reshape(pts.shape); Y /= np.linalg.norm(Y, axis=1, keepdims=True); c = maxip(Y)
        trace.append({"beta": beta, "c": c, "nit": int(res.nit), "t": round(time.time() - t0, 1)})
        print("beta=%.0e c=%.16e drop=%.3e" % (beta, c, base - c), flush=True)
        if c < bestc:
            best, bestc = Y, c
            np.savetxt(os.path.join(outdir, "lse_650.txt.tmp"), best, delimiter=",", fmt="%.20e")
            os.replace(os.path.join(outdir, "lse_650.txt.tmp"), os.path.join(outdir, "lse_650.txt"))
        json.dump({"start": base, "best": bestc, "drop": base - bestc, "trace": trace}, open(os.path.join(outdir, "lse_status.json"), "w"))
    print("DONE drop=%.6e" % (base - bestc), flush=True)

if __name__ == "__main__":
    main()
