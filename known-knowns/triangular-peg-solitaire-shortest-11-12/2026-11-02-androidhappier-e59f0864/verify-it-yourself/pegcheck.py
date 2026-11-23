#!/usr/bin/env python3
"""Independent simulator for triangular peg solitaire (OEIS A127500 / G. I. Bell notation).
Board Triangle(n): holes (r, c) with 1 <= c <= r <= n; hole name = letter(c) + str(r), a = column 1.
Jumps along the three lattice directions in skew coordinates: (0,+-2), (+-2,0), (+-2,+-2), over the midpoint.
Input: a solution as moves separated by commas, each move 'h0-h1-...-hk' (one peg jumping k times).
Brackets [ ] and a trailing '(k)' are ignored. The start position is the full board minus the landing hole of
the first jump. Moves are counted as maximal runs of consecutive jumps by the same peg (definition in A127500).
Prints the start vacancy, finish hole, jumps, moves; exits 1 on any illegal jump or more than one final peg."""
import re, sys

def parse_hole(s, n):
    m = re.fullmatch(r'([a-z])(\d+)', s.strip())
    if not m: raise ValueError('bad hole %r' % s)
    c = ord(m.group(1)) - 96; r = int(m.group(2))
    if not (1 <= c <= r <= n): raise ValueError('hole off board %r' % s)
    return (r, c)

def name(h): return chr(96 + h[1]) + str(h[0])

def check(n, text):
    text = re.sub(r'\(\d+\)', '', text).replace('[', ',').replace(']', ',')
    toks = [t.strip() for t in re.split(r'[,\n;]+', text) if t.strip()]
    jumps = []
    for t in toks:
        hs = [parse_hole(x, n) for x in t.split('-')]
        if len(hs) < 2: raise ValueError('move with no jump %r' % t)
        for a, b in zip(hs, hs[1:]): jumps.append((a, b))
    board = {(r, c): 1 for r in range(1, n + 1) for c in range(1, r + 1)}
    start = jumps[0][1]; board[start] = 0
    moves = 0; prev_end = None
    for a, b in jumps:
        dr, dc = b[0] - a[0], b[1] - a[1]
        if (dr, dc) not in [(0, 2), (0, -2), (2, 0), (-2, 0), (2, 2), (-2, -2)]:
            raise ValueError('not a lattice jump %s-%s' % (name(a), name(b)))
        mid = (a[0] + dr // 2, a[1] + dc // 2)
        if board.get(a) != 1 or board.get(mid) != 1 or board.get(b) != 0:
            raise ValueError('illegal jump %s-%s' % (name(a), name(b)))
        board[a] = 0; board[mid] = 0; board[b] = 1
        if a != prev_end: moves += 1
        prev_end = b
    left = [h for h, v in board.items() if v]
    return start, left, len(jumps), moves

if __name__ == '__main__':
    n = int(sys.argv[1]); text = open(sys.argv[2]).read()
    try:
        start, left, nj, nm = check(n, text)
    except ValueError as e:
        print('ILLEGAL', e); sys.exit(1)
    ok = len(left) == 1 and nj == n * (n + 1) // 2 - 2
    print('n=%d start_vacancy=%s pegs_left=%d finish=%s jumps=%d moves=%d %s' % (
        n, name(start), len(left), ','.join(name(h) for h in left), nj, nm, 'VALID' if ok else 'NOT_SOLVED'))
    sys.exit(0 if ok else 1)
