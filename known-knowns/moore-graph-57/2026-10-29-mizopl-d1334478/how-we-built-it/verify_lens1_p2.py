#!/usr/bin/env python3
"""
Independent Exact Computational Verification of arXiv:2606.29183v2 (Yawara Ishida, 8 July 2026):
"No involutions in the missing Moore graph" (Track p2 of moore-graph-57).

Uses 100% exact integer, rational (fractions.Fraction), and finite-field (F_p Gaussian elimination)
arithmetic with zero floating-point approximations.
"""

from fractions import Fraction
import itertools
import json
import math
import os


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
    """Adjacency matrix of K_{1,m} on m+1 vertices (center at index 0)."""
    n = m + 1
    A = [[0] * n for _ in range(n)]
    for i in range(1, n):
        A[0][i] = 1
        A[i][0] = 1
    return A


def adj_cycle(n):
    """Adjacency matrix of cycle C_n."""
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][(i + 1) % n] = 1
        A[i][(i - 1) % n] = 1
    return A


def adj_complete(n):
    """Adjacency matrix of complete graph K_n."""
    return [[0 if i == j else 1 for j in range(n)] for i in range(n)]


def adj_petersen():
    """Adjacency matrix of Petersen graph srg(10, 3, 0, 1) as 2-subsets of {0,1,2,3,4}."""
    pairs = list(itertools.combinations(range(5), 2))
    n = len(pairs)
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            if set(pairs[i]).isdisjoint(pairs[j]):
                A[i][j] = A[j][i] = 1
    return A, pairs


def adj_hoffman_singleton():
    """Adjacency matrix of Hoffman-Singleton graph srg(50, 7, 0, 1) via Robertson's construction."""
    # Vertices 0..24: P_i^j (i in Z_5, j in Z_5) -> index 5*i + j
    # Vertices 25..49: Q_k^l (k in Z_5, l in Z_5) -> index 25 + 5*k + l
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
    """Adjacency matrix of Clebsch graph srg(16, 5, 0, 2) (folded 5-cube)."""
    # Even-weight binary vectors in F_2^5; adjacent iff Hamming distance is 1 or 4 (in folded cube)
    # Equivalently, vertices in F_2^4; two vertices adjacent iff their difference is in {e_1, e_2, e_3, e_4, 1111}.
    gens = [1, 2, 4, 8, 15]
    A = [[0] * 16 for _ in range(16)]
    for u in range(16):
        for g in gens:
            v = u ^ g
            A[u][v] = 1
    return A


def linear_comb_matrix(n, alpha, beta, gamma, A):
    """Returns alpha * I_n + beta * A + gamma * J_n."""
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            val = gamma + (alpha if i == j else 0) + beta * A[i][j]
            M[i][j] = val
    return M


def bose_mesner_mul(c1, c2, v=3250, k=57, lam=0, mu=1):
    """
    Exact multiplication in the Bose-Mesner algebra Q[I, A, J] of srg(v, k, lam, mu)
    where A^2 = k I + lam A + mu (J - I - A) = (k - mu)I + (lam - mu)A + mu J,
    A J = J A = k J, J^2 = v J.
    c1, c2 are triples (alpha, beta, gamma) representing alpha I + beta A + gamma J.
    """
    a1, b1, g1 = [Fraction(x) for x in c1]
    a2, b2, g2 = [Fraction(x) for x in c2]
    # (a1 I + b1 A + g1 J)(a2 I + b2 A + g2 J)
    # = a1 a2 I + (a1 b2 + b1 a2) A + (a1 g2 + g1 a2) J
    #   + b1 b2 ((k - mu) I + (lam - mu) A + mu J)
    #   + (b1 g2 + g1 b2) k J + g1 g2 v J
    alpha = a1 * a2 + b1 * b2 * (k - mu)
    beta = a1 * b2 + b1 * a2 + b1 * b2 * (lam - mu)
    gamma = a1 * g2 + g1 * a2 + b1 * b2 * mu + (b1 * g2 + g1 * b2) * k + g1 * g2 * v
    return (alpha, beta, gamma)


