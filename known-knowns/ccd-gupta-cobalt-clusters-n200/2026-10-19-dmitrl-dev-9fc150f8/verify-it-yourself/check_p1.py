#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Checker for the audit of the CCD Gupta cobalt table (bank target ccd-gupta-cobalt-clusters-n200, partial win p1).

    python3 check_p1.py OBJECT_CSV [DATA_DIR]

Without DATA_DIR it downloads cobalt.html, points.tgz and Co.zip once each from
https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/ (no retries) into a temporary folder; with DATA_DIR it reads them
there. Either way each file must match the pinned sha256 below. It recomputes every row of OBJECT_CSV and prints PASS
only if every field agrees. Needs numpy and scipy (polishing); Python 3.8+.

Definition (reduced units, r in units of r0; energies in eV): E = sum_i [ sum_{j!=i} A exp(-p (r_ij - 1))
 - sqrt( sum_{j!=i} xi^2 exp(-2 q (r_ij - 1)) ) ], Cleri-Rosato cobalt A 0.0950, xi 1.4880, p 11.604, q 2.286.
"as is" = the energy of the posted coordinates; "polished" = after L-BFGS to a gradient norm below 1e-4 eV per reduced length (near a minimum the
remaining energy error is then about |g|^2 / (2 lambda_min), below 1e-7 eV here).
"""
import csv, hashlib, html, math, os, re, sys, tarfile, tempfile, urllib.request, zipfile

BASE = "https://www-wales.ch.cam.ac.uk/~wales/CCD/CoCCD/"
PINS = {"cobalt.html": "b1033b4142e8db518d0e9ef448c5e9d9e7fe651bc2088a0d54aad671eec030ef",
        "points.tgz": "bd568d308fc3944501e97fae1eb64d536769b59f0677f0e080246416c3c5f561",
        "Co.zip": "28141c13e9658f901e6fa49228b38f3eca69a206f904a34043280f2ecebde9ca"}
A, XI, P, Q = 0.0950, 1.4880, 11.604, 2.286


def fail(msg):
    print(msg)
    print("FAIL")
    sys.exit(1)


def get_data(ddir):
    out = {}
    for f, h in PINS.items():
        if ddir:
            b = open(os.path.join(ddir, f), "rb").read()
        else:
            try:
                with urllib.request.urlopen(BASE + f, timeout=120) as r:
                    b = r.read()
            except Exception as e:
                fail("could not download %s (%s); pass a DATA_DIR holding the three files" % (f, e))
        if hashlib.sha256(b).hexdigest() != h:
            fail("%s: sha256 %s differs from the pinned %s" % (f, hashlib.sha256(b).hexdigest(), h))
        out[f] = b
    return out


def main():
    try:
        import numpy as np
        from scipy.optimize import minimize
    except ImportError:
        fail("numpy and scipy are required (pip install numpy scipy)")

    def e_g(x):
        X = x.reshape(-1, 3); n = len(X); i, j = np.triu_indices(n, 1)
        dv = X[i] - X[j]; r = np.sqrt((dv * dv).sum(1))
        rep = 2.0 * A * np.exp(-P * (r - 1.0)); att = XI * XI * np.exp(-2.0 * Q * (r - 1.0))
        rho = np.bincount(i, att, n) + np.bincount(j, att, n); s = np.sqrt(rho)
        e = math.fsum(rep.tolist()) - math.fsum(s.tolist())
        w = (-P * rep + Q * att * (1.0 / s[i] + 1.0 / s[j])) / r
        g = np.zeros_like(X); np.add.at(g, i, w[:, None] * dv); np.add.at(g, j, -w[:, None] * dv)
        return e, g.ravel()

    def polished(x):
        r = minimize(e_g, x, jac=True, method="L-BFGS-B", options=dict(maxiter=50000, maxcor=50, gtol=1e-10, ftol=1e-17))
        e, g = e_g(r.x)
        if float(np.linalg.norm(g)) > 1e-4:
            fail("polish did not reach a gradient norm below 1e-4 (%.2e)" % float(np.linalg.norm(g)))
        return e

    def load(s):
        return np.array([[float(v) for v in l.split()[:3]] for l in s.splitlines() if len(l.split()) >= 3]).ravel()

    obj = sys.argv[1]
    data = get_data(sys.argv[2] if len(sys.argv) > 2 else None)
    page = " ".join(html.unescape(re.sub(r"<[^>]+>", " ", data["cobalt.html"].decode("latin-1"))).split())
    tab_txt = page[page.find("N PG Energy / eV"):]
    posted = {}
    for n, pg, en in re.findall(r"(?<![\d.])(\d{1,3}) ((?:[A-Z][a-z]* ?(?:\d+[vhd]?|infh|[vhds])?|C s|C 1|C i|O h|T d|I h|D infh)) (-\d+\.\d+)", tab_txt):
        if 2 <= int(n) <= 200 and int(n) not in posted:
            posted[int(n)] = (pg.strip(), en)
    if sorted(posted) != list(range(2, 201)):
        fail("could not parse 199 table rows from cobalt.html")
    tf = tarfile.open(fileobj=__import__("io").BytesIO(data["points.tgz"]), mode="r:gz")
    tab = {int(m.name.split("/")[-1]): load(tf.extractfile(m).read().decode()) for m in tf.getmembers() if m.isfile()}
    zf = zipfile.ZipFile(__import__("io").BytesIO(data["Co.zip"]))
    zx = {int(re.search(r"Co(\d+)\.txt", i.filename).group(1)): load(zf.read(i).decode()) for i in zf.infolist() if re.search(r"Co\d+\.txt", i.filename)}
    zE = {int(a): b for a, b in re.findall(r"Co(\d+)\s*:\s*(-\d+\.\d+)", zf.read("Co/Energy.txt").decode())}
    rows = list(csv.DictReader(open(obj, newline="")))
    if [int(r["N"]) for r in rows] != list(range(2, 201)):
        fail("object must list N = 2..200 in order")
    bad = []
    for r in rows:
        n = int(r["N"]); x = tab[n]
        if len(x) != 3 * n:
            fail("points file %d has %d atoms" % (n, len(x) // 3))
        e0 = e_g(x)[0]; ep = polished(x)
        exp = {"point_group": posted[n][0], "E_table_posted": posted[n][1],
               "as_is_off_by_more_than_1e-5": "yes" if abs(e0 - float(posted[n][1])) > 1e-5 else "no",
               "polished_within_1e-5": "yes" if abs(ep - float(posted[n][1])) <= 1e-5 else "no",
               "polishes_lower_by_more_than_1e-4": "yes" if ep < float(posted[n][1]) - 1e-4 else "no"}
        num = {"E_table_as_is": (e0, 2e-9), "E_table_polished": (ep, 2e-6)}
        eb, src = ep, "table"
        if n in zx:
            ez0 = e_g(zx[n])[0]; ezp = polished(zx[n])
            exp["E_coZip_posted"] = zE[n]
            num["E_coZip_as_is"] = (ez0, 2e-9)
            if abs(ez0 - float(zE[n])) > 5e-7:
                bad.append("N=%d: Co.zip file energy %.9f does not reproduce Energy.txt %s" % (n, ez0, zE[n]))
            if ezp < ep:
                eb, src = ezp, "Co.zip"
        else:
            exp["E_coZip_posted"] = ""
            if r["E_coZip_as_is"] != "":
                bad.append("N=%d: E_coZip_as_is should be empty" % n)
        exp["best_source"] = src
        num["E_best"] = (eb, 2e-6)
        for k, v in exp.items():
            if r[k] != v:
                bad.append("N=%d %s: object %r, recomputed %r" % (n, k, r[k], v))
        for k, (v, tol) in num.items():
            try:
                ok = abs(float(r[k]) - v) <= tol
            except ValueError:
                ok = False
            if not ok:
                bad.append("N=%d %s: object %r, recomputed %.9f" % (n, k, r[k], v))
    off = [r["N"] for r in rows if r["as_is_off_by_more_than_1e-5"] == "yes"]
    print("rows checked: %d; Co.zip rows: %d" % (len(rows), len(zx)))
    print("as posted, energy off by more than 1e-5 eV at N = %s" % ", ".join(off))
    print("after polishing, every posted energy reproduced within 1e-5 eV: %s" % all(r["polished_within_1e-5"] == "yes" for r in rows))
    print("posted structures that polish lower by more than 1e-4 eV: %s" % ([r["N"] for r in rows if r["polishes_lower_by_more_than_1e-4"] == "yes"] or "none"))
    print("rows whose best known energy is the Co.zip one: %s" % ", ".join(r["N"] for r in rows if r["best_source"] == "Co.zip"))
    for b in bad[:20]:
        print("MISMATCH", b)
    print("PASS" if not bad else "FAIL")
    sys.exit(0 if not bad else 1)


if __name__ == "__main__":
    main()
