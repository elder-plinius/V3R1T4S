#!/usr/bin/env python3
"""Verify the toroidal queens certificate and check the packaged tables.

Requires Python 3.10+ and uses only the standard library.

Direct game-tree checks cover toroidal sizes 1–12, all 21 symmetry orbits
of the size-14 counterexample certificate, planar margins at sizes 8, 10
and 12, the size-14 planar mutual-reply certificate, and planar nimbers at
sizes 0–8. Other records are checked against saved counts and reconstructed
board geometry. The packaged C++ solvers recompute the full results.

Prints diagnostics, ending in PASS on success or FAIL on a detected error.
"""
import json
import os
import sys
import time


def fail(msg):
    print("ERROR: " + msg)
    print("FAIL")
    sys.exit(1)


def require(cond, msg):
    if not cond:
        fail(msg)


def build_toroidal_attacks(n):
    N = n * n
    attacks = [0] * N
    for r1 in range(n):
        for c1 in range(n):
            u = r1 * n + c1
            m = 0
            for r2 in range(n):
                for c2 in range(n):
                    if (r1 == r2 or c1 == c2 or
                        (r1 - c1) % n == (r2 - c2) % n or
                        (r1 + c1) % n == (r2 + c2) % n):
                        m |= 1 << (r2 * n + c2)
            attacks[u] = m
    return attacks


def build_d4_origin_perms(n):
    N = n * n
    perms = []
    for s in range(8):
        perm = [0] * N
        for r in range(n):
            for c in range(n):
                nr = (n - r) % n
                nc = (n - c) % n
                rr, cc = [
                    (r, c), (r, nc), (nr, c), (nr, nc),
                    (c, r), (c, nr), (nc, r), (nc, nr)
                ][s]
                perm[r * n + c] = rr * n + cc
        perms.append(perm)
    return perms


def build_planar_attacks(n):
    N = n * n
    attacks = [0] * N
    for r1 in range(n):
        for c1 in range(n):
            u = r1 * n + c1
            m = 0
            for r2 in range(n):
                for c2 in range(n):
                    if (r1 == r2 or c1 == c2 or
                        (r1 - c1) == (r2 - c2) or
                        (r1 + c1) == (r2 + c2)):
                        m |= 1 << (r2 * n + c2)
            attacks[u] = m
    return attacks


def build_planar_d4_perms(n):
    N = n * n
    perms = []
    for s in range(8):
        perm = [0] * N
        for r in range(n):
            for c in range(n):
                nr = n - 1 - r
                nc = n - 1 - c
                rr, cc = [
                    (r, c), (r, nc), (nr, c), (nr, nc),
                    (c, r), (c, nr), (nc, r), (nc, nr)
                ][s]
                perm[r * n + c] = rr * n + cc
        perms.append(perm)
    return perms


def make_win_solver(attacks):
    memo = {0: False}

    def win(avail):
        v = memo.get(avail)
        if v is not None:
            return v
        pc = avail.bit_count()
        if pc == 1:
            memo[avail] = True
            return True
        if pc == 2:
            u = (avail & -avail).bit_length() - 1
            res = (avail & ~attacks[u]) == 0
            memo[avail] = res
            return res
        moves = []
        a = avail
        while a:
            b = a & -a
            u = b.bit_length() - 1
            a ^= b
            rem = avail & ~attacks[u]
            if rem == 0:
                memo[avail] = True
                return True
            rpc = rem.bit_count()
            if rpc == 1:
                continue
            moves.append((rpc, rem))
        if not moves:
            memo[avail] = False
            return False
        moves.sort()
        res = False
        prev_rem = -1
        for rpc, rem in moves:
            if rem == prev_rem:
                continue
            prev_rem = rem
            if not win(rem):
                res = True
                break
        memo[avail] = res
        return res

    return win, memo


def solve_planar_nimber_exact(n):
    if n == 0:
        return 0
    N = n * n
    attacks = build_planar_attacks(n)
    perms = build_planar_d4_perms(n)
    memo = {0: 0}

    def canon(mask):
        best = mask
        for s in range(1, 8):
            p = perms[s]
            m = 0
            a = mask
            while a:
                b = a & -a
                u = b.bit_length() - 1
                a ^= b
                m |= 1 << p[u]
            if m < best:
                best = m
        return best

    def sg(avail):
        c = canon(avail) if avail.bit_count() >= 5 else avail
        v = memo.get(c)
        if v is not None:
            return v
        pc = c.bit_count()
        if pc == 1:
            memo[c] = 1
            return 1
        seen = 0
        a = c
        while a:
            b = a & -a
            u = b.bit_length() - 1
            a ^= b
            seen |= 1 << sg(c & ~attacks[u])
        g = 0
        while (seen >> g) & 1:
            g += 1
        memo[c] = g
        return g

    return sg((1 << N) - 1)


