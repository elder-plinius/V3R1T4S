#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Fast checker for the A396618 term list.

Recomputes a(2) through a(19) from the definition with count.c (exact integer
square root, 0 counts as a square) and requires every term in object/terms.json
to equal the attested list. a(22) through a(25) are not re-enumerated here;
those totals are the saved full counts named in the panel.
Last line is PASS or FAIL.
"""
import json, os, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXPECTED = [4, 3, 4, 8, 26, 70, 206, 674, 2032, 6431, 20096, 63708, 200646,
            634782, 2005025, 6341137, 20044802, 63389326, 200432444, 633827657,
            2004269529, 6338072189, 20042521382, 63380064097, 200424655855]

def fail(msg):
    print(msg)
    print("FAIL")
    sys.exit(1)

def main():
    path = os.path.join(ROOT, "object", "terms.json")
    try:
        obj = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        fail("object/terms.json: %s" % e)
    if obj.get("sequence") != "A396618":
        fail("sequence id is not A396618")
    got = obj.get("a")
    if not isinstance(got, dict):
        fail("object has no term map")
    for n, exp in enumerate(EXPECTED, 1):
        if got.get(str(n)) != exp:
            fail("a(%d) object=%s attested=%d" % (n, got.get(str(n)), exp))
    if set(got) != set(str(i) for i in range(1, 26)):
        fail("term map is not exactly a(1) through a(25)")
    src = os.path.join(HERE, "count.c")
    fd, binpath = tempfile.mkstemp(prefix="a396618-count-")
    os.close(fd)
    try:
        c = subprocess.run(["gcc", "-O2", "-o", binpath, src, "-lm"],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if c.returncode != 0:
            fail("count.c did not compile")
        for n in range(2, 20):
            out = subprocess.run([binpath, str(n)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if out.returncode != 0:
                fail("counter failed for n=%d" % n)
            try:
                val = int(out.stdout.decode().strip().split()[-1])
            except ValueError:
                fail("counter output for n=%d was not an integer" % n)
            print("a(%d) = %d  attested %d  %s" % (n, val, EXPECTED[n - 1], "OK" if val == EXPECTED[n - 1] else "MISMATCH"))
            if val != EXPECTED[n - 1]:
                fail("recomputed a(%d) disagrees with the attested term" % n)
    finally:
        try:
            os.remove(binpath)
        except OSError:
            pass
    print("a(20) through a(25) match the attested list (full counts are the saved logs, not this run)")
    print("PASS")

if __name__ == "__main__":
    main()
