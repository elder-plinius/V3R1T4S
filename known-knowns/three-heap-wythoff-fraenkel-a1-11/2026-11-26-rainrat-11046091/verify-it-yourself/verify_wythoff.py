#!/usr/bin/env python3
"""Standalone pure-Python verifier for Fraenkel's 3-heap Wythoff conjectures at A_1 = 12.

Python 3.8+ standard library only. Shares zero code with reverse.cpp or direct.cpp.
Recomputes all P-positions (m, Y, Z) directly from Fraenkel's game rules (cross-checked
against literal 3D brute force on 0 <= p1 <= 12, p3 <= 55), verifies Sun & Zeilberger
Table 1 (m = 0..10), checks every hypothesis of Claims 3.3, 3.4, and 3.5 (using the
standard half-sum midpoint matching Table 1) as well as the self-contained direct
Lemma 2.6 induction proof for all layers m = 0..12, and validates every field of the
certificate JSON.
"""
from collections import defaultdict
import json
import math
import os
import sys


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


def floor_phi(k):
    if k < 0:
        fail(f"Negative argument to floor_phi: {k}")
    if k == 0:
        return 0
    return (k + math.isqrt(5 * k * k)) // 2


def xor_period(m):
    return 1 if m == 0 else (1 << m.bit_length())


def brute_force_3heap(max_m, max_p3):
    """Literal 3D game-tree evaluation on 0 <= p1 <= max_m, p1 <= p2 <= p3 <= max_p3."""
    p_set = set()
    for p1 in range(max_m + 1):
        for p2 in range(p1, max_p3 + 1):
            for p3 in range(p2, max_p3 + 1):
                if (p1, p2, p3) == (0, 0, 0):
                    p_set.add((0, 0, 0))
                    continue
                losing = True
                for q in range(p1):
                    if (q, p2, p3) in p_set:
                        losing = False
                        break
                if losing:
                    for q in range(p2):
                        if tuple(sorted((p1, q, p3))) in p_set:
                            losing = False
                            break
                if losing:
                    for q in range(p3):
                        if tuple(sorted((p1, p2, q))) in p_set:
                            losing = False
                            break
                if losing:
                    for a1 in range(p1 + 1):
                        for a2 in range(p2 + 1):
                            a3 = a1 ^ a2
                            if a1 + a2 + a3 > 0 and a3 <= p3:
                                if tuple(sorted((p1 - a1, p2 - a2, p3 - a3))) in p_set:
                                    losing = False
                                    break
                        if not losing:
                            break
                if losing:
                    p_set.add((p1, p2, p3))
    return p_set


def recompute_p_positions(max_m, max_second_heap):
    """Exact retrograde/mex recomputation of all P-positions (m, Y, Z) up to max_second_heap.

    Because any legal move from (m, Y, Z) leaves at least two coordinates <= Y, sorting
    any destination never produces a middle coordinate > Y. Computing complete layers
    in ascending m order up to max_second_heap is therefore exact with no truncation error.
    """
    p_seq = {}
    p_by_y = {}

    for m in range(max_m + 1):
        pm = xor_period(m)
        mask = pm - 1
        residue_groups = [defaultdict(set) for _ in range(m)]
        full_col_blocked = set()
        full_row_blocked = set()
        small_targets = []

        for a in range(m):
            for A0, B0 in p_seq[a][1:]:
                q1, q2, q3 = a, a + A0, a + A0 + B0
                if q2 == m:
                    full_col_blocked.add(B0)
                    full_row_blocked.add(A0 + B0)
                if q3 == m:
                    full_row_blocked.add(A0)
                if q2 < m or q3 < m or B0 <= m:
                    small_targets.append((q1, q2, q3))

        ingest_ptr = [1] * m
        seq_m = [None]
        map_m = {}
        seen_B = set()
        seen_diag = set()

        for Y in range(m, max_second_heap + 1):
            b = Y - m
            for a in range(m):
                while ingest_ptr[a] < len(p_seq[a]):
                    A0, B0 = p_seq[a][ingest_ptr[a]]
                    q2 = a + A0
                    if q2 > Y:
                        break
                    residue_groups[a][q2 & mask].add(B0)
                    ingest_ptr[a] += 1

            if b in full_col_blocked or b in seen_diag:
                continue

            forbidden_c = set(full_row_blocked) | seen_B
            for s in seen_diag:
                if s >= b:
                    forbidden_c.add(s - b)
            for a in range(m):
                if Y in p_by_y[a]:
                    forbidden_c.add(p_by_y[a][Y] - Y)
            for c0 in full_col_blocked:
                if c0 >= b:
                    forbidden_c.add(c0 - b)

            for a in range(m):
                d = m - a
                for r in range(pm):
                    shift = (d ^ r) - r
                    for B0 in residue_groups[a][(Y - r) & mask]:
                        c_val = B0 + shift
                        if c_val >= 0:
                            forbidden_c.add(c_val)

            for q1, q2, q3 in small_targets:
                for u1, u2, u3 in (
                    (q1, q2, q3), (q1, q3, q2),
                    (q2, q1, q3), (q2, q3, q1),
                    (q3, q1, q2), (q3, q2, q1),
                ):
                    if u1 < m and u2 <= Y:
                        r1 = m - u1
                        r2 = Y - u2
                        r3 = r1 ^ r2
                        Z = u3 + r3
                        if Z >= Y:
                            forbidden_c.add(Z - Y)

            c = 0
            while c in forbidden_c:
                c += 1

            seq_m.append((b, c))
            map_m[Y] = Y + c
            seen_B.add(c)
            seen_diag.add(b + c)

        p_seq[m] = seq_m
        p_by_y[m] = map_m

    return p_seq, p_by_y


