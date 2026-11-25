"""Shared machinery: grid lines in [0,n)^3 with >= 3 points, admissibility checker."""
import sys
from math import gcd

def enumerate_lines(n):
    """All lines in the n x n x n grid containing >= 3 grid points.
    Returns (lines, point_lines) where lines is a list of frozensets of point ids
    and point_lines[p] is the list of line indices through point p.
    Point id p = x + n*y + n*n*z."""
    dirs = []
    B = n - 1
    for dx in range(-B, B + 1):
        for dy in range(-B, B + 1):
            for dz in range(-B, B + 1):
                if (dx, dy, dz) == (0, 0, 0):
                    continue
                if gcd(gcd(abs(dx), abs(dy)), abs(dz)) != 1:
                    continue
                # canonical direction: first nonzero positive
                for c in (dx, dy, dz):
                    if c != 0:
                        if c < 0:
                            break
                        break
                else:
                    continue
                if c < 0:
                    continue
                dirs.append((dx, dy, dz))
    lines = []
    for x in range(n):
        for y in range(n):
            for z in range(n):
                for (dx, dy, dz) in dirs:
                    # start point: no earlier grid point on this line
                    px, py, pz = x - dx, y - dy, z - dz
                    if 0 <= px < n and 0 <= py < n and 0 <= pz < n:
                        continue
                    pts = []
                    cx, cy, cz = x, y, z
                    while 0 <= cx < n and 0 <= cy < n and 0 <= cz < n:
                        pts.append(cx + n * cy + n * n * cz)
                        cx += dx; cy += dy; cz += dz
                    if len(pts) >= 3:
                        lines.append(tuple(pts))
    # dedupe: (dir, start) is unique so no dupes expected, but be safe
    lines = sorted(set(lines))
    point_lines = [[] for _ in range(n ** 3)]
    for li, pts in enumerate(lines):
        for p in pts:
            point_lines[p].append(li)
    return lines, point_lines

def is_admissible(pts, lines, n):
    """pts: iterable of point ids. Returns (ok, bad_line) with every line <= 2 pts."""
    s = set(pts)
    for pts_on_line in lines:
        c = sum(1 for p in pts_on_line if p in s)
        if c > 2:
            return False, pts_on_line
    return True, None

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    lines, pl = enumerate_lines(n)
    print(f"n={n}: {len(lines)} lines of length>=3; total point-line incidences {sum(len(l) for l in pl)}")
