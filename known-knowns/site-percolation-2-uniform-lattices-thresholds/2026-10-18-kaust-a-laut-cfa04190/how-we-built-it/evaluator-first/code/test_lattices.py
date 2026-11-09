"""Known positives and negatives for the tiling checker (lattices.check_tiling)."""
import math
import os
import sys
from fractions import Fraction as Fr
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lattices as L  # noqa: E402


def frac(res):
    return {L.conf_str(c): f for c, f in res["fractions"].items()}


def main():
    fails = 0

    def expect(cond, msg):
        nonlocal fails
        print(("ok    " if cond else "FAIL  ") + msg)
        fails += not cond

    # positives: Wikipedia rows #20-#23 and Archimedean lattices
    want = {
        "20": ({"3^6": Fr(1, 2), "3^3.4^2": Fr(1, 2)}, Fr(11, 2)),
        "21": ({"3^6": Fr(1, 3), "3^3.4^2": Fr(2, 3)}, Fr(16, 3)),
        "22": ({"3^3.4^2": Fr(2, 3), "4^4": Fr(1, 3)}, Fr(14, 3)),
        "23": ({"3^3.4^2": Fr(1, 2), "4^4": Fr(1, 2)}, Fr(9, 2)),
    }
    for k, (fr, zb) in want.items():
        r = L.check_tiling(L.TWO_UNIFORM[k](), verbose=False)
        expect(not r["problems"] and frac(r) == fr and r["zbar"] == zb and r["orbits"] == 2,
               "#%s: fractions %s, zbar %s, 2 orbits" % (k, fr, zb))
    for name, conf in [("square", "4^4"), ("triangular", "3^6"), ("kagome", "3.6.3.6"), ("honeycomb", "6^3"),
                       ("(3,12^2)", "3.12^2")]:
        r = L.check_tiling(L.ARCHIMEDEAN[name](), verbose=False)
        expect(not r["problems"] and frac(r) == {conf: 1} and r["orbits"] == 1, "%s is %s, 1 orbit" % (name, conf))

    # negative 1: rows SSTT is a 3-uniform tiling (three vertex types, three orbits)
    r = L.check_tiling(L.rows("SSTT"), verbose=False)
    expect(not r["problems"] and len(r["fractions"]) == 3 and r["orbits"] == 3, "SSTT has 3 vertex types and 3 orbits")

    # negative 2: a square lattice with an added diagonal is not a tiling by regular polygons
    sq = L.rows("S")
    bad = dict(sq)
    bad["edges"] = sq["edges"] + [(0, 0, 1, 1)]
    r = L.check_tiling(bad, verbose=False)
    expect(bool(r["problems"]), "square + diagonal is rejected (%s)" % (r["problems"][:2],))

    # negative 3: kagome with one vertex displaced (not a unit-edge tiling any more)
    r3 = math.sqrt(3)
    k = L.make_lattice("kagome-bad", (2, 0), (1, r3), [(0, 0), (1, 0), (0.5, r3 / 2 + 0.05)])
    r = L.check_tiling(k, verbose=False)
    expect(bool(r["problems"]) or frac(r) != {"3.6.3.6": 1}, "distorted kagome is rejected (%s)" % (r["problems"][:1],))

    # negative 4: rows SST mislabelled as #23 would fail the #23 fractions
    r = L.check_tiling(L.rows("SST"), verbose=False)
    expect(frac(r) != want["23"][0], "SST does not pass as #23")

    print("TESTS: %s (%d failures)" % ("PASS" if fails == 0 else "FAIL", fails))


if __name__ == "__main__":
    main()
