#!/usr/bin/env python3
"""Standalone checker: is a 0/1 matrix K_{3,3}-free (no 3 rows and 3 columns whose 9 common entries are all 1)?

Standard library only. Usage (from the claim folder):
    python check/check_matrix.py matrix/z_16x19_142.txt --rows 16 --cols 19 --ones 142
Prints PASS or FAIL as the last line and exits 0 on PASS, 1 on FAIL.
    python check/check_matrix.py --selftest     known positive and known negative cases, then PASS/FAIL

Two independent methods are run and must agree:
  A (literal definition): for every set of 3 rows and every set of 3 columns, test the 9 entries.
  B (counting): for every set of 3 rows, count the columns where all three rows have a 1; a K33 exists iff some
    row triple has >= 3 such columns.
The matrix file is plain text: one row per line, characters 0 and 1 only (blank lines ignored).
"""
import argparse
import sys
from itertools import combinations


def load(path):
    rows = []
    with open(path, "r", encoding="ascii", newline="") as f:
        for ln, line in enumerate(f, 1):
            s = line.strip()
            if not s:
                continue
            if set(s) - {"0", "1"}:
                raise ValueError("line %d has a character other than 0 or 1" % ln)
            rows.append([int(ch) for ch in s])
    if not rows:
        raise ValueError("empty matrix")
    if len({len(r) for r in rows}) != 1:
        raise ValueError("rows have different lengths")
    return rows


def method_a(M):
    """Return the first (rows, cols) with all nine entries 1, or None."""
    m, n = len(M), len(M[0])
    for rs in combinations(range(m), 3):
        for cs in combinations(range(n), 3):
            if all(M[r][c] for r in rs for c in cs):
                return rs, cs
    return None


def method_b(M):
    m, n = len(M), len(M[0])
    for rs in combinations(range(m), 3):
        common = [c for c in range(n) if M[rs[0]][c] and M[rs[1]][c] and M[rs[2]][c]]
        if len(common) >= 3:
            return rs, tuple(common[:3])
    return None


def check(M, rows=None, cols=None, ones=None):
    """Return (ok, list of messages)."""
    msgs, ok = [], True
    m, n = len(M), len(M[0])
    total = sum(map(sum, M))
    msgs.append("shape %d x %d, ones %d" % (m, n, total))
    if rows is not None and m != rows:
        ok = False
        msgs.append("wrong number of rows: %d, expected %d" % (m, rows))
    if cols is not None and n != cols:
        ok = False
        msgs.append("wrong number of columns: %d, expected %d" % (n, cols))
    if ones is not None and total < ones:
        ok = False
        msgs.append("only %d ones, need at least %d" % (total, ones))
    a, b = method_a(M), method_b(M)
    if (a is None) != (b is None):
        ok = False
        msgs.append("methods A and B disagree (A=%s B=%s)" % (a, b))
    if a is not None or b is not None:
        ok = False
        w = a or b
        msgs.append("all-ones 3x3 submatrix at rows %s, columns %s" % (w[0], w[1]))
    else:
        msgs.append("no all-ones 3x3 submatrix (methods A and B agree; %d row triples x %d column triples)" % (
            len(list(combinations(range(m), 3))), len(list(combinations(range(n), 3)))))
    return ok, msgs


def selftest():
    ok_all = True
    pos = [[1, 1, 1, 0], [1, 1, 1, 0], [1, 1, 0, 1]]          # 3x4, columns 0,1,2 only two rows full: no K33
    neg = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]                   # K33 itself
    neg2 = [[1, 1, 1, 0], [1, 1, 1, 1], [1, 1, 1, 0], [0, 0, 0, 1]]   # K33 inside a bigger matrix
    for name, M, expect in (("positive", pos, True), ("negative K33", neg, False), ("negative embedded", neg2, False)):
        got, _ = check(M)
        print("selftest %-18s expected %-5s got %-5s %s" % (name, expect, got, "ok" if got == expect else "WRONG"))
        ok_all &= got == expect
    return ok_all


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("matrix", nargs="?")
    ap.add_argument("--rows", type=int)
    ap.add_argument("--cols", type=int)
    ap.add_argument("--ones", type=int, help="require at least this many ones")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        good = selftest()
        print("PASS" if good else "FAIL")
        return 0 if good else 1
    if not a.matrix:
        ap.error("matrix file required (or --selftest)")
    try:
        M = load(a.matrix)
    except (OSError, ValueError) as e:
        print("cannot read matrix: %s" % e)
        print("FAIL")
        return 1
    good, msgs = check(M, a.rows, a.cols, a.ones)
    for s in msgs:
        print(s)
    print("PASS" if good else "FAIL")
    return 0 if good else 1


if __name__ == "__main__":
    sys.exit(main())
