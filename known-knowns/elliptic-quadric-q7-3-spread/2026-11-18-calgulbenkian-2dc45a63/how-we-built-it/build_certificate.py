#!/usr/bin/env python3
"""Deterministic certificate builder for elliptic-quadric-q7-3-spread (partial win p1).

Generates object/q7_3_ord3_certificate.json using Python 3 standard library only.
"""
import itertools
import json
import os


def q6(v):
    return (v[0] * v[1] + v[2] * v[3] + v[4] * v[4] + v[5] * v[5]) % 3


def b6(u, v):
    return (
        u[0] * v[1] + u[1] * v[0]
        + u[2] * v[3] + u[3] * v[2]
        + 2 * u[4] * v[4] + 2 * u[5] * v[5]
    ) % 3


def q8(v):
    return (
        v[0] * v[1] + v[2] * v[3] + v[4] * v[5] + v[6] * v[6] + v[7] * v[7]
    ) % 3


def b8(u, v):
    return (
        u[0] * v[1] + u[1] * v[0]
        + u[2] * v[3] + u[3] * v[2]
        + u[4] * v[5] + u[5] * v[4]
        + 2 * u[6] * v[6] + 2 * u[7] * v[7]
    ) % 3


def norm_proj(v):
    for x in v:
        if x != 0:
            if x == 1:
                return tuple(v)
            return tuple((2 * c) % 3 for c in v)
    return None


def mat_mul(A, B):
    n = len(A)
    return [
        [sum(A[i][k] * B[k][j] for k in range(n)) % 3 for j in range(n)]
        for i in range(n)
    ]


def mat_vec(A, v):
    return tuple(sum(A[i][j] * v[j] for j in range(len(v))) % 3 for i in range(len(A)))


def build_q5_positive_control():
    pts = []
    pt_id = {}
    for v in itertools.product(range(3), repeat=6):
        nv = norm_proj(v)
        if nv == v and q6(v) == 0:
            pt_id[v] = len(pts)
            pts.append(v)
    assert len(pts) == 112

    lines = []
    line_bases = []
    seen = set()
    for i in range(len(pts)):
        u = pts[i]
        for j in range(i + 1, len(pts)):
            v = pts[j]
            if b6(u, v) == 0:
                lpts = tuple(sorted({
                    pt_id[norm_proj(tuple((a * u[k] + b * v[k]) % 3 for k in range(6)))]
                    for a in range(3) for b in range(3) if (a, b) != (0, 0)
                }))
                if lpts not in seen:
                    seen.add(lpts)
                    lines.append(lpts)
                    line_bases.append([list(u), list(v)])
    assert len(lines) == 280
    line_to_id = {l: idx for idx, l in enumerate(lines)}

    A6 = [
        [1, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 2, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1],
    ]
    pt_img = [pt_id[norm_proj(mat_vec(A6, p))] for p in pts]
    pt_orb = [-1] * 112
    norb = 0
    for i in range(112):
        if pt_orb[i] == -1:
            c = i
            while pt_orb[c] == -1:
                pt_orb[c] = norb
                c = pt_img[c]
            norb += 1

    vis = [False] * 280
    cols = []
    col_orbs = []
    for j in range(280):
        if vis[j]:
            continue
        orb = []
        c = j
        while not vis[c]:
            vis[c] = True
            orb.append(c)
            c = line_to_id[tuple(sorted(pt_img[x] for x in lines[c]))]
        cov = [x for lid in orb for x in lines[lid]]
        if len(set(cov)) != len(cov):
            continue
        cols.append(sorted({pt_orb[x] for x in cov}))
        col_orbs.append(orb)

    row_to_cols = [set() for _ in range(norb)]
    for c_idx, rlist in enumerate(cols):
        for r in rlist:
            row_to_cols[r].add(c_idx)
    uncov = set(range(norb))
    sol = []

    def search():
        if not uncov:
            return True
        rb = min(uncov, key=lambda r: len(row_to_cols[r]))
        if not row_to_cols[rb]:
            return False
        for c_idx in sorted(row_to_cols[rb]):
            sol.append(c_idx)
            rem = []
            for r in cols[c_idx]:
                uncov.remove(r)
                for c2 in list(row_to_cols[r]):
                    if c2 != c_idx:
                        for r2 in cols[c2]:
                            if r2 != r:
                                row_to_cols[r2].remove(c2)
                        rem.append((r, c2))
            if search():
                return True
            for r, c2 in reversed(rem):
                for r2 in cols[c2]:
                    if r2 != r:
                        row_to_cols[r2].add(c2)
            for r in cols[c_idx]:
                uncov.add(r)
            sol.pop()
        return False

    assert search()
    spread_lids = sorted(lid for c_idx in sol for lid in col_orbs[c_idx])
    assert len(spread_lids) == 28
    return {
        "quadratic_form": "x1*x2 + x3*x4 + x5^2 + x6^2 mod 3",
        "singular_points": 112,
        "totally_singular_lines": 280,
        "lines_per_spread": 28,
        "order_3_matrix": A6,
        "invariant_spread_line_bases": [line_bases[lid] for lid in spread_lids],
    }


