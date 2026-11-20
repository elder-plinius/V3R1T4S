#!/usr/bin/env python3
"""
build_certificate.py
Deterministic zero-dependency (Python 3 standard library only, zero floating-point arithmetic)
builder for:
  object/d19_nonisometric_periodic_packing_certificate.json

Reconstructs from first principles:
1. The 4,096-word extended binary Golay code G_24 in standard 4x6 MOG coordinates
   and the 24x24 Hermite Normal Form basis of sqrt(8) * Lambda_24 (det = 2^36).
2. Both Co_0-inequivalent saturated rank-5 cross-sections K_I (Ruitao Chen, Jiachen Hu,
   Binghui Li, Liwei Wang, and Tianyi Wu 2025, arXiv:2505.02394) and K_II (discovered here)
   of determinant 300 inside Lambda_24, together with integer Smith Normal Form right-inverse
   saturation witnesses (Y_A * Z_A = I_5, Y_B * Z_B = I_19), exact 19-dimensional orthogonal
   complements L_I and L_II, exact rational LLL-reduced bases, exact rational R^T * D * R
   Cholesky decompositions, and exact 6-translate coset clusters.
3. The exact rational discriminant-square ray shift u_ray / 1860 (22560^2 - 1440 * 14880 = 22080^2,
   alpha = 1/31, reduced ambient denominator 465, basis denominator 930) isolating P19_II_vtx
   as a 0-dimensional vertex of its 12,166-contact kissing-graph stratum
   (bilateral_contact_rank_trans = 95/95, bilateral_contact_rank_full = 285/285).
"""
from fractions import Fraction
import itertools
import json
import math
import os
import sys


def build_mog_golay():
    add4 = [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]]
    mul4 = [[0, 0, 0, 0], [0, 1, 2, 3], [0, 2, 3, 1], [0, 3, 1, 2]]
    hg = [[1, 0, 0, 1, 3, 2], [0, 1, 0, 1, 2, 3], [0, 0, 1, 1, 1, 1]]
    hex_words = [
        [add4[mul4[a][hg[0][j]]][add4[mul4[b][hg[1][j]]][mul4[c][hg[2][j]]]] for j in range(6)]
        for a in range(4) for b in range(4) for c in range(4)
    ]
    col_by_ps = {(p, s): [] for p in (0, 1) for s in range(4)}
    for mask in range(16):
        b = [(mask >> i) & 1 for i in range(4)]
        p = b[0] ^ b[1] ^ b[2] ^ b[3]
        s = 0
        if b[1]:
            s = add4[s][1]
        if b[2]:
            s = add4[s][2]
        if b[3]:
            s = add4[s][3]
        col_by_ps[(p, s)].append((mask, b[0]))
    codewords = []
    for p in (0, 1):
        for hw in hex_words:
            lists = [col_by_ps[(p, hw[j])] for j in range(6)]
            for choice in itertools.product(*lists[:5]):
                need_b0 = p ^ (sum(x[1] for x in choice) & 1)
                c5 = [x[0] for x in lists[5] if x[1] == need_b0][0]
                w24 = 0
                for j in range(5):
                    w24 |= (choice[j][0] << (4 * j))
                w24 |= (c5 << 20)
                codewords.append(w24)
    return sorted(set(codewords))


def row_hnf(mat_rows, ncols_piv=None):
    M = [[int(x) for x in row] for row in mat_rows]
    nrows, ncols = len(M), len(M[0])
    if ncols_piv is None:
        ncols_piv = ncols
    r = 0
    for c in range(ncols_piv):
        while True:
            nz = [i for i in range(r, nrows) if M[i][c] != 0]
            if not nz:
                break
            idx = min(nz, key=lambda i: abs(M[i][c]))
            M[r], M[idx] = M[idx], M[r]
            if M[r][c] < 0:
                M[r] = [-x for x in M[r]]
            piv = M[r][c]
            any_rem = False
            for i in range(r + 1, nrows):
                if M[i][c] != 0:
                    q = M[i][c] // piv
                    M[i] = [M[i][j] - q * M[r][j] for j in range(ncols)]
                    if M[i][c] != 0:
                        any_rem = True
            if not any_rem:
                for i in range(r):
                    if M[i][c] != 0:
                        q = M[i][c] // piv
                        M[i] = [M[i][j] - q * M[r][j] for j in range(ncols)]
                r += 1
                break
    return M, r