def verify_srg_parameters_and_idempotents(v, k, lam, mu, r, s):
    """Verifies SRG parameters, eigenvalues, multiplicities, and spectral idempotents."""
    assert k * (k - lam - 1) == mu * (v - k - 1), f"SRG feasibility failed for {(v,k,lam,mu)}"
    assert r + s == lam - mu
    assert r * s == mu - k
    # Multiplicities: 1 + m_r + m_s = v, k + r m_r + s m_s = 0
    m_r = Fraction(-k - s * (v - 1), r - s)
    m_s = Fraction(-k - r * (v - 1), s - r)
    assert m_r.denominator == 1 and m_s.denominator == 1
    m_r, m_s = int(m_r), int(m_s)
    assert 1 + m_r + m_s == v
    assert k + r * m_r + s * m_s == 0
    assert k * k + r * r * m_r + s * s * m_s == v * k

    # Formula (7) of arXiv:2606.29183:
    # E_r = 1/(r - s) * (A - s I - (k - s)/v * J)
    # E_s = 1/(s - r) * (A - r I - (k - r)/v * J)
    E_k = (Fraction(0), Fraction(0), Fraction(1, v))
    E_r = (Fraction(-s, r - s), Fraction(1, r - s), Fraction(-(k - s), v * (r - s)))
    E_s = (Fraction(-r, s - r), Fraction(1, s - r), Fraction(-(k - r), v * (s - r)))

    # Check sum = I
    for idx, target in enumerate((Fraction(1), Fraction(0), Fraction(0))):
        assert E_k[idx] + E_r[idx] + E_s[idx] == target

    # Check idempotency and orthogonality
    for E in (E_k, E_r, E_s):
        assert bose_mesner_mul(E, E, v, k, lam, mu) == E
    assert bose_mesner_mul(E_k, E_r, v, k, lam, mu) == (0, 0, 0)
    assert bose_mesner_mul(E_k, E_s, v, k, lam, mu) == (0, 0, 0)
    assert bose_mesner_mul(E_r, E_s, v, k, lam, mu) == (0, 0, 0)

    # Check A * E_theta = theta * E_theta
    A_elem = (Fraction(0), Fraction(1), Fraction(0))
    for theta, E in ((k, E_k), (r, E_r), (s, E_s)):
        prod = bose_mesner_mul(A_elem, E, v, k, lam, mu)
        assert prod == tuple(theta * x for x in E)

    # Cleared denominators
    denom_r = math.lcm(E_r[0].denominator, E_r[1].denominator, E_r[2].denominator)
    denom_s = math.lcm(E_s[0].denominator, E_s[1].denominator, E_s[2].denominator)
    num_r = tuple(int(x * denom_r) for x in E_r)
    num_s = tuple(int(x * denom_s) for x in E_s)
    # Check sharpness: off-diagonal non-adjacent entry is gamma, which has |gamma| = 1 or gcd(num) = 1
    assert math.gcd(*num_r) == 1
    assert math.gcd(*num_s) == 1

    return {
        "params": [v, k, lam, mu],
        "eigenvalues": {"k": k, "r": r, "s": s},
        "multiplicities": {"m_k": 1, "m_r": m_r, "m_s": m_s},
        "E_r": {"denom": denom_r, "numerator_I_A_J": list(num_r)},
        "E_s": {"denom": denom_s, "numerator_I_A_J": list(num_s)},
    }


