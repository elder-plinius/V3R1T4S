#!/usr/bin/env python3
"""Exact checker for a frozen Gram target (standard library only).

Usage: python3 check_gram.py OBJECT_JSON RECORD_NORM_DET RECORDS_JSON [--neg]
  OBJECT_JSON holds n, G (n x n integers), Q_num and Q_den (G = Q Q^T with Q = Q_num / Q_den),
  M0 (rows of a +-1 matrix) and norm_det_sqrt_G (the author's stated value).
Checks, all exact: G symmetric; diagonal n; every off-diagonal entry congruent to n mod 2;
all triple congruences G_ij + G_ik + G_jk + n = 0 mod 4; positive definite (exact rational
elimination, all pivots positive); det G by that elimination equals fraction-free Bareiss;
det G is a perfect square s*s and s is divisible by 2**(n-1); s / 2**(n-1) equals the stated
value and exceeds RECORD_NORM_DET (the live record, as an exact integer); det G does not
exceed the Barba bound squared; rational congruence to n*I: Q Q^T = G exactly, and n is a
perfect square, so P = Q / sqrt(n) satisfies P (n I) P^T = G with P rational; the rows M0 are
+-1, their number is at least n-2, and M0 M0^T equals the leading principal block of G.
--neg adds 4 to G[0][1] and G[1][0] (negative control: must fail).
The last output line is a JSON object.
"""
import sys, json, math, itertools, decimal
from fractions import Fraction


def bareiss(A):
    n = len(A); M = [r[:] for r in A]; sign = 1; prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            for i in range(k + 1, n):
                if M[i][k] != 0:
                    M[k], M[i] = M[i], M[k]; sign = -sign; break
            else:
                return 0
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                M[i][j] = (M[i][j] * M[k][k] - M[i][k] * M[k][j]) // prev
        prev = M[k][k]
    return sign * M[n - 1][n - 1]


def main():
    d = json.load(open(sys.argv[1])); rec = int(sys.argv[2]); recs = json.load(open(sys.argv[3]))
    n = d["n"]; G = [r[:] for r in d["G"]]; M0 = d["M0"]; Qn = d["Q_num"]; qd = d["Q_den"]
    res = {"file": sys.argv[1].split("/")[-1], "n": n}
    if "--neg" in sys.argv:
        G[0][1] += 4; G[1][0] += 4; res["negative_control"] = "G[0][1] and G[1][0] increased by 4"
    res["symmetric"] = all(G[i][j] == G[j][i] for i in range(n) for j in range(n))
    res["diagonal_is_n"] = all(G[i][i] == n for i in range(n))
    res["offdiag_congruent_to_n_mod_2"] = all((G[i][j] - n) % 2 == 0 for i in range(n) for j in range(n) if i != j)
    res["triple_congruences_mod_4"] = all((G[i][j] + G[i][k] + G[j][k] + n) % 4 == 0
                                          for i, j, k in itertools.combinations(range(n), 3))
    M = [[Fraction(x) for x in r] for r in G]; piv = []; pd = True
    for k in range(n):
        p = M[k][k]
        if p <= 0: pd = False; break
        piv.append(p)
        for i in range(k + 1, n):
            f = M[i][k] / p
            if f:
                for j in range(k, n): M[i][j] -= f * M[k][j]
    res["positive_definite"] = pd
    if not pd:
        print(json.dumps(res)); return 0
    detG = 1
    for p in piv: detG *= p
    assert detG.denominator == 1
    detG = int(detG)
    res["det_by_elimination_equals_bareiss"] = (bareiss(G) == detG)
    s = math.isqrt(detG)
    res["det_is_perfect_square"] = (s * s == detG)
    den = 1 << (n - 1)
    ok = res["det_is_perfect_square"] and s % den == 0
    nd = s // den if ok else None
    res["sqrt_det_over_2^(n-1)"] = str(nd)
    res["equals_stated_value"] = (str(nd) == d["norm_det_sqrt_G"])
    res["record_norm_det"] = str(rec)
    res["greater_than_record"] = bool(ok and nd > rec)
    cmp = []
    for r in recs["records"]:
        cmp.append({"source": r["source"], "value": r["value"], "greater": bool(ok and decimal.Decimal(nd) > decimal.Decimal(r["value"]))})
    res["comparison_with_records"] = cmp
    bar2 = (2 * n - 1) * (n - 1) ** (n - 1)
    res["det_le_Barba_bound_squared"] = (detG <= bar2)
    decimal.getcontext().prec = 40
    res["sqrt_det_over_Barba_bound"] = str((decimal.Decimal(detG) / decimal.Decimal(bar2)).sqrt())[:8]
    sq = math.isqrt(n)
    res["n_is_perfect_square"] = (sq * sq == n)
    qq = True
    for i in range(n):
        for j in range(i, n):
            if sum(Qn[i][k] * Qn[j][k] for k in range(n)) != G[i][j] * qd * qd:
                qq = False; break
        if not qq: break
    res["Q_Qt_equals_G_exactly"] = qq
    k = len(M0)
    res["M0_rows"] = k
    res["M0_entries_plus_minus_one"] = all(len(r) == n and all(x in (1, -1) for x in r) for r in M0)
    blk = True
    for i in range(k):
        for j in range(i, k):
            if sum(a * b for a, b in zip(M0[i], M0[j])) != G[i][j]:
                blk = False; break
        if not blk: break
    res["M0_Mt0_equals_leading_block_of_G"] = blk
    res["M0_rows_at_least_n_minus_2"] = (k >= n - 2)
    print(json.dumps(res))
    return 0


sys.exit(main())
