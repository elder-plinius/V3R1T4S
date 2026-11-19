#!/usr/bin/env python3
"""
Exact Subspace Homomorphism Substitution (Q -> Z / ZT),
Equivariant GL(Z) Gauge Elimination, and Inverse-Distributivity Unfolding.
"""
import glob
import itertools
import json
import os
import re
import sys
from fractions import Fraction

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))
from verify_z_brent import load_reference_bounds, verify_scheme


def load_mpl_raw(path, m, n, p):
    txt = open(path, "r", encoding="utf-8").read()
    triads = re.findall(
        r"Triad\(\[Matrix\(\d+, \d+, (\[\[.*?\]\])\), Matrix\(\d+, \d+, (\[\[.*?\]\])\), Matrix\(\d+, \d+, (\[\[.*?\]\])\)\]\)",
        txt,
    )
    U, V, W = [], [], []
    for u_str, v_str, w_str in triads:
        u_mat = eval(re.sub(r"(-?\d+)/(\d+)", r"Fraction(\1,\2)", u_str))
        v_mat = eval(re.sub(r"(-?\d+)/(\d+)", r"Fraction(\1,\2)", v_str))
        w_mat = eval(re.sub(r"(-?\d+)/(\d+)", r"Fraction(\1,\2)", w_str))
        U.append([Fraction(u_mat[i][j]) for i in range(m) for j in range(n)])
        V.append([Fraction(v_mat[j][k]) for j in range(n) for k in range(p)])
        W.append([Fraction(w_mat[k][i]) for k in range(p) for i in range(m)])
    return [U, V, W]


def solve_linear_map(A0, B):
    R, d, D = len(A0), len(A0[0]), len(B[0])
    if len(B) != R:
        return None
    aug = [list(A0[r]) + list(B[r]) for r in range(R)]
    row = 0
    for col in range(d):
        piv = next((r for r in range(row, R) if aug[r][col] != 0), None)
        if piv is None:
            return None
        aug[row], aug[piv] = aug[piv], aug[row]
        pv = aug[row][col]
        aug[row] = [x / pv for x in aug[row]]
        for r in range(R):
            if r != row and aug[r][col] != 0:
                f = aug[r][col]
                aug[r] = [aug[r][c] - f * aug[row][c] for c in range(d + D)]
        row += 1
    if any(aug[r][d + c] != 0 for r in range(d, R) for c in range(D)):
        return None
    P = [[aug[r][d + c] for c in range(D)] for r in range(d)]
    if any(x.denominator != 1 for row_p in P for x in row_p):
        return None
    return [[int(x) for x in row_p] for row_p in P]


def matmul_int(A, P):
    R_new, d, D = len(A), len(A[0]), len(P[0])
    out = [[0] * D for _ in range(R_new)]
    for r in range(R_new):
        for k in range(d):
            a = A[r][k]
            if a != 0:
                pk = P[k]
                out_r = out[r]
                for c in range(D):
                    if pk[c] != 0:
                        out_r[c] += a * pk[c]
    return out


