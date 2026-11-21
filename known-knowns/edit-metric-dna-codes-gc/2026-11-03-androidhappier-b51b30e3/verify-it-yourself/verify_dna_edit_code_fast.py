#!/usr/bin/env python3
"""Faster standalone checker for Sun-type (n, d, w)_4 DNA edit-metric codes, written from the definition
(J. Sun, M.Sc. thesis, Brock University 2010, Sec. 1.5): words over {A,C,G,T} of length n, GC weight exactly
w = floor(n/2), Levenshtein (edit) distance d(x, y) >= d for all distinct codewords x, y, and
d(x, rc(y)) >= d for ALL codewords x, y INCLUDING x = y (rc = Watson-Crick reverse complement, A<->T, C<->G).

Same definition and the same two methods as the family checker verify_dna_edit_code.py, made fast enough for codes
with about a thousand words in pure Python:
  A: exact Levenshtein distance (substitution, insertion, deletion, each cost 1) for all distinct pairs and ALL
     ordered pairs (x, rc(y)) including x = y, computed with the bit-parallel form of the dynamic-programming
     recurrence (Myers 1999 / Hyyroe 2001); before use it is compared with the plain DP on random strings
     (self-test, printed);
  B: explicit edit balls, met in the middle via a hash index: with r1 = floor((d-1)/2) and r2 = d-1-r1, ball(u, r)
     is the set of ALL strings (any length) reachable from u by at most r single insertions/deletions/substitutions
     (breadth-first search). d(u, v) <= d-1 iff ball(u, r2) and ball(v, r1) intersect. Every string of every
     radius-r1 ball (of every codeword and of every reverse complement) is put in a dictionary; every string of every
     radius-r2 ball of a codeword is looked up in it. A violation is any pair of distinct codewords, or any codeword
     and any rc(y) (y = x included), whose balls meet.
A and B must report the same set of violations. Python 3 standard library only.

usage: verify_dna_edit_code_fast.py FILE n d [--expect-size K] [--method-a-only]
Prints VALID / NOT VALID details and, as last line, PASS or FAIL (exit code 0 / 1).
"""
import sys
import random
from collections import defaultdict

COMP = {"A": "T", "T": "A", "C": "G", "G": "C"}


def rc(x):
    return "".join(COMP[c] for c in reversed(x))


def lev_dp(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb))
        prev = cur
    return prev[-1]


def peq_of(a):
    p = {"A": 0, "C": 0, "G": 0, "T": 0}
    for i, c in enumerate(a):
        p[c] = p.get(c, 0) | (1 << i)
    return p


def lev_bp(peq, m, b):
    """Levenshtein distance between the length-m string described by peq and the string b (bit-parallel DP)."""
    if m == 0:
        return len(b)
    mask = (1 << m) - 1
    hb = 1 << (m - 1)
    pv, mv, score = mask, 0, m
    for c in b:
        eq = peq.get(c, 0)
        xv = eq | mv
        xh = ((((eq & pv) + pv) & mask) ^ pv) | eq
        ph = mv | (~(xh | pv) & mask)
        mh = pv & xh
        if ph & hb:
            score += 1
        elif mh & hb:
            score -= 1
        ph = ((ph << 1) | 1) & mask
        mh = (mh << 1) & mask
        pv = mh | (~(xv | ph) & mask)
        mv = ph & xv
    return score


def self_test():
    rnd = random.Random(12345)
    bad = 0
    for _ in range(20000):
        a = "".join(rnd.choice("ACGT") for _ in range(rnd.randint(0, 11)))
        b = "".join(rnd.choice("ACGT") for _ in range(rnd.randint(0, 11)))
        if lev_bp(peq_of(a), len(a), b) != lev_dp(a, b):
            bad += 1
    return bad


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
    st = self_test()
    print("self-test: bit-parallel Levenshtein vs plain DP on 20000 random string pairs (lengths 0-11): %d mismatches" % st)
    if st:
        print("FAIL")
        return 1
    k = len(words)
    rcs = [rc(x) for x in words]
    # method A
    viol_a = set()
    mn_pair = mn_rc = None
    for i in range(k):
        p, m = peq_of(words[i]), len(words[i])
        for j in range(i + 1, k):
            a = lev_bp(p, m, words[j])
            if mn_pair is None or a < mn_pair:
                mn_pair = a
            if a < d:
                viol_a.add(("pair", i, j))
        for j in range(k):
            b = lev_bp(p, m, rcs[j])
            if mn_rc is None or b < mn_rc:
                mn_rc = b
            if b < d:
                viol_a.add(("rc", min(i, j), max(i, j)))
    print("method A (bit-parallel DP Levenshtein): %d distinct pairs, min d(x,y) = %s; %d ordered pairs incl. x=y, "
          "min d(x,rc(y)) = %s" % (k * (k - 1) // 2, mn_pair, k * k, mn_rc))
    if a_only:
        print("method B skipped (--method-a-only); method A: %d violations" % len(viol_a))
        viol_b = set(viol_a)
    else:
        viol_b = set()
        r1 = (d - 1) // 2
        r2 = d - 1 - r1
        idx_w = defaultdict(list)
        idx_r = defaultdict(list)
        for j in range(k):
            for s in ball(words[j], r1):
                idx_w[s].append(j)
            for s in ball(rcs[j], r1):
                idx_r[s].append(j)
        for i in range(k):
            for s in ball(words[i], r2):
                for j in idx_w.get(s, ()):
                    if j != i:
                        viol_b.add(("pair", min(i, j), max(i, j)))
                for j in idx_r.get(s, ()):
                    viol_b.add(("rc", min(i, j), max(i, j)))
        print("method B (edit balls of radii %d and %d, hash index, meet in the middle): %d violations; method A: %d violations"
              % (r2, r1, len(viol_b), len(viol_a)))
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
              (kind, i + 1, j + 1, x, y, lev_dp(x, y), lev_dp(x, rc(y))))
        ok = False
    if not ok:
        print("NOT a valid (%d,%d,%d)_4 RC+GC edit-metric DNA code" % (n, d, w))
        print("FAIL")
        return 1
    print("VALID: %d words, a (%d,%d,%d)_4 DNA code with edit distance, fixed GC weight and reverse-complement constraint"
          % (k, n, d, w))
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