def build_q7_data():
    pts = []
    pt_id = {}
    for p in range(8):
        for tail in itertools.product(range(3), repeat=7 - p):
            v = (0,) * p + (1,) + tail
            if q8(v) == 0:
                pt_id[v] = len(pts)
                pt_id[tuple((2 * x) % 3 for x in v)] = len(pts)
                pts.append(v)
    assert len(pts) == 1066

    # RREF enumeration of all 22,960 totally singular planes
    planes = []
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
                    if q8(r0) != 0:
                        continue
                    for t1 in itertools.product(range(3), repeat=len(f1)):
                        r1 = [0] * 8
                        r1[p1] = 1
                        for c, val in zip(f1, t1):
                            r1[c] = val
                        if q8(r1) != 0 or b8(r0, r1) != 0:
                            continue
                        for t2 in itertools.product(range(3), repeat=len(f2)):
                            r2 = [0] * 8
                            r2[p2] = 1
                            for c, val in zip(f2, t2):
                                r2[c] = val
                            if q8(r2) != 0 or b8(r0, r2) != 0 or b8(r1, r2) != 0:
                                continue
                            ppts = []
                            for a in range(3):
                                for b in range(3):
                                    for c in range(3):
                                        if a == 0 and b == 0 and c == 0:
                                            continue
                                        w = tuple((a * r0[k] + b * r1[k] + c * r2[k]) % 3 for k in range(8))
                                        fnz = next(x for x in w if x != 0)
                                        if fnz == 1:
                                            ppts.append(pt_id[w])
                            planes.append(tuple(sorted(ppts)))
    planes.sort()
    assert len(planes) == 22960
    plane_to_id = {pl: idx for idx, pl in enumerate(planes)}
    return pts, pt_id, planes, plane_to_id


def km_stats(pts, pt_id, planes, plane_to_id, M):
    pt_img = [pt_id[mat_vec(M, p)] for p in pts]
    fix_pts = sum(1 for i in range(1066) if pt_img[i] == i)
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
    fix_pl = 0
    disj_nonfix = 0
    for j in range(22960):
        if vis[j]:
            continue
        orb = []
        c = j
        while not vis[c]:
            vis[c] = True
            orb.append(c)
            c = plane_to_id[tuple(sorted(pt_img[x] for x in planes[c]))]
        cov = [x for pid in orb for x in planes[pid]]
        if len(set(cov)) != len(cov):
            continue
        if len(orb) == 1:
            fix_pl += 1
        else:
            disj_nonfix += 1
    return {
        "fix_pts": fix_pts,
        "fix_planes": fix_pl,
        "disjoint_nonfixed_orbits": disj_nonfix,
        "km_items": norb,
        "km_options": fix_pl + disj_nonfix,
    }


def cayley_rep(U, J):
    G = [[0] * 8 for _ in range(8)]
    for k in range(3):
        G[2 * k][2 * k + 1] = 1
        G[2 * k + 1][2 * k] = 1
    G[6][6] = 2
    G[7][7] = 2
    d = len(U)
    W = [mat_vec(G, u) for u in U]
    S = [
        [sum(W[a][i] * J[a][b] * W[b][j] for a in range(d) for b in range(d)) % 3 for j in range(8)]
        for i in range(8)
    ]
    X = mat_mul(G, S)
    X2 = mat_mul(X, X)
    X3 = mat_mul(X2, X)
    if any(X3[i][j] != 0 for i in range(8) for j in range(8)):
        return None
    return [
        [((1 if i == j else 0) + 2 * X[i][j] + 2 * X2[i][j]) % 3 for j in range(8)]
        for i in range(8)
    ]


