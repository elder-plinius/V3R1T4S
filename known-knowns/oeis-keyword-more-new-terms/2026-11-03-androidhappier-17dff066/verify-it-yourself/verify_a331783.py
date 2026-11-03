#!/usr/bin/env python3
"""Standalone checker for OEIS A331783 (locally disjoint rooted semi-identity trees with n unlabeled vertices).

Written from the entry's definition (name, comments, Mathematica disjunsQ):
  a rooted tree is semi-identity if its non-leaf branches are pairwise distinct (leaf branches may repeat), and
  locally disjoint if no two distinct branches of any vertex share a common branch (Intersection of their branch
  lists is empty); both conditions hold at every vertex.
So a tree of size n is: k >= 0 leaf children plus a SET S of distinct non-leaf valid trees whose sets of branch
types are pairwise disjoint (the leaf counts as a type, so at most one member of S may itself have a leaf child),
with k + sum of sizes in S = n - 1. A single branch is always allowed.

Usage:  python3 verify_a331783.py [VALUE_FILE]   -> prints "n a(n)" for n = 1..21, compares with DATA and VALUE_FILE;
                                                     also checks a literal disjunsQ transcription agrees for n <= 11
        python3 verify_a331783.py --nodisj         -> negative control without local disjointness (must NOT match DATA;
                                                     exits 0 only if it reproduces DATA)
Python 3 standard library only.
"""
import sys

DATA = [1, 1, 2, 4, 8, 17, 37, 83, 191, 450, 1076, 2610, 6404, 15875, 39676, 99880, 253016, 644524, 1649918, 4242226]
N = 21


def count(N, disjoint=True, out=print):
    # tree ids: 0 = the one-vertex tree (leaf). types[i] = frozenset of distinct branch ids of tree i; sizes[i] = size.
    sizes = [1]
    types = [frozenset()]
    bigcount = {}
    out("1 1")
    res = [1]
    for n in range(2, N + 1):
        # non-leaf candidates are ids 1..len-1, sorted by size (nondecreasing) by construction
        limit = len(sizes)
        # Branch types are only needed for trees that can sit next to another non-leaf branch inside a tree of size
        # <= N, i.e. sizes <= N - 3. Bigger trees (sizes N-2, N-1) can only be the sole non-leaf branch, so for them
        # only their number is kept (bigcount) and added below. This keeps memory to a few hundred MB.
        store = n <= N - 3
        new_sizes = []
        new_types = []
        used = set()
        chosen = []
        cnt = 0

        def rec(minid, rem):
            nonlocal cnt
            cnt += 1                       # the current set S, remaining rem vertices become leaf children
            if store:
                t = set(chosen)
                if rem > 0:
                    t.add(0)
                new_sizes.append(n)
                new_types.append(frozenset(t))
            i = minid
            while i < limit and sizes[i] <= rem:
                ti = types[i]
                if not disjoint or used.isdisjoint(ti):
                    if disjoint:
                        used.update(ti)
                    chosen.append(i)
                    rec(i + 1, rem - sizes[i])
                    chosen.pop()
                    if disjoint:
                        used.difference_update(ti)
                i += 1

        rec(1, n - 1)
        for s_big, c_big in bigcount.items():
            if s_big <= n - 1:
                cnt += c_big                # S = {one tree of size s_big}, the rest leaves
        if not store:
            bigcount[n] = cnt
        sizes.extend(new_sizes)
        types.extend(new_types)
        out("%d %d" % (n, cnt))
        res.append(cnt)
    return res


def literal(nmax):
    """Direct transcription of the entry's Mathematica: trees as sorted tuples of branches; for every integer
    partition of n-1 take sorted tuples of valid trees and keep those passing disjunsQ (one branch, or non-leaf
    branches pairwise distinct and every two branches equal or with empty intersection)."""
    def parts(n, m):
        if n == 0:
            yield ()
            return
        for k in range(min(n, m), 0, -1):
            for p in parts(n - k, k):
                yield (k,) + p

    def disjuns(u):
        if len(u) == 1:
            return True
        nl = [b for b in u if b != ()]
        if len(set(nl)) != len(nl):
            return False
        return all(a == b or not (set(a) & set(b)) for a in u for b in u)

    def tuples(lists, start=0):
        # nondecreasing choices within equal-size blocks are handled by sorting + set
        if start == len(lists):
            yield ()
            return
        for x in lists[start]:
            for rest in tuples(lists, start + 1):
                yield (x,) + rest

    ld = {1: [()]}
    for n in range(2, nmax + 1):
        seen = set()
        for c in parts(n - 1, n - 1):
            for t in tuples([ld[k] for k in c]):
                seen.add(tuple(sorted(t)))
        ld[n] = [t for t in seen if disjuns(t)]
    return [len(ld[n]) for n in range(1, nmax + 1)]


def main():
    sys.setrecursionlimit(10000)
    if len(sys.argv) > 1 and sys.argv[1] == "--nodisj":
        r = count(16, disjoint=False, out=lambda s: None)
        print("nodisj control a(1..16):", r)
        sys.exit(0 if r == DATA[:16] else 1)
    L = literal(11)
    r = count(N)
    ok = True
    if L == r[:11]:
        print("literal Mathematica transcription equals the fast count for n = 1..11")
    else:
        print("literal transcription DIFFERS for n <= 11:", L); ok = False
    if r[:20] == DATA:
        print("a(1..20) equal OEIS DATA")
    else:
        print("a(1..20) DIFFER from OEIS DATA"); ok = False
    if len(sys.argv) > 1:
        line = open(sys.argv[1]).read().strip()
        want = int(line.split("=")[1])
        print("computed a(21) = %d; object says %d" % (r[20], want))
        ok = ok and r[20] == want
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
