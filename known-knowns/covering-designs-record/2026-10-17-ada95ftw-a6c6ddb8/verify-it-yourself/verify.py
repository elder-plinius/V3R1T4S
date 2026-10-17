#!/usr/bin/env python3
"""Standalone checker for a (v,k,t) covering design, written from the definition (Python 3 standard library only).
Definition: a (v,k,t) covering design is a collection of k-element subsets (blocks) of {1,...,v} such that every
t-element subset of {1,...,v} is contained in at least one block. C(v,k,t) is the minimum number of blocks.
Usage: verify.py v k t blockfile claimed_b
Checks: every line is k distinct integers in 1..v; the blocks are pairwise distinct; the number of blocks equals
claimed_b; EVERY t-subset (all C(v,t) of them, exhaustively) lies in some block; claimed_b >= Schonheim L(v,k,t).
Exit code 0 and last line 'VERIFIED C(v,k,t) <= b' only if everything holds."""
import sys, itertools, hashlib
from math import comb

def schonheim(v, k, t):
    # L(v,k,t) = ceil(v/k * L(v-1,k-1,t-1)), L(.,.,0) = 1, exact integer arithmetic
    if t == 0:
        return 1
    return -(-v * schonheim(v - 1, k - 1, t - 1) // k)

def main():
    v, k, t = map(int, sys.argv[1:4]); fn = sys.argv[4]; claimed = int(sys.argv[5])
    raw = open(fn, 'rb').read()
    print("sha256", hashlib.sha256(raw).hexdigest(), fn)
    bad = []; blocks = []
    for n, line in enumerate(raw.decode('ascii', 'replace').splitlines(), 1):
        if not line.strip():
            continue
        try:
            b = [int(x) for x in line.split()]
        except ValueError:
            bad.append(n); continue
        if len(b) != k or len(set(b)) != k or not all(1 <= x <= v for x in b):
            bad.append(n); continue
        blocks.append(frozenset(b))
    distinct = len(set(blocks))
    # exhaustive: test every t-subset for containment in some block
    uncovered = 0
    for s in itertools.combinations(range(1, v + 1), t):
        ss = set(s)
        if not any(ss <= b for b in blocks):
            uncovered += 1
    L = schonheim(v, k, t)
    print(f"v={v} k={k} t={t} blocks={len(blocks)} distinct={distinct} bad_lines={len(bad)} "
          f"t_subsets={comb(v, t)} uncovered={uncovered} schonheim={L}")
    ok = (not bad and distinct == len(blocks) == claimed and uncovered == 0 and claimed >= L)
    if ok:
        print(f"VERIFIED C({v},{k},{t}) <= {claimed}")
        return 0
    print("NOT VERIFIED")
    return 1

def selftest():
    # Fano plane is a (7,3,2) covering with 7 blocks; dropping a block must leave pairs uncovered.
    fano = [{1,2,3},{1,4,5},{1,6,7},{2,4,6},{2,5,7},{3,4,7},{3,5,6}]
    def unc(bl): return sum(1 for s in itertools.combinations(range(1, 8), 2) if not any(set(s) <= b for b in bl))
    assert unc(fano) == 0 and unc(fano[:-1]) == 3 and schonheim(7, 3, 2) == 7 and schonheim(20, 6, 3) == 64
    print("selftest: Fano covers (0 uncovered), Fano minus a block leaves 3 uncovered, L(7,3,2)=7, L(20,6,3)=64: OK")

if __name__ == '__main__':
    selftest()
    sys.exit(main())
