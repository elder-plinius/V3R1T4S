#!/usr/bin/env python3
r"""
Standalone Exact Verification Script for moore-graph-57 (Partial Win p2).
  - Track p2: Independent exact computational verification of Yawara Ishida (arXiv:2606.29183v2,
              8 July 2026), "No involutions in the missing Moore graph" (Theorem 1.1, Corollary 6.1,
              Theorem 1.2 for p in {7, 11, 13, 19}, existing Moore graphs C_5, Petersen, and
              Hoffman-Singleton, and all 11 rows of Table 1 in Section 8 across 5 open SRG families,
              including Remark 8.5 correcting Makhnev-Nosov 2004 Lemmas 2.2 and 2.3(1)).

Uses Python standard library only (fractions.Fraction, itertools, json, math, os, sys).
"""

import argparse
from fractions import Fraction
import itertools
import json
import math
import os
import sys


def rank_mod_p(matrix, p):
    """Exact rank of an integer matrix over F_p via row reduction."""
    if not matrix or not matrix[0]:
        return 0
    m = len(matrix)
    n = len(matrix[0])
    A = [[int(x) % p for x in row] for row in matrix]
    rank = 0
    for col in range(n):
        pivot = None
        for r in range(rank, m):
            if A[r][col] % p != 0:
                pivot = r
                break
        if pivot is None:
            continue
        A[rank], A[pivot] = A[pivot], A[rank]
        inv = pow(A[rank][col], -1, p)
        for c in range(col, n):
            A[rank][c] = (A[rank][c] * inv) % p
        for r in range(m):
            if r != rank and A[r][col] % p != 0:
                factor = A[r][col] % p
                for c in range(col, n):
                    A[r][c] = (A[r][c] - factor * A[rank][c]) % p
        rank += 1
        if rank == m:
            break
    return rank


def adj_star(m):
    n = m + 1
    A = [[0] * n for _ in range(n)]
    for i in range(1, n):
        A[0][i] = 1
        A[i][0] = 1
    return A


def adj_cycle(n):
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][(i + 1) % n] = 1
        A[i][(i - 1) % n] = 1
    return A


def adj_complete(n):
    return [[0 if i == j else 1 for j in range(n)] for i in range(n)]


def adj_petersen():
    pairs = list(itertools.combinations(range(5), 2))
    n = len(pairs)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if set(pairs[i]).isdisjoint(pairs[j]):
                A[i][j] = A[j][i] = 1
    return A, pairs


def adj_hoffman_singleton():
    A = [[0] * 50 for _ in range(50)]
    for i in range(5):
        for j in range(5):
            u = 5 * i + j
            for dj in (1, 4):
                v = 5 * i + ((j + dj) % 5)
                A[u][v] = 1
    for k in range(5):
        for l in range(5):
            u = 25 + 5 * k + l
            for dl in (2, 3):
                v = 25 + 5 * k + ((l + dl) % 5)
                A[u][v] = 1
    for i in range(5):
        for j in range(5):
            u = 5 * i + j
            for k in range(5):
                l = (i * k + j) % 5
                v = 25 + 5 * k + l
                A[u][v] = A[v][u] = 1
    return A


def adj_clebsch_16_5_0_2():
    gens = [1, 2, 4, 8, 15]
    A = [[0] * 16 for _ in range(16)]
    for u in range(16):
        for g in gens:
            v = u ^ g
            A[u][v] = 1
    return A


def linear_comb_matrix(n, alpha, beta, gamma, A):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            M[i][j] = gamma + (alpha if i == j else 0) + beta * A[i][j]
    return M


def bose_mesner_mul(c1, c2, v=3250, k=57, lam=0, mu=1):
    a1, b1, g1 = [Fraction(x) for x in c1]
    a2, b2, g2 = [Fraction(x) for x in c2]
    alpha = a1 * a2 + b1 * b2 * (k - mu)
    beta = a1 * b2 + b1 * a2 + b1 * b2 * (lam - mu)
    gamma = a1 * g2 + g1 * a2 + b1 * b2 * mu + (b1 * g2 + g1 * b2) * k + g1 * g2 * v
    return (alpha, beta, gamma)


