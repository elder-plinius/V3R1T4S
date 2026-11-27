#!/usr/bin/env python3
"""Enriches a 3-column raw certificate TSV with exact reduced rational fractions (column 4) and canonical sorting."""
import sys
from fractions import Fraction

PRIMES = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59]


def exact_distortion_loss(ex, k0, ms):
    r = len(ex)
    prod_base = Fraction(1, 1)
    sum_base = Fraction(0, 1)
    dist = {1: Fraction(1, 1)}
    for m in range(k0):
        p, e = PRIMES[m], ex[m]
        pe = p ** e
        s_m = ((p - 2) * pe + 1) // (p - 1)
        th = Fraction((pe - 1) // (p - 1), s_m)
        prod_base *= (1 + th)
        sum_base += th
        tails = [Fraction(1, 1)] + [Fraction(p ** (e - t), s_m) for t in range(1, e + 1)] + [Fraction(0, 1)]
        ndist = {}
        for t in range(e + 1):
            pr = tails[t] - tails[t + 1]
            if pr > 0:
                dv = 1 + t
                for mv, pv in dist.items():
                    ndist[mv * dv] = ndist.get(mv * dv, Fraction(0, 1)) + pv * pr
        dist = ndist
    tot = prod_base - 1 - sum_base
    for i in range(k0, r):
        p, e = PRIMES[i], ex[i]
        pe = p ** e
        rho = Fraction(pe - 1, (p - 1) * pe)
        c_cap = Fraction(ms[i - k0], 32)
        delta = 1 - Fraction(1, c_cap)
        loss_i = Fraction(0, 1)
        for mv, pv in dist.items():
            alpha = rho * mv
            if alpha > delta:
                loss_i += pv * c_cap * (alpha - delta)
        tot += loss_i
        if i < r - 1:
            tails = [Fraction(1, 1)] + [min(Fraction(1, 1), c_cap / (p ** t)) for t in range(1, e + 1)] + [Fraction(0, 1)]
            ndist = {}
            for t in range(e + 1):
                pr = tails[t] - tails[t + 1]
                if pr > 0:
                    dv = 1 + t
                    for mv, pv in dist.items():
                        ndist[mv * dv] = ndist.get(mv * dv, Fraction(0, 1)) + pv * pr
            dist = ndist
    return tot


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: enrich_exact_fractions.py raw.tsv out.tsv")
    rows = []
    with open(sys.argv[1], "r", encoding="utf-8") as fh:
        next(fh)
        for line in fh:
            ex_s, k0_s, ms_s = line.strip().split("\t")
            ex = tuple(int(x) for x in ex_s.split(","))
            k0 = int(k0_s)
            ms = tuple(int(x) for x in ms_s.split(","))
            tot = exact_distortion_loss(ex, k0, ms)
            assert tot < 1
            rows.append((ex_s, k0_s, ms_s, f"{tot.numerator}/{tot.denominator}"))
    rows.sort(key=lambda r: tuple(int(x) for x in r[0].split(",")))
    with open(sys.argv[2], "w", encoding="utf-8") as out:
        out.write("exponents\tk0\tm_over_32\texact_upper_bound\n")
        for ex_s, k0_s, ms_s, rat_s in rows:
            out.write(f"{ex_s}\t{k0_s}\t{ms_s}\t{rat_s}\n")


if __name__ == "__main__":
    main()
