#!/usr/bin/env python3
"""Counter A: intercalates in a Latin square, O(n^3), direct definition.

Definition (bank/targets.json verification_method): for each pair of rows r < r' and each column c,
let c' be the column where row r' has the symbol L[r][c]; count when L[r'][c] = L[r][c'] and c < c'.
This is the literal definition. It does not assume the square is Latin.
"""
import sys, json

def load_sq(path):
    rows = []
    for line in open(path):
        toks = line.split()
        if not toks:
            continue
        rows.append([int(t) for t in toks])
    n = len(rows)
    assert all(len(r) == n for r in rows), "not square"
    return rows

def is_latin(L):
    n = len(L)
    syms = set(range(n))
    for r in L:
        if set(r) != syms:
            return False
    for c in range(n):
        if set(L[r][c] for r in range(n)) != syms:
            return False
    return True

def count_intercalates(L):
    n = len(L)
    # pos[r][s] = column of symbol s in row r
    pos = [[0]*n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            pos[r][L[r][c]] = c
    total = 0
    for r in range(n):
        for rr in range(r+1, n):
            rowr, rowrr = L[r], L[rr]
            for c in range(n):
                cp = pos[rr][rowr[c]]
                if rowrr[c] == rowr[cp] and c < cp:
                    total += 1
    return total

def main():
    path = sys.argv[1]
    L = load_sq(path)
    n = len(L)
    latin = is_latin(L)
    cnt = count_intercalates(L)
    print(json.dumps({"file": path, "n": n, "latin": latin, "intercalates": cnt}))

if __name__ == "__main__":
    main()
