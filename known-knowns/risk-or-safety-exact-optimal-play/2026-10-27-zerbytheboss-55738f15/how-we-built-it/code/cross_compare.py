#!/usr/bin/env python3
"""cross_compare.py -- independently cross-compare Extender lens and Contrarian lens outputs."""
import os
import sys
from fractions import Fraction

def load_vals(path):
    d = {}
    for line in open(path):
        p = line.strip().split()
        if len(p) == 2:
            d[int(p[0])] = Fraction(p[1])
    return d

def load_bfile(path):
    d = {}
    for line in open(path):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        p = line.split()
        if len(p) == 2:
            d[int(p[0])] = int(p[1])
    return d

def main():
    root = os.path.dirname(os.path.abspath(__file__))
    ext_path = os.path.join(root, "extender", "values.txt")
    con_path = os.path.join(root, "contrarian", "values_contrarian.txt")
    data_dir = os.path.join(os.path.dirname(root), "data")

    ext_vals = load_vals(ext_path)
    con_vals = load_vals(con_path)

    print(f"Loaded {len(ext_vals)} extender values and {len(con_vals)} contrarian values.")

    mismatches = []
    for n in range(1, 46):
        if n not in ext_vals or n not in con_vals:
            mismatches.append(f"n={n} missing from one of the solvers")
            continue
        v1 = ext_vals[n]
        v2 = con_vals[n]
        if v1 != v2:
            mismatches.append(f"n={n} solver mismatch: ext={v1} con={v2}")

    print(f"Extender vs Contrarian comparison across n=1..45: {len(mismatches)} mismatches")
    if mismatches:
        for m in mismatches[:10]:
            print(" ", m)
        sys.exit(1)

    # Check OEIS n=1..15
    oeis_num = load_bfile(os.path.join(data_dir, "b387261.txt"))
    oeis_den = load_bfile(os.path.join(data_dir, "b387262.txt"))
    oeis_mismatches = []
    for n in range(1, 16):
        v = ext_vals[n]
        if n not in oeis_num or n not in oeis_den:
            oeis_mismatches.append(f"n={n} missing from OEIS b-files")
            continue
        exp = Fraction(oeis_num[n], oeis_den[n])
        if v != exp or v.numerator != oeis_num[n] or v.denominator != oeis_den[n]:
            oeis_mismatches.append(f"n={n} OEIS mismatch: mine={v} oeis={exp}")

    print(f"OEIS n=1..15 comparison: {len(oeis_mismatches)} mismatches")

    # Check known-knowns n=16..30
    kk_vals = load_vals(os.path.join(data_dir, "values_16_30.txt"))
    kk_mismatches = []
    for n in range(16, 31):
        v = ext_vals[n]
        if n not in kk_vals:
            kk_mismatches.append(f"n={n} missing from values_16_30.txt")
            continue
        exp = kk_vals[n]
        if v != exp or v.numerator != exp.numerator or v.denominator != exp.denominator:
            kk_mismatches.append(f"n={n} known-knowns mismatch: mine={v} kk={exp}")

    print(f"Known-knowns n=16..30 comparison: {len(kk_mismatches)} mismatches")

    if not mismatches and not oeis_mismatches and not kk_mismatches:
        print("ALL_CROSS_CHECKS_PASS: Both independent solvers agree on all 45 terms; n=1..15 match OEIS; n=16..30 match known-knowns.")
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
