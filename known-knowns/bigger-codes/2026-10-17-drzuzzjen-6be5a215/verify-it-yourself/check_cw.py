#!/usr/bin/env python3
"""Standalone checker (Python standard library only), written from the definition:
A(n,d,w) code = a set of binary words of length n, each of Hamming weight exactly w, pairwise Hamming distance >= d.
usage: check_cw.py FILE n d w CLAIMED_M
The file holds one word per line as a string of n characters over {0,1}. Checks: line count == CLAIMED_M; each
line has length n and only 0/1; weight == w; all words distinct; for ALL pairs, popcount(x XOR y) >= d.
Last output line: PASS or FAIL."""
import sys


def main():
    path, n, d, w, m = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    lines = [ln.strip() for ln in open(path, encoding="ascii") if ln.strip()]
    ok = True
    if len(lines) != m:
        print("count %d != claimed %d" % (len(lines), m)); ok = False
    words = []
    for i, ln in enumerate(lines):
        if len(ln) != n or set(ln) - {"0", "1"}:
            print("line %d: bad format" % (i + 1)); ok = False; continue
        if ln.count("1") != w:
            print("line %d: weight %d != %d" % (i + 1, ln.count("1"), w)); ok = False
        words.append(int(ln, 2))
    if len(set(words)) != len(words):
        print("duplicate words"); ok = False
    bad = 0
    mind = n
    for i in range(len(words)):
        x = words[i]
        for j in range(i + 1, len(words)):
            dist = bin(x ^ words[j]).count("1")
            if dist < mind:
                mind = dist
            if dist < d:
                bad += 1
    print("words %d, pairs %d, minimum distance %d, pairs below %d: %d" % (len(words), len(words) * (len(words) - 1) // 2, mind, d, bad))
    if bad:
        ok = False
    print("PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
