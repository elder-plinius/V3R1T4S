#!/usr/bin/env python3
"""Exact term accounting for <19,19,19>:3633 -> <18,19,19>:3424 -> <18,18,19>:3225, and what plain coordinate
projections give, from the same LITA scheme. Uses the run's engine (needs python-flint) only for restrict/absorb, and
re-derives the kill counts directly from the factor supports.

Usage: drop_accounting.py lita_19.json rebuilt.step2.json
Prints: coordinate-projection baselines; per step, how many terms each side of the slice kills (and overlap); each
2-reduction (factor pair used, term removed); and checks that the replayed result is identical to rebuilt.step2.json.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fractions import Fraction as F
import engine
from engine import load_json, restrict, absorb_once, PAIRS

src, ref = sys.argv[1], sys.argv[2]
S = load_json(src)
N = S[0]
terms = S[3]
print("input <%d,%d,%d> rank %d" % (N, N, N, len(terms)))

def rows_of(f, cols):
    return {i // cols for i in f}
def cols_of(f, cols):
    return {i % cols for i in f}

# ---------------- plain coordinate projections (delete one index; drop terms whose factor becomes zero; no reductions)
# axis 0 (row i0 of A and C): term vanishes iff U lives in row i0 or W lives in row i0
# axis 1 (column j0 of A, row j0 of B): term vanishes iff U lives in column j0 or V lives in row j0
def surv_axis0(T, n2, n3, i0):
    return [t for t in T if not (rows_of(t[0], n2) == {i0} or rows_of(t[2], n3) == {i0})]
def surv_axis1(T, n2, n3, j0):
    return [t for t in T if not (cols_of(t[0], n2) == {j0} or rows_of(t[1], n3) == {j0})]

best0 = min((len(surv_axis0(terms, N, N, i)), i) for i in range(N))
print("\n[coordinate projection, 19^3 -> 18x19x19] best row: delete index %d -> %d terms (%d vanish); other rows: %s"
      % (best0[1], best0[0], len(terms) - best0[0],
         sorted({len(terms) - len(surv_axis0(terms, N, N, i)) for i in range(N)})))
best = None
for i in range(N):
    T1 = surv_axis0(terms, N, N, i)
    for j in range(N):
        # after deleting row i, column indices of U are unchanged; V rows unchanged
        T2 = [t for t in T1 if not ((cols_of({k for k in t[0] if k // N != i}, N) == {j}) or rows_of(t[1], N) == {j}
                                     or not {k for k in t[0] if k // N != i})]
        cand = (len(T2), i, j)
        if best is None or cand < best:
            best = cand
print("[coordinate projection, 19^3 -> 18x18x19] best pair: delete row %d and column %d -> %d terms (%d vanish)"
      % (best[1], best[2], best[0], len(terms) - best[0]))

# ---------------- the actual slices
star = tuple(F(-(N - 5) // 2) if i == (N - 1) // 2 else F(1) for i in range(N))
unit = tuple(F(int(i == 0)) for i in range(N))
print("\nstar vector e*: entry %s at index %d, 1 elsewhere; e_0 = unit vector at index 0" % (star[(N - 1) // 2], (N - 1) // 2))

def is_outer_left(f, rows, cols, vec):
    """f == vec x^T for some x (each column of f is a multiple of vec)."""
    byc = {}
    for idx, c in f.items():
        r, cc = divmod(idx, cols)
        byc.setdefault(cc, {})[r] = c
    for cc, col in byc.items():
        r0 = next(iter(col)); lam = col[r0] / vec[r0] if vec[r0] else None
        if lam is None:
            return False
        for r in range(rows):
            if col.get(r, 0) != lam * vec[r]:
                return False
    return True

def is_outer_right(f, rows, cols, vec):
    """f == x vec^T (each row of f is a multiple of vec)."""
    byr = {}
    for idx, c in f.items():
        r, cc = divmod(idx, cols)
        byr.setdefault(r, {})[cc] = c
    for r, row in byr.items():
        c0 = next(iter(row)); lam = row[c0] / vec[c0] if vec[c0] else None
        if lam is None:
            return False
        for cc in range(cols):
            if row.get(cc, 0) != lam * vec[cc]:
                return False
    return True

def absorb_logged(S, seed=1, max_rounds=50):
    quiet = rounds = pi = 0
    log = []
    while quiet < 3 and rounds < max_rounds:
        pair = PAIRS[pi % 3]
        before = S
        S2, k = absorb_once(S, pair, seed=seed + rounds)
        if k:
            log.append((pair, k, len(before[3]), len(S2[3])))
            S = S2; quiet = 0
        else:
            quiet += 1
        pi += 1; rounds += 1
    return S, log

names = {0: "u (A side)", 1: "v (B side)", 2: "w (C side)"}
n1, n2, n3 = S[:3]
kU = {k for k, t in enumerate(terms) if is_outer_left(t[0], n1, n2, star)}
kW = {k for k, t in enumerate(terms) if is_outer_left(t[2], n1, n3, unit)}
print("\nstep 1, slice axis 0 (row index shared by A and C), e = e* on A, f = e_0 on C:")
print("  terms with U = e* x^T (killed on the A side): %d; with W = e_0 y^T (killed on the C side): %d; both: %d; total %d"
      % (len(kU), len(kW), len(kU & kW), len(kU | kW)))
S1 = restrict(S, 0, star, unit)
print("  after the slice: <%d,%d,%d> rank %d  (3633 - %d = %d)" % (S1[0], S1[1], S1[2], len(S1[3]), len(kU | kW), len(terms) - len(kU | kW)))
assert len(S1[3]) == len(terms) - len(kU | kW)
S1, log1 = absorb_logged(S1)
for pair, k, a, b in log1:
    print("  2-reduction: dependency among the %s and %s factors, removed %d term -> rank %d" % (names[pair[0]], names[pair[1]], k, b))
print("  step 1 result: <%d,%d,%d> rank %d" % (S1[0], S1[1], S1[2], len(S1[3])))
best1 = min((len(surv_axis1(S1[3], S1[1], S1[2], j)), j) for j in range(S1[1]))
print("\n[coordinate projection, 18x19x19:%d -> 18x18x19] best column: delete index %d -> %d terms (%d vanish); range of vanishing counts over all columns: %s"
      % (len(S1[3]), best1[1], best1[0], len(S1[3]) - best1[0],
         (min(len(S1[3]) - len(surv_axis1(S1[3], S1[1], S1[2], j)) for j in range(S1[1])),
          max(len(S1[3]) - len(surv_axis1(S1[3], S1[1], S1[2], j)) for j in range(S1[1])))))

m1, m2, m3 = S1[:3]
T1 = S1[3]
kU2 = {k for k, t in enumerate(T1) if is_outer_right(t[0], m1, m2, unit)}
kV2 = {k for k, t in enumerate(T1) if is_outer_left(t[1], m2, m3, star)}
print("\nstep 2, slice axis 1 (column index of A = row index of B), e = e_0 on A, f = e* on B:")
print("  terms with U = x e_0^T (killed on the A side): %d; with V = e* y^T (killed on the B side): %d; both: %d; total %d"
      % (len(kU2), len(kV2), len(kU2 & kV2), len(kU2 | kV2)))
S2 = restrict(S1, 1, unit, star)
print("  after the slice: <%d,%d,%d> rank %d  (%d - %d = %d)" % (S2[0], S2[1], S2[2], len(S2[3]), len(T1), len(kU2 | kV2), len(T1) - len(kU2 | kV2)))
assert len(S2[3]) == len(T1) - len(kU2 | kV2)
S2, log2 = absorb_logged(S2)
for pair, k, a, b in log2:
    print("  2-reduction: dependency among the %s and %s factors, removed %d term -> rank %d" % (names[pair[0]], names[pair[1]], k, b))
print("  step 2 result: <%d,%d,%d> rank %d" % (S2[0], S2[1], S2[2], len(S2[3])))

R = load_json(ref)
same = R[:3] == S2[:3] and R[3] == S2[3]
print("\nreplayed scheme identical (term by term, exact) to %s: %s" % (os.path.basename(ref), same))
print("\nsummary: 3633 -[slice 1 kills %d]-> %d -[2-reduction]-> %d -[slice 2 kills %d]-> %d -[2-reduction]-> %d"
      % (len(kU | kW), len(terms) - len(kU | kW), len(T1), len(kU2 | kV2), len(T1) - len(kU2 | kV2), len(S2[3])))
