#!/usr/bin/env python3
"""cwcheck.py FILE n d w [--M M] [--sha256 HEX]  --  check a binary constant-weight code with python3 + numpy only.

Definition used: a set of M distinct binary words of length n, each of Hamming weight exactly w, with pairwise
Hamming distance >= d.  Such a set proves A(n, d, w) >= M.

File format: one word per line as a string of n characters '0'/'1', no header, no blank lines.

Tests (all must pass for VALID):
  F  format: every line has exactly n characters from {0,1}; the line count equals M (if --M is given, else the
     number in the file name A<n>_<d>_<w>_<M>.txt)
  W  every word has weight w; all words are distinct
  A  all M(M-1)/2 pairwise Hamming distances via uint64 XOR + popcount (blocked), minimum >= d; the full distance
     histogram is printed
  B  independent route: with t = w - d/2 + 1, two words at distance < d share at least t common ones, so all
     t-subsets of all supports must be pairwise distinct; the test enumerates them and counts collisions
  H  optional: sha256 of the file equals --sha256

Output: one line per test and a final VERDICT line.  Exit code 0 iff VALID.
"""
import hashlib
import itertools
import os
import re
import sys

import numpy as np


def popcount64(a):
    if hasattr(np, "bitwise_count"):
        return np.bitwise_count(a).astype(np.int64)
    tbl = np.array([bin(i).count("1") for i in range(256)], dtype=np.int64)
    return tbl[a.view(np.uint8).reshape(a.shape + (8,))].sum(axis=-1)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    opts = {}
    it = iter(sys.argv[1:])
    for a in it:
        if a in ("--M", "--sha256"):
            opts[a] = next(it)
    if len(args) < 4:
        print(__doc__)
        sys.exit(2)
    path, n, d, w = args[0], int(args[1]), int(args[2]), int(args[3])
    if d % 2 or n > 64:
        print("this checker needs even d and n <= 64")
        sys.exit(2)
    raw = open(path, "rb").read()
    sha = hashlib.sha256(raw).hexdigest()
    m = re.search(r"A(\d+)_(\d+)_(\d+)_(\d+)\.txt$", os.path.basename(path))
    M_claim = int(opts["--M"]) if "--M" in opts else (int(m.group(4)) if m else None)

    lines = raw.split(b"\n")
    if lines and lines[-1] == b"":
        lines.pop()                      # one trailing newline is fine
    bad_fmt = sum(1 for ln in lines if len(ln) != n or any(c not in (48, 49) for c in ln))
    words = [int(ln, 2) for ln in lines if len(ln) == n and all(c in (48, 49) for c in ln)]
    M = len(lines)
    print("file=%s sha256=%s" % (os.path.basename(path), sha))
    ok = True
    print("F format: lines=%d claimed_M=%s bad_lines=%d" % (M, M_claim, bad_fmt))
    if bad_fmt or (M_claim is not None and M != M_claim):
        ok = False
    bad_w = sum(1 for x in words if bin(x).count("1") != w)
    distinct = len(set(words))
    print("W weight/distinct: bad_weight=%d distinct=%d" % (bad_w, distinct))
    if bad_w or distinct != M:
        ok = False

    Mw = len(words)                      # well-formed words only; a bad line already made the verdict INVALID
    arr = np.array(words, dtype=np.uint64)
    hist = np.zeros(n + 1, dtype=np.int64)
    blk = max(1, min(Mw, int(1.0e7 // max(Mw, 1))))
    for i0 in range(0, Mw, blk):
        i1 = min(Mw, i0 + blk)
        x = arr[i0:i1, None] ^ arr[None, i0:]
        dist = popcount64(x)
        r = np.arange(i1 - i0)[:, None]
        c = np.arange(Mw - i0)[None, :]
        dist = dist[c > r]
        hist += np.bincount(dist, minlength=n + 1)
    npairs = int(hist.sum())
    mind = int(np.nonzero(hist)[0][0]) if npairs else n
    print("A all-pairs: words=%d pairs=%d expected=%d min_distance=%d need>=%d histogram=%s" %
          (Mw, npairs, Mw * (Mw - 1) // 2, mind, d, {int(k): int(v) for k, v in enumerate(hist) if v}))
    if npairs != Mw * (Mw - 1) // 2 or mind < d:
        ok = False

    t = w - d // 2 + 1
    seen = set()
    total = 0
    for x in words:
        pos = [i for i in range(n) if (x >> i) & 1]
        for comb in itertools.combinations(pos, t):
            mm = 0
            for p in comb:
                mm |= 1 << p
            seen.add(mm)
            total += 1
    print("B packing: t=%d subsets=%d distinct=%d collisions=%d" % (t, total, len(seen), total - len(seen)))
    if total != len(seen):
        ok = False
    if "--sha256" in opts:
        same = sha == opts["--sha256"].lower()
        print("H sha256 matches expected: %s" % same)
        ok = ok and same
    print("VERDICT: %s  A(%d,%d,%d) >= %d" % ("VALID" if ok else "INVALID", n, d, w, M))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