def verify_ray_move(m, Y, c, w, p_by_y, pm):
    """Verify w = [a, A0, B0] is a valid lower P-position with a legal XOR move from (m, Y, Y+c)."""
    if not isinstance(w, list) or len(w) != 3 or not all(isinstance(x, int) for x in w):
        return False
    a, A0, B0 = w
    if not (0 <= a < m and A0 >= 0 and B0 >= 0):
        return False
    q2 = a + A0
    q3 = q2 + B0
    if p_by_y[a].get(q2) != q3:
        return False
    Z = Y + c
    for u1, u2, u3 in (
        (a, q2, q3), (a, q3, q2),
        (q2, a, q3), (q2, q3, a),
        (q3, a, q2), (q3, q2, a),
    ):
        if u1 <= m and u2 <= Y and u3 <= Z:
            d, e, f = m - u1, Y - u2, Z - u3
            if 0 <= d < pm and (d ^ e ^ f) == 0 and (d + e + f) > 0:
                return True
    return False


def main():
    default_cert = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "object",
        "wythoff_a1_12_certificate.json",
    )
    if not os.path.isfile(default_cert):
        default_cert = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "wythoff_a1_12_certificate.json",
        )
    cert_path = sys.argv[1] if len(sys.argv) > 1 else default_cert
    if not os.path.isfile(cert_path):
        fail(f"Certificate not found: {cert_path}")

    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            cert = json.load(f)
    except Exception as exc:
        fail(f"Invalid JSON: {exc}")

    if cert.get("target_id") != "three-heap-wythoff-fraenkel-a1-11":
        fail("Unexpected target_id")
    if cert.get("target_A1") != 12:
        fail("Unexpected target_A1")
    levels = cert.get("levels")
    if not isinstance(levels, list) or len(levels) != 13:
        fail("Certificate must contain exactly 13 levels (m = 0..12)")

    max_Y_needed = max(int(lv.get("next_middle", 0)) for lv in levels)
    max_second_heap = max(5500, max_Y_needed + 150)

    print("[1/5] Cross-checking literal 3D brute-force (0 <= p1 <= 12, p3 <= 55) and recomputing through Y <= %d..." % max_second_heap)
    brute_p = brute_force_3heap(12, 55)
    p_seq, p_by_y = recompute_p_positions(12, max_second_heap)
    for p1 in range(13):
        for p2 in range(p1, 56):
            for p3 in range(p2, 56):
                if (p_by_y[p1].get(p2) == p3) != ((p1, p2, p3) in brute_p):
                    fail(f"Brute-force mismatch at ({p1}, {p2}, {p3})")
    print(f"      Brute-force match OK ({len(brute_p)} P-positions checked).")

    print("[2/5] Verifying m = 0..12 constants, Table 1 (m = 0..10), Claims 3.3-3.5, and Lemma 2.6 direct induction...")
    verified = {}
    for expected_m, lv in enumerate(levels):
        if lv.get("m") != expected_m:
            fail(f"Level index mismatch: expected {expected_m}, got {lv.get('m')}")
        m = expected_m
        pm = xor_period(m)
        if lv.get("p_m") != pm:
            fail(f"m={m}: p_m mismatch")

        seq = p_seq[m]
        cutoff = len(seq) - 20

        # Recompute T^m from Claim 3.1
        recomp_T = sorted(p_by_y[a][m] - m for a in range(m) if m in p_by_y[a])
        if lv.get("T") != recomp_T:
            fail(f"m={m}: T mismatch")

        # Verify mex rule across prefix through cutoff
        used = set(range(m)) | {m + b for b in recomp_T}
        least = m
        for j in range(1, cutoff + 1):
            while least in used:
                least += 1
            A_j, B_j = seq[j]
            if m + A_j != least:
                fail(f"m={m}: mex failed at j={j}")
            if m + A_j + B_j in used:
                fail(f"m={m}: Z_{j} reused in mex")
            used.update((m + A_j, m + A_j + B_j))

        n1 = int(lv["n1"])
        n2 = int(lv["n2"])
        N_c34 = int(lv["N_claim34"])
        alpha = int(lv["alpha"])
        if n1 + 5 >= len(seq) or not (0 <= N_c34 < n2 < n1):
            fail(f"m={m}: invalid index ordering or horizon")
        if lv.get("N_claim34") != n2 - 1:
            fail(f"m={m}: N_claim34 mismatch")

        # Validate exact spot fields
        if lv.get("A_n1") != seq[n1][0] or lv.get("B_n1") != seq[n1][1]:
            fail(f"m={m}: A_n1/B_n1 mismatch")
        if lv.get("P_n2_plus_3") != [m, seq[n2 + 3][0], seq[n2 + 3][1]]:
            fail(f"m={m}: P_n2_plus_3 mismatch")
        if lv.get("P_n1") != [m, seq[n1][0], seq[n1][1]]:
            fail(f"m={m}: P_n1 mismatch")
        if lv.get("next_middle") != m + seq[n1 + 1][0] or lv.get("next_gap") != seq[n1 + 1][1]:
            fail(f"m={m}: next_middle/next_gap mismatch")

        def offset_at(j):
            return m + seq[j][0] - floor_phi(seq[j][1])

        def eps_at(j):
            return offset_at(j) - alpha

        # Recompute N1, N2, N3, B_N3, B_N3_plus_1, S
        recomp_N1 = max((j + 1 for j in range(1, cutoff) if seq[j + 1][1] != seq[j][1] + 1), default=1)
        recomp_N2 = max((j + 1 for j in range(1, cutoff) if abs(eps_at(j)) > 1), default=1)
        recomp_N3 = max((j + 1 for j in range(1, n1) if eps_at(j) != 0 and eps_at(j + 1) != 0), default=1)
        if m > 0:
            recomp_S = sorted(set(range(seq[cutoff][1])) - {seq[j][1] for j in range(1, cutoff + 1)})
        else:
            recomp_S = []

        if lv.get("N1") != recomp_N1 or lv.get("N2") != recomp_N2 or lv.get("N3") != recomp_N3:
            fail(f"m={m}: N1/N2/N3 mismatch")
        if lv.get("B_N3") != seq[recomp_N3][1] or lv.get("B_N3_plus_1") != seq[recomp_N3 + 1][1]:
            fail(f"m={m}: B_N3 / B_N3_plus_1 mismatch")
        if lv.get("S") != recomp_S:
            fail(f"m={m}: S mismatch")

        # Forbidden max for synthetic Wythoff continuation
        start = 2 if m == 0 else recomp_N1
        forbidden_max = max([m - 1, *[m + b for b in recomp_T], *[m + seq[j][0] + seq[j][1] for j in range(1, start)]])
        if lv.get("Wythoff_forbidden_max") != forbidden_max:
            fail(f"m={m}: Wythoff_forbidden_max mismatch")
        if m + seq[start][0] + seq[start][1] <= forbidden_max:
            fail(f"m={m}: Z_start <= Wythoff_forbidden_max")
        if not all(seq[j][1] < seq[start][1] for j in range(1, start)):
            fail(f"m={m}: early gap >= B_start")
        if not all(seq[j + 1][1] == seq[j][1] + 1 for j in range(start, n1 + 2)):
            fail(f"m={m}: gaps not consecutive from start through n1+1")

        # Lemma 2.6 history checks
        first_above = next(j for j in range(1, n1) if m + seq[j][0] > forbidden_max)
        if m + seq[n2 - 3][0] <= forbidden_max:
            fail(f"m={m}: Y_{{n2-3}} <= Wythoff_forbidden_max")
        if m + seq[n1 - 3][0] <= m + seq[first_above][0] + seq[first_above][1]:
            fail(f"m={m}: Y_{{n1-3}} <= Z_first_above")
        if m + seq[n1 - 3][0] - 1 <= m + seq[n2 - 5][0] + seq[n2 - 5][1]:
            fail(f"m={m}: Y_{{n1-3}}-1 <= Z_{{n2-5}}")
        if m + seq[n1][0] <= m + seq[n2][0] + seq[n2][1]:
            fail(f"m={m}: Y_n1 <= Z_n2")
        if eps_at(n1) != 0:
            fail(f"m={m}: eps_n1 != 0")
        if not all(abs(eps_at(j)) <= 1 for j in range(max(1, n2 - 4), n1 + 1)):
            fail(f"m={m}: |eps| > 1 in Lemma 2.6 window")
        if not all(eps_at(j - 2) * eps_at(j - 1) * eps_at(j) == 0 for j in range(max(3, n2 - 2), n1 + 1)):
            fail(f"m={m}: nonzero triple in Lemma 2.6 window")

        if m > 0:
            # Claim 3.5 conditions 1..8 (half-sum midpoint)
            if seq[n1][0] <= seq[n2 + 3][0] + seq[n2 + 3][1]:
                fail(f"m={m}: Claim 3.5 Cond 1 failed")
            if not all(seq[j + 1][1] == seq[j][1] + 1 for j in range(n2, n1 + 1)):
                fail(f"m={m}: Claim 3.5 Cond 2 failed")
            B_prefix = {seq[j][1] for j in range(1, n1 + 1)}
            if seq[n1][1] != max(B_prefix):
                fail(f"m={m}: Claim 3.5 Cond 3 failed")
            mex_val = 0
            s1 = lv.get("S1_n1")
            if s1 != recomp_S:
                fail(f"m={m}: S1_n1 != S")
            while mex_val in B_prefix or mex_val in set(s1):
                mex_val += 1
            if mex_val != seq[n1][1] + 1:
                fail(f"m={m}: Claim 3.5 Cond 4 failed")
            als = [offset_at(j) for j in range(n2, n1 + 1)]
            if max(als) - min(als) > 2 or (max(als) + min(als)) // 2 != alpha:
                fail(f"m={m}: Claim 3.5 Cond 5 failed")
            for i in range(m):
                if seq[n1][1] <= verified[i]["B_N3"] or seq[n1][1] <= verified[i]["B_N3_plus_1"]:
                    fail(f"m={m}: Claim 3.5 Cond 6 failed vs i={i}")
                if verified[i]["alpha"] - alpha < 4 * (m - i):
                    fail(f"m={m}: Claim 3.5 Cond 7 failed vs i={i}")
            if not all(abs(eps_at(j)) <= 1 for j in range(n2 - 2, n1 + 1)):
                fail(f"m={m}: Claim 3.5 Cond 8a failed")
            if not all(eps_at(j - 2) * eps_at(j - 1) * eps_at(j) == 0 for j in range(n2, n1 + 1)):
                fail(f"m={m}: Claim 3.5 Cond 8b failed")

            # Claim 3.4 thresholds and anchor separation
            max_T_m = max([0, *[v for i in range(m) for v in verified[i]["T"]], *recomp_T])
            if lv.get("max_T_through_m") != max_T_m:
                fail(f"m={m}: max_T_through_m mismatch")
            if not all(seq[j][0] > max_T_m and seq[j][1] > m + max_T_m for j in range(n2, n1 + 2)):
                fail(f"m={m}: Claim 3.4 threshold failed")
            Y_next = m + seq[n1 + 1][0]
            B_next = seq[n1 + 1][1]
            for i in range(m):
                for A_i, B_i in p_seq[i][1:]:
                    if i + A_i <= Y_next and B_next - B_i <= m - i:
                        fail(f"m={m}: Claim 3.4 lower separation failed at i={i}")

            # Direct induction bounds (small_two_max & offset_slack)
            small_two_max = max(i + A_i + B_i for i in range(m) for A_i, B_i in p_seq[i][1:] if i + A_i <= m)
            if lv.get("small_two_max") != small_two_max:
                fail(f"m={m}: small_two_max mismatch")
            if m + seq[n1][0] <= small_two_max or seq[n1][1] <= small_two_max + m:
                fail(f"m={m}: small_two_max anchor bound failed")
            recomp_slack = [verified[i]["alpha"] - alpha - floor_phi(m - i) - 3 for i in range(m)]
            if lv.get("offset_slack") != recomp_slack:
                fail(f"m={m}: offset_slack mismatch")
            if m >= 11:
                if min(recomp_slack) <= 0:
                    fail(f"m={m}: nonpositive offset_slack")
            else:
                if not all(sl > 0 or (sl == 0 and m - i == 1) for i, sl in enumerate(recomp_slack)):
                    fail(f"m={m}: unexpected zero/negative offset_slack")

            # Claim 3.3 modulo-p(m) XOR ray witnesses across [Y_n1, Y_n1 + p_m]
            Y_n1 = m + seq[n1][0]
            witnesses = lv.get("S1_n1_witnesses")
            if not isinstance(witnesses, list) or len(witnesses) != len(recomp_S):
                fail(f"m={m}: S1_n1_witnesses length mismatch")
            for c_val, entry in zip(recomp_S, witnesses):
                if entry.get("c") != c_val or entry.get("ray_start_Y") != Y_n1 or entry.get("period") != pm:
                    fail(f"m={m}: witness header mismatch for c={c_val}")
                dests = entry.get("destinations")
                if not isinstance(dests, list) or len(dests) != pm + 1:
                    fail(f"m={m}: witness destinations length != p_m+1 for c={c_val}")
                for offset, dest in enumerate(dests):
                    if not verify_ray_move(m, Y_n1 + offset, c_val, dest, p_by_y, pm):
                        fail(f"m={m}: invalid XOR witness at c={c_val}, offset={offset}")

        verified[m] = lv
        print(f"      m={m:2d} OK: alpha={alpha:3d}, N1={recomp_N1:4d}, N2={recomp_N2:4d}, "
              f"N3={recomp_N3:4d} (B_N3={seq[recomp_N3][1]:4d}), n2={n2:4d}, n1={n1:4d}")

    print("[3/5] Auditing Sun & Zeilberger Table 1 (m = 0..10)...")
    for m in range(11):
        lv = verified[m]
        pub = PUBLISHED_TABLE_1[m]
        if (lv["T"] != pub["T"] or lv["S"] != pub["S"] or lv["alpha"] != pub["alpha"]
                or lv["N1"] != pub["N1"] or lv["N2"] != pub["N2"]):
            fail(f"Table 1 mismatch at m={m}")
    print("      All 11 rows of Sun & Zeilberger Table 1 match identically (partial win p1 confirmed).")

    print("[4/5] Verifying m = 11 prerequisite and m = 12 target constants...")
    for m in (11, 12):
        lv = verified[m]
        print(f"      m={m}: T={lv['T']}, |S|={len(lv['S'])}, alpha={lv['alpha']}, "
              f"N1={lv['N1']}, N2={lv['N2']}, N3={lv['N3']}, B_N3={lv['B_N3']}, "
              f"n2={lv['n2']}, n1={lv['n1']}, B_n1={lv['B_n1']}, min_slack={min(lv['offset_slack'])}")

    print("[5/5] All certificate integrity, rule-recomputation, Table 1, Claim 3.3-3.5, and Lemma 2.6 checks complete.")
    print("PASS")


if __name__ == "__main__":
    main()
