#!/usr/bin/env python3
"""
Standalone exact from-definition verifier for qutrit EAQECCs [[n, k, d; c]]_3.

Takes a JSON file containing:
  n, k, c, d_claimed, S
where S is an s x 2n matrix with entries in {0, 1, 2} over GF(3).

Verifies:
1. S has dimensions s x 2n with entries in {0, 1, 2}.
2. rank_GF3(S) == s.
3. Symplectic commutation matrix Omega = S * J * S^T mod 3, where J = [[0, I_n], [-I_n, 0]].
4. c == rank_GF3(Omega) // 2, c >= 1, and k == n - s + c.
5. Computes exact basis for span(S)^perp = {v in GF(3)^(2n) : S * J * v^T == 0 mod 3} (dim 2n - s)
   and isotropic subgroup I = span(S) cap span(S)^perp (dim s - 2c).
6. Exhaustively enumerates ALL 3^(2n - s) - 1 nonzero vectors in span(S)^perp, computing both:
   - d_pure = min_{v in span(S)^perp \ {0}} wt_symp(v)
   - d_ea   = min_{v in span(S)^perp \ I}   wt_symp(v)
7. Parses data/qutrit.php.html and verifies d_lower < d_ea <= d_upper and d_ea == d_claimed (and not excluded).
"""

import json
import os
import re
import sys
import time


def rref_gf3(mat, ncols):
    """Returns (rref_rows, pivot_cols) over GF(3)."""
    rows = [r[:] for r in mat]
    nrows = len(rows)
    pivots = []
    r = 0
    for c in range(ncols):
        if r >= nrows:
            break
        piv = None
        for i in range(r, nrows):
            if rows[i][c] % 3 != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = rows[r][c] % 3  # in GF(3), inv(1)=1, inv(2)=2
        rows[r] = [(x * inv) % 3 for x in rows[r]]
        for i in range(nrows):
            if i != r and rows[i][c] % 3 != 0:
                factor = rows[i][c] % 3
                rows[i] = [(rows[i][j] - factor * rows[r][j]) % 3 for j in range(ncols)]
        pivots.append(c)
        r += 1
    return rows[:r], pivots


def nullspace_gf3(mat, ncols):
    """Returns a basis of {v in GF(3)^ncols : mat * v^T == 0 mod 3}."""
    rref, pivots = rref_gf3(mat, ncols)
    piv_set = set(pivots)
    free_cols = [c for c in range(ncols) if c not in piv_set]
    basis = []
    for fc in free_cols:
        v = [0] * ncols
        v[fc] = 1
        for idx, pc in enumerate(pivots):
            v[pc] = (-rref[idx][fc]) % 3
        basis.append(v)
    return basis


def symp_inner(u, v, n):
    """Computes u * J * v^T mod 3 where J = [[0, I_n], [-I_n, 0]]."""
    s = 0
    for i in range(n):
        s += u[i] * v[n + i] - u[n + i] * v[i]
    return s % 3


def in_span_gf3(v, rref_rows, pivots, ncols):
    """Checks if v is in the row span of rref_rows."""
    rem = v[:]
    for idx, pc in enumerate(pivots):
        coeff = rem[pc] % 3
        if coeff != 0:
            row = rref_rows[idx]
            for j in range(pc, ncols):
                rem[j] = (rem[j] - coeff * row[j]) % 3
    return all(x % 3 == 0 for x in rem)


