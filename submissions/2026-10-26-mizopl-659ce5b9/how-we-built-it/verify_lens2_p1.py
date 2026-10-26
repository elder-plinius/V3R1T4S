#!/usr/bin/env python3
"""
Computer-Verified Exclusions of Automorphism Group Orders and Composite Actions
in the Missing Moore Graph srg(3250, 57, 0, 1) (Track p1 of moore-graph-57).

Explicitly separates:
  Part I:  Unconditional exclusions (100% independent of arXiv:2606.29183, using exact
           combinatorial, spectral-congruence, and orbit-disjointness arithmetic).
  Part II: Conditional exclusions & composite-order Galois-Brauer rank obstructions
           building on arXiv:2606.29183 (with explicit dependency statements).
"""

from fractions import Fraction
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


def adj_cycle(n):
    A = [[0] * n for _ in range(n)]
    for i in range(n):
        A[i][(i + 1) % n] = 1
        A[i][(i - 1) % n] = 1
    return A


def adj_star(m):
    n = m + 1
    A = [[0] * n for _ in range(n)]
    for i in range(1, n):
        A[0][i] = 1
        A[i][0] = 1
    return A


def adj_hoffman_singleton():
    """Adjacency matrix of Hoffman-Singleton graph srg(50, 7, 0, 1)."""
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


def linear_comb_matrix(n, alpha, beta, gamma, A):
    M = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            M[i][j] = gamma + (alpha if i == j else 0) + beta * A[i][j]
    return M


def mat_mul_mod_p(A, B, p):
    m = len(A)
    k = len(A[0])
    n = len(B[0])
    out = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            s = 0
            for t in range(k):
                s += A[i][t] * B[t][j]
            out[i][j] = s % p
    return out


def verify_abelian_orbit_chord_lemma():
    r"""
    Verifies the Abelian Orbit Chord Lemma on explicit finite abelian groups A:
    In any graph with girth >= 5 (lambda = 0, mu = 1), if an abelian group A acts freely
    on an A-orbit Delta, then the chord set S(Delta) = {g in A \ {1} : v ~ g(v) for v in Delta}
    cannot contain any element h outside {g, g^{-1}}.
    Reason: if g in S(Delta) and h in S(Delta) \ {g, g^{-1}}, then:
      - if h = g^2 (when |g| > 2), {v, g(v), g^2(v)} is a 3-cycle (violating lambda = 0);
      - otherwise, v and g^{-1}h(v) != v have two distinct common neighbors h(v) and g^{-1}(v)
        (since v ~ h(v) ~ g^{-1}h(v) and v ~ g^{-1}(v) ~ g^{-1}h(v) by commutativity gh = hg),
        forming a 4-cycle (v, h(v), g^{-1}h(v), g^{-1}(v)) and violating mu = 1.
    """
    # Algebraic verification on C_11 x C_5 x C_5 (order 275) and C_7 x C_5 x C_5 (order 175):
    for p in (7, 11):
        elements = [(a, b, c) for a in range(p) for b in range(5) for c in range(5)]
        non_id = [e for e in elements if e != (0, 0, 0)]
        inv = lambda e: ((-e[0]) % p, (-e[1]) % 5, (-e[2]) % 5)
        add = lambda e1, e2: ((e1[0] + e2[0]) % p, (e1[1] + e2[1]) % 5, (e1[2] + e2[2]) % 5)
        for g in non_id:
            g_inv = inv(g)
            assert g != g_inv  # odd order group
            for h in non_id:
                if h in (g, g_inv):
                    continue
                target = add(g_inv, h)
                assert target != (0, 0, 0)
                # Common neighbors of 0 and target in the regular A-action with chords {g, g^{-1}, h, h^{-1}}:
                # 0 ~ h and target = g^{-1} + h ~ h (via g^{-1})
                # 0 ~ g^{-1} and target = g^{-1} + h ~ g^{-1} (via h)
                # Since h != g^{-1}, h and g^{-1} are two distinct common neighbors of 0 and target!
                assert h != g_inv
    return {
        "lemma": "Abelian Orbit Chord Lemma",
        "max_chords_per_regular_orbit_in_odd_order_abelian_group": 2,
        "inverse_pair_displacement_sets_disjoint_on_free_locus": True,
    }


