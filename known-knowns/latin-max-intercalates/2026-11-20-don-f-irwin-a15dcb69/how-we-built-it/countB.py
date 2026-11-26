#!/usr/bin/env python3
"""Counter B: independent intercalate counter, different algorithm.

Instead of the definition's row-pair/column scan, this builds for every unordered pair of rows the permutation
sigma = row_r^{-1} o row_r' and counts its 2-cycles (transpositions). An intercalate between rows r and r' is
exactly a transposition of that permutation: a 2x2 subsquare {c1,c2} x {r,r'}.

Written independently of Counter A so that a bug in one does not hide in the other.
"""
import sys, json

def load_sq(path):
    rows = []
    for line in open(path):
        toks = line.split()
        if toks:
            rows.append([int(t) for t in toks])
    n = len(rows)
    assert all(len(r) == n for r in rows)
    return rows

def count_by_transpositions(L):
    n = len(L)
    total = 0
    for r in range(n):
        for rr in range(r+1, n):
            # sigma[c] = position in row rr of symbol L[r][c]; count c < sigma[c] with sigma[sigma[c]] == c
            inv_rr = [0]*n
            for c in range(n):
                inv_rr[L[rr][c]] = c
            sigma = [inv_rr[L[r][c]] for c in range(n)]
            t = 0
            for c in range(n):
                s = sigma[c]
                if c < s and sigma[s] == c:
                    t += 1
            total += t
    return total

def latin_check(L):
    n = len(L)
    return all(set(r) == set(range(n)) for r in L) and all(len({L[r][c] for r in range(n)}) == n for c in range(n))

def main():
    L = load_sq(sys.argv[1])
    print(json.dumps({"file": sys.argv[1], "n": len(L), "latin": latin_check(L),
                      "intercalates": count_by_transpositions(L)}))

if __name__ == "__main__":
    main()
