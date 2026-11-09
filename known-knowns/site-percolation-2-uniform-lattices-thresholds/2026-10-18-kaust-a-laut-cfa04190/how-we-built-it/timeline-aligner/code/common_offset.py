"""PREREG.v5 addition 2: common-offset kill rule for the site Monte Carlo, computed from saved outputs only.

Inputs: the fss_mc.py output of kagome site (60-block one look) and of square site (PREREG.v3 A), and the
triangular_test.py output (L = 16, 32, 64). From fss_mc.py the line starting "primary" gives p_MC and sigma_MC;
from the triangular test each "p_L ... +- ..." line gives p_L and sigma_L.
Offsets d_i = p_i - exact_i; D = sum(d_i / s_i^2) / sum(1 / s_i^2); sigma_D = 1 / sqrt(sum(1 / s_i^2)).
Verdict: STOP (the Monte Carlo line stops for every lattice) if |D| > 3 sigma_D, else PASS.
Written 2026-10-17 before any input that decides it exists (the triangular input is already seen, PREREG.v5).

usage: python common_offset.py <kagome fss output> <square fss output> <triangular test output>
"""
import math
import re
import sys

KAGOME = 1 - 2 * math.sin(math.pi / 18)
SQUARE = 0.59274605079210


def primary(path):
    for line in open(path):
        m = re.match(r"\s*primary.*p_MC ([0-9.]+) \+- ([0-9.e+-]+)", line)
        if m:
            return float(m.group(1)), float(m.group(2))
    raise SystemExit("no 'primary ... p_MC' line in %s" % path)


def triangular(path):
    out = []
    for line in open(path):
        m = re.search(r"L\s+(\d+)x\s*(\d+).*p_L ([0-9.]+) \+- ([0-9.e+-]+)", line)
        if m:
            out.append(("triangular L=%s" % m.group(1), float(m.group(3)), float(m.group(4)), 0.5))
    if len(out) != 3:
        raise SystemExit("expected 3 triangular sizes in %s, found %d" % (path, len(out)))
    return out


def main():
    k, s, t = sys.argv[1:4]
    rows = [("kagome site", *primary(k), KAGOME), ("square site", *primary(s), SQUARE)] + triangular(t)
    num = den = 0.0
    for name, p, sig, ex in rows:
        d = p - ex
        num += d / sig ** 2
        den += 1 / sig ** 2
        print("%-16s p %.10f +- %.2e  exact %.12f  offset %+.3e (%+.2f sigma)" % (name, p, sig, ex, d, d / sig))
    D, sD = num / den, den ** -0.5
    print("D %+.3e +- %.3e (%+.2f sigma) -> %s" % (D, sD, D / sD, "STOP" if abs(D) > 3 * sD else "PASS"))


if __name__ == "__main__":
    main()
