#!/usr/bin/env python3
"""Standalone pure-Python stdlib verifier for p2 (arXiv:2112.11766 Section 6 order-5 240-plane problem)."""
import sys

def mat_mul_f2(A, B):
    rA, cA, cB = len(A), len(A[0]), len(B[0])
    out = [[0] * cB for _ in range(rA)]
    for i in range(rA):
        for k in range(cA):
            if A[i][k]:
                for j in range(cB):
                    out[i][j] ^= B[k][j]
    return out

def is_rref_3x7(G):
    if len(G) != 3 or any(len(row) != 7 for row in G):
        return False
    if any(x not in (0, 1) for row in G for x in row):
        return False
    pivs = []
    for r in range(3):
        p = None
        for c in range(7):
            if G[r][c] == 1:
                p = c
                break
        if p is None:
            return False
        if pivs and p <= pivs[-1]:
            return False
        for r2 in range(3):
            if r2 != r and G[r2][p] != 0:
                return False
        pivs.append(p)
    return True

def verify_file(path):
    with open(path, "r") as f:
        tokens = [int(tok) for tok in f.read().split()]
    if len(tokens) < 50:
        return False, "File too short"
    pi = [tokens[7*r : 7*(r+1)] for r in range(7)]
    if any(x not in (0, 1) for row in pi for x in row):
        return False, "Non-binary entry in pi"
    n_planes = tokens[49]
    if n_planes != 240:
        return False, f"Expected 240 planes, got {n_planes}"
    if len(tokens) != 50 + 240 * 21:
        return False, f"Token count mismatch: {len(tokens)}"

    # 1. Check pi has exact order 5 in GL(7,2)
    I7 = [[1 if i == j else 0 for j in range(7)] for i in range(7)]
    if pi == I7:
        return False, "pi equals I_7 (order 1)"
    cur = pi
    for p in range(2, 6):
        cur = mat_mul_f2(cur, pi)
        if p < 5 and cur == I7:
            return False, f"pi has order {p} != 5"
    if cur != I7:
        return False, "pi^5 != I_7"

    # 2. Brute-force all 128 vectors of F_2^7 and find fixed-point space F = {v : v*pi = v}
    def apply_pi(v_bits):
        res = [0] * 7
        for r in range(7):
            if v_bits[r]:
                for c in range(7):
                    res[c] ^= pi[r][c]
        return tuple(res)

    all_vecs = [tuple((i >> b) & 1 for b in range(7)) for i in range(128)]
    zero = (0, 0, 0, 0, 0, 0, 0)
    F_vecs = {v for v in all_vecs if apply_pi(v) == v}
    if len(F_vecs) != 8:
        return False, f"Fixed subspace |F| = {len(F_vecs)} vectors (expected 8, i.e. 7 projective points)"
    # Check F is closed under addition
    for u in F_vecs:
        for w in F_vecs:
            if tuple(u[i] ^ w[i] for i in range(7)) not in F_vecs:
                return False, "F is not a linear subspace"
    F_nonzero = F_vecs - {zero}

    # 3. Parse all 240 planes, check RREF rank 3, distinctness, disjointness from F
    planes_pts = []
    seen_planes = set()
    for idx in range(240):
        base = 50 + idx * 21
        G = [tokens[base + 7*r : base + 7*(r+1)] for r in range(3)]
        if not is_rref_3x7(G):
            return False, f"Plane {idx} is not a rank-3 3x7 binary RREF matrix"
        # Generate all 8 vectors in rowspace(G)
        sub = set()
        for mask in range(8):
            vec = [0] * 7
            for r in range(3):
                if (mask >> r) & 1:
                    for c in range(7):
                        vec[c] ^= G[r][c]
            sub.add(tuple(vec))
        if len(sub) != 8:
            return False, f"Plane {idx} does not have 8 vectors"
        nz = frozenset(sub - {zero})
        if nz in seen_planes:
            return False, f"Duplicate plane at index {idx}"
        if nz & F_nonzero:
            return False, f"Plane {idx} intersects fixed plane F"
        seen_planes.add(nz)
        planes_pts.append(nz)

    # 4. Check pi-invariance of the 240-plane set
    for idx, nz in enumerate(planes_pts):
        img = frozenset(apply_pi(v) for v in nz)
        if img not in seen_planes:
            return False, f"Plane {idx} image under pi is not in C"

    # 5. Brute-force all 2,667 lines of F_2^7 and check each lies in at most 1 plane of C
    # Also check pairwise intersection directly
    line_cov = {}
    for nz in planes_pts:
        pts_list = sorted(nz)
        lines_in_plane = set()
        for i in range(7):
            for j in range(i + 1, 7):
                u, w = pts_list[i], pts_list[j]
                third = tuple(u[c] ^ w[c] for c in range(7))
                line = frozenset((u, w, third))
                lines_in_plane.add(line)
        if len(lines_in_plane) != 7:
            return False, "Plane failed to yield 7 lines"
        for line in lines_in_plane:
            cnt = line_cov.get(line, 0) + 1
            if cnt > 1:
                return False, "Two planes intersect in a line (line covered >= 2 times)"
            line_cov[line] = cnt

    if len(line_cov) != 240 * 7:
        return False, f"Expected 1680 covered lines, got {len(line_cov)}"

    # 6. Check point coverage on all 127 projective points
    pt_cov = {v: 0 for v in all_vecs if v != zero}
    for nz in planes_pts:
        for v in nz:
            pt_cov[v] += 1
    for v in F_nonzero:
        if pt_cov[v] != 0:
            return False, f"Fixed point {v} covered {pt_cov[v]} != 0 times"
    for v in all_vecs:
        if v != zero and v not in F_nonzero:
            if pt_cov[v] != 14:
                return False, f"Outside point {v} covered {pt_cov[v]} != 14 times"

    return True, "PASS: 240 distinct rank-3 planes, order-5 pi-invariant, disjoint from 7-pt F, 1680/2667 lines <=1, all 120 pts outside F covered 14x"

if __name__ == "__main__":
    ok, msg = verify_file(sys.argv[1])
    print(msg)
    sys.exit(0 if ok else 1)
