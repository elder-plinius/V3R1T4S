#!/usr/bin/env python3
"""Checker A (integers + popcount): words as uint64; asserts length/range, weight == w for every word, all distinct,
and popcount(x ^ y) >= d for ALL pairs (blocked numpy XOR + popcount). Independent of every search program.
usage: cwcheck_int.py FILE n d w   ->  JSON receipt, exit 0 if valid, 1 if invalid, 2 on bad input."""
import json
import sys

import numpy as np

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from cwio import read_code  # noqa: E402


def popcount64(a):
    a = a - ((a >> np.uint64(1)) & np.uint64(0x5555555555555555))
    a = (a & np.uint64(0x3333333333333333)) + ((a >> np.uint64(2)) & np.uint64(0x3333333333333333))
    a = (a + (a >> np.uint64(4))) & np.uint64(0x0F0F0F0F0F0F0F0F)
    return ((a * np.uint64(0x0101010101010101)) >> np.uint64(56)).astype(np.int64)


def check(words, n, d, w):
    r = {"n": n, "d": d, "w": w, "M": len(words)}
    if n > 64:
        raise ValueError("n > 64 not supported by this checker")
    a = np.array(words, dtype=np.uint64)
    r["range_ok"] = bool(np.all(a < (np.uint64(1) << np.uint64(n)))) if n < 64 else True
    wt = popcount64(a)
    r["weights_ok"] = bool(np.all(wt == w))
    r["distinct"] = len(set(words)) == len(words)
    mind = None
    bad = 0
    B = 2048
    for i in range(0, len(a), B):
        x = a[i:i + B]
        for j in range(i, len(a), B):
            y = a[j:j + B]
            dist = popcount64(x[:, None] ^ y[None, :])
            if i == j:
                iu = np.triu_indices(len(x), 1)
                dd = dist[iu]
            else:
                dd = dist.ravel()
            if dd.size:
                m = int(dd.min())
                mind = m if mind is None else min(mind, m)
                bad += int((dd < d).sum())
    r["pairs_tested"] = len(words) * (len(words) - 1) // 2
    r["min_distance"] = mind
    r["pairs_below_d"] = bad
    r["valid"] = bool(r["range_ok"] and r["weights_ok"] and r["distinct"] and bad == 0)
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
