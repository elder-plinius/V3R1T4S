#!/usr/bin/env python3
"""Rebuild object/square_n28_3324.txt from its published factors and check the rebuild is exact.

Run from the package folder: python3 how-we-built-it/rebuild_object.py

Factor A: the order-2 Latin square (unique up to isotopy)  0 1 / 1 0
Factor B: the order-14 Latin square published in OEIS A092237's proving list (a092237_2.txt),
          header "n=14, a(14)>=391". Its 14 rows are embedded below so this script is self-contained.

Product: P[(i1,i2)][(j1,j2)] = (A[i1][j1], B[i2][j2]), symbols relabelled by first occurrence to 0..27.
"""
import os, sys

A = [[0, 1], [1, 0]]

B14 = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    [1, 2, 0, 4, 3, 6, 5, 8, 7, 10, 9, 13, 11, 12],
    [2, 0, 1, 6, 5, 4, 3, 10, 9, 8, 7, 12, 13, 11],
    [3, 5, 4, 7, 0, 1, 2, 11, 12, 13, 6, 9, 8, 10],
    [4, 6, 3, 0, 8, 2, 1, 12, 11, 5, 13, 10, 7, 9],
    [5, 3, 6, 1, 2, 0, 4, 9, 13, 11, 12, 7, 10, 8],
    [6, 4, 5, 2, 1, 3, 0, 13, 10, 12, 11, 8, 9, 7],
    [7, 9, 8, 11, 12, 13, 10, 3, 0, 1, 2, 5, 4, 6],
    [8, 10, 7, 12, 11, 9, 13, 0, 4, 2, 1, 6, 3, 5],
    [9, 7, 10, 5, 13, 11, 12, 1, 2, 0, 8, 3, 6, 4],
    [10, 8, 9, 13, 6, 12, 11, 2, 1, 7, 0, 4, 5, 3],
    [11, 12, 13, 10, 9, 8, 7, 6, 5, 4, 3, 0, 1, 2],
    [12, 13, 11, 8, 7, 10, 9, 4, 3, 6, 5, 2, 0, 1],
    [13, 11, 12, 9, 10, 7, 8, 5, 6, 3, 4, 1, 2, 0],
]

def product(A, B):
    m, k = len(A), len(B)
    return [[(A[i1][j1], B[i2][j2]) for j1 in range(m) for j2 in range(k)]
            for i1 in range(m) for i2 in range(k)]

def relabel(L):
    syms = {}
    out = []
    for row in L:
        r = []
        for s in row:
            if s not in syms:
                syms[s] = len(syms)
            r.append(syms[s])
        out.append(r)
    return out

rebuilt = relabel(product(A, B14))
claimed_path = os.path.join('object', 'square_n28_3324.txt')
claimed = [[int(t) for t in line.split()] for line in open(claimed_path) if line.strip()]
match = rebuilt == claimed
print("rebuild size:", len(rebuilt), "x", len(rebuilt[0]))
print("rebuild equals object/square_n28_3324.txt:", match)
print("PASS" if match else "FAIL")
sys.exit(0 if match else 1)
