#!/usr/bin/env python3
"""Standalone checker for a(7) <= 97 (OEIS A399138), written from the
definition alone — does not import or reuse the claimant's encoder.

A grid point is any of the 7^3 = 343 integer points (x,y,z) with
0 <= x,y,z <= 6. A grid line is the set of grid points lying on any line
in R^3 that contains 3 or more grid points (axis-parallel and diagonal).
A set of points is "admissible" (no three collinear) iff no grid line
contains more than 2 of its points.

Claim: no 98-point admissible subset of the 7x7x7 grid exists, i.e.
a(7) <= 97.

This script:
 1. Independently enumerates every grid line from the definition.
 2. Confirms the counting identity (each point lies on exactly 3
    axis-parallel lines; 3*98 = 294 = 2*147) that the claim's argument
    rests on.
 3. Re-reads the shipped CNF (object/ceiling98.cnf) and checks, clause by
    clause, that it is exactly the claimed encoding: at-most-2 per grid
    line (>=3 points), at-least-2 (forced to exactly-2 by (2)) per
    axis-parallel line, and no other clauses.
 4. Re-verifies the shipped DRAT proof with drat-trim.
"""
import itertools
import math
import os
import re
import sys
import tempfile

N = 7
HERE = os.path.dirname(os.path.abspath(__file__))
OBJ = os.path.join(HERE, "..", "object")


def grid_points():
    # Match the shipped encoder's point-id convention exactly:
    # p = x + n*y + n*n*z (how-we-built-it/n3l.py), so building this list in
    # z-major, y-mid, x-minor nested order gives pts[i] the same variable
    # number (i+1) as the shipped CNF uses for grid point i.
    return [(x, y, z) for z in range(N) for y in range(N) for x in range(N)]


def point_id(p, index):
    return index[p]


