#!/usr/bin/env python3
r"""
verify.py
=========
Standalone, zero-dependency first-principles verifier for the
`magic-state-distillation-fewest-qubits` submission package (`CONFIRMED_PARTIAL`: `p1, p2`).

Requires ONLY Python 3.8+ standard library and `numpy`.
Verifies from first principles:
  1. All 6 constructive tightness witnesses in `object/constructive_tightness_witnesses.json`:
     - Exact triorthogonality Eqs. (18a)-(18d) for T-to-T and Eqs. (40a)-(40d) for T-to-CCZ.
     - Exact fault distance d in {3, 4, 5} by Eq. (19) and Eq. (42) over F_2.
     - Master Theorem 3a (Hyperplane Parity Split Law: u0 odd, u1 even across all 2^r - 1 covectors).
     - Master Theorem 4 (Parity-Extension Lifting Theorem: even-n d=4 on N -> odd-(n+1) d=5 on N+1).
  2. Milestone p1 certificate in `object/p1_p2_lower_bound_certificates.json` (N_CCZ(4) = 10):
     - Exact weight enumerator of all 2^22 = 4,194,304 codewords of RM(2, 6) (0 codewords in [49, 63]).
     - Exact collinear-triple rank 57/63 on X = F_2^6 \ {0} (dim(V_4(X)/L_X) = 6 - 6 = 0 < 3).
     - Exhaustive F_2-linear Fredholm/quotient sweep across all 912 pointed supports of m <= 6 (1 <= n <= 63),
       confirming 0 SAT hits for N <= 9, d >= 4 T-to-CCZ and 0 SAT hits for N <= 7, d >= 4 T-to-T.
  3. Milestone p2 certificate in `object/p1_p2_lower_bound_certificates.json` (N_T(4) >= 9):
     - Handle 1 (Pairwise Orbit Disjointness): computes AGL(7,2)-invariant WL2 + T3_ker + pt_f01 signatures
       across all 3,486 RM(3, 7) classes (3,484 unique signatures + proves the 2 complement collision pairs
       non-isomorphic via exact pruned AGL(7,2) search).
     - Handle 2 (Exact Stabilizer Orders): verifies every generator matrix is invertible in GL(7,2) and
       preserves f_i, and computes the exact subgroup order via an 8-level Schreier-Sims stabilizer chain
       on base B = (0, 1, 2, 4, 8, 16, 32, 64) matching stab_size on all 3,486 classes.
     - Handle 3 (Exact 2^64 Orbit Mass & Full 128-Shift Sweep): verifies sum |AGL(7,2)| / stab_size == 2^64
       and sweeps all 3,486 * 128 = 446,208 shifted supports (400,256 with n >= 55) via the exact F_2-linear
       Fredholm Alternative, confirming 0 SAT hits for N <= 8, d >= 4 T-to-T across all 1 <= n <= 127.

Usage:
  python3 verify-it-yourself/verify.py
  python3 verify-it-yourself/verify.py --corrupt
"""
from __future__ import annotations

import argparse
import copy
import json
import sys
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
OBJ_DIR = PKG_ROOT / "object"

AGL7_ORDER = 128 * 163849992929280
BASE = (0, 1, 2, 4, 8, 16, 32, 64)
ID_G = ((1, 2, 4, 8, 16, 32, 64), 0)
X128 = np.arange(128, dtype=np.int32)
XOR128 = X128[:, None] ^ X128[None, :]


def fail(msg: str) -> int:
    print(f"VERIFICATION ERROR: {msg}")
    print("FAIL")
    return 1


def sm64(z):
    z = (z + np.uint64(0x9E3779B97F4A7C15))
    z = (z ^ (z >> np.uint64(30))) * np.uint64(0xBF58476D1CE4E5B9)
    z = (z ^ (z >> np.uint64(27))) * np.uint64(0x94D049BB133111EB)
    return z ^ (z >> np.uint64(31))


def insert_pivot(vec: int, pivots: dict[int, int]) -> bool:
    while vec:
        b = vec.bit_length() - 1
        p = pivots.get(b)
        if p is None:
            pivots[b] = vec
            return True
        vec ^= p
    return False


def reduce_vec(vec: int, pivots: dict[int, int]) -> int:
    while vec:
        b = vec.bit_length() - 1
        p = pivots.get(b)
        if p is None:
            break
        vec ^= p
    return vec


def anf_to_mask(anf_s: str, m: int = 7) -> int:
    if not isinstance(anf_s, str) or not anf_s.strip():
        return -1
    terms = anf_s.strip().split("+")
    mono_masks = []
    for t in terms:
        t = t.strip()
        if t == "0":
            continue
        elif t == "1":
            mono_masks.append(0)
        else:
            if len(t) > 3:
                return -1
            mm = 0
            for ch in t:
                idx = ord(ch) - ord("a")
                if idx < 0 or idx >= m or (mm & (1 << idx)):
                    return -1
                mm |= (1 << idx)
            mono_masks.append(mm)
    mask = 0
    for x in range(1 << m):
        val = 0
        for mm in mono_masks:
            if (x & mm) == mm:
                val ^= 1
        if val:
            mask |= (1 << x)
    return mask


