"""Check an S_k set of m tournaments straight from Jeffries' Definition 2.1 (standard library only).
Usage: python3 -I check_witness.py <witness.json> <k>
The JSON is a list of m adjacency matrices; A[v][u] = 1 means v -> u (v beats u)."""
import sys, json, itertools

Ts = json.load(open(sys.argv[1])); k = int(sys.argv[2]); n = len(Ts[0])
for A in Ts:  # each matrix is a tournament: zero diagonal, exactly one direction per pair
    assert len(A) == n and all(len(r) == n for r in A)
    assert all(A[i][i] == 0 for i in range(n))
    assert all(A[i][j] + A[j][i] == 1 for i in range(n) for j in range(n) if i != j)
bad = [U for U in itertools.combinations(range(n), k)
       if not any(all(A[v][u] for u in U) for A in Ts for v in range(n) if v not in U)]
print(f'm={len(Ts)} n={n} k={k} subsets={sum(1 for _ in itertools.combinations(range(n), k))} undominated={len(bad)}')
print('PASS' if not bad else 'FAIL')