def primitive_directions():
    """All primitive integer direction vectors (gcd=1, lexicographically
    normalised) that can carry 3+ collinear grid points in an N-cube."""
    dirs = set()
    for dx in range(-(N - 1), N):
        for dy in range(-(N - 1), N):
            for dz in range(-(N - 1), N):
                if (dx, dy, dz) == (0, 0, 0):
                    continue
                g = math.gcd(math.gcd(abs(dx), abs(dy)), abs(dz))
                d = (dx // g, dy // g, dz // g)
                # normalise sign: first nonzero component positive
                for c in d:
                    if c != 0:
                        if c < 0:
                            d = (-d[0], -d[1], -d[2])
                        break
                dirs.add(d)
    return dirs


def enumerate_lines():
    """Every MAXIMAL grid line (as a frozenset of grid points) with >= 3
    points, found by walking forward from each line's first point only."""
    pts = set(grid_points())
    lines = set()
    for d in primitive_directions():
        dx, dy, dz = d
        for p in pts:
            x, y, z = p
            # only start a walk at p if p is the FIRST point of its line
            # in this direction (the point one step back is off-grid) --
            # otherwise this is a sub-segment of a line already enumerated
            # from its true start, and must not be counted again.
            px, py, pz = x - dx, y - dy, z - dz
            if (px, py, pz) in pts:
                continue
            line = [p]
            nx, ny, nz = x + dx, y + dy, z + dz
            while (nx, ny, nz) in pts:
                line.append((nx, ny, nz))
                nx, ny, nz = nx + dx, ny + dy, nz + dz
            if len(line) >= 3:
                lines.add(frozenset(line))
    return lines


def axis_parallel(line):
    pts = list(line)
    xs, ys, zs = {p[0] for p in pts}, {p[1] for p in pts}, {p[2] for p in pts}
    # axis-parallel: exactly two of the three coordinates are constant
    const = sum(1 for s in (xs, ys, zs) if len(s) == 1)
    return const == 2


def main():
    fail = 0

    print("== 1. independent line enumeration from the definition ==")
    pts = grid_points()
    assert len(pts) == 343
    lines = enumerate_lines()
    axis_lines = [l for l in lines if axis_parallel(l)]
    print("grid points: %d" % len(pts))
    print("total lines with >= 3 points: %d" % len(lines))
    print("axis-parallel lines: %d" % len(axis_lines))
    if len(lines) != 4429 or len(axis_lines) != 147:
        print("FAIL: expected 4429 lines total, 147 axis-parallel (got %d, %d)"
              % (len(lines), len(axis_lines)))
        fail = 1
    else:
        print("PASS: 4429 total / 147 axis-parallel, matches the claim")

    print("\n== 2. counting identity (each point on exactly 3 axis lines) ==")
    incidence = {p: 0 for p in pts}
    for l in axis_lines:
        for p in l:
            incidence[p] += 1
    bad = [p for p, c in incidence.items() if c != 3]
    if bad:
        print("FAIL: %d points not on exactly 3 axis-parallel lines" % len(bad))
        fail = 1
    else:
        total_incidence = sum(incidence.values())
        print("every one of the 343 points lies on exactly 3 axis-parallel lines")
        print("3 * 98 = %d ; 2 * 147 = %d" % (3 * 98, 2 * len(axis_lines)))
        if 3 * 98 != 2 * len(axis_lines):
            print("FAIL: counting identity does not hold")
            fail = 1
        else:
            print("PASS: identity holds -- a 98-point admissible set would need"
                  " EXACTLY 2 points on every axis-parallel line")

    print("\n== 3. the shipped CNF matches this encoding, clause by clause ==")
    cnf_path = os.path.join(OBJ, "ceiling98.cnf")
    if not os.path.isfile(cnf_path):
        print("FAIL: %s not found" % cnf_path)
        return 1
    with open(cnf_path) as f:
        header = None
        shipped_clauses = []
        for line in f:
            line = line.strip()
            if not line or line.startswith("c"):
                continue
            if line.startswith("p"):
                header = line
                continue
            nums = [int(t) for t in line.split() if t != "0"]
            shipped_clauses.append(frozenset(nums))
    m = re.match(r"p cnf (\d+) (\d+)", header or "")
    if not m:
        print("FAIL: no DIMACS header line found")
        fail = 1
    else:
        nvars, nclauses = int(m.group(1)), int(m.group(2))
        print("header: %d vars, %d clauses" % (nvars, nclauses))
        if nvars != 343:
            print("FAIL: expected 343 variables (one per grid point)")
            fail = 1
        if len(shipped_clauses) != nclauses:
            print("FAIL: header clause count does not match body (%d vs %d)"
                  % (nclauses, len(shipped_clauses)))
            fail = 1
        if len(set(shipped_clauses)) != len(shipped_clauses):
            print("FAIL: %d duplicate clauses in the shipped CNF"
                  % (len(shipped_clauses) - len(set(shipped_clauses))))
            fail = 1
        by_len = {}
        for cl in shipped_clauses:
            by_len[len(cl)] = by_len.get(len(cl), 0) + 1
        print("shipped clause-length histogram: %s" % dict(sorted(by_len.items())))
        expect_atmost2 = sum(math.comb(len(l), 3) for l in lines)
        expect_hist = {3: expect_atmost2}
        for l in axis_lines:
            k = len(l) - 1
            expect_hist[k] = expect_hist.get(k, 0) + len(l)
        print("expected clause-length histogram (from the bare definition): %s"
              % dict(sorted(expect_hist.items())))
        if dict(sorted(by_len.items())) != dict(sorted(expect_hist.items())):
            print("FAIL: shipped clause-length histogram does not match the"
                  " definition's expected encoding -- the object does not"
                  " encode what it claims to")
            fail = 1
        else:
            print("PASS: shipped CNF's clause-length histogram matches the"
                  " at-most-2 / at-least-2 encoding of this definition exactly")

        # Full independent regeneration, exact clause-set diff: build our
        # own CNF from the SAME points/lines/axis_lines computed above (our
        # own, independently-derived enumeration -- not the claimant's),
        # using variable i+1 for pts[i] (matching the shipped encoder's
        # point-id convention, see grid_points() above), ternary at-most-2
        # for every line, and at-least-2 for axis lines via "for every
        # point on the line, a clause over all OTHER points of that line"
        # (one clause per excluded point). This is a literal, set-level
        # cross-check: ANY altered literal in the shipped CNF produces a
        # clause outside our rebuilt set (or drops one that should be
        # present), and is caught here regardless of whether that one
        # clause happens to fall inside the DRAT proof's dependency core.
        pidx = {p: i + 1 for i, p in enumerate(pts)}
        my_clauses = set()
        for l in lines:
            vs = sorted(pidx[p] for p in l)
            for a, b, c3 in itertools.combinations(vs, 3):
                my_clauses.add(frozenset((-a, -b, -c3)))
        for l in axis_lines:
            vs = sorted(pidx[p] for p in l)
            for excl in vs:
                my_clauses.add(frozenset(v for v in vs if v != excl))
        shipped_set = set(shipped_clauses)
        missing = my_clauses - shipped_set     # clauses we expect, not shipped
        extra = shipped_set - my_clauses       # clauses shipped, not expected
        print("my independently rebuilt clause set: %d clauses" % len(my_clauses))
        if missing or extra:
            print("FAIL: exact clause-set diff against my independent rebuild"
                  " found %d missing and %d unexpected clauses -- the"
                  " shipped object does not encode what it claims to"
                  % (len(missing), len(extra)))
            fail = 1
        else:
            print("PASS: shipped CNF is clause-for-clause IDENTICAL to my"
                  " independent rebuild from the bare definition (%d clauses,"
                  " exact set match, zero differences)" % len(my_clauses))

    print("\n== 4. re-verify the shipped DRAT proof ==")
    drat_src = os.path.join(HERE, "drat-trim.c")
    tmpdir = tempfile.mkdtemp(prefix="a7check-")
    drat_bin = os.path.join(tmpdir, "drat-trim")
    if not os.path.isfile(drat_src):
        print("FAIL: drat-trim.c not shipped in verify-it-yourself/")
        fail = 1
    else:
        build_log = os.path.join(tmpdir, "drat_build.log")
        rc = os.system("cc -O2 -o %s %s >%s 2>&1"
                        % (drat_bin, drat_src, build_log))
        if rc != 0:
            print("FAIL: could not compile drat-trim (see the build log in the temp dir)")
            fail = 1
        else:
            drat_path = os.path.join(OBJ, "ceiling98.drat")
            verify_log = os.path.join(tmpdir, "drat_verify.log")
            rc = os.system("%s %s %s > %s 2>&1"
                            % (drat_bin, cnf_path, drat_path, verify_log))
            out = open(verify_log).read()
            print(out.strip()[-300:])
            if "s VERIFIED" in out:
                print("PASS: drat-trim verified the shipped proof")
            else:
                print("FAIL: drat-trim did not print 's VERIFIED'")
                fail = 1

    print("\n== 5. tamper check: a corrupted object must be REJECTED ==")
    import random
    random.seed(0)
    with open(cnf_path, "rb") as f:
        raw = bytearray(f.read())
    # flip one ASCII digit in a literal, well away from the header line
    digit_positions = [i for i, b in enumerate(raw) if 48 <= b <= 57 and i > 200]
    if not digit_positions:
        print("FAIL: could not find a digit to flip for the tamper check")
        fail = 1
    else:
        i = digit_positions[len(digit_positions) // 2]
        tampered = bytearray(raw)
        tampered[i] = ord('0') if raw[i] != ord('0') else ord('1')
        tamper_path = os.path.join(tmpdir, "tampered.cnf")
        with open(tamper_path, "wb") as f:
            f.write(tampered)
        drat_path = os.path.join(OBJ, "ceiling98.drat")
        tamper_log = os.path.join(tmpdir, "tamper_verify.log")
        os.system("%s %s %s > %s 2>&1" % (drat_bin, tamper_path, drat_path, tamper_log))
        tout = open(tamper_log).read()
        if "s VERIFIED" in tout:
            print("FAIL: the checker still verified after the object was tampered "
                  "with (digit flip at byte %d) -- it is not really checking "
                  "the object" % i)
            fail = 1
        else:
            print("PASS: tampering with the object (one digit flipped) made "
                  "verification fail, as it must: %s" % tout.strip().splitlines()[-1]
                  if tout.strip() else "PASS: tampering made verification fail (no output)")
        os.remove(tamper_path)
        os.remove(tamper_log)

    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)
    print()
    if fail:
        print("FAIL")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