def check_support_T_d4(X_pts: list[int], r: int) -> tuple[bool, int]:
    n = len(X_pts)
    if n == 0:
        return False, 0
    pivots: dict[int, int] = {}
    coord_masks = [0] * r
    for idx, x in enumerate(X_pts):
        bit = 1 << idx
        for a in range(r):
            if (x >> a) & 1:
                coord_masks[a] |= bit
    for a in range(r):
        insert_pivot(coord_masks[a], pivots)
    for a in range(r):
        ca = coord_masks[a]
        for b in range(a + 1, r):
            insert_pivot(ca & coord_masks[b], pivots)
    target = (1 << n) - 1
    if reduce_vec(target, pivots) == 0:
        return False, n - len(pivots)
    pos = {x: idx for idx, x in enumerate(X_pts)}
    for i in range(n):
        xi = X_pts[i]
        bi = 1 << i
        for j in range(i + 1, n):
            k = pos.get(xi ^ X_pts[j])
            if k is not None and k > j:
                if insert_pivot(bi | (1 << j) | (1 << k), pivots):
                    if reduce_vec(target, pivots) == 0:
                        return False, n - len(pivots)
    return True, n - len(pivots)


def check_support_CCZ_d4(X_pts: list[int], r: int) -> tuple[bool, int]:
    n = len(X_pts)
    if n < 7:
        return False, 0
    pivots: dict[int, int] = {}
    coord_masks = [0] * r
    for idx, x in enumerate(X_pts):
        bit = 1 << idx
        for a in range(r):
            if (x >> a) & 1:
                coord_masks[a] |= bit
    l_pivots: dict[int, int] = {}
    for a in range(r):
        insert_pivot(coord_masks[a], l_pivots)
    rank_L = len(l_pivots)
    insert_pivot((1 << n) - 1, pivots)
    for a in range(r):
        insert_pivot(coord_masks[a], pivots)
    for a in range(r):
        ca = coord_masks[a]
        for b in range(a + 1, r):
            insert_pivot(ca & coord_masks[b], pivots)
    max_pivots = n - rank_L - 3
    if len(pivots) > max_pivots:
        return False, n - len(pivots) - rank_L
    pos = {x: idx for idx, x in enumerate(X_pts)}
    for i in range(n):
        xi = X_pts[i]
        bi = 1 << i
        for j in range(i + 1, n):
            k = pos.get(xi ^ X_pts[j])
            if k is not None and k > j:
                if insert_pivot(bi | (1 << j) | (1 << k), pivots):
                    if len(pivots) > max_pivots:
                        return False, n - len(pivots) - rank_L
    q_dim = n - len(pivots) - rank_L
    if q_dim < 3:
        return False, q_dim
    free_cols = [c for c in range(n) if c not in pivots]
    ker_basis = []
    for fc in free_cols:
        vec = 1 << fc
        for b in sorted(pivots.keys()):
            p = pivots[b]
            if (p & vec).bit_count() & 1:
                vec |= (1 << b)
        red = reduce_vec(vec, l_pivots)
        if red:
            insert_pivot(red, l_pivots)
            ker_basis.append(vec)
    all_vecs = [0]
    for b_vec in ker_basis:
        all_vecs += [v ^ b_vec for v in all_vecs]
    all_vecs = all_vecs[1:]
    adj = {u: set() for u in all_vecs}
    for i, u in enumerate(all_vecs):
        for j in range(i + 1, len(all_vecs)):
            v = all_vecs[j]
            uv = u & v
            if (uv.bit_count() & 1) == 0 and all(((uv & cm).bit_count() & 1) == 0 for cm in coord_masks):
                adj[u].add(v)
                adj[v].add(u)
    for u in all_vecs:
        au = adj[u]
        for v in au:
            if v > u:
                for w in (au & adj[v]):
                    if w > v and ((u & v & w).bit_count() & 1) == 1:
                        return True, q_dim
    return False, q_dim


def check_T_matrix(G_arr: np.ndarray) -> tuple[bool, int]:
    N, n = G_arr.shape
    w1 = [int(G_arr[i].sum() % 2) for i in range(N)]
    ok_w1 = (w1[0] == 1) and all(x == 0 for x in w1[1:])
    ok_w2 = all(int((G_arr[i] & G_arr[j]).sum() % 2) == 0 for i, j in combinations(range(N), 2))
    ok_w3 = all(int((G_arr[i] & G_arr[j] & G_arr[k]).sum() % 2) == 0 for i, j, k in combinations(range(N), 3))
    cols = [int(sum(int(G_arr[r, c]) << r for r in range(N))) for c in range(n)]
    col_set = set(cols)
    d = 5
    if 1 in col_set:
        d = 1
    elif any((c ^ 1) in col_set for c in cols):
        d = 2
    elif any((cols[i] ^ cols[j] ^ 1) in col_set for i, j in combinations(range(n), 2)):
        d = 3
    else:
        pair_sums = {cols[i] ^ cols[j] for i, j in combinations(range(n), 2)}
        if any((p ^ 1) in pair_sums for p in pair_sums):
            d = 4
    return (ok_w1 and ok_w2 and ok_w3), d