def exact_det_and_inv(mat_int):
    n = len(mat_int)
    A = [[Fraction(int(mat_int[i][j]), 1) for j in range(n)] for i in range(n)]
    inv = [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]
    det = Fraction(1, 1)
    for col in range(n):
        piv = next(row for row in range(col, n) if A[row][col] != 0)
        if piv != col:
            A[col], A[piv] = A[piv], A[col]
            inv[col], inv[piv] = inv[piv], inv[col]
            det = -det
        pv = A[col][col]
        det *= pv
        for k in range(n):
            A[col][k] /= pv
            inv[col][k] /= pv
        for row in range(n):
            if row != col and A[row][col] != 0:
                f = A[row][col]
                for k in range(n):
                    A[row][k] -= f * A[col][k]
                    inv[row][k] -= f * inv[col][k]
    return int(det), inv


def nearest_int_exact(frac_val):
    """Exact tie-away-from-zero nearest integer to a Fraction, zero floats."""
    if frac_val >= 0:
        return int((2 * frac_val.numerator + frac_val.denominator) // (2 * frac_val.denominator))
    pos = -frac_val
    return -int((2 * pos.numerator + pos.denominator) // (2 * pos.denominator))


def lll_reduce_exact_fraction(B_in):
    """100% exact rational LLL-(99/100) basis reduction with zero floating-point arithmetic."""
    d, n_amb = len(B_in), len(B_in[0])
    B = [row[:] for row in B_in]
    U = [[1 if i == j else 0 for j in range(d)] for i in range(d)]
    delta = Fraction(99, 100)

    def compute_gs_exact():
        B_star = [[Fraction(0, 1)] * n_amb for _ in range(d)]
        mu = [[Fraction(0, 1)] * d for _ in range(d)]
        B_norm = [Fraction(0, 1)] * d
        for i in range(d):
            for t in range(n_amb):
                B_star[i][t] = Fraction(B[i][t], 1)
            for j in range(i):
                dot = sum(B[i][t] * B_star[j][t] for t in range(n_amb))
                mu[i][j] = dot / B_norm[j]
                for t in range(n_amb):
                    B_star[i][t] -= mu[i][j] * B_star[j][t]
            B_norm[i] = sum(x * x for t_idx, x in enumerate(B_star[i]))
        return mu, B_norm

    mu, B_norm = compute_gs_exact()
    k = 1
    half = Fraction(1, 2)
    while k < d:
        for j in range(k - 1, -1, -1):
            if abs(mu[k][j]) > half:
                q = nearest_int_exact(mu[k][j])
                if q != 0:
                    B[k] = [B[k][t] - q * B[j][t] for t in range(n_amb)]
                    U[k] = [U[k][t] - q * U[j][t] for t in range(d)]
                    mu, B_norm = compute_gs_exact()
        if B_norm[k] >= (delta - mu[k][k - 1] * mu[k][k - 1]) * B_norm[k - 1]:
            k += 1
        else:
            B[k], B[k - 1] = B[k - 1], B[k]
            U[k], U[k - 1] = U[k - 1], U[k]
            mu, B_norm = compute_gs_exact()
            k = max(k - 1, 1)
    return B, U


def exact_rtdr(G_int):
    n = len(G_int)
    G = [[Fraction(int(G_int[i][j]), 1) for j in range(n)] for i in range(n)]
    R = [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]
    D = [Fraction(0, 1)] * n
    for i in range(n):
        D[i] = G[i][i] - sum(D[k] * R[k][i] * R[k][i] for k in range(i))
        for j in range(i + 1, n):
            R[i][j] = (G[i][j] - sum(D[k] * R[k][i] * R[k][j] for k in range(i))) / D[i]
    return R, D


def solve_leech_upper_tri(rows, leech_B):
    out = []
    for r in rows:
        rem = [int(x) for x in r]
        y = [0] * 24
        for i in range(24):
            assert rem[i] % leech_B[i][i] == 0
            yi = rem[i] // leech_B[i][i]
            y[i] = yi
            for c in range(i, 24):
                rem[c] -= yi * leech_B[i][c]
        assert all(v == 0 for v in rem)
        out.append(y)
    return out


def snf_right_inverse_transpose(Y):
    """
    Exact integer Smith Normal Form L * Y * R = [I_k | 0], returning Z^T (k x 24)
    such that Y * Z == I_k in Z^(k x k), certifying saturation inside Z^24.
    """
    k, n = len(Y), len(Y[0])
    M = [row[:] for row in Y]
    L = [[1 if i == j else 0 for j in range(k)] for i in range(k)]
    R = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    for p in range(k):
        while True:
            best = None
            for i in range(p, k):
                for j in range(p, n):
                    if M[i][j] != 0:
                        cand = (abs(M[i][j]), i, j)
                        if best is None or cand < best:
                            best = cand
            assert best is not None
            _, bi, bj = best
            if bi != p:
                M[p], M[bi] = M[bi], M[p]
                L[p], L[bi] = L[bi], L[p]
            if bj != p:
                for i in range(k):
                    M[i][p], M[i][bj] = M[i][bj], M[i][p]
                for i in range(n):
                    R[i][p], R[i][bj] = R[i][bj], R[i][p]
            if M[p][p] < 0:
                M[p] = [-x for x in M[p]]
                L[p] = [-x for x in L[p]]

            changed = False
            for i in range(p + 1, k):
                if M[i][p] != 0:
                    q = M[i][p] // M[p][p]
                    for j in range(p, n):
                        M[i][j] -= q * M[p][j]
                    for j in range(k):
                        L[i][j] -= q * L[p][j]
                    if M[i][p] != 0:
                        changed = True
            for j in range(p + 1, n):
                if M[p][j] != 0:
                    q = M[p][j] // M[p][p]
                    for i in range(p, k):
                        M[i][j] -= q * M[i][p]
                    for i in range(n):
                        R[i][j] -= q * R[i][p]
                    if M[p][j] != 0:
                        changed = True
            if changed:
                continue

            bad = None
            for i in range(p + 1, k):
                for j in range(p + 1, n):
                    if M[i][j] % M[p][p] != 0:
                        bad = i
                        break
                if bad is not None:
                    break
            if bad is not None:
                for j in range(p, n):
                    M[p][j] += M[bad][j]
                for j in range(k):
                    L[p][j] += L[bad][j]
                continue
            break

    assert [M[i][i] for i in range(k)] == [1] * k
    Z_T = [[sum(R[c][t] * L[t][b] for t in range(k)) for c in range(n)] for b in range(k)]
    for a in range(k):
        for b in range(k):
            assert sum(Y[a][c] * Z_T[b][c] for c in range(n)) == (1 if a == b else 0)
    return Z_T


def fmt_frac(x):
    return f"{x.numerator}/{x.denominator}" if x.denominator != 1 else str(x.numerator)


def build_entry(name, A_scaled, leech_B, u_ray=None):
    K_gram = [[sum(A_scaled[i][c] * A_scaled[j][c] for c in range(24)) // 8 for j in range(5)] for i in range(5)]
    det_K, M_inv = exact_det_and_inv(K_gram)
    assert det_K == 300
    M60 = [[int(M_inv[i][j] * 60) for j in range(5)] for i in range(5)]

    phi_mat = [[sum(leech_B[r][c] * A_scaled[j][c] for c in range(24)) // 8 for j in range(5)] for r in range(24)]
    aug = [phi_mat[r] + [1 if c == r else 0 for c in range(24)] for r in range(24)]
    H_aug, rk = row_hnf(aug, 5)
    assert rk == 5
    W_uni = [row[5:] for row in H_aug]
    NewB = [[sum(W_uni[i][k] * leech_B[k][c] for k in range(24)) for c in range(24)] for i in range(24)]
    DualLifts = NewB[:5]
    B_orig = NewB[5:]

    B_lll, U_lll = lll_reduce_exact_fraction(B_orig)
    det_U, _ = exact_det_and_inv(U_lll)
    assert det_U in (-1, 1)
    G_19 = [[sum(B_lll[i][c] * B_lll[j][c] for c in range(24)) // 8 for j in range(19)] for i in range(19)]
    det_G, G_inv = exact_det_and_inv(G_19)
    assert det_G == 300
    R_rat, D_rat = exact_rtdr(G_19)

    YA = solve_leech_upper_tri(A_scaled, leech_B)
    YB = solve_leech_upper_tri(B_lll, leech_B)
    ZA_T = snf_right_inverse_transpose(YA)
    ZB_T = snf_right_inverse_transpose(YB)

    S_coords = [[0] * 5] + [[1 if j == i else 0 for j in range(5)] for i in range(5)]
    den_amb = 1860 if u_ray is not None else 60
    t_raw = []
    for idx_s in range(6):
        z = S_coords[idx_s]
        w0 = [sum(z[k] * DualLifts[k][c] for k in range(5)) for c in range(24)]
        zM = [sum(z[a] * M60[a][b] for a in range(5)) for b in range(5)]
        proj = [sum(zM[b] * A_scaled[b][c] for b in range(5)) for c in range(24)]
        base_60 = [60 * w0[c] - proj[c] for c in range(24)]
        if u_ray is not None:
            shift = u_ray if idx_s in (1, 2, 3) else [0] * 24
            num = [31 * base_60[c] + shift[c] for c in range(24)]
        else:
            num = base_60
        t_raw.append(num)

    g_amb = den_amb
    for arr in t_raw:
        for v in arr:
            if v != 0:
                g_amb = math.gcd(g_amb, abs(v))
    den_amb //= g_amb
    t_amb = [[v // g_amb for v in arr] for arr in t_raw]

    c_fracs = []
    for idx_s in range(6):
        rhs = [Fraction(sum(t_amb[idx_s][c] * B_lll[m][c] for c in range(24)), 8 * den_amb) for m in range(19)]
        c_vec = [sum(rhs[k] * G_inv[k][m] for k in range(19)) for m in range(19)]
        c_mod = [c_vec[m] - math.floor(c_vec[m]) for m in range(19)]
        c_fracs.append(c_mod)

    den_c = 1
    for row in c_fracs:
        for x in row:
            den_c = math.lcm(den_c, x.denominator)
    c_nums = [[int(x * den_c) for x in row] for row in c_fracs]

    return {
        "name": name,
        "leech_section_A_scaled": A_scaled,
        "leech_section_A_right_inv_T_5x24": ZA_T,
        "leech_complement_B_original_scaled": B_orig,
        "unimodular_U_lll": U_lll,
        "det_U_lll": det_U,
        "leech_complement_B_lll_scaled": B_lll,
        "leech_complement_B_lll_right_inv_T_19x24": ZB_T,
        "gram_G_19x19": G_19,
        "cholesky_R_19x19": [[fmt_frac(x) for x in row] for row in R_rat],
        "cholesky_D_19": [fmt_frac(x) for x in D_rat],
        "translates_basis_coords_den": den_c,
        "translates_basis_coords_num": c_nums,
        "translates_ambient_24d_den": den_amb,
        "translates_ambient_24d_num": t_amb,
    }


def main():
    out_file = sys.argv[1] if len(sys.argv) >= 2 else "object/d19_nonisometric_periodic_packing_certificate.json"
    golay = build_mog_golay()
    g_basis, pivots = [], []
    for w in golay:
        cur = w
        for p, bw in zip(pivots, g_basis):
            if (cur >> p) & 1:
                cur ^= bw
        if cur:
            pivots.append((cur & -cur).bit_length() - 1)
            g_basis.append(cur)
        if len(g_basis) == 12:
            break
    gens = [[8] + [0] * 23] + [[4 if j in (0, i) else 0 for j in range(24)] for i in range(1, 24)]
    for w in g_basis:
        gens.append([2 if ((w >> i) & 1) else 0 for i in range(24)])
    gens.append([-3] + [1] * 23)
    H_leech, _ = row_hnf(gens, 24)
    leech_B = H_leech[:24]

    A_II = [
        [-4, -4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [-4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 2, 0, 0, -2, 2, 0, -2, 0, 0, 0, 2, -2, 0, 2, -2, 0, 0, 0, 0, 0],
        [3, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1],
        [2, 0, 0, 0, -2, 0, 0, 0, 0, 0, 2, 0, -2, -2, 0, 2, 0, 0, 2, 0, 0, 0, -2, 0],
    ]
    u_ray = [0, 0, -16, -16, 62, -16, 16, 18, -18, -16, 26, -16, -24, -24, -18, 26, 16, -18, -62, -16, -16, 16, -24, -16]

    A_I_ref = [
        [2 * x for x in ([0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0] + [0] * 12)],
        [2 * x for x in ([2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0] + [0] * 12)],
        [2 * x for x in ([0, 2, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0] + [0] * 12)],
        [2 * x for x in ([-1, -1, -1, -1, -1, -1, 1, 1, 0, 0, 0, 0] + [0] * 12)],
        [2 * x for x in ([-1, -1, 1, 1, 0, 0, 0, 0, -1, -1, 1, 1] + [0] * 12)],
    ]

    entry_new = build_entry("P19_II_vtx", A_II, leech_B, u_ray)
    entry_new["expected_invariants"] = {
        "det_G": 300,
        "leech_saturation_unimodular": True,
        "sym_trans_stabilizer_size": 1,
        "intra_lattice_min_sq": "4",
        "intra_lattice_norm4_count": 6858,
        "packing_min_sq": "52/15",
        "kissing_per_translate": [4072, 4022, 4072, 4072, 4072, 4022],
        "kissing_sorted": [4022, 4022, 4072, 4072, 4072, 4072],
        "kissing_min": 4022,
        "kissing_max": 4072,
        "kissing_avg": "12166/3",
        "tight_translate_pairs": 8,
        "translate_contact_triangles": 2,
        "translate_contact_graph_connected": True,
        "bilateral_contact_rank_trans": 95,
        "bilateral_contact_nullity_trans": 0,
        "bilateral_contact_rank_full": 285,
        "bilateral_contact_nullity_full": 0,
    }

    entry_ref = build_entry("P19_ChenHuLiWangWu2025_ref", A_I_ref, leech_B, None)
    entry_ref["expected_invariants"] = {
        "det_G": 300,
        "leech_saturation_unimodular": True,
        "sym_trans_stabilizer_size": 1,
        "intra_lattice_min_sq": "4",
        "intra_lattice_norm4_count": 6942,
        "packing_min_sq": "52/15",
        "kissing_per_translate": [4110, 4110, 4110, 4110, 4110, 4110],
        "kissing_sorted": [4110, 4110, 4110, 4110, 4110, 4110],
        "kissing_min": 4110,
        "kissing_max": 4110,
        "kissing_avg": "4110",
        "tight_translate_pairs": 6,
        "translate_contact_triangles": 2,
        "translate_contact_graph_connected": False,
        "bilateral_contact_rank_trans": 76,
        "bilateral_contact_nullity_trans": 19,
        "bilateral_contact_rank_full": 266,
        "bilateral_contact_nullity_full": 19,
    }

    E8_gram = [
        [2, -1, 0, 0, 0, 0, 0, 0],
        [-1, 2, -1, 0, 0, 0, 0, 0],
        [0, -1, 2, -1, 0, 0, 0, -1],
        [0, 0, -1, 2, -1, 0, 0, 0],
        [0, 0, 0, -1, 2, -1, 0, 0],
        [0, 0, 0, 0, -1, 2, -1, 0],
        [0, 0, 0, 0, 0, -1, 2, 0],
        [0, 0, -1, 0, 0, 0, 0, 2],
    ]
    R_e8, D_e8 = exact_rtdr(E8_gram)
    delta_sq = Fraction(13 ** 19, (3 ** 18) * (5 ** 21))

    cert = {
        "schema": "v3r1t4s-periodic-sphere-packing-certificate-v2",
        "target_id": "cohn-sphere-packing-density-table",
        "claim_level": "partial_win_p1",
        "dimension": 19,
        "num_translates": 6,
        "minimal_squared_distance": "52/15",
        "packing_radius_squared": "13/15",
        "cohn_live_center_density_formula": "3^(-9) * 5^(-21/2) * 13^(19/2)",
        "center_density_squared_num": str(delta_sq.numerator),
        "center_density_squared_den": str(delta_sq.denominator),
        "leech_lattice_basis_scaled_sqrt8": leech_B,
        "calibration_e8": {
            "dimension": 8,
            "num_translates": 1,
            "gram_G_8x8": E8_gram,
            "cholesky_R_8x8": [[fmt_frac(x) for x in row] for row in R_e8],
            "cholesky_D_8": [fmt_frac(x) for x in D_e8],
            "expected_det_G": 1,
            "expected_min_sq": "2",
            "expected_kissing": 240,
            "expected_center_density_squared": "1/256",
        },
        "new_packing": entry_new,
        "reference_packing_chen2025": entry_ref,
    }
    os.makedirs(os.path.dirname(os.path.abspath(out_file)), exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(cert, f, indent=2)
    print(f"Built {out_file} ({os.path.getsize(out_file)} bytes)")


if __name__ == "__main__":
    main()
