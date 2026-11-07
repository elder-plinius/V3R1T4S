#!/usr/bin/env python3
"""Term accounting for the two slices of rebuild_lita_slices.py, N x N x N -> (N-1) x N x N -> (N-1) x (N-1) x N.

Counts, directly from the factor supports, how many terms each slice kills (a term vanishes in a slice when its factor
on one side is an outer product with the slice direction on that side), compares the counts with the ranks the
rebuild printed, and gives the baselines of plain coordinate projections (delete one index, drop the terms whose factor
becomes zero, no reductions). It does not redo the 2-reductions; it reads their results from the saved step JSONs.

Usage: slice_accounting.py lita_N.json step1.json step2.json   (the three files the commands in COMMANDS.md write)
Needs the engine's JSON loader only (python-flint is imported by engine.py but not used here).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
from collections import Counter
from engine import load_json

S = load_json(sys.argv[1]); S1 = load_json(sys.argv[2]); S2 = load_json(sys.argv[3])
N = S[0]
assert S[:3] == (N, N, N) and N % 2 == 1
terms = S[3]
r0, r1, r2 = len(terms), len(S1[3]), len(S2[3])
print("input <%d,%d,%d> rank %d" % (N, N, N, r0))

def rows_of(f, cols): return {i // cols for i in f}
def cols_of(f, cols): return {i % cols for i in f}

# ---- plain coordinate projections
# axis 0 (row i0 of A and C): a term vanishes iff U lives in row i0 or W lives in row i0
# axis 1 (column j0 of A, row j0 of B): a term vanishes iff U lives in column j0 or V lives in row j0
per0 = [(rows_of(t[0], N), rows_of(t[2], N)) for t in terms]
van0 = [sum(1 for ur, wr in per0 if ur == {i} or wr == {i}) for i in range(N)]
b0 = max(range(N), key=lambda i: van0[i])
print("\n[coordinate projection, %d^3 -> %dx%dx%d] best row: delete index %d -> %d terms (%d vanish); vanishing counts over all rows: %s"
      % (N, N - 1, N, N, b0, r0 - van0[b0], van0[b0], sorted(set(van0))))
best = None
rowsets = [{} for _ in terms]
for k, t in enumerate(terms):
    d = {}
    for idx in t[0]:
        d.setdefault(idx // N, set()).add(idx % N)
    rowsets[k] = d
vr = [rows_of(t[1], N) for t in terms]
wr = [rows_of(t[2], N) for t in terms]
for i in range(N):
    cnt = Counter(); alive = 0
    for k in range(len(terms)):
        d = rowsets[k]
        if set(d) == {i} or wr[k] == {i}:
            continue
        alive += 1
        cu = set()
        for r, cs in d.items():
            if r != i: cu |= cs
        kill_cols = set()
        if len(cu) == 1: kill_cols |= cu
        if len(vr[k]) == 1: kill_cols |= vr[k]
        for j in kill_cols: cnt[j] += 1
    for j in range(N):
        cand = (alive - cnt[j], i, j)
        if best is None or cand < best: best = cand
print("[coordinate projection, %d^3 -> %dx%dx%d] best pair: delete row %d and column %d -> %d terms (%d vanish)"
      % (N, N - 1, N - 1, N, best[1], best[2], best[0], r0 - best[0]))

# ---- the slices
star_val = -(N - 5) // 2
mid = (N - 1) // 2
star = tuple(F(star_val) if i == mid else F(1) for i in range(N))
unit = tuple(F(int(i == 0)) for i in range(N))
print("\nstar vector e*: entry %s at index %d, 1 elsewhere; e_0 = unit vector at index 0" % (star[mid], mid))

def is_outer_left(f, rows, cols, vec):
    """f == vec x^T for some x (each column of f is a multiple of vec)."""
    byc = {}
    for idx, c in f.items():
        r, cc = divmod(idx, cols)
        byc.setdefault(cc, {})[r] = c
    for cc, col in byc.items():
        r0_ = next(iter(col))
        if not vec[r0_]: return False
        lam = col[r0_] / vec[r0_]
        for r in range(rows):
            if col.get(r, 0) != lam * vec[r]: return False
    return True

def is_outer_right(f, rows, cols, vec):
    """f == x vec^T (each row of f is a multiple of vec)."""
    byr = {}
    for idx, c in f.items():
        r, cc = divmod(idx, cols)
        byr.setdefault(r, {})[cc] = c
    for r, row in byr.items():
        c0 = next(iter(row))
        if not vec[c0]: return False
        lam = row[c0] / vec[c0]
        for cc in range(cols):
            if row.get(cc, 0) != lam * vec[cc]: return False
    return True

n1, n2, n3 = S[:3]
kU = {k for k, t in enumerate(terms) if is_outer_left(t[0], n1, n2, star)}
kW = {k for k, t in enumerate(terms) if is_outer_left(t[2], n1, n3, unit)}
print("\nstep 1, slice axis 0 (row index shared by A and C), e = e* on A, f = e_0 on C:")
print("  terms with U = e* x^T (killed on the A side): %d; with W = e_0 y^T (killed on the C side): %d; both: %d; total %d"
      % (len(kU), len(kW), len(kU & kW), len(kU | kW)))
after1 = r0 - len(kU | kW)
print("  after the slice: <%d,%d,%d> rank %d  (%d - %d = %d)" % (N - 1, N, N, after1, r0, len(kU | kW), after1))
print("  2-reduction(s) (saved step1.json): removed %d -> rank %d" % (after1 - r1, r1))
assert S1[:3] == (N - 1, N, N)
T1 = S1[3]
m1, m2, m3 = S1[:3]
def surv_axis1(T, n2_, n3_, j0):
    return sum(1 for t in T if not (cols_of(t[0], n2_) == {j0} or rows_of(t[1], n3_) == {j0}))
v1 = [len(T1) - surv_axis1(T1, m2, m3, j) for j in range(m2)]
bj = max(range(m2), key=lambda j: v1[j])
print("\n[coordinate projection, %dx%dx%d:%d -> %dx%dx%d] best column: delete index %d -> %d terms (%d vanish); range of vanishing counts over all columns: (%d, %d)"
      % (m1, m2, m3, r1, m1, m2 - 1, m3, bj, r1 - v1[bj], v1[bj], min(v1), max(v1)))
kU2 = {k for k, t in enumerate(T1) if is_outer_right(t[0], m1, m2, unit)}
kV2 = {k for k, t in enumerate(T1) if is_outer_left(t[1], m2, m3, star)}
print("\nstep 2, slice axis 1 (column index of A = row index of B), e = e_0 on A, f = e* on B:")
print("  terms with U = x e_0^T (killed on the A side): %d; with V = e* y^T (killed on the B side): %d; both: %d; total %d"
      % (len(kU2), len(kV2), len(kU2 & kV2), len(kU2 | kV2)))
after2 = r1 - len(kU2 | kV2)
print("  after the slice: <%d,%d,%d> rank %d  (%d - %d = %d)" % (N - 1, N - 1, N, after2, r1, len(kU2 | kV2), after2))
print("  2-reduction(s) (saved step2.json): removed %d -> rank %d" % (after2 - r2, r2))
assert S2[:3] == (N - 1, N - 1, N)
print("\nsummary: %d -[slice 1 kills %d]-> %d -[2-reduction]-> %d -[slice 2 kills %d]-> %d -[2-reduction]-> %d; total removed %d"
      % (r0, len(kU | kW), after1, r1, len(kU2 | kV2), after2, r2, r0 - r2))
print("closed forms: step 1 removes (N^2+3N)/2 = %d (measured %d); step 2 removes (N^2+2N-1)/2 = %d (measured %d)"
      % ((N * N + 3 * N) // 2, r0 - r1, (N * N + 2 * N - 1) // 2, r1 - r2))