def parse_html_table(html_path):
    """Parses qutrit.php.html and returns dict mapping (n, k, c) -> (d_lower, d_upper, title)."""
    with open(html_path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    pattern = re.compile(r'title="([^"]*)">\[\[(\d+),(\d+),(\d+)(?:-(\d+))?;(\d+)\]\]')
    cells = {}
    for m in pattern.finditer(text):
        title = m.group(1)
        n = int(m.group(2))
        k = int(m.group(3))
        dl = int(m.group(4))
        du = int(m.group(5)) if m.group(5) else dl
        c = int(m.group(6))
        cells[(n, k, c)] = (dl, du, title)
    return cells


def verify_certificate(cert_path, html_path):
    t0 = time.time()
    with open(cert_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    n = int(data["n"])
    k = int(data["k"])
    c = int(data["c"])
    d_claimed = int(data["d_claimed"])
    S = data["S"]

    assert (n, k, c) not in [(14, 3, 5), (33, 1, 24)], f"Cell {(n, k, c)} is excluded by open PR constraint!"
    assert n >= 1 and k >= 1 and c >= 1, f"Invalid parameters n={n}, k={k}, c={c} (require k>=1, c>=1)"

    s = len(S)
    ncols = 2 * n
    assert s >= 1, "S must be non-empty"
    for row in S:
        assert len(row) == ncols, f"Row length {len(row)} != 2n = {ncols}"
        for val in row:
            assert val in (0, 1, 2), f"Invalid entry {val} not in {{0,1,2}}"

    # 1. Check rank_GF3(S) == s
    rref_S, pivots_S = rref_gf3(S, ncols)
    rank_S = len(rref_S)
    assert rank_S == s, f"rank_GF3(S) = {rank_S} != s = {s}"

    # 2. Compute symplectic product matrix Omega = S * J * S^T mod 3
    Omega = [[symp_inner(S[i], S[j], n) for j in range(s)] for i in range(s)]
    rref_Omega, _ = rref_gf3(Omega, s)
    rank_Omega = len(rref_Omega)
    assert rank_Omega % 2 == 0, f"rank_GF3(Omega) = {rank_Omega} is odd!"
    c_calc = rank_Omega // 2
    assert c_calc == c, f"Computed c = {c_calc} != claimed c = {c}"
    k_calc = n - s + c
    assert k_calc == k, f"Computed k = n - s + c = {k_calc} != claimed k = {k}"

    # 3. Compute basis for span(S)^perp = {v in GF(3)^(2n) : S * J * v^T == 0 mod 3}
    # Note: (S * J)_{i, j} = S_{i, j-n} for j >= n, and -S_{i, j+n} for j < n.
    SJ = [[(-S[i][n + j]) % 3 for j in range(n)] + [S[i][j] % 3 for j in range(n)] for i in range(s)]
    perp_basis = nullspace_gf3(SJ, ncols)
    m = len(perp_basis)
    assert m == 2 * n - s, f"dim(span(S)^perp) = {m} != 2n - s = {2 * n - s}"

    # 4. Compute isotropic subgroup I = span(S) cap span(S)^perp
    # A vector u = sum_i a_i S_i in span(S) is in span(S)^perp iff Omega * a^T == 0 mod 3.
    iso_coeffs = nullspace_gf3(Omega, s)
    r_iso = len(iso_coeffs)
    assert r_iso == s - 2 * c, f"dim(I) = {r_iso} != s - 2c = {s - 2 * c}"
    I_basis = []
    for coeff in iso_coeffs:
        vec = [sum(coeff[i] * S[i][j] for i in range(s)) % 3 for j in range(ncols)]
        assert in_span_gf3(vec, rref_S, pivots_S, ncols), "Isotropic vector not in span(S)"
        for i in range(s):
            assert symp_inner(S[i], vec, n) == 0, "Isotropic vector not orthogonal to S"
        I_basis.append(vec)
    rref_I, pivots_I = rref_gf3(I_basis, ncols)
    assert len(rref_I) == r_iso, f"rank(I_basis) = {len(rref_I)} != {r_iso}"

    # Reorder/construct ordered basis of span(S)^perp where first r_iso rows are rref_I
    # and remaining 2k rows extend rref_I to a full basis of span(S)^perp.
    ordered_basis = [row[:] for row in rref_I]
    cur_rref, cur_pivs = rref_gf3(ordered_basis, ncols) if ordered_basis else ([], [])
    for vec in perp_basis:
        if not in_span_gf3(vec, cur_rref, cur_pivs, ncols):
            ordered_basis.append(vec[:])
            cur_rref, cur_pivs = rref_gf3(ordered_basis, ncols)
    assert len(ordered_basis) == m, f"ordered_basis len {len(ordered_basis)} != {m}"

    # Verify ordered_basis spans the exact same subspace as perp_basis and first r_iso span I
    for vec in ordered_basis[:r_iso]:
        assert in_span_gf3(vec, rref_I, pivots_I, ncols)
    for idx in range(r_iso, m):
        assert not in_span_gf3(ordered_basis[idx], rref_I, pivots_I, ncols)

    # 5. Exhaustively enumerate ALL 3^m - 1 nonzero vectors in span(S)^perp
    # Pack each vector into (lo, hi) 2n-bit masks for fast exact enumeration
    basis_lo = []
    basis_hi = []
    basis_lo2 = []
    basis_hi2 = []
    for vec in ordered_basis:
        lo = 0
        hi = 0
        for idx, val in enumerate(vec):
            if val == 1:
                lo |= (1 << idx)
            elif val == 2:
                hi |= (1 << idx)
        basis_lo.append(lo)
        basis_hi.append(hi)
        basis_lo2.append(hi)  # 2 * v swaps lo and hi!
        basis_hi2.append(lo)

    mask_n = (1 << n) - 1

    # Split basis into first r_iso vectors (spanning I) and remaining 2k = m - r_iso vectors (complement L)
    # Every vector in span(S)^perp is uniquely u_I + u_L with u_I in I (3^r_iso choices) and u_L in L (3^(2k) choices).
    # Wait: if r_iso is very small or large, we can split the m basis vectors at mid = m // 2 for balanced tables,
    # while tracking whether the vector lies in I (which happens iff all coordinates >= r_iso are 0!).
    def generate_half(b_lo, b_hi, b_lo2, b_hi2):
        res = [(0, 0, True)]  # (lo, hi, is_zero)
        for i in range(len(b_lo)):
            lo1, hi1 = b_lo[i], b_hi[i]
            lo2, hi2 = b_lo2[i], b_hi2[i]
            new_res = list(res)
            for l0, h0, _ in res:
                # add (lo1, hi1)
                nl1 = (l0 & ~(lo1 | hi1)) | (lo1 & ~(l0 | h0)) | (h0 & hi1)
                nh1 = (h0 & ~(lo1 | hi1)) | (hi1 & ~(l0 | h0)) | (l0 & lo1)
                new_res.append((nl1, nh1, False))
                # add (lo2, hi2)
                nl2 = (l0 & ~(lo2 | hi2)) | (lo2 & ~(l0 | h0)) | (h0 & hi2)
                nh2 = (h0 & ~(lo2 | hi2)) | (hi2 & ~(l0 | h0)) | (l0 & lo2)
                new_res.append((nl2, nh2, False))
            res = new_res
        return res

    # Split at mid = min(max(r_iso, m // 2), m) if we want, or simply split at mid = m // 2
    # and track `outside_I` for each half!
    mid = m // 2
    left_list = [(0, 0, False)]  # (lo, hi, has_non_I_component)
    for i in range(mid):
        lo1, hi1 = basis_lo[i], basis_hi[i]
        lo2, hi2 = basis_lo2[i], basis_hi2[i]
        non_i = (i >= r_iso)
        new_list = list(left_list)
        for l0, h0, ni0 in left_list:
            nl1 = (l0 & ~(lo1 | hi1)) | (lo1 & ~(l0 | h0)) | (h0 & hi1)
            nh1 = (h0 & ~(lo1 | hi1)) | (hi1 & ~(l0 | h0)) | (l0 & lo1)
            new_list.append((nl1, nh1, ni0 or non_i))
            nl2 = (l0 & ~(lo2 | hi2)) | (lo2 & ~(l0 | h0)) | (h0 & hi2)
            nh2 = (h0 & ~(lo2 | hi2)) | (hi2 & ~(l0 | h0)) | (l0 & lo2)
            new_list.append((nl2, nh2, ni0 or non_i))
        left_list = new_list

    right_list = [(0, 0, False)]
    for i in range(mid, m):
        lo1, hi1 = basis_lo[i], basis_hi[i]
        lo2, hi2 = basis_lo2[i], basis_hi2[i]
        non_i = (i >= r_iso)
        new_list = list(right_list)
        for l0, h0, ni0 in right_list:
            nl1 = (l0 & ~(lo1 | hi1)) | (lo1 & ~(l0 | h0)) | (h0 & hi1)
            nh1 = (h0 & ~(lo1 | hi1)) | (hi1 & ~(l0 | h0)) | (l0 & lo1)
            new_list.append((nl1, nh1, ni0 or non_i))
            nl2 = (l0 & ~(lo2 | hi2)) | (lo2 & ~(l0 | h0)) | (h0 & hi2)
            nh2 = (h0 & ~(lo2 | hi2)) | (hi2 & ~(l0 | h0)) | (l0 & lo2)
            new_list.append((nl2, nh2, ni0 or non_i))
        right_list = new_list

    total_enumerated = 0
    total_non_iso = 0
    d_pure = n + 1
    d_ea = n + 1

    pop16 = [bin(i).count("1") for i in range(65536)]
    if n <= 16:
        for lR, hR, niR in right_list:
            zR = ~(lR | hR)
            for lL, hL, niL in left_list:
                nl = (lL & zR) | (lR & ~(lL | hL)) | (hL & hR)
                nh = (hL & zR) | (hR & ~(lL | hL)) | (lL & lR)
                nz = nl | nh
                if nz == 0:
                    continue
                total_enumerated += 1
                wt = pop16[(nz & mask_n) | (nz >> n)]
                if wt < d_pure:
                    d_pure = wt
                if (niL or niR):
                    total_non_iso += 1
                    if wt < d_ea:
                        d_ea = wt
    else:
        for lR, hR, niR in right_list:
            zR = ~(lR | hR)
            for lL, hL, niL in left_list:
                nl = (lL & zR) | (lR & ~(lL | hL)) | (hL & hR)
                nh = (hL & zR) | (hR & ~(lL | hL)) | (lL & lR)
                nz = nl | nh
                if nz == 0:
                    continue
                total_enumerated += 1
                supp = (nz & mask_n) | (nz >> n)
                wt = pop16[supp & 0xFFFF] + pop16[(supp >> 16) & 0xFFFF] + pop16[supp >> 32]
                if wt < d_pure:
                    d_pure = wt
                if (niL or niR):
                    total_non_iso += 1
                    if wt < d_ea:
                        d_ea = wt

    expected_total = (3 ** m) - 1
    expected_non_iso = (3 ** m) - (3 ** r_iso)
    assert total_enumerated == expected_total, f"Enumerated {total_enumerated} != {expected_total}"
    assert total_non_iso == expected_non_iso, f"Enumerated non-iso {total_non_iso} != {expected_non_iso}"
    assert d_ea == d_claimed, f"Computed exact d_ea = {d_ea} != d_claimed = {d_claimed}"

    # 6. Compare against data/qutrit.php.html
    cells = parse_html_table(html_path)
    assert (n, k, c) in cells, f"Cell {(n, k, c)} not found in {html_path}!"
    d_lower, d_upper, title = cells[(n, k, c)]
    assert d_ea > d_lower, f"d_ea = {d_ea} is NOT strictly greater than d_lower = {d_lower}!"
    assert d_ea <= d_upper, f"d_ea = {d_ea} exceeds d_upper = {d_upper}!"

    elapsed = time.time() - t0
    receipt = {
        "certificate": os.path.basename(cert_path),
        "parameters": f"[[{n}, {k}, {d_ea}; {c}]]_3",
        "n": n,
        "k": k,
        "c": c,
        "s": s,
        "m_dual_dim": m,
        "r_isotropic_dim": r_iso,
        "vectors_enumerated": total_enumerated,
        "non_isotropic_vectors_enumerated": total_non_iso,
        "d_pure": d_pure,
        "d_ea": d_ea,
        "d_claimed": d_claimed,
        "table_d_lower": d_lower,
        "table_d_upper": d_upper,
        "table_previous_entry": f"[[{n},{k},{d_lower}-{d_upper};{c}]]_3 ({title})",
        "improvement": d_ea - d_lower,
        "verified": True,
        "elapsed_seconds": round(elapsed, 4),
    }
    print(json.dumps(receipt, indent=2))
    return receipt


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 verify_eaqecc.py {cert.json} [data/qutrit.php.html]", file=sys.stderr)
        sys.exit(1)
    cert_file = sys.argv[1]
    html_file = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(os.path.dirname(__file__), "data", "qutrit.php.html")
    verify_certificate(cert_file, html_file)