def check_CCZ_matrix(G_arr: np.ndarray) -> tuple[bool, int]:
    A = G_arr.copy()
    A[2:] = np.bitwise_xor.accumulate(G_arr[2:], axis=0)
    N, n = A.shape
    ok1 = all(int(A[i].sum() % 2) == 0 for i in range(N))
    ok2 = all(int((A[i] & A[j]).sum() % 2) == 0 for i, j in combinations(range(N), 2))
    ok3 = True
    for i, j, k in combinations(range(N), 3):
        s = int((A[i] & A[j] & A[k]).sum() % 2)
        if i == 0 and j == 1:
            if s != 1:
                ok3 = False
        else:
            if s != 0:
                ok3 = False
    E_C = set()
    for i in (0, 1):
        for j in (0, 1):
            for k in (0, 1):
                if (i, j, k) != (0, 0, 0):
                    vec = [j, k] + [i] * (N - 2)
                    E_C.add(sum(vec[r] << r for r in range(N)))
    cols = [int(sum(int(A[r, c]) << r for r in range(N))) for c in range(n)]
    col_set = set(cols)
    d = 5
    if any(c in E_C for c in cols):
        d = 1
    elif any((c ^ e) in col_set for c in cols for e in E_C):
        d = 2
    elif any((cols[i] ^ cols[j] ^ e) in col_set for i, j in combinations(range(n), 2) for e in E_C):
        d = 3
    else:
        pair_sums = {cols[i] ^ cols[j] for i, j in combinations(range(n), 2)}
        if any((p ^ e) in pair_sums for p in pair_sums for e in E_C):
            d = 4
    return (ok1 and ok2 and ok3), d


def verify_constructive_witnesses(cw: dict) -> tuple[bool, str]:
    witnesses = cw.get("witnesses", [])
    if len(witnesses) != 6:
        return False, f"Expected 6 constructive witnesses, got {len(witnesses)}"

    w_by_id = {}
    for w in witnesses:
        wid = w.get("id", "<unknown>")
        G_list = w.get("G", [])
        N = w.get("N")
        k = w.get("k")
        r = w.get("r")
        n = w.get("n")
        d_exp = w.get("d")
        if not isinstance(G_list, list) or len(G_list) != N or N - k != r:
            return False, f"{wid}: invalid dimensions N={N}, k={k}, r={r}"
        for row in G_list:
            if not isinstance(row, list) or len(row) != n or any(x not in (0, 1) for x in row):
                return False, f"{wid}: matrix G contains non-binary entry or wrong column count"
        G_arr = np.array(G_list, dtype=np.uint8)
        w_by_id[wid] = G_arr

        if w.get("protocol_type") == "T_to_CCZ":
            ok_alg, d_act = check_CCZ_matrix(G_arr)
            if not ok_alg or d_act != d_exp:
                return False, f"{wid}: CCZ verification failed (ok_alg={ok_alg}, d_act={d_act}, d_exp={d_exp})"
        elif w.get("protocol_type") == "T_to_T":
            ok_alg, d_act = check_T_matrix(G_arr)
            if not ok_alg or d_act != d_exp:
                return False, f"{wid}: T-to-T verification failed (ok_alg={ok_alg}, d_act={d_act}, d_exp={d_exp})"

            # Verify Master Theorem 3a (Hyperplane Parity Split Law) across all 2^r - 1 covectors
            col_u: dict[int, int] = {}
            col_c: dict[int, int] = {}
            for c_idx in range(n):
                u_bit = int(G_arr[0, c_idx])
                mask = 0
                for rw in range(1, N):
                    if G_arr[rw, c_idx]:
                        mask |= (1 << (rw - 1))
                if mask != 0:
                    col_c[mask] = col_c.get(mask, 0) ^ 1
                    col_u[mask] = col_u.get(mask, 0) ^ u_bit
            X = sorted(m for m, cnt in col_c.items() if cnt == 1)
            u_map = {m: col_u[m] for m in X}
            min_w0 = len(X) + 1
            best_split = None
            for v in range(1, 1 << r):
                X0 = [x for x in X if ((x & v).bit_count() & 1) == 0]
                X1 = [x for x in X if ((x & v).bit_count() & 1) == 1]
                u0 = sum(u_map[x] for x in X0)
                u1 = sum(u_map[x] for x in X1)
                if (u0 & 1) != 1 or (u1 & 1) != 0:
                    return False, f"{wid}: Hyperplane Parity Split Law violated at v={v} (u0={u0}, u1={u1})"
                if len(X0) < min_w0:
                    min_w0 = len(X0)
                    best_split = [v, len(X0), len(X1), u0, u1]
            if w.get("min_w0_split") != best_split:
                return False, f"{wid}: min_w0_split mismatch: got {best_split}, expected {w.get('min_w0_split')}"
        else:
            return False, f"{wid}: unknown protocol_type {w.get('protocol_type')}"

    # Verify Master Theorem 4 (Parity-Extension Lifting Theorem: even-n d=4 on N=10 -> odd-(n+1) d=5 on N=11)
    for base_id in ("W3_52T_to_1T_N10_d4", "W4_64T_to_1T_N10_d4"):
        G_base = w_by_id[base_id]
        N_b, n_b = G_base.shape
        G_lift = np.zeros((N_b + 1, n_b + 1), dtype=np.uint8)
        G_lift[0, :n_b] = G_base[0]
        G_lift[1, :n_b] = G_base[0] ^ 1
        G_lift[1, n_b] = 1
        G_lift[2:, :n_b] = G_base[1:]
        ok_lift, d_lift = check_T_matrix(G_lift)
        if not ok_lift or d_lift != 5:
            return False, f"Master Theorem 4 parity-extension lift failed on {base_id}"

    return True, "Verified all 6 constructive tightness witnesses (W1..W6), Master Theorem 3a (Hyperplane Parity Split), and Master Theorem 4 (Parity-Extension Lift)"


