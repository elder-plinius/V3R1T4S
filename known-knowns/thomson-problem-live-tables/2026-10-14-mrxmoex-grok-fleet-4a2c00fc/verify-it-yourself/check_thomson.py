#!/usr/bin/env python3
"""Standalone checker for the N = 3552 configuration in object/riesz_3552_polished.txt (Python 3 standard library only).
Energy E = sum_{i<j} 1/|x_i - x_j| of the points normalized to the unit sphere.
Float64 with math.fsum, enough to resolve the 1.5e-5 gap; the 25-digit value needs the full cert in RUN_IT_YOURSELF.md."""
import sys, os, math
from decimal import Decimal as D, getcontext
getcontext().prec = 40
HERE = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(HERE, "..", "object", "riesz_3552_polished.txt")
N = 3552
CELL = D("6191355.6866585")          # posted table cell compared against
CLAIM = D("6191355.686643545416998382")        # claimed mpmath dps-30 energy of the object
MODE = "mismatch"             # below: object must be >= 1e-6 below CELL; mismatch: |object - CELL| > 1e-6
FAST = True               # float64 + math.fsum (large N); otherwise Decimal at 40 digits
ETOL = D("1e-8"); GTOL = 1e-6

def load():
    rows = [l.split() for l in open(OBJ).read().splitlines() if l.strip()]
    if len(rows) != N or any(len(r) != 3 for r in rows):
        print("points: expected %d rows of 3, got %d" % (N, len(rows))); return None
    if min(len(t.lstrip("+-").replace(".", "").lstrip("0")) for r in rows for t in r) < 20:
        print("coordinates: fewer than 20 digits"); return None
    P = []
    for r in rows:
        x, y, z = (D(t) for t in r)
        n = (x * x + y * y + z * z).sqrt()
        P.append((x / n, y / n, z / n))
    return P

def energy_decimal(P):
    E = D(0); G = [[D(0)] * 3 for _ in range(N)]
    for i in range(N):
        xi, yi, zi = P[i]; gi = G[i]
        for j in range(i + 1, N):
            xj, yj, zj = P[j]
            dx = xi - xj; dy = yi - yj; dz = zi - zj
            ir = 1 / (dx * dx + dy * dy + dz * dz).sqrt(); ir3 = ir * ir * ir
            E += ir
            gi[0] -= dx * ir3; gi[1] -= dy * ir3; gi[2] -= dz * ir3
            gj = G[j]; gj[0] += dx * ir3; gj[1] += dy * ir3; gj[2] += dz * ir3
    g2 = D(0)
    for p, g in zip(P, G):
        d = p[0] * g[0] + p[1] * g[1] + p[2] * g[2]
        for k in range(3):
            t = g[k] - d * p[k]; g2 += t * t
    return E, float(g2.sqrt())

def energy_float(P):
    Q = [(float(a), float(b), float(c)) for a, b, c in P]
    terms = []; G = [[0.0] * 3 for _ in range(N)]
    for i in range(N):
        xi, yi, zi = Q[i]; gi = G[i]; row = []
        for j in range(i + 1, N):
            xj, yj, zj = Q[j]
            dx = xi - xj; dy = yi - yj; dz = zi - zj
            ir = 1.0 / math.sqrt(dx * dx + dy * dy + dz * dz); ir3 = ir * ir * ir
            row.append(ir)
            gi[0] -= dx * ir3; gi[1] -= dy * ir3; gi[2] -= dz * ir3
            gj = G[j]; gj[0] += dx * ir3; gj[1] += dy * ir3; gj[2] += dz * ir3
        terms.append(math.fsum(row))
    g2 = 0.0
    for p, g in zip(Q, G):
        d = p[0] * g[0] + p[1] * g[1] + p[2] * g[2]
        for k in range(3):
            t = g[k] - d * p[k]; g2 += t * t
    return D(repr(math.fsum(terms))), math.sqrt(g2)

def main():
    P = load()
    if P is None: return False
    print("points", N)
    E, gn = energy_float(P) if FAST else energy_decimal(P)
    ok = True
    print("energy %s" % format(E.quantize(D("1e-12")), "f"))
    print("claimed %s  |diff| %.3e (tolerance %s)" % (CLAIM, abs(E - CLAIM), ETOL))
    print("table_cell %s  cell - energy %.6e" % (CELL, CELL - E))
    print("tangent_grad_2norm %.3e (threshold %g)" % (gn, GTOL))
    if abs(E - CLAIM) > ETOL: print("energy does not match the claim"); ok = False
    if MODE == "below" and CELL - E < D("1e-6"): print("not below the table cell by 1e-6"); ok = False
    if MODE == "mismatch" and abs(CELL - E) <= D("1e-6"): print("table cell is reproduced within 1e-6"); ok = False
    if gn >= GTOL: print("tangent gradient too large"); ok = False
    return ok

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