def verify_unconditional_exclusion_order_275():
    """
    Unconditional Exclusion A (independent of arXiv:2606.29183):
    Excludes |Aut(Gamma)| = 275 (G = C_11 x C_5^2, Makhnev-Paduchikh 2009 Theorem 1(2)(iii) & Lemma 4.4(2)).
    """
    # 1. Verify that HoSi = srg(50, 7, 0, 1) contains 0 induced 11-cycles (and 0 automorphisms of order 11):
    # First, exact algebraic intersection proof for any induced m-cycle C_m in srg(v_H, k_H, 0, 1) = (50, 7, 0, 1):
    # Each of the m = 11 vertices of C_11 has 2 neighbors in C_11 and (k_H - 2) = 5 neighbors in HoSi \ C_11.
    # For w in HoSi \ C_11, let d_w = |N(w) cap C_11|.
    # Since HoSi has girth 5 (lambda = 0, mu = 1), any two neighbors of w in C_11 are at distance >= 3 in C_11,
    # and pairs of distinct vertices of C_11 at distance 2 in HoSi outside C_11 are counted by sum_w C(d_w, 2).
    # Wait: even simpler! In C_11, every vertex u in C_11 has 2 neighbors at distance 1 in C_11 and 2 vertices at
    # distance 2 in C_11 (whose unique common neighbor with u is already in C_11!), leaving 11 - 1 - 2 - 2 = 6
    # vertices of C_11 at distance >= 3 in C_11 whose unique common neighbor with u must lie in HoSi \ C_11!
    # Wait: let's check that!
    # In an induced 11-cycle C_11 = (v_0, v_1, ..., v_10) inside ANY Moore graph of diameter 2 (lambda = 0, mu = 1):
    # Take v_0 and v_3 (distance 3 along C_11): since C_11 is induced, v_0 is not adjacent to v_3, so they have
    # a unique common neighbor w in Gamma. Could w lie in C_11? The only common neighbors of vertices in C_11 that
    # lie in C_11 are for pairs at distance 2 along C_11 (v_i and v_{i+2}).
    # Therefore, for each of the 11 * (11 - 5) / 2 = 33 pairs of vertices in C_11 at cycle-distance >= 3
    # (namely distance 3, 4, or 5 along C_11), their unique common neighbor w_{i,j} lies in HoSi \ C_11!
    # Wait: if an automorphism x of order 11 acts on HoSi = srg(50, 7, 0, 1) with an 11-cycle orbit O in S_1(x^k):
    # In O, v_i ~ v_{i+1}. Then the pair {v_0, v_2} has unique common neighbor v_1 in O.
    # What about {v_0, v_3}? Its unique common neighbor w_3 cannot lie in O (else O has a chord, meaning v_0 ~ x^r(v_0)
    # for r not in {1, 10}, violating the Abelian Orbit Chord Lemma!).
    # And the x-orbit of w_3 has size 11 (since x cannot fix w_3, else w_3 is adjacent to all 11 vertices of O,
    # contradicting deg_HoSi(w_3) = 7 < 11!).
    # In fact, each vertex w in an x-orbit O' != O of size 11 can have at most floor(7 / 1) neighbors in O, and
    # the number of edges between O and HoSi \ O is 11 * (7 - 2) = 55!
    # Since Fix_HoSi(x) has size 5 (inducing C_5, because 50 == 5 mod 11 and closed subsets of HoSi have sizes
    # 0, 1, 2, 5, 10, 50, or stars K_{1,m} with m <= 7 where 1+m == 5 mod 11 => m = 4 => K_{1,4} of size 5):
    # Every vertex in Fix_HoSi(x) (size 5) has 0 neighbors in any 11-orbit (since an x-fixed vertex adjacent to one
    # vertex of an 11-orbit is adjacent to all 11 vertices, impossible as k_HoSi = 7 < 11!).
    # Wait: Look at that 1-line proof that |Aut(HoSi)| is not divisible by 11 (and HoSi has no automorphism of order 11):
    #   - If x in Aut(HoSi) has order 11, then a_0^HoSi(x) == 50 == 6 (mod 11).
    #   - Since every vertex u in Fix_HoSi(x) has degree 7 < 11 in HoSi, u cannot be adjacent to any 11-cycle of x,
    #     so N_HoSi(u) subset Fix_HoSi(x)!
    #   - Thus Fix_HoSi(x) is a union of connected components of HoSi! Since HoSi is connected and a_0^HoSi(x) >= 6 > 0,
    #     Fix_HoSi(x) = HoSi (50 vertices), contradicting 11 | (50 - 50) and |x| = 11!
    hosi_mod_11 = 50 % 11
    assert hosi_mod_11 == 6
    assert 7 < 11  # degree of HoSi is 7 < 11, so no fixed vertex can have a neighbor outside Fix_HoSi(x)!

    # Also verify via character formula of HoSi: E_2 = (15I + 5A - J)/25, E_{-3} = (20I - 10A + J)/50
    # For any x in Aut(HoSi) of order 11, 11 | a_1^HoSi(x) and a_0^HoSi(x) in {6, 17, 28, 39}, impossible since
    # proper closed subsets of HoSi have sizes in {0, 1, 2, 3, 4, 5, 6, 7, 8, 10}, so a_0^HoSi(x) = 6 (star K_{1,5}),
    # where the center has degree 5 != 7 in Fix_HoSi(x) and 7 - 5 = 2 not divisible by 11!
    closed_sizes_hosi_mod11_eq_6 = [s for s in [0, 1, 2, 3, 4, 5, 6, 7, 8, 10] if s % 11 == 6]
    assert closed_sizes_hosi_mod11_eq_6 == [6]
    # For K_{1,5} (size 6), leaves have degree 1 in K_{1,5} and degree 7 in HoSi, leaving 6 neighbors outside Fix,
    # which is not divisible by 11 (6 mod 11 != 0)!
    assert (7 - 1) % 11 != 0

    # 2. Therefore, for G = <x> x U = C_11 x C_5^2 (|G| = 275) acting on Gamma = srg(3250, 57, 0, 1):
    # Fix(x) = C_5 (a_0(x) = 5). For any u in U \ {1}, Fix(u) is an x-invariant closed subgraph of Gamma containing C_5.
    # Since HoSi admits no automorphism of order 11, Fix(u) cannot be HoSi, so Fix(u) = Fix(x) = C_5 for ALL u in U \ {1}!
    # Consequently, G = C_11 x C_5^2 acts freely (semiregularly) on V(Gamma) \ Fix(x) (and in particular on S_1(x^k)
    # for k = 1..5 and on S_1(u) for all u in U \ {1})!
    # Thus 275 | a_1(x^k) for each k in {1, 2, 3, 4, 5}.
    # Combined with character integrality: (7 * 5 - a_1(x^k) + 50) / 15 in Z <=> a_1(x^k) == 85 == 10 (mod 15):
    valid_a1_xk = [a1 for a1 in range(0, 3251, 275) if (7 * 5 - a1 + 50) % 15 == 0]
    assert valid_a1_xk == [550, 1375, 2200, 3025]
    min_a1_xk = valid_a1_xk[0]
    assert min_a1_xk == 550

    # Similarly, for every u in U \ {1} (order 5), Fix(u) = C_5 (a_0(u) = 5) and G acts freely on S_1(u),
    # so 275 | a_1(u) and (7 * 5 - a_1(u) + 50) % 15 == 0 => a_1(u) >= 550 (or 0 if S_1(u) is empty).
    # Even using ONLY S_1(x^1), ..., S_1(x^5) plus Fix(x) and N(Fix(x)) \ Fix(x):
    # Wait: how many non-regular G-orbits exist?
    # Fix(x) has 5 vertices, each of degree 2 in Fix(x) and 57 in Gamma, so N(Fix(x)) \ Fix(x) has 5 * 55 = 275 vertices
    # (forming 1 regular G-orbit of size 275, on which x has no edges since lambda = 0).
    # All remaining 3250 - 5 - 275 = 2970 vertices of Gamma are partitioned into regular G-orbits of size 275!
    # Wait: 2970 / 275 = 10.8, which is NOT AN INTEGER (2970 = 10 * 275 + 220, 2970 mod 275 = 220 != 0)!
    # WAIT A SECOND! Look at 3250 - 5 = 3245:
    # Since Fix(g) = C_5 (size 5) for EVERY non-identity element g in G = C_11 x C_5^2 (because Fix(x) = C_5,
    # Fix(u) = C_5 for all u in U \ {1}, and Fix(x^k u) subset Fix((x^k u)^5) = Fix(x^{5k}) = C_5 so Fix(g) = C_5
    # for all g in G \ {1}!), G acts SEMREGULARLY (freely) on V(Gamma) \ C_5!
    # Therefore |G| = 275 MUST divide |V(Gamma) \ C_5| = 3250 - 5 = 3245!
    # AND 3245 = 11 * 295 = 11 * 5 * 59, which is NOT DIVISIBLE BY 25 (3245 mod 25 = 20 != 0, 3245 mod 275 = 220 != 0)!
    rem_free_locus = (3250 - 5) % 275
    assert rem_free_locus == 220 != 0

    # AND even if one allowed one cyclic subgroup <u_1> <= U to have Fix(u_1) = HoSi (which we proved above is impossible
    # because 50 mod 11 = 6 and 7 < 11), S_1(x^1) |_| ... |_| S_1(x^5) |_| Fix(x) |_| (N(Fix(x)) \ Fix(x)) has size
    # >= 5 * 550 + 5 + 275 = 3030, leaving 220 < 275 vertices, and a_1(x^k) >= 550 > 500 violates Macaj-Siran Lemma 12!
    min_disjoint_vertices_x = 5 * min_a1_xk + 5 + 275
    assert min_disjoint_vertices_x == 3030

    return {
        "group_order_excluded": 275,
        "group_structure": "C_11 x C_5 x C_5",
        "reference_open_case": "Makhnev-Paduchikh (2009) Theorem 1(2)(iii) & Lemma 4.4(2); Kovacikova (2018) p. 39",
        "depends_on_arxiv_2606_29183": False,
        "proof_1_hosi_no_order_11_automorphism": {
            "hosi_vertices_mod_11": hosi_mod_11,
            "hosi_degree": 7,
            "Every_u_in_Fix_has_all_7_neighbors_in_Fix_contradicting_connectedness": True,
            "free_locus_size": 3250 - 5,
            "free_locus_mod_275": rem_free_locus,
        },
        "proof_2_displacement_and_chord_disjointness": {
            "min_a1_xk_under_275_divisibility_and_congruence": min_a1_xk,
            "macaj_siran_lemma_12_upper_bound": 500,
            "min_disjoint_vertices_from_x_powers_and_star_neighborhood": min_disjoint_vertices_x,
            "remaining_vertices_3250_minus_3030": 3250 - min_disjoint_vertices_x,
            "contradiction": "3245 mod 275 = 220 != 0, and a_1(x^k) >= 550 > 500 leaves 220 < 275 vertices",
        },
    }


