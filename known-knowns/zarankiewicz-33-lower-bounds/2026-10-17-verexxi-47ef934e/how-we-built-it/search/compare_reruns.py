"""Compare each 142-one matrix found by the reruns with the claimed matrix: weight signature and exact isomorphism
(row and column permutations). Run from the attempt folder: python code/compare_reruns.py CLAIM_MATRIX RERUN_DIR"""
import glob, os, sys
claim, rerun = sys.argv[1], sys.argv[2]


def ld(p):
    return [[int(c) for c in l.strip()] for l in open(p) if l.strip()]


def sig(A):
    return (sum(map(sum, A)), tuple(sorted(sum(r) for r in A)), tuple(sorted(sum(A[i][j] for i in range(len(A))) for j in range(len(A[0])))))


def isomorphic(A, B):
    ma, na = len(A), len(A[0])
    if (ma, na) != (len(B), len(B[0])) or sig(A) != sig(B):
        return False
    wa = [sum(r) for r in A]; wb = [sum(r) for r in B]
    order = sorted(range(ma), key=lambda i: sum(1 for j in range(ma) if wb[j] == wa[i]))
    used = [False] * ma; amap = []

    def colmulti(X, rows):
        return sorted(tuple(X[r][c] for r in rows) for c in range(na))

    def rec(k):
        if k == ma:
            return True
        i = order[k]
        for j in range(ma):
            if used[j] or wb[j] != wa[i]:
                continue
            ra = [x for x, _ in amap] + [i]; rb = [y for _, y in amap] + [j]
            if colmulti(A, ra) != colmulti(B, rb):
                continue
            used[j] = True; amap.append((i, j))
            if rec(k + 1):
                return True
            amap.pop(); used[j] = False
        return False
    return rec(0)


ref = ld(claim)
print("claimed matrix: ones %d, row weights %s" % (sig(ref)[0], sorted(sum(r) for r in ref)))
for f in sorted(glob.glob(os.path.join(rerun, "z_16x19_*.txt"))):
    A = ld(f)
    same_sig = sig(A) == sig(ref)
    print("%-26s ones %d  same weight signature as claim: %-5s  isomorphic to claim: %s" % (
        os.path.basename(f), sig(A)[0], same_sig, isomorphic(A, ref) if same_sig else False))
