#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Fast checker for the A395265 witnesses.

Every positive difference of each witness is counted in pure Python. The
witnesses are upper bounds (a diameter that exists). That no smaller diameter
exists is the saved exhaustive record named in the panel. A changed witness
fails this script.
Last line is PASS or FAIL.
"""
import json, os, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
R20 = [0, 1, 2, 3, 8, 11, 14, 16, 20, 24, 29, 31, 36, 40, 43, 46, 50, 54, 55, 56]
R21 = [0, 1, 2, 3, 8, 12, 17, 19, 23, 27, 30, 35, 37, 40, 43, 49, 52, 56, 60, 61, 62]
G = 5

def fail(msg):
    print(msg)
    print("FAIL")
    sys.exit(1)

def check(w, n, diameter, label):
    if w != (R20 if n == 20 else R21):
        fail("%s is not the attested witness" % label)
    if len(w) != n or len(set(w)) != n or w != sorted(w):
        fail("%s: marks are not %d sorted distinct integers" % (label, n))
    if w[0] != 0 or w[-1] != diameter:
        fail("%s: diameter is not %d" % (label, diameter))
    counts = Counter(b - a for i, a in enumerate(w) for b in w[i + 1:])
    worst = max(counts.values())
    if worst > G:
        fail("%s: a difference occurs %d times" % (label, worst))
    print("OK  %s  marks %d  diameter %d  max multiplicity %d" % (label, n, diameter, worst))

def main():
    path = os.path.join(ROOT, "object", "rulers.json")
    try:
        obj = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        fail("object/rulers.json: %s" % e)
    if obj.get("sequence") != "A395265" or obj.get("multiplicity") != 5:
        fail("sequence id or multiplicity is not the attested claim")
    if obj.get("a20") != 56 or obj.get("a21") != 62:
        fail("claimed diameters are not 56 and 62")
    check(obj.get("witness20"), 20, 56, "a(20)")
    check(obj.get("witness21"), 21, 62, "a(21)")
    print("PASS")

if __name__ == "__main__":
    main()
