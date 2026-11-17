#!/usr/bin/env python3
"""
Standalone Clean-Room Referee Verifier for Fraenkel's 3-Heap Wythoff Conjectures at A_1 = 11
(and Sun & Zeilberger Table 1 recomputation for A_1 = 0..10).

Python 3 standard library only. Shares zero code with fraenkel_wythoff.c.
Recomputes P-positions directly from Fraenkel's normal-play game rules, cross-checks against
brute-force 3D game-tree evaluation, verifies Table 1 (m = 0..10), and checks all hypotheses of
Claims 3.3, 3.4, 3.5, and Lemma 2.4 of Sun & Zeilberger (Ann. Comb. 8 (2004), 225-238) for m = 0..11.
"""

import json
import math
import os
import sys


# Published Table 1 from Sun & Zeilberger, Ann. Comb. 8 (2004), p. 237 (page 13 of preprint)
PUBLISHED_TABLE_1 = {
    0: {"T": [], "S": [], "alpha": 0, "N1": 1, "N2": 1},
    1: {"T": [1], "S": [2, 17, 22], "alpha": -4, "N1": 21, "N2": 28},
    2: {"T": [], "S": [1, 5, 8, 24, 26, 32], "alpha": -10, "N1": 28, "N2": 58},
    3: {"T": [1, 2, 3], "S": [2, 3, 4, 5, 8, 10, 11, 12, 28, 41, 57], "alpha": -16, "N1": 48, "N2": 73},
    4: {"T": [3, 6], "S": [2, 5, 6, 7, 8, 9, 11, 12, 14, 17, 46, 48, 59], "alpha": -20, "N1": 126, "N2": 208},
    5: {"T": [4, 7, 10], "S": [1, 3, 5, 6, 8, 10, 11, 12, 15, 16, 17, 18, 19, 28, 56, 77, 83], "alpha": -26, "N1": 71, "N2": 123},
    6: {"T": [2, 3, 4, 6], "S": [1, 2, 3, 4, 5, 7, 8, 10, 11, 12, 13, 14, 15, 16, 18, 21, 44, 58, 95, 96, 132], "alpha": -32, "N1": 113, "N2": 232},
    7: {"T": [1, 4, 6, 7, 9], "S": [0, 1, 2, 4, 5, 6, 7, 8, 10, 12, 13, 14, 15, 17, 18, 19, 21, 22, 23, 24, 28, 30, 86, 88, 232, 251], "alpha": -39, "N1": 227, "N2": 343},
    8: {"T": [3, 5, 10, 13], "S": [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 13, 14, 16, 17, 19, 20, 21, 22, 24, 26, 27, 28, 33, 34, 46, 155, 257, 390, 415], "alpha": -46, "N1": 388, "N2": 648},
    9: {"T": [4, 6, 11, 15], "S": [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 20, 24, 25, 26, 27, 30, 36, 37, 44, 48, 62, 254, 388, 421, 676], "alpha": -52, "N1": 645, "N2": 645},
    10: {"T": [6, 7, 8, 9, 13], "S": [0, 1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 25, 27, 28, 29, 30, 31, 32, 34, 39, 50, 53, 103, 391, 424, 690], "alpha": -56, "N1": 656, "N2": 656},
}