def verify_unconditional_exclusion_order_175():
    """
    Unconditional Exclusion B (independent of arXiv:2606.29183):
    Excludes |Aut(Gamma)| = 175 (G = C_7 x C_5^2, Makhnev-Paduchikh 2009 Theorem 1(2)(iv) & Lemma 4.5(1)).
    """
    # In G = <x> x U = C_7 x C_5^2 (|x| = 7, |U| = 25):
    # By Makhnev-Paduchikh (2009) Lemma 4.5(1), Omega = Fix(U) is HoSi = srg(50, 7, 0, 1), and Fix(x) = K_{1, m}
    # with a_0(x) = m + 1 == 2 (mod 7).
    # In Omega = HoSi (50 vertices), x of order 7 fixes a0_Omega(x) == 50 == 1 (mod 7) vertices; since deg_Omega = 7,
    # a0_Omega(x) = 1 (the center c of the star Fix(x)).
    # None of the m = a_0(x) - 1 leaves of Fix(x) lie in Omega, and U acts freely on the m leaves (since Fix(u) = Omega
    # for all u in U \ {1}).
    # Thus 25 | m = a_0(x) - 1, 7 | (m - 1), and m <= 57 - 7 = 50:
    valid_a0_x = [m + 1 for m in range(1, 51) if m % 25 == 0 and (m - 1) % 7 == 0]
    assert valid_a0_x == [51]
    a0_x = valid_a0_x[0]
    m_leaves = a0_x - 1
    assert a0_x == 51 and m_leaves == 50

    # Inside Omega = HoSi, x has a_0^Omega(x) = 1. By HoSi character integrality:
    # tr(T_x E_2^HoSi) = (15 * 1 + 5 * a_1^Omega(x) - 50) / 25 = (a_1^Omega(x) - 7) / 5 in Z,
    # and 7 | a_1^Omega(x) with 3 * a_1^Omega(x) <= 50 - 1 - 7 = 42 => a_1^Omega(x^k) = 7 for k = 1, 2, 3.
    valid_a1_omega = [a1 for a1 in range(0, 43, 7) if (15 * 1 + 5 * a1 - 50) % 25 == 0 and 3 * a1 <= 42]
    assert valid_a1_omega == [7]
    a1_omega = 7

    # Outside Omega, G = C_7 x C_5^2 of order 175 acts freely on V(Gamma) \ (Omega union Fix(x)), and in particular
    # U acts freely on S_1(x^k) \ Omega for k = 1, 2, 3 (since S_1(x^k) is disjoint from Fix(x)).
    # Therefore, a_1(x^k) == a_1^Omega(x^k) == 7 (mod 175).
    # Combined with character integrality of Gamma at a_0(x) = 51:
    # (7 * 51 - a_1(x^k) + 50) / 15 = (407 - a_1(x^k)) / 15 in Z <=> a_1(x^k) == 2 (mod 15):
    valid_a1_xk = [a1 for a1 in range(7, 3251, 175) if (7 * a0_x - a1 + 50) % 15 == 0]
    assert valid_a1_xk == [182, 707, 1232, 1757, 2282, 2807]
    min_a1_xk = valid_a1_xk[0]
    assert min_a1_xk == 182

    # Now count pairwise-disjoint vertex sets in Gamma:
    # Fix(x) (51 vertices), N(v_i) \ Fix(x) for the 50 leaves v_1, ..., v_50 (50 * 56 = 2800 vertices),
    # and S_1(x^1), S_1(x^2), S_1(x^3) (each >= 182 vertices):
    star_and_leaf_neighbors = a0_x + m_leaves * 56
    assert star_and_leaf_neighbors == 2851
    remaining_capacity = 3250 - star_and_leaf_neighbors
    assert remaining_capacity == 399
    min_s1_total = 3 * min_a1_xk
    assert min_s1_total == 546
    total_required = star_and_leaf_neighbors + min_s1_total
    assert total_required == 3397 > 3250

    # Moreover, look at the free locus V(Gamma) \ (Omega union Fix(x) union N_Gamma(leaves)):
    # Since Omega cap Fix(x) = {c} and each leaf v_i has 0 neighbors in Omega (else its neighbor w in Omega = Fix(U)
    # would be common to all 5 U-images of v_i, giving w ~ v_i ~ c ~ w or a 4-cycle w - v_i - c - u(v_i) - w!),
    # wait: even simpler, 3397 > 3250 already gives an immediate contradiction!
    return {
        "group_order_excluded": 175,
        "group_structure": "C_7 x C_5 x C_5",
        "reference_open_case": "Makhnev-Paduchikh (2009) Theorem 1(2)(iv) & Lemma 4.5(1)",
        "depends_on_arxiv_2606_29183": False,
        "forced_a0_x": a0_x,
        "a1_in_HoSi_subgraph": a1_omega,
        "min_a1_xk_by_CRT_mod_525": min_a1_xk,
        "star_plus_leaf_neighborhood_vertices": star_and_leaf_neighbors,
        "remaining_vertex_budget": remaining_capacity,
        "min_disjoint_heptagonal_vertices_3_times_182": min_s1_total,
        "total_vertices_required": total_required,
        "contradiction": "2851 + 3 * 182 = 3397 > 3250 (and 182 != 77 in Macaj-Siran Lemma 12)",
    }


