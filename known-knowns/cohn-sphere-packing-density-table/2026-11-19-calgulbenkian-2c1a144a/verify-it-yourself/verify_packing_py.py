#!/usr/bin/env python3
"""
verify_packing_py.py
Independent, zero-shared-code, zero-floating-point Python standard-library verifier
(fractions.Fraction + math.isqrt + json + sys ONLY) for:
  Target: cohn-sphere-packing-density-table (Partial Win p1, dimension 19)
"""
from fractions import Fraction
from math import isqrt
import json
import sys


def parse_frac(s):
    if isinstance(s, int):
        return Fraction(s, 1)
    if "/" in s:
        a, b = s.split("/")
        return Fraction(int(a), int(b))
    return Fraction(int(s), 1)


def exact_det_and_inv_fraction(mat_int):
    """Exact determinant and inverse over Q via Gauss-Jordan in fractions.Fraction."""
    n = len(mat_int)
    A = [[Fraction(int(mat_int[i][j]), 1) for j in range(n)] for i in range(n)]
    inv = [[Fraction(1 if i == j else 0, 1) for j in range(n)] for i in range(n)]
    det = Fraction(1, 1)
    for col in range(n):
        piv = None
        for row in range(col, n):
            if A[row][col] != 0:
                piv = row
                break
        if piv is None:
            return Fraction(0, 1), None
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
                factor = A[row][col]
                for k in range(n):
                    A[row][k] -= factor * A[col][k]
                    inv[row][k] -= factor * inv[col][k]
    return det, inv


def independent_cholesky_fraction(G_int):
    d = len(G_int)
    G = [[Fraction(int(G_int[i][j]), 1) for j in range(d)] for i in range(d)]
    R = [[Fraction(1 if i == j else 0, 1) for j in range(d)] for i in range(d)]
    D = [Fraction(0, 1) for _ in range(d)]
    for i in range(d):
        diag_val = G[i][i] - sum(D[k] * R[k][i] * R[k][i] for k in range(i))
        if diag_val <= 0:
            raise AssertionError(f"Non-positive Cholesky pivot at {i}")
        D[i] = diag_val
        for j in range(i + 1, d):
            num = G[i][j] - sum(D[k] * R[k][i] * R[k][j] for k in range(i))
            R[i][j] = num / D[i]
    return R, D