def verify_p1_certificate(p1: dict) -> tuple[bool, str]:
    # 1. Recompute exact weight enumerator of all 2^22 = 4,194,304 codewords of RM(2, 6)
    X6 = np.arange(64, dtype=np.uint8)
    bits6 = ((X6[:, None] >> np.arange(6)) & 1).astype(np.uint8)
    basis_rm26 = [np.ones(64, dtype=np.uint8)]
    for i in range(6):
        basis_rm26.append(bits6[:, i])
    for i, j in combinations(range(6), 2):
        basis_rm26.append(bits6[:, i] & bits6[:, j])
    B26 = np.array(basis_rm26, dtype=np.uint8)
    masks26 = np.array([sum(int(B26[r, c]) << c for c in range(64)) for r in range(22)], dtype=np.uint64)
    low11 = np.zeros(1 << 11, dtype=np.uint64)
    high11 = np.zeros(1 << 11, dtype=np.uint64)
    for b in range(11):
        low11[((np.arange(1 << 11) >> b) & 1) == 1] ^= masks26[b]
        high11[((np.arange(1 << 11) >> b) & 1) == 1] ^= masks26[b + 11]
    all_cw = low11[:, None] ^ high11[None, :]
    c = all_cw - ((all_cw >> np.uint64(1)) & np.uint64(0x5555555555555555))
    c = (c & np.uint64(0x3333333333333333)) + ((c >> np.uint64(2)) & np.uint64(0x3333333333333333))
    c = (c + (c >> np.uint64(4))) & np.uint64(0x0F0F0F0F0F0F0F0F)
    pop_cw = ((c * np.uint64(0x0101010101010101)) >> np.uint64(56)).astype(np.int32)
    w_dist = np.bincount(pop_cw.ravel(), minlength=65)
    nz_weights = [[int(w), int(w_dist[w])] for w in range(65) if w_dist[w] > 0]
    if p1.get("rm26_weight_enumerator") != nz_weights:
        return False, f"p1: RM(2,6) weight enumerator mismatch: got {nz_weights}"
    if any(49 <= w <= 63 and cnt > 0 for w, cnt in nz_weights):
        return False, "p1: unexpected codeword weight in [49, 63]"

    # 2. Analytic & exact collinear-triple rank check on X = F_2^6 \ {0} (n = 63)
    X63 = list(range(1, 64))
    l_pivs: dict[int, int] = {}
    for a in range(6):
        cm = sum((1 << idx) for idx, x in enumerate(X63) if (x >> a) & 1)
        insert_pivot(cm, l_pivs)
    col_pivs: dict[int, int] = {}
    pos63 = {x: idx for idx, x in enumerate(X63)}
    for i in range(63):
        xi = X63[i]
        bi = 1 << i
        for j in range(i + 1, 63):
            k = pos63.get(xi ^ X63[j])
            if k is not None and k > j:
                insert_pivot(bi | (1 << j) | (1 << k), col_pivs)
    col_rank = len(col_pivs)
    rank_L = len(l_pivs)
    dim_V4 = 63 - col_rank
    qdim = dim_V4 - rank_L
    n63_inv = [63, col_rank, rank_L, dim_V4, qdim]
    if p1.get("n63_full_space_invariants") != n63_inv or qdim != 0:
        return False, f"p1: n=63 full-space invariants mismatch: got {n63_inv}"

    # 3. Exhaustive sweep across all 16 affine seeds and 912 pointed supports for m <= 6
    seeds = p1.get("m_le_6_affine_seeds", [])
    if len(seeds) != 16:
        return False, f"p1: expected 16 affine seeds for m<=6, got {len(seeds)}"
    seen_seeds = set()
    m6_supports_tested = 0
    m6_t_sat = 0
    m6_ccz_sat = 0
    for item in seeds:
        if not isinstance(item, list) or len(item) != 2:
            return False, "p1: malformed seed entry"
        m, mono_masks = item[0], tuple(item[1])
        if m not in (4, 5, 6) or any(not isinstance(mm, int) or mm < 0 or mm >= (1 << m) or mm.bit_count() > m - 4 for mm in mono_masks):
            return False, f"p1: invalid seed degree or range in {item}"
        if (m, mono_masks) in seen_seeds:
            return False, f"p1: duplicate seed {item}"
        seen_seeds.add((m, mono_masks))
        Y = {x for x in range(1 << m) if sum((x & mm) == mm for mm in mono_masks) % 2 == 1}
        for b in range(1 << m):
            X = sorted((x ^ b) for x in Y if (x ^ b) != 0)
            m6_supports_tested += 1
            sat_t, _ = check_support_T_d4(X, m)
            if sat_t:
                m6_t_sat += 1
            sat_ccz, _ = check_support_CCZ_d4(X, m)
            if sat_ccz:
                m6_ccz_sat += 1
            if m <= 5 and len(Y) > 0:
                X_hyp = sorted((x | (1 << m)) for x in Y)
                m6_supports_tested += 1
                if check_support_T_d4(X_hyp, m + 1)[0]:
                    m6_t_sat += 1
                if check_support_CCZ_d4(X_hyp, m + 1)[0]:
                    m6_ccz_sat += 1

    summary_act = [len(seeds), m6_supports_tested, m6_t_sat, m6_ccz_sat]
    if p1.get("expected_summary") != summary_act or m6_t_sat != 0 or m6_ccz_sat != 0:
        return False, f"p1: summary mismatch: got {summary_act}, expected {p1.get('expected_summary')}"

    return True, "Verified Milestone p1 (N_CCZ(4) = 10 & N=7 T-to-T control across all 4,194,304 RM(2,6) codewords and 912 pointed supports)"


