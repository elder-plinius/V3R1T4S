#!/usr/bin/env python3
"""Standalone check of every minimiser's onset (Python standard library only).
Definition: Langton's ant, white -> turn right, black -> turn left, flip the cell, step forward. Ant at (0,0) heading
north, y down. onset(C) = least t such that, after t updates, the remaining run is the period-104 highway.
Test used here: the turn made at update u equals the turn at update u+104 for every u >= t up to a long horizon, the
104-update displacement is (+-2,+-2), the ant ends far from every cell touched before t+104, and t is least (the turn
at update t-1 differs from the one at t+103). This certifies each listed onset value; it does not re-prove minimality
(that is the job of the two completeness searches in how-we-built-it/)."""
import re, sys
H = 200000
def turns(black):
    black = set(black); x = y = 0; d = 0; D = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    T = []; P = [(0, 0)]
    for _ in range(H):
        c = (x, y)
        if c in black: d = (d + 3) % 4; black.discard(c); T.append('L')
        else: d = (d + 1) % 4; black.add(c); T.append('R')
        x += D[d][0]; y += D[d][1]; P.append((x, y))
    return T, P
def onset(cells):
    T, P = turns(cells)
    last = max((u for u in range(H - 104) if T[u] != T[u + 104]), default=-1)
    t = last + 1
    assert H - t > 104 * 1000
    dx = P[t + 104][0] - P[t][0]; dy = P[t + 104][1] - P[t][1]
    assert abs(dx) == 2 and abs(dy) == 2
    touched = set(cells) | set(P[:t + 105]); ex, ey = P[-1]
    assert min(max(abs(ex - a), abs(ey - b)) for a, b in touched) > 1000
    return t
def main(path):
    ok = True; n = 0
    b = onset([]); print("blank onset", b, "expected 9977"); ok &= (b == 9977)
    for line in open(path):
        m = re.match(r"MIN t=(\d+) p=\d+ k=(\d+) cells: (.*)", line.strip())
        if not m: continue
        t, k = int(m.group(1)), int(m.group(2))
        cells = [tuple(map(int, c)) for c in re.findall(r"\((-?\d+),(-?\d+)\)", m.group(3))]
        o = onset(cells); n += 1
        good = (o == t and len(cells) == k)
        print("k=%d listed onset %d computed %d cells %d %s" % (k, t, o, len(cells), "ok" if good else "MISMATCH"))
        ok &= good
    ok &= (n == 13)
    print("PASS" if ok else "FAIL")
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "object/minimisers.txt")