def fp_enumerate_fraction(R, D, G_int, delta_c, bound_sq, skip_zero=False):
    d = len(D)
    x = [0] * d
    yc = [Fraction(0, 1)] * d
    violations = 0
    best_sq = None
    tight_vectors = []

    def rec(m, rem):
        nonlocal violations, best_sq
        if m < 0:
            if skip_zero and all(v == 0 for v in x):
                return
            sos_sq = bound_sq - rem
            if sos_sq <= bound_sq:
                if best_sq is None or sos_sq < best_sq:
                    best_sq = sos_sq
                if sos_sq < bound_sq:
                    violations += 1
                else:
                    tight_vectors.append(tuple(yc))
            return

        alpha = delta_c[m]
        row_R = R[m]
        for l in range(m + 1, d):
            if yc[l] != 0 and row_R[l] != 0:
                alpha += row_R[l] * yc[l]

        ratio = rem / D[m]
        if ratio < 0:
            return
        a, b = alpha.numerator, alpha.denominator
        p, q = ratio.numerator, ratio.denominator
        limit = isqrt(p * q * b * b)
        denom = q * b
        lo_num = -limit - q * a
        hi_num = limit - q * a
        x_lo = -((-lo_num) // denom) if lo_num < 0 else (lo_num + denom - 1) // denom
        x_hi = hi_num // denom

        dm = D[m]
        dc_m = delta_c[m]
        for xv in range(x_lo, x_hi + 1):
            t_val = xv + alpha
            new_rem = rem - dm * t_val * t_val
            if new_rem >= 0:
                x[m] = xv
                yc[m] = xv + dc_m
                rec(m - 1, new_rem)

    rec(d - 1, bound_sq)
    if tight_vectors:
        for tv in (tight_vectors[0], tight_vectors[-1]):
            qf = sum(tv[i] * G_int[i][j] * tv[j] for i in range(d) for j in range(d))
            assert qf == bound_sq
    return violations, best_sq, tight_vectors


def round_robin_contacts(pair_buckets):
    max_len = max((len(b) for b in pair_buckets), default=0)
    for off in range(max_len):
        for b in pair_buckets:
            if off < len(b):
                yield b[off]


def incremental_q_rank_95(pair_buckets, rank_upper):
    """Exact Q-rank of 95-column bilateral translate contact-Jacobian via fractions.Fraction."""
    pivots = {}
    for (i, j, _z, w_cov) in round_robin_contacts(pair_buckets):
        if len(pivots) == rank_upper:
            break
        raw = [0] * 95
        if j > 0:
            for m in range(19):
                raw[(j - 1) * 19 + m] += w_cov[m]
        if i > 0:
            for m in range(19):
                raw[(i - 1) * 19 + m] -= w_cov[m]
        if not any(raw):
            continue
        vec = [Fraction(v, 1) for v in raw]
        for pcol in sorted(pivots.keys()):
            val = vec[pcol]
            if val != 0:
                prow = pivots[pcol]
                for c in range(pcol, 95):
                    if prow[c] != 0:
                        vec[c] -= val * prow[c]
        for c in range(95):
            if vec[c] != 0:
                inv = Fraction(1, 1) / vec[c]
                pivots[c] = [vec[k] * inv for k in range(95)]
                break
    return len(pivots)


def certify_bilateral_contact_rank_285(pair_buckets, comp, n_comp):
    """
    Deductive exact Q-rank certificate on the 285-column bilateral bar-framework contact Jacobian
    (190 symmetric metric-strain columns + 95 relative translate-shift columns):
      1. Upper bound over Q: each non-root connected component k in 1..n_comp-1 yields
         19 linearly independent integer vectors verified to annihilate 100% of rows in Z.
      2. Lower bound over Q: exact Gaussian elimination over Mersenne prime field F_P
         (P = 2^61 - 1 = 2305843009213693951) exhibits rank_upper independent pivots,
         certifying a non-zero integer minor mod P and hence non-zero over Q.
    """
    for k in range(1, n_comp):
        assert comp[0] != k
        for b in pair_buckets:
            for (i, j, _z, w_cov) in b:
                coeff = (1 if comp[j] == k else 0) - (1 if comp[i] == k else 0)
                if coeff != 0:
                    for m in range(19):
                        assert coeff * w_cov[m] == 0

    rank_upper = 285 - 19 * (n_comp - 1)
    prime = (1 << 61) - 1
    pivots = {}
    for (i, j, z_int, w_cov) in round_robin_contacts(pair_buckets):
        if len(pivots) == rank_upper:
            break
        row = []
        for a in range(19):
            row.append((z_int[a] * z_int[a]) % prime)
            for b_idx in range(a + 1, 19):
                row.append((2 * z_int[a] * z_int[b_idx]) % prime)
        tpart = [0] * 95
        if j > 0:
            base = (j - 1) * 19
            for m in range(19):
                tpart[base + m] += w_cov[m]
        if i > 0:
            base = (i - 1) * 19
            for m in range(19):
                tpart[base + m] -= w_cov[m]
        for v in tpart:
            row.append(v % prime)

        for pcol in sorted(pivots.keys()):
            val = row[pcol]
            if val:
                prow = pivots[pcol]
                for c in range(pcol, 285):
                    if prow[c]:
                        row[c] = (row[c] - val * prow[c]) % prime
        for c in range(285):
            if row[c]:
                inv = pow(row[c], prime - 2, prime)
                pivots[c] = [(row[k] * inv) % prime for k in range(285)]
                break

    rank_lower = len(pivots)
    assert rank_lower == rank_upper
    return rank_lower


def solve_leech_coords(vec24, leech_B):
    """Solve y * leech_B == vec24 (upper-triangular 24x24) and return exact integer y in Z^24."""
    rem = [int(v) for v in vec24]
    y = [0] * 24
    for i in range(24):
        piv = int(leech_B[i][i])
        if rem[i] % piv != 0:
            raise AssertionError("Vector not in Z-span of leech_B")
        yi = rem[i] // piv
        y[i] = yi
        if yi != 0:
            for c in range(i, 24):
                rem[c] -= yi * int(leech_B[i][c])
    assert all(r == 0 for r in rem)
    return y


def independent_snf_invariant_factors(Y_int):
    """Compute exact integer Smith Normal Form diagonal of k x 24 integer matrix from scratch."""
    k, n = len(Y_int), len(Y_int[0])
    M = [[int(x) for x in row] for row in Y_int]
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
            if bj != p:
                for i in range(k):
                    M[i][p], M[i][bj] = M[i][bj], M[i][p]
            if M[p][p] < 0:
                M[p] = [-x for x in M[p]]
            changed = False
            for i in range(p + 1, k):
                if M[i][p] != 0:
                    q = M[i][p] // M[p][p]
                    for j in range(p, n):
                        M[i][j] -= q * M[p][j]
                    if M[i][p] != 0:
                        changed = True
            for j in range(p + 1, n):
                if M[p][j] != 0:
                    q = M[p][j] // M[p][p]
                    for i in range(p, k):
                        M[i][j] -= q * M[i][p]
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
                continue
            break
    return [M[i][i] for i in range(k)]


def verify_d19_entry(entry, expected_name, leech_B, corrupt=False):
    assert entry["name"] == expected_name
    A = entry["leech_section_A_scaled"]
    ZA_T = entry["leech_section_A_right_inv_T_5x24"]
    B_orig = entry["leech_complement_B_original_scaled"]
    U_lll = entry["unimodular_U_lll"]
    det_U_cert = int(entry["det_U_lll"])
    B_lll = entry["leech_complement_B_lll_scaled"]
    ZB_T = entry["leech_complement_B_lll_right_inv_T_19x24"]
    G = entry["gram_G_19x19"]
    R_cert = [[parse_frac(x) for x in row] for row in entry["cholesky_R_19x19"]]
    D_cert = [parse_frac(x) for x in entry["cholesky_D_19"]]
    den_c = int(entry["translates_basis_coords_den"])
    C_num = [row[:] for row in entry["translates_basis_coords_num"]]
    den_amb = int(entry["translates_ambient_24d_den"])
    T_amb = entry["translates_ambient_24d_num"]

    if corrupt:
        C_num[2][1] -= 25

    YA = [solve_leech_coords(row, leech_B) for row in A]
    for row in B_orig:
        solve_leech_coords(row, leech_B)
    YB = [solve_leech_coords(row, leech_B) for row in B_lll]

    # Verify both right-inverse witness AND independent Smith Normal Form saturation in Lambda_24
    for a in range(5):
        for b in range(5):
            assert sum(YA[a][c] * ZA_T[b][c] for c in range(24)) == (1 if a == b else 0)
    for a in range(19):
        for b in range(19):
            assert sum(YB[a][c] * ZB_T[b][c] for c in range(24)) == (1 if a == b else 0)
    assert independent_snf_invariant_factors(YA) == [1] * 5
    assert independent_snf_invariant_factors(YB) == [1] * 19
    leech_sat = True

    K_sec = [[Fraction(sum(A[i][c] * A[j][c] for c in range(24)), 8) for j in range(5)] for i in range(5)]
    assert all(x.denominator == 1 for row in K_sec for x in row)
    det_K, _ = exact_det_and_inv_fraction([[int(x) for x in row] for row in K_sec])
    assert det_K == Fraction(300, 1)

    det_U, _ = exact_det_and_inv_fraction(U_lll)
    assert det_U == Fraction(det_U_cert, 1) and det_U in (Fraction(-1, 1), Fraction(1, 1))
    for i in range(19):
        for c in range(24):
            assert sum(U_lll[i][k] * B_orig[k][c] for k in range(19)) == B_lll[i][c]
        for r in range(5):
            assert sum(B_lll[i][c] * A[r][c] for c in range(24)) == 0
    for i in range(19):
        for j in range(19):
            assert sum(B_lll[i][c] * B_lll[j][c] for c in range(24)) == 8 * G[i][j]

    det_G_lu, G_inv = exact_det_and_inv_fraction(G)
    assert det_G_lu == Fraction(300, 1)

    if not corrupt:
        assert len(T_amb) == 6 and T_amb[0] == [0] * 24 and C_num[0] == [0] * 19
        for s_idx in range(6):
            assert len(T_amb[s_idx]) == 24 and len(C_num[s_idx]) == 19
            assert all(0 <= C_num[s_idx][m] < den_c for m in range(19))
            for r in range(5):
                assert sum(T_amb[s_idx][c] * A[r][c] for c in range(24)) == 0
            diff24 = [
                Fraction(T_amb[s_idx][c], den_amb)
                - sum(Fraction(C_num[s_idx][m], den_c) * B_lll[m][c] for m in range(19))
                for c in range(24)
            ]
            rhs = [sum(diff24[c] * B_lll[m][c] for c in range(24)) / 8 for m in range(19)]
            q_vec = [sum(rhs[k] * G_inv[k][m] for k in range(19)) for m in range(19)]
            assert all(x.denominator == 1 for x in q_vec)
            for c in range(24):
                assert sum(int(q_vec[m]) * B_lll[m][c] for m in range(19)) == diff24[c]

    R, D = independent_cholesky_fraction(G)
    assert R == R_cert and D == D_cert
    det_G = Fraction(1, 1)
    for dm in D:
        det_G *= dm
    assert det_G == Fraction(300, 1)

    viol0, best0, tight0 = fp_enumerate_fraction(R, D, G, [Fraction(0, 1)] * 19, Fraction(4, 1), skip_zero=True)
    if not corrupt:
        assert viol0 == 0 and best0 == Fraction(4, 1)
    norm4_L = len(tight0)

    c_vecs = [[Fraction(C_num[i][m], den_c) for m in range(19)] for i in range(6)]
    for i in range(6):
        for j in range(i + 1, 6):
            assert not all((c_vecs[j][m] - c_vecs[i][m]).denominator == 1 for m in range(19))

    # Intrinsic maximal translation group check: (c_i + c_s) mod Z^19 preserves {c_0..c_5} mod Z^19 iff s == 0
    sym_trans_stab = []
    for s in range(6):
        preserves = True
        for i in range(6):
            if not any(all((c_vecs[i][m] + c_vecs[s][m] - c_vecs[j][m]).denominator == 1 for m in range(19)) for j in range(6)):
                preserves = False
                break
        if preserves:
            sym_trans_stab.append(s)
    if not corrupt:
        assert sym_trans_stab == [0]
    sym_trans_stab_size = len(sym_trans_stab)

    target_sq = Fraction(52, 15)
    tau = [0] * 6
    adj = [[False] * 6 for _ in range(6)]
    tight_pairs = 0
    pair_buckets = []

    for i in range(6):
        for j in range(i + 1, 6):
            dc = [c_vecs[j][m] - c_vecs[i][m] for m in range(19)]
            viol, best_ij, tvecs = fp_enumerate_fraction(R, D, G, dc, target_sq, skip_zero=False)
            if viol > 0:
                if corrupt:
                    print(f"Corrupted packing rejected at pair ({i},{j}) with min_sq={best_ij}")
                    print("FAIL")
                    sys.exit(1)
                raise AssertionError(f"Pair ({i},{j}) violates min_sq")
            if tvecs:
                adj[i][j] = adj[j][i] = True
                tight_pairs += 1
                cnt = len(tvecs)
                tau[i] += cnt
                tau[j] += cnt
                bucket = []
                for yv in tvecs:
                    z_int = [int(yv[m] * den_c) for m in range(19)]
                    w_cov = [sum(G[m][l] * z_int[l] for l in range(19)) for m in range(19)]
                    bucket.append((i, j, z_int, w_cov))
                pair_buckets.append(bucket)

    if corrupt:
        raise AssertionError("Corrupted packing was not rejected")

    comp = [-1] * 6
    n_comp = 0
    for s in range(6):
        if comp[s] < 0:
            comp[s] = n_comp
            queue = [s]
            while queue:
                u = queue.pop(0)
                for v in range(6):
                    if adj[u][v] and comp[v] < 0:
                        comp[v] = n_comp
                        queue.append(v)
            n_comp += 1

    connected = (n_comp == 1)
    triangles = sum(1 for a in range(6) for b in range(a + 1, 6) for c in range(b + 1, 6) if adj[a][b] and adj[b][c] and adj[a][c])

    trans_rank_upper = 95 - 19 * (n_comp - 1)
    bilat_rank_full = certify_bilateral_contact_rank_285(pair_buckets, comp, n_comp)
    bilat_nullity_full = 285 - bilat_rank_full
    bilat_rank_trans = incremental_q_rank_95(pair_buckets, trans_rank_upper)
    assert bilat_rank_trans == trans_rank_upper
    bilat_nullity_trans = 95 - bilat_rank_trans
    tau_sorted = sorted(tau)
    tau_avg = Fraction(sum(tau), 6)

    exp = entry["expected_invariants"]
    assert int(det_G) == exp["det_G"]
    assert leech_sat == exp["leech_saturation_unimodular"]
    assert sym_trans_stab_size == exp["sym_trans_stabilizer_size"]
    assert parse_frac(exp["intra_lattice_min_sq"]) == Fraction(4, 1)
    assert norm4_L == exp["intra_lattice_norm4_count"]
    assert parse_frac(exp["packing_min_sq"]) == Fraction(52, 15)
    assert tau == exp["kissing_per_translate"]
    assert tau_sorted == exp["kissing_sorted"]
    assert min(tau) == exp["kissing_min"] and max(tau) == exp["kissing_max"]
    assert tau_avg == parse_frac(exp["kissing_avg"])
    assert tight_pairs == exp["tight_translate_pairs"]
    assert triangles == exp["translate_contact_triangles"]
    assert connected == exp["translate_contact_graph_connected"]
    assert bilat_rank_trans == exp["bilateral_contact_rank_trans"]
    assert bilat_nullity_trans == exp["bilateral_contact_nullity_trans"]
    assert bilat_rank_full == exp["bilateral_contact_rank_full"]
    assert bilat_nullity_full == exp["bilateral_contact_nullity_full"]

    print(
        f"[PY PROVED] {expected_name}: det(G)={int(det_G)}, leech_sat={int(leech_sat)}, "
        f"sym_trans_stab_size={sym_trans_stab_size}, norm4(L)={norm4_L}, min_sq=52/15, "
        f"tau_sorted={tuple(tau_sorted)}, min={min(tau)}, max={max(tau)}, avg={tau_avg}, "
        f"tight_pairs={tight_pairs}/15, triangles={triangles}, connected={connected}, "
        f"bilateral_contact_rank_trans={bilat_rank_trans}/95, bilateral_contact_nullity_trans={bilat_nullity_trans}, "
        f"bilateral_contact_rank_full={bilat_rank_full}/285, bilateral_contact_nullity_full={bilat_nullity_full}"
    )
    return {
        "det_G": det_G,
        "leech_sat": leech_sat,
        "sym_trans_stab_size": sym_trans_stab_size,
        "norm4_L": norm4_L,
        "tau_sorted": tau_sorted,
        "tau_min": min(tau),
        "tau_max": max(tau),
        "bilat_rank_trans": bilat_rank_trans,
        "bilat_nullity_trans": bilat_nullity_trans,
        "bilat_rank_full": bilat_rank_full,
        "bilat_nullity_full": bilat_nullity_full,
        "connected": connected,
    }


def main():
    if len(sys.argv) < 2:
        print("FAIL")
        sys.exit(1)
    corrupt_cli = (len(sys.argv) >= 3 and sys.argv[2] == "--corrupt")
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        cert = json.load(f)

    assert cert["schema"] == "v3r1t4s-periodic-sphere-packing-certificate-v2"
    assert cert["target_id"] == "cohn-sphere-packing-density-table"
    assert cert["claim_level"] == "partial_win_p1"
    assert int(cert["dimension"]) == 19
    assert int(cert["num_translates"]) == 6
    assert parse_frac(cert["minimal_squared_distance"]) == Fraction(52, 15)
    assert parse_frac(cert["packing_radius_squared"]) == Fraction(13, 15)
    assert cert["cohn_live_center_density_formula"] == "3^(-9) * 5^(-21/2) * 13^(19/2)"

    leech_B = cert["leech_lattice_basis_scaled_sqrt8"]
    assert len(leech_B) == 24 and all(len(r) == 24 for r in leech_B)
    det_l = 1
    for i in range(24):
        assert all(leech_B[i][j] == 0 for j in range(i))
        det_l *= int(leech_B[i][i])
    assert det_l == 2 ** 36

    if corrupt_cli:
        verify_d19_entry(cert["new_packing"], "P19_II_vtx", leech_B, corrupt=True)
        print("FAIL")
        sys.exit(1)

    e8 = cert["calibration_e8"]
    assert int(e8["dimension"]) == 8 and int(e8["num_translates"]) == 1
    R8_cert = [[parse_frac(x) for x in row] for row in e8["cholesky_R_8x8"]]
    D8_cert = [parse_frac(x) for x in e8["cholesky_D_8"]]
    R8, D8 = independent_cholesky_fraction(e8["gram_G_8x8"])
    assert R8 == R8_cert and D8 == D8_cert
    det8 = Fraction(1, 1)
    for d_i in D8:
        det8 *= d_i
    v8, b8, t8 = fp_enumerate_fraction(R8, D8, e8["gram_G_8x8"], [Fraction(0, 1)] * 8, Fraction(2, 1), skip_zero=True)
    cd8_sq = (Fraction(2, 4) ** 8) / det8
    assert det8 == int(e8["expected_det_G"]) == 1
    assert v8 == 0 and b8 == parse_frac(e8["expected_min_sq"]) == 2
    assert len(t8) == int(e8["expected_kissing"]) == 240
    assert cd8_sq == parse_frac(e8["expected_center_density_squared"]) == Fraction(1, 256)
    print("[PY CALIBRATION] E_8 verified: det=1, min_sq=2, kissing=240, center_density=1/16.")

    res_new = verify_d19_entry(cert["new_packing"], "P19_II_vtx", leech_B, corrupt=False)
    res_ref = verify_d19_entry(cert["reference_packing_chen2025"], "P19_ChenHuLiWangWu2025_ref", leech_B, corrupt=False)

    cd_sq_new = Fraction(36, 1) * (Fraction(13, 15) ** 19) / res_new["det_G"]
    cd_sq_cohn = Fraction(13 ** 19, (3 ** 18) * (5 ** 21))
    assert cd_sq_new == cd_sq_cohn
    assert str(cd_sq_new.numerator) == cert["center_density_squared_num"]
    assert str(cd_sq_new.denominator) == cert["center_density_squared_den"]
    print(
        f"[PY PROVED] Exact center density squared = {cd_sq_new.numerator} / {cd_sq_new.denominator} "
        f"== (3^(-9) * 5^(-21/2) * 13^(19/2))^2 (MATCHES COHN LIVE RECORD)."
    )

    assert res_new["leech_sat"] and res_ref["leech_sat"]
    assert res_new["sym_trans_stab_size"] == 1 and res_ref["sym_trans_stab_size"] == 1
    assert res_new["norm4_L"] != res_ref["norm4_L"]
    assert res_new["tau_sorted"] != res_ref["tau_sorted"]
    assert res_new["tau_max"] < res_ref["tau_min"]
    assert res_new["bilat_rank_trans"] == 95 and res_new["bilat_nullity_trans"] == 0
    assert res_new["bilat_rank_full"] == 285 and res_new["bilat_nullity_full"] == 0 and res_new["connected"]
    print(
        f"[PY PROVED] Strict Non-Isometry & Kissing-Stratum Vertex Isolation certified: "
        f"leech_sat=1; sym_trans_stab_size=1; norm4(L_new)={res_new['norm4_L']} != norm4(L_ref)={res_ref['norm4_L']}; "
        f"max(tau_new)={res_new['tau_max']} strictly_below min(tau_ref)={res_ref['tau_min']}; "
        f"bilateral_contact_rank_trans=95/95 (nullity=0); bilateral_contact_rank_full=285/285 (nullity=0)."
    )
    print("PY_VERIFIER: PASS")


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception as exc:
        print(f"Verification error: {exc}")
        print("FAIL")
        sys.exit(1)
