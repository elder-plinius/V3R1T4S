"""Independent checker written from Definition 2.2 (Jeffries arXiv:2604.08790).
A tuple of m tournaments (adjacency matrices A[t][i][j]) on n vertices is S_k if every k-subset U of vertices
has a single tournament t and a vertex v not in U with A[t][v][u]=1 for all u in U."""
from itertools import combinations
import json, sys

def is_tournament(A):
    n = len(A)
    return all(A[i][i] == 0 for i in range(n)) and all(A[i][j] in (0, 1) for i in range(n) for j in range(n)) \
        and all(A[i][j] + A[j][i] == 1 for i in range(n) for j in range(n) if i != j)

def undominated(mats, k):
    """Number of k-subsets not dominated (0 means S_k). Also validates tournaments."""
    n = len(mats[0])
    assert all(len(A) == n and is_tournament(A) for A in mats), "not tournaments on one vertex set"
    out = [[sum(1 << u for u in range(n) if A[v][u]) for v in range(n)] for A in mats]
    bad = 0
    for U in combinations(range(n), k):
        mask = sum(1 << u for u in U)
        if not any((o & mask) == mask for outs in out for o in outs):
            bad += 1
    return bad

if __name__ == "__main__":
    mats = json.load(open(sys.argv[1])); k = int(sys.argv[2])
    b = undominated(mats, k)
    print(f"n={len(mats[0])} m={len(mats)} k={k} undominated={b} {'PASS' if b == 0 else 'FAIL'}")
