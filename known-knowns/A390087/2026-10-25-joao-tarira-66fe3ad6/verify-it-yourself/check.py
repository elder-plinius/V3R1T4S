#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Fast checker for the A390087 / A390085 witnesses.

Enumerates every nonempty proper subset of each witness (pure Python) and
checks the odd-zero-sum conditions. The exact minimality (no shorter index,
and the A390085 values between the witnesses) is the saved exhaustive record
named in the panel; this run checks that object/terms.json still carries that
attested table and that both witnesses meet the definition.
Last line is PASS or FAIL.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
W8 = [77, 75, 73, 71, 69, 67, -65, 63, -61, -59, -57, -55, -53, -51, -49, -45]
W9 = [95, 93, 91, 89, 87, 85, 83, -81, 79, -77, -75, -73, -71, -69, -67, -65, -63, -61]
A85 = [7] * 8 + [8] * 9 + [9]

def fail(msg):
    print(msg)
    print("FAIL")
    sys.exit(1)

def irreducible(w):
    n = len(w)
    # iterative subset sums of nonempty proper subsets, early exit on 0
    # 2^n masks; n is 16 or 18
    zero = False
    for mask in range(1, (1 << n) - 1):
        s = 0
        m = mask
        i = 0
        while m:
            if m & 1:
                s += w[i]
            m >>= 1
            i += 1
        if s == 0:
            zero = True
            break
    return not zero

def check_witness(w, length, k, label):
    if len(w) != length or len(set(w)) != length:
        fail("%s: expected %d distinct elements" % (label, length))
    if any(x % 2 == 0 for x in w):
        fail("%s: an element is even" % label)
    if sum(w) != 0:
        fail("%s: sum is not 0" % label)
    if max(abs(x) for x in w) != 2 * k - 1:
        fail("%s: max absolute value is not 2*%d-1" % (label, k))
    if not irreducible(w):
        fail("%s: a nonempty proper subset sums to 0" % label)
    print("OK  %s  length %d  k %d  irreducible" % (label, length, k))

def main():
    path = os.path.join(ROOT, "object", "terms.json")
    try:
        obj = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        fail("object/terms.json: %s" % e)
    if obj.get("sequence") != "A390087":
        fail("sequence id is not A390087")
    if obj.get("a8") != 39 or obj.get("a9") != 48:
        fail("claimed a(8) or a(9) is not the attested value")
    if obj.get("witness8") != W8 or obj.get("witness9") != W9:
        fail("a witness is not the attested set")
    if obj.get("A390085_from_31_to_48") != A85:
        fail("A390085(31) through A390085(48) is not the attested row")
    check_witness(obj["witness8"], 16, 39, "a(8) witness")
    check_witness(obj["witness9"], 18, 48, "a(9) witness")
    if obj["A390085_from_31_to_48"][8] != len(obj["witness8"]) // 2:
        fail("A390085(39) does not match half the a(8) witness length")
    if obj["A390085_from_31_to_48"][17] != len(obj["witness9"]) // 2:
        fail("A390085(48) does not match half the a(9) witness length")
    print("PASS")

if __name__ == "__main__":
    main()
