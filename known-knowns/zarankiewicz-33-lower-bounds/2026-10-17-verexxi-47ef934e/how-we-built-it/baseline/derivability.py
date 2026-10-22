"""Is the claimed 16x19 matrix an exact extension of a public witness?  i.e. does it contain, as a sub-matrix on some
set of rows R and columns C, a matrix isomorphic (row and column permutations) to a public base matrix?

If yes for some base, the claim is "base + added lines" (a trivial append) and the repo policy says it is not a record.
Method: for every public base of size mb x nb (mb <= 16, nb <= 19) enumerate all row sets R (size mb) and column sets C
(size nb) of the claimed matrix, keep the sub-matrices with the same number of ones and the same sorted row and column
weights as the base, then decide isomorphism exactly (colour refinement + backtracking on rows).
Limit, stated plainly: this only detects an EXACT sub-matrix copy. A derivation that also adds ones inside the old
block (the greedy-saturation step of the surgery baseline) is not detected here; the surgery baseline covers that.
usage: python baseline/derivability.py matrix/z_16x19_142.txt baseline
       python baseline/derivability.py --selftest      (positive and negative control for the isomorphism test)
"""
import os, sys
from itertools import combinations

if len(sys.argv) == 2 and sys.argv[1] == "--selftest":
    claim_path, base_dir = None, os.path.dirname(os.path.abspath(__file__))
elif len(sys.argv) == 3:
    claim_path, base_dir = sys.argv[1], sys.argv[2]
else:
    sys.exit(__doc__)
sys.path.insert(0, base_dir)
import surgery_baseline as sb  # the claim's own loader for the public witness files

if claim_path:
    M = [[int(c) for c in l.strip()] for l in open(claim_path) if l.strip()]
    m, n = len(M), len(M[0])


def sub(R, C):
    return [[M[r][c] for c in C] for r in R]


def sig(A):
    return (sum(map(sum, A)), tuple(sorted(sum(r) for r in A)), tuple(sorted(sum(A[i][j] for i in range(len(A))) for j in range(len(A[0])))))


def isomorphic(A, B):
    """Exact isomorphism of 0/1 matrices under independent row and column permutations."""
    ma, na = len(A), len(A[0])
    if (ma, na) != (len(B), len(B[0])) or sig(A) != sig(B):
        return False
    # candidate rows of B for each row of A: same weight; order rows of A by fewest candidates
    wa = [sum(r) for r in A]; wb = [sum(r) for r in B]
    order = sorted(range(ma), key=lambda i: sum(1 for j in range(ma) if wb[j] == wa[i]))
    used = [False] * ma
    amap = []

    def colmulti(X, rows):
        return sorted(tuple(X[r][c] for r in rows) for c in range(na))

    def rec(k):
        if k == ma:
            return True
        i = order[k]
        for j in range(ma):
            if used[j] or wb[j] != wa[i]:
                continue
            ra = [x for x, _ in amap] + [i]
            rb = [y for _, y in amap] + [j]
            if colmulti(A, ra) != colmulti(B, rb):
                continue
            used[j] = True; amap.append((i, j))
            if rec(k + 1):
                return True
            amap.pop(); used[j] = False
        return False
    return rec(0)


if claim_path is None:
    import random
    B = sb.bases()["Sau 13x19 (118)"]
    rng = random.Random(5)
    r = list(range(13)); c = list(range(19)); rng.shuffle(r); rng.shuffle(c)
    P = [[B[i][j] for j in c] for i in r]
    print("permuted copy isomorphic (expect True):", isomorphic(P, B))
    Q = [row[:] for row in P]
    j1 = Q[0].index(1); j0 = Q[0].index(0); Q[0][j1] = 0; Q[0][j0] = 1
    print("perturbed copy isomorphic (expect False):", isomorphic(Q, B))
    sys.exit(0)


tot_checked = 0
hits = []
for name, B in sb.bases().items():
    mb, nb = len(B), len(B[0])
    if mb > m or nb > n:
        print("%-18s %2dx%-2d  skipped (larger than the claimed matrix in some dimension)" % (name, mb, nb))
        continue
    sB = sig(B)
    cand = 0; iso = 0
    for R in combinations(range(m), mb):
        for C in combinations(range(n), nb):
            S = sub(R, C)
            if sig(S) != sB:
                continue
            cand += 1
            if isomorphic(S, B):
                iso += 1
                hits.append((name, R, C))
    tot_checked += 1
    print("%-18s %2dx%-2d  sub-matrices with equal weight signature %5d, isomorphic to the base %d" % (name, mb, nb, cand, iso))
    sys.stdout.flush()
print("bases checked: %d" % tot_checked)
print("EXACT_SUBMATRIX_COPIES:", len(hits))
for h in hits[:10]:
    print("  ", h)
