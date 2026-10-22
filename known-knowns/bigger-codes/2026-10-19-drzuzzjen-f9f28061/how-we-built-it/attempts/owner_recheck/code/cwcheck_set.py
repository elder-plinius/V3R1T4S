#!/usr/bin/env python3
"""Checker B (sets, standard library only, different route): each word becomes the tuple of its 1-positions.
Checks: every position in 0..n-1, exactly w positions, all words distinct, and that NO (w - d/2 + 1)-subset of
positions occurs in two different words. For weight-w words, distance(x, y) = 2(w - |x & y|) >= d iff
|x & y| <= w - d/2 iff they share no (w - d/2 + 1)-subset; so this tests every pair without computing distances.
Requires d even (Brouwer's convention). Does not import the other checker or any search program.
usage: cwcheck_set.py FILE n d w   ->  JSON receipt, exit 0 valid / 1 invalid / 2 bad input."""
import itertools
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cwio import read_code  # noqa: E402  (parsing only)


def positions(x, n):
    pos = []
    i = 0
    while x:
        if x & 1:
            pos.append(i)
        x >>= 1
        i += 1
    return tuple(pos)


def check(words, n, d, w):
    r = {"n": n, "d": d, "w": w, "M": len(words), "route": "no shared (w-d/2+1)-subset"}
    if d % 2:
        raise ValueError("d must be even")
    sets = [positions(x, n) for x in words]
    r["range_ok"] = all(all(0 <= p < n for p in s) for s in sets)
    r["weights_ok"] = all(len(s) == w for s in sets)
    r["distinct"] = len(set(sets)) == len(sets)
    t = w - d // 2 + 1
    r["t"] = t
    seen = {}
    collisions = 0
    example = None
    if t <= w:
        for idx, s in enumerate(sets):
            for sub in itertools.combinations(s, t):
                j = seen.get(sub)
                if j is not None and j != idx:
                    collisions += 1
                    if example is None:
                        example = [j, idx, list(sub)]
                else:
                    seen[sub] = idx
    r["t_subsets_indexed"] = len(seen)
    r["collisions"] = collisions
    r["first_collision"] = example
    r["valid"] = bool(r["range_ok"] and r["weights_ok"] and r["distinct"] and collisions == 0)
    return r


def main():
    if len(sys.argv) != 5:
        print(__doc__)
        sys.exit(2)
    path, n, d, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    try:
        fn, words = read_code(path, n)
    except Exception as e:  # noqa: BLE001
        print(json.dumps({"file": path, "error": str(e), "valid": False}))
        sys.exit(2)
    if fn != n:
        print(json.dumps({"file": path, "error": "file length %d != n %d" % (fn, n), "valid": False}))
        sys.exit(1)
    r = check(words, n, d, w)
    r["file"] = path
    print(json.dumps(r))
    sys.exit(0 if r["valid"] else 1)


if __name__ == "__main__":
    main()
