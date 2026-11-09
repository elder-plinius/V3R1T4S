#!/usr/bin/env python3
"""Independent checker for hsp4 packings (no numpy, no search code).
Usage: check.py <coords-file> <radius-table>
The coords file has '#' header lines, then N rows of 4 decimal coordinates.
r* = min( min_{i<j} |c_i - c_j| / 2 , 1 - max_i |c_i| ), evaluated in mpmath at 50 digits
directly from the decimal strings. Prints r*, the table value, the difference, and BEATEN
only if r* - table >= 1e-10 (target rule)."""
import sys
from mpmath import mp, mpf, sqrt, nstr
mp.dps = 50

def main(path, table_path):
    rows = []
    for line in open(path):
        s = line.strip()
        if not s or s.startswith('#'): continue
        parts = s.split()
        if len(parts) != 4: raise SystemExit(f'bad row: {s!r}')
        rows.append([mpf(p) for p in parts])
    n = len(rows)
    tab = None
    for line in open(table_path):
        p = line.split()
        if len(p) >= 2 and p[0] == str(n): tab = mpf(p[1])
    if tab is None: raise SystemExit(f'N={n} not in table')
    min_d2 = None
    for i in range(n):
        a = rows[i]
        for j in range(i + 1, n):
            b = rows[j]
            d2 = (a[0]-b[0])**2 + (a[1]-b[1])**2 + (a[2]-b[2])**2 + (a[3]-b[3])**2
            if min_d2 is None or d2 < min_d2: min_d2 = d2
    max_n2 = max(c[0]**2 + c[1]**2 + c[2]**2 + c[3]**2 for c in rows)
    half = sqrt(min_d2) / 2
    bnd = 1 - sqrt(max_n2)
    r = min(half, bnd)
    diff = r - tab
    ok = diff >= mpf('1e-10')
    print(f'N={n} r*={nstr(r, 25)} half_min_dist={nstr(half, 25)} 1-max_norm={nstr(bnd, 25)} '
          f'table={nstr(tab, 12)} diff={nstr(diff, 6)} {"BEATEN" if ok else "NOT_BEATEN"}')
    return ok

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2]) else 1)