def agl_apply(g, x: int) -> int:
    rows, tr = g
    res = tr
    for i in range(7):
        if (x >> i) & 1:
            res ^= rows[i]
    return res


def agl_mul(g1, g2):
    r1, b1 = g1
    r2, b2 = g2
    return (tuple(agl_apply((r1, 0), r2[i]) for i in range(7)), agl_apply(g1, b2))


def agl_inv(g):
    rows, tr = g
    aug = [(rows[i] << 7) | (1 << i) for i in range(7)]
    for col in range(7):
        piv = None
        for r in range(col, 7):
            if (aug[r] >> (col + 7)) & 1:
                piv = r
                break
        if piv is None:
            return None
        aug[col], aug[piv] = aug[piv], aug[col]
        for r in range(7):
            if r != col and ((aug[r] >> (col + 7)) & 1):
                aug[r] ^= aug[col]
    inv_rows = tuple(aug[col] & 0x7F for col in range(7))
    return (inv_rows, agl_apply((inv_rows, 0), tr))


def _verify_p2_chunk(chunk):
    """Worker verifying a slice of RM(3,7) orbits: Schreier-Sims stabilizer order, WL2+T3 signature, and all 128 shifts."""
    out = []
    for idx, entry in chunk:
        if not isinstance(entry, list) or len(entry) != 3:
            return None
        anf, stab_size, gens_raw = entry
        mask = anf_to_mask(anf, 7)
        if mask < 0 or not isinstance(stab_size, int) or stab_size <= 0 or AGL7_ORDER % stab_size != 0:
            return None
        f = np.array([(mask >> i) & 1 for i in range(128)], dtype=np.int64)

        # Verify generators and compute exact 8-level Schreier-Sims order
        gens = []
        seen_g = set()
        for gr in gens_raw:
            if not isinstance(gr, list) or len(gr) != 8 or any(not isinstance(v, int) or v < 0 or v > 127 for v in gr):
                return None
            g = (tuple(gr[:7]), gr[7])
            if g in seen_g or agl_inv(g) is None:
                return None
            seen_g.add(g)
            for x in range(128):
                if f[agl_apply(g, x)] != f[x]:
                    return None
            gens.append(g)

        level_gens = [list(gens)] + [[] for _ in range(7)]
        trans = [{BASE[i]: ID_G} for i in range(8)]
        inv_trans = [{BASE[i]: ID_G} for i in range(8)]

        def sift(g, start_lvl=0):
            for i in range(start_lvl, 8):
                pt = agl_apply(g, BASE[i])
                u = inv_trans[i].get(pt)
                if u is None:
                    return i, g
                g = agl_mul(u, g)
            return 8, g

        def rebuild(i):
            orb, inv_orb, q = {BASE[i]: ID_G}, {BASE[i]: ID_G}, [BASE[i]]
            gens_i = [h for j in range(i, 8) for h in level_gens[j]]
            while q:
                x = q.pop()
                ux = orb[x]
                for h in gens_i:
                    y = agl_apply(h, x)
                    if y not in orb:
                        uy = agl_mul(h, ux)
                        inv_uy = agl_inv(uy)
                        if inv_uy is None:
                            return False
                        orb[y], inv_orb[y] = uy, inv_uy
                        q.append(y)
            trans[i], inv_trans[i] = orb, inv_orb
            return True

        for i in range(8):
            if not rebuild(i):
                return None
        i = 7
        while i >= 0:
            added = False
            for x, ux in list(trans[i].items()):
                for h in [h for j in range(i, 8) for h in level_gens[j]]:
                    lvl, rem = sift(agl_mul(h, ux), i)
                    if lvl < 8:
                        level_gens[lvl].append(rem)
                        for k in range(lvl + 1):
                            if not rebuild(k):
                                return None
                        i, added = lvl, True
                        break
                if added:
                    break
            if not added:
                i -= 1
        ord_ss = 1
        for i in range(8):
            ord_ss *= len(trans[i])
        if ord_ss != stab_size:
            return None

        # Compute AGL(7,2)-invariant signature (WL2 + T3_ker + pt_f01_sig)
        F = f[XOR128]
        D = f[:, None] ^ F
        Df = D * f[:, None]
        w_d = D.sum(axis=0).astype(np.uint64)
        G1 = (D.T @ D).astype(np.uint64)
        G2 = (Df.T @ Df).astype(np.uint64)
        G3 = (D.T @ Df).astype(np.uint64)
        pair_feat = (
            G1 + (G2 << np.uint64(8)) + (G3 << np.uint64(16)) +
            (G1[X128[:, None], XOR128] << np.uint64(24)) +
            (G2[X128[:, None], XOR128] << np.uint64(32)) +
            (G3[X128[:, None], XOR128] << np.uint64(40)) +
            (w_d[None, :] << np.uint64(48)) + (w_d[XOR128] << np.uint64(56))
        )
        H_pair = sm64(pair_feat)
        H_pair[:, 0] = 0
        c_dir1 = sm64(w_d + H_pair.sum(axis=1) ^ np.bitwise_xor.reduce(H_pair, axis=1))
        c_dir1[0] = 0
        pt_feat1 = sm64((f[:, None].astype(np.uint64) << np.uint64(62)) ^ (F.astype(np.uint64) << np.uint64(61)) ^ c_dir1[None, :])
        pt_feat1[:, 0] = 0
        c_pt1 = sm64(pt_feat1.sum(axis=1) ^ np.bitwise_xor.reduce(pt_feat1, axis=1))
        c_pt_xor = c_pt1[XOR128]
        dir_from_pt = sm64(c_pt1[:, None] + c_pt_xor + (D.astype(np.uint64) << np.uint64(60))).sum(axis=0)
        dir_from_dir = sm64(H_pair ^ c_dir1[None, :] ^ (c_dir1[XOR128] * np.uint64(0x9E3779B97F4A7C15))).sum(axis=1)
        c_dir2 = sm64(c_dir1 ^ dir_from_pt ^ dir_from_dir)
        c_dir2[0] = 0
        pt_deriv = sm64((D.astype(np.uint64) * c_dir2[None, :]).sum(axis=1) ^ np.bitwise_xor.reduce(D.astype(np.uint64) * c_dir1[None, :], axis=1))
        by_c: dict[int, list[int]] = {}
        for x in range(128):
            by_c.setdefault(int(pt_deriv[x]), [0, 0])[int(f[x])] += 1
        pt_f01_sig = tuple(sorted((k, v[0], v[1]) for k, v in by_c.items()))

        B0 = f[0] ^ f[:, None] ^ f[None, :] ^ F
        # Because d3 -> T3(d1, d2, d3) is F_2-linear in d3, T3(d1, d2, :) == 0 on F_2^7
        # iff T3(d1, d2, 2^k) == 0 for the 7 standard basis vectors 2^k in {1, 2, 4, 8, 16, 32, 64}!
        nz_mask = np.zeros((128, 128), dtype=np.int64)
        for k_b in range(7):
            eb = 1 << k_b
            nz_mask |= (B0 ^ B0[:, eb : eb + 1] ^ B0[:, XOR128[:, eb]])
        T3_ker = np.sort((nz_mask[1:, :] == 0).sum(axis=1)).tolist()
        sig = (int(f.sum()), tuple(T3_ker), tuple(np.sort(c_dir2[1:]).tolist()), pt_f01_sig)

        # Partition {0..127} into verified H_i-orbits (plus translation periods) and check each representative
        # Since every generator in gens is verified in GL(7,2) and preserves Y_pts, (Y ^ b2)\{0} = L((Y ^ b1)\{0})
        Y_pts = [x for x in range(128) if f[x] == 1]
        w_Y = len(Y_pts)
        col_locked = 0
        if w_Y >= 56:
            X0 = [x for x in Y_pts if x != 0]
            l_p: dict[int, int] = {}
            for a in range(7):
                insert_pivot(sum((1 << idx_x) for idx_x, x in enumerate(X0) if (x >> a) & 1), l_p)
            c_p: dict[int, int] = {}
            pos0 = {x: idx_x for idx_x, x in enumerate(X0)}
            for i1 in range(len(X0)):
                xi = X0[i1]
                bi = 1 << i1
                for j1 in range(i1 + 1, len(X0)):
                    k1 = pos0.get(xi ^ X0[j1])
                    if k1 is not None and k1 > j1:
                        insert_pivot(bi | (1 << j1) | (1 << k1), c_p)
            if len(X0) - len(c_p) == len(l_p):
                col_locked = 1

        visited = [False] * 128
        shifts_ge55 = 0
        sat_hits = 0
        for start in range(128):
            if visited[start]:
                continue
            orb_sz = 1
            visited[start] = True
            q_orb = [start]
            while q_orb:
                cur = q_orb.pop()
                for g in gens:
                    nxt = agl_apply(g, cur)
                    if not visited[nxt]:
                        visited[nxt] = True
                        orb_sz += 1
                        q_orb.append(nxt)
            Xb = sorted((y ^ start) for y in Y_pts if (y ^ start) != 0)
            n_x = len(Xb)
            if n_x >= 55:
                shifts_ge55 += orb_sz
            if n_x == 0:
                continue
            c_masks = [0] * 7
            pos = [-1] * 128
            for i_x, x in enumerate(Xb):
                pos[x] = i_x
                bit = 1 << i_x
                for a in range(7):
                    if (x >> a) & 1:
                        c_masks[a] |= bit
            basis = [0] * n_x

            def add_row(v: int) -> bool:
                while v:
                    msb = v.bit_length() - 1
                    bv = basis[msb]
                    if bv == 0:
                        basis[msb] = v
                        return True
                    v ^= bv
                return False

            def in_span(v: int) -> bool:
                while v:
                    msb = v.bit_length() - 1
                    bv = basis[msb]
                    if bv == 0:
                        return False
                    v ^= bv
                return True

            for a in range(7):
                add_row(c_masks[a])
            for a in range(7):
                ca = c_masks[a]
                for a2 in range(a + 1, 7):
                    add_row(ca & c_masks[a2])
            all_ones = (1 << n_x) - 1
            if in_span(all_ones):
                continue
            resolved = False
            for i_x in range(n_x):
                xi = Xb[i_x]
                bi = 1 << i_x
                for j_x in range(i_x + 1, n_x):
                    k_x = pos[xi ^ Xb[j_x]]
                    if k_x > j_x:
                        if add_row(bi | (1 << j_x) | (1 << k_x)):
                            if in_span(all_ones):
                                resolved = True
                                break
                if resolved:
                    break
            if not resolved and not in_span(all_ones):
                sat_hits += orb_sz

        out.append((idx, sig, stab_size, 128, shifts_ge55, sat_hits, 1 if w_Y >= 56 else 0, col_locked))
    return out


