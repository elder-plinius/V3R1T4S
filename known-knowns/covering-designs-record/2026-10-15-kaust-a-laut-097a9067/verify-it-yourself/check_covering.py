"""Standalone checker for a (v,k,t) covering design, written from the definition (Python standard library only).

Definition: a (v,k,t)-covering design is a collection of k-element subsets (blocks) of {1,...,v} such that every
t-element subset of {1,...,v} is contained in at least one block.

usage: python check_covering.py v k t blocks.txt expected_blocks expected_sha256
Checks: the file's sha256; the number of blocks; every block has exactly k distinct integers in 1..v; blocks are
pairwise distinct; EVERY t-subset of {1..v} lies in some block (exhaustive enumeration, no sampling); the block count
is at least the Schonheim bound. Prints PASS or FAIL as its last line."""
import hashlib
import sys
from itertools import combinations
from math import comb


def schonheim(v, k, t):
    # L(v,k,1) = ceil(v/k); L(v,k,t) = ceil(v/k * L(v-1,k-1,t-1)), exact integer arithmetic
    if t == 0:
        return 1
    inner = schonheim(v - 1, k - 1, t - 1)
    return -(-v * inner // k)


def main():
    v, k, t = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    path, want_b, want_sha = sys.argv[4], int(sys.argv[5]), sys.argv[6].lower()
    raw = open(path, 'rb').read()
    ok = True
    sha = hashlib.sha256(raw).hexdigest()
    print('sha256', sha, 'matches' if sha == want_sha else 'MISMATCH')
    ok &= sha == want_sha
    blocks = []
    for n, line in enumerate(raw.decode('ascii').splitlines(), 1):
        if not line.strip():
            continue
        pts = [int(x) for x in line.split()]
        if len(pts) != k or len(set(pts)) != k or min(pts) < 1 or max(pts) > v:
            print('bad block on line', n, pts)
            ok = False
        blocks.append(frozenset(pts))
    print('blocks', len(blocks), 'expected', want_b, 'distinct', len(set(blocks)))
    ok &= len(blocks) == want_b and len(set(blocks)) == len(blocks)
    masks = [sum(1 << p for p in b) for b in blocks]
    total = comb(v, t)
    missing = 0
    for T in combinations(range(1, v + 1), t):
        m = 0
        for p in T:
            m |= 1 << p
        if not any(b & m == m for b in masks):
            missing += 1
    print('t-subsets', total, 'uncovered', missing)
    ok &= missing == 0
    L = schonheim(v, k, t)
    print('Schonheim bound', L, 'blocks >= bound', len(blocks) >= L)
    ok &= len(blocks) >= L
    print('PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
