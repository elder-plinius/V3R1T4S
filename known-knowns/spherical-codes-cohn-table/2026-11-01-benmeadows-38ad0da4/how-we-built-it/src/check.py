"""Independent checker. Reads only a saved coordinate file and the stored table
(/plain snapshot). Pure mpmath at 50 digits; no numpy, no search code.
Usage: python check.py FILE [FILE ...]
Prints c* to 20 digits, minimal angle in degrees, table value, margin, and
BEATEN only if table - c* >= 1e-10."""
import sys, os
from mpmath import mp, mpf, sqrt, acos, degrees, nstr

mp.dps = 50
PLAIN = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "..", "data", "spherical-codes.org_plain")


def table_value(d, N):
    for line in open(PLAIN):
        p = line.strip().split(",")
        if len(p) >= 3 and p[0] == str(d) and p[1] == str(N):
            return p[2], len(p)
    return None, 0


def check(fn):
    pts = []
    for line in open(fn):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        pts.append([mpf(t) for t in s.split()])
    N, d = len(pts), len(pts[0])
    assert all(len(p) == d for p in pts), "ragged rows"
    unit = []
    for p in pts:
        n = sqrt(sum(x * x for x in p))
        unit.append([x / n for x in p])
    cstar = mpf(-2)
    for i in range(N):
        a = unit[i]
        for j in range(i + 1, N):
            b = unit[j]
            s = mp.fsum(a[k] * b[k] for k in range(d))
            if s > cstar:
                cstar = s
    tv, nf = table_value(d, N)
    margin = mpf(tv) - cstar if tv else None
    beaten = tv is not None and nf == 3 and margin >= mpf("1e-10")
    print(f"{os.path.basename(fn)} d={d} N={N} c*={nstr(cstar, 20)} "
          f"angle_deg={nstr(degrees(acos(cstar)), 15)} table={tv} "
          f"margin={nstr(margin, 6) if tv else 'na'} BEATEN={'yes' if beaten else 'no'}")
    return beaten


if __name__ == "__main__":
    for f in sys.argv[1:]:
        check(f)
