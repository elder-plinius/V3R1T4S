"""Independent checker (does not import the search code).

usage: python3 check.py result.txt [radius_table.txt]

result.txt: first line is a '#' header; then N lines of 4 decimal coordinates
(ball centres, container = unit 4-ball at the origin). r* is computed in
mpmath at 50 digits from the decimal strings with no tolerance:
    r* = min( min_{i<j} |c_i - c_j| / 2 , 1 - max_i |c_i| ).
"""
import sys, os
from mpmath import mp, mpf, sqrt

mp.dps = 50


def load(path):
    pts = []
    with open(path) as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            pts.append([mpf(t) for t in line.split()])
    return pts


def rstar(pts):
    n = len(pts)
    d = len(pts[0])
    assert all(len(p) == d for p in pts)
    m2 = None
    for i in range(n):
        pi = pts[i]
        for j in range(i + 1, n):
            pj = pts[j]
            s = mpf(0)
            for k in range(d):
                t = pi[k] - pj[k]
                s += t * t
            if m2 is None or s < m2:
                m2 = s
    maxn = max(sqrt(sum(c * c for c in p)) for p in pts)
    half = sqrt(m2) / 2
    return min(half, 1 - maxn), half, 1 - maxn


def table_value(path, n):
    with open(path) as fh:
        for line in fh:
            p = line.split()
            if len(p) >= 2 and p[0] == str(n):
                return mpf(p[1])
    raise KeyError(n)


if __name__ == "__main__":
    res = sys.argv[1]
    tab = sys.argv[2] if len(sys.argv) > 2 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "../../../data/packomania.com_hsp4_txt_radius.txt")
    pts = load(res)
    n = len(pts)
    r, half, gap = rstar(pts)
    rt = table_value(tab, n)
    diff = r - rt
    beaten = diff >= mpf("1e-10")
    print(f"N={n} d={len(pts[0])}")
    print(f"half_min_dist = {mp.nstr(half, 25)}")
    print(f"1 - max_norm  = {mp.nstr(gap, 25)}")
    print(f"r*            = {mp.nstr(r, 25)}")
    print(f"table         = {mp.nstr(rt, 13)}")
    print(f"r* - table    = {mp.nstr(diff, 6)}")
    print("BEATEN" if beaten else "NOT BEATEN")
