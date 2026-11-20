#!/usr/bin/env python3
"""Exact checker for an unrestricted q-ary code, written from the definition of A_q(n,d).

usage: python3 check_code.py CODE_FILE q n d claimed_size table_lower_bound table_upper_bound [sha256]

CODE_FILE: one codeword per line, written as n digits 0..q-1; lines starting with '#' and blank lines are skipped.
Checks, with plain integers and no sampling: every word has length n; every symbol is in {0, ..., q-1}; the words are
pairwise distinct; the Hamming distance of every one of the M(M-1)/2 pairs is >= d; M equals the claimed size;
M is strictly greater than the table's lower bound and at most the table's upper bound. With a sha256 argument it
also checks the file's sha256. Prints the facts it computed, then PASS or FAIL on the last line (exit 0 or 1).
"""
import hashlib
import sys


def main(argv):
    if len(argv) not in (8, 9):
        print(__doc__)
        print("FAIL")
        return 1
    path = argv[1]
    q, n, d, claimed, lb, ub = (int(x) for x in argv[2:8])
    want_sha = argv[8] if len(argv) == 9 else None
    raw = open(path, "rb").read()
    problems = []
    sha = hashlib.sha256(raw).hexdigest()
    print("file sha256", sha)
    if want_sha is not None and sha != want_sha:
        problems.append("sha256 differs from the expected %s" % want_sha)
    words = []
    for lineno, line in enumerate(raw.decode("ascii", "replace").splitlines(), 1):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if len(s) != n:
            problems.append("line %d: length %d, expected %d" % (lineno, len(s), n))
            continue
        if any(ch not in "0123456789"[:q] for ch in s):
            problems.append("line %d: symbol outside 0..%d" % (lineno, q - 1))
            continue
        words.append(tuple(ord(ch) - 48 for ch in s))
    M = len(words)
    print("q = %d, n = %d, words read: %d" % (q, n, M))
    if len(set(words)) != M:
        problems.append("%d repeated words" % (M - len(set(words))))
    dmin = None
    hist = {}
    for i in range(M):
        a = words[i]
        for j in range(i + 1, M):
            b = words[j]
            h = 0
            for k in range(n):
                if a[k] != b[k]:
                    h += 1
            hist[h] = hist.get(h, 0) + 1
            if dmin is None or h < dmin:
                dmin = h
    print("pairs checked: %d (all of them)" % (M * (M - 1) // 2))
    print("distance distribution:", " ".join("%d:%d" % (k, hist[k]) for k in sorted(hist)))
    print("minimum distance:", dmin)
    if dmin is None or dmin < d:
        problems.append("minimum distance %s is below %d" % (dmin, d))
    if M != claimed:
        problems.append("size %d differs from the claimed %d" % (M, claimed))
    print("table lower bound %d, upper bound %d, size %d: margin over the lower bound %d" % (lb, ub, M, M - lb))
    if not M > lb:
        problems.append("size %d is not strictly greater than the table's lower bound %d" % (M, lb))
    if M > ub:
        problems.append("size %d exceeds the table's upper bound %d (a bug somewhere)" % (M, ub))
    for p in problems:
        print("problem:", p)
    print("FAIL" if problems else "PASS")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
