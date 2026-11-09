#!/usr/bin/env python3
"""Standalone checker for OEIS A316471 (number of locally disjoint rooted identity trees with n nodes).
Python 3 standard library only. Written for this package from the entry's definition:
  - a rooted tree is the multiset of its branches (subtrees at the root);
  - identity: the branches of every node are pairwise distinct (so a node's branches form a set);
  - locally disjoint: no two distinct branches of the same node have a branch in common;
  - both conditions hold at every node (recursively).
Each tree is kept as a canonical string "(" + sorted child strings + ")" and its set of child strings, so
pairwise disjointness is tested literally on the children's own branch sets.
Usage:
  verify_a316471.py VALUE_FILE        count n = 1..21, require a(1..20) = OEIS DATA and a(21) = value in VALUE_FILE
  verify_a316471.py --no-disjoint     negative control: drop the disjointness test; must give A004111, not DATA
"""
import sys

DATA = [1, 1, 1, 2, 3, 6, 11, 21, 43, 89, 185, 391, 840, 1822, 3975, 8727, 19280, 42841, 95661, 214490]  # a(1..20)
A004111 = [1, 1, 1, 2, 3, 6, 12, 25, 52, 113, 247, 548, 1226, 2770, 6299, 14426]  # rooted identity trees, n = 1..16


def count(nmax, disjoint=True):
    # trees: list over all stored trees, in nondecreasing size: (size, canon, frozenset(child canons))
    trees = []
    out = []
    for n in range(1, nmax + 1):
        if n == 1:
            new = [(1, "()", frozenset())]
            out.append(1)
            trees.extend(new)
            continue
        last = n == nmax
        found = 0
        new = []
        tot = len(trees)
        chosen = []

        def rec(rem, start):
            nonlocal found
            if rem == 0:
                found += 1
                if not last:
                    kids = sorted(trees[i][1] for i in chosen)
                    new.append((n, "(" + "".join(kids) + ")", frozenset(kids)))
                return
            for i in range(start, tot):  # strictly increasing index = pairwise distinct branches
                s, _, gk = trees[i]
                if s > rem:
                    break
                if disjoint and any(not gk.isdisjoint(trees[j][2]) for j in chosen):
                    continue
                chosen.append(i)
                rec(rem - s, i + 1)
                chosen.pop()

        rec(n - 1, 0)
        if not last:
            canons = set(t[1] for t in new)
            if len(canons) != len(new):
                raise SystemExit("internal error: duplicate canonical forms at n=%d" % n)
        trees.extend(new)
        out.append(found)
    return out


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--no-disjoint":
        got = count(16, disjoint=False)
        print("control (no disjointness) a(1..16):", got)
        print("control equals A004111:", got == A004111)
        same = got == DATA[:16]
        print("control equals A316471 DATA:", same)
        sys.exit(0 if same else 1)  # exit 1 = control differs from DATA (expected)
    want = int(open(sys.argv[1]).read().strip().split("=")[-1])
    got = count(21)
    for n, v in enumerate(got, 1):
        print(n, v)
    ok = got[:20] == DATA
    print("a(1..20) equal OEIS DATA" if ok else "a(1..20) DIFFER from OEIS DATA")
    print("computed a(21) = %d; object says %d" % (got[20], want))
    sys.exit(0 if ok and got[20] == want else 1)


if __name__ == "__main__":
    main()