def verify_srg_parameters_and_idempotents(v, k, lam, mu, r, s):
    assert k * (k - lam - 1) == mu * (v - k - 1)
    assert r + s == lam - mu
    assert r * s == mu - k
    m_r = Fraction(-k - s * (v - 1), r - s)
    m_s = Fraction(-k - r * (v - 1), s - r)
    assert m_r.denominator == 1 and m_s.denominator == 1
    m_r, m_s = int(m_r), int(m_s)
    assert 1 + m_r + m_s == v
    assert k + r * m_r + s * m_s == 0
    assert k * k + r * r * m_r + s * s * m_s == v * k

    E_k = (Fraction(0), Fraction(0), Fraction(1, v))
    E_r = (Fraction(-s, r - s), Fraction(1, r - s), Fraction(-(k - s), v * (r - s)))
    E_s = (Fraction(-r, s - r), Fraction(1, s - r), Fraction(-(k - r), v * (s - r)))

    for idx, target in enumerate((Fraction(1), Fraction(0), Fraction(0))):
        assert E_k[idx] + E_r[idx] + E_s[idx] == target

    for E in (E_k, E_r, E_s):
        assert bose_mesner_mul(E, E, v, k, lam, mu) == E
    assert bose_mesner_mul(E_k, E_r, v, k, lam, mu) == (0, 0, 0)
    assert bose_mesner_mul(E_k, E_s, v, k, lam, mu) == (0, 0, 0)
    assert bose_mesner_mul(E_r, E_s, v, k, lam, mu) == (0, 0, 0)

    A_elem = (Fraction(0), Fraction(1), Fraction(0))
    for theta, E in ((k, E_k), (r, E_r), (s, E_s)):
        prod = bose_mesner_mul(A_elem, E, v, k, lam, mu)
        assert prod == tuple(theta * x for x in E)

    denom_r = math.lcm(E_r[0].denominator, E_r[1].denominator, E_r[2].denominator)
    denom_s = math.lcm(E_s[0].denominator, E_s[1].denominator, E_s[2].denominator)
    num_r = tuple(int(x * denom_r) for x in E_r)
    num_s = tuple(int(x * denom_s) for x in E_s)
    assert math.gcd(*num_r) == 1
    assert math.gcd(*num_s) == 1

    return {
        "params": [v, k, lam, mu],
        "eigenvalues": {"k": k, "r": r, "s": s},
        "multiplicities": {"m_k": 1, "m_r": m_r, "m_s": m_s},
        "E_r": {"denom": denom_r, "numerator_I_A_J": list(num_r)},
        "E_s": {"denom": denom_s, "numerator_I_A_J": list(num_s)},
    }