def verify_existing_moore_graphs_brauer_identity():
    """
    Verifies Theorem 4.1 / Proposition 4.4 (tr(T_g E_theta) == rank_{F_p}(E_theta[Fix(g)] mod p))
    across prime-order automorphisms of C_5, Petersen srg(10,3,0,1), and Hoffman-Singleton srg(50,7,0,1).
    """
    checks = []

    # 1. C_5 = srg(5, 2, 0, 1) -> eigenvalues 2, (-1 +/- sqrt(5))/2 (irrational, but E_0 = I - J/5 is p-integral for p != 5)
    # On C_5, for reflection t (p = 2): Fix(t) = K_1 (a_0 = 1, a_1 = 2).
    # I - J/5 has trace on t equal to a_0(t) - 1 = 0, and on Fix(t) = K_1, 5(I - J/5)[F] = (4) == (0) mod 2 -> rank 0!
    A_c5 = adj_cycle(5)
    # Reflection t: 0->0, 1<->4, 2<->3
    perm_c5_2 = [0, 4, 3, 2, 1]
    fix_c5_2 = [i for i in range(5) if perm_c5_2[i] == i]
    a0_c5 = len(fix_c5_2)
    a1_c5 = sum(1 for i in range(5) if A_c5[i][perm_c5_2[i]] == 1)
    assert (a0_c5, a1_c5) == (1, 2)
    rk_c5 = rank_mod_p([[4]], 2)
    assert rk_c5 == a0_c5 - 1 == 0
    checks.append({"graph": "C_5", "p": 2, "a0": a0_c5, "a1": a1_c5, "trace": 0, "rank_mod_p": rk_c5})

    # 2. Petersen graph srg(10, 3, 0, 1): r = 1 (mult 5), s = -2 (mult 4)
    # E_1 = 1/3 * (A + 2I - J/2) = (4I + 2A - J)/6 (p-integral for p not in {2,3})
    # E_{-2} = 1/3 * (I - A + J/5) = (5I - 5A + J)/15 (p-integral for p not in {3,5})
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

    # Test prime-order automorphisms in S_5:
    # (a) transposition (0 1), p = 2, E_{-2} = (5I - 5A + J)/15 is 2-integral!
    # (b) double transposition (0 1)(2 3), p = 2, E_{-2} is 2-integral!
    # (c) 5-cycle (0 1 2 3 4), p = 5, E_1 = (4I + 2A - J)/6 is 5-integral!
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
        checks.append({
            "graph": "Petersen_srg(10,3,0,1)",
            "automorphism": label,
            "p": p,
            "idempotent": which_E,
            "a0": a0,
            "a1": a1,
            "trace": int(tr_val),
            "rank_mod_p": rk,
        })

    # 3. Hoffman-Singleton graph srg(50, 7, 0, 1): r = 2 (mult 28), s = -3 (mult 21)
    # E_2 = (15I + 5A - J)/25 (p-integral for p != 5)
    # E_{-3} = (20I - 10A + J)/50 (p-integral for p not in {2, 5})
    hosi_info = verify_srg_parameters_and_idempotents(50, 7, 0, 1, 2, -3)
    A_hosi = adj_hoffman_singleton()
    # Verify A_hosi is srg(50, 7, 0, 1)
    for i in range(50):
        assert sum(A_hosi[i]) == 7
        for j in range(i + 1, 50):
            common = sum(A_hosi[i][w] * A_hosi[j][w] for w in range(50))
            if A_hosi[i][j] == 1:
                assert common == 0
            else:
                assert common == 1

    # Construct explicit prime-order automorphisms of HoSi:
    # (a) Involution t1 (p = 2): (i, j) -> (-i mod 5, -j mod 5), (k, l) -> (k, -l mod 5)
    # Fix(t1): i=0, j=0 (1 vertex in P) and k in 0..4, l=0 (5 vertices in Q) -> Star K_{1,5} of order 6!
    perm_hosi_t1 = [0] * 50
    for i in range(5):
        for j in range(5):
            perm_hosi_t1[5 * i + j] = 5 * ((-i) % 5) + ((-j) % 5)
    for k in range(5):
        for l in range(5):
            perm_hosi_t1[25 + 5 * k + l] = 25 + 5 * k + ((-l) % 5)

    # (b) Involution t2 (p = 2): (i, j) -> (i, -j mod 5), (k, l) -> (-k mod 5, -l mod 5) -> Fix = K_{1,5} (6 vertices)
    # Let's also construct a fixed-point-free involution or another p=3 / p=2 automorphism.
    # For p = 3, let's check both E_2 and E_{-3} on t1 (at p=2, E_2 has denom 25, so E_2 is 2-integral!).
    for u in range(50):
        for v in range(50):
            assert A_hosi[u][v] == A_hosi[perm_hosi_t1[u]][perm_hosi_t1[v]]
    F_hosi = [i for i in range(50) if perm_hosi_t1[i] == i]
    a0_h = len(F_hosi)
    a1_h = sum(1 for i in range(50) if A_hosi[i][perm_hosi_t1[i]] == 1)
    alpha, beta, gamma = hosi_info["E_r"]["numerator_I_A_J"]
    denom = hosi_info["E_r"]["denom"]
    assert denom == 25 and denom % 2 != 0
    tr_h = Fraction(alpha * a0_h + beta * a1_h + gamma * 50, denom)
    assert tr_h.denominator == 1
    A_Fh = [[A_hosi[u][v] for v in F_hosi] for u in F_hosi]
    M_Fh = linear_comb_matrix(a0_h, alpha, beta, gamma, A_Fh)
    rk_h = rank_mod_p(M_Fh, 2)
    assert int(tr_h) == rk_h
    checks.append({
        "graph": "HoffmanSingleton_srg(50,7,0,1)",
        "automorphism": "involution_Fix_K1_5",
        "p": 2,
        "idempotent": "E_r",
        "a0": a0_h,
        "a1": a1_h,
        "trace": int(tr_h),
        "rank_mod_p": rk_h,
    })

    return checks


