#!/usr/bin/env python3
"""Standalone checker for N = 745 Thomson config in object/cand_745.txt.
stdlib only (decimal). Checks points, energy vs claim, margin under Riesz cell, tangent grad < 1e-15."""
import sys, os
from decimal import Decimal as D, getcontext
getcontext().prec = 40
HERE = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(HERE, "..", "object", "cand_745.txt")
N = 745
TABLE_MIN = D("266280.2589229")
CLAIM = D("266280.2015165256924341327")

def main():
    ok = True
    rows = [l.split() for l in open(OBJ).read().splitlines() if l.strip()]
    if len(rows) != N or any(len(r) != 3 for r in rows):
        print("points: expected %d rows of 3, got %d" % (N, len(rows))); return False
    if min(len(t.lstrip("+-").replace(".", "").lstrip("0")) for r in rows for t in r) < 20:
        print("coordinates: fewer than 20 digits"); ok = False
    P = []
    for r in rows:
        x, y, z = (D(t) for t in r)
        n = (x * x + y * y + z * z).sqrt()
        P.append((x / n, y / n, z / n))
    print("points", N)
    E = D(0)
    G = [[D(0)] * 3 for _ in range(N)]
    for i in range(N):
        xi, yi, zi = P[i]; gi = G[i]
        for j in range(i + 1, N):
            xj, yj, zj = P[j]
            dx = xi - xj; dy = yi - yj; dz = zi - zj
            r2 = dx * dx + dy * dy + dz * dz
            ir = 1 / r2.sqrt(); ir3 = ir * ir * ir
            E += ir
            gi[0] -= dx * ir3; gi[1] -= dy * ir3; gi[2] -= dz * ir3
            gj = G[j]; gj[0] += dx * ir3; gj[1] += dy * ir3; gj[2] += dz * ir3
    g2 = D(0)
    for p, g in zip(P, G):
        d = p[0] * g[0] + p[1] * g[1] + p[2] * g[2]
        for k in range(3):
            t = g[k] - d * p[k]; g2 += t * t
    gn = g2.sqrt()
    print("energy %s" % format(E.quantize(D("1e-25")), "f"))
    print("claimed %s  |diff| %.3e" % (CLAIM, abs(E - CLAIM)))
    print("table_min %s  margin %.6e" % (TABLE_MIN, TABLE_MIN - E))
    print("tangent_grad_2norm %.3e" % gn)
    if abs(E - CLAIM) > D("1e-15"): print("energy does not match the claim"); ok = False
    if TABLE_MIN - E < D("1e-6"): print("not below the table by 1e-6"); ok = False
    if gn >= D("1e-15"): print("tangent gradient too large"); ok = False
    return ok

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
