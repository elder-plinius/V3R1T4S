#!/usr/bin/env python3
"""Exact check of a binary constant-weight code against a table cell.

usage: python3 check_cw.py CODE_FILE n d w claimed_size table_lower_bound table_upper_bound [expected_sha256]

The code file has one word per line as n characters 0/1; lines starting with '#' are comments.
Checks: every word has length n, only 0 and 1, weight exactly w; all words distinct; the Hamming distance of
every pair (no sampling) is >= d; the number of words equals the claimed size, is strictly greater than the
table's lower bound and not greater than its upper bound. Prints PASS or FAIL on the last line.
"""
import hashlib
import sys
from collections import Counter


def main(argv):
    path = argv[1]
    n, d, w, claimed, lb, ub = (int(x) for x in argv[2:8])
    sha = argv[8] if len(argv) > 8 else None
    raw = open(path, "rb").read()
    ok = True
    if sha is not None:
        got = hashlib.sha256(raw).hexdigest()
        print("file sha256", got)
        if got != sha:
            print("sha256 differs from the expected", sha)
            ok = False
    words = [l.strip() for l in raw.decode("ascii", "replace").splitlines() if l.strip() and not l.startswith("#")]
    print("n = %d, d = %d, w = %d, words read: %d" % (n, d, w, len(words)))
    for k, s in enumerate(words, 1):
        if len(s) != n:
            print("word %d has length %d" % (k, len(s)))
            ok = False
        if set(s) - {"0", "1"}:
            print("word %d has a symbol other than 0 and 1" % k)
            ok = False
        if s.count("1") != w:
            print("word %d has weight %d" % (k, s.count("1")))
            ok = False
    if len(set(words)) != len(words):
        print("duplicate words: %d lines, %d distinct" % (len(words), len(set(words))))
        ok = False
    vals = [int(s, 2) if set(s) <= {"0", "1"} and s else 0 for s in words]
    dist = Counter()
    for i in range(len(vals)):
        for j in range(i + 1, len(vals)):
            dist[bin(vals[i] ^ vals[j]).count("1")] += 1
    pairs = sum(dist.values())
    print("pairs checked: %d (all of them)" % pairs)
    print("distance distribution: " + " ".join("%d:%d" % kv for kv in sorted(dist.items())))
    mind = min(dist) if dist else None
    print("minimum distance:", mind)
    if mind is None or mind < d:
        ok = False
    if d % 2:
        print("d is odd; the table uses even d")
        ok = False
    m = len(words)
    if m != claimed:
        print("size %d differs from the claimed %d" % (m, claimed))
        ok = False
    print("table lower bound %d, upper bound %d, size %d: margin over the lower bound %d" % (lb, ub, m, m - lb))
    if not (lb < m <= ub):
        ok = False
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
