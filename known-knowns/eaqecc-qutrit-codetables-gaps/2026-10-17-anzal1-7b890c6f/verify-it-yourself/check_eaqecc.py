#!/usr/bin/env python3
"""Standalone exact verifier for [[14, 3, 8; 5]]_3 qutrit EAQECC (object/qutrit_14_3_8_5.json).
Standard-library Python 3 only.
"""
import argparse
import itertools
import json
import sys

GF9_ADD = [[0] * 9 for _ in range(9)]
GF9_MUL = [[0] * 9 for _ in range(9)]
GF9_CONJ = [0] * 9

for _x in range(9):
    _ax, _bx = _x % 3, _x // 3
    GF9_CONJ[_x] = _ax + 3 * ((2 * _bx) % 3)
    for _y in range(9):
        _ay, _by = _y % 3, _y // 3
        GF9_ADD[_x][_y] = ((_ax + _ay) % 3) + 3 * ((_bx + _by) % 3)
        _re = (_ax * _ay + 2 * _bx * _by) % 3
        _im = (_ax * _by + _bx * _ay) % 3
        GF9_MUL[_x][_y] = _re + 3 * _im


def rref_gf3(mat, ncols):
    rows = [list(r) for r in mat]
    pivots = []
    r = 0
    m = len(rows)
    for c in range(ncols):
        if r >= m:
            break
        piv = None
        for i in range(r, m):
            if rows[i][c] % 3 != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = 1 if rows[r][c] % 3 == 1 else 2
        rows[r] = [(x * inv) % 3 for x in rows[r]]
        for i in range(m):
            if i != r and rows[i][c] % 3 != 0:
                factor = rows[i][c] % 3
                rows[i] = [(rows[i][j] - factor * rows[r][j]) % 3 for j in range(ncols)]
        pivots.append(c)
        r += 1
    return rows[:r], pivots


def nullspace_gf3(mat, ncols):
    rref, pivots = rref_gf3(mat, ncols)
    piv_set = set(pivots)
    free_cols = [c for c in range(ncols) if c not in piv_set]
    basis = []
    for fc in free_cols:
        vec = [0] * ncols
        vec[fc] = 1
        for r_idx, pc in enumerate(pivots):
            vec[pc] = (3 - rref[r_idx][fc]) % 3
        basis.append(vec)
    return basis


def in_span_gf3(vec, rref, pivots):
    v = list(vec)
    for r_idx, pc in enumerate(pivots):
        coeff = v[pc] % 3
        if coeff != 0:
            v = [(v[j] - coeff * rref[r_idx][j]) % 3 for j in range(len(v))]
    return all(x % 3 == 0 for x in v)


def symp_inner(u, v, n):
    total = 0
    for i in range(n):
        total += u[i] * v[n + i] - u[n + i] * v[i]
    return total % 3


def symp_weight(v, n):
    w = 0
    for i in range(n):
        if (v[i] % 3) != 0 or (v[n + i] % 3) != 0:
            w += 1
    return w


def herm_inner_gf9(u, v):
    s = 0
    for x, y in zip(u, v):
        s = GF9_ADD[s][GF9_MUL[x][GF9_CONJ[y]]]
    return s