def are_agl_isomorphic(anf1: str, anf2: str) -> bool:
    def feat(anf_s: str):
        m_b = anf_to_mask(anf_s, 7)
        f_v = np.array([(m_b >> i) & 1 for i in range(128)], dtype=np.int64)
        F_v = f_v[XOR128]
        D_v = f_v[:, None] ^ F_v
        Df_v = D_v * f_v[:, None]
        w_v = D_v.sum(axis=0).astype(np.uint64)
        G1_v = (D_v.T @ D_v).astype(np.uint64)
        G2_v = (Df_v.T @ Df_v).astype(np.uint64)
        G3_v = (D_v.T @ Df_v).astype(np.uint64)
        pf = (
            G1_v + (G2_v << np.uint64(8)) + (G3_v << np.uint64(16)) +
            (G1_v[X128[:, None], XOR128] << np.uint64(24)) +
            (G2_v[X128[:, None], XOR128] << np.uint64(32)) +
            (G3_v[X128[:, None], XOR128] << np.uint64(40)) +
            (w_v[None, :] << np.uint64(48)) + (w_v[XOR128] << np.uint64(56))
        )
        Hp = sm64(pf)
        Hp[:, 0] = 0
        cd1 = sm64(w_v + Hp.sum(axis=1) ^ np.bitwise_xor.reduce(Hp, axis=1))
        cd1[0] = 0
        pf1 = sm64((f_v[:, None].astype(np.uint64) << np.uint64(62)) ^ (F_v.astype(np.uint64) << np.uint64(61)) ^ cd1[None, :])
        pf1[:, 0] = 0
        cp1 = sm64(pf1.sum(axis=1) ^ np.bitwise_xor.reduce(pf1, axis=1))
        cpx = cp1[XOR128]
        dfp = sm64(cp1[:, None] + cpx + (D_v.astype(np.uint64) << np.uint64(60))).sum(axis=0)
        dfd = sm64(Hp ^ cd1[None, :] ^ (cd1[XOR128] * np.uint64(0x9E3779B97F4A7C15))).sum(axis=1)
        cd2 = sm64(cd1 ^ dfp ^ dfd)
        cd2[0] = 0
        ptd = sm64((D_v.astype(np.uint64) * cd2[None, :]).sum(axis=1) ^ np.bitwise_xor.reduce(D_v.astype(np.uint64) * cd1[None, :], axis=1))
        wd_i = D_v.sum(axis=0)
        return f_v, Hp, [(int(f_v[x]), int(ptd[x])) for x in range(128)], [(int(wd_i[d]), int(cd2[d])) for d in range(128)]

    f1, H1, pt1, dir1 = feat(anf1)
    f2, H2, pt2, dir2 = feat(anf2)

    def can_map(lvl, b, span_map):
        if lvl == 7:
            return True
        target_sub = f1[1 << lvl : 2 << lvl]
        req_dir = dir1[1 << lvl]
        for v in range(1, 128):
            if dir2[v] != req_dir:
                continue
            ok = True
            for idx_s, sx in enumerate(span_map):
                ny = sx ^ v
                if ny == b or f2[ny] != target_sub[idx_s] or pt2[ny] != pt1[(1 << lvl) | idx_s] or H2[v, sx ^ b] != H1[1 << lvl, idx_s]:
                    ok = False
                    break
            if ok and can_map(lvl + 1, b, span_map + [sx ^ v for sx in span_map]):
                return True
        return False

    return any(pt2[b] == pt1[0] and can_map(0, b, [b]) for b in range(128))


