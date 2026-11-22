#!/usr/bin/env python3
"""Part B, lens 1b (exploratory; PREREG.v5.md): growth from best(N-1) with the lens-3b site set, N = 200..101.
Based on lens 3b; its docstring follows.

Part B, lens 3b (exploratory; PREREG.v4.md): growth chains with 3-fold and 4-fold sites. Based on lens 3.
Lens 3 docstring follows.

Part B, lens 3 (exploratory): decahedral family propagation for Gupta Co_N (PREREG.v3.md).

    python3 search_deca.py WALL_SECONDS

Chains (seed -> sizes): 95 -> 94..89 and 96..100; 101 -> 100..96 and 102..107; 113 -> 112..107 and 114..119;
121 -> 120..115; 122 -> 123..128; 196 -> 195..190; 198 -> 199; 200 -> 199. Seeds are the polished Co.zip files.
Grow: add one atom at every surface hollow site (above a triangle of mutually bonded atoms, both sides, kept if no
atom is closer than 0.85), quick relax, polish the best three, keep the lowest. Etch: remove each atom with
coordination < 10 the same way. Each chain member is compared with E_best(N) = min(polished table, polished Co.zip).
Writes deca_log.jsonl and best_deca/<N>.xyz for gains > 1e-5 eV.
"""
import itertools, json, os, re, subprocess, sys, tarfile, time, zipfile
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gupta

HERE = os.path.dirname(os.path.abspath(__file__))
WALL = float(sys.argv[1]) if len(sys.argv) > 1 else 3000
T0 = time.time()
CHAINS = [(196, [197]), (121, [122]), (95, list(range(96, 101))), (101, list(range(102, 108))), (113, list(range(114, 120))),
          (122, list(range(123, 129))), (198, [199])]


def load_xyz(s):
    return np.array([[float(v) for v in l.split()[:3]] for l in s.splitlines() if len(l.split()) >= 3])


def relax(X, gtol=1e-4, maxiter=3000):
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
    with open(os.path.join(HERE, "grow1b_log.jsonl"), "a") as fh:
        fh.write(json.dumps(rec) + "\n")


def hollow_sites(X):
    d = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    coord = ((d < 1.2) & ~np.eye(len(X), dtype=bool)).sum(1)
    k = np.arange(40) + 0.5
    phi = np.arccos(1 - 2 * k / 40); th = np.pi * (1 + 5 ** 0.5) * k
    dirs = np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], 1)
    out = []
    for i in np.where(coord < 10)[0]:
        for s in X[i] + 0.95 * dirs:
            dd = np.linalg.norm(X - s, axis=1)
            if dd.min() >= 0.85 and (dd < 1.15).sum() >= 3 and all(np.linalg.norm(s - t) > 0.25 for t in out):
                out.append(s)
    return out


def hollow_sites_v3(X):
    d = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1))
    bond = (d < 1.2) & ~np.eye(len(X), dtype=bool)
    coord = bond.sum(1)
    surf = np.where(coord < 10)[0]
    sset = set(surf.tolist())
    sites = []
    for i in surf:
        nb = [j for j in np.where(bond[i])[0] if j > i and j in sset]
        for j, k in itertools.combinations(nb, 2):
            if not bond[j, k]:
                continue
            P = X[[i, j, k]]; cen = P.mean(0)
            nrm = np.cross(P[1] - P[0], P[2] - P[0]); nrm /= np.linalg.norm(nrm)
            side = np.mean([np.linalg.norm(P[a] - cen) for a in range(3)])
            h = np.sqrt(max(0.81 - side ** 2, 0.04))
            for sgn in (1.0, -1.0):
                s = cen + sgn * h * nrm
                if np.min(np.linalg.norm(X - s, axis=1)) >= 0.85:
                    sites.append(s)
    out = []
    for s in sites:
        if all(np.linalg.norm(s - t) > 0.2 for t in out):
            out.append(s)
    return out


def best_of(cands):
    quick = sorted((relax(Y)[::-1] for Y in cands), key=lambda t: t[0])[:3]
    fin = [relax(Y, gtol=1e-9, maxiter=20000) for _, Y in quick]
    Xb, eb = min(fin, key=lambda t: t[1])
    return Xb, eb


def main():
    tf = tarfile.open(os.path.join(HERE, "net", "points.tgz"), "r:gz")
    tab = {int(m.name.split("/")[-1]): load_xyz(tf.extractfile(m).read().decode()) for m in tf.getmembers() if m.isfile()}
    zf = zipfile.ZipFile(os.path.join(HERE, "net", "Co.zip"))
    zp = {int(re.search(r"Co(\d+)\.txt", i.filename).group(1)): load_xyz(zf.read(i).decode()) for i in zf.infolist() if re.search(r"Co\d+\.txt", i.filename)}
    best = {}
    for n in range(100, 201):
        X, e = relax(tab[n], gtol=1e-8)
        if n in zp:
            Xz, ez = relax(zp[n], gtol=1e-8)
            if ez < e: X, e = Xz, ez
        best[n] = (X, e)
    os.makedirs(os.path.join(HERE, "best_grow1b"), exist_ok=True)
    log({"event": "start", "lens": "1b", "range": [200, 101]})
    for n in range(200, 100, -1):
        if time.time() - T0 > WALL:
            log({"event": "stop", "reason": "wall", "next_N": n}); return
        if free_mem_pct() < 15:
            log({"event": "stop", "reason": "free memory < 15%", "next_N": n}); return
        t1 = time.time()
        cur = best[n - 1][0]
        cands = [np.vstack([cur, s]) for s in hollow_sites(cur)]
        Xb, eb = best_of(cands)
        gain = best[n][1] - eb
        log({"event": "size", "N": n, "n_cands": len(cands), "E_best_ref": round(best[n][1], 7), "E_found": round(eb, 7),
             "gain": round(gain, 7), "sec": round(time.time() - t1, 1)})
        if gain > 1e-5:
            np.savetxt(os.path.join(HERE, "best_grow1b", "%d.xyz" % n), Xb, fmt="%.12f")
    log({"event": "stop", "reason": "range done"})


if __name__ == "__main__":
    main()
