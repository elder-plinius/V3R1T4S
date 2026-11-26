#!/usr/bin/env python3
"""Standalone checker, standard library only. Run from the package folder:
    python3 verify-it-yourself/run_checks.py

Checks, from the definition and with no import of the author's counters:
 1. object/square_n28_3324.txt is an order-28 Latin square (every row and column is a permutation of 0..27);
 2. its intercalate count is 3324, counted twice by two independent methods written here;
 3. 3324 is strictly greater than the bar 2940 and at most the proven bound 28*28*27/4 = 5292.
Prints PASS or FAIL as its last line.
"""
import os, sys

OBJ = os.path.join('object', 'square_n28_3324.txt')
BAR = 2940
N = 28
BOUND = N * N * (N - 1) // 4  # Heinrich-Wallis even-order bound
EXPECTED = 3324

def load(path):
    rows = []
    for line in open(path):
        toks = line.split()
        if toks:
            rows.append([int(t) for t in toks])
    return rows

def is_latin(L):
    n = len(L)
    if n != N or any(len(r) != N for r in L):
        return False
    syms = set(range(N))
    for r in L:
        if set(r) != syms:
            return False
    for c in range(N):
        if {L[r][c] for r in range(N)} != syms:
            return False
    return True

def count_by_2x2_blocks(L):
    """Literal definition: a 2x2 subsquare is an intercalate iff its two rows and two columns form a Latin
    square of order 2, i.e. the four entries are exactly two symbols each appearing twice (pattern a,b,b,a)."""
    n = len(L)
    total = 0
    for r in range(n):
        for rr in range(r + 1, n):
            for c in range(n):
                for cp in range(c + 1, n):
                    a, b = L[r][c], L[r][cp]
                    if a != b and L[rr][c] == b and L[rr][cp] == a:
                        total += 1
    return total

def count_by_permutation_cycles(L):
    """Second, independent method: for each row pair the permutation taking row r to row rr has a 2-cycle at
    (c, cp) exactly when those two columns form an intercalate. Count all 2-cycles."""
    n = len(L)
    total = 0
    for r in range(n):
        inv = {L[rr][c]: c for c in range(n)} if False else None
        for rr in range(r + 1, n):
            inv = [0] * n
            for c in range(n):
                inv[L[rr][c]] = c
            sigma = [inv[L[r][c]] for c in range(n)]
            total += sum(1 for c in range(n) if c < sigma[c] and sigma[sigma[c]] == c)
    return total

def main():
    if not os.path.exists(OBJ):
        print("FAIL: missing", OBJ)
        return 1
    L = load(OBJ)
    latin = is_latin(L)
    a = count_by_2x2_blocks(L)
    b = count_by_permutation_cycles(L)
    print("order:", len(L))
    print("latin:", latin)
    print("intercalates (2x2-block method):", a)
    print("intercalates (permutation-cycle method):", b)
    print("bar:", BAR, "| proven bound:", BOUND)
    ok = (latin and a == EXPECTED and b == EXPECTED and a == b
          and a > BAR and a <= BOUND)
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.exit(main())
