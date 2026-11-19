#!/usr/bin/env python3
"""Convert a dense scheme file to and from the plain-text format that tools/zt_flip_reduce.c reads on stdin and writes
on stdout (the format run_c_opt in tools/unfold_z_to_zt.py uses): a header line "n1 n2 n3 R", then the R rows of u,
the R rows of v and the R rows of w, one row per line, entries separated by spaces. Standard library only.

Usage:
  python3 -I flip_io.py to-text   DENSE.json TEXT.txt
  python3 -I flip_io.py from-text TEXT.txt   DENSE.json
"""
import json
import sys


def to_text(src, dst):
    d = json.load(open(src))
    n1, n2, n3 = d["n"]
    lines = [f"{n1} {n2} {n3} {d['m']}"]
    for key in ("u", "v", "w"):
        lines += [" ".join(str(x) for x in row) for row in d[key]]
    open(dst, "w").write("\n".join(lines) + "\n")


def from_text(src, dst):
    lines = open(src).read().strip().split("\n")
    n1, n2, n3, r = map(int, lines[0].split())
    rows = [list(map(int, line.split())) for line in lines[1:1 + 3 * r]]
    json.dump({"n": [n1, n2, n3], "m": r, "u": rows[:r], "v": rows[r:2 * r], "w": rows[2 * r:]},
              open(dst, "w"), separators=(",", ":"))


if __name__ == "__main__":
    {"to-text": to_text, "from-text": from_text}[sys.argv[1]](sys.argv[2], sys.argv[3])