def verify_p2_certificate(p2: dict) -> tuple[bool, str]:
    if p2.get("agl7_order") != AGL7_ORDER or p2.get("total_rm37_codewords_pow2") != 64:
        return False, "p2: agl7_order or total_rm37_codewords_pow2 mismatch"
    orbits = p2.get("rm37_orbits", [])
    if len(orbits) != 3486:
        return False, f"p2: expected 3,486 RM(3,7) orbits, got {len(orbits)}"

    indexed = list(enumerate(orbits))
    chunks = [indexed[i::16] for i in range(16)]
    try:
        with ProcessPoolExecutor(max_workers=4) as ex:
            chunk_results = list(ex.map(_verify_p2_chunk, chunks))
    except Exception:
        chunk_results = [_verify_p2_chunk(c) for c in chunks]

    if any(cr is None for cr in chunk_results):
        return False, "p2: Schreier-Sims stabilizer or generator verification failed on one or more RM(3,7) classes"

    flat_res = [item for cr in chunk_results for item in cr]
    flat_res.sort(key=lambda x: x[0])
    sigs: dict[tuple, int] = {}
    collision_pairs = []
    orbit_mass_sum = 0
    total_shifts = 0
    shifts_ge55 = 0
    sat_hits = 0
    ge56_cnt = 0
    col_locked_cnt = 0

    for idx, sig, stab_size, sh_tot, sh_55, hits, is_ge56, locked in flat_res:
        if sig in sigs:
            collision_pairs.append([sigs[sig], idx])
        else:
            sigs[sig] = idx
        orbit_mass_sum += AGL7_ORDER // stab_size
        total_shifts += sh_tot
        shifts_ge55 += sh_55
        sat_hits += hits
        ge56_cnt += is_ge56
        col_locked_cnt += locked

    if orbit_mass_sum != (1 << 64):
        return False, f"p2: orbit mass sum {orbit_mass_sum} != 2^64"
    if p2.get("complement_collision_pairs") != collision_pairs:
        return False, f"p2: complement_collision_pairs mismatch: got {collision_pairs}"
    for i, j in collision_pairs:
        if are_agl_isomorphic(orbits[i][0], orbits[j][0]):
            return False, f"p2: collision pair ({i}, {j}) is isomorphic"

    summary_act = [len(orbits), len(sigs), total_shifts, shifts_ge55, sat_hits, ge56_cnt, col_locked_cnt]
    if p2.get("expected_summary") != summary_act or sat_hits != 0:
        return False, f"p2: summary mismatch: got {summary_act}, expected {p2.get('expected_summary')}"

    return True, "Verified Milestone p2 (N_T(4) >= 9 across all 3,486 RM(3,7) orbits, 6,074,355 disjoint pairs, 2^64 orbit mass, and 446,208 shifted supports)"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corrupt", action="store_true", help="Adversarially corrupt certificate in-memory and expect FAIL")
    args = parser.parse_args()

    cw_path = OBJ_DIR / "constructive_tightness_witnesses.json"
    lb_path = OBJ_DIR / "p1_p2_lower_bound_certificates.json"
    if not cw_path.is_file() or not lb_path.is_file():
        return fail("Missing object/constructive_tightness_witnesses.json or object/p1_p2_lower_bound_certificates.json")

    try:
        cw = json.loads(cw_path.read_text(encoding="utf-8"))
        lb = json.loads(lb_path.read_text(encoding="utf-8"))
    except Exception as e:
        return fail(f"JSON parse error: {e}")

    if args.corrupt:
        cw = copy.deepcopy(cw)
        cw["witnesses"][0]["G"][0][0] ^= 1

    ok1, msg1 = verify_constructive_witnesses(cw)
    if not ok1:
        return fail(msg1)
    print(f"[OK] {msg1}")

    ok2, msg2 = verify_p1_certificate(lb.get("p1_certificate", {}))
    if not ok2:
        return fail(msg2)
    print(f"[OK] {msg2}")

    ok3, msg3 = verify_p2_certificate(lb.get("p2_certificate", {}))
    if not ok3:
        return fail(msg3)
    print(f"[OK] {msg3}")

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
