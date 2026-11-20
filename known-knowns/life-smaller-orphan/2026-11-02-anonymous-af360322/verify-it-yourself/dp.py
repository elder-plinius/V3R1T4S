#!/usr/bin/env python3
"""Independent predecessor test by column transfer: states are pairs of adjacent predecessor columns (height h+2);
reading target columns left to right, the set of reachable states becomes empty exactly when the prefix is an orphan.
first_orphan_width(h, B, S, W) returns the least width <= W with an h-row orphan, or None. B, S are bit masks
(bit n set = birth/survival on n live neighbours); Life is B=8, S=12."""
import sys, time
def first_orphan_width(h, B, S, W):
    H = h + 2; nc = 1 << H
    def nxt_cell(col3, i):  # col3 = (a,b,c); target row i (0..h-1) corresponds to pred row i+1
        a, b, c = col3
        n = 0
        for col in (a, b, c):
            for r in (i, i + 1, i + 2):
                n += (col >> r) & 1
        centre = (b >> (i + 1)) & 1
        n -= centre
        return ((S >> n) & 1) if centre else ((B >> n) & 1)
    T = 1 << h
    nxt = [[0] * T for _ in range(nc * nc)]
    for a in range(nc):
        for b in range(nc):
            s = a * nc + b
            for c in range(nc):
                t = 0
                for i in range(h):
                    t |= nxt_cell((a, b, c), i) << i
                nxt[s][t] |= 1 << (b * nc + c)
    frontier = {(1 << (nc * nc)) - 1}
    seen = set(frontier)
    for w in range(1, W + 1):
        new = set()
        for S_ in frontier:
            for t in range(T):
                m = 0; x = S_
                while x:
                    lb = x & -x; s = lb.bit_length() - 1; x ^= lb
                    m |= nxt[s][t]
                if m == 0:
                    return w
                if m not in seen:
                    seen.add(m); new.add(m)
        frontier = new
        if not frontier:
            return None  # closed: no orphan of this height at any width
    return None
