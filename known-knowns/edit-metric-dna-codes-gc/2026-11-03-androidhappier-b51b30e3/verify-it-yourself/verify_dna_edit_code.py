#!/usr/bin/env python3
"""Standalone checker for Sun-type (n, d, w)_4 DNA edit-metric codes, written from the definition
(J. Sun, M.Sc. thesis, Brock University 2010, Sec. 1.5): words over {A,C,G,T} of length n, GC weight exactly
w = floor(n/2), Levenshtein (edit) distance d(x, y) >= d for all distinct codewords x, y, and
d(x, rc(y)) >= d for ALL codewords x, y INCLUDING x = y (rc = Watson-Crick reverse complement, A<->T, C<->G).

Two independent methods, which must agree:
  A: all-pairs dynamic-programming Levenshtein distance (substitution, insertion, deletion, each cost 1);
  B: explicit edit balls (meet in the middle): with r1 = floor((d-1)/2) and r2 = d-1-r1, the sets of ALL strings
     (any length) reachable by at most r1 resp. r2 single insertions/deletions/substitutions are built by
     breadth-first search. Since edit distance is the shortest-path metric of single edits, d(u, v) <= d-1 iff
     ball(u, r2) and ball(v, r1) intersect. A violation is any pair of distinct codewords x, y, or any codeword x and
     any rc(y) (y = x included), whose balls intersect.
Python 3 standard library only.

usage: verify_dna_edit_code.py FILE n d [--expect-size K] [--method-a-only]
--method-a-only skips method B (used only for the quick "read with a larger d" control, where radius-3 edit balls of
length-9 words would make the control slow; method A alone already decides that the object fails at that d).
Prints VALID / NOT VALID details and, as last line, PASS or FAIL (exit code 0 / 1).
"""
import sys
import itertools

COMP = {"A": "T", "T": "A", "C": "G", "G": "C"}


def rc(x):
    return "".join(COMP[c] for c in reversed(x))


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def ball(x, r):
    """All strings within edit distance r of x (breadth-first over single edits)."""
    seen = {x}
    frontier = {x}
    for _ in range(r):
        nxt = set()
        for s in frontier:
            for i in range(len(s) + 1):
                for c in "ACGT":
                    nxt.add(s[:i] + c + s[i:])              # insertion
            for i in range(len(s)):
                nxt.add(s[:i] + s[i + 1:])                  # deletion
                for c in "ACGT":
                    if c != s[i]:
                        nxt.add(s[:i] + c + s[i + 1:])      # substitution
        nxt -= seen
        seen |= nxt
        frontier = nxt
    return seen


def main(argv):
    args = list(argv[1:])
    expect = None
    if "--expect-size" in args:
        k = args.index("--expect-size")
        expect = int(args[k + 1])
        del args[k:k + 2]
    a_only = "--method-a-only" in args
    if a_only:
        args.remove("--method-a-only")
    path, n, d = args[0], int(args[1]), int(args[2])
    w = n // 2
    words = [l.strip() for l in open(path, encoding="ascii", errors="replace") if l.strip()]
    print("file: %s  n=%d d=%d w=floor(n/2)=%d  words=%d" % (path, n, d, w, len(words)))
    ok = True
    bad_fmt = [x for x in words if len(x) != n or set(x) - set("ACGT")]
    if bad_fmt:
        print("format: %d words are not length-%d words over ACGT, e.g. %r" % (len(bad_fmt), n, bad_fmt[0]))
        ok = False
    else:
        print("format: all %d words are length %d over ACGT" % (len(words), n))
    bad_gc = [x for x in words if not bad_fmt and sum(c in "GC" for c in x) != w]
    if bad_gc:
        print("GC weight: %d words do not have exactly %d letters from {G,C}, e.g. %s" % (len(bad_gc), w, bad_gc[0]))
        ok = False
    elif not bad_fmt:
        print("GC weight: every word has exactly %d letters from {G,C}" % w)
    dups = len(words) - len(set(words))
    print("distinct: %s" % ("yes" if dups == 0 else "%d duplicate lines" % dups))
    if dups:
        ok = False
    if expect is not None:
        print("size: %d (expected %d) %s" % (len(words), expect, "ok" if len(words) == expect else "MISMATCH"))
        if len(words) != expect:
            ok = False
    if bad_fmt or dups:
        print("FAIL")
        return 1
    # method A
    viol_a = set()
    mn_pair = mn_rc = None
    for i, j in itertools.combinations(range(len(words)), 2):
        x, y = words[i], words[j]
        a = lev(x, y)
        mn_pair = a if mn_pair is None else min(mn_pair, a)
        if a < d:
            viol_a.add(("pair", i, j))
    for i, j in itertools.product(range(len(words)), repeat=2):
        b = lev(words[i], rc(words[j]))
        mn_rc = b if mn_rc is None else min(mn_rc, b)
        if b < d:
            viol_a.add(("rc", min(i, j), max(i, j)))
    npairs = len(words) * (len(words) - 1) // 2
    print("method A (DP Levenshtein): %d distinct pairs, min d(x,y) = %s; %d ordered pairs incl. x=y, min d(x,rc(y)) = %s"
          % (npairs, mn_pair, len(words) ** 2, mn_rc))
    if a_only:
        print("method B skipped (--method-a-only); method A: %d violations" % len(viol_a))
        viol_b = set(viol_a)
    else:  # method B
        viol_b = set()
        r1 = (d - 1) // 2
        r2 = d - 1 - r1
        big = [ball(x, r2) for x in words]
        small = [ball(x, r1) for x in words]
        small_rc = [ball(rc(y), r1) for y in words]
        for i, j in itertools.combinations(range(len(words)), 2):
            if not big[i].isdisjoint(small[j]):
                viol_b.add(("pair", i, j))
        for i, j in itertools.product(range(len(words)), repeat=2):
            if not big[i].isdisjoint(small_rc[j]):
                viol_b.add(("rc", min(i, j), max(i, j)))
        print("method B (edit balls of radii %d and %d, meet in the middle): %d violations; method A: %d violations" % (r2, r1, len(viol_b), len(viol_a)))
    if viol_a != viol_b:
        print("methods A and B DISAGREE")
        print("FAIL")
        return 1
    if not a_only:
        print("methods A and B agree")
    if viol_a:
        kind, i, j = sorted(viol_a)[0]
        x, y = words[i], words[j]
        print("first violation: %s, lines %d and %d (%s, %s): d(x,y)=%d d(x,rc y)=%d" %
              (kind, i + 1, j + 1, x, y, lev(x, y), lev(x, rc(y))))
        ok = False
    if not ok:
        print("NOT a valid (%d,%d,%d)_4 RC+GC edit-metric DNA code" % (n, d, w))
        print("FAIL")
        return 1
    print("VALID: %d words, a (%d,%d,%d)_4 DNA code with edit distance, fixed GC weight and reverse-complement constraint"
          % (len(words), n, d, w))
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