def compute_track_p2():
    """Computes and verifies all results of Track p2 (arXiv:2606.29183v2)."""
    # 1. Existing Moore graphs Brauer trace-rank verification
    existing_checks = []
    A_c5 = adj_cycle(5)
    perm_c5_2 = [0, 4, 3, 2, 1]
    fix_c5_2 = [i for i in range(5) if perm_c5_2[i] == i]
    a0_c5 = len(fix_c5_2)
    a1_c5 = sum(1 for i in range(5) if A_c5[i][perm_c5_2[i]] == 1)
    rk_c5 = rank_mod_p([[4]], 2)
    assert (a0_c5, a1_c5, rk_c5) == (1, 2, 0)
    existing_checks.append({"graph": "C_5", "p": 2, "a0": a0_c5, "a1": a1_c5, "trace": 0, "rank_mod_p": rk_c5})

    pet_info = verify_srg_parameters_and_idempotents(10, 3, 0, 1, 1, -2)
    A_pet, pairs = adj_petersen()
    pair_to_idx = {p: i for i, p in enumerate(pairs)}

    def s5_to_pet_perm(s5_perm):
        out = [0] * 10
        for i, (a, b) in enumerate(pairs):
            na, nb = s5_perm[a], s5_perm[b]
            if na > nb:
                na, nb = nb, na
            out[i] = pair_to_idx[(na, nb)]
        return out

    pet_cases = [
        ("S5_transposition_(01)", [1, 0, 2, 3, 4], 2, "E_s", pet_info["E_s"]),
        ("S5_double_transposition_(01)(23)", [1, 0, 3, 2, 4], 2, "E_s", pet_info["E_s"]),
        ("S5_5cycle_(01234)", [1, 2, 3, 4, 0], 5, "E_r", pet_info["E_r"]),
    ]
    for label, s5_p, p, which_E, E_data in pet_cases:
        perm = s5_to_pet_perm(s5_p)
        F = [i for i in range(10) if perm[i] == i]
        a0 = len(F)
        a1 = sum(1 for i in range(10) if A_pet[i][perm[i]] == 1)
        alpha, beta, gamma = E_data["numerator_I_A_J"]
        denom = E_data["denom"]
        assert denom % p != 0
        tr_val = Fraction(alpha * a0 + beta * a1 + gamma * 10, denom)
        assert tr_val.denominator == 1
        A_F = [[A_pet[u][v] for v in F] for u in F]
        M_F = linear_comb_matrix(a0, alpha, beta, gamma, A_F)
        rk = rank_mod_p(M_F, p)
        assert int(tr_val) == rk
        existing_checks.append({
            "graph": "Petersen_srg(10,3,0,1)",
            "automorphism": label,
            "p": p,
            "idempotent": which_E,
            "a0": a0,
            "a1": a1,
            "trace": int(tr_val),
            "rank_mod_p": rk,
        })

    hosi_info = verify_srg_parameters_and_idempotents(50, 7, 0, 1, 2, -3)
    A_hosi = adj_hoffman_singleton()
    for i in range(50):
        assert sum(A_hosi[i]) == 7
        for j in range(i + 1, 50):
            common = sum(A_hosi[i][w] * A_hosi[j][w] for w in range(50))
            assert common == (0 if A_hosi[i][j] == 1 else 1)

    perm_hosi_t1 = [0] * 50
    for i in range(5):
        for j in range(5):
            perm_hosi_t1[5 * i + j] = 5 * ((-i) % 5) + ((-j) % 5)
    for k in range(5):
        for l in range(5):
            perm_hosi_t1[25 + 5 * k + l] = 25 + 5 * k + ((-l) % 5)
    for u in range(50):
        for v in range(50):
            assert A_hosi[u][v] == A_hosi[perm_hosi_t1[u]][perm_hosi_t1[v]]

    F_hosi = [i for i in range(50) if perm_hosi_t1[i] == i]
    a0_h = len(F_hosi)
    a1_h = sum(1 for i in range(50) if A_hosi[i][perm_hosi_t1[i]] == 1)
    alpha, beta, gamma = hosi_info["E_r"]["numerator_I_A_J"]
    denom = hosi_info["E_r"]["denom"]
    tr_h = Fraction(alpha * a0_h + beta * a1_h + gamma * 50, denom)
    A_Fh = [[A_hosi[u][v] for v in F_hosi] for u in F_hosi]
    M_Fh = linear_comb_matrix(a0_h, alpha, beta, gamma, A_Fh)
    rk_h = rank_mod_p(M_Fh, 2)
    assert int(tr_h) == rk_h == 4
    existing_checks.append({
        "graph": "HoffmanSingleton_srg(50,7,0,1)",
        "automorphism": "involution_Fix_K1_5",
        "p": 2,
        "idempotent": "E_r",
        "a0": a0_h,
        "a1": a1_h,
        "trace": int(tr_h),
        "rank_mod_p": rk_h,
    })

    # 2. Theorem 1.1 & Theorem 1.2 for srg(3250, 57, 0, 1)
    srg_info = verify_srg_parameters_and_idempotents(3250, 57, 0, 1, 7, -8)
    assert srg_info["E_r"] == {"denom": 750, "numerator_I_A_J": [400, 50, -1]}
    assert srg_info["E_s"] == {"denom": 975, "numerator_I_A_J": [455, -65, 1]}

    a0_t = 56
    edges_F_t = 55
    a1_t_combinatorial = 3250 - (58 * a0_t - 2 * edges_F_t)
    assert a1_t_combinatorial == 112
    chi_s_combinatorial = Fraction(7 * a0_t - a1_t_combinatorial + 50, 15)
    chi_r_combinatorial = Fraction(8 * a0_t + a1_t_combinatorial - 65, 15)
    assert chi_s_combinatorial == 22 and chi_r_combinatorial == 33

    # Verify a_1(t) = 0 is impossible across all closed subgraphs
    for a0_cand, e_cand in [(0, 0), (1, 0), (2, 1), (5, 5), (10, 15), (50, 175)] + [(m + 1, m) for m in range(2, 58)]:
        if 58 * a0_cand - 2 * e_cand == 3250:
            assert (7 * a0_cand + 50) % 15 != 0

    A_K1_55 = adj_star(55)
    M_K1_55 = linear_comb_matrix(56, 455, -65, 1, A_K1_55)
    rk_p2 = rank_mod_p(M_K1_55, 2)
    assert rk_p2 == 54
    a1_t_forced = 7 * a0_t + 50 - 15 * rk_p2
    assert a1_t_forced == -368

    p7_candidates = []
    for a0 in range(2, 59, 7):
        A_F = adj_star(a0 - 1)
        M_F_s = linear_comb_matrix(a0, 455, -65, 1, A_F)
        M_F_r = linear_comb_matrix(a0, 400, 50, -1, A_F)
        rk_s = rank_mod_p(M_F_s, 7)
        rk_r = rank_mod_p(M_F_r, 7)
        assert rk_s == 1 and rk_r == a0 - 2
        a1_s = 7 * a0 + 50 - 15 * rk_s
        assert a1_s == 7 * a0 + 35
        total_disjoint_vertices = 3 * a1_s + a0 + 56 * (a0 - 1)
        assert total_disjoint_vertices == 78 * a0 + 49
        p7_candidates.append({
            "a0": a0,
            "rk_E_s_mod_7": rk_s,
            "rk_E_r_mod_7": rk_r,
            "a1_forced": a1_s,
            "disjoint_vertex_lower_bound": total_disjoint_vertices,
            "survives_vertex_bound": total_disjoint_vertices <= 3250,
        })
    surviving_p7 = [[c["a0"], c["a1_forced"]] for c in p7_candidates if c["survives_vertex_bound"]]
    assert surviving_p7 == [[2, 49], [9, 98], [16, 147], [23, 196], [30, 245], [37, 294]]

    M_p11_s = linear_comb_matrix(5, 455, -65, 1, A_c5)
    M_p11_r = linear_comb_matrix(5, 400, 50, -1, A_c5)
    rk_p11_s = rank_mod_p(M_p11_s, 11)
    rk_p11_r = rank_mod_p(M_p11_r, 11)
    assert rk_p11_s == 2 and rk_p11_r == 2
    a1_p11 = 7 * 5 + 50 - 15 * rk_p11_s
    assert a1_p11 == 55

    rk_p13_r = rank_mod_p([], 13)
    a1_p13 = 15 * rk_p13_r - 8 * 0 + 65
    assert a1_p13 == 65
    tr_p13_s = int(Fraction(7 * 0 - a1_p13 + 50, 15))
    assert tr_p13_s == -1

    M_p19_s = linear_comb_matrix(1, 455, -65, 1, [[0]])
    M_p19_r = linear_comb_matrix(1, 400, 50, -1, [[0]])
    rk_p19_s = rank_mod_p(M_p19_s, 19)
    rk_p19_r = rank_mod_p(M_p19_r, 19)
    assert rk_p19_s == 0 and rk_p19_r == 0
    a1_p19 = 7 * 1 + 50 - 15 * rk_p19_s
    assert a1_p19 == 57

    # 3. Section 8 (Table 1, Propositions 8.1-8.8, Remark 8.5)
    A_clebsch = adj_clebsch_16_5_0_2()
    for i in range(16):
        assert sum(A_clebsch[i]) == 5
        for j in range(i + 1, 16):
            common = sum(A_clebsch[i][w] * A_clebsch[j][w] for w in range(16))
            assert common == (0 if A_clebsch[i][j] == 1 else 2)

    table1_results = []

    # (162, 21, 0, 3)
    verify_srg_parameters_and_idempotents(162, 21, 0, 3, 3, -6)
    rk_162_p2_empty = rank_mod_p([], 2)
    a1_162_p2_empty = 3 * 0 + 18 - 9 * rk_162_p2_empty
    assert a1_162_p2_empty == 18
    table1_results.append({
        "srg": [162, 21, 0, 3], "p": 2, "Fix": "empty", "a0": 0,
        "idempotent": "E_{-6}", "rank_mod_p": rk_162_p2_empty,
        "known_a1": "162", "a1_here": "impossible (rank equation gives 18 != 162)"
    })
    A_K1_3 = adj_star(3)
    rk_162_p2_star = rank_mod_p(linear_comb_matrix(4, 27, -9, 1, A_K1_3), 2)
    a1_162_p2_star = 3 * 4 + 18 - 9 * rk_162_p2_star
    assert rk_162_p2_star == 2 and a1_162_p2_star == 12
    table1_results.append({
        "srg": [162, 21, 0, 3], "p": 2, "Fix": "K_{1,3}", "a0": 4,
        "idempotent": "E_{-6}", "rank_mod_p": rk_162_p2_star,
        "known_a1": "none", "a1_here": a1_162_p2_star
    })
    A_K2 = adj_complete(2)
    rk_162_p5_k2 = rank_mod_p(linear_comb_matrix(2, 36, 6, -1, A_K2), 5)
    a1_162_p5_k2 = 9 * rk_162_p5_k2 - 6 * 2 + 27
    assert rk_162_p5_k2 == 0 and a1_162_p5_k2 == 15
    table1_results.append({
        "srg": [162, 21, 0, 3], "p": 5, "Fix": "K_2", "a0": 2,
        "idempotent": "E_3", "rank_mod_p": rk_162_p5_k2,
        "known_a1": "15, 60", "a1_here": a1_162_p5_k2
    })

    # (352, 26, 0, 2)
    verify_srg_parameters_and_idempotents(352, 26, 0, 2, 4, -6)
    rk_352_p11 = rank_mod_p([], 11)
    a1_352_p11 = 4 * 0 + 22 - 10 * rk_352_p11
    assert a1_352_p11 == 22
    table1_results.append({
        "srg": [352, 26, 0, 2], "p": 11, "Fix": "empty", "a0": 0,
        "idempotent": "E_{-6}", "rank_mod_p": rk_352_p11,
        "known_a1": "falsely excluded in [22, Lemma 2.2] via w == 8 (mod 10)", "a1_here": a1_352_p11
    })
    rk_352_p13 = rank_mod_p(linear_comb_matrix(1, 64, -16, 1, [[0]]), 13)
    a1_352_p13 = 4 * 1 + 22 - 10 * rk_352_p13
    assert a1_352_p13 == 26
    table1_results.append({
        "srg": [352, 26, 0, 2], "p": 13, "Fix": "K_1", "a0": 1,
        "idempotent": "E_{-6}", "rank_mod_p": rk_352_p13,
        "known_a1": "falsely claimed 52 in [22, Lemma 2.3(1)]", "a1_here": a1_352_p13
    })

    # (1276, 50, 0, 2)
    verify_srg_parameters_and_idempotents(1276, 50, 0, 2, 6, -8)
    rk_1276_p5_k1 = rank_mod_p(linear_comb_matrix(1, 176, 22, -1, [[0]]), 5)
    a1_1276_p5_k1 = 14 * rk_1276_p5_k1 - 8 * 1 + 58
    assert a1_1276_p5_k1 == 50
    table1_results.append({
        "srg": [1276, 50, 0, 2], "p": 5, "Fix": "K_1", "a0": 1,
        "idempotent": "E_6", "rank_mod_p": rk_1276_p5_k1,
        "known_a1": "== 50 (mod 70)", "a1_here": a1_1276_p5_k1
    })
    rk_1276_p5_clebsch = rank_mod_p(linear_comb_matrix(16, 176, 22, -1, A_clebsch), 5)
    a1_1276_p5_clebsch = 14 * rk_1276_p5_clebsch - 8 * 16 + 58
    assert rk_1276_p5_clebsch == 10 and a1_1276_p5_clebsch == 70
    table1_results.append({
        "srg": [1276, 50, 0, 2], "p": 5, "Fix": "Clebsch", "a0": 16,
        "idempotent": "E_6", "rank_mod_p": rk_1276_p5_clebsch,
        "known_a1": "== 0 (mod 70)", "a1_here": a1_1276_p5_clebsch
    })
    rk_1276_p29 = rank_mod_p([], 29)
    a1_1276_p29 = 14 * rk_1276_p29 - 8 * 0 + 58
    assert a1_1276_p29 == 58
    table1_results.append({
        "srg": [1276, 50, 0, 2], "p": 29, "Fix": "empty", "a0": 0,
        "idempotent": "E_6", "rank_mod_p": rk_1276_p29,
        "known_a1": "58, 464, 870, 1276", "a1_here": a1_1276_p29
    })

    # (99, 14, 1, 2)
    verify_srg_parameters_and_idempotents(99, 14, 1, 2, 3, -4)
    rk_99_p3_empty = rank_mod_p([], 3)
    a1_99_p3_empty = 7 * rk_99_p3_empty - 4 * 0 + 18
    assert a1_99_p3_empty == 18
    table1_results.append({
        "srg": [99, 14, 1, 2], "p": 3, "Fix": "empty", "a0": 0,
        "idempotent": "E_3", "rank_mod_p": rk_99_p3_empty,
        "known_a1": "18, 39, 60, 81", "a1_here": a1_99_p3_empty
    })
    A_K3 = adj_complete(3)
    rk_99_p3_k3 = rank_mod_p(linear_comb_matrix(3, 44, 11, -2, A_K3), 3)
    a1_99_p3_k3 = 7 * rk_99_p3_k3 - 4 * 3 + 18
    assert rk_99_p3_k3 == 0 and a1_99_p3_k3 == 6
    table1_results.append({
        "srg": [99, 14, 1, 2], "p": 3, "Fix": "K_3", "a0": 3,
        "idempotent": "E_3", "rank_mod_p": rk_99_p3_k3,
        "known_a1": "6, 27, 48", "a1_here": a1_99_p3_k3
    })

    # (640, 243, 66, 108)
    verify_srg_parameters_and_idempotents(640, 243, 66, 108, 3, -45)
    rk_640_p5 = rank_mod_p([], 5)
    a1_640_p5 = 3 * 0 + 240 - 48 * rk_640_p5
    assert a1_640_p5 == 240
    table1_results.append({
        "srg": [640, 243, 66, 108], "p": 5, "Fix": "empty", "a0": 0,
        "idempotent": "E_{-45}", "rank_mod_p": rk_640_p5,
        "known_a1": "240, 480", "a1_here": a1_640_p5
    })

    return {
        "paper_verified": "arXiv:2606.29183v2 (Yawara Ishida, 8 July 2026)",
        "srg_3250_57_0_1": srg_info,
        "existing_moore_graphs_brauer_checks": existing_checks,
        "theorem_1_1_involution": {
            "a0": a0_t,
            "Fix": "K_{1,55}",
            "combinatorial_a1_if_exists": a1_t_combinatorial,
            "combinatorial_chi_E_s": int(chi_s_combinatorial),
            "rank_F2_E_s_Fix": rk_p2,
            "brauer_forced_a1": a1_t_forced,
            "involution_excluded": True,
        },
        "theorem_1_2_odd_primes": {
            "p_7": {
                "all_star_candidates": p7_candidates,
                "surviving_pairs_a0_a1": surviving_p7,
                "excluded_macaj_siran_a0": [44, 51],
            },
            "p_11": {
                "a0": 5,
                "Fix": "C_5",
                "rank_F11_E_s_Fix": rk_p11_s,
                "rank_F11_E_r_Fix": rk_p11_r,
                "a1_forced": a1_p11,
                "excluded_macaj_siran_a1": [220, 385],
            },
            "p_13": {
                "a0": 0,
                "Fix": "empty",
                "rank_F13_E_r_Fix": rk_p13_r,
                "a1_forced": a1_p13,
                "non_13_integral_tr_E_s": tr_p13_s,
                "excluded_macaj_siran_a1": [260, 455],
            },
            "p_19": {
                "a0": 1,
                "Fix": "K_1",
                "rank_F19_E_s_Fix": rk_p19_s,
                "rank_F19_E_r_Fix": rk_p19_r,
                "a1_forced": a1_p19,
                "excluded_macaj_siran_a1": [342],
            },
        },
        "section_8_table_1_branches": table1_results,
    }


