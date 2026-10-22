"""Write the certificate record result/bound.json: exact worst margins of window.py's check at one p, depths 0..k.

usage: python cert.py <p as a fraction> <k> <out.json>
"""
import hashlib
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import window as W  # noqa: E402


def main():
    p, k, out = F(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    rows = []
    for kk, M, U, D in W.levels(p, k):
        m, ob, cside = M.check(U, D)
        rows.append({"depth": kk, "worst_margin": "%d/%d" % (m.numerator, m.denominator),
                     "worst_margin_float": float(m), "passes": m > 0, "worst_case": {"b2_orientation": ob,
                     "c_parent_side": cside}, "cone_sizes": {"U": {o: len(U[o]) for o in U},
                     "D": {o: len(D[o]) for o in D}}})
        print("depth %d: worst margin %.9e exact %s (b2 %s, c side %s) -> %s"
              % (kk, float(m), "%d/%d" % (m.numerator, m.denominator) if len(str(m.denominator)) < 40 else "(long)",
                 ob, cside, "PASS" if m > 0 else "fail"), flush=True)
    sha = hashlib.sha256(open(os.path.join(HERE, "window.py"), "rb").read()).hexdigest()
    res = {"claim": "p_c^site(Z^2) >= 1 - p", "p": "%d/%d" % (p.numerator, p.denominator),
           "bound": "%d/%d" % ((1 - p).numerator, (1 - p).denominator), "bound_float": float(1 - p),
           "window_py_sha256": sha, "grid": "2^40 outward rounding (window.round_out)", "levels": rows,
           "certified": any(r["passes"] for r in rows)}
    with open(out, "w", newline="\n") as f:
        json.dump(res, f, indent=1)
    print("certified p_c >= %s: %s" % (res["bound"], res["certified"]))


if __name__ == "__main__":
    main()
