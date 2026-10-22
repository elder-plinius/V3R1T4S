"""Standalone check of the certificate for p_c^site(Z^2) >= 0.5567 (standard library only).

usage: python check_bound.py <object folder>     (run_checks.sh calls it; last line PASS or FAIL)

1. The object files are the panelled ones (sha256 against OBJECT_FILES.sha256), and bound.json names window.py's
   sha256.
2. bound = 1 - p exactly, and bound > 0.556 (the 1996 record) strictly.
3. Independent recomputation (indep_cones.py, written from the definitions in a separate context; it does not use
   window.py and keeps the cones exact, with no rounding): the exact worst margin at each depth 0..3. Each value in
   bound.json, from window.py's outwardly rounded cones, must be <= the exact one and within 1e-9 of it. The exact
   depth-3 margin must be > 0.
4. The root step, computed here from the definition: the origin's four children dominate Bernoulli(1-p)^4 on every
   increasing event, and P(origin open) = 1 - (1-p)^2 >= 1 - p.
"""
import hashlib
import json
import os
import sys
from fractions import Fraction as F
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def fail(msg):
    print("problem:", msg)
    print("FAIL")
    sys.exit(1)


def eadj(v, sv, w, sw):
    """eps-adjacency of neighbours v, w of Z^2 (van den Berg-Ermakov 1996, p. 203): min = smaller coordinate sum;
    upper(min)-upper(max), lower(min)-lower(max) or upper(min)-lower(max). States are (upper, lower)."""
    mn, mx = (sv, sw) if v[0] + v[1] < w[0] + w[1] else (sw, sv)
    return bool((mn[0] and mx[0]) or (mn[1] and mx[1]) or (mn[0] and mx[1]))


def root_step(p):
    q = 1 - p
    states = [(u, l) for u in (0, 1) for l in (0, 1)]
    pi = {s: (p if s[0] else q) * (p if s[1] else q) for s in states}
    opens = [s for s in states if s != (0, 0)]
    kids = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    pts = list(product((0, 1), repeat=4))
    law = {x: F(0) for x in pts}
    z = sum(pi[b] for b in opens)
    for b in opens:
        pk = [sum(pi[a] for a in states if eadj((0, 0), b, k, a)) for k in kids]
        for x in pts:
            t = pi[b] / z
            for xi, pp in zip(x, pk):
                t *= pp if xi else 1 - pp
            law[x] += t
    worst, n = None, 0
    for mask in range(1, 2 ** 16 - 1):
        S = [pts[i] for i in range(16) if mask >> i & 1]
        Sset = set(S)
        if not all(y in Sset for x in S for y in pts if all(b >= a for a, b in zip(x, y))):
            continue
        n += 1
        tgt = F(0)
        for x in S:
            t = F(1)
            for xi in x:
                t *= (1 - p) if xi else p
            tgt += t
        m = sum(law[x] for x in S) - tgt
        worst = m if worst is None else min(worst, m)
    return n, worst, (1 - q * q) - (1 - p)


def main():
    obj = sys.argv[1] if len(sys.argv) > 1 else "object"
    pins = {}
    for line in open(os.path.join(HERE, "OBJECT_FILES.sha256")):
        h, name = line.split()
        pins[name] = h
    for name, h in sorted(pins.items()):
        path = os.path.join(obj, name)
        if not os.path.isfile(path) or hashlib.sha256(open(path, "rb").read()).hexdigest() != h:
            fail("object/%s does not match its pinned sha256" % name)
    print("object files match OBJECT_FILES.sha256 (%d files)" % len(pins))
    b = json.load(open(os.path.join(obj, "bound.json")))
    if b["window_py_sha256"] != pins["window.py"]:
        fail("bound.json does not name window.py's sha256")
    p, bound = F(b["p"]), F(b["bound"])
    if bound != 1 - p:
        fail("bound != 1 - p")
    if not bound > F(556, 1000):
        fail("bound is not strictly above 0.556")
    print("p = %s, bound = %s = %s > 0.556" % (p, bound, float(bound)))

    import indep_cones as I
    rows = {r["depth"]: F(r["worst_margin"]) for r in b["levels"]}
    exact = {}
    for k, m, U, D in I.run_levels(p, 3):
        exact[k] = m.check(U, D)[0]
        if k not in rows:
            fail("bound.json has no depth %d" % k)
        r = rows[k]
        if not (r <= exact[k] and exact[k] - r < F(1, 10 ** 9)):
            fail("depth %d: bound.json margin %s is not within (exact - 1e-9, exact], exact %.12e" % (k, float(r), float(exact[k])))
        print("depth %d: exact worst margin %.9e (independent), certificate %.9e: consistent" % (k, float(exact[k]), float(r)))
    if not exact[3] > 0:
        fail("exact depth-3 margin is not positive")
    n, rm, r0 = root_step(p)
    print("root step: %d increasing events of {0,1}^4, worst margin %.9e; P(origin open) - (1-p) = %.6e" % (n, float(rm), float(r0)))
    if n != 166 or not rm > 0 or not r0 >= 0:
        fail("root step")
    print("p_c^site(Z^2) >= %s (given PROOF.md)" % bound)
    print("PASS")


if __name__ == "__main__":
    main()
