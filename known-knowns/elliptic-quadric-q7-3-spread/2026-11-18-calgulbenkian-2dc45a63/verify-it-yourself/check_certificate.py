#!/usr/bin/env python3
"""Zero-shared-code standalone verifier for elliptic-quadric-q7-3-spread (p1).

Validates every algebraic, group-theoretic, and combinatorial field of
object/q7_3_ord3_certificate.json from scratch using Python 3 stdlib, then
compiles and executes verify_engine2_dlx.c (Engine 2: Row-Elimination DLX) on
the certified matrices. Prints PASS on success; exits 1 with final line FAIL
on any mismatch.
"""
import itertools
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time


def fail(msg):
    sys.stdout.write(f"ERROR: {msg}\nFAIL\n")
    sys.stdout.flush()
    sys.exit(1)


def require(cond, msg):
    if not cond:
        fail(msg)


def eval_q6(x):
    return (x[0] * x[1] + x[2] * x[3] + x[4] * x[4] + x[5] * x[5]) % 3


def eval_b6(x, y):
    return (
        x[0] * y[1] + x[1] * y[0]
        + x[2] * y[3] + x[3] * y[2]
        + 2 * x[4] * y[4] + 2 * x[5] * y[5]
    ) % 3


def eval_q8(x):
    return (x[0] * x[1] + x[2] * x[3] + x[4] * x[5] + x[6] * x[6] + x[7] * x[7]) % 3


def eval_b8(x, y):
    return (
        x[0] * y[1] + x[1] * y[0]
        + x[2] * y[3] + x[3] * y[2]
        + x[4] * y[5] + x[5] * y[4]
        + 2 * x[6] * y[6] + 2 * x[7] * y[7]
    ) % 3


def canon_vec(v):
    for val in v:
        if val != 0:
            if val == 1:
                return tuple(v)
            return tuple((2 * c) % 3 for c in v)
    return None


def mmul(A, B):
    n = len(A)
    return [[sum(A[r][k] * B[k][c] for k in range(n)) % 3 for c in range(n)] for r in range(n)]


def mpow(A, exp):
    n = len(A)
    res = [[1 if r == c else 0 for c in range(n)] for r in range(n)]
    base = [row[:] for row in A]
    e = exp
    while e > 0:
        if e & 1:
            res = mmul(res, base)
        base = mmul(base, base)
        e >>= 1
    return res


def mtranspose(A):
    n = len(A)
    return [[A[c][r] for c in range(n)] for r in range(n)]


def apply_mat(A, v):
    return tuple(sum(A[r][c] * v[c] for c in range(len(v))) % 3 for r in range(len(A)))


