#!/usr/bin/env python3
"""Check object/code.txt: 43 distinct length-16 binary words, pairwise LCS at most 12.
Last line is PASS or FAIL.
"""
import sys
from pathlib import Path


def lcs(a, b):
    prev = [0] * (len(b) + 1)
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = prev[j] if prev[j] >= cur[j - 1] else cur[j - 1]
        prev = cur
    return prev[-1]


def fail(msg):
    print(msg)
    print("FAIL")
    return 1


def main():
    path = Path("object/code.txt")
    if not path.is_file():
        return fail("missing object/code.txt")
    words = []
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        words.append(line)
    print("size=%d" % len(words))
    if len(words) < 43:
        return fail("size %d is below 43" % len(words))
    if len(words) != len(set(words)):
        return fail("duplicate word")
    for w in words:
        if len(w) != 16 or any(c not in "01" for c in w):
            return fail("bad word")
    worst = 0
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            ell = lcs(words[i], words[j])
            if ell > worst:
                worst = ell
            if ell >= 13:
                return fail("LCS %d" % ell)
    print("max_lcs=%d" % worst)
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
