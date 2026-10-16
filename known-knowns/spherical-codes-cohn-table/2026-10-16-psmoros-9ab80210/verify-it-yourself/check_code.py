#!/usr/bin/env python3
"""Standalone checker for this package (Python standard library only).

Definition (bank target spherical-codes-cohn-table): normalise each of the N vectors to unit length; c* is the
maximum pairwise inner product (the cosine of the minimal angle); the claim needs c* lower than the table's 12-decimal
cosine for (d, N) by at least 1e-10, with every coordinate written to at least 20 significant digits.

Method: every coordinate is read as an exact decimal; norms are computed exactly and their square roots to 70
significant digits (decimal module); the inner product of EVERY pair of normalised vectors is computed at 70 digits
(no floating-point screen). The table cosine and the object's sha256 are read from the-record-we-beat/cell.json.
Run from the package folder:  python3 -I -B verify-it-yourself/check_code.py
"""
import decimal
import hashlib
import json
import sys
from decimal import Decimal

ctx = decimal.getcontext()
ctx.prec = 70


def main():
    cell = json.load(open("the-record-we-beat/cell.json"))
    d, N = int(cell["d"]), int(cell["N"])
    path = cell["file"]
    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    ok = True
    print("object", path, "sha256", sha)
    if sha != cell["sha256"]:
        print("FAIL: sha256 differs from cell.json", cell["sha256"])
        ok = False
    rows = [l.split() for l in raw.decode("ascii").splitlines() if l.strip()]
    if len(rows) != N or any(len(r) != d for r in rows):
        print("FAIL: expected %d points with %d coordinates each" % (N, d))
        print("FAIL")
        return 1
    digits = min(len(t.lower().split("e")[0].lstrip("+-").replace(".", "").lstrip("0") or "0") for r in rows for t in r)
    print("points", N, "dimension", d, "minimum significant digits", digits)
    if digits < 20:
        print("FAIL: fewer than 20 significant digits")
        ok = False
    X = [[Decimal(t) for t in r] for r in rows]
    U = []
    for v in X:
        n2 = sum(x * x for x in v)
        if not n2 > 0:
            print("FAIL: zero vector")
            print("FAIL")
            return 1
        inv = 1 / n2.sqrt()
        U.append([x * inv for x in v])
    best, arg = Decimal(-2), None
    for i in range(N):
        ui = U[i]
        for j in range(i + 1, N):
            s = sum(a * b for a, b in zip(ui, U[j]))
            if s > best:
                best, arg = s, (i, j)
    print("pairs checked", N * (N - 1) // 2)
    print("c* =", format(best.quantize(Decimal(10) ** -30)), "at points", arg)
    table = Decimal(cell["table_cosine"])
    gain = table - best
    print("table cosine", cell["table_cosine"], "(%s, fetched %s)" % (cell["table_url"], cell["table_fetched_utc"]))
    print("gain = table - c* =", format(gain.quantize(Decimal(10) ** -20)))
    if not gain >= Decimal("1e-10"):
        print("FAIL: gain below 1e-10")
        ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