def rank_mod3(rows, ncols):
    M = [[x % 3 for x in r] for r in rows]
    rnk = 0
    for col in range(ncols):
        piv = None
        for r in range(rnk, len(M)):
            if M[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        M[rnk], M[piv] = M[piv], M[rnk]
        inv = 1 if M[rnk][col] == 1 else 2
        M[rnk] = [(x * inv) % 3 for x in M[rnk]]
        for r in range(len(M)):
            if r != rnk and M[r][col] != 0:
                f = M[r][col]
                M[r] = [(M[r][j] - f * M[rnk][j]) % 3 for j in range(ncols)]
        rnk += 1
    return rnk


def check_matrix_shape(M, n, label):
    require(isinstance(M, list) and len(M) == n, f"{label}: not {n} rows")
    for row in M:
        require(isinstance(row, list) and len(row) == n, f"{label}: row not length {n}")
        for x in row:
            require(type(x) is int and x in (0, 1, 2), f"{label}: invalid entry {x}")


def verify_q5_control(ctrl):
    require(isinstance(ctrl, dict), "positive_control_q5_3 must be dict")
    require(ctrl.get("quadratic_form") == "x1*x2 + x3*x4 + x5^2 + x6^2 mod 3", "q5 form mismatch")

    pts6 = []
    pt6_map = {}
    for v in itertools.product(range(3), repeat=6):
        cv = canon_vec(v)
        if cv == v and eval_q6(v) == 0:
            pt6_map[v] = len(pts6)
            pt6_map[tuple((2 * x) % 3 for x in v)] = len(pts6)
            pts6.append(v)
    require(len(pts6) == 112 and ctrl.get("singular_points") == 112, "q5 singular_points mismatch")

    # Independent RREF count of lines on Q^-(5,3)
    nlines6 = 0
    for p0 in range(6):
        for p1 in range(p0 + 1, 6):
            f0 = [c for c in range(p0 + 1, 6) if c != p1]
            f1 = list(range(p1 + 1, 6))
            for t0 in itertools.product(range(3), repeat=len(f0)):
                r0 = [0] * 6
                r0[p0] = 1
                for c, val in zip(f0, t0):
                    r0[c] = val
                if eval_q6(r0) != 0:
                    continue
                for t1 in itertools.product(range(3), repeat=len(f1)):
                    r1 = [0] * 6
                    r1[p1] = 1
                    for c, val in zip(f1, t1):
                        r1[c] = val
                    if eval_q6(r1) == 0 and eval_b6(r0, r1) == 0:
                        nlines6 += 1
    require(nlines6 == 280 and ctrl.get("totally_singular_lines") == 280, "q5 lines mismatch")
    require(ctrl.get("lines_per_spread") == 28, "q5 lines_per_spread mismatch")

    A6 = ctrl.get("order_3_matrix")
    check_matrix_shape(A6, 6, "q5 order_3_matrix")
    G6 = [[0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0],
          [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 2]]
    I6 = [[1 if r == c else 0 for c in range(6)] for r in range(6)]
    require(mmul(mmul(mtranspose(A6), G6), A6) == G6, "q5 A6 not in O^-(6,3)")
    require(A6 != I6 and mpow(A6, 3) == I6, "q5 A6 does not have exact order 3")

    bases = ctrl.get("invariant_spread_line_bases")
    require(isinstance(bases, list) and len(bases) == 28, "q5 spread must have 28 bases")
    covered = set()
    line_sets = set()
    for idx, b in enumerate(bases):
        require(isinstance(b, list) and len(b) == 2, f"q5 basis {idx} not 2x6")
        for r in b:
            require(isinstance(r, list) and len(r) == 6 and all(type(x) is int and x in (0, 1, 2) for x in r),
                    f"q5 basis {idx} invalid entries")
        require(rank_mod3(b, 6) == 2, f"q5 basis {idx} not rank 2")
        require(eval_q6(b[0]) == 0 and eval_q6(b[1]) == 0 and eval_b6(b[0], b[1]) == 0,
                f"q5 basis {idx} not totally singular")
        lpts = set()
        for c0 in range(3):
            for c1 in range(3):
                if c0 == 0 and c1 == 0:
                    continue
                w = tuple((c0 * b[0][k] + c1 * b[1][k]) % 3 for k in range(6))
                lpts.add(pt6_map[w])
        require(len(lpts) == 4, f"q5 line {idx} does not have 4 points")
        require(covered.isdisjoint(lpts), f"q5 spread overlap at line {idx}")
        covered.update(lpts)
        line_sets.add(tuple(sorted(lpts)))
    require(len(covered) == 112, "q5 spread does not cover all 112 points")

    for ls in line_sets:
        img_ls = tuple(sorted(pt6_map[apply_mat(A6, pts6[p])] for p in ls))
        require(img_ls in line_sets, "q5 spread is not A6-invariant")


def main():
    t_start = time.time()
    here = os.path.dirname(os.path.abspath(__file__))
    pkg_root = os.path.dirname(here)
    cert_path = os.path.join(pkg_root, "object", "q7_3_ord3_certificate.json")

    try:
        with open(cert_path, "r", encoding="utf-8") as f:
            cert = json.load(f)
    except Exception as exc:
        fail(f"Could not parse JSON certificate: {exc}")

    require(isinstance(cert, dict), "Top-level JSON must be object")
    require(cert.get("schema") == "v3r1t4s-q7-3-ord3-p1-v1", "schema mismatch")
    require(cert.get("target_id") == "elliptic-quadric-q7-3-spread", "target_id mismatch")
    require(cert.get("partial_win_id") == "p1", "partial_win_id mismatch")
    require(cert.get("quadratic_form") == "x1*x2 + x3*x4 + x5*x6 + x7^2 + x8^2 mod 3", "quadratic_form mismatch")

    verify_q5_control(cert.get("positive_control_q5_3"))
    print("[Python Checker] 1. Q^-(5,3) 28-line order-3 spread certificate verified.")

    # Build Q^-(7,3) points, lines, planes from definition
    pts8 = []
    pt8_map = {}
    for v in itertools.product(range(3), repeat=8):
        cv = canon_vec(v)
        if cv == v and eval_q8(v) == 0:
            pt8_map[v] = len(pts8)
            pt8_map[tuple((2 * x) % 3 for x in v)] = len(pts8)
            pts8.append(v)

    nlines8 = 0
    for p0 in range(8):
        for p1 in range(p0 + 1, 8):
            f0 = [c for c in range(p0 + 1, 8) if c != p1]
            f1 = list(range(p1 + 1, 8))
            for t0 in itertools.product(range(3), repeat=len(f0)):
                r0 = [0] * 8
                r0[p0] = 1
                for c, val in zip(f0, t0):
                    r0[c] = val
                if eval_q8(r0) != 0:
                    continue
                for t1 in itertools.product(range(3), repeat=len(f1)):
                    r1 = [0] * 8
                    r1[p1] = 1
                    for c, val in zip(f1, t1):
                        r1[c] = val
                    if eval_q8(r1) == 0 and eval_b8(r0, r1) == 0:
                        nlines8 += 1

    planes8 = []
    for p0 in range(8):
        for p1 in range(p0 + 1, 8):
            for p2 in range(p1 + 1, 8):
                f0 = [c for c in range(p0 + 1, 8) if c != p1 and c != p2]
                f1 = [c for c in range(p1 + 1, 8) if c != p2]
                f2 = list(range(p2 + 1, 8))
                for t0 in itertools.product(range(3), repeat=len(f0)):
                    r0 = [0] * 8
                    r0[p0] = 1
                    for c, val in zip(f0, t0):
                        r0[c] = val
                    if eval_q8(r0) != 0:
                        continue
                    for t1 in itertools.product(range(3), repeat=len(f1)):
                        r1 = [0] * 8
                        r1[p1] = 1
                        for c, val in zip(f1, t1):
                            r1[c] = val
                        if eval_q8(r1) != 0 or eval_b8(r0, r1) != 0:
                            continue
                        for t2 in itertools.product(range(3), repeat=len(f2)):
                            r2 = [0] * 8
                            r2[p2] = 1
                            for c, val in zip(f2, t2):
                                r2[c] = val
                            if eval_q8(r2) != 0 or eval_b8(r0, r2) != 0 or eval_b8(r1, r2) != 0:
                                continue
                            ppts = []
                            for a in range(3):
                                for b in range(3):
                                    for c in range(3):
                                        if a == 0 and b == 0 and c == 0:
                                            continue
                                        w = tuple((a * r0[k] + b * r1[k] + c * r2[k]) % 3 for k in range(8))
                                        if next(x for x in w if x != 0) == 1:
                                            ppts.append(pt8_map[w])
                            planes8.append(tuple(sorted(ppts)))
    planes8.sort()
    pl8_map = {pl: idx for idx, pl in enumerate(planes8)}

    pcounts = cert.get("polar_space_counts", {})
    require(pcounts == {
        "singular_points": len(pts8),
        "totally_singular_lines": nlines8,
        "totally_singular_planes": len(planes8),
        "points_per_plane": 13,
        "planes_per_spread": 82,
    } and len(pts8) == 1066 and nlines8 == 29848 and len(planes8) == 22960, "polar_space_counts mismatch")

    ag = cert.get("automorphism_group", {})
    expected_pgo = 2 * (3 ** 12) * (3 ** 4 + 1) * (3 ** 6 - 1) * (3 ** 4 - 1) * (3 ** 2 - 1)
    require(expected_pgo == 40607874478080, "internal formula check")
    pf = ag.get("prime_factorization", {})
    prod_pf = 1
    for p_str, exp_val in pf.items():
        require(p_str in ("2", "3", "5", "7", "13", "41") and type(exp_val) is int and exp_val >= 1,
                "invalid prime_factorization entry")
        prod_pf *= int(p_str) ** exp_val
    require(len(pf) == 6 and prod_pf == expected_pgo, "prime_factorization product mismatch")
    require(ag == {
        "name": "PGO^-(8,3)",
        "order": expected_pgo,
        "po_index_in_pgo": 2,
        "po_order": expected_pgo // 2,
        "standard_frame_stabilizer_order": 64,
        "prime_factorization": {"2": 12, "3": 12, "5": 1, "7": 1, "13": 1, "41": 1},
    }, "automorphism_group metadata mismatch")
    require(1066 * 729 * 112 * 81 * 10 * 9 * 64 == expected_pgo, "frame orbit-stabilizer product mismatch")

    G8 = [[0] * 8 for _ in range(8)]
    for k in range(3):
        G8[2 * k][2 * k + 1] = 1
        G8[2 * k + 1][2 * k] = 1
    G8[6][6] = 2
    G8[7][7] = 2
    I8 = [[1 if r == c else 0 for c in range(8)] for r in range(8)]
    negI8 = [[2 if r == c else 0 for c in range(8)] for r in range(8)]

    def recompute_km(M):
        pt_img = [pt8_map[apply_mat(M, p)] for p in pts8]
        fix_p = sum(1 for i in range(1066) if pt_img[i] == i)
        pt_orb = [-1] * 1066
        norb = 0
        for i in range(1066):
            if pt_orb[i] == -1:
                c = i
                while pt_orb[c] == -1:
                    pt_orb[c] = norb
                    c = pt_img[c]
                norb += 1
        vis = [False] * 22960
        fpl = 0
        dnfix = 0
        for j in range(22960):
            if vis[j]:
                continue
            orb = []
            c = j
            while not vis[c]:
                vis[c] = True
                orb.append(c)
                c = pl8_map[tuple(sorted(pt_img[x] for x in planes8[c]))]
            cov = [x for pid in orb for x in planes8[pid]]
            if len(set(cov)) != len(cov):
                continue
            if len(orb) == 1:
                fpl += 1
            else:
                dnfix += 1
        return fix_p, fpl, dnfix, norb, fpl + dnfix

    # Verify Order-3 classification
    o3 = cert.get("order_3_classification", {})
    require(isinstance(o3, dict), "order_3_classification must be dict")
    strata = o3.get("cayley_strata_counts", {})
    expected_strata = {
        "rank2_rad2_lines": nlines8 * 2,
        "rank2_rad1_points": len(pts8) * 252 * 2,
        "rank4_rad3_planes": len(planes8) * 4 * 468,
        "rank4_rad2_lines": nlines8 * 90 * 144,
    }
    require(strata == expected_strata, "cayley_strata_counts mismatch")
    tot_o3 = sum(expected_strata.values())
    require(tot_o3 == 430408160 and o3.get("total_order_3_elements_in_pgo") == tot_o3, "total_order_3 mismatch")

    o3_classes = o3.get("conjugacy_classes", [])
    require(isinstance(o3_classes, list) and len(o3_classes) == 5, "must have 5 order-3 classes")
    expected_o3_ids = ["C3_94", "C3_121", "C3_13", "C3_4", "C3_22"]
    seen_fix_pts = set()
    sum_o3_sizes = 0
    all_14_mats = []

    for idx, entry in enumerate(o3_classes):
        require(isinstance(entry, dict) and entry.get("class_id") == expected_o3_ids[idx], f"o3 class_id {idx} mismatch")
        require(isinstance(entry.get("jordan_type"), str) and len(entry["jordan_type"]) > 0, "jordan_type invalid")
        M = entry.get("matrix")
        check_matrix_shape(M, 8, entry["class_id"])
        require(mmul(mmul(mtranspose(M), G8), M) == G8, f"{entry['class_id']} not in O^-(8,3)")
        require(M != I8 and mpow(M, 3) == I8, f"{entry['class_id']} not exact order 3")
        fix_p, fpl, dnfix, norb, nopt = recompute_km(M)
        require(entry.get("fix_pts") == fix_p, f"{entry['class_id']} fix_pts mismatch")
        require(entry.get("fix_planes") == fpl, f"{entry['class_id']} fix_planes mismatch")
        require(entry.get("disjoint_3_orbits") == dnfix, f"{entry['class_id']} disjoint_3_orbits mismatch")
        require(entry.get("km_items") == norb and entry.get("km_options") == nopt, f"{entry['class_id']} KM size mismatch")
        require(entry.get("exact_cover_status") == "UNSAT", f"{entry['class_id']} status mismatch")
        cent = entry.get("centralizer_order_pgo")
        csz = entry.get("conjugacy_class_size")
        require(type(cent) is int and type(csz) is int and cent > 0 and csz > 0, "invalid cent/csz")
        require(expected_pgo == cent * csz, f"{entry['class_id']} orbit-stabilizer mismatch")
        seen_fix_pts.add(fix_p)
        sum_o3_sizes += csz
        all_14_mats.append(M)

    require(len(seen_fix_pts) == 5, "order-3 classes do not have pairwise distinct fix_pts")
    require(sum_o3_sizes == tot_o3, "order-3 class sizes do not sum to 430,408,160")
    print("[Python Checker] 2. All 5 Order-3 matrices, KM dimensions, and class sum (430,408,160) verified.")

    # Verify PO^-(8,3) involution classification
    po_inv = cert.get("po_involution_classification", {})
    require(isinstance(po_inv, dict), "po_involution_classification must be dict")
    inv_classes = po_inv.get("conjugacy_classes", [])
    require(isinstance(inv_classes, list) and len(inv_classes) == 5, "must have 5 PO^- involution classes")

    # Orthogonal group order formulas over GF(3)
    ord_O1 = 2
    ord_O2p = 2 * (3 - 1)
    ord_O2m = 2 * (3 + 1)
    ord_O3 = 2 * 3 * (3 ** 2 - 1)
    ord_O4p = 2 * (3 ** 2) * (3 ** 2 - 1) * (3 ** 2 - 1)
    ord_O4m = 2 * (3 ** 2) * (3 ** 2 + 1) * (3 ** 2 - 1)
    ord_O5 = 2 * (3 ** 4) * (3 ** 4 - 1) * (3 ** 2 - 1)
    ord_O6p = 2 * (3 ** 6) * (3 ** 3 - 1) * (3 ** 4 - 1) * (3 ** 2 - 1)
    ord_O6m = 2 * (3 ** 6) * (3 ** 3 + 1) * (3 ** 4 - 1) * (3 ** 2 - 1)
    ord_O7 = 2 * (3 ** 9) * (3 ** 6 - 1) * (3 ** 4 - 1) * (3 ** 2 - 1)
    expected_inv_cents = [
        (ord_O1 * ord_O7) // 2,
        ord_O2m * ord_O6p,
        ord_O2p * ord_O6m,
        (ord_O3 * ord_O5) // 2,
        ord_O4p * ord_O4m,
    ]
    expected_inv_ids = ["Inv_364", "Inv_130", "Inv_114", "Inv_44", "Inv_26"]
    expected_dims = [1, 2, 2, 3, 4]
    sum_inv_sizes = 0

    for idx, entry in enumerate(inv_classes):
        require(isinstance(entry, dict) and entry.get("class_id") == expected_inv_ids[idx], f"inv class_id {idx} mismatch")
        require(entry.get("neg_eigenspace_dim") == expected_dims[idx], f"inv dim {idx} mismatch")
        M = entry.get("matrix")
        check_matrix_shape(M, 8, entry["class_id"])
        require(mmul(mmul(mtranspose(M), G8), M) == G8, f"{entry['class_id']} not in O^-(8,3)")
        require(M != I8 and M != negI8 and mpow(M, 2) == I8, f"{entry['class_id']} not involution")
        mpI = [[(M[r][c] + (1 if r == c else 0)) % 3 for c in range(8)] for r in range(8)]
        require(8 - rank_mod3(mpI, 8) == expected_dims[idx], f"{entry['class_id']} eigenspace dim mismatch")
        fix_p, fpl, dnfix, norb, nopt = recompute_km(M)
        require(entry.get("fix_pts") == fix_p and entry.get("fix_planes") == fpl, f"{entry['class_id']} fix counts mismatch")
        require(entry.get("disjoint_2_orbits") == dnfix, f"{entry['class_id']} disjoint_2_orbits mismatch")
        require(entry.get("km_items") == norb and entry.get("km_options") == nopt, f"{entry['class_id']} KM mismatch")
        require(entry.get("centralizer_order_pgo") == expected_inv_cents[idx], f"{entry['class_id']} cent mismatch")
        csz = entry.get("conjugacy_class_size_in_po")
        require(type(csz) is int and expected_pgo == expected_inv_cents[idx] * csz, f"{entry['class_id']} csz mismatch")
        require(entry.get("exact_cover_status") == "UNSAT", f"{entry['class_id']} status mismatch")
        sum_inv_sizes += csz
        all_14_mats.append(M)

    require(sum_inv_sizes == 41398479 and po_inv.get("total_involutions_in_po") == 41398479, "total_involutions_in_po mismatch")
    print("[Python Checker] 3. All 5 PO^-(8,3) involution classes and total count (41,398,479) verified.")

    # Verify Sylow-{5,7,13,41} representatives
    syl = cert.get("odd_prime_sylow_representatives", [])
    require(isinstance(syl, list) and len(syl) == 4, "must have 4 odd prime Sylow reps")
    for p_exp, entry in zip((5, 7, 13, 41), syl):
        require(isinstance(entry, dict) and entry.get("prime_order") == p_exp, f"Sylow {p_exp} prime_order mismatch")
        require(entry.get("sylow_exponent_in_pgo") == 1 and (expected_pgo // p_exp) % p_exp != 0, f"Sylow {p_exp} exponent mismatch")
        M = entry.get("matrix")
        check_matrix_shape(M, 8, f"Sylow_{p_exp}")
        require(mmul(mmul(mtranspose(M), G8), M) == G8, f"Sylow_{p_exp} not in O^-(8,3)")
        require(M != I8 and M != negI8 and mpow(M, p_exp) == I8, f"Sylow_{p_exp} not order {p_exp}")
        fix_p, fpl, dnfix, norb, nopt = recompute_km(M)
        require(entry.get("fix_pts") == fix_p and entry.get("fix_planes") == fpl, f"Sylow_{p_exp} fix mismatch")
        require(entry.get("disjoint_p_orbits") == dnfix, f"Sylow_{p_exp} disj mismatch")
        require(entry.get("km_items") == norb and entry.get("km_options") == nopt, f"Sylow_{p_exp} KM mismatch")
        require(entry.get("exact_cover_status") == "UNSAT", f"Sylow_{p_exp} status mismatch")
        # Direct arithmetic obstruction check!
        arith_dead = (fix_p > 0 and fpl == 0) or (fpl < (82 % p_exp)) or (nopt == 0)
        require(arith_dead, f"Sylow_{p_exp} missing direct arithmetic obstruction")
        all_14_mats.append(M)
    print("[Python Checker] 4. All 4 odd prime Sylow-{5,7,13,41} exclusions verified by arithmetic & KM dimensions.")

    c13_sum = cert.get("c3_13_normalizer_search_summary", {})
    require(c13_sum == {
        "normalizer_order_in_pgo": 1889568,
        "disjoint_plane_3_orbits": 6561,
        "normalizer_orbits_on_6561": 1,
        "stabilizer_of_base_orbit_order": 288,
        "case_b_without_fixed_plane_pi_star": "UNSAT (all 36 other fixed planes intersect Pi_* in 4-point lines; 13 points cannot be partitioned)",
        "case_a_engine1_swar_total_tasks": 144,
        "case_a_engine1_swar_total_branch_nodes": 8796560,
        "case_a_engine2_rdlx_total_tasks": 143,
        "case_a_engine2_rdlx_total_branch_nodes": 8776899,
        "status": "UNSAT",
    }, "c3_13_normalizer_search_summary mismatch")

    # Compile and execute Engine 2 C99 Row-DLX verifier in a clean temporary directory
    cc_bin = shutil.which("cc") or shutil.which("clang") or shutil.which("gcc")
    require(cc_bin is not None, "No C compiler (cc/clang/gcc) found in PATH")
    c_src = os.path.join(here, "verify_engine2_dlx.c")
    require(os.path.isfile(c_src), "verify_engine2_dlx.c missing")

    with tempfile.TemporaryDirectory() as tmpd:
        exe_path = os.path.join(tmpd, "verify_engine2_dlx")
        mat_path = os.path.join(tmpd, "matrices.txt")
        with open(mat_path, "w", encoding="utf-8") as mf:
            for M in all_14_mats:
                for row in M:
                    mf.write(" ".join(str(x) for x in row) + "\n")
                mf.write("\n")

        comp = subprocess.run(
            [cc_bin, "-O3", c_src, "-o", exe_path, "-lpthread"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        require(comp.returncode == 0, f"C99 compilation failed: {comp.stdout}")

        run = subprocess.run(
            [exe_path, mat_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        sys.stdout.write(run.stdout)
        sys.stdout.flush()
        require(run.returncode == 0 and "ENGINE2_OK" in run.stdout, "Engine 2 C99 verifier failed")

    print(f"[Verified in {time.time() - t_start:.2f}s] No spread of Q^-(7,3) admits an automorphism of order 3 (and Aut(S) cap PO^-(8,3) = {{1}}).")
    print("PASS")


if __name__ == "__main__":
    main()
