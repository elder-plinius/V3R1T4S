"""Ceiling-saturation SAT model at 98.

Model: points of the 7-cube as 343 booleans.
- at-most-2 on EVERY grid line with >=3 points (4429 lines): clause (-p_i -p_j -p_k) for every triple.
- at-least-2 on each of the 147 axis-parallel lines: for each point p on the line,
  clause (all other points of the line).
Justification: a 98-point admissible set must have exactly 2 points on every axis-parallel
line (3*|S| = sum of axis-line counts <= 2*147 = 294, equality iff all axis lines full).
So SAT <=> a(7) = 98 exactly; UNSAT (with drat-trim-verified receipt) => a(7) <= 97 (p2 candidate).
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from n3l import enumerate_lines

N = 7
lines, point_lines = enumerate_lines(N)
axis = [l for l in lines
        if len({p % N for p in l}) == 1 and len({(p // N) % N for p in l}) == 1
        or len({p % N for p in l}) == 1 and len({p // (N * N) for p in l}) == 1
        or len({(p // N) % N for p in l}) == 1 and len({p // (N * N) for p in l}) == 1]
assert len(axis) == 3 * N * N, f"expected 147 axis lines, got {len(axis)}"

clauses = []
for l in lines:
    l = [p + 1 for p in l]  # DIMACS vars are 1-based; point ids are 0-based
    m = len(l)
    for i in range(m - 2):
        for j in range(i + 1, m - 1):
            for k in range(j + 1, m):
                clauses.append((-l[i], -l[j], -l[k]))
for l in axis:
    l = [p + 1 for p in l]  # DIMACS vars are 1-based
    for p in l:
        clauses.append(tuple(q for q in l if q != p))

out = __file__.rsplit('/', 1)[0] + '/ceiling98.cnf'
with open(out, 'w') as f:
    f.write(f"p cnf {N**3} {len(clauses)}\n")
    for c in clauses:
        f.write(' '.join(map(str, c)) + ' 0\n')
print(f"CNF written: {N**3} vars, {len(clauses)} clauses -> {out}")
