"""Exact maximum Sidon subset by integer linear programming (pulp with the CBC solver).

Usage: python3 ilp_sidon.py A.json --expect-s S

Variables x_a in {0,1} for each element a of A. For every relation a + b = c + d among elements of A with
{a, b} != {c, d} (a = b allowed, so 3-term arithmetic progressions a + a = c + d are included), the constraint
x_a + x_b + x_c + x_d <= |{a, b, c, d}| - 1 forbids taking all distinct elements of that relation together.
Maximise sum x_a. A subset is Sidon exactly when it contains no such relation, so the optimum is s(A).
CBC proves optimality; the script also re-checks the returned subset directly.
"""
import json, sys
from itertools import combinations
import pulp

A = sorted(json.load(open(sys.argv[1]))['A'])
expect = int(sys.argv[sys.argv.index('--expect-s') + 1]) if '--expect-s' in sys.argv else None
n = len(A)
pairs = {}
for i in range(n):
    for j in range(i, n):
        pairs.setdefault(A[i] + A[j], []).append((i, j))
rels = []
for prs in pairs.values():
    for p, q in combinations(prs, 2):
        rels.append(sorted(set(p) | set(q)))
prob = pulp.LpProblem('max_sidon', pulp.LpMaximize)
x = [pulp.LpVariable(f'x{i}', cat='Binary') for i in range(n)]
prob += pulp.lpSum(x)
for r in rels:
    prob += pulp.lpSum(x[i] for i in r) <= len(r) - 1
status = prob.solve(pulp.PULP_CBC_CMD(msg=0))
chosen = [A[i] for i in range(n) if x[i].value() > 0.5]
s = len(chosen)
sums = [a + b for a, b in combinations(chosen, 2)] + [2 * a for a in chosen]
sidon = len(sums) == len(set(sums))
ok = pulp.LpStatus[status] == 'Optimal' and sidon and (expect is None or s == expect)
print(f"ILP: n={n} relations={len(rels)} status={pulp.LpStatus[status]} s(A)={s} returned_subset_is_sidon={sidon} {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)
