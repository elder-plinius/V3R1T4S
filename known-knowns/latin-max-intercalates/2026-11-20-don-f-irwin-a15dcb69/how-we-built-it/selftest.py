#!/usr/bin/env python3
"""Selftest for countA.py and countB.py.

Known positive: the n=4 elementary abelian 2-group table (0-1-2-3 / 1-0-3-2 / 2-3-0-1 / 3-2-1-0) has 12
intercalates -- the published A092237 a(4)=12.
Known negative: a cyclic Latin square of order 4 has 0 intercalates (all row permutations are 4-cycles).
Exhaustive cross-check: for n=3,4,5 enumerate ALL Latin squares and compare the maximum against published
a(3)=0, a(4)=12, a(5)=4; also verify both counters agree on every square enumerated.
"""
import itertools, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from countA import count_intercalates, is_latin
from countB import count_by_transpositions

def cyclic(n):
    return [[(r+c) % n for c in range(n)] for r in range(n)]

def group4():
    return [[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]]

fails = []

# 1. known positive
c = count_intercalates(group4())
print(f"known positive: n=4 group table intercalates A={c} B={count_by_transpositions(group4())} (expect 12)")
if c != 12: fails.append("positive 12")
if count_by_transpositions(group4()) != 12: fails.append("positive B 12")

# 2. known negative: odd-order cyclic square has no intercalate (row differences are odd-order permutations)
c = count_intercalates(cyclic(5))
print(f"known negative: cyclic n=5 intercalates A={c} B={count_by_transpositions(cyclic(5))} (expect 0)")
if c != 0: fails.append("negative 0")

# 2b. hand-verified positive: cyclic n=4 has exactly 4 (rows {0,2} and {1,3} each give 2 intercalates).
#     My first draft of this selftest wrongly expected 0 here; the counters were right.
c = count_intercalates(cyclic(4))
print(f"hand-checked: cyclic n=4 intercalates A={c} B={count_by_transpositions(cyclic(4))} (expect 4)")
if c != 4: fails.append("cyclic4 4")

# 3. exhaustive Latin square enumeration n=3,4,5; counters must agree everywhere
#    Enumerate row by row: each row is a permutation, first row fixed WLOG for the MAXIMUM only.
def latin_squares(n):
    perms = list(itertools.permutations(range(n)))
    def rec(rows):
        if len(rows) == n:
            yield rows
            return
        used = [set(rows[r][c] for r in range(len(rows))) for c in range(n)]
        for p in perms:
            if all(p[c] not in used[c] for c in range(n)):
                yield from rec(rows + [list(p)])
    yield from rec([])

for n in (3,4,5):
    best = -1
    cnt = 0
    mismatch = 0
    for sq in latin_squares(n):
        cnt += 1
        a = count_intercalates(sq)
        b = count_by_transpositions(sq)
        if a != b: mismatch += 1
        best = max(best, a)
    print(f"exhaustive n={n}: {cnt} Latin squares, max intercalates {best}, A/B mismatches {mismatch}")
    if mismatch: fails.append(f"mismatch n={n}")
    expected = {3:0, 4:12, 5:4}[n]
    if best != expected: fails.append(f"max n={n} got {best} expect {expected}")

print("SELFTEST:", "PASS" if not fails else "FAIL " + str(fails))
sys.exit(0 if not fails else 1)