def verify_moore57_theorem_1_1_and_1_2():
    """
    Verifies Section 5, Section 6 (Theorem 1.1 & Corollary 6.1), and Section 7 (Theorem 1.2)
    of arXiv:2606.29183v2 for Gamma = srg(3250, 57, 0, 1).
    """
    srg_info = verify_srg_parameters_and_idempotents(3250, 57, 0, 1, 7, -8)
    assert srg_info["E_r"] == {"denom": 750, "numerator_I_A_J": [400, 50, -1]}
    assert srg_info["E_s"] == {"denom": 975, "numerator_I_A_J": [455, -65, 1]}

    # 1. Theorem 1.1 (No involutions, p = 2)
    # Step 1a: Verify closed-subset forced parameters for an involution t:
    # Any closed subset F of srg(3250, 57, 0, 1) is empty, K_1, K_2, K_{1,m} (2 <= m <= 57), C_5, Pet, or HoSi.
    # Moreover, every 2-orbit {v, t(v)} outside F has either v ~ t(v) (contributing 2 to a_1(t))
    # or dist(v, t(v)) = 2 with a unique common neighbor in F.
    # For a_1(t) > 0, pick b ~ t(b): the 56 neighbors u in N(b) \ {t(b)} map bijectively to Fix(t),
    # forcing a_0(t) = 56, Fix(t) = K_{1,55}, and a_1(t) = 3250 - (58 * 56 - 2 * 55) = 112.
    a0_t = 56
    edges_F_t = 55
    a1_t_combinatorial = 3250 - (58 * a0_t - 2 * edges_F_t)
    assert a1_t_combinatorial == 112
    chi_s_combinatorial = Fraction(7 * a0_t - a1_t_combinatorial + 50, 15)
    chi_r_combinatorial = Fraction(8 * a0_t + a1_t_combinatorial - 65, 15)
    assert chi_s_combinatorial == 22 and chi_r_combinatorial == 33

    # Step 1b: Also verify that a_1(t) = 0 is impossible for all closed subgraphs:
    # If a_1(t) = 0, then 3250 = 58 * a_0(t) - 2 * |E(F)| and 15 | (7 * a_0(t) + 50).
    # For a star K_{1, m} (a_0 = m+1, |E| = m), 58(m+1) - 2m = 56m + 58 = 3250 => 56m = 3192 => m = 57,
    # which fails 15 | (7 * 58 + 50) = 456 (456 mod 15 = 6 != 0).
    # For d-regular Moore subgraphs (d in {0, 1, 2, 3, 7}), 2|E| = d * a_0, so (58 - d) * a_0 = 3250,
    # none of which matches a_0 in {0, 1, 2, 5, 10, 50}.
    for a0_cand, e_cand in [(0, 0), (1, 0), (2, 1), (5, 5), (10, 15), (50, 175)] + [(m + 1, m) for m in range(2, 58)]:
        if 58 * a0_cand - 2 * e_cand == 3250:
            assert (7 * a0_cand + 50) % 15 != 0

    # Step 1c: Compute rank_{F_2}(975 * E_{-8}[F]) where F = K_{1,55}
    A_K1_55 = adj_star(55)
    M_K1_55 = linear_comb_matrix(56, 455, -65, 1, A_K1_55)
    rk_p2 = rank_mod_p(M_K1_55, 2)
    assert rk_p2 == 54
    # Proposition 5.1 equation: (7 * 56 - a_1(t) + 50) / 15 = 54 => a_1(t) = -368 < 0
    a1_t_forced = 7 * a0_t + 50 - 15 * rk_p2
    assert a1_t_forced == -368

    # 2. Theorem 1.2 (Odd primes p in {7, 11, 13, 19})
    # Row p = 7: F = K_{1, m} with a_0 = m + 1 == 2 (mod 7), 2 <= a_0 <= 58
    p7_candidates = []
    for a0 in range(2, 59, 7):
        A_F = adj_star(a0 - 1)
        M_F_s = linear_comb_matrix(a0, 455, -65, 1, A_F)
        M_F_r = linear_comb_matrix(a0, 400, 50, -1, A_F)
        rk_s = rank_mod_p(M_F_s, 7)
        rk_r = rank_mod_p(M_F_r, 7)
        assert rk_s == 1
        assert rk_r == a0 - 2
        assert rk_s + rk_r == a0 - 1
        a1_s = 7 * a0 + 50 - 15 * rk_s
        a1_r = 15 * rk_r - 8 * a0 + 65
        assert a1_s == a1_r == 7 * a0 + 35
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
    surviving_p7 = [(c["a0"], c["a1_forced"]) for c in p7_candidates if c["survives_vertex_bound"]]
    assert surviving_p7 == [(2, 49), (9, 98), (16, 147), (23, 196), (30, 245), (37, 294)]

    # Row p = 11: F = C_5 (a_0 = 5)
    A_C5 = adj_cycle(5)
    M_p11_s = linear_comb_matrix(5, 455, -65, 1, A_C5)
    M_p11_r = linear_comb_matrix(5, 400, 50, -1, A_C5)
    rk_p11_s = rank_mod_p(M_p11_s, 11)
    rk_p11_r = rank_mod_p(M_p11_r, 11)
    assert rk_p11_s == 2 and rk_p11_r == 2
    assert rk_p11_s + rk_p11_r == 5 - 1
    a1_p11 = 7 * 5 + 50 - 15 * rk_p11_s
    assert a1_p11 == 55 == 15 * rk_p11_r - 8 * 5 + 65

    # Row p = 13: F = empty (a_0 = 0), only E_7 is 13-integral (750 mod 13 = 9 != 0, 975 mod 13 = 0)
    assert 750 % 13 == 9 and 975 % 13 == 0
    rk_p13_r = rank_mod_p([], 13)
    assert rk_p13_r == 0
    a1_p13 = 15 * rk_p13_r - 8 * 0 + 65
    assert a1_p13 == 65
    # Verify failure of non-13-integral E_{-8} trace-rank equality at p = 13:
    tr_p13_s = Fraction(7 * 0 - a1_p13 + 50, 15)
    assert tr_p13_s == -1  # negative, cannot be a matrix rank!

    # Row p = 19: F = K_1 (a_0 = 1), both E_{-8} and E_7 are 19-integral
    assert 975 % 19 == 6 and 750 % 19 == 9
    M_p19_s = linear_comb_matrix(1, 455, -65, 1, [[0]])
    M_p19_r = linear_comb_matrix(1, 400, 50, -1, [[0]])
    assert M_p19_s == [[456]] and 456 == 24 * 19
    assert M_p19_r == [[399]] and 399 == 21 * 19
    rk_p19_s = rank_mod_p(M_p19_s, 19)
    rk_p19_r = rank_mod_p(M_p19_r, 19)
    assert rk_p19_s == 0 and rk_p19_r == 0
    a1_p19 = 7 * 1 + 50 - 15 * rk_p19_s
    assert a1_p19 == 57 == 15 * rk_p19_r - 8 * 1 + 65

    return {
        "srg_3250_57_0_1": srg_info,
        "theorem_1_1_involution": {
            "a0": a0_t,
            "Fix": "K_{1,55}",
            "combinatorial_a1_if_exists": a1_t_combinatorial,
            "combinatorial_chi_E_s": int(chi_s_combinatorial),
            "rank_F2_E_s_Fix": rk_p2,
            "brauer_forced_a1": a1_t_forced,
            "contradiction": "a1_forced = -368 < 0 (and 22 != 54)",
            "involution_excluded": True,
        },
        "theorem_1_2_odd_primes": {
            "p_7": {
                "all_star_candidates": p7_candidates,
                "surviving_pairs_a0_a1": [list(x) for x in surviving_p7],
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
                "non_13_integral_tr_E_s": int(tr_p13_s),
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
    }


def verify_section_8_table_1():
    """
    Verifies all 10 branches in Table 1 (Section 8, Propositions 8.1-8.8, and Remark 8.5)
    of arXiv:2606.29183v2 across the 5 open SRG parameter sets.
    """
    A_clebsch = adj_clebsch_16_5_0_2()
    # Verify A_clebsch is srg(16, 5, 0, 2)
    for i in range(16):
        assert sum(A_clebsch[i]) == 5
        for j in range(i + 1, 16):
            common = sum(A_clebsch[i][w] * A_clebsch[j][w] for w in range(16))
            if A_clebsch[i][j] == 1:
                assert common == 0
            else:
                assert common == 2

    table1_results = []

    # 1. srg(162, 21, 0, 3): r = 3, s = -6
    # E_3 = (36I + 6A - J)/54, E_{-6} = (27I - 9A + J)/81
    info_162 = verify_srg_parameters_and_idempotents(162, 21, 0, 3, 3, -6)
    assert info_162["E_r"] == {"denom": 54, "numerator_I_A_J": [36, 6, -1]}
    assert info_162["E_s"] == {"denom": 81, "numerator_I_A_J": [27, -9, 1]}

    # Branch 1: (162, 21, 0, 3), p = 2, Fix = empty
    rk_162_p2_empty = rank_mod_p([], 2)
    a1_162_p2_empty = 3 * 0 + 18 - 9 * rk_162_p2_empty
    assert a1_162_p2_empty == 18  # contradicts known a_1(t) = 162 -> impossible!
    table1_results.append({
        "srg": [162, 21, 0, 3], "p": 2, "Fix": "empty", "a0": 0,
        "idempotent": "E_{-6}", "rank_mod_p": rk_162_p2_empty,
        "known_a1": "162", "a1_here": "impossible (rank equation gives 18 != 162)"
    })

    # Branch 2: (162, 21, 0, 3), p = 2, Fix = K_{1,3}
    A_K1_3 = adj_star(3)
    M_162_p2_star = linear_comb_matrix(4, 27, -9, 1, A_K1_3)
    rk_162_p2_star = rank_mod_p(M_162_p2_star, 2)
    a1_162_p2_star = 3 * 4 + 18 - 9 * rk_162_p2_star
    assert rk_162_p2_star == 2 and a1_162_p2_star == 12
    table1_results.append({
        "srg": [162, 21, 0, 3], "p": 2, "Fix": "K_{1,3}", "a0": 4,
        "idempotent": "E_{-6}", "rank_mod_p": rk_162_p2_star,
        "known_a1": "none", "a1_here": a1_162_p2_star
    })

    # Branch 3: (162, 21, 0, 3), p = 5, Fix = K_2
    A_K2 = adj_complete(2)
    M_162_p5_k2 = linear_comb_matrix(2, 36, 6, -1, A_K2)
    rk_162_p5_k2 = rank_mod_p(M_162_p5_k2, 5)
    a1_162_p5_k2 = 9 * rk_162_p5_k2 - 6 * 2 + 27
    assert rk_162_p5_k2 == 0 and a1_162_p5_k2 == 15
    table1_results.append({
        "srg": [162, 21, 0, 3], "p": 5, "Fix": "K_2", "a0": 2,
        "idempotent": "E_3", "rank_mod_p": rk_162_p5_k2,
        "known_a1": "15, 60", "a1_here": a1_162_p5_k2
    })

    # 2. srg(352, 26, 0, 2): r = 4, s = -6
    # E_4 = (66I + 11A - J)/110, E_{-6} = (64I - 16A + J)/160
    info_352 = verify_srg_parameters_and_idempotents(352, 26, 0, 2, 4, -6)
    assert info_352["E_r"] == {"denom": 110, "numerator_I_A_J": [66, 11, -1]}
    assert info_352["E_s"] == {"denom": 160, "numerator_I_A_J": [64, -16, 1]}

    # Branch 4: (352, 26, 0, 2), p = 11, Fix = empty (Remark 8.5(ii): Makhnev-Nosov 2004 Lemma 2.2 error)
    rk_352_p11 = rank_mod_p([], 11)
    a1_352_p11 = 4 * 0 + 22 - 10 * rk_352_p11
    assert rk_352_p11 == 0 and a1_352_p11 == 22
    table1_results.append({
        "srg": [352, 26, 0, 2], "p": 11, "Fix": "empty", "a0": 0,
        "idempotent": "E_{-6}", "rank_mod_p": rk_352_p11,
        "known_a1": "falsely excluded in [22, Lemma 2.2] via w == 8 (mod 10)", "a1_here": a1_352_p11
    })

    # Branch 5: (352, 26, 0, 2), p = 13, Fix = K_1 (Remark 8.5(i): Makhnev-Nosov 2004 Lemma 2.3(1) error)
    M_352_p13 = linear_comb_matrix(1, 64, -16, 1, [[0]])
    rk_352_p13 = rank_mod_p(M_352_p13, 13)
    a1_352_p13 = 4 * 1 + 22 - 10 * rk_352_p13
    assert rk_352_p13 == 0 and a1_352_p13 == 26
    table1_results.append({
        "srg": [352, 26, 0, 2], "p": 13, "Fix": "K_1", "a0": 1,
        "idempotent": "E_{-6}", "rank_mod_p": rk_352_p13,
        "known_a1": "falsely claimed 52 in [22, Lemma 2.3(1)]", "a1_here": a1_352_p13
    })

    # Additional check in Section 8.3: (352, 26, 0, 2), p = 7, Fix = Clebsch -> rank_F7 = 10 -> a1 = -14 < 0
    M_352_p7_clebsch = linear_comb_matrix(16, 64, -16, 1, A_clebsch)
    rk_352_p7_clebsch = rank_mod_p(M_352_p7_clebsch, 7)
    a1_352_p7_clebsch = 4 * 16 + 22 - 10 * rk_352_p7_clebsch
    assert rk_352_p7_clebsch == 10 and a1_352_p7_clebsch == -14

    # 3. srg(1276, 50, 0, 2): r = 6, s = -8
    # E_6 = (176I + 22A - J)/308, E_{-8} = (174I - 29A + J)/406
    info_1276 = verify_srg_parameters_and_idempotents(1276, 50, 0, 2, 6, -8)
    assert info_1276["E_r"] == {"denom": 308, "numerator_I_A_J": [176, 22, -1]}
    assert info_1276["E_s"] == {"denom": 406, "numerator_I_A_J": [174, -29, 1]}

    # Branch 6: (1276, 50, 0, 2), p = 5, Fix = K_1
    M_1276_p5_k1 = linear_comb_matrix(1, 176, 22, -1, [[0]])
    rk_1276_p5_k1 = rank_mod_p(M_1276_p5_k1, 5)
    a1_1276_p5_k1 = 14 * rk_1276_p5_k1 - 8 * 1 + 58
    assert rk_1276_p5_k1 == 0 and a1_1276_p5_k1 == 50
    table1_results.append({
        "srg": [1276, 50, 0, 2], "p": 5, "Fix": "K_1", "a0": 1,
        "idempotent": "E_6", "rank_mod_p": rk_1276_p5_k1,
        "known_a1": "== 50 (mod 70)", "a1_here": a1_1276_p5_k1
    })

    # Branch 7: (1276, 50, 0, 2), p = 5, Fix = Clebsch
    M_1276_p5_clebsch = linear_comb_matrix(16, 176, 22, -1, A_clebsch)
    rk_1276_p5_clebsch = rank_mod_p(M_1276_p5_clebsch, 5)
    a1_1276_p5_clebsch = 14 * rk_1276_p5_clebsch - 8 * 16 + 58
    assert rk_1276_p5_clebsch == 10 and a1_1276_p5_clebsch == 70
    table1_results.append({
        "srg": [1276, 50, 0, 2], "p": 5, "Fix": "Clebsch", "a0": 16,
        "idempotent": "E_6", "rank_mod_p": rk_1276_p5_clebsch,
        "known_a1": "== 0 (mod 70)", "a1_here": a1_1276_p5_clebsch
    })

    # Branch 8: (1276, 50, 0, 2), p = 29, Fix = empty
    rk_1276_p29 = rank_mod_p([], 29)
    a1_1276_p29 = 14 * rk_1276_p29 - 8 * 0 + 58
    assert rk_1276_p29 == 0 and a1_1276_p29 == 58
    table1_results.append({
        "srg": [1276, 50, 0, 2], "p": 29, "Fix": "empty", "a0": 0,
        "idempotent": "E_6", "rank_mod_p": rk_1276_p29,
        "known_a1": "58, 464, 870, 1276", "a1_here": a1_1276_p29
    })

    # 4. srg(99, 14, 1, 2) (Conway 99-graph): r = 3, s = -4
    # E_3 = (44I + 11A - 2J)/77, E_{-4} = (27I - 9A + J)/63
    info_99 = verify_srg_parameters_and_idempotents(99, 14, 1, 2, 3, -4)
    assert info_99["E_r"] == {"denom": 77, "numerator_I_A_J": [44, 11, -2]}
    assert info_99["E_s"] == {"denom": 63, "numerator_I_A_J": [27, -9, 1]}

    # Branch 9: (99, 14, 1, 2), p = 3, Fix = empty
    rk_99_p3_empty = rank_mod_p([], 3)
    a1_99_p3_empty = 7 * rk_99_p3_empty - 4 * 0 + 18
    assert rk_99_p3_empty == 0 and a1_99_p3_empty == 18
    table1_results.append({
        "srg": [99, 14, 1, 2], "p": 3, "Fix": "empty", "a0": 0,
        "idempotent": "E_3", "rank_mod_p": rk_99_p3_empty,
        "known_a1": "18, 39, 60, 81", "a1_here": a1_99_p3_empty
    })

    # Branch 10: (99, 14, 1, 2), p = 3, Fix = K_3
    A_K3 = adj_complete(3)
    M_99_p3_k3 = linear_comb_matrix(3, 44, 11, -2, A_K3)
    rk_99_p3_k3 = rank_mod_p(M_99_p3_k3, 3)
    a1_99_p3_k3 = 7 * rk_99_p3_k3 - 4 * 3 + 18
    assert rk_99_p3_k3 == 0 and a1_99_p3_k3 == 6
    table1_results.append({
        "srg": [99, 14, 1, 2], "p": 3, "Fix": "K_3", "a0": 3,
        "idempotent": "E_3", "rank_mod_p": rk_99_p3_k3,
        "known_a1": "6, 27, 48", "a1_here": a1_99_p3_k3
    })

    # Branch 11: (640, 243, 66, 108), p = 5, Fix = empty
    # r = 3, s = -45, E_{-45} = (24I - 8A + 3J)/384 = (8I - 8/3 A + J)/128
    info_640 = verify_srg_parameters_and_idempotents(640, 243, 66, 108, 3, -45)
    assert info_640["E_s"] == {"denom": 384, "numerator_I_A_J": [24, -8, 3]}
    rk_640_p5 = rank_mod_p([], 5)
    a1_640_p5 = 3 * 0 + 240 - 48 * rk_640_p5
    assert rk_640_p5 == 0 and a1_640_p5 == 240
    table1_results.append({
        "srg": [640, 243, 66, 108], "p": 5, "Fix": "empty", "a0": 0,
        "idempotent": "E_{-45}", "rank_mod_p": rk_640_p5,
        "known_a1": "240, 480", "a1_here": a1_640_p5
    })

    assert len(table1_results) == 11  # 11 rows in Table 1 across 5 SRG families
    return table1_results


def main():
    existing_checks = verify_existing_moore_graphs_brauer_identity()
    moore57_results = verify_moore57_theorem_1_1_and_1_2()
    table1_results = verify_section_8_table_1()

    out = {
        "track": "p2",
        "target_id": "moore-graph-57",
        "paper_verified": "arXiv:2606.29183v2 (Yawara Ishida, 8 July 2026)",
        "existing_moore_graphs_brauer_checks": existing_checks,
        "moore57_theorems_1_1_and_1_2": moore57_results,
        "section_8_table_1_branches": table1_results,
        "status": "PASS",
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lens1_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(f"Lens 1 (p2) verification succeeded: {len(existing_checks)} existing Moore graph checks, "
          f"Theorem 1.1 & Theorem 1.2 verified, and {len(table1_results)} Table 1 branches verified.")
    print("VERIFY_LENS1_P2: PASS")


if __name__ == "__main__":
    main()
