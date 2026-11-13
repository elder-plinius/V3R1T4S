#!/usr/bin/env python3
"""Part B (exploratory) search: neighbour seeding for Gupta Co_N, N = 2..200 (see PREREG.md, addendum A1).

    python3 search_seed.py WALL_SECONDS

Reference E_best(N) = min(polished table, polished Co.zip). For each N in the queue: remove each surface atom of the
best N+1 structure, and add one atom above up to MAXF convex-hull facets of the best N-1 structure; quick L-BFGS relax
(gtol 1e-5), then a tight polish of the best candidate. A gain > 1e-5 eV is logged, the best is replaced, and N-1, N+1
are queued again (cascade). Writes search_log.jsonl and best/<N>.xyz (improvements only). One process.
"""
import io, json, os, re, subprocess, sys, tarfile, time, zipfile
import numpy as np
from scipy.optimize import minimize
from scipy.spatial import ConvexHull
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gupta

HERE = os.path.dirname(os.path.abspath(__file__))
WALL = float(sys.argv[1]) if len(sys.argv) > 1 else 3600
MAXF = 120
T0 = time.time()
rng_master = np.random.default_rng(20261019)


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
    with open(os.path.join(HERE, "search_log.jsonl"), "a") as fh:
        fh.write(json.dumps(rec) + "\n")


def main():
    tf = tarfile.open(os.path.join(HERE, "net", "points.tgz"), "r:gz")
    best = {}
    for m in tf.getmembers():
        if m.isfile():
            n = int(m.name.split("/")[-1])
            X, e = relax(load_xyz(tf.extractfile(m).read().decode()), gtol=1e-7)
            best[n] = (e, X, "table")
    zf = zipfile.ZipFile(os.path.join(HERE, "net", "Co.zip"))
    for i in zf.infolist():
        g = re.search(r"Co(\d+)\.txt", i.filename)
        if g:
            n = int(g.group(1)); X, e = relax(load_xyz(zf.read(i).decode()), gtol=1e-7)
            if e < best[n][0]:
                best[n] = (e, X, "Co.zip")
    ref = {n: best[n][0] for n in best}
    zips = sorted(n for n in best if best[n][2] == "Co.zip")
    first = []
    for z in zips:
        for n in (z - 1, z + 1):
            if 2 < n < 200 and n not in zips and n not in first:
                first.append(n)
    queue = first + [n for n in range(200, 79, -1) if n not in first] + [n for n in range(79, 2, -1) if n not in first]
    log({"event": "start", "queue_head": queue[:15], "n_queue": len(queue), "zips": zips})
    os.makedirs(os.path.join(HERE, "best"), exist_ok=True)
    done = 0
    while queue:
        if time.time() - T0 > WALL:
            log({"event": "stop", "reason": "wall", "done": done}); return
        if done % 10 == 0 and free_mem_pct() < 15:
            log({"event": "stop", "reason": "free memory < 15%", "done": done}); return
        n = queue.pop(0)
        cands = []
        if n + 1 in best:
            Xp = best[n + 1][1]
            d = np.sqrt(((Xp[:, None] - Xp[None]) ** 2).sum(-1))
            coord = (d < 1.2).sum(1) - 1
            for k in np.where(coord < 10)[0]:
                cands.append(("remove from %d (%s) atom %d" % (n + 1, best[n + 1][2], k), np.delete(Xp, k, axis=0)))
        if n - 1 in best and n - 1 >= 4:
            Xm = best[n - 1][1]
            c0 = Xm.mean(0)
            hull = ConvexHull(Xm)
            facets = hull.simplices
            if len(facets) > MAXF:
                facets = facets[rng_master.choice(len(facets), MAXF, replace=False)]
            for f in facets:
                P = Xm[f]; cen = P.mean(0); nrm = np.cross(P[1] - P[0], P[2] - P[0]); nrm /= np.linalg.norm(nrm)
                if np.dot(nrm, cen - c0) < 0: nrm = -nrm
                side = np.mean([np.linalg.norm(P[a] - cen) for a in range(3)])
                h = np.sqrt(max(0.81 - side ** 2, 0.04))
                cands.append(("add to %d (%s) facet" % (n - 1, best[n - 1][2]), np.vstack([Xm, cen + h * nrm])))
        bestc = (np.inf, None, None)
        for lab, X in cands:
            Xr, e = relax(X)
            if e < bestc[0]:
                bestc = (e, Xr, lab)
        if bestc[1] is None:
            done += 1; continue
        Xr, e = relax(bestc[1], gtol=1e-9, maxiter=20000)
        gain = best[n][0] - e
        rec = {"event": "size", "N": n, "n_cands": len(cands), "E_ref": round(ref[n], 7), "E_best_before": round(best[n][0], 7),
               "E_found": round(e, 7), "gain_vs_best": round(gain, 7), "gain_vs_ref": round(ref[n] - e, 7), "from": bestc[2]}
        log(rec)
        if gain > 1e-5:
            best[n] = (e, Xr, "seed")
            np.savetxt(os.path.join(HERE, "best", "%d.xyz" % n), Xr, fmt="%.12f")
            for m in (n - 1, n + 1):
                if 2 < m <= 200 and m not in queue[:3]:
                    queue.insert(0, m)
        done += 1
    log({"event": "stop", "reason": "queue empty", "done": done})


if __name__ == "__main__":
    main()
