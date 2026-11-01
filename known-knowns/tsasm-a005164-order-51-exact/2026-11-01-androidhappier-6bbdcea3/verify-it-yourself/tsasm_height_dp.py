#!/usr/bin/env python3
"""Standalone exact counter for A005164: totally symmetric (D4-invariant) ASMs of order N = 2n+1.
Python 3 standard library only, exact big integers, no modular arithmetic.

Reduction (height functions, standard ASM <-> six-vertex bijection):
  For an N x N ASM A let c(i,j) = sum of A[k][l] over k < i, l < j, for 0 <= i,j <= N, and H(i,j) = i + j - 2 c(i,j).
  A is an ASM exactly when H has |difference| = 1 between horizontally or vertically adjacent points, with
  boundary H(0,j) = j, H(i,0) = i, H(N,j) = N - j, H(i,N) = N - i.
  Transpose of A  <=>  H(i,j) = H(j,i).   Reversing the row order of A  <=>  H(i,j) = N - H(N-i,j).
  These two generate D4, so A is a TSASM iff H has both symmetries. With N = 2n+1 the second one forces
  |2 H(n,j) - N| = 1 on row n, i.e. H(n,j) in {n, n+1}, and parity H(i,j) = i+j (mod 2) pins H(n,j) = n + (j mod 2).
  By transpose the same holds on column n. So a(n) = number of H on the triangle 0 <= i <= j <= n with unit steps
  along every grid edge inside it, H(0,j) = j (top row) and H(i,n) = n + (i mod 2) (right column); the diagonal
  points need no extra condition (symmetry identifies the two cells on either side of it).
Sweep: column by column (j = 0..n), each column filled top to bottom (i = 0..j); the state is the current column
profile. Pruning only by the exact Lipschitz bound |H(i,j) - H(i,n)| <= n - j.
Usage: python3 tsasm_height_dp.py NMIN NMAX   -> prints "n a(n)" lines."""
import sys


def count(n):
    right = [n + (i % 2) for i in range(n + 1)]          # forced H(i, n)
    col = {(0,): 1}                                       # column j=0 restricted to the triangle: H(0,0)=0
    for j in range(1, n + 1):
        # profile while filling column j: entries 0..i-1 are column j (new), entries i..j-1 are column j-1 (old)
        prof = {}
        for s, c in col.items():
            key = (j,) + s[1:]                            # H(0,j) = j (top boundary)
            prof[key] = prof.get(key, 0) + c
        for i in range(1, j + 1):
            nxt = {}
            for s, c in prof.items():
                up = s[i - 1]                             # H(i-1, j), already new
                for v in (up - 1, up + 1):
                    if i < j and abs(v - s[i]) != 1:      # left neighbour H(i, j-1) (old column)
                        continue
                    if abs(v - right[i]) > n - j:         # must still reach the forced column n
                        continue
                    key = s[:i] + (v,) + s[i + 1:]        # for i == j this appends the diagonal point
                    nxt[key] = nxt.get(key, 0) + c
            prof = nxt
        col = prof
    total = 0
    for s, c in col.items():
        if list(s) != right:
            raise SystemExit("internal error: final column does not match the forced boundary")
        total += c
    return total


if __name__ == "__main__":
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    for n in range(lo, hi + 1):
        print(n, count(n), flush=True)
