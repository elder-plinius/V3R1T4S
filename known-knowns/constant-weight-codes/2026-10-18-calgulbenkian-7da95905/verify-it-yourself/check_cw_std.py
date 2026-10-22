"""Standard-library exact checker for a binary constant-weight code.

Usage: python3 -I check_cw_std.py FILE n d w M [--pairwise]

FILE has one word per line, a 0/1 string of length n. The checker asserts: every line is a 0/1 string of length n,
there are exactly M lines, they are distinct, and every word has exactly w ones. Then it proves minimum distance >= d
(d even) in one of two exact ways:
  default     two distinct weight-w words differ in 2*(w - |intersection|) positions, so distance >= d holds exactly
              when no two words share t = w - d/2 + 1 common ones; the checker lists every t-subset of ones of every
              word and requires all of them to be distinct (a collision names the offending pair).
  --pairwise  computes the popcount of x XOR y for all M*(M-1)/2 pairs (slow in pure Python, minutes for M above 10000).
Exit status 0 on PASS, 1 otherwise.
"""
import sys
from itertools import combinations

def main():
    args = [a for a in sys.argv[1:] if a != "--pairwise"]
    pairwise = "--pairwise" in sys.argv[1:]
    path = args[0]
    n, d, w, M = map(int, args[1:5])
    if d % 2:
        print("FAIL d must be even"); return 1
    rows = [l.strip() for l in open(path) if l.strip()]
    name = path.replace("\\", "/").split("/")[-1]
    if any(len(r) != n or set(r) - {"0", "1"} for r in rows):
        print("FAIL a row is not a 0/1 string of length", n); return 1
    if len(rows) != M:
        print("FAIL count", len(rows), "expected", M); return 1
    if len(set(rows)) != M:
        print("FAIL duplicate words"); return 1
    if any(r.count("1") != w for r in rows):
        print("FAIL a word does not have weight", w); return 1
    if pairwise:
        xs = [int(r, 2) for r in rows]
        mind = n
        for i in range(M - 1):
            xi = xs[i]
            for xj in xs[i + 1:]:
                dist = bin(xi ^ xj).count("1")
                if dist < mind:
                    mind = dist
                    if mind < d:
                        print("FAIL distance", mind, "between words", i, "and", xs.index(xj)); return 1
        print("%s: M=%d n=%d w=%d min distance %d >= %d (all pairs) PASS" % (name, M, n, w, mind, d))
        return 0
    t = w - d // 2 + 1
    seen = {}
    for i, r in enumerate(rows):
        ones = [k for k, ch in enumerate(r) if ch == "1"]
        for sub in combinations(ones, t):
            if sub in seen:
                print("FAIL words %d and %d share %d common ones, so their distance is below %d" % (seen[sub], i, t, d))
                return 1
            seen[sub] = i
    print("%s: M=%d n=%d w=%d distinct, weight w, no two words share %d ones, so min distance >= %d PASS" % (name, M, n, w, t, d))
    return 0

sys.exit(main())