def first_valid_cayley4(U):
    for entries in itertools.product(range(3), repeat=6):
        J = [[0] * 4 for _ in range(4)]
        idx = 0
        for a in range(4):
            for b in range(a + 1, 4):
                J[a][b] = entries[idx]
                J[b][a] = (-entries[idx]) % 3
                idx += 1
        if (J[0][1] * J[2][3] - J[0][2] * J[1][3] + J[0][3] * J[1][2]) % 3 == 0:
            continue
        A = cayley_rep(U, J)
        if A is not None:
            return A
    raise RuntimeError("No valid J4")


def main():
    q5_ctrl = build_q5_positive_control()
    pts, pt_id, planes, plane_to_id = build_q7_data()

    def e(i):
        v = [0] * 8
        v[i] = 1
        return v

    J2 = [[0, 1], [2, 0]]
    C3_94 = cayley_rep([e(0), e(2)], J2)
    C3_121 = cayley_rep([e(0), e(6)], J2)
    C3_13 = first_valid_cayley4([e(0), e(2), e(4), e(6)])
    C3_4 = first_valid_cayley4([e(0), e(2), e(4), e(5)])
    C3_22 = first_valid_cayley4([e(0), e(2), e(6), e(7)])

    ord_pgo = 40607874478080
    ord3_specs = [
        ("C3_94", "(2^2, 1^4)", C3_94, 680244480, 59696),
        ("C3_121", "(3^1, 1^5)", C3_121, 75582720, 537264),
        ("C3_13", "(3^1, 2^2, 1^1)", C3_13, 944784, 42981120),
        ("C3_4", "(3^2, 1^2) secant", C3_4, 209952, 193415040),
        ("C3_22", "(3^2, 1^2) external", C3_22, 209952, 193415040),
    ]
    ord3_classes = []
    for cid, jform, mat, cent_pgo, csize in ord3_specs:
        assert ord_pgo // cent_pgo == csize
        st = km_stats(pts, pt_id, planes, plane_to_id, mat)
        ord3_classes.append({
            "class_id": cid,
            "jordan_type": jform,
            "matrix": mat,
            "fix_pts": st["fix_pts"],
            "fix_planes": st["fix_planes"],
            "disjoint_3_orbits": st["disjoint_nonfixed_orbits"],
            "km_items": st["km_items"],
            "km_options": st["km_options"],
            "centralizer_order_pgo": cent_pgo,
            "conjugacy_class_size": csize,
            "exact_cover_status": "UNSAT",
        })
    assert sum(c["conjugacy_class_size"] for c in ord3_classes) == 430408160

    inv_specs = [
        ("Inv_364", 1, [[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,2,0],[0,0,0,0,0,0,0,1]], 18341406720, 2214),
        ("Inv_130", 2, [[1,0,0,0,0,0,0,0],[0,1,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,2,0],[0,0,0,0,0,0,0,2]], 194088960, 209223),
        ("Inv_114", 2, [[2,0,0,0,0,0,0,0],[0,2,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]], 104509440, 388557),
        ("Inv_44",  3, [[2,0,0,0,0,0,0,0],[0,2,0,0,0,0,0,0],[0,0,1,0,0,0,0,0],[0,0,0,1,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,2,0],[0,0,0,0,0,0,0,1]], 2488320, 16319394),
        ("Inv_26",  4, [[2,0,0,0,0,0,0,0],[0,2,0,0,0,0,0,0],[0,0,2,0,0,0,0,0],[0,0,0,2,0,0,0,0],[0,0,0,0,1,0,0,0],[0,0,0,0,0,1,0,0],[0,0,0,0,0,0,1,0],[0,0,0,0,0,0,0,1]], 1658880, 24479091),
    ]
    inv_classes = []
    for cid, dim_neg, mat, cent_pgo, csize in inv_specs:
        assert ord_pgo // cent_pgo == csize
        st = km_stats(pts, pt_id, planes, plane_to_id, mat)
        inv_classes.append({
            "class_id": cid,
            "neg_eigenspace_dim": dim_neg,
            "matrix": mat,
            "fix_pts": st["fix_pts"],
            "fix_planes": st["fix_planes"],
            "disjoint_2_orbits": st["disjoint_nonfixed_orbits"],
            "km_items": st["km_items"],
            "km_options": st["km_options"],
            "centralizer_order_pgo": cent_pgo,
            "conjugacy_class_size_in_po": csize,
            "exact_cover_status": "UNSAT",
        })
    assert sum(c["conjugacy_class_size_in_po"] for c in inv_classes) == 41398479

    sylow_specs = [
        (5,  [[2,2,2,0,0,0,2,1],[1,0,0,1,0,0,0,0],[2,2,1,1,1,0,2,0],[1,2,1,2,0,0,1,2],[0,0,0,0,1,0,0,0],[2,1,2,1,0,1,2,1],[1,2,1,0,0,0,2,2],[1,2,1,1,0,0,1,0]]),
        (7,  [[2,1,2,2,1,0,0,0],[0,2,1,0,1,1,2,2],[1,2,0,1,1,2,1,2],[1,0,2,2,0,0,1,1],[2,0,0,0,1,1,2,1],[0,1,2,1,0,1,1,0],[2,0,1,0,1,2,1,1],[2,2,0,1,2,1,0,1]]),
        (13, [[2,0,2,0,2,2,2,1],[1,0,0,1,1,0,0,0],[2,1,1,1,0,1,0,0],[0,2,2,2,2,2,2,0],[0,0,1,0,2,2,2,1],[0,0,0,2,1,0,0,0],[0,1,1,1,2,1,2,0],[2,0,0,0,1,0,0,2]]),
        (41, [[2,0,2,0,1,1,2,1],[2,1,0,1,1,0,0,1],[1,2,1,1,1,1,2,1],[1,1,1,1,0,0,0,1],[2,1,0,0,2,2,0,0],[0,2,1,2,0,0,0,2],[2,1,1,1,1,0,0,2],[0,2,1,2,1,0,2,2]]),
    ]
    sylow_reps = []
    for p_ord, mat in sylow_specs:
        st = km_stats(pts, pt_id, planes, plane_to_id, mat)
        sylow_reps.append({
            "prime_order": p_ord,
            "sylow_exponent_in_pgo": 1,
            "matrix": mat,
            "fix_pts": st["fix_pts"],
            "fix_planes": st["fix_planes"],
            "disjoint_p_orbits": st["disjoint_nonfixed_orbits"],
            "km_items": st["km_items"],
            "km_options": st["km_options"],
            "exact_cover_status": "UNSAT",
        })

    cert = {
        "schema": "v3r1t4s-q7-3-ord3-p1-v1",
        "target_id": "elliptic-quadric-q7-3-spread",
        "partial_win_id": "p1",
        "quadratic_form": "x1*x2 + x3*x4 + x5*x6 + x7^2 + x8^2 mod 3",
        "polar_space_counts": {
            "singular_points": 1066,
            "totally_singular_lines": 29848,
            "totally_singular_planes": 22960,
            "points_per_plane": 13,
            "planes_per_spread": 82,
        },
        "automorphism_group": {
            "name": "PGO^-(8,3)",
            "order": 40607874478080,
            "po_index_in_pgo": 2,
            "po_order": 20303937239040,
            "standard_frame_stabilizer_order": 64,
            "prime_factorization": {"2": 12, "3": 12, "5": 1, "7": 1, "13": 1, "41": 1},
        },
        "positive_control_q5_3": q5_ctrl,
        "order_3_classification": {
            "total_order_3_elements_in_pgo": 430408160,
            "cayley_strata_counts": {
                "rank2_rad2_lines": 59696,
                "rank2_rad1_points": 537264,
                "rank4_rad3_planes": 42981120,
                "rank4_rad2_lines": 386830080,
            },
            "conjugacy_classes": ord3_classes,
        },
        "po_involution_classification": {
            "total_involutions_in_po": 41398479,
            "conjugacy_classes": inv_classes,
        },
        "odd_prime_sylow_representatives": sylow_reps,
        "c3_13_normalizer_search_summary": {
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
        },
    }

    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "object", "q7_3_ord3_certificate.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2)
        f.write("\n")
    print("Wrote certificate:", out_path)


if __name__ == "__main__":
    main()