def verify_json_object(obj_path):
    t0 = time.time()
    try:
        with open(obj_path, "r", encoding="utf-8") as f:
            obj = json.load(f)
    except Exception as e:
        fail(f"Failed to parse JSON {obj_path}: {e}")

    require(isinstance(obj, dict), "Top-level JSON must be an object")
    expected_top_keys = {
        "target_id",
        "toroidal_queens_nimbers",
        "tq14_counterexample_certificate",
        "central_strike_refutation_margins",
        "planar_a344227_calibration",
    }
    require(set(obj.keys()) == expected_top_keys, f"Unexpected top-level keys: {set(obj.keys())}")
    require(obj["target_id"] == "non-attacking-queens-game-nimbers-a344227", "Mismatched target_id")

    # 1. Verify toroidal_queens_nimbers (n = 1..16)
    tq_list = obj["toroidal_queens_nimbers"]
    require(isinstance(tq_list, list) and len(tq_list) == 16, "toroidal_queens_nimbers must have 16 entries")

    expected_tq_win_replies = {
        1: 0, 2: 0, 3: 0, 4: 4, 5: 0, 6: 16, 7: 0, 8: 36,
        9: 0, 10: 8, 11: 0, 12: 20, 13: 0, 14: 0, 15: 0, 16: 196
    }

    for idx, rec in enumerate(tq_list):
        n = idx + 1
        require(isinstance(rec, dict), f"TQ record {n} must be a dict")
        req_keys = {
            "n", "N_squares", "closed_neighborhood_size", "Hn_live_squares",
            "Hn_d4_orbits", "G_TQn", "Hn_winning_replies", "Hn_losing_replies",
            "conjecture_T1_prediction_for_n_ge_4", "conjecture_T1_holds_for_n_ge_4"
        }
        require(set(rec.keys()) == req_keys, f"TQ_{n} keys mismatch")
        require(rec["n"] == n, f"TQ_{n} n mismatch")
        N = n * n
        require(rec["N_squares"] == N, f"TQ_{n} N_squares mismatch")

        attacks = build_toroidal_attacks(n)
        perms = build_d4_origin_perms(n)
        full = (1 << N) - 1
        H_n = full & ~attacks[0]
        live = H_n.bit_count()
        deg = attacks[0].bit_count()
        require(rec["closed_neighborhood_size"] == deg, f"TQ_{n} closed_neighborhood_size mismatch")
        require(rec["Hn_live_squares"] == live, f"TQ_{n} Hn_live_squares mismatch")
        require(deg + live == N, f"TQ_{n} deg + live != N")

        orbits = {}
        a = H_n
        while a:
            b = a & -a
            u = b.bit_length() - 1
            a ^= b
            rep = min(perms[s][u] for s in range(8))
            orbits.setdefault(rep, set()).add(u)
        require(rec["Hn_d4_orbits"] == len(orbits), f"TQ_{n} Hn_d4_orbits mismatch")

        win_rep = rec["Hn_winning_replies"]
        lose_rep = rec["Hn_losing_replies"]
        require(win_rep == expected_tq_win_replies[n], f"TQ_{n} Hn_winning_replies mismatch")
        require(lose_rep == live - win_rep, f"TQ_{n} Hn_losing_replies mismatch")
        g_expected = 1 if win_rep == 0 else 0
        require(rec["G_TQn"] == g_expected, f"TQ_{n} G_TQn mismatch")

        t1_pred = (n % 2) if n >= 4 else -1
        t1_holds = (1 if g_expected == (n % 2) else 0) if n >= 4 else -1
        require(rec["conjecture_T1_prediction_for_n_ge_4"] == t1_pred, f"TQ_{n} T1 prediction mismatch")
        require(rec["conjecture_T1_holds_for_n_ge_4"] == t1_holds, f"TQ_{n} T1 holds mismatch")

        # For n = 1..12, solve every D_4((0,0)) orbit of H_n directly in pure Python
        if n <= 12:
            win_fn, _ = make_win_solver(attacks)
            computed_win_replies = 0
            for rep, members in orbits.items():
                if not win_fn(H_n & ~attacks[rep]):
                    computed_win_replies += len(members)
            require(computed_win_replies == win_rep,
                    f"TQ_{n} direct game-tree win replies {computed_win_replies} != {win_rep}")

    print(f"[1/4] Checked toroidal table for n=1..16 (direct game-tree solve for n=1..12) in {time.time()-t0:.2f}s")

    # 2. Verify tq14_counterexample_certificate (complete pure-Python verification of all 21 D_4 orbits of H_14)
    t1 = time.time()
    cert = obj["tq14_counterexample_certificate"]
    require(isinstance(cert, dict), "tq14_counterexample_certificate must be a dict")
    req_cert_keys = {
        "n", "G_TQ14", "conjecture_T1_prediction", "Hn_live_squares",
        "Hn_d4_orbits", "Hn_winning_replies", "Hn_losing_replies", "d4_orbit_certificates"
    }
    require(set(cert.keys()) == req_cert_keys, "tq14_counterexample_certificate keys mismatch")
    require(cert["n"] == 14, "cert n != 14")
    require(cert["G_TQ14"] == 1, "cert G_TQ14 != 1")
    require(cert["conjecture_T1_prediction"] == 0, "cert conjecture_T1_prediction != 0")
    require(cert["Hn_live_squares"] == 144, "cert Hn_live_squares != 144")
    require(cert["Hn_d4_orbits"] == 21, "cert Hn_d4_orbits != 21")
    require(cert["Hn_winning_replies"] == 0, "cert Hn_winning_replies != 0")
    require(cert["Hn_losing_replies"] == 144, "cert Hn_losing_replies != 144")

    attacks14 = build_toroidal_attacks(14)
    perms14 = build_d4_origin_perms(14)
    H14 = ((1 << 196) - 1) & ~attacks14[0]
    win14, _ = make_win_solver(attacks14)

    orb_list = cert["d4_orbit_certificates"]
    require(isinstance(orb_list, list) and len(orb_list) == 21, "d4_orbit_certificates must have 21 entries")
    covered_H14 = set()
    prev_u2 = -1
    for idx, orec in enumerate(orb_list, 1):
        req_okeys = {
            "orbit_id", "u2_idx", "u2_rc", "orbit_size", "orbit_members_idx",
            "M1_live_squares", "player1_winning_reply_w3_idx",
            "player1_winning_reply_w3_rc", "P1_residual_live_squares"
        }
        require(set(orec.keys()) == req_okeys, f"Orbit {idx} keys mismatch")
        require(orec["orbit_id"] == idx, f"Orbit {idx} orbit_id mismatch")
        u2 = orec["u2_idx"]
        require(isinstance(u2, int) and u2 > prev_u2, f"Orbit {idx} u2_idx ordering invalid")
        prev_u2 = u2
        require(orec["u2_rc"] == [u2 // 14, u2 % 14], f"Orbit {idx} u2_rc mismatch")
        require(((H14 >> u2) & 1) == 1, f"Orbit {idx} u2 not in H_14")

        true_members = sorted({perms14[s][u2] for s in range(8)})
        require(u2 == true_members[0], f"Orbit {idx} u2 is not minimal orbit representative")
        require(orec["orbit_members_idx"] == true_members, f"Orbit {idx} orbit_members_idx mismatch")
        require(orec["orbit_size"] == len(true_members), f"Orbit {idx} orbit_size mismatch")
        for m in true_members:
            require(m not in covered_H14, f"Orbit {idx} member {m} overlaps previous orbit")
            covered_H14.add(m)

        M1 = H14 & ~attacks14[u2]
        require(orec["M1_live_squares"] == M1.bit_count(), f"Orbit {idx} M1_live_squares mismatch")
        w3 = orec["player1_winning_reply_w3_idx"]
        require(isinstance(w3, int) and 0 <= w3 < 196, f"Orbit {idx} w3 out of range")
        require(orec["player1_winning_reply_w3_rc"] == [w3 // 14, w3 % 14], f"Orbit {idx} w3_rc mismatch")
        require(((M1 >> w3) & 1) == 1, f"Orbit {idx} reply w3={w3} is not a legal live square in M1")
        P1 = M1 & ~attacks14[w3]
        require(orec["P1_residual_live_squares"] == P1.bit_count(), f"Orbit {idx} P1_residual_live_squares mismatch")
        require(not win14(P1), f"Orbit {idx} residual P1 after u2={u2}, w3={w3} is NOT a P-position!")

    true_H14_set = {u for u in range(196) if (H14 >> u) & 1}
    require(covered_H14 == true_H14_set and len(covered_H14) == 144,
            "21 D_4 orbits do not partition all 144 live squares of H_14")
    print(f"[2/4] Verified 21-orbit ply-3 strategy certificate for G(TQ_14) = 1 (all 144 replies in H_14 refuted) in {time.time()-t1:.2f}s")

    # 3. Verify central_strike_refutation_margins (n = 8, 10, 12, 14, 16)
    t2 = time.time()
    margins = obj["central_strike_refutation_margins"]
    require(isinstance(margins, list) and len(margins) == 5, "central_strike_refutation_margins must have 5 entries")
    expected_margin_ns = [8, 10, 12, 14, 16]
    expected_ref_counts = {8: 0, 10: 8, 12: 100, 14: 140, 16: 146}
    expected_non_ref = {
        10: [[0,1],[0,2],[0,3],[0,5],[0,6],[0,7],[0,9],[1,0],[1,2],[1,3],[1,5],[1,6],[1,8],[2,0],[2,1],[2,5],[2,7],[2,8],[2,9],[3,0],[3,1],[3,6],[3,7],[3,8],[5,0],[5,1],[5,2],[5,7],[5,8],[5,9],[6,0],[6,1],[6,3],[6,7],[6,8],[6,9],[7,0],[7,2],[7,3],[7,5],[7,6],[7,8],[7,9],[8,1],[8,2],[8,3],[8,5],[8,6],[8,7],[8,9],[9,0],[9,2],[9,5],[9,6],[9,7],[9,8]],
        12: [],
        14: [[4,7],[7,4],[7,8],[8,7]],
        16: [[0,1],[0,2],[0,8],[0,13],[0,15],[1,0],[1,10],[1,15],[2,0],[4,6],[4,8],[4,9],[4,13],[5,6],[5,8],[6,4],[6,5],[6,9],[6,10],[6,11],[6,15],[8,0],[8,4],[8,5],[8,9],[8,10],[8,11],[9,4],[9,6],[9,8],[9,10],[9,11],[10,1],[10,6],[10,8],[10,9],[10,13],[11,6],[11,8],[11,9],[13,0],[13,4],[13,10],[13,15],[14,15],[15,0],[15,1],[15,6],[15,13],[15,14]]
    }

    for idx, mrec in enumerate(margins):
        n = expected_margin_ns[idx]
        req_mkeys = {
            "n", "c_star_rc", "c_star_idx", "Rn_live_squares",
            "refuting_replies_count", "non_refuting_replies_count",
            "refuting_squares_rc", "non_refuting_squares_rc"
        }
        require(set(mrec.keys()) == req_mkeys, f"R_{n} keys mismatch")
        require(mrec["n"] == n, f"R_{n} n mismatch")
        c_star_r = n // 2 - 1
        c_star_idx = c_star_r * n + c_star_r
        require(mrec["c_star_rc"] == [c_star_r, c_star_r], f"R_{n} c_star_rc mismatch")
        require(mrec["c_star_idx"] == c_star_idx, f"R_{n} c_star_idx mismatch")

        attacks_p = build_planar_attacks(n)
        Rn_mask = ((1 << (n * n)) - 1) & ~attacks_p[c_star_idx]
        true_live_rc = [[u // n, u % n] for u in range(n * n) if (Rn_mask >> u) & 1]
        require(len(true_live_rc) == (n - 2) * (n - 2), f"R_{n} live count != (n-2)^2")
        require(mrec["Rn_live_squares"] == len(true_live_rc), f"R_{n} Rn_live_squares mismatch")

        ref_rc = mrec["refuting_squares_rc"]
        non_ref_rc = mrec["non_refuting_squares_rc"]
        require(isinstance(ref_rc, list) and isinstance(non_ref_rc, list), f"R_{n} square lists must be lists")
        require(mrec["refuting_replies_count"] == expected_ref_counts[n], f"R_{n} refuting_replies_count mismatch")
        require(mrec["non_refuting_replies_count"] == len(true_live_rc) - expected_ref_counts[n],
                f"R_{n} non_refuting_replies_count mismatch")
        require(len(ref_rc) == mrec["refuting_replies_count"], f"R_{n} len(ref_rc) mismatch")
        require(len(non_ref_rc) == mrec["non_refuting_replies_count"], f"R_{n} len(non_ref_rc) mismatch")

        # Check strict sorting, format, disjointness, exact partition of R_n, and diagonal reflection symmetry
        for lst_name, lst in [("refuting", ref_rc), ("non_refuting", non_ref_rc)]:
            for k_i, pair in enumerate(lst):
                require(isinstance(pair, list) and len(pair) == 2 and
                        isinstance(pair[0], int) and isinstance(pair[1], int),
                        f"R_{n} {lst_name} entry {k_i} invalid")
                if k_i > 0:
                    require(lst[k_i - 1] < pair, f"R_{n} {lst_name} not strictly sorted at {k_i}")
            s_tuples = {tuple(p) for p in lst}
            for r_i, c_i in s_tuples:
                require((c_i, r_i) in s_tuples, f"R_{n} {lst_name} not diagonally symmetric at ({r_i},{c_i})")

        ref_set = {tuple(p) for p in ref_rc}
        non_ref_set = {tuple(p) for p in non_ref_rc}
        true_set = {tuple(p) for p in true_live_rc}
        require(ref_set.isdisjoint(non_ref_set), f"R_{n} refuting and non_refuting overlap")
        require(ref_set | non_ref_set == true_set, f"R_{n} refuting union non_refuting != R_{n}")

        if n in expected_non_ref:
            require(non_ref_rc == expected_non_ref[n], f"R_{n} non_refuting_squares_rc mismatch")

        # Direct pure-Python game-tree verification for n = 8, 10, 12 (folded across main diagonal r <= c)
        if n <= 12:
            win_p, _ = make_win_solver(attacks_p)
            comp_ref_set = set()
            comp_non_ref_set = set()
            for r_i, c_i in true_live_rc:
                if r_i > c_i:
                    continue
                u = r_i * n + c_i
                if not win_p(Rn_mask & ~attacks_p[u]):
                    comp_ref_set.add((r_i, c_i))
                    comp_ref_set.add((c_i, r_i))
                else:
                    comp_non_ref_set.add((r_i, c_i))
                    comp_non_ref_set.add((c_i, r_i))
            comp_ref = sorted([list(p) for p in comp_ref_set])
            comp_non_ref = sorted([list(p) for p in comp_non_ref_set])
            require(comp_ref == ref_rc, f"R_{n} direct game-tree refuting squares mismatch")
            require(comp_non_ref == non_ref_rc, f"R_{n} direct game-tree non-refuting squares mismatch")

        # For n = 14, also verify in pure Python that the 4 non-refuting squares (4,7), (7,8) and (7,4), (8,7)
        # form two mutual winning-reply pairs whose residual board is a P-position!
        if n == 14:
            win_p14, _ = make_win_solver(attacks_p)
            u_47 = 4 * 14 + 7
            u_78 = 7 * 14 + 8
            P_pair = Rn_mask & ~attacks_p[u_47] & ~attacks_p[u_78]
            require(not win_p14(P_pair), "R_14 mutual reply residual P_pair for (4,7)+(7,8) is not a P-position!")

    print(f"[3/4] Checked planar margin tables (direct R_8, R_10, R_12 solves and the R_14 mutual-reply certificate) in {time.time()-t2:.2f}s")

    # 4. Verify planar_a344227_calibration (n = 0..16, with exact mex solve for n = 0..8)
    t3 = time.time()
    cal = obj["planar_a344227_calibration"]
    expected_a344227 = [0, 1, 1, 2, 1, 3, 1, 2, 3, 1, 0, 1, 0, 1, 0, 1, 0]
    require(isinstance(cal, list) and len(cal) == 17, "planar_a344227_calibration must have 17 entries")
    for n, rec in enumerate(cal):
        require(isinstance(rec, dict) and set(rec.keys()) == {"n", "G_Qn"}, f"A344227({n}) keys mismatch")
        require(rec["n"] == n, f"A344227({n}) n mismatch")
        require(rec["G_Qn"] == expected_a344227[n], f"A344227({n}) G_Qn mismatch")
        if n <= 8:
            g_comp = solve_planar_nimber_exact(n)
            require(g_comp == rec["G_Qn"], f"A344227({n}) exact mex {g_comp} != {rec['G_Qn']}")

    print(f"[4/4] Checked planar A344227 table for n=0..16 (exact mex solve for n=0..8) in {time.time()-t3:.2f}s")
    print(f"All checks passed in {time.time()-t0:.2f}s.")
    print("PASS")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    candidates = [
        sys.argv[1] if len(sys.argv) > 1 else "",
        os.path.join(here, "..", "object", "toroidal_queens_and_margins.json"),
        os.path.join(here, "..", "result", "toroidal_queens_and_margins.json"),
        "object/toroidal_queens_and_margins.json",
        "result/toroidal_queens_and_margins.json",
    ]
    target_path = None
    for c in candidates:
        if c and os.path.isfile(c):
            target_path = c
            break
    if not target_path:
        fail("Could not locate toroidal_queens_and_margins.json")
    verify_json_object(target_path)
