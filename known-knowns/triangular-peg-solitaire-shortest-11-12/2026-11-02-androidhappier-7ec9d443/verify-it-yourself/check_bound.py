#!/usr/bin/env python3
"""Check object/BOUND.txt: it must pin the sha256 of the solution file, and every number in it must equal what the
standalone checker (check_peg.py) computes from that file. Standard library only. Run from the package folder."""
import csv, hashlib, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_peg

def h(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()

ok = True
row = list(csv.DictReader(open("INDEX.csv")))[0]
sol = row["file"]
got = h(sol)
print("%s sha256 %s (INDEX.csv: %s)" % (sol, got, "match" if got == row["sha256"] else "MISMATCH"))
ok &= got == row["sha256"]
try:
    nm, nj, left, merges = check_peg.check(12, open(sol).read(), "a3")
except (ValueError, KeyError) as e:
    print("solution does not replay: %s" % e)
    print("FAIL")
    sys.exit(1)
expected = "\n".join([
    "object: an explicit solution of triangular peg solitaire on Triangle(12), OEIS A127500, cell a(12)",
    "solution_file: %s" % sol,
    "solution_sha256: %s" % got,
    "board: Triangle(12), 78 holes, G. I. Bell's notation (a1 = top corner, row r holds a..(r-th letter))",
    "start: full board minus a3",
    "finish: one peg at %s" % ",".join(left),
    "jumps: %d" % nj,
    "moves: %d" % nm,
    "bound: a(12) <= %d" % nm,
    "published_upper_bound: 29 (OEIS A127500 comment and G. I. Bell, Large Triangular Boards, both fetched 2026-11-02T17:31:50Z)",
    "published_lower_bound: 21",
    "claim: upper bound only; the exact value of a(12) is not claimed",
]) + "\n"
same = open("object/BOUND.txt").read() == expected
print("object/BOUND.txt %s the values recomputed from the solution" % ("matches" if same else "DOES NOT MATCH"))
ok &= same
ok &= len(left) == 1 and merges == 0 and nm == int(row["value"]) and nm < 29
print("bound a(12) <= %d, published 29: %s" % (nm, "strictly better" if nm < 29 else "NOT better"))
print("ok" if ok else "FAIL")
sys.exit(0 if ok else 1)
