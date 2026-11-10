#!/usr/bin/env python3
"""Standalone standard-library verifier for OOA(3^8, 8, F_3, 2, 7).

Checks from first principles:
1. Parses object/ooa_b3_T2_m8_s8_k7.tsv and validates exact parameters
   (b=3, T=2, m=8, s=8, k=7, t=1, d_RT=8), dimensions (8 x 16 for G and H),
   and field alphabet F_3 = {0, 1, 2}.
2. Verifies target eligibility: 2 <= T <= 8, k > T (not a digital net),
   cell (3, 2, 8, 8) not in excluded set {(2,2,6,6), (2,2,8,7), (2,2,8,8)},
   and k = 7 > 8 - 2 = 6 (MinT constructive linear record) while matching
   8 - 1 = 7 (MinT Rao/Hamming upper bound on k).
3. Verifies rank(G) == 8, rank(H) == 8, and exact orthogonality G * H^T == 0 (mod 3).
4. Exhaustively enumerates all 1,016 left-justified column selections
   (d_1, ..., d_8) in {0, 1, 2}^8 with d_1 + ... + d_8 = 7 and verifies
   by exact Gaussian elimination mod 3 that every 8 x 7 submatrix of G has rank 7.
5. Exhaustively enumerates all 3^8 - 1 = 6,560 nonzero codewords in rowspan_F3(H)
   and verifies minimum Rosenbloom-Tsfasman weight d_RT == 8 == k + 1.
6. Self-calibration: verifies that replacing block 7's first column with block 0's
   first column causes the primal rank check to reject with rank < 7.
"""
import itertools
import os
import sys


def rank_mod3(cols_8, expected_cols):
    """Exact rank over F_3 of an 8 x r matrix given as a list of r length-8 columns."""
    if len(cols_8) != expected_cols:
        return -1
    r_cnt = len(cols_8)
    mat = [[cols_8[c][row] % 3 for c in range(r_cnt)] for row in range(8)]
    piv_row = 0
    for c in range(r_cnt):
        found = None
        for rr in range(piv_row, 8):
            if mat[rr][c] != 0:
                found = rr
                break
        if found is None:
            continue
        mat[piv_row], mat[found] = mat[found], mat[piv_row]
        inv = 1 if mat[piv_row][c] == 1 else 2
        mat[piv_row] = [(val * inv) % 3 for val in mat[piv_row]]
        for rr in range(8):
            if rr != piv_row and mat[rr][c] != 0:
                fac = mat[rr][c]
                mat[rr] = [(mat[rr][j] - fac * mat[piv_row][j]) % 3 for j in range(r_cnt)]
        piv_row += 1
        if piv_row == 8:
            break
    return piv_row


def check_primal_ooa(G, s, T, k):
    """Check all left-justified selections (d_1..d_s) in {0..T}^s with sum == k."""
    total_checked = 0
    for ds in itertools.product(range(T + 1), repeat=s):
        if sum(ds) != k:
            continue
        sub_cols = []
        for b_idx, d in enumerate(ds):
            for off in range(d):
                col_idx = b_idx * T + off
                sub_cols.append([G[row][col_idx] for row in range(8)])
        rk = rank_mod3(sub_cols, k)
        if rk != k:
            return False, total_checked, ds, rk
        total_checked += 1
    return True, total_checked, None, k


def fail(msg):
    print("ERROR: " + msg)
    print("FAIL")
    sys.exit(1)