def fail(msg):
    print(f"VERIFICATION ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def floor_golden(k):
    """Exact floor(k * (1 + sqrt(5)) / 2) for integer k >= 0."""
    if k < 0:
        fail(f"Negative argument to floor_golden: {k}")
    if k == 0:
        return 0
    return (k + math.isqrt(5 * k * k)) // 2


def xor_period(m):
    """p(m) = 2^(floor(log2(m)) + 1) for m >= 1, and 1 for m == 0."""
    if m == 0:
        return 1
    return 1 << m.bit_length()


def brute_force_3heap(max_m, max_p3):
    """Literal definition of Fraenkel's 3-heap Wythoff game on 0 <= p1 <= p2 <= p3 <= max_p3."""
    p_set = set()
    for p1 in range(max_m + 1):
        for p2 in range(p1, max_p3 + 1):
            for p3 in range(p2, max_p3 + 1):
                if (p1, p2, p3) == (0, 0, 0):
                    p_set.add((0, 0, 0))
                    continue
                losing = True
                # 1. Single-heap moves
                for q in range(p1):
                    if (q, p2, p3) in p_set:
                        losing = False
                        break
                if losing:
                    for q in range(p2):
                        t = tuple(sorted((p1, q, p3)))
                        if t in p_set:
                            losing = False
                            break
                if losing:
                    for q in range(p3):
                        t = tuple(sorted((p1, p2, q)))
                        if t in p_set:
                            losing = False
                            break
                # 2. Multi-heap Nim-sum-zero moves: a1 ^ a2 ^ a3 == 0 and a1 + a2 + a3 > 0
                if losing:
                    for a1 in range(p1 + 1):
                        for a2 in range(p2 + 1):
                            a3 = a1 ^ a2
                            if (a1 + a2 + a3 > 0) and a3 <= p3:
                                t = tuple(sorted((p1 - a1, p2 - a2, p3 - a3)))
                                if t in p_set:
                                    losing = False
                                    break
                        if not losing:
                            break
                if losing:
                    p_set.add((p1, p2, p3))
    return p_set


def recompute_p_positions(max_m, max_second_heap):
    """
    Recompute all P-positions (p1, p2, p3) with 0 <= p1 <= max_m and p1 <= p2 <= max_second_heap
    directly from Fraenkel's game rules.
    Returns dict P_seq[m] = 1-indexed list (index 0 unused) of tuples (A, B) where
    heaps are (m, m + A, m + A + B).
    """
    p_seq = {}
    p_heaps_by_p2 = {}  # m -> dict mapping p2 -> p3

    for m in range(max_m + 1):
        pm = xor_period(m)
        mask = pm - 1

        full_col_blocked = set()
        full_row_blocked = set()
        small_targets = []
        residue_groups = [[set() for _ in range(pm)] for _ in range(m)]

        # Pre-scan P^a for 0 <= a < m for moves with p2 == m, p3 == m, or small coordinates
        for a in range(m):
            for idx in range(1, len(p_seq[a])):
                A0, B0 = p_seq[a][idx]
                q1, q2, q3 = a, a + A0, a + A0 + B0
                if q2 == m:
                    # Single-pile (q3 -> a from X=q3) blocks whole column b = B0
                    full_col_blocked.add(B0)
                    # Nim-sum (0, k, k) to (a, m, m+B0) blocks whole row c = A0 + B0
                    full_row_blocked.add(A0 + B0)
                if q3 == m:
                    # Nim-sum (0, k, k) to (a, a+A0, m) blocks whole row c = A0
                    full_row_blocked.add(A0)
                if q2 < m or q3 < m or B0 <= m:
                    small_targets.append((q1, q2, q3))

        ingest_ptr = [1] * m
        seq_m = [None]  # 1-indexed
        map_m = {}
        seen_B_m = set()
        seen_diag_m = set()

        for X in range(m, max_second_heap + 1):
            b = X - m
            for a in range(m):
                while ingest_ptr[a] < len(p_seq[a]):
                    A0, B0 = p_seq[a][ingest_ptr[a]]
                    q2 = a + A0
                    if q2 > X:
                        break
                    residue_groups[a][q2 & mask].add(B0)
                    ingest_ptr[a] += 1

            if b in full_col_blocked or b in seen_diag_m:
                continue

            forbidden_c = set(full_row_blocked) | set(seen_B_m)

            # Moves within P^m along south-east diagonal: (m, m+b_i+k, m+b_i+c_i) -> (m, m+b_i, m+b_i+c_i)
            for s in seen_diag_m:
                if s >= b:
                    forbidden_c.add(s - b)

            # Single-pile move reducing m -> a: requires (a, X, Y) in P^a
            for a in range(m):
                if X in p_heaps_by_p2[a]:
                    forbidden_c.add(p_heaps_by_p2[a][X] - X)

            # Single-pile move reducing X -> a when (a, m, m+c0) in P^a and m+c0 >= X
            for c0 in full_col_blocked:
                if c0 >= b:
                    forbidden_c.add(c0 - b)

            # 3-pile Nim-sum-0 moves to (a, q2, q3) with q2 <= X (ordered assignment)
            for a in range(m):
                d = m - a
                for r in range(pm):
                    shift = (d ^ r) - r
                    grp = residue_groups[a][(X - r) & mask]
                    for B0 in grp:
                        c_val = B0 + shift
                        if c_val >= 0:
                            forbidden_c.add(c_val)

            # Permuted assignments (only reachable when q2 < m, q3 < m, or B0 <= m)
            for (q1, q2, q3) in small_targets:
                for u1, u2, u3 in (
                    (q1, q2, q3), (q1, q3, q2),
                    (q2, q1, q3), (q2, q3, q1),
                    (q3, q1, q2), (q3, q2, q1),
                ):
                    if u1 < m and u2 <= X:
                        r1 = m - u1
                        r2 = X - u2
                        r3 = r1 ^ r2
                        Y = u3 + r3
                        if Y >= X:
                            forbidden_c.add(Y - X)

            c = 0
            while c in forbidden_c:
                c += 1

            seq_m.append((b, c))
            map_m[X] = X + c
            seen_B_m.add(c)
            seen_diag_m.add(b + c)

        p_seq[m] = seq_m
        p_heaps_by_p2[m] = map_m

    return p_seq, p_heaps_by_p2


def is_valid_p_pos(w, p_heaps_by_p2):
    """Verify [a, A0, B0] is a genuine recomputed P-position."""
    if not isinstance(w, list) or len(w) != 3:
        return False
    a, A0, B0 = w
    if a < 0 or A0 < 0 or B0 < 0 or a not in p_heaps_by_p2:
        return False
    q2 = a + A0
    q3 = q2 + B0
    return p_heaps_by_p2[a].get(q2) == q3


def verify_three_pile_nim_move(m, x, c, w):
    """
    Verify that [m, x, c] = heaps (m, m+x, m+x+c) has a legal 3-pile Nim-sum-0 move
    (r1, r2, r3) with 1 <= r1 <= m, 0 <= r2 <= m+x, 0 <= r3 <= m+x+c, r1 ^ r2 ^ r3 == 0
    leaving multiset {a, a+A0, a+A0+B0} where w = [a, A0, B0] with 0 <= a < m.
    """
    a, A0, B0 = w
    if not (0 <= a < m):
        return False
    p1, p2, p3 = a, a + A0, a + A0 + B0
    X = m + x
    Y = X + c
    for u1, u2, u3 in (
        (p1, p2, p3), (p1, p3, p2),
        (p2, p1, p3), (p2, p3, p1),
        (p3, p1, p2), (p3, p2, p1),
    ):
        if u1 < m and u2 <= X and u3 <= Y:
            r1 = m - u1
            r2 = X - u2
            r3 = Y - u3
            if 1 <= r1 <= m and (r1 ^ r2 ^ r3) == 0:
                return True
    return False


def main():
    default_cert = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "object",
        "wythoff_a1_11_certificate.json",
    )
    cert_path = sys.argv[1] if len(sys.argv) > 1 else default_cert
    if not os.path.isfile(cert_path):
        fail(f"Certificate file not found: {cert_path}")

    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            cert = json.load(f)
    except Exception as exc:
        fail(f"Invalid JSON in certificate: {exc}")

    if cert.get("target_A1") != 11:
        fail(f"Unexpected target_A1: {cert.get('target_A1')}")

    levels = cert.get("levels")
    if not isinstance(levels, list) or len(levels) != 12:
        fail("Certificate must contain exactly 12 level entries (m = 0..11)")

    # Determine required second-heap horizon from claimed n1 values
    max_n1 = max(int(lv.get("n1", 0)) for lv in levels)
    max_second_heap = int(max_n1 * 1.7) + 200
    if max_second_heap < 6000:
        max_second_heap = 6000

    print(f"[1/4] Cross-checking literal 3D brute-force move rules on 0 <= p1 <= 11, p3 <= 55...")
    brute_p = brute_force_3heap(11, 55)
    p_seq, p_heaps_by_p2 = recompute_p_positions(11, max_second_heap)

    for p1 in range(12):
        for p2 in range(p1, 56):
            for p3 in range(p2, 56):
                in_recomp = (p_heaps_by_p2[p1].get(p2) == p3)
                in_brute = ((p1, p2, p3) in brute_p)
                if in_recomp != in_brute:
                    fail(f"Brute-force mismatch at ({p1}, {p2}, {p3}): recomp={in_recomp}, brute={in_brute}")
    print(f"      Brute-force check OK ({len(brute_p)} P-positions verified directly).")

    print(f"[2/4] Verifying base case m = 0 and inductive Sun-Zeilberger proofs for m = 1..11...")
    verified_levels = {}

    for expected_m, lv in enumerate(levels):
        if lv.get("m") != expected_m:
            fail(f"Level index mismatch: expected m={expected_m}, got {lv.get('m')}")
        m = expected_m
        pm = xor_period(m)
        if lv.get("p_m") != pm:
            fail(f"m={m}: p_m mismatch ({lv.get('p_m')} != {pm})")

        seq = p_seq[m]

        # Recompute T^m from definition (Claim 3.1): { b : exists a < m with [a, m-a, b] in P^a }
        recomp_T = sorted(
            p_heaps_by_p2[a][m] - m
            for a in range(m)
            if m in p_heaps_by_p2[a]
        )
        if lv.get("T") != recomp_T:
            fail(f"m={m}: T^m mismatch: claimed {lv.get('T')} vs recomputed {recomp_T}")

        if m == 0:
            # Classical 2-heap Wythoff game: A^0_n = floor((n-1)*phi), B^0_n = n-1 for n >= 1
            if lv.get("S") != [] or lv.get("alpha") != 0 or lv.get("N1") != 1 or lv.get("N2") != 1 or lv.get("N3") != 1:
                fail(f"m=0 base constants invalid: {lv}")
            if lv.get("B_N3") != seq[1][1] or lv.get("B_N3_plus_1") != seq[2][1]:
                fail("m=0 B_N3 mismatch")
            for k in range(1, 50):
                if seq[k] != (floor_golden(k - 1), k - 1):
                    fail(f"m=0 Wythoff pair mismatch at k={k}")
            verified_levels[0] = lv
            continue

        n1 = int(lv["n1"])
        n2 = int(lv["n2"])
        N_c34 = int(lv["N_claim34"])
        j_chop = int(lv["j_chop"])
        m1_lem = int(lv["m1_lemma24"])

        if n1 + 2 >= len(seq):
            fail(f"m={m}: recomputed table too short ({len(seq) - 1}) for n1={n1}")
        if not (0 <= N_c34 < n2 <= j_chop < m1_lem < n1):
            fail(f"m={m}: invalid index ordering N={N_c34}, n2={n2}, j_chop={j_chop}, m1={m1_lem}, n1={n1}")

        # Verify spot-check position fields in certificate
        if lv.get("P_n2_plus_3") != [m, seq[n2 + 3][0], seq[n2 + 3][1]]:
            fail(f"m={m}: P_n2_plus_3 mismatch")
        if lv.get("P_m1_lemma24") != [m, seq[m1_lem][0], seq[m1_lem][1]]:
            fail(f"m={m}: P_m1_lemma24 mismatch")
        if lv.get("P_n1") != [m, seq[n1][0], seq[n1][1]]:
            fail(f"m={m}: P_n1 mismatch")

        # Verify Claim 3.3 certificates for S_1^m(n1) (and record certification threshold per c)
        claimed_S = lv.get("S")
        s1_certs = lv.get("S1_n1_certificates")
        if not isinstance(claimed_S, list) or not isinstance(s1_certs, list) or len(claimed_S) != len(s1_certs):
            fail(f"m={m}: S and S1_n1_certificates length mismatch")
        if claimed_S != sorted(set(claimed_S)):
            fail(f"m={m}: claimed S is not strictly sorted")

        B_up_to_n1 = {seq[i][1] for i in range(1, n1 + 1)}
        cert_threshold_for_c = {}

        for c_val, sc in zip(claimed_S, s1_certs):
            if sc.get("c") != c_val:
                fail(f"m={m}: S1 certificate c mismatch ({sc.get('c')} != {c_val})")
            if c_val in B_up_to_n1:
                fail(f"m={m}: c={c_val} claimed in S^m actually appears in B^m_1..B^m_n1")
            rule = sc.get("rule")
            if rule == 1:
                w = sc.get("witness_P")
                if not is_valid_p_pos(w, p_heaps_by_p2):
                    fail(f"m={m}, c={c_val}: invalid Rule 1 witness P-position {w}")
                a, b0, c0 = w
                if not (0 <= a < m and a + b0 == m and b0 + c0 == c_val):
                    fail(f"m={m}, c={c_val}: Rule 1 equation failed for {w}")
                cert_threshold_for_c[c_val] = 0
            elif rule == 2:
                w = sc.get("witness_P")
                if not is_valid_p_pos(w, p_heaps_by_p2):
                    fail(f"m={m}, c={c_val}: invalid Rule 2 witness P-position {w}")
                a, b0, c0 = w
                if not (0 <= a < m and a + b0 + c0 == m and b0 == c_val):
                    fail(f"m={m}, c={c_val}: Rule 2 equation failed for {w}")
                cert_threshold_for_c[c_val] = 0
            elif rule == 3:
                rn = int(sc.get("n", -1))
                if not (1 <= rn <= n1):
                    fail(f"m={m}, c={c_val}: Rule 3 n={rn} out of range 1..{n1}")
                An, Bn = seq[rn]
                if sc.get("A_n") != An or sc.get("B_n") != Bn:
                    fail(f"m={m}, c={c_val}: Rule 3 (A_n, B_n) mismatch at n={rn}")
                if Bn <= c_val:
                    fail(f"m={m}, c={c_val}: Rule 3 requires B_n > c, got B_{rn}={Bn}")
                win_list = sc.get("window_witness_P")
                if not isinstance(win_list, list) or len(win_list) != pm + 1:
                    fail(f"m={m}, c={c_val}: Rule 3 requires {pm + 1} window witnesses")
                for k in range(pm + 1):
                    w = win_list[k]
                    if not is_valid_p_pos(w, p_heaps_by_p2):
                        fail(f"m={m}, c={c_val}, k={k}: invalid window witness {w}")
                    if not verify_three_pile_nim_move(m, An + k, c_val, w):
                        fail(f"m={m}, c={c_val}, k={k}: [m, {An + k}, {c_val}] cannot reach {w} via 3-pile Nim move")
                cert_threshold_for_c[c_val] = rn
            else:
                fail(f"m={m}, c={c_val}: unknown Claim 3.3 rule {rule}")

        # Verify Claim 3.4 threshold N_c34 non-circularly
        max_T_le_m = max(
            [0] + [t for i in range(m + 1) for t in (verified_levels[i]["T"] if i < m else recomp_T)]
        )
        if seq[N_c34 + 1][0] <= max_T_le_m:
            fail(f"m={m}: Claim 3.4 A_{{N+1}} <= max_{{i<=m}} T^i at N={N_c34}")
        B_up_to_N34 = {seq[i][1] for i in range(1, N_c34 + 1)}
        for c_small in range(m + max_T_le_m + 1):
            if c_small not in B_up_to_N34:
                if c_small not in cert_threshold_for_c or cert_threshold_for_c[c_small] > N_c34:
                    fail(f"m={m}: Claim 3.4 c={c_small} not yet excluded by N={N_c34}")

        # Verify ALL 8 conditions of Claim 3.5 + strengthened Lemma 2.4 chopping condition
        # Condition 1 (and Lemma 2.4 chopping):
        if not (seq[n2 + 3][0] + seq[n2 + 3][1] < seq[n1][0]):
            fail(f"m={m}: Claim 3.5 Condition 1 failed")
        max_tilde_T = max(recomp_T + [seq[i][0] + seq[i][1] for i in range(1, n2)] + [0])
        if not (seq[j_chop + 1][0] > max_tilde_T and m1_lem > j_chop + 2):
            fail(f"m={m}: Lemma 2.4 chopping bound failed at j_chop={j_chop}")
        if not (seq[m1_lem][0] + seq[m1_lem][1] < seq[n1][0]):
            fail(f"m={m}: Strengthened Lemma 2.4 A_m1 + B_m1 < A_n1 failed")

        # Condition 2: B_{j+1} = B_j + 1 for n2 <= j <= n1
        for j in range(n2, n1 + 1):
            if seq[j + 1][1] != seq[j][1] + 1:
                fail(f"m={m}: Claim 3.5 Condition 2 failed at j={j}")

        # Condition 3: B_{n1} = max({B_i : 1 <= i <= n1})
        if seq[n1][1] != max(B_up_to_n1):
            fail(f"m={m}: Claim 3.5 Condition 3 failed")

        # Condition 4: mex({B_i : 1 <= i <= n1} union S_1^m(n1)) = B_{n1} + 1
        union_set = B_up_to_n1 | set(claimed_S)
        mex_v = 0
        while mex_v in union_set:
            mex_v += 1
        if mex_v != seq[n1][1] + 1:
            fail(f"m={m}: Claim 3.5 Condition 4 mex={mex_v} != B_n1+1={seq[n1][1] + 1}")

        # Condition 5: max(alpha_j) - min(alpha_j) <= 2 on n2 <= j <= n1, and alpha' == claimed alpha
        alphas_win = [m + seq[j][0] - floor_golden(seq[j][1]) for j in range(n2, n1 + 1)]
        hi_al, lo_al = max(alphas_win), min(alphas_win)
        if hi_al - lo_al > 2:
            fail(f"m={m}: Claim 3.5 Condition 5 failed (spread {hi_al - lo_al} > 2)")
        alpha_prime = (hi_al + lo_al) // 2
        if lv.get("alpha") != alpha_prime:
            fail(f"m={m}: alpha mismatch: claimed {lv.get('alpha')} != alpha'={alpha_prime}")

        # Condition 6: B^m_{n1} > B^i_{N3^i} (and > B^i_{N3^i + 1}) for all 0 <= i < m
        for i in range(m):
            if seq[n1][1] <= verified_levels[i]["B_N3"] or seq[n1][1] <= verified_levels[i]["B_N3_plus_1"]:
                fail(f"m={m}: Claim 3.5 Condition 6 failed against i={i}")

        # Condition 7: alpha^i - alpha' >= 4*(m - i) for all 0 <= i < m
        for i in range(m):
            if verified_levels[i]["alpha"] - alpha_prime < 4 * (m - i):
                fail(f"m={m}: Claim 3.5 Condition 7 failed against i={i}")

        # Condition 8: |eps_j| <= 1 on n2-2 <= j <= n1 and eps_{j-2}*eps_{j-1}*eps_j == 0 on n2 <= j <= n1
        def eps_at(idx):
            return (m + seq[idx][0] - floor_golden(seq[idx][1])) - alpha_prime

        for j in range(max(1, n2 - 2), n1 + 1):
            if eps_at(j) not in (-1, 0, 1):
                fail(f"m={m}: |eps_{j}| > 1 in Claim 3.5 window")
        for j in range(n2, n1 + 1):
            if eps_at(j - 2) * eps_at(j - 1) * eps_at(j) != 0:
                fail(f"m={m}: Claim 3.5 Condition 8 failed at j={j}")

        # Verify exactness & minimality of N1^m, N2^m, N3^m, B_N3^m
        max_Tm = max(recomp_T) if recomp_T else -1
        recomp_N1 = 1
        for j in range(1, n1 + 1):
            if seq[j + 1][1] != seq[j][1] + 1 or seq[j][0] <= max_Tm:
                recomp_N1 = j + 1
        recomp_N2 = recomp_N1
        for j in range(recomp_N1, n1 + 1):
            if eps_at(j) not in (-1, 0, 1):
                recomp_N2 = j + 1
        recomp_N3 = recomp_N2
        for j in range(recomp_N2, n1 + 1):
            if eps_at(j) * eps_at(j + 1) != 0:
                recomp_N3 = j + 1

        if lv.get("N1") != recomp_N1:
            fail(f"m={m}: N1 mismatch: claimed {lv.get('N1')} != {recomp_N1}")
        if lv.get("N2") != recomp_N2:
            fail(f"m={m}: N2 mismatch: claimed {lv.get('N2')} != {recomp_N2}")
        if lv.get("N3") != recomp_N3:
            fail(f"m={m}: N3 mismatch: claimed {lv.get('N3')} != {recomp_N3}")
        if lv.get("B_N3") != seq[recomp_N3][1]:
            fail(f"m={m}: B_N3 mismatch: claimed {lv.get('B_N3')} != {seq[recomp_N3][1]}")
        if lv.get("B_N3_plus_1") != seq[recomp_N3 + 1][1]:
            fail(f"m={m}: B_N3_plus_1 mismatch: claimed {lv.get('B_N3_plus_1')} != {seq[recomp_N3 + 1][1]}")

        verified_levels[m] = lv
        print(f"      m={m:2d} OK: alpha={alpha_prime:3d}, N1={recomp_N1:4d}, N2={recomp_N2:4d}, "
              f"N3={recomp_N3:4d} (B_N3={seq[recomp_N3][1]:4d}), n2={n2:4d}, n1={n1:4d}")

    print("[3/4] Auditing Sun & Zeilberger Table 1 (m = 0..10)...")
    for m in range(11):
        lv = verified_levels[m]
        pub = PUBLISHED_TABLE_1[m]
        if (lv["T"] != pub["T"] or lv["S"] != pub["S"] or lv["alpha"] != pub["alpha"]
                or lv["N1"] != pub["N1"] or lv["N2"] != pub["N2"]):
            fail(f"Table 1 mismatch at m={m}: got {lv}, published {pub}")
    print("      All 11 rows (m = 0..10) of Sun & Zeilberger Table 1 match identically (partial win p1 confirmed).")

    lv11 = verified_levels[11]
    print("[4/4] Final summary for open case A_1 = 11:")
    print(f"      T^11 = {lv11['T']}")
    print(f"      |S^11| = {len(lv11['S'])}, max(S^11) = {max(lv11['S'])}")
    print(f"      alpha^11 = {lv11['alpha']}, N1^11 = {lv11['N1']}, N2^11 = {lv11['N2']}, "
          f"N3^11 = {lv11['N3']}, B^11_{{N3^11}} = {lv11['B_N3']}")
    print(f"      Claim 3.4/3.5 witnesses: N = {lv11['N_claim34']}, n2 = {lv11['n2']}, n1 = {lv11['n1']}")
    print("PASS")


if __name__ == "__main__":
    main()