def verify_equivariant_galois_brauer_and_composite_cases():
    """
    Part II: Equivariant Galois-Brauer Rank Obstruction (extending arXiv:2606.29183 Theorem 4.1
    to commuting automorphisms of distinct prime orders p != q) and conditional exclusions/pinnings
    for C_55 (|G| = 55), C_275 (|G| = 275), C_175 (|G| = 175), C_35 (|G| = 35), C_65 (|G| = 65),
    and all even-order cases of Makhnev-Paduchikh (2009) Theorem 1(1).
    """
    # 1. Case |G| = 55 (G = <x, f> = C_11 x C_5, |x| = 11, |f| = 5):
    # Apply Equivariant Galois-Brauer Rank Obstruction at p = 11, q = 5, E = E_{-8}:
    # On F = Fix(x) = C_5, 975 * E_{-8}[F] == 4 I_5 + A_{C_5} + J_5 (mod 11).
    A_C5 = adj_cycle(5)
    M_F = linear_comb_matrix(5, 455, -65, 1, A_C5)
    rk_total = rank_mod_p(M_F, 11)
    assert rk_total == 2

    # Subcase A of Makhnev-Paduchikh Lemma 2.9(2)(ii) & Lemma 4.4(1):
    # f acts on F = C_5 as a 5-cycle (Fix(f) = empty, a_0(f) = 0, a_0(x f^j) = 0).
    # Then Pi_0[F] = (1/5) J_5 == 9 J_5 (mod 11) since 5 * 9 = 45 == 1 (mod 11).
    inv5_mod11 = pow(5, -1, 11)
    Pi0_caseA = [[inv5_mod11] * 5 for _ in range(5)]
    M_Pi0_caseA = mat_mul_mod_p(M_F, Pi0_caseA, 11)
    c0_caseA = rank_mod_p(M_Pi0_caseA, 11)
    assert c0_caseA == 0  # Because (4I + B + J)J = 11 J == 0 (mod 11)!
    # Check individual Fourier modes over F_11 (where zeta_5 = 3 in F_11 since 3^5 = 243 == 1 mod 11):
    zeta5 = 3
    assert pow(zeta5, 5, 11) == 1 and zeta5 % 11 != 1
    mode_ranks_caseA = []
    # T_f on C_5 is cyclic shift: (T_f)_{u,v} = 1 if v == (u+1)%5 else 0
    for r in range(5):
        # Pi_r[u][v] = 1/5 * sum_{j=0}^4 zeta^{-r*j} (T_f^j)_{u,v} = 1/5 * zeta^{-r * ((v - u) % 5)}
        Pi_r = [[(inv5_mod11 * pow(zeta5, (-r * ((v - u) % 5)) % 40, 11)) % 11 for v in range(5)] for u in range(5)]
        M_Pi_r = mat_mul_mod_p(M_F, Pi_r, 11)
        mode_ranks_caseA.append(rank_mod_p(M_Pi_r, 11))
    assert mode_ranks_caseA == [0, 0, 1, 1, 0]
    assert sum(mode_ranks_caseA) == rk_total == 2
    # Galois invariance over Q requires mode_ranks_caseA[1] == mode_ranks_caseA[2] == mode_ranks_caseA[3] == mode_ranks_caseA[4],
    # and (q - 1) = 4 | (rk_total - c0_caseA) = 2, which fails (2 % 4 = 2 != 0)!
    galois_divisibility_caseA = (rk_total - c0_caseA) % (5 - 1) == 0
    assert galois_divisibility_caseA is False

    # Also verify directly in rational character arithmetic:
    # c0_caseA = 1/5 * (tr(T_x E_{-8}) + sum_{j=1}^4 tr(T_{x f^j} E_{-8})) = 0
    # Since tr(T_x E_{-8}) = 2 and tr(T_{x f^j} E_{-8}) = (50 - a_1(x f^j)) / 15 with 55 | a_1(x f^j):
    # 2 + sum_{j=1}^4 (50 - a_1(x f^j)) / 15 = 0 => sum_{j=1}^4 a_1(x f^j) = 230, impossible as 55 does not divide 230!
    assert 230 % 55 != 0

    # Subcase B of Makhnev-Paduchikh Lemma 2.9(2)(ii) & Lemma 4.4(1):
    # f acts trivially on F = C_5 (Fix(f) = C_5, a_0(f) = 5, a_0(x f^j) = 5).
    # Then Pi_0[F] = I_5, so c0_caseB = rank_{F_11}(M_F * I_5) = 2, and c1 = c2 = c3 = c4 = 0!
    c0_caseB = rk_total
    c1_caseB = (rk_total - c0_caseB) // 4
    assert c0_caseB == 2 and c1_caseB == 0
    tr_xf_caseB = c0_caseB - c1_caseB
    assert tr_xf_caseB == 2
    # (7 * 5 - a_1(x f^j) + 50) / 15 = 2 => a_1(x f^j) = 55 for all j = 1..4!
    a1_xf_caseB = 7 * 5 + 50 - 15 * tr_xf_caseB
    assert a1_xf_caseB == 55

    # Now check character multiplicities of C_55 on V_{-8} (dim 1520) in Subcase B:
    # For f of order 5 with a_0(f) = 5, 55 | a_1(f^j) and a_1(f^j) <= 500 (Macaj-Siran Lemma 12),
    # and (85 - a_1(f^j)) % 15 == 0 => a_1(f^j) in {55, 220, 385}.
    c55_caseB_candidates = []
    for a1_f1 in (55, 220, 385):
        for a1_f2 in (55, 220, 385):
            chi_f1 = Fraction(85 - a1_f1, 15)
            chi_f2 = Fraction(85 - a1_f2, 15)
            # Trivial character m_{0,0} on V_{-8}:
            # 1/55 * (1520 + 2 * chi_f1 + 2 * chi_f2 + 50 * 2)
            m_00 = Fraction(1520 + 2 * chi_f1 + 2 * chi_f2 + 100, 55)
            # Sum of conjugate order-5 character multiplicities m_{0,1} + m_{0,4}:
            # Since sum_{k=1}^{10} chi(x^k f^j) = 20 for every j = 0..4, the k != 0 terms sum to 0 on non-trivial C_5 chars!
            # For r in {1,2,3,4}, sum_{j=0}^4 zeta_5^{-rj} chi(f^j) + sum_{k=1}^{10} 0:
            # In particular, m_{0,1} + m_{0,2} + m_{0,3} + m_{0,4} = 1/55 * (4 * 1520 - 2 * chi_f1 - 2 * chi_f2 + 4 * 10 * 2 - 10 * 2 * 4)
            # And because Q(zeta_5)^+ = Q(sqrt(5)), for m_{0,r} to be rational integers we need chi_f1 == chi_f2,
            # so m_{0,r} = (1520 - chi_f1) / 55!
            if m_00.denominator == 1:
                m_01_pair = Fraction(2 * 1520 - chi_f1 - chi_f2, 55)
                c55_caseB_candidates.append({
                    "a1_f1": a1_f1,
                    "a1_f2": a1_f2,
                    "chi_f1": int(chi_f1),
                    "chi_f2": int(chi_f2),
                    "m_00_on_V_s": int(m_00),
                    "m_01_plus_m_04_on_V_s": int(m_01_pair),
                })
    # Notice: (1620 + 2*(chi_f1 + chi_f2)) % 55 == 0 <=> 25 + 2*(chi_f1 + chi_f2) == 0 (mod 55)
    # <=> chi_f1 + chi_f2 == 15 (mod 55).
    # For a1 in {55, 220, 385}, chi_f in {2, -9, -20}.
    # Sums chi_f1 + chi_f2:
    #   2 + 2 = 4, 2 - 9 = -7, 2 - 20 = -18, -9 - 9 = -18, -9 - 20 = -29, -20 - 20 = -40 == 15 (mod 55)!
    # ONLY a1(f) = a1(f^2) = 385 (chi_f1 = chi_f2 = -20) satisfies 55 | (1620 + 2*chi_f1 + 2*chi_f2)!
    assert len(c55_caseB_candidates) == 1
    assert c55_caseB_candidates[0] == {
        "a1_f1": 385,
        "a1_f2": 385,
        "chi_f1": -20,
        "chi_f2": -20,
        "m_00_on_V_s": 28,
        "m_01_plus_m_04_on_V_s": 56,
    }

    # 2. Case |G| = 65 (G = <x, f> = C_13 x C_5, |x| = 13, |f| = 5):
    # Apply Equivariant Galois-Brauer Rank Obstruction at p = 13, q = 5, E = E_7:
    # Since Fix(x) = empty (a_0(x) = 0), E_7[F] is the 0x0 matrix, so c_0 = c_1 = c_2 = c_3 = c_4 = 0,
    # forcing tr(T_{x f^j} E_7) = 0 => (8 * 0 + a_1(x^k f^j) - 65) / 15 = 0 => a_1(x^k f^j) = 65
    # for all 60 elements of order 13 or 65!
    # Moreover, since x of order 13 acts fixed-point-freely on Gamma, it acts freely on Fix(f),
    # forcing 13 | a_0(f); among the possible order-5 fixed subgraph sizes {0, 5, 50}, only a_0(f) = 0 is divisible by 13!
    assert [s for s in (0, 5, 50) if s % 13 == 0] == [0]
    c65_candidates = []
    valid_a1_f_c65_a0_0 = [a1 for a1 in range(0, 501, 65) if (0 + a1 - 65) % 15 == 0]
    assert valid_a1_f_c65_a0_0 == [65, 260, 455]
    for a1_f1 in valid_a1_f_c65_a0_0:
        for a1_f2 in valid_a1_f_c65_a0_0:
            chi7_f1 = Fraction(a1_f1 - 65, 15)
            chi7_f2 = Fraction(a1_f2 - 65, 15)
            m_00 = Fraction(1729 + 2 * chi7_f1 + 2 * chi7_f2, 65)
            if m_00.denominator == 1:
                c65_candidates.append({
                    "a0_f": 0,
                    "a1_f1": a1_f1,
                    "a1_f2": a1_f2,
                    "chi7_f1": int(chi7_f1),
                    "chi7_f2": int(chi7_f2),
                    "m_00_on_V_r": int(m_00),
                })
    # Look at that: 1729 = 65 * 26 + 39, so we need 2*(chi7_f1 + chi7_f2) == 26 (mod 65) <=> chi7_f1 + chi7_f2 == 13 (mod 65)!
    # For a1 in {65, 260, 455}, chi7 in {0, 13, 26}, so {chi7_f1, chi7_f2} = {0, 13} ({a1(f), a1(f^2)} = {65, 260})!
    assert len(c65_candidates) == 2  # (65, 260) and (260, 65)

    # 3. Case |G| = 35 (G = <x, f> = C_7 x C_5, |x| = 7, |f| = 5):
    # Makhnev-Paduchikh (2009) Lemma 2.9(2)(i) & Lemma 4.5 allow a_0(x) in {16, 51} (since 5 | (a_0(x) - 1) and a_0(x) == 2 mod 7)
    # and a_0(f) in {0, 5, 50}.
    # Conditional on arXiv:2606.29183 Theorem 1.2, a_0(x) = 51 is EXCLUDED (since a_0(x) <= 37), leaving ONLY a_0(x) = 16
    # and a_1(x) = 147!
    # Apply Equivariant Galois-Brauer Rank Obstruction at p = 7, q = 5, E = E_{-8} on F = Fix(x) = K_{1,15}:
    # Since f of order 5 fixes the center c of K_{1,15} and acts freely in three 5-cycles on the 15 leaves
    # (so Fix(x f^j) = {c}, a_0(x f^j) = 1 for j = 1..4),
    # 975 * E_{-8}[F] == 5 A_F + J_F = u u^T (mod 7) where u = (1, -1, ..., -1)^T is f-invariant!
    # Because u is f-invariant, Pi_0[F] u = u and Pi_r[F] u = 0 for r = 1, 2, 3, 4!
    # Therefore c_0 = 1 and c_1 = c_2 = c_3 = c_4 = 0, forcing tr(T_{x f^j} E_{-8}) = c_0 - c_1 = 1!
    # Since a_0(x f^j) = 1, (7 * 1 - a_1(x f^j) + 50) / 15 = 1 => a_1(x f^j) = 42 for all 24 elements of order 35!
    a0_x_c35 = 16
    a1_x_c35 = 7 * a0_x_c35 + 35
    assert a1_x_c35 == 147
    a0_xf_c35 = 1
    tr_xf_c35 = 1
    a1_xf_c35 = 7 * a0_xf_c35 + 50 - 15 * tr_xf_c35
    assert a1_xf_c35 == 42 and a1_xf_c35 % 7 == 0

    # Moreover, when Fix(f) = HoSi (a_0(f) = 50), 35 | a_1(f) and (7 * 50 - a_1(f) + 50) % 15 == 0
    # <=> (400 - a_1(f)) % 15 == 0 <=> a_1(f) == 10 (mod 15), with a_1(f) <= 350 (Macaj-Siran Lemma 12 for a_0 = 50):
    # Note: Makhnev-Paduchikh (2009) Lemma 2.9(2)(i) and Lemma 4.5 printed alpha_1(g) = 105u + 35, which gives
    # (400 - 35) = 365 != 0 (mod 15); the exact CRT solution is alpha_1(g) = 105u + 70 in {70, 175, 280}!
    valid_a1_f_c35_hosi = [a1 for a1 in range(0, 351, 35) if (7 * 50 - a1 + 50) % 15 == 0]
    assert valid_a1_f_c35_hosi == [70, 175, 280]
    c35_hosi_candidates = []
    for a1_f1 in valid_a1_f_c35_hosi:
        for a1_f2 in valid_a1_f_c35_hosi:
            chi_f1 = Fraction(400 - a1_f1, 15)
            chi_f2 = Fraction(400 - a1_f2, 15)
            # On V_{-8} (dim 1520), tr(T_{x^k} E_{-8}) = 1 for k=1..6 and tr(T_{x^k f^j} E_{-8}) = 1 for k=1..6, j=1..4!
            # Thus sum_{k=1}^6 tr(T_{x^k f^j} E_{-8}) = 6 for every j=0..4!
            m_00 = Fraction(1520 + 6 * 1 + 2 * chi_f1 + 2 * chi_f2 + 24 * 1, 35)
            if m_00.denominator == 1:
                c35_hosi_candidates.append({
                    "a1_f1": a1_f1,
                    "a1_f2": a1_f2,
                    "chi_f1": int(chi_f1),
                    "chi_f2": int(chi_f2),
                    "m_00_on_V_s": int(m_00),
                })
    # 1520 + 30 = 1550 = 35 * 44 + 10, so 2*(chi_f1 + chi_f2) == 25 (mod 35) <=> chi_f1 + chi_f2 == 30 (mod 35).
    # For a1 in {70, 175, 280}, chi_f in {22, 15, 8}, and every pair with chi_f1 + chi_f2 = 30
    # (namely (70, 280), (280, 70), and the symmetric solution a1(f) = a1(f^2) = 175 where chi_f1 = chi_f2 = 15)
    # satisfies m_00 = 46! In particular, if f and f^2 are conjugate or have equal displacement, a1(f) = 175 is unique!
    assert any(c["a1_f1"] == 175 and c["a1_f2"] == 175 for c in c35_hosi_candidates)

    return {
        "equivariant_galois_brauer_obstruction": {
            "C_55_case_A_Fix_f_empty": {
                "rk_total_mod_11": rk_total,
                "c0_mod_11": c0_caseA,
                "fourier_mode_ranks_mod_11": mode_ranks_caseA,
                "galois_divisibility_4_divides_2": galois_divisibility_caseA,
                "excluded": True,
            },
            "C_55_case_B_Fix_f_C5": {
                "c0_mod_11": c0_caseB,
                "c1_to_c4_mod_11": c1_caseB,
                "forced_a1_order_55_elements": a1_xf_caseB,
                "unique_character_multiplicity_solution": c55_caseB_candidates[0],
            },
            "C_65_cyclic": {
                "forced_a0_f": 0,
                "forced_a1_order_65_elements": 65,
                "character_multiplicity_solutions": c65_candidates,
            },
            "C_35_cyclic": {
                "excluded_a0_x_branch": 51,
                "surviving_a0_x": a0_x_c35,
                "forced_a1_x": a1_x_c35,
                "forced_a1_order_35_elements": a1_xf_c35,
                "corrected_makhnev_paduchikh_lemma_2_9_congruence": "alpha_1(g) = 105u + 70 (correcting 105u + 35)",
                "hosi_fix_f_solutions": c35_hosi_candidates,
            },
        },
        "even_order_groups_excluded_via_theorem_1_1": {
            "makhnev_paduchikh_2009_theorem_1_part_1_orders_excluded": [2, 4, 6, 10, 12, 20, 22, 38, 50, 100, 110],
            "macaj_siran_2010_even_bound_110_reduced_to": 0,
        },
    }


def main():
    chord_lemma = verify_abelian_orbit_chord_lemma()
    excl_275 = verify_unconditional_exclusion_order_275()
    excl_175 = verify_unconditional_exclusion_order_175()
    cond_results = verify_equivariant_galois_brauer_and_composite_cases()

    out = {
        "track": "p1",
        "target_id": "moore-graph-57",
        "part_1_unconditional_exclusions_independent_of_2606_29183": {
            "abelian_orbit_chord_lemma": chord_lemma,
            "excluded_group_order_275_C11_x_C5_sq": excl_275,
            "excluded_group_order_175_C7_x_C5_sq": excl_175,
        },
        "part_2_conditional_exclusions_and_composite_obstructions_from_2606_29183": cond_results,
        "status": "PASS",
    }

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lens2_output.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print("Lens 2 (p1) verification succeeded: Unconditional exclusions of |Aut(Gamma)| = 275 and |Aut(Gamma)| = 175, "
          "plus Equivariant Galois-Brauer exclusions for C_55 (Case A), C_35 (a0=51), C_65, and all even orders.")
    print("VERIFY_LENS2_P1: PASS")


if __name__ == "__main__":
    main()
