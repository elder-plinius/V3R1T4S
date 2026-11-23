#!/usr/bin/env python3
"""Standalone checker for triangular peg solitaire, written from the OEIS A127500 definition (standard library only).

Board Triangle(n): holes (r, c) with 1 <= c <= r <= n. Hole name (G. I. Bell's notation) = letter(c) + str(r),
so a1 is the top corner and row r has holes a..(r-th letter). A jump takes a peg from p over the adjacent hole
p+d (which must hold a peg; it is removed) into the empty hole p+2d, where d is one of the six lattice steps
(0,+-1), (+-1,0), (+1,+1), (-1,-1). A move (A127500: "one or more jumps by the same peg") is one comma-separated
item h0-h1-...-hk. Square brackets and a trailing "(k)" (Bell's move count) are ignored.

usage: check_peg.py N FILE VACANCY [EXPECT_MOVES [EXPECT_FINISH]]
The start position is the full board minus VACANCY (given explicitly, not inferred). The solution is valid when
every jump is legal and exactly one peg is left after T(N)-2 jumps. Also reports "merges": adjacent items where
the next starts at the hole the previous ended, which would make two listed items one move (must be 0 for the
listed item count to equal the A127500 move count). Exit 0 iff valid and every given expectation holds."""
import re, sys

STEPS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]

def hole(s, n):
    m = re.fullmatch(r"([a-z])(\d+)", s.strip())
    if not m:
        raise ValueError("bad hole name %r" % s)
    r, c = int(m.group(2)), ord(m.group(1)) - 96
    if not 1 <= c <= r <= n:
        raise ValueError("hole %r is off the Triangle(%d) board" % (s, n))
    return (r, c)

def name(h):
    return chr(96 + h[1]) + str(h[0])

def check(n, text, vacancy):
    text = re.sub(r"\(\d+\)", "", text).replace("[", "").replace("]", "")
    items = [t.strip() for t in text.split(",") if t.strip()]
    board = {(r, c): True for r in range(1, n + 1) for c in range(1, r + 1)}
    board[hole(vacancy, n)] = False
    moves, jumps = [], 0
    for i, it in enumerate(items, 1):
        hs = [hole(x, n) for x in it.split("-")]
        if len(hs) < 2:
            raise ValueError("move %d has no jump: %r" % (i, it))
        for a, b in zip(hs, hs[1:]):
            dr, dc = b[0] - a[0], b[1] - a[1]
            if dr % 2 or dc % 2 or (dr // 2, dc // 2) not in STEPS:
                raise ValueError("move %d: %s-%s is not a lattice jump" % (i, name(a), name(b)))
            mid = (a[0] + dr // 2, a[1] + dc // 2)
            if not (board[a] and board[mid] and not board[b]):
                raise ValueError("move %d: illegal jump %s-%s" % (i, name(a), name(b)))
            board[a], board[mid], board[b] = False, False, True
            jumps += 1
        moves.append(hs)
    merges = sum(1 for p, q in zip(moves, moves[1:]) if p[-1] == q[0])
    left = sorted(name(h) for h, v in board.items() if v)
    return len(moves), jumps, left, merges

def main():
    n, path, vac = int(sys.argv[1]), sys.argv[2], sys.argv[3]
    exp_m = int(sys.argv[4]) if len(sys.argv) > 4 else None
    exp_f = sys.argv[5] if len(sys.argv) > 5 else None
    try:
        nm, nj, left, merges = check(n, open(path).read(), vac)
    except (ValueError, KeyError) as e:
        print("check_peg: n=%d vacancy=%s ILLEGAL (%s)" % (n, vac, e))
        return 1
    ok = len(left) == 1 and nj == n * (n + 1) // 2 - 2 and merges == 0
    if exp_m is not None and nm != exp_m:
        ok = False
    if exp_f is not None and left != [exp_f]:
        ok = False
    print("check_peg: n=%d vacancy=%s moves=%d jumps=%d pegs_left=%d finish=%s merges=%d %s" % (
        n, vac, nm, nj, len(left), ",".join(left), merges, "VALID" if ok else "NOT_VALID"))
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
