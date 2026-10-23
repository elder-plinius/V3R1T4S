#!/usr/bin/env python3
"""Check object/651.txt against the-record-we-beat/table_rows.tsv.

Stdlib Decimal at 50 digits. Last line is PASS or FAIL.
"""
import os
import sys
from decimal import Decimal, localcontext

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
MARGIN = Decimal("1e-10")
AGREE = Decimal("1e-48")


def sig_digits(tok):
    mant = tok.lower().split("e")[0].replace("-", "").replace("+", "").replace(".", "")
    return len(mant)


def main():
    with open(os.path.join(ROOT, "the-record-we-beat", "table_rows.tsv")) as f:
        header = f.readline().split()
        if header[:4] != ["N", "cos", "needs_more_optimization", "star"]:
            print("FAIL")
            return 1
        parts = f.readline().split()
        if len(parts) != 4:
            print("FAIL")
            return 1
        n = int(parts[0])
        cos = Decimal(parts[1])
        needs = int(parts[2])
        star = int(parts[3])
    path = os.path.join(ROOT, "object", "651.txt")
    rows = []
    total = Decimal(0)
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            toks = line.split(",")
            if len(toks) != 25:
                print("FAIL")
                return 1
            if any(sig_digits(t) < 20 for t in toks):
                print("FAIL")
                return 1
            for t in toks:
                total += Decimal(t)
            rows.append(toks)
    if len(rows) != 651 or n != 651:
        print("FAIL")
        return 1
    with localcontext() as ctx:
        ctx.prec = 50
        unit = []
        for toks in rows:
            r = [Decimal(t) for t in toks]
            s = sum((x * x for x in r), Decimal(0)).sqrt()
            if s == 0:
                print("FAIL")
                return 1
            unit.append([x / s for x in r])
        best = Decimal("-1")
        for i in range(651):
            ui = unit[i]
            for j in range(i + 1, 651):
                ip = sum((a * b for a, b in zip(ui, unit[j])), Decimal(0))
                if ip > best:
                    best = ip
        exp = Decimal(open(os.path.join(HERE, "expected_c.txt")).read().strip())
        exp_sum = Decimal(open(os.path.join(HERE, "expected_sum.txt")).read().strip())
        delta = cos - best
        ok = (
            delta >= MARGIN
            and needs == 0
            and star == 0
            and abs(best - exp) <= AGREE
            and total == exp_sum
        )
        print("N=651 d=25")
        print("c*=" + format(best, "f"))
        print("delta=" + format(delta, "f"))
        print("coord_sum=" + format(total, "f"))
        print("needs_more_optimization=%d star=%d" % (needs, star))
        print("PASS" if ok else "FAIL")
        return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
