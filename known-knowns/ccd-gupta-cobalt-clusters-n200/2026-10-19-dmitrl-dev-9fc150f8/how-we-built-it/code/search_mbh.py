#!/usr/bin/env python3
"""Part B, lens 2 (exploratory): monotonic basin hopping with surface moves for Gupta Co_N (PREREG.v2.md).

    python3 search_mbh.py WALL_SECONDS STEPS_PER_SIZE N_HI N_LO

For N from N_HI down to N_LO: start from E_best(N) = min(polished table, polished Co.zip); each step moves 1-3 of the
least-coordinated atoms to sites above random convex-hull facets (90% of steps) or shakes all atoms by a Gaussian of
0.08 r0 (10%), relaxes (L-BFGS, gtol 1e-5) and accepts if lower by > 1e-6 eV. Seeds: default_rng(100000 * N + 2).
Writes mbh_log.jsonl and best_mbh/<N>.xyz for any size whose final polished energy beats E_best(N) by > 1e-5 eV.
"""
import json, os, re, subprocess, sys, tarfile, time, zipfile
import numpy as np
from scipy.optimize import minimize
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gupta

HERE = os.path.dirname(os.path.abspath(__file__))
WALL, STEPS, NHI, NLO = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
T0 = time.time()


def load_xyz(s):
    return np.array([[float(v) for v in l.split()[:3]] for l in s.splitlines() if len(l.split()) >= 3])


def relax(X, gtol=1e-5, maxiter=3000):
    r = minimize(gupta.energy_grad, np.asarray(X, float).ravel(), jac=True, method="L-BFGS-B",
                 options=dict(maxiter=maxiter, maxcor=30, gtol=gtol, ftol=1e-15))
    return r.x.reshape(-1, 3), float(r.fun)


def free_mem_pct():
    try:
        out = subprocess.run(["memory_pressure"], capture_output=True, text=True, timeout=20).stdout
        m = re.search(r"free percentage: (\d+)%", out)
        return int(m.group(1)) if m else 100
    except Exception:
        return 100


def log(rec):
    rec["t"] = round(time.time() - T0, 1)
    with open(os.path.join(HERE, "mbh_log.jsonl"), "a") as fh:
        fh.write(json.dumps(rec) + "\n")


def surface_move(X, rng):
    n = len(X)
    d = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    coord = (d < 1.2).sum(1) - 1
    k = int(rng.integers(1, 4))
    low = np.argsort(coord + rng.random(n) * 0.5)[:max(k, 1)]
    Y = np.delete(X, low, axis=0)
    hull = ConvexHull(Y); c0 = Y.mean(0)
    for _ in range(k):
        f = hull.simplices[rng.integers(len(hull.simplices))]
        P = Y[f]; cen = P.mean(0); nrm = np.cross(P[1] - P[0], P[2] - P[0]); nrm /= np.linalg.norm(nrm)
        if np.dot(nrm, cen - c0) < 0: nrm = -nrm
        side = np.mean([np.linalg.norm(P[a] - cen) for a in range(3)])
        Y = np.vstack([Y, cen + np.sqrt(max(0.81 - side ** 2, 0.04)) * nrm + rng.normal(0, 0.05, 3)])
    return Y


def main():
    tf = tarfile.open(os.path.join(HERE, "net", "points.tgz"), "r:gz")
    tab = {int(m.name.split("/")[-1]): load_xyz(tf.extractfile(m).read().decode()) for m in tf.getmembers() if m.isfile()}
    zf = zipfile.ZipFile(os.path.join(HERE, "net", "Co.zip"))
    zp = {int(re.search(r"Co(\d+)\.txt", i.filename).group(1)): load_xyz(zf.read(i).decode()) for i in zf.infolist() if re.search(r"Co\d+\.txt", i.filename)}
    os.makedirs(os.path.join(HERE, "best_mbh"), exist_ok=True)
    log({"event": "start", "steps": STEPS, "range": [NHI, NLO]})
    for n in range(NHI, NLO - 1, -1):
        if time.time() - T0 > WALL:
            log({"event": "stop", "reason": "wall", "next_N": n}); return
        if free_mem_pct() < 15:
            log({"event": "stop", "reason": "free memory < 15%", "next_N": n}); return
        X, e = relax(tab[n], gtol=1e-8)
        if n in zp:
            Xz, ez = relax(zp[n], gtol=1e-8)
            if ez < e: X, e = Xz, ez
        ref = e; cur = (e, X); rng = np.random.default_rng(100000 * n + 2); acc = 0; t1 = time.time()
        for s in range(STEPS):
            if rng.random() < 0.9:
                Y = surface_move(cur[1], rng)
            else:
                Y = cur[1] + rng.normal(0, 0.08, cur[1].shape)
            Yr, ey = relax(Y)
            if ey < cur[0] - 1e-6:
                cur = (ey, Yr); acc += 1
        Xf, ef = relax(cur[1], gtol=1e-9, maxiter=20000)
        rec = {"event": "size", "N": n, "E_ref": round(ref, 7), "E_found": round(ef, 7), "gain": round(ref - ef, 7),
               "accepted": acc, "steps": STEPS, "sec": round(time.time() - t1, 1)}
        log(rec)
        if ref - ef > 1e-5:
            np.savetxt(os.path.join(HERE, "best_mbh", "%d.xyz" % n), Xf, fmt="%.12f")
    log({"event": "stop", "reason": "range done"})


if __name__ == "__main__":
    main()
