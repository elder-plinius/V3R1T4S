#!/usr/bin/env python3
"""Standalone exact Fraction + Branch-and-Bound AND independent exhaustive Gray-code checker for Komlos C_24 p2."""
from fractions import Fraction
import sys

EXPECTED_DISC = Fraction(205956508661, 100000000000)

def check_file(path):
    with open(path, "r", encoding="utf-8") as f:
        toks = f.read().split()
    if len(toks) < 3:
        raise ValueError("Malformed header")
    m, n, D = int(toks[0]), int(toks[1]), int(toks[2])
    if m <= 0 or n <= 0 or n > 15 or D <= 0 or len(toks) != 3 + m * n:
        raise ValueError("Invalid dimensions or token count")

    P = []
    A = []
    idx = 3
    for i in range(m):
        prow = []
        arow = []
        for j in range(n):
            v = int(toks[idx])
            idx += 1
            prow.append(v)
            arow.append(Fraction(v, D))
        P.append(prow)
        A.append(arow)

    # 1. Exact Fraction column Euclidean norm <= 1 and > 0 check
    for j in range(n):
        col_sq = sum(A[i][j] * A[i][j] for i in range(m))
        if col_sq <= 0 or col_sq > 1:
            raise ValueError(f"Column {j} failed norm^2 <= 1 check: {col_sq}")

    # 2. Method A: Exact recursive Branch-and-Bound
    order = [0] + sorted(range(1, n), key=lambda j: -sum(P[i][j] * P[i][j] for i in range(m)))
    Q = [[P[i][order[k]] for k in range(n)] for i in range(m)]
    rem = [[0] * m for _ in range(n + 1)]
    for k in range(n - 1, -1, -1):
        for i in range(m):
            rem[k][i] = rem[k + 1][i] + abs(Q[i][k])

    cur = [Q[i][0] for i in range(m)]
    best_x = [1] * n
    init_cur = cur[:]
    for k in range(1, n):
        mp = max(abs(init_cur[i] + Q[i][k]) for i in range(m))
        mn = max(abs(init_cur[i] - Q[i][k]) for i in range(m))
        if mp <= mn:
            best_x[k] = 1
            for i in range(m): init_cur[i] += Q[i][k]
        else:
            best_x[k] = -1
            for i in range(m): init_cur[i] -= Q[i][k]
    best_min = max(abs(v) for v in init_cur)
    x_work = [1] * n

    def dfs(k):
        nonlocal best_min, best_x
        if k == n:
            mx = max(abs(v) for v in cur)
            if mx < best_min:
                best_min = mx
                best_x = x_work[:]
            return
        rk = rem[k]
        for i in range(m):
            if abs(cur[i]) - rk[i] >= best_min:
                return
        col = [Q[i][k] for i in range(m)]
        mp = max(abs(cur[i] + col[i]) for i in range(m))
        mn = max(abs(cur[i] - col[i]) for i in range(m))
        branches = (1, -1) if mp <= mn else (-1, 1)
        for s in branches:
            x_work[k] = s
            if s == 1:
                for i in range(m): cur[i] += col[i]
                dfs(k + 1)
                for i in range(m): cur[i] -= col[i]
            else:
                for i in range(m): cur[i] -= col[i]
                dfs(k + 1)
                for i in range(m): cur[i] += col[i]

    dfs(1)
    orig_x = [0] * n
    for k in range(n):
        orig_x[order[k]] = best_x[k]
    disc_bnb = max(abs(sum(A[i][j] * orig_x[j] for j in range(n))) for i in range(m))
    if disc_bnb != Fraction(best_min, D):
        raise ValueError("Internal B&B witness mismatch")

    # 3. Method B: Independent exhaustive Gray-code scan over all 2^(n-1) sign vectors
    S = [sum(P[i][j] for j in range(n)) for i in range(m)]
    sgn = [1] * n
    gray_min = max(abs(v) for v in S)
    gprev = 0
    for k in range(1, 1 << (n - 1)):
        g = k ^ (k >> 1)
        diff = g ^ gprev
        col_idx = (diff & -diff).bit_length()  # 1..n-1
        gprev = g
        delta = -2 if sgn[col_idx] == 1 else 2
        sgn[col_idx] = -sgn[col_idx]
        for i in range(m):
            S[i] += delta * P[i][col_idx]
        mx = max(abs(v) for v in S)
        if mx < gray_min:
            gray_min = mx

    disc_gray = Fraction(gray_min, D)
    if disc_bnb != disc_gray:
        raise ValueError(f"Disagreement between B&B ({disc_bnb}) and Gray-code ({disc_gray})")

    if not (n <= 15 and disc_bnb >= 2 and disc_bnb > Fraction(2006, 1000)):
        raise ValueError(f"Does not meet p2 threshold > 2.006: {disc_bnb}")
    if disc_bnb != EXPECTED_DISC:
        raise ValueError(f"Object discrepancy {disc_bnb} differs from certified {EXPECTED_DISC}")

    print(f"PY_EXACT_BNB_AND_GRAY: m={m} n={n} disc={disc_bnb.numerator}/{disc_bnb.denominator} ({float(disc_bnb):.12f}) > 2.006")

if __name__ == "__main__":
    try:
        check_file(sys.argv[1])
    except Exception as exc:
        print(f"CHECK_ERROR: {exc}")
        print("FAIL")
        sys.exit(1)
