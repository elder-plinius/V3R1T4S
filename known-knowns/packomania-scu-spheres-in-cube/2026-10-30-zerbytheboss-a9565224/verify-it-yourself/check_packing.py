#!/usr/bin/env python3
import sys
import os
from mpmath import mp

def check():
    mp.dps = 50
    pkg_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obj_path = os.path.join(pkg_dir, "object", "candidate_scu344_solution.txt")

    if not os.path.isfile(obj_path):
        print(f"FAIL: Object file missing: {obj_path}")
        return False

    with open(obj_path, "r") as f:
        lines = [l.strip() for l in f if l.strip() and not l.startswith("#")]

    pts = []
    try:
        for l in lines[1:]:
            parts = l.split()
            if len(parts) >= 4 and parts[0].isdigit():
                pts.append((mp.mpf(parts[1]), mp.mpf(parts[2]), mp.mpf(parts[3])))
    except Exception as e:
        print(f"FAIL: Could not parse coordinates: {e}")
        return False

    if len(pts) != 344:
        print(f"FAIL: Expected 344 sphere centers, found {len(pts)}")
        return False

    half = mp.mpf("0.5")
    # Cube containment
    min_wall = min(half - max(abs(x), abs(y), abs(z)) for x, y, z in pts)
    if min_wall <= 0:
        print(f"FAIL: Point violates cube containment: min_wall={min_wall}")
        return False

    # Pairwise distances
    min_dist = mp.inf
    for i in range(len(pts)):
        xi, yi, zi = pts[i]
        for j in range(i + 1, len(pts)):
            xj, yj, zj = pts[j]
            d = mp.sqrt((xi - xj)**2 + (yi - yj)**2 + (zi - zj)**2) / 2
            if d < min_dist:
                min_dist = d

    r_star = min(min_wall, min_dist)
    table_r = mp.mpf("0.075110834623")
    diff = r_star - table_r

    print(f"Checked N=344 spheres in cube.")
    print(f"Achieved feasible radius r*: {str(r_star)[:35]}")
    print(f"Live table radius:          {str(table_r)}")
    print(f"Margin:                     {float(diff):.12e}")

    if diff < mp.mpf("1e-11"):
        print(f"FAIL: Margin {diff} is less than required 1e-11")
        return False

    return True

if __name__ == "__main__":
    if check():
        print("PASS")
        sys.exit(0)
    else:
        print("FAIL")
        sys.exit(1)
