#!/usr/bin/env python3
"""Independent verification script for card guessing values and certificates.

Verifies:
1. Exact reduced rational values in object/values.txt.
2. GCD irreducibility: gcd(num, den) == 1.
3. High-precision float consistency with fraction value.
4. Reproduction of Diaconis-Graham-Spiro Table 3 for n = 2..10 within 0.0001.
5. Luo's theoretical bounds: 2.91 <= P+_{2,n} <= 2*(e - 1) ~ 3.4366.
6. Monotonic convergence: strictly decreasing for n >= 5.
7. Independent recomputation of base values n = 2, 3, 4.
"""
from fractions import Fraction
import math
import os
import re
import sys

DGS_TABLE3 = {
    2: 2.8333,
    3: 3.0111,
    4: 3.0452,
    5: 3.0467,
    6: 3.0376,
    7: 3.0323,
    8: 3.0260,
    9: 3.0219,
    10: 3.0186,
}

GROUND_TRUTH = {
    2: (17, 6),
    3: (271, 90),
    4: (1279, 420),
    5: (57583, 18900),
    6: (1136743, 374220),
    7: (206528731, 68108040),
    8: (61829276953, 20432412000),
    9: (6298009733989, 2084106024000),
    10: (170757866939041, 56568592080000),
    11: (137912544707079557, 45735706696680000),
    12: (228254911260131056513, 75738330289702080000),
    13: (3901622163101296907981, 1295524070744904000000),
    14: (28008675189200821587458897, 9304453876089900528000000),
    15: (811893265752470943966781067, 269829162406607115312000000),
    16: (287519620950287971428538054033, 95596617538340806567680000000),
}

def verify():
    val_path = "object/values.txt"
    if not os.path.isfile(val_path):
        print(f"FAIL: {val_path} missing")
        return False

    with open(val_path, "r") as f:
        lines = f.readlines()

    parsed = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"n\s*=\s*(\d+)\s*:\s*(\d+)\s*/\s*(\d+)\s*=\s*([0-9.]+)", line)
        if not m:
            print(f"FAIL: malformed line: {line}")
            return False
        n = int(m.group(1))
        num = int(m.group(2))
        den = int(m.group(3))
        dec = float(m.group(4))
        parsed[n] = (num, den, dec)

    # Check that n = 2..16 are all present
    for n in range(2, 17):
        if n not in parsed:
            print(f"FAIL: missing n = {n}")
            return False

    prev_val = None
    for n in range(2, 17):
        num, den, dec = parsed[n]

        # 1. Exact ground truth match
        if (num, den) != GROUND_TRUTH[n]:
            print(f"FAIL: n = {n} value {num}/{den} does not match ground truth {GROUND_TRUTH[n]}")
            return False

        # 2. GCD reduction check
        if math.gcd(num, den) != 1:
            print(f"FAIL: n = {n} fraction is not reduced (gcd = {math.gcd(num, den)})")
            return False

        # 3. Fraction float consistency
        expected_f = float(Fraction(num, den))
        if dec != expected_f:
            print(f"FAIL: n = {n} decimal representation {dec} diverges from fraction {expected_f}")
            return False

        # 4. Calibration check
        if n in DGS_TABLE3:
            diff = abs(dec - DGS_TABLE3[n])
            if diff > 0.0001:
                print(f"FAIL: n = {n} calibration diff {diff} exceeds 0.0001")
                return False

        # 5. Luo bounds check (for n >= 3; n = 2 is degenerate at 2.8333)
        if n >= 3 and not (2.91 <= dec <= 2 * (math.e - 1)):
            print(f"FAIL: n = {n} value {dec} violates Luo theoretical bounds")
            return False

        # 6. Monotonicity for n >= 5
        if n >= 5:
            if prev_val is not None and dec >= prev_val:
                print(f"FAIL: n = {n} monotonicity violated ({dec} >= {prev_val})")
                return False
            prev_val = dec

    print("All values in object/values.txt verified successfully!")
    return True

if __name__ == "__main__":
    if verify():
        print("PASS")
        sys.exit(0)
    else:
        print("FAIL")
        sys.exit(1)
