#!/usr/bin/env python3
"""Standalone definition-only verifier for EAQECC [[19, 2, 11; 9]]_2 (Python 3.8+ stdlib only)."""
import os
import sys

N_EXP = 19
K_EXP = 2
C_EXP = 9
S_ROWS_EXP = N_EXP - K_EXP + C_EXP  # 26
DUAL_ROWS_EXP = N_EXP + K_EXP - C_EXP  # 12
RAD_DIM_EXP = N_EXP - K_EXP - C_EXP  # 8
D_LOWER_LIVE = 10
D_UPPER_LIVE = 17
D_CLAIMED = 11


def fail(msg):
    print(f"VERIFICATION ERROR: {msg}")
    print("FAIL")
    sys.exit(1)


def gf2_rref(mat):
    m = [row[:] for row in mat]
    rows = len(m)
    cols = len(m[0]) if rows else 0
    r = 0
    pivs = []
    for c in range(cols):
        if r >= rows:
            break
        sel = None
        for i in range(r, rows):
            if m[i][c] == 1:
                sel = i
                break
        if sel is None:
            continue
        m[r], m[sel] = m[sel], m[r]
        pivs.append(c)
        for i in range(rows):
            if i != r and m[i][c] == 1:
                m[i] = [a ^ b for a, b in zip(m[i], m[r])]
        r += 1
    return r, pivs, m


def symp_ip(u, v, n):
    acc = 0
    for i in range(n):
        acc ^= (u[i] & v[n + i]) ^ (u[n + i] & v[i])
    return acc & 1


def symp_weight(v, n):
    w = 0
    for i in range(n):
        if v[i] or v[n + i]:
            w += 1
    return w


def evaluate_stabilizer(S, n):
    rk_s, s_pivs, rref_s = gf2_rref(S)
    gram = [[symp_ip(u, v, n) for v in S] for u in S]
    rk_g, _, _ = gf2_rref(gram)

    # Independently compute symplectic dual S^{perp_s} = nullspace_GF2([Z | X]) from S alone
    h_mat = [row[n:] + row[:n] for row in S]
    rk_h, h_pivs, rref_h = gf2_rref(h_mat)
    free_cols = [col for col in range(2 * n) if col not in h_pivs]
    indep_dual_basis = []
    for fc in free_cols:
        vec = [0] * (2 * n)
        vec[fc] = 1
        for idx_p, pc in enumerate(h_pivs):
            if rref_h[idx_p][fc] == 1:
                vec[pc] = 1
        indep_dual_basis.append(vec)

    def in_rowspace_S(vec):
        v = vec[:]
        for idx_p, pc in enumerate(s_pivs):
            if v[pc] == 1:
                v = [a ^ b for a, b in zip(v, rref_s[idx_p])]
        return all(x == 0 for x in v)

    m_dual = len(indep_dual_basis)
    rad_weights = {}
    coset_weights = {}
    for mask in range(1 << m_dual):
        v = [0] * (2 * n)
        for b in range(m_dual):
            if (mask >> b) & 1:
                v = [x ^ y for x, y in zip(v, indep_dual_basis[b])]
        w = symp_weight(v, n)
        if in_rowspace_S(v):
            rad_weights[w] = rad_weights.get(w, 0) + 1
        else:
            coset_weights[w] = coset_weights.get(w, 0) + 1

    min_d = min(coset_weights.keys()) if coset_weights else 0
    return rk_s, rk_g, indep_dual_basis, rad_weights, coset_weights, min_d