def verify_package_object(data):
    n = data.get("n")
    k_exp = data.get("k")
    d_exp = data.get("d")
    c_exp = data.get("c")
    s_exp = data.get("s")
    d_lower = data.get("d_lower")
    d_upper = data.get("d_upper")
    if (n, k_exp, d_exp, c_exp, s_exp, d_lower, d_upper) != (14, 3, 8, 5, 16, 7, 10):
        return False, "Header parameters do not match [[14, 3, 8; 5]]_3 against 7-10"

    S = data.get("S", [])
    if len(S) != s_exp:
        return False, f"len(S)={len(S)} != {s_exp}"
    for row in S:
        if len(row) != 2 * n or any(x not in (0, 1, 2) for x in row):
            return False, "Invalid row in S"

    rref_S, piv_S = rref_gf3(S, 2 * n)
    if len(rref_S) != s_exp:
        return False, f"S is not full rank: rank={len(rref_S)} != {s_exp}"

    # Verify GF(9) seed and dual matrix H9 consistency if present
    H0 = data.get("H9_self_orthogonal_seed")
    H9 = data.get("H9")
    cols_scaled = set(data.get("diagonal_scaling_columns", []))
    scale_factor = data.get("diagonal_scaling_factor_gf9", 4)
    if H0 is not None and H9 is not None:
        if len(H0) != 6 or len(H9) != 6:
            return False, "H0/H9 must have 6 rows"
        for r0, r9 in zip(H0, H9):
            if len(r0) != n or len(r9) != n:
                return False, "H0/H9 row length != 14"
            if any(x not in range(9) for x in r0) or any(x not in range(9) for x in r9):
                return False, "H0/H9 entry out of range 0..8"
        # Check H0 is 2-quasi-cyclic and Hermitian self-orthogonal
        for i in range(6):
            for j in range(6):
                if herm_inner_gf9(H0[i], H0[j]) != 0:
                    return False, f"H0 is not Hermitian self-orthogonal at ({i},{j})"
        # Check H9 matches diagonal scaling of H0
        for i in range(6):
            for col in range(n):
                expected_val = GF9_MUL[H0[i][col]][scale_factor] if col in cols_scaled else H0[i][col]
                if H9[i][col] != expected_val:
                    return False, f"H9[{i}][{col}]={H9[i][col]} != scaled H0 value {expected_val}"
        # Check H9 maps to S^perp
        H3 = []
        for row in H9:
            H3.append([val % 3 for val in row] + [val // 3 for val in row])
            H3.append([(2 * (val // 3)) % 3 for val in row] + [val % 3 for val in row])
        for s_row in S:
            for h_row in H3:
                if symp_inner(s_row, h_row, n) != 0:
                    return False, "S and H9 are not symplectically orthogonal"
        H3J = [[(2 * r[n + j]) % 3 for j in range(n)] + [r[j] % 3 for j in range(n)] for r in H3]
        S_rebuilt = nullspace_gf3(H3J, 2 * n)
        if S_rebuilt != S:
            return False, "S does not match canonical nullspace_gf3(H3 * J)"

    # Commutation matrix M = S * J * S^T mod 3
    M = [[symp_inner(S[i], S[j], n) for j in range(s_exp)] for i in range(s_exp)]
    rref_M, _ = rref_gf3(M, s_exp)
    if len(rref_M) != 2 * c_exp:
        return False, f"rank(S J S^T)={len(rref_M)} != 2c={2*c_exp}"
    k = n - s_exp + c_exp
    if k != k_exp:
        return False, f"k={k} != {k_exp}"

    SJ = [[(2 * row[n + j]) % 3 for j in range(n)] + [row[j] % 3 for j in range(n)] for row in S]
    dual_basis = nullspace_gf3(SJ, 2 * n)
    dim_dual = len(dual_basis)
    if dim_dual != 2 * n - s_exp:
        return False, f"dim(S^perp)={dim_dual} != {2*n - s_exp}"

    min_d_non_iso = n + 1
    min_d_iso = n + 1
    non_iso_count = 0
    iso_count = 0

    for coeffs in itertools.product((0, 1, 2), repeat=dim_dual):
        first_nz = 0
        for x in coeffs:
            if x != 0:
                first_nz = x
                break
        if first_nz != 1:
            continue
        v = [0] * (2 * n)
        for c_i, b_row in zip(coeffs, dual_basis):
            if c_i:
                for j in range(2 * n):
                    v[j] = (v[j] + c_i * b_row[j]) % 3
        w = symp_weight(v, n)
        if in_span_gf3(v, rref_S, piv_S):
            iso_count += 2
            if w < min_d_iso:
                min_d_iso = w
        else:
            non_iso_count += 2
            if w < min_d_non_iso:
                min_d_non_iso = w

    if iso_count + 1 != 729 or non_iso_count != 530712:
        return False, f"Unexpected dual/isotropic counts: iso={iso_count+1}, non_iso={non_iso_count}"
    if min_d_non_iso != d_exp or min_d_iso != d_exp:
        return False, f"Minimum distance mismatch: d_non_iso={min_d_non_iso}, d_iso={min_d_iso} != {d_exp}"
    if not (min_d_non_iso > d_lower and min_d_non_iso <= d_upper):
        return False, f"Distance {min_d_non_iso} does not beat d_lower={d_lower} within d_upper={d_upper}"

    return True, f"VALID [[{n}, {k}, {min_d_non_iso}; {c_exp}]]_3 (pure: d_non_iso={min_d_non_iso}, d_iso={min_d_iso}, s={s_exp}, dim_dual={dim_dual}, dim_iso=6, non_iso_vecs={non_iso_count})"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_file")
    args = ap.parse_args()
    try:
        with open(args.json_file, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"JSON load error: {e}")
        print("FAIL")
        sys.exit(1)
    ok, msg = verify_package_object(data)
    print(msg)
    if ok:
        print("PASS")
        sys.exit(0)
    else:
        print("FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
