#!/usr/bin/env python3
"""Constructs the three finite Equation677 separation models (Fin7, Fin25, Fin55)
in object/separation_models.json from their algebraic formulas.
Python 3 standard library only.
"""
import json
import sys


def build_sep7():
    return [[(4 * x + y) % 7 for y in range(7)] for x in range(7)]


def build_sep25():
    def swap01(k):
        return 1 if k == 0 else (0 if k == 1 else k)

    def op5a(s, t):
        return (2 * s + 4 * t) % 5

    def op5b(s, t):
        return swap01(op5a(swap01(s), swap01(t)))

    def fn25(u, v):
        x1, s1 = divmod(u, 5)
        x2, s2 = divmod(v, 5)
        x3 = op5a(x1, x2)
        s3 = op5a(s1, s2) if x1 == x2 else op5b(s1, s2)
        return (5 * x3 + s3) % 25

    return [[fn25(u, v) for v in range(25)] for u in range(25)]


def build_sep55():
    qr11 = {1, 3, 4, 5, 9}

    def fn55(u, v):
        x1, s1 = divmod(u, 5)
        x2, s2 = divmod(v, 5)
        x3 = (10 * x1 + 2 * x2) % 11
        d = (x2 + 11 - (x1 % 11)) % 11
        if d == 0:
            s3 = (2 * s1 + 4 * s2) % 5
        elif d in qr11:
            s3 = s2 % 5
        else:
            s3 = (4 * s1 + 4 * s2) % 5
        return (5 * x3 + s3) % 55

    return [[fn55(u, v) for v in range(55)] for u in range(55)]


def main():
    out_path = sys.argv[1] if len(sys.argv) > 1 else "object/separation_models.json"
    data = {
        "Fin7": build_sep7(),
        "Fin25": build_sep25(),
        "Fin55": build_sep55(),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"Wrote {out_path} (Fin7 n=7, Fin25 n=25, Fin55 n=55)")


if __name__ == "__main__":
    main()