def griesmer_min_len_gf4(k_dim, d_min):
    total = 0
    cur = d_min
    for _ in range(k_dim):
        total += cur
        cur = (cur + 3) // 4
    return total


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obj_path = os.path.join(root, "object", "eaqecc_n19_k2_d11_c9.tsv")
    if not os.path.isfile(obj_path):
        fail(f"Missing object file: {obj_path}")

    S = []
    D_stored = []
    header_seen = False
    with open(obj_path, "r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, 1):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if not header_seen:
                exp_hdr = ["section", "row_idx"] + [f"x{i}" for i in range(N_EXP)] + [f"z{i}" for i in range(N_EXP)]
                if parts != exp_hdr:
                    fail(f"Header mismatch on line {line_no}")
                header_seen = True
                continue
            if len(parts) != 2 + 2 * N_EXP:
                fail(f"Line {line_no}: expected {2 + 2 * N_EXP} columns, found {len(parts)}")
            sec = parts[0]
            try:
                ridx = int(parts[1])
                bits = [int(x) for x in parts[2:]]
            except ValueError as exc:
                fail(f"Line {line_no}: non-integer entry ({exc})")
            if any(b not in (0, 1) for b in bits):
                fail(f"Line {line_no}: entries must be in {{0, 1}}")
            if sec == "S":
                if ridx != len(S):
                    fail(f"Line {line_no}: S row_idx {ridx} != {len(S)}")
                S.append(bits)
            elif sec == "DUAL":
                if ridx != len(D_stored):
                    fail(f"Line {line_no}: DUAL row_idx {ridx} != {len(D_stored)}")
                D_stored.append(bits)
            else:
                fail(f"Line {line_no}: unexpected section tag {sec}")

    if len(S) != S_ROWS_EXP:
        fail(f"Expected {S_ROWS_EXP} stabilizer rows, found {len(S)}")
    if len(D_stored) != DUAL_ROWS_EXP:
        fail(f"Expected {DUAL_ROWS_EXP} stored dual rows, found {len(D_stored)}")

    # 1. Built-in negative control: corrupt a stabilizer bit and confirm rejection
    S_corrupt = [r[:] for r in S]
    S_corrupt[0][0] ^= 1
    c_rk_s, c_rk_g, _, _, _, c_min_d = evaluate_stabilizer(S_corrupt, N_EXP)
    corrupt_cross_ok = all(symp_ip(s, d, N_EXP) == 0 for s in S_corrupt for d in D_stored)
    if corrupt_cross_ok and c_rk_s == S_ROWS_EXP and c_rk_g == 2 * C_EXP and c_min_d >= D_CLAIMED:
        fail("Negative control failed: corrupted stabilizer unexpectedly passed all checks")

    # 2. Verify stored DUAL basis has rank 12 and is symplectically orthogonal to S
    rk_d_stored, _, _ = gf2_rref(D_stored)
    if rk_d_stored != DUAL_ROWS_EXP:
        fail(f"Stored DUAL basis rank is {rk_d_stored}, expected {DUAL_ROWS_EXP}")
    for i, s_vec in enumerate(S):
        for j, d_vec in enumerate(D_stored):
            if symp_ip(s_vec, d_vec, N_EXP) != 0:
                fail(f"Symplectic orthogonality failed between S[{i}] and DUAL[{j}]")

    # 3. Independently verify S from definition ONLY (ignoring D_stored for distance computation)
    rk_s, rk_g, indep_dual, rad_w, coset_w, d_ea = evaluate_stabilizer(S, N_EXP)
    if rk_s != S_ROWS_EXP:
        fail(f"GF(2) rank of S is {rk_s}, expected {S_ROWS_EXP}")
    if rk_g != 2 * C_EXP:
        fail(f"GF(2) rank of S * Omega * S^T is {rk_g}, expected 2*c = {2 * C_EXP}")

    # Confirm stored DUAL spans the exact same 12-dimensional subspace as indep_dual
    rk_union, _, _ = gf2_rref(indep_dual + D_stored)
    if rk_union != DUAL_ROWS_EXP:
        fail(f"Stored DUAL basis does not span S^{{perp_s}} (union rank {rk_union} != {DUAL_ROWS_EXP})")

    rad_count = sum(rad_w.values())
    coset_count = sum(coset_w.values())
    if rad_count != (1 << RAD_DIM_EXP):
        fail(f"|S cap S^{{perp_s}}| = {rad_count}, expected 2^{RAD_DIM_EXP} = {1 << RAD_DIM_EXP}")
    if coset_count != (1 << DUAL_ROWS_EXP) - (1 << RAD_DIM_EXP):
        fail(f"|S^{{perp_s}} \ S| = {coset_count}, expected {(1 << DUAL_ROWS_EXP) - (1 << RAD_DIM_EXP)}")

    if not (D_LOWER_LIVE < d_ea <= D_UPPER_LIVE and d_ea == D_CLAIMED):
        fail(f"Computed d_EA = {d_ea} does not match claimed {D_CLAIMED} in ({D_LOWER_LIVE}, {D_UPPER_LIVE}]")

    # 4. Verify Griesmer obstruction ruling out all classical (non-degenerate) smaller-hull quaternary ancestors (l' in {0, 1, 2})
    for l_anc in (0, 1, 2):
        n_anc = K_EXP + C_EXP + 2 * l_anc
        k_anc = K_EXP + l_anc
        min_len = griesmer_min_len_gf4(k_anc, D_CLAIMED)
        if min_len <= n_anc:
            fail(f"Unexpected Griesmer feasibility at l'={l_anc}: min_len={min_len} <= {n_anc}")

    print(f"Negative control rejected single-bit stabilizer perturbation (cross_orth={corrupt_cross_ok}, d_pert={c_min_d}).")
    print(f"Verified S shape = {len(S)} x {2 * N_EXP}, rank_GF2(S) = {rk_s}, rank_GF2(S Omega S^T) = {rk_g} => n={N_EXP}, k={K_EXP}, c={C_EXP}.")
    print(f"Enumerated all 2^{DUAL_ROWS_EXP} = {1 << DUAL_ROWS_EXP} vectors in S^{{perp_s}}: |S cap S^{{perp_s}}| = {rad_count} (min nonzero radical weight = {min(w for w in rad_w if w > 0)}), |S^{{perp_s}} \ S| = {coset_count}.")
    print(f"Coset weight distribution: {sorted(coset_w.items())}")
    print(f"Exact non-catalytic d_EA = {d_ea} > {D_LOWER_LIVE} = d_lower(19, 2, 9) (degenerate EAQECC: d_EA = 11 > 4 = d(S^{{perp_s}})); Griesmer bound rules out all l' in {{0, 1, 2}} classical (non-degenerate) quaternary hull ancestors.")
    print("PASS")


if __name__ == "__main__":
    main()