def optimize_block(PU0, PV0, PW0, zt0, zt1, zt2, m0, n0, p0):
    DU, DV, DW = len(PU0[0]), len(PV0[0]), len(PW0[0])
    best_pu, best_pv, best_pw = PU0, PV0, PW0

    def score(pu, pv, pw):
        uo = matmul_int(zt0, pu)
        vo = matmul_int(zt1, pv)
        wo = matmul_int(zt2, pw)
        bad_terms = sum(
            1 for r in range(len(uo)) if any(abs(x) > 1 for x in uo[r] + vo[r] + wo[r])
        )
        bad_entries = sum(
            abs(x) - 1
            for mat in (uo, vo, wo)
            for row in mat
            for x in row
            if abs(x) > 1
        )
        l1 = sum(abs(x) for mat in (pu, pv, pw) for row in mat for x in row)
        return (bad_terms, bad_entries, l1)

    best_sc = score(PU0, PV0, PW0)
    if best_sc[0] > 0:
        PU = [list(r) for r in PU0]
        PV = [list(r) for r in PV0]
        PW = [list(r) for r in PW0]
        cur_sc = best_sc
        improved = True
        while improved:
            improved = False
            for j1 in range(n0):
                for j2 in range(n0):
                    if j1 == j2:
                        continue
                    for alpha in (-1, 1):
                        pu2 = [list(r) for r in PU]
                        pv2 = [list(r) for r in PV]
                        for i in range(m0):
                            r1, r2 = i * n0 + j1, i * n0 + j2
                            for c in range(DU):
                                pu2[r1][c] += alpha * pu2[r2][c]
                        for k in range(p0):
                            r1, r2 = j1 * p0 + k, j2 * p0 + k
                            for c in range(DV):
                                pv2[r2][c] -= alpha * pv2[r1][c]
                        s = score(pu2, pv2, PW)
                        if s < cur_sc:
                            cur_sc = s
                            PU, PV = pu2, pv2
                            improved = True
            for i1 in range(m0):
                for i2 in range(m0):
                    if i1 == i2:
                        continue
                    for alpha in (-1, 1):
                        pu2 = [list(r) for r in PU]
                        pw2 = [list(r) for r in PW]
                        for j in range(n0):
                            r1, r2 = i1 * n0 + j, i2 * n0 + j
                            for c in range(DU):
                                pu2[r1][c] += alpha * pu2[r2][c]
                        for k in range(p0):
                            r1, r2 = k * m0 + i1, k * m0 + i2
                            for c in range(DW):
                                pw2[r2][c] -= alpha * pw2[r1][c]
                        s = score(pu2, PV, pw2)
                        if s < cur_sc:
                            cur_sc = s
                            PU, PW = pu2, pw2
                            improved = True
        if cur_sc < best_sc:
            best_sc = cur_sc
            best_pu, best_pv, best_pw = PU, PV, PW

    if best_sc[0] > 0:
        for base_pu, base_pv, base_pw in [(PU0, PV0, PW0), (best_pu, best_pv, best_pw)]:
            for perm in itertools.permutations(range(n0)):
                for signs in itertools.product((-1, 1), repeat=n0):
                    pu = [[0] * DU for _ in range(m0 * n0)]
                    pv = [[0] * DV for _ in range(n0 * p0)]
                    for i in range(m0):
                        for j in range(n0):
                            jj, s = perm[j], signs[j]
                            for c in range(DU):
                                pu[i * n0 + j][c] = s * base_pu[i * n0 + jj][c]
                    for j in range(n0):
                        jj, s = perm[j], signs[j]
                        for k in range(p0):
                            for c in range(DV):
                                pv[j * p0 + k][c] = s * base_pv[jj * p0 + k][c]
                    s = score(pu, pv, base_pw)
                    if s < best_sc:
                        best_sc = s
                        best_pu, best_pv, best_pw = pu, pv, base_pw
                        if best_sc[0] == 0:
                            break
                if best_sc[0] == 0:
                    break
            if best_sc[0] == 0:
                break
    return (
        matmul_int(zt0, best_pu),
        matmul_int(zt1, best_pv),
        matmul_int(zt2, best_pw),
        best_sc,
    )


def split_vec_to_ternary(vec):
    v1, v2 = [], []
    for x in vec:
        if x == 2:
            v1.append(1)
            v2.append(1)
        elif x == -2:
            v1.append(-1)
            v2.append(-1)
        else:
            v1.append(x)
            v2.append(0)
    return v1, v2


def try_split_to_zt(U, V, W, max_rank):
    """
    If all non-ternary entries have |x| <= 2 and splitting each non-ternary triad
    into ternary triads yields total rank < max_rank, return (U_zt, V_zt, W_zt).
    """
    U_zt, V_zt, W_zt = [], [], []
    for u, v, w in zip(U, V, W):
        if any(abs(x) > 2 for x in u + v + w):
            return None
        bu = any(abs(x) > 1 for x in u)
        bv = any(abs(x) > 1 for x in v)
        bw = any(abs(x) > 1 for x in w)
        us = list(split_vec_to_ternary(u)) if bu else [u]
        vs = list(split_vec_to_ternary(v)) if bv else [v]
        ws = list(split_vec_to_ternary(w)) if bw else [w]
        for ui in us:
            for vi in vs:
                for wi in ws:
                    U_zt.append(ui)
                    V_zt.append(vi)
                    W_zt.append(wi)
        if len(U_zt) >= max_rank:
            return None
    return U_zt, V_zt, W_zt


