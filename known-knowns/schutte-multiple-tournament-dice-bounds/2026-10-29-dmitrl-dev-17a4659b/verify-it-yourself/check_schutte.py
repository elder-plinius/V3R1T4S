#!/usr/bin/env python3
"""Direct checker for Definition 2.2 of arXiv:2604.08790 (Jeffries 2026).

Input: JSON {"m": int, "k": int, "n": int, "tournaments": [[row strings or 0/1 lists], ...]}
A[t][i][j] = 1 means i -> j (i beats j) in tournament t.
The tuple is S_k when every k-subset U of V = {0..n-1} has one tournament t and one vertex v outside U
with A[t][v][u] = 1 for every u in U (the same v and the same t for all of U).
Stdlib only; independent of any SAT encoding.
"""
import json, sys
from itertools import combinations

def load(path):
    d = json.load(open(path))
    T = [[[int(c) for c in row] for row in A] for A in d["tournaments"]]
    return d["m"], d["k"], d["n"], T

def check(m, k, n, T):
    errs = []
    if len(T) != m: errs.append(f"expected {m} tournaments, got {len(T)}")
    if not (n >= k + 1): errs.append(f"n={n} < k+1={k+1}")
    for t, A in enumerate(T):
        if len(A) != n or any(len(r) != n for r in A):
            errs.append(f"tournament {t}: not {n}x{n}"); continue
        for i in range(n):
            if A[i][i] != 0: errs.append(f"tournament {t}: A[{i}][{i}] != 0")
            for j in range(n):
                if A[i][j] not in (0, 1): errs.append(f"tournament {t}: entry ({i},{j}) not 0/1")
                if i != j and A[i][j] + A[j][i] != 1: errs.append(f"tournament {t}: A[{i}][{j}]+A[{j}][{i}] != 1")
    if errs: return False, errs, None
    bad = []
    count = 0
    for U in combinations(range(n), k):
        count += 1
        Us = set(U)
        ok = any(all(A[v][u] == 1 for u in U) for A in T for v in range(n) if v not in Us)
        if not ok: bad.append(U)
    return not bad, bad, count

if __name__ == "__main__":
    m, k, n, T = load(sys.argv[1])
    ok, info, count = check(m, k, n, T)
    if count is None:
        print("INVALID:", "; ".join(info[:10])); sys.exit(2)
    print(f"m={m} k={k} n={n}: {count} k-subsets checked, {len(info)} undominated -> {'PASS' if ok else 'FAIL'}")
    if not ok: print("first undominated:", info[:5])
    sys.exit(0 if ok else 1)
