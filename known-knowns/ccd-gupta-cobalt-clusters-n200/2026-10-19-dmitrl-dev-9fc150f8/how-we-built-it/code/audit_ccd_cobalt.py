#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Audit of the CCD Gupta cobalt table (bank target ccd-gupta-cobalt-clusters-n200, partial win p1).

    python3 audit_ccd_cobalt.py DATA_DIR OUT_CSV

DATA_DIR holds cobalt.html, points.tgz and Co.zip exactly as downloaded from
https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/. For every table file (N = 2..200) and every Co.zip file: energy as
posted (float64, math.fsum), gradient norm, then L-BFGS polish (scipy) and the polished energy; compares with the
posted table energy and with Co/Energy.txt; writes the merged table. Needs numpy and scipy.
Potential: Gupta in reduced units r/r0 with the Cleri-Rosato cobalt parameters A 0.0950, xi 1.4880, p 11.604, q 2.286.
"""
import csv, html, io, math, re, sys, tarfile, zipfile
import numpy as np
from scipy.optimize import minimize

A, XI, P, Q = 0.0950, 1.4880, 11.604, 2.286


def e_g(x):
    X = x.reshape(-1, 3); n = len(X); i, j = np.triu_indices(n, 1)
    dv = X[i] - X[j]; r = np.sqrt((dv * dv).sum(1))
    rep = 2.0 * A * np.exp(-P * (r - 1.0)); att = XI * XI * np.exp(-2.0 * Q * (r - 1.0))
    rho = np.bincount(i, att, n) + np.bincount(j, att, n); s = np.sqrt(rho)
    e = math.fsum(rep.tolist()) - math.fsum(s.tolist())
    w = (-P * rep + Q * att * (1.0 / s[i] + 1.0 / s[j])) / r
    g = np.zeros_like(X); np.add.at(g, i, w[:, None] * dv); np.add.at(g, j, -w[:, None] * dv)
    return e, g.ravel()


def polish(x):
    r = minimize(e_g, x, jac=True, method="L-BFGS-B", options=dict(maxiter=50000, maxcor=50, gtol=1e-11, ftol=1e-17))
    e, g = e_g(r.x)
    return r.x, e, float(np.linalg.norm(g))


def load(s):
    return np.array([[float(v) for v in l.split()[:3]] for l in s.splitlines() if len(l.split()) >= 3]).ravel()


def main():
    ddir, out = sys.argv[1], sys.argv[2]
    page = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", open(ddir + "/cobalt.html", "rb").read().decode("latin-1"))).split())
    tab_txt = page[page.find("N PG Energy / eV"):]
    posted = {}
    for n, pg, en in re.findall(r"(?<![\d.])(\d{1,3}) ((?:[A-Z][a-z]* ?(?:\d+[vhd]?|infh|[vhds])?|C s|C 1|C i|O h|T d|I h|D infh)) (-\d+\.\d+)", tab_txt):
        if 2 <= int(n) <= 200 and int(n) not in posted:
            posted[int(n)] = (pg.strip(), en)
    assert sorted(posted) == list(range(2, 201)), "table parse"
    tf = tarfile.open(ddir + "/points.tgz", "r:gz")
    tab = {int(m.name.split("/")[-1]): load(tf.extractfile(m).read().decode()) for m in tf.getmembers() if m.isfile()}
    zf = zipfile.ZipFile(ddir + "/Co.zip")
    zx = {int(re.search(r"Co(\d+)\.txt", i.filename).group(1)): load(zf.read(i).decode()) for i in zf.infolist() if re.search(r"Co\d+\.txt", i.filename)}
    zE = {int(a): b for a, b in re.findall(r"Co(\d+)\s*:\s*(-\d+\.\d+)", zf.read("Co/Energy.txt").decode())}
    rows, as_is_bad, pol_bad, pol_lower = [], [], [], []
    for n in range(2, 201):
        x = tab[n]; assert len(x) == 3 * n
        e0, g0 = e_g(x); xp, ep, gp = polish(x)
        d0, dp = e0 - float(posted[n][1]), ep - float(posted[n][1])
        if abs(d0) > 1e-5: as_is_bad.append(n)
        if abs(dp) > 1e-5: pol_bad.append(n)
        if dp < -1e-4: pol_lower.append(n)
        row = dict(N=n, point_group=posted[n][0], E_table_posted=posted[n][1], E_table_file_as_is="%.9f" % e0,
                   d_as_is="%+.2e" % d0, grad_as_is="%.2e" % float(np.linalg.norm(g0)), E_table_polished="%.9f" % ep,
                   d_polished="%+.2e" % dp, grad_polished="%.1e" % gp, E_coZip_posted="", E_coZip_file_as_is="",
                   E_coZip_polished="", E_best="%.6f" % ep, best_source="table")
        if n in zx:
            ez0 = e_g(zx[n])[0]; _, ezp, _ = polish(zx[n])
            row.update(E_coZip_posted=zE[n], E_coZip_file_as_is="%.9f" % ez0, E_coZip_polished="%.9f" % ezp)
            if ezp < ep:
                row.update(E_best="%.6f" % ezp, best_source="Co.zip")
        rows.append(row)
    with open(out, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    dz = max(abs(float(r["E_coZip_file_as_is"]) - float(r["E_coZip_posted"])) for r in rows if r["E_coZip_posted"] != "")
    dpm = max(abs(float(r["d_polished"])) for r in rows)
    print("table files: 199; Co.zip files: %d" % len(zx))
    print("Co.zip as-is energy vs Co/Energy.txt: max |d| = %.2e eV" % dz)
    print("table files whose as-is energy differs from the posted energy by > 1e-5 eV: %s" % as_is_bad)
    print("table files whose polished energy differs from the posted energy by > 1e-5 eV: %s" % pol_bad)
    print("max |polished - posted| over the table: %.2e eV" % dpm)
    print("posted structures that polish lower than posted by > 1e-4 eV: %s" % pol_lower)
    print("rows where Co.zip is the best: %s" % [r["N"] for r in rows if r["best_source"] == "Co.zip"])


if __name__ == "__main__":
    main()