def main():
    table, sota = load_reference_bounds(".")
    mpl_245 = load_mpl_raw("data/2x4x5_tensor.mpl", 2, 4, 5)
    mpl_347 = load_mpl_raw("data/3x4x7_tensor.mpl", 3, 4, 7)
    zt_245_d = json.load(open("data/2x4x5_m33_ZT.json"))
    zt_245 = [zt_245_d["u"], zt_245_d["v"], zt_245_d["w"]]
    zt_347_d = json.load(open("data/3x4x7_m64_ZT.json"))
    zt_347 = [zt_347_d["u"], zt_347_d["v"], zt_347_d["w"]]

    os.makedirs("attempts/representation-absorber/result", exist_ok=True)
    upgrades = []

    best_written = {}

    for f in sorted(glob.glob("data/*x*x*_m*_Z.json")):
        d = json.load(open(f))
        n_list = [int(x) for x in d["n"]]
        dims = tuple(sorted(n_list))
        fmt = f"{n_list[0]}x{n_list[1]}x{n_list[2]}"
        ref = table[dims]
        zt_split = try_split_to_zt(d["u"], d["v"], d["w"], ref["ZT"])
        if zt_split is not None:
            U_zt, V_zt, W_zt = zt_split
            R_zt = len(U_zt)
            zt_path = f"attempts/representation-absorber/result/{fmt}_m{R_zt}_ZT.json"
            zt_d = {"n": n_list, "m": R_zt, "u": U_zt, "v": V_zt, "w": W_zt}
            with open(zt_path, "w", encoding="utf-8") as out_f:
                json.dump(zt_d, out_f, separators=(",", ":"))
            sz_zt = os.path.getsize(zt_path)
            print(
                f"UPGRADE (Z->ZT): {os.path.basename(f):21s} -> {os.path.basename(zt_path):24s} | "
                f"Q={ref['Q']} Z={ref['Z']} ZT={ref['ZT']} | new_R={R_zt} (saved {ref['ZT'] - R_zt}) | "
                f"max_abs=1 non_zt=0 size={sz_zt}"
            )
            best_written[zt_path] = (1, 0)
            upgrades.append(zt_path)

    for f in sorted(glob.glob("data/*x*x*_m*_Q.json")):
        d = json.load(open(f))
        n_list = [int(x) for x in d["n"]]
        dims = tuple(sorted(n_list))
        fmt = f"{n_list[0]}x{n_list[1]}x{n_list[2]}"
        ref = table[dims]
        R = d["m"]
        U = [[Fraction(x) for x in row] for row in d["u"]]
        V = [[Fraction(x) for x in row] for row in d["v"]]
        W = [[Fraction(x) for x in row] for row in d["w"]]
        frac_set = set(
            r for r in range(R) if any(x.denominator != 1 for x in U[r] + V[r] + W[r])
        )
        min_blocks = (len(frac_set) + 62) // 63
        if R + min_blocks >= ref["Z"] and R + min_blocks >= ref["ZT"]:
            continue

        r = 0
        new_U, new_V, new_W = [], [], []
        b245, b347 = 0, 0
        ok = True
        while r < R:
            if r in frac_set:
                matched = False
                for bsize, mpl, zt, mdims, tag in [
                    (32, mpl_245, zt_245, (2, 4, 5), "245"),
                    (63, mpl_347, zt_347, (3, 4, 7), "347"),
                ]:
                    if r + bsize <= R:
                        Ub, Vb, Wb = (
                            U[r : r + bsize],
                            V[r : r + bsize],
                            W[r : r + bsize],
                        )
                        for perm in itertools.permutations([0, 1, 2]):
                            PU = solve_linear_map(mpl[perm[0]], Ub)
                            if PU is None:
                                continue
                            PV = solve_linear_map(mpl[perm[1]], Vb)
                            if PV is None:
                                continue
                            PW = solve_linear_map(mpl[perm[2]], Wb)
                            if PW is None:
                                continue
                            P_canon = [None, None, None]
                            P_canon[perm[0]] = PU
                            P_canon[perm[1]] = PV
                            P_canon[perm[2]] = PW
                            u_c, v_c, w_c, sc = optimize_block(
                                P_canon[0],
                                P_canon[1],
                                P_canon[2],
                                zt[0],
                                zt[1],
                                zt[2],
                                *mdims,
                            )
                            out_c = [u_c, v_c, w_c]
                            new_U.extend(out_c[perm[0]])
                            new_V.extend(out_c[perm[1]])
                            new_W.extend(out_c[perm[2]])
                            matched = True
                            if tag == "245":
                                b245 += 1
                            else:
                                b347 += 1
                            r += bsize
                            break
                    if matched:
                        break
                if not matched:
                    ok = False
                    break
            else:
                new_U.append([int(x) for x in U[r]])
                new_V.append([int(x) for x in V[r]])
                new_W.append([int(x) for x in W[r]])
                r += 1

        if not ok:
            continue

        new_R = len(new_U)
        max_abs = max(
            abs(x) for mat in (new_U, new_V, new_W) for row in mat for x in row
        )
        coeff_class = "ZT" if max_abs <= 1 else "Z"
        ref_rank = ref["ZT"] if coeff_class == "ZT" else ref["Z"]
        if new_R < ref_rank:
            non_zt = sum(
                1
                for r_idx in range(new_R)
                if any(abs(x) > 1 for x in new_U[r_idx] + new_V[r_idx] + new_W[r_idx])
            )
            out_path = f"attempts/representation-absorber/result/{fmt}_m{new_R}_{coeff_class}.json"
            if out_path not in best_written or (max_abs, non_zt) < best_written[out_path]:
                best_written[out_path] = (max_abs, non_zt)
                out_d = {"n": n_list, "m": new_R, "u": new_U, "v": new_V, "w": new_W}
                with open(out_path, "w", encoding="utf-8") as out_f:
                    json.dump(out_d, out_f, separators=(",", ":"))
                sz = os.path.getsize(out_path)
                print(
                    f"UPGRADE: {os.path.basename(f):24s} -> {os.path.basename(out_path):24s} | "
                    f"Q={ref['Q']} Z={ref['Z']} ZT={ref['ZT']} | new_R={new_R} (saved {ref_rank - new_R}) | "
                    f"b245={b245} b347={b347} max_abs={max_abs} non_zt={non_zt} size={sz}"
                )
                if out_path not in upgrades:
                    upgrades.append(out_path)

            if coeff_class == "Z":
                zt_split = try_split_to_zt(new_U, new_V, new_W, ref["ZT"])
                if zt_split is not None:
                    U_zt, V_zt, W_zt = zt_split
                    R_zt = len(U_zt)
                    zt_path = f"attempts/representation-absorber/result/{fmt}_m{R_zt}_ZT.json"
                    if zt_path not in best_written:
                        best_written[zt_path] = (1, 0)
                        zt_d = {"n": n_list, "m": R_zt, "u": U_zt, "v": V_zt, "w": W_zt}
                        with open(zt_path, "w", encoding="utf-8") as out_f:
                            json.dump(zt_d, out_f, separators=(",", ":"))
                        sz_zt = os.path.getsize(zt_path)
                        print(
                            f"UPGRADE (ZT split): {os.path.basename(f):13s} -> {os.path.basename(zt_path):24s} | "
                            f"Q={ref['Q']} Z={ref['Z']} ZT={ref['ZT']} | new_R={R_zt} (saved {ref['ZT'] - R_zt}) | "
                            f"max_abs=1 non_zt=0 size={sz_zt}"
                        )
                        if zt_path not in upgrades:
                            upgrades.append(zt_path)

    print(f"Total unique upgrades written: {len(upgrades)}")


if __name__ == "__main__":
    main()