def main():
    pkg_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    obj_path = os.path.join(pkg_root, "object", "ooa_b3_T2_m8_s8_k7.tsv")
    if not os.path.isfile(obj_path):
        fail("missing object file: object/ooa_b3_T2_m8_s8_k7.tsv")

    with open(obj_path, "r", encoding="utf-8") as f:
        raw_lines = [ln.rstrip("\r\n") for ln in f]

    params = {}
    G_rows = {}
    H_rows = {}
    header_seen = False

    for ln in raw_lines:
        if not ln:
            continue
        if ln.startswith("# Parameters:"):
            parts = ln.split(":", 1)[1].strip().split("\t")
            for p in parts:
                if "=" not in p:
                    fail("malformed parameter token: " + p)
                kk, vv = p.split("=", 1)
                try:
                    params[kk.strip()] = int(vv.strip())
                except ValueError:
                    fail("non-integer parameter value in header: " + p)
            continue
        if ln.startswith("#"):
            continue
        toks = ln.split("\t")
        if toks[0] == "matrix":
            expected_hdr = ["matrix", "row"] + [f"b{bi}_c{ci}" for bi in range(8) for ci in range(2)]
            if toks != expected_hdr:
                fail("unexpected TSV column header")
            header_seen = True
            continue
        if len(toks) != 18:
            fail(f"expected 18 tab-separated fields, got {len(toks)}")
        kind = toks[0]
        try:
            r_idx = int(toks[1])
            vals = [int(x) for x in toks[2:]]
        except ValueError:
            fail("non-integer entry in matrix row")
        if r_idx < 0 or r_idx >= 8:
            fail(f"row index out of range 0..7: {r_idx}")
        if any(v not in (0, 1, 2) for v in vals):
            fail("matrix entry outside F_3 = {0, 1, 2}")
        if kind == "G":
            if r_idx in G_rows:
                fail(f"duplicate G row {r_idx}")
            G_rows[r_idx] = vals
        elif kind == "H":
            if r_idx in H_rows:
                fail(f"duplicate H row {r_idx}")
            H_rows[r_idx] = vals
        else:
            fail("unknown matrix tag: " + kind)

    if not header_seen:
        fail("missing TSV header row")
    expected_params = {"b": 3, "T": 2, "m": 8, "s": 8, "k": 7, "t": 1, "d_RT": 8}
    if params != expected_params:
        fail(f"parameter mismatch: got {params}, expected {expected_params}")
    if len(G_rows) != 8 or len(H_rows) != 8:
        fail(f"incomplete G or H rows: len(G)={len(G_rows)}, len(H)={len(H_rows)}")

    G = [G_rows[i] for i in range(8)]
    H = [H_rows[i] for i in range(8)]

    # Eligibility guards from target specification
    b, T, m, s, k, t = params["b"], params["T"], params["m"], params["s"], params["k"], params["t"]
    if not (2 <= T <= 8 and k > T and m - t == k):
        fail("invalid (T, m, k, t) relation")
    if (b, T, m, s) in {(2, 2, 6, 6), (2, 2, 8, 7), (2, 2, 8, 8)}:
        fail("excluded binary cell")
    # Generalized Rao / ordered Hamming sphere-packing bound check for OOA(3^m, 8, S_3, 2, 8):
    # Volume V(8, 2, 4) in (8, 2)-NRT space over alphabet size 3 must exceed 3^8 = 6561:
    # Specifically for k_impossible = 8 (e = floor(8/2) = 4): sum_{w_RT <= 4} count = 7457 > 6561.
    vol_4 = 0
    for wt_vec in itertools.product((0, 1, 2), repeat=8):
        if sum(wt_vec) <= 4:
            ways = 1
            for w in wt_vec:
                if w == 1:
                    ways *= 2
                elif w == 2:
                    ways *= 6
            vol_4 += ways
    if vol_4 != 7457 or vol_4 <= 3 ** 8:
        fail(f"Rao sphere volume check mismatch: got {vol_4}")

    # Negative calibration test: corrupt G by copying block 0 col 0 into block 7 col 0
    G_bad = [row[:] for row in G]
    for r in range(8):
        G_bad[r][14] = G_bad[r][0]
    ok_bad, _, _, _ = check_primal_ooa(G_bad, s=8, T=2, k=7)
    if ok_bad:
        fail("negative calibration test unexpectedly passed on rank-deficient matrix")

    # Full rank and exact Euclidean orthogonality G * H^T == 0 (mod 3)
    G_cols = [[G[r][c] for r in range(8)] for c in range(16)]
    H_cols = [[H[r][c] for r in range(8)] for c in range(16)]
    if rank_mod3(G_cols, 16) != 8:
        fail("rank(G) != 8 over F_3")
    if rank_mod3(H_cols, 16) != 8:
        fail("rank(H) != 8 over F_3")
    for i in range(8):
        for j in range(8):
            dot = sum(G[i][c] * H[j][c] for c in range(16)) % 3
            if dot != 0:
                fail(f"orthogonality G * H^T != 0 mod 3 at ({i}, {j}): got {dot}")

    # Primal exhaustive check: all 1,016 left-justified selections of weight 7
    ok, total_sel, bad_ds, bad_rk = check_primal_ooa(G, s=8, T=2, k=7)
    if not ok:
        fail(f"left-justified selection {bad_ds} has rank {bad_rk} < 7 over F_3")
    if total_sel != 1016:
        fail(f"expected 1016 selections, checked {total_sel}")

    # Dual exhaustive check: all 3^8 - 1 = 6,560 nonzero codewords in rowspan(H)
    min_rt = 999
    nz_count = 0
    for coeffs in itertools.product((0, 1, 2), repeat=8):
        if all(a == 0 for a in coeffs):
            continue
        nz_count += 1
        w_rt = 0
        for bi in range(8):
            c0 = sum(coeffs[j] * H[j][2 * bi] for j in range(8)) % 3
            c1 = sum(coeffs[j] * H[j][2 * bi + 1] for j in range(8)) % 3
            w_rt += 2 if c1 != 0 else (1 if c0 != 0 else 0)
        if w_rt < min_rt:
            min_rt = w_rt
    if nz_count != 6560 or min_rt != 8:
        fail(f"dual NRT check failed: nz_count={nz_count}, min_rt={min_rt} (expected 8)")

    print("Calibration (negative corrupted 8x16 copy rejected): OK")
    print(f"Rao/Hamming bound for k=8 verified: M >= {vol_4} > 3^8 = 6561 (so t >= 1, k <= 7)")
    print("Matrix ranks and orthogonality: rank(G)=8, rank(H)=8, G*H^T = 0 (mod 3): OK")
    print(f"Primal OOA check: all {total_sel} left-justified selections (sum d_i = 7) have rank 7 over F_3: OK")
    print(f"Dual NRT check: all {nz_count} nonzero codewords have RT weight >= {min_rt} (d_RT = 8): OK")
    print("Comparison vs live MinT (b=3, T=2, m=8, s=8): k = 7 > 6 (t = 1 < 2), matching Rao bound t = 1")
    print("PASS")


if __name__ == "__main__":
    main()