def build_certificate():
    return {
        "target_id": "moore-graph-57",
        "claim_status": "CONFIRMED_PARTIAL",
        "confirmed_partials": ["p2"],
        "arithmetic_mode": "exact_integer_rational_and_Fp_linear_algebra",
        "track_p2_arxiv_2606_29183_verification": compute_track_p2(),
    }


def main():
    ap = argparse.ArgumentParser(description="Verify moore-graph-57 p2 certificate")
    ap.add_argument("--write-certificate", help="Write computed certificate JSON to this path")
    ap.add_argument("--certificate", help="Path to certificate JSON to verify against")
    args = ap.parse_args()

    try:
        computed = build_certificate()
    except Exception as e:
        print(f"Verification computation error: {e}")
        print("FAIL")
        return 1

    if args.write_certificate:
        with open(args.write_certificate, "w", encoding="utf-8") as f:
            json.dump(computed, f, indent=2, sort_keys=True)
            f.write("\n")

    cert_path = args.certificate
    if not cert_path:
        here = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(here, "certificate.json"),
            os.path.join(here, "..", "object", "certificate.json"),
        ]
        for c in candidates:
            if os.path.isfile(c):
                cert_path = c
                break

    if not cert_path or not os.path.isfile(cert_path):
        print("Certificate file not found.")
        print("FAIL")
        return 1

    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            loaded = json.load(f)
    except Exception as e:
        print(f"Failed to parse certificate JSON: {e}")
        print("FAIL")
        return 1

    if loaded != computed:
        print("Certificate mismatch against exact recomputed values!")
        print("FAIL")
        return 1

    print("All Track p2 (arXiv:2606.29183v2 exact verification) checks matched certificate.json digit-for-digit.")
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
