#!/usr/bin/env python3
"""Standalone check of every listed LLRL seed's highway onset (Python standard library only).
Definition: 4 colours 0..3. On colour c the ant turns LEFT for c in {0,1,3} and RIGHT for c = 2, writes (c+1) mod 4,
then steps one cell forward. Ant at (0,0) facing north, y grows downward. onset(C) = least t such that the colours read
from update t on are the period-384 highway of the blank grid (in some phase).
Test used here: simulate to a long horizon H; the read colour at update u equals the one at u+384 for every u >= t up
to H-384 (and not for u = t-1); the 384-update displacement is (+-4,+-4) with the same heading; the ant ends far from
every cell touched before t+384; and the 384-colour word read from t is a cyclic rotation of the blank grid's highway
word. This certifies each listed onset value; it does not re-prove minimality (that is the job of the two exhaustive
searches in how-we-built-it/)."""
import re, sys
P = 384
def run(seed, H):
    g = dict(seed); x = y = 0; d = 0; D = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    R = []; X = [(0, 0, 0)]
    for _ in range(H):
        c = g.get((x, y), 0); R.append(c)
        d = (d + 1) % 4 if c == 2 else (d + 3) % 4
        g[(x, y)] = (c + 1) % 4
        x += D[d][0]; y += D[d][1]; X.append((x, y, d))
    return R, X
def onset(seed, guess):
    H = guess + P * 1200
    R, X = run(seed, H)
    last = max((u for u in range(H - P) if R[u] != R[u + P]), default=-1)
    t = last + 1
    assert H - t > P * 1000
    dx = X[t + P][0] - X[t][0]; dy = X[t + P][1] - X[t][1]
    assert abs(dx) == 4 and abs(dy) == 4 and X[t + P][2] == X[t][2]
    touched = set(seed) | {(a, b) for a, b, _ in X[:t + P + 1]}; ex, ey, _ = X[-1]
    assert min(max(abs(ex - a), abs(ey - b)) for a, b in touched) > 1000
    return t, R[t:t + P]
def main(path):
    ok = True; n = 0
    b, W = onset({}, 256241); print("blank onset", b, "expected 256241"); ok &= (b == 256241)
    rots = {tuple(W[i:] + W[:i]) for i in range(P)}
    for line in open(path):
        m = re.match(r"k=(\d+) onset=(\d+) seed=(.*)", line.strip())
        if not m or m.group(3) == "(blank)": continue
        k, t = int(m.group(1)), int(m.group(2))
        cells = [tuple(map(int, c.split(","))) for c in m.group(3).split(";")]
        seed = {(x, y): c for x, y, c in cells}
        o, w = onset(seed, t); n += 1
        good = (o == t and len(seed) == k and all(1 <= c <= 3 for c in seed.values()) and tuple(w) in rots)
        print("k=%d listed onset %d computed %d cells %d word %s %s" % (k, t, o, len(seed), "H384" if tuple(w) in rots else "OTHER", "ok" if good else "MISMATCH"))
        ok &= good
    ok &= (n == 15)
    print("PASS" if ok else "FAIL")
if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "object/minimisers.txt")
