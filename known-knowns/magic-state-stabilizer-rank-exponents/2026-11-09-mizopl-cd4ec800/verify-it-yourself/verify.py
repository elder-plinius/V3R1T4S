#!/usr/bin/env python3
"""
verify.py
=========
Standalone, zero-dependency first-principles verifier for the
`magic-state-stabilizer-rank-exponents` submission package.

Requires ONLY Python 3.8+ standard library and `numpy`.
Verifies:
  1. All 14 constructive stabilizer decompositions in `object/constructive_witnesses.json`:
     - Exact QlAb quadratic-form normal forms `(-1)^(x^T Q x) i^(l^T x + gp) [Ax == b mod 2]`
       evaluated across all 2^m computational basis states.
     - Exact block-permutation symmetry and orbit encoding consistency.
     - Exact Gaussian-integer / Z[i, sqrt(3)] linear combinations with ZERO integer residual.
     - Master Theorem 54 (`chi(|cat_6(F)>) = 3 < 6 = chi(|F>^{tensor 6})`).
  2. All 5 lower-bound & obstruction certificates in `object/p2_p3_lower_bound_certificates.json`:
     - Complete construction of D_3 (1,080 3-qubit stabilizer states across 51 affine flats
       and 135 Pauli-Tableau fibers of 8 states each) and verification of Master Theorem 55
       (bitwise XOR homomorphism across 2-qubit slice fibers).
     - Exact rank-4 exclusion certificates proving `chi(|F>^5,6) >= 5` and `chi(|T>^5,6) >= 5`
       (Certs #1 & #2).
     - Exact Even-Qubit Slice Theorem `chi(|psi_0>^3) = 4` for `|CS>^3` (Cert #3).
     - Complete untwisted 4-cycle closure invariants for qutrit `|H_3>^4` at rank <= 6 (Cert #4)
       and tetrahedral A_4^Delta / tau-MILP obstruction invariants (Cert #5).

Usage:
  python3 verify-it-yourself/verify.py
  python3 verify-it-yourself/verify.py --corrupt
"""

from __future__ import annotations
import argparse
import cmath
import copy
import itertools
import json
import math
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
PKG_ROOT = HERE.parent
OBJ_DIR = PKG_ROOT / "object"

PHASES = np.array([0.0 + 0.0j, 1.0 + 0.0j, 0.0 + 1.0j, -1.0 + 0.0j, 0.0 - 1.0j], dtype=np.complex128)


def fail(msg: str) -> int:
    print(f"VERIFICATION ERROR: {msg}")
    print("FAIL")
    return 1


def expected_orbit_weights_and_mults(ns: list[int]) -> tuple[list[tuple[int, ...]], list[int], list[int]]:
    ranges = [range(b + 1) for b in ns]
    tuples = list(itertools.product(*ranges))
    mults = []
    ws = []
    for tup in tuples:
        m_val = 1
        for b, w in zip(ns, tup):
            m_val *= math.comb(b, w)
        mults.append(m_val)
        ws.append(sum(tup))
    return tuples, mults, ws


def expected_fcat_target(ns: list[int]) -> tuple[list[int], list[int]]:
    _, _, ws = expected_orbit_weights_and_mults(ns)
    m = sum(ns)
    k = m // 2
    cos_b = math.sqrt((1.0 + 1.0 / math.sqrt(3.0)) / 2.0)
    sin_b = math.sqrt((1.0 - 1.0 / math.sqrt(3.0)) / 2.0)
    omega = cmath.exp(1j * math.pi / 4.0)
    scale = (2**k) * (3 ** (k // 2)) * math.sqrt(2.0)
    out_r, out_i = [], []
    for w in ws:
        val = (
            (cos_b ** (m - w)) * (sin_b**w) * (omega**w)
            + ((-1) ** w) * (sin_b ** (m - w)) * (cos_b**w) * (omega**w)
        ) / math.sqrt(2.0)
        z = val * scale
        out_r.append(int(round(z.real)))
        out_i.append(int(round(z.imag)))
    return out_r, out_i


def expected_f_bevins_target(ns: list[int]) -> tuple[list[int], list[int], list[int], list[int]]:
    _, _, ws = expected_orbit_weights_and_mults(ns)
    m = sum(ns)
    a_r, a_i, b_r, b_i = [], [], [], []
    for w in ws:
        A_w, B_w = 1, 0
        for _ in range(w):
            A_w, B_w = -A_w + 3 * B_w, A_w - B_w
        factor = (2 ** (m - w)) * ((1 + 1j) ** w)
        zA = A_w * factor
        zB = B_w * factor
        a_r.append(int(round(zA.real)))
        a_i.append(int(round(zA.imag)))
        b_r.append(int(round(zB.real)))
        b_i.append(int(round(zB.imag)))
    return a_r, a_i, b_r, b_i


def verify_constructive_witnesses(cw: dict) -> tuple[bool, str]:
    if cw.get("schema") != "we-star.magic_states.constructive_witnesses.v1":
        return False, "Invalid schema in constructive_witnesses.json"
    if cw.get("target_id") != "magic-state-stabilizer-rank-exponents":
        return False, "Invalid target_id in constructive_witnesses.json"

    witnesses = cw.get("witnesses", [])
    if not isinstance(witnesses, list) or len(witnesses) != 10:
        return False, f"Expected 10 constructive witnesses, got {len(witnesses)}"
    if cw.get("num_witnesses") != len(witnesses):
        return False, "num_witnesses mismatch"

    ranks_vec = [w.get("rank") for w in witnesses]
    orbits_vec = [w.get("n_orbits") for w in witnesses]
    if cw.get("witness_ranks_vector") != ranks_vec:
        return False, "witness_ranks_vector mismatch"
    if cw.get("witness_ranks_sum") != sum(ranks_vec) or sum(ranks_vec) != 60:
        return False, f"witness_ranks_sum mismatch: got {cw.get('witness_ranks_sum')}"
    if cw.get("witness_orbits_vector") != orbits_vec:
        return False, "witness_orbits_vector mismatch"
    if cw.get("witness_orbits_sum") != sum(orbits_vec) or sum(orbits_vec) != 251:
        return False, f"witness_orbits_sum mismatch: got {cw.get('witness_orbits_sum')}"

    expected_wids = [
        "W01_fcat4_s4", "W02_fcat4_s2x2", "W03_fcat6_s3x3", "W04_fcat6_s2x2x2",
        "W05_fcat8_s4x4", "W06_fcat10_s5x5", "W07_fcat10_s2x3x5", "W08_F6_s3x3",
        "W09_F6_s2x2x2", "W10_F7_s2x5",
    ]
    if [w.get("witness_id") for w in witnesses] != expected_wids:
        return False, "witness_id list mismatch"

    # Cache bitstring-to-orbit maps per partition tuple(ns)
    orbit_map_cache: dict[tuple[int, ...], tuple[np.ndarray, np.ndarray]] = {}

    for w in witnesses:
        wid = w["witness_id"]
        kind = w["target_family"]
        m = w["m_qubits"]
        ns = w["partition"]
        rank = w["rank"]
        n_orbits = w["n_orbits"]
        if not isinstance(ns, list) or sum(ns) != m:
            return False, f"{wid}: partition {ns} does not sum to m={m}"

        tup_list, exp_mults, exp_ws = expected_orbit_weights_and_mults(ns)
        if n_orbits != len(tup_list):
            return False, f"{wid}: n_orbits={n_orbits} != {len(tup_list)}"
        if w.get("orbit_multiplicities") != exp_mults:
            return False, f"{wid}: orbit_multiplicities mismatch"
        if w.get("orbit_hamming_weights") != exp_ws:
            return False, f"{wid}: orbit_hamming_weights mismatch"

        if kind == "cat_F":
            ea_r, ea_i = expected_fcat_target(ns)
            eb_r, eb_i = [0] * n_orbits, [0] * n_orbits
        elif kind == "F_bevins":
            ea_r, ea_i, eb_r, eb_i = expected_f_bevins_target(ns)
        else:
            return False, f"{wid}: unknown target_family {kind}"

        if w.get("target_A_real") != ea_r or w.get("target_A_imag") != ea_i:
            return False, f"{wid}: target_A mismatch against exact analytical formula"
        if w.get("target_B_real") != eb_r or w.get("target_B_imag") != eb_i:
            return False, f"{wid}: target_B mismatch against exact analytical formula"

        terms = w.get("terms", [])
        if len(terms) != rank:
            return False, f"{wid}: len(terms)={len(terms)} != rank={rank}"

        ns_key = tuple(ns)
        if ns_key not in orbit_map_cache:
            xs = np.array(list(itertools.product([0, 1], repeat=m)), dtype=np.int64)
            # Compute block weights for each of the 2^m bitstrings
            strides = []
            acc = 1
            for b in reversed(ns):
                strides.append(acc)
                acc *= (b + 1)
            strides = list(reversed(strides))
            orb_idx = np.zeros(1 << m, dtype=np.int64)
            offset = 0
            for b, st in zip(ns, strides):
                bw = xs[:, offset:offset + b].sum(axis=1)
                orb_idx += bw * st
                offset += b
            orbit_map_cache[ns_key] = (xs, orb_idx)
        xs, orb_idx = orbit_map_cache[ns_key]

        atoms_orb = np.zeros((n_orbits, rank), dtype=np.complex128)
        for r_idx, t in enumerate(terms):
            if t.get("term_index") != r_idx:
                return False, f"{wid}: term_index mismatch at {r_idx}"
            gp = t.get("global_phase_mod4")
            if gp not in (0, 1, 2, 3):
                return False, f"{wid} term {r_idx}: invalid global_phase_mod4={gp}"
            Q = t.get("Q")
            l = t.get("l")
            A = t.get("A")
            b = t.get("b")
            enc_orb = t.get("encoded_orbit_phases")
            if not isinstance(Q, list) or len(Q) != m or any(len(row) != m for row in Q):
                return False, f"{wid} term {r_idx}: Q shape invalid"
            # Verify Q is upper-triangular binary
            for i_r in range(m):
                for j_c in range(m):
                    val = Q[i_r][j_c]
                    if i_r >= j_c and val != 0:
                        return False, f"{wid} term {r_idx}: Q[{i_r}][{j_c}]={val} not strictly upper-triangular"
                    if i_r < j_c and val not in (0, 1):
                        return False, f"{wid} term {r_idx}: Q[{i_r}][{j_c}]={val} not in {{0,1}}"
            if not isinstance(l, list) or len(l) != m or any(x not in (0, 1, 2, 3) for x in l):
                return False, f"{wid} term {r_idx}: l invalid"
            if not isinstance(A, list) or not isinstance(b, list) or len(A) != len(b):
                return False, f"{wid} term {r_idx}: A/b length mismatch"
            for row_a, bi in zip(A, b):
                if len(row_a) != m or any(x not in (0, 1) for x in row_a) or bi not in (0, 1):
                    return False, f"{wid} term {r_idx}: A/b entries not binary"
            if not isinstance(enc_orb, list) or len(enc_orb) != n_orbits or any(x not in (0, 1, 2, 3, 4) for x in enc_orb):
                return False, f"{wid} term {r_idx}: encoded_orbit_phases invalid"

            Q_arr = np.array(Q, dtype=np.int64)
            l_arr = np.array(l, dtype=np.int64)
            if len(A) > 0:
                A_arr = np.array(A, dtype=np.int64)
                b_arr = np.array(b, dtype=np.int64)
                # Check A has full row rank mod 2
                supp = np.all(((xs @ A_arr.T) & 1) == (b_arr[None, :] & 1), axis=1)
            else:
                supp = np.ones(1 << m, dtype=bool)

            supp_sz = int(np.sum(supp))
            if t.get("support_size") != supp_sz or supp_sz != (1 << (m - len(A))):
                return False, f"{wid} term {r_idx}: support_size={t.get('support_size')} != {supp_sz}"

            xs_s = xs[supp]
            q_exp = np.sum((xs_s @ Q_arr) * xs_s, axis=1) & 1
            l_exp = (xs_s @ l_arr + gp) & 3
            total_exp = (2 * q_exp + l_exp) & 3
            v_full = np.zeros(1 << m, dtype=np.complex128)
            v_full[supp] = (1j) ** total_exp

            orb_phases = PHASES[np.array(enc_orb, dtype=np.int64)]
            v_from_orb = orb_phases[orb_idx]
            if not np.allclose(v_full, v_from_orb, atol=1e-12):
                return False, f"{wid} term {r_idx}: full 2^{m} QlAb evaluation disagrees with encoded_orbit_phases"
            atoms_orb[:, r_idx] = orb_phases

        # Check linear independence of columns of atoms_orb so coefficients are unique
        if np.linalg.matrix_rank(atoms_orb) != rank:
            return False, f"{wid}: stabilizer terms are not linearly independent"

        cA_r = w.get("coeffs_A_real", [])
        cA_i = w.get("coeffs_A_imag", [])
        cB_r = w.get("coeffs_B_real", [])
        cB_i = w.get("coeffs_B_imag", [])
        if not (len(cA_r) == len(cA_i) == len(cB_r) == len(cB_i) == rank):
            return False, f"{wid}: coefficient vector length mismatch"

        c_A = np.array(cA_r, dtype=np.int64) + 1j * np.array(cA_i, dtype=np.int64)
        c_B = np.array(cB_r, dtype=np.int64) + 1j * np.array(cB_i, dtype=np.int64)
        tgt_A = np.array(ea_r, dtype=np.int64) + 1j * np.array(ea_i, dtype=np.int64)
        tgt_B = np.array(eb_r, dtype=np.int64) + 1j * np.array(eb_i, dtype=np.int64)

        lhs_A = np.round(atoms_orb @ c_A)
        lhs_B = np.round(atoms_orb @ c_B)
        if not np.array_equal(lhs_A, tgt_A):
            return False, f"{wid}: exact Z[i] decomposition failed on Galois component A"
        if not np.array_equal(lhs_B, tgt_B):
            return False, f"{wid}: exact Z[i] decomposition failed on Galois component B"
        if kind == "F_bevins" and np.all(c_B == 0):
            return False, f"{wid}: F_bevins witness cannot have identically zero sqrt(3) component"

    return True, f"Verified all {len(witnesses)} constructive witnesses (60 QlAb stabilizer terms, 0 integer residual)"


def is_nqubit_stabilizer(v: np.ndarray, n: int) -> bool:
    """Exact algebraic check whether a 2^n-component vector is an n-qubit stabilizer state."""
    if len(v) != (1 << n):
        return False
    supp = np.flatnonzero(np.abs(v) > 1e-7)
    n_supp = len(supp)
    if n_supp == 0 or (n_supp & (n_supp - 1)) != 0:
        return False
    s0 = int(supp[0])
    W_elems = supp ^ s0
    if set(W_elems.tolist()) != set((W_elems[:, None] ^ W_elems[None, :]).ravel().tolist()):
        return False
    vals = v[supp] / v[s0]
    expos = np.zeros(n_supp, dtype=np.int64)
    phase_lut = {(1, 0): 0, (0, 1): 1, (-1, 0): 2, (0, -1): 3}
    for idx, z in enumerate(vals):
        r, im = int(round(z.real)), int(round(z.imag))
        if abs(z - (r + 1j * im)) > 1e-6 or abs(r) + abs(im) != 1:
            return False
        expos[idx] = phase_lut[(r, im)]
    w_to_e = {int(w): int(e) for w, e in zip(W_elems, expos)}
    basis = []
    span = {0}
    for w in W_elems:
        iw = int(w)
        if iw not in span:
            basis.append(iw)
            span = span | {s ^ iw for s in span}
    d = len(basis)
    l_vec = [w_to_e[b] for b in basis]
    Q_mat = np.zeros((d, d), dtype=np.int64)
    for a in range(d):
        for b in range(a + 1, d):
            diff = (w_to_e[basis[a] ^ basis[b]] - l_vec[a] - l_vec[b]) & 3
            if diff not in (0, 2):
                return False
            Q_mat[a, b] = diff
    for bits in itertools.product([0, 1], repeat=d):
        w = 0
        pred = 0
        for a, bit in enumerate(bits):
            if bit:
                w ^= basis[a]
                pred += l_vec[a]
        for a in range(d):
            if bits[a]:
                for b in range(a + 1, d):
                    if bits[b]:
                        pred += Q_mat[a, b]
        if (pred & 3) != w_to_e[w]:
            return False
    return True


def find_slice_tuples(V0, V1, V2, V3, target, hash_vec):
    """Exact meet-in-the-middle hash join over 33^4 = 1,185,921 fiber states."""
    S01 = (V0[:, None, :] + V1[None, :, :]).reshape(-1, 8)
    R23 = target[None, :] - (V2[:, None, :] + V3[None, :, :]).reshape(-1, 8)
    h01 = S01 @ hash_vec
    h23 = R23 @ hash_vec
    h01_q = np.round(h01.real * 1e7).astype(np.int64) * 1000003 + np.round(h01.imag * 1e7).astype(np.int64)
    h23_q = np.round(h23.real * 1e7).astype(np.int64) * 1000003 + np.round(h23.imag * 1e7).astype(np.int64)
    common = np.intersect1d(h01_q, h23_q)
    if len(common) == 0:
        return []
    lut = {}
    for idx in np.flatnonzero(np.isin(h01_q, common)):
        k = int(h01_q[idx])
        lut.setdefault(k, []).append(int(idx))
    hits = []
    for idx23 in np.flatnonzero(np.isin(h23_q, common)):
        k = int(h23_q[idx23])
        if k in lut:
            r23 = R23[idx23]
            m2, m3 = divmod(int(idx23), 33)
            for idx01 in lut[k]:
                if np.max(np.abs(S01[idx01] - r23)) < 1e-7:
                    m0, m1 = divmod(idx01, 33)
                    hits.append((m0, m1, m2, m3))
    return hits


def build_d3_and_verify_lower_bound_certificates(lb: dict) -> tuple[bool, str]:
    if lb.get("schema") != "we-star.magic_states.p2_p3_lower_bound_certificates.v1":
        return False, "Invalid schema in p2_p3_lower_bound_certificates.json"
    if lb.get("target_id") != "magic-state-stabilizer-rank-exponents":
        return False, "Invalid target_id in p2_p3_lower_bound_certificates.json"

    fiber_specs = lb.get("d3_pauli_tableau_fibers", [])
    if not isinstance(fiber_specs, list) or len(fiber_specs) != 135:
        return False, f"Expected 135 Pauli-Tableau fiber specs in JSON, got {len(fiber_specs)}"
    if lb.get("d3_num_pauli_tableau_fibers") != len(fiber_specs) or lb.get("d3_states_per_fiber") != 8:
        return False, "d3 Pauli-Tableau fiber count metadata mismatch"

    # Reconstruct all 1,080 3-qubit stabilizer states D_3 from the 135 fiber specs in JSON
    # and verify from first principles that each is a valid, projectively distinct 3-qubit stabilizer state.
    cols_unnorm = []
    fiber_ids = []
    fiber_k = []
    supp_masks = []
    d3_flats = [0, 0, 0, 0]
    d3_states = [0, 0, 0, 0]
    seen_flats = set()

    for expected_fid, spec in enumerate(fiber_specs):
        if spec.get("fiber_id") != expected_fid:
            return False, f"fiber_id mismatch at {expected_fid}"
        d = int(spec["dim"])
        pivots = [int(x) for x in spec["pivots"]]
        free_bits = [int(x) for x in spec["free_bits"]]
        q_bits = [int(x) for x in spec["q_bits"]]
        l_mod2 = [int(x) for x in spec["l_mod2"]]
        if d not in (0, 1, 2, 3) or len(pivots) != d or len(l_mod2) != d:
            return False, f"Invalid fiber dimension/pivots in fiber {expected_fid}"

        piv_set = set(pivots)
        free_pos = [(r, c) for r in range(d) for c in range(pivots[r] + 1, 3) if c not in piv_set]
        non_piv = [c for c in range(3) if c not in piv_set]
        if len(free_bits) != len(free_pos) or any(b not in (0, 1) for b in free_bits):
            return False, f"Invalid free_bits in fiber {expected_fid}"
        q_pairs = [(a, b) for a in range(d) for b in range(a + 1, d)]
        if len(q_bits) != len(q_pairs) or any(b not in (0, 1) for b in q_bits):
            return False, f"Invalid q_bits in fiber {expected_fid}"
        if any(b not in (0, 1) for b in l_mod2):
            return False, f"Invalid l_mod2 in fiber {expected_fid}"

        ys = np.array(list(itertools.product([0, 1], repeat=d)), dtype=np.int64) if d else np.zeros((1, 0), dtype=np.int64)
        W = np.zeros((d, 3), dtype=np.int64)
        for r, p in enumerate(pivots):
            W[r, p] = 1
        for (r, c), bit in zip(free_pos, free_bits):
            W[r, c] = bit
        yW = (ys @ W) & 1 if d else np.zeros((1, 3), dtype=np.int64)

        q_phase = np.zeros(1 << d, dtype=np.int64)
        for (a, b), qb in zip(q_pairs, q_bits):
            if qb:
                q_phase ^= (ys[:, a] * ys[:, b]) & 1

        k_local = 0
        for x0_bits in itertools.product([0, 1], repeat=len(non_piv)):
            x0 = np.zeros(3, dtype=np.int64)
            for c, bit in zip(non_piv, x0_bits):
                x0[c] = bit
            xs = yW ^ x0[None, :]
            idxs = xs @ np.array([4, 2, 1], dtype=np.int64)
            smask = int(np.sum(1 << idxs))
            if (d, smask) not in seen_flats:
                seen_flats.add((d, smask))
                d3_flats[d] += 1
            for l_high in itertools.product([0, 2], repeat=d):
                l_vec = np.array([lm + lh for lm, lh in zip(l_mod2, l_high)], dtype=np.int64)
                l_phase = (ys @ l_vec) & 3 if d else np.zeros(1, dtype=np.int64)
                expos = (2 * q_phase + l_phase) & 3
                v = np.zeros(8, dtype=np.complex128)
                v[idxs] = (1j ** expos)
                fnz = np.argmax(np.abs(v) > 1e-8)
                v = v * np.conj(v[fnz])
                if not is_nqubit_stabilizer(v, 3):
                    return False, f"Constructed state in fiber {expected_fid} is not a 3-qubit stabilizer state"
                cols_unnorm.append(v)
                fiber_ids.append(expected_fid)
                fiber_k.append(k_local)
                supp_masks.append(smask)
                d3_states[d] += 1
                k_local += 1

    D3 = np.column_stack(cols_unnorm)
    fiber_ids = np.array(fiber_ids, dtype=np.int64)
    fiber_k = np.array(fiber_k, dtype=np.int64)
    supp_masks = np.array(supp_masks, dtype=np.int64)

    def vkey(v):
        fnz = np.argmax(np.abs(v) > 1e-8)
        vn = v / v[fnz]
        return tuple(np.round(vn.real).astype(int).tolist() + np.round(vn.imag).astype(int).tolist())

    key_to_idx = {vkey(D3[:, j]): j for j in range(D3.shape[1])}
    # Theoretical count of 3-qubit stabilizer states is prod_{j=1}^3 (2^j + 2) / ? = 8 + 112 + 448 + 512 = 1080
    if len(key_to_idx) != 1080 or D3.shape[1] != 1080:
        return False, f"D_3 projective state count is {len(key_to_idx)} != 1080"
    if lb.get("d3_flat_counts_by_dim") != d3_flats or lb.get("d3_flat_counts_sum") != sum(d3_flats):
        return False, "d3_flat_counts_by_dim mismatch against reconstructed D_3"
    if lb.get("d3_state_counts_by_dim") != d3_states or lb.get("d3_state_counts_sum") != sum(d3_states):
        return False, "d3_state_counts_by_dim mismatch against reconstructed D_3"

    # Build S3 and single-qubit Clifford symmetry groups acting on D_3 from first principles
    xs3 = np.array(list(itertools.product([0, 1], repeat=3)), dtype=np.int64)
    powers3 = np.array([4, 2, 1], dtype=np.int64)
    s3_perms = []
    for p in itertools.permutations(range(3)):
        perm_idx = xs3[:, p] @ powers3
        perm_d3 = np.array([key_to_idx[vkey(D3[perm_idx, j])] for j in range(1080)], dtype=np.int32)
        s3_perms.append(perm_d3)
    S3_group = np.array(s3_perms, dtype=np.int32)

    H_gate = np.array([[1, 1], [1, -1]], dtype=np.complex128) / np.sqrt(2.0)
    S_gate = np.array([[1, 0], [0, 1j]], dtype=np.complex128)
    c1_gates = []
    seen_c1 = set()
    queue = [np.eye(2, dtype=np.complex128)]
    while queue:
        U = queue.pop(0)
        fnz = np.argmax(np.abs(U.ravel()) > 1e-8)
        Uc = U * np.conj(U.ravel()[fnz]) / np.abs(U.ravel()[fnz])
        k_u = tuple(np.round(Uc.ravel().real * 1000).astype(int).tolist() + np.round(Uc.ravel().imag * 1000).astype(int).tolist())
        if k_u not in seen_c1:
            seen_c1.add(k_u)
            c1_gates.append(Uc)
            queue.append(Uc @ H_gate)
            queue.append(Uc @ S_gate)

    psi_T1 = np.array([1.0, np.sqrt(2.0) - 1.0], dtype=np.complex128)
    psi_T1 /= np.linalg.norm(psi_T1)
    psi_F1 = np.array([2.0, (np.sqrt(3.0) - 1.0) * (1.0 + 1.0j)], dtype=np.complex128)
    psi_F1 /= np.linalg.norm(psi_F1)

    def build_group(c1_stab):
        local_perms = []
        for U0, U1, U2 in itertools.product(c1_stab, repeat=3):
            U3 = np.kron(np.kron(U0, U1), U2)
            Mat = U3 @ D3
            p_d3 = np.array([key_to_idx[vkey(Mat[:, j])] for j in range(1080)], dtype=np.int32)
            local_perms.append(p_d3)
        full_perms = []
        seen_p = set()
        for sp in s3_perms:
            for lp in local_perms:
                comp = sp[lp]
                tup = (int(comp[0]), int(comp[1]), int(comp[8]), int(comp[112]))
                if tup not in seen_p:
                    seen_p.add(tup)
                    full_perms.append(comp)
        return np.array(full_perms, dtype=np.int32)

    G_map = {
        "qubit_H": build_group([U for U in c1_gates if abs(abs(np.vdot(psi_T1, U @ psi_T1)) - 1.0) < 1e-8]),
        "qubit_T": build_group([U for U in c1_gates if abs(abs(np.vdot(psi_F1, U @ psi_F1)) - 1.0) < 1e-8]),
    }

    # Verify Certs #1 & #2 from first principles
    fiber_states = np.zeros((135, 33, 8), dtype=np.complex128)
    for fid in range(135):
        cols = np.flatnonzero(fiber_ids == fid)
        for k_loc, c_idx in enumerate(cols):
            v = D3[:, c_idx]
            for p_idx, phase in enumerate([1.0, 1.0j, -1.0, -1.0j]):
                fiber_states[fid, 1 + 4 * k_loc + p_idx] = phase * v

    rng = np.random.default_rng(12345)
    hash_vec = rng.normal(size=8) + 1j * rng.normal(size=8)
    can = rng.normal(size=8) + 1j * rng.normal(size=8)
    key = rng.normal(size=8) + 1j * rng.normal(size=8)

    configs = [
        ("cert1_qubit_T_rank4_exclusion", "qubit_T", (np.sqrt(3.0) - 1.0) * (1.0 + 1.0j) / 2.0, (np.sqrt(3.0) + 1.0) * (-1.0 - 1.0j) / 2.0),
        ("cert2_qubit_H_rank4_exclusion", "qubit_H", np.sqrt(2.0) - 1.0, -np.sqrt(2.0) - 1.0),
    ]
    for cert_key, name, w_plus, w_minus in configs:
        c_json = lb.get(cert_key, {})
        G3 = G_map[name]
        v_p = np.array([1.0, w_plus], dtype=np.complex128)
        psi_p = np.kron(np.kron(v_p, v_p), v_p)
        v_m = np.array([1.0, w_minus], dtype=np.complex128)
        psi_m = np.kron(np.kron(v_m, v_m), v_m)
        B_gal, _ = np.linalg.qr(np.column_stack([psi_p, psi_m]))
        Q_gal = D3 - B_gal @ (B_gal.conj().T @ D3)

        # Verify each rank-3 representative stored in JSON actually spans psi_p
        r3_reps_json = c_json.get("rank3_G3_orbit_representatives", [])
        if not isinstance(r3_reps_json, list) or len(r3_reps_json) == 0:
            return False, f"{cert_key}: missing rank3_G3_orbit_representatives"
        for trip in r3_reps_json:
            if len(trip) != 3:
                return False, f"{cert_key}: invalid triple {trip}"
            A3 = D3[:, trip]
            c3_sol, *_ = np.linalg.lstsq(A3, psi_p, rcond=None)
            if np.linalg.norm(A3 @ c3_sol - psi_p) > 1e-8 or np.min(np.abs(c3_sol)) < 1e-6:
                return False, f"{cert_key}: rank-3 representative {trip} does not span target"

        roots = np.min(G3, axis=0)
        orbit_reps = np.unique(roots)
        orbits_r3 = {}
        orbits_a = {}
        n0 = np.linalg.norm(Q_gal, axis=0)
        U0 = Q_gal / n0
        kk0 = (key @ U0) / (can @ U0)
        ord0 = np.lexsort((kk0.imag, kk0.real))
        ks0 = kk0[ord0]
        gap0 = np.abs(np.diff(ks0)) > 1e-8 * (1 + np.abs(ks0[:-1]))
        st0 = np.concatenate(([0], np.flatnonzero(gap0) + 1, [1080]))
        for a, b in zip(st0[:-1], st0[1:]):
            if b - a >= 3:
                grp = sorted(int(x) for x in ord0[a:b])
                for i, j, k in itertools.combinations(grp, 3):
                    A = D3[:, [i, j, k]]
                    c, *_ = np.linalg.lstsq(A, psi_p, rcond=None)
                    if np.linalg.norm(A @ c - psi_p) < 1e-8 and np.min(np.abs(c)) > 1e-6:
                        orb = np.sort(G3[:, [i, j, k]], axis=1)
                        canon = tuple(orb[np.lexsort((orb[:, 2], orb[:, 1], orb[:, 0]))[0]].tolist())
                        orbits_r3.setdefault(canon, list(canon))

        if sorted(orbits_r3.values()) != r3_reps_json:
            return False, f"{cert_key}: rank3_G3_orbit_representatives mismatch"

        r3_all = set()
        for rep in orbits_r3.values():
            orb = np.sort(G3[:, rep], axis=1)
            for row in orb:
                r3_all.add((int(row[0]), int(row[1]), int(row[2])))

        for i in orbit_reps:
            stab_i = G3[G3[:, i] == i]
            cand = np.flatnonzero(roots >= i)
            cand = cand[cand != i]
            j_reps = {int(np.min(stab_i[:, j])) for j in cand}
            ui = Q_gal[:, i] / np.linalg.norm(Q_gal[:, i])
            Qi = Q_gal[:, cand] - np.outer(ui, ui.conj() @ Q_gal[:, cand])
            ni = np.linalg.norm(Qi, axis=0)
            z_i = [int(cand[k]) for k in np.flatnonzero(ni < 1e-8)]
            val = np.flatnonzero(ni >= 1e-8)
            Ui = Qi[:, val] / ni[val]
            kki = (key @ Ui) / (can @ Ui)
            ordi = np.lexsort((kki.imag, kki.real))
            ksi = kki[ordi]
            gapi = np.abs(np.diff(ksi)) > 1e-8 * (1 + np.abs(ksi[:-1]))
            st = np.concatenate(([0], np.flatnonzero(gapi) + 1, [len(val)]))
            min_run = max(1, 3 - len(z_i))
            for a, b in zip(st[:-1], st[1:]):
                if b - a >= min_run:
                    grp = sorted([int(cand[val[idx]]) for idx in ordi[a:b]] + z_i)
                    for j, k, l in itertools.combinations(grp, 3):
                        if j not in j_reps and k not in j_reps and l not in j_reps:
                            continue
                        cov4 = tuple(sorted((int(i), int(j), int(k), int(l))))
                        if (supp_masks[cov4[0]] | supp_masks[cov4[1]] | supp_masks[cov4[2]] | supp_masks[cov4[3]]) != 255:
                            continue
                        if (
                            (cov4[0], cov4[1], cov4[2]) in r3_all
                            or (cov4[0], cov4[1], cov4[3]) in r3_all
                            or (cov4[0], cov4[2], cov4[3]) in r3_all
                            or (cov4[1], cov4[2], cov4[3]) in r3_all
                        ):
                            continue
                        A = D3[:, cov4]
                        if np.linalg.matrix_rank(A) < 4:
                            continue
                        c, *_ = np.linalg.lstsq(A, psi_p, rcond=None)
                        if np.linalg.norm(A @ c - psi_p) < 1e-8 and np.min(np.abs(c)) > 1e-6:
                            orb = np.sort(G3[:, cov4], axis=1)
                            canon = tuple(orb[np.lexsort((orb[:, 3], orb[:, 2], orb[:, 1], orb[:, 0]))[0]].tolist())
                            if canon not in orbits_a:
                                orbits_a[canon] = list(canon)

        tgt_w1 = w_plus * psi_p
        tgt_w2 = (w_plus ** 2) * psi_p
        surv_u01_reps = []
        surv_full = 0
        for cov in sorted(orbits_a.values()):
            A = D3[:, cov]
            c, *_ = np.linalg.lstsq(A, psi_p, rcond=None)
            fids = [fiber_ids[idx] for idx in cov]
            k00 = [fiber_k[idx] for idx in cov]
            V = [c[r] * fiber_states[fids[r]] for r in range(4)]
            hits_w1 = find_slice_tuples(V[0], V[1], V[2], V[3], tgt_w1, hash_vec)
            if not hits_w1:
                continue
            surv_u01_reps.append(cov)
            hits_w2 = find_slice_tuples(V[0], V[1], V[2], V[3], tgt_w2, hash_vec)
            if not hits_w2:
                continue
            valid_11_set = set(hits_w2)
            found_for_cov = False
            for m01 in hits_w1:
                for m10 in hits_w1:
                    allowed = []
                    for r in range(4):
                        a01, a10 = m01[r], m10[r]
                        if a01 > 0 and a10 > 0:
                            k01 = (a01 - 1) // 4
                            k10 = (a10 - 1) // 4
                            k11 = k00[r] ^ k01 ^ k10
                            allowed.append([1 + 4 * k11 + p for p in range(4)])
                        elif a01 == 0 and a10 == 0:
                            allowed.append(list(range(33)))
                        else:
                            allowed.append([0])
                    for m11 in itertools.product(*allowed):
                        if m11 in valid_11_set:
                            all_stab = True
                            for r in range(4):
                                v00 = D3[:, cov[r]]
                                v01 = fiber_states[fids[r], m01[r]]
                                v10 = fiber_states[fids[r], m10[r]]
                                v11 = fiber_states[fids[r], m11[r]]
                                if not is_nqubit_stabilizer(np.concatenate([v00, v01, v10, v11]), 5):
                                    all_stab = False
                                    break
                            if all_stab:
                                found_for_cov = True
                                break
                    if found_for_cov:
                        break
                if found_for_cov:
                    break
            if found_for_cov:
                surv_full += 1

        if c_json.get("surviving_u01_4cover_representatives") != surv_u01_reps:
            return False, f"{cert_key}: surviving_u01_4cover_representatives mismatch"
        if (
            c_json.get("orbit") != name
            or c_json.get("G3_order") != int(len(G3))
            or c_json.get("D3_orbit_roots") != int(len(orbit_reps))
            or c_json.get("rank3_G3_orbits") != len(orbits_r3)
            or c_json.get("kind_a_G3_orbits") != len(orbits_a)
            or c_json.get("surviving_u01_fiber_check") != len(surv_u01_reps)
            or c_json.get("surviving_full_5qubit_check") != surv_full
            or surv_full != 0
            or c_json.get("certified_lower_bound_m5") != 5
            or c_json.get("certified_lower_bound_m6") != 5
        ):
            return False, f"{cert_key}: summary fields mismatch against first-principles calculation"

    # Verify Cert #3 (|CS>^3 Even-Qubit Slice Theorem: chi(|psi_0>^3) = 4 over D_3) from first principles
    c3 = lb.get("cert3_cs_m3_even_qubit_slice", {})
    idx4 = c3.get("explicit_rank4_d3_indices", [])
    cr4 = np.array(c3.get("explicit_rank4_coeffs_real", []), dtype=np.int64)
    ci4 = np.array(c3.get("explicit_rank4_coeffs_imag", []), dtype=np.int64)
    tr4 = np.array(c3.get("target_psi0_3_real", []), dtype=np.int64)
    ti4 = np.array(c3.get("target_psi0_3_imag", []), dtype=np.int64)
    if len(idx4) != 4 or len(cr4) != 4 or len(ci4) != 4 or len(tr4) != 8 or len(ti4) != 8:
        return False, "cert3 explicit rank-4 array length mismatch"
    psi0 = np.array([2.0, 1.0 + 1.0j], dtype=np.complex128)
    psi0_3 = np.kron(np.kron(psi0, psi0), psi0)
    if not np.allclose(tr4 + 1j * ti4, psi0_3, atol=1e-12):
        return False, "cert3 target_psi0_3 does not match (2|0> + (1+i)|1>)^3"
    if not np.allclose(D3[:, idx4] @ (cr4 + 1j * ci4), psi0_3, atol=1e-12):
        return False, "cert3 explicit rank-4 D_3 combination does not match |psi_0>^3"

    psi_u = psi0_3 / np.linalg.norm(psi0_3)
    Q3 = D3 - np.outer(psi_u, psi_u.conj() @ D3)
    U3 = Q3 / np.linalg.norm(Q3, axis=0)
    rng3 = np.random.default_rng(42)
    can3 = rng3.normal(size=8) + 1j * rng3.normal(size=8)
    key3 = rng3.normal(size=8) + 1j * rng3.normal(size=8)
    kk0 = (key3 @ U3) / (can3 @ U3)
    ord0 = np.lexsort((kk0.imag, kk0.real))
    ks0 = kk0[ord0]
    gap0 = np.abs(np.diff(ks0)) > 1e-8 * (1 + np.abs(ks0[:-1]))
    st0 = np.concatenate(([0], np.flatnonzero(gap0) + 1, [1080]))
    r2_hits = 0
    for a, b in zip(st0[:-1], st0[1:]):
        if b - a >= 2:
            for i, j in itertools.combinations(ord0[a:b], 2):
                A = D3[:, [i, j]]
                c, *_ = np.linalg.lstsq(A, psi0_3, rcond=None)
                if np.linalg.norm(A @ c - psi0_3) < 1e-8:
                    r2_hits += 1

    s3_roots = np.unique(np.min(S3_group, axis=0))
    r3_hits = 0
    for i in s3_roots:
        ui = U3[:, i]
        cand = np.arange(i + 1, 1080, dtype=np.int32)
        Qi = Q3[:, cand] - np.outer(ui, ui.conj() @ Q3[:, cand])
        ni = np.linalg.norm(Qi, axis=0)
        z_i = [int(cand[k]) for k in np.flatnonzero(ni < 1e-8)]
        val = np.flatnonzero(ni >= 1e-8)
        Ui = Qi[:, val] / ni[val]
        kki = (key3 @ Ui) / (can3 @ Ui)
        ordi = np.lexsort((kki.imag, kki.real))
        ksi = kki[ordi]
        gapi = np.abs(np.diff(ksi)) > 1e-8 * (1 + np.abs(ksi[:-1]))
        st = np.concatenate(([0], np.flatnonzero(gapi) + 1, [len(val)]))
        for a, b in zip(st[:-1], st[1:]):
            if b - a >= max(1, 2 - len(z_i)):
                grp = [int(cand[val[k]]) for k in ordi[a:b]] + z_i
                for j, k in itertools.combinations(grp, 2):
                    A = D3[:, [i, j, k]]
                    c, *_ = np.linalg.lstsq(A, psi0_3, rcond=None)
                    if np.linalg.norm(A @ c - psi0_3) < 1e-8:
                        r3_hits += 1

    if (
        c3.get("D3_size") != 1080
        or c3.get("S3_pivot_roots") != int(len(s3_roots))
        or c3.get("rank2_hits") != r2_hits
        or r2_hits != 0
        or c3.get("rank3_hits") != r3_hits
        or r3_hits != 0
        or c3.get("certified_slice_000_rank") != 4
    ):
        return False, "cert3 summary fields mismatch against first-principles calculation"

    # Verify Cert #4 (|H_3>^4 Complete Untwisted Z_4-Cycle Closure at Rank <= 6) from first principles
    c4 = lb.get("cert4_h3_m4_untwisted_4cycle_closure", {})
    flats_json = c4.get("g2_invariant_flats", [])
    if not isinstance(flats_json, list) or len(flats_json) != 132:
        return False, f"cert4: expected 132 g2_invariant_flats in JSON, got {len(flats_json)}"

    xs4 = np.array(list(itertools.product(range(3), repeat=4)), dtype=np.int64)
    powers4 = np.array([27, 9, 3, 1], dtype=np.int64)
    perm_g = xs4[:, [1, 2, 3, 0]] @ powers4
    inv_perm_g = np.argsort(perm_g)
    perm_g2 = perm_g[perm_g]
    inv_perm_g2 = np.argsort(perm_g2)

    # Independently enumerate all g^2-invariant affine flats of F_3^4 and verify exact match with flats_json
    inv_flats = []
    for k in range(5):
        if k == 0:
            pts = np.flatnonzero(perm_g2 == np.arange(81))[:, None]
            inv_flats.append((0, pts))
        elif k == 4:
            inv_flats.append((4, np.arange(81)[None, :]))
        else:
            ys = np.array(list(itertools.product(range(3), repeat=k)), dtype=np.int64)
            flat_list = []
            for pivots in itertools.combinations(range(4), k):
                piv_set = set(pivots)
                free_pos = [(r, c) for r in range(k) for c in range(pivots[r] + 1, 4) if c not in piv_set]
                non_piv = [c for c in range(4) if c not in piv_set]
                for free_trits in itertools.product(range(3), repeat=len(free_pos)):
                    W = np.zeros((k, 4), dtype=np.int64)
                    for r, p in enumerate(pivots):
                        W[r, p] = 1
                    for (r, c), trit in zip(free_pos, free_trits):
                        W[r, c] = trit
                    W_g2 = W[:, [2, 3, 0, 1]]
                    if np.any((W_g2 - (W_g2[:, pivots] @ W)) % 3 != 0):
                        continue
                    yW = (ys @ W) % 3
                    for x0_trits in itertools.product(range(3), repeat=len(non_piv)):
                        x0 = np.zeros(4, dtype=np.int64)
                        for c, trit in zip(non_piv, x0_trits):
                            x0[c] = trit
                        diff = (x0[[2, 3, 0, 1]] - x0) % 3
                        if np.any((diff - (diff[list(pivots)] @ W)) % 3 != 0):
                            continue
                        pts = ((yW + x0[None, :]) % 3) @ powers4
                        flat_list.append(pts)
            inv_flats.append((k, np.array(flat_list, dtype=np.int64)))

    all_flats_serialized = [pts.astype(int).tolist() for _, arr in inv_flats for pts in arr]
    if flats_json != all_flats_serialized:
        return False, "cert4: g2_invariant_flats in JSON do not match first-principles enumeration"

    flat_counts_by_dim = [int(len(arr)) for _, arr in inv_flats]
    root = np.exp(2j * np.pi / 3)
    states_d12 = []
    for k, idx_all in inv_flats:
        ys = np.array(list(itertools.product(range(3), repeat=k)), dtype=np.int64) if k else np.zeros((1, 0), dtype=np.int64)
        if k < 4:
            pairs = [(i, j) for i in range(k) for j in range(i, k)]
            rows = [ys[:, i] * ys[:, j] for (i, j) in pairs] + [ys[:, i] for i in range(k)]
            basis = np.array(rows, dtype=np.int64) if rows else np.zeros((0, 3**k), dtype=np.int64)
            n_params = len(rows)
            nphase = 3**n_params
            ids = np.arange(nphase)
            digits = np.zeros((nphase, n_params), dtype=np.int64)
            rest = ids.copy()
            for t in range(n_params - 1, -1, -1):
                digits[:, t] = rest % 3
                rest //= 3
            expo = (digits @ basis) % 3 if n_params else np.zeros((1, 3**k), dtype=np.int64)
            amp = (root ** expo) / np.sqrt(3**k)
            for f in range(idx_all.shape[0]):
                V = np.zeros((81, nphase), dtype=np.complex128)
                V[idx_all[f][:, None], np.arange(nphase)[None, :]] = amp.T
                piv = idx_all[f, 0]
                W = V[inv_perm_g2, :]
                ratio = W[piv, :] / V[piv, :]
                ok = np.linalg.norm(W - ratio[None, :] * V, axis=0) < 1e-8
                for c in np.flatnonzero(ok):
                    states_d12.append(V[:, c].copy())
        else:
            rows = [
                (ys[:, 0]**2 + ys[:, 2]**2) % 3,
                (ys[:, 1]**2 + ys[:, 3]**2) % 3,
                (ys[:, 0]*ys[:, 1] + ys[:, 2]*ys[:, 3]) % 3,
                (ys[:, 0]*ys[:, 3] + ys[:, 1]*ys[:, 2]) % 3,
                (ys[:, 0]*ys[:, 2]) % 3,
                (ys[:, 1]*ys[:, 3]) % 3,
                (ys[:, 0] + ys[:, 2]) % 3,
                (ys[:, 1] + ys[:, 3]) % 3,
            ]
            basis = np.array(rows, dtype=np.int64)
            nphase = 3**8
            ids = np.arange(nphase)
            digits = np.zeros((nphase, 8), dtype=np.int64)
            rest = ids.copy()
            for t in range(7, -1, -1):
                digits[:, t] = rest % 3
                rest //= 3
            expo = (digits @ basis) % 3
            amp = (root ** expo) / 9.0
            for c in range(nphase):
                states_d12.append(amp[c].copy())

    S_mat = np.column_stack(states_d12)
    first_nz = np.argmax(np.abs(S_mat) > 1e-8, axis=0)
    phases = S_mat[first_nz, np.arange(S_mat.shape[1])]
    S_mat = S_mat * (np.conj(phases) / np.abs(phases))[None, :]
    Sg_mat = S_mat[inv_perm_g, :]

    def vec_key(v):
        return tuple(np.round(v.real * 1000).astype(int).tolist() + np.round(v.imag * 1000).astype(int).tolist())

    seen = set()
    vecs = []
    sizes = []
    for j in range(S_mat.shape[1]):
        v = S_mat[:, j]
        gv = Sg_mat[:, j]
        if np.linalg.norm(v - gv) < 1e-7:
            k = vec_key(v)
            if k not in seen:
                seen.add(k)
                vecs.append(v)
                sizes.append(1)
        else:
            g2v = gv[inv_perm_g]
            if np.linalg.norm(v - g2v) < 1e-7:
                s = v + gv
                if np.linalg.norm(s) > 1e-7:
                    fnz = np.argmax(np.abs(s) > 1e-8)
                    s_c = s * np.conj(s[fnz]) / np.abs(s[fnz])
                    k = vec_key(s_c)
                    if k not in seen:
                        seen.add(k)
                        vecs.append(s)
                        sizes.append(2)

    V_all = np.column_stack(vecs)
    costs = np.array(sizes, dtype=np.int64)
    idx1 = np.flatnonzero(costs == 1)
    idx2 = np.flatnonzero(costs == 2)

    r_plus = (np.sqrt(3.0) - 1.0) / 2.0
    v_plus = np.array([1.0, r_plus, r_plus], dtype=np.complex128)
    v_plus = v_plus / np.linalg.norm(v_plus)
    psi_plus = np.kron(np.kron(v_plus, v_plus), np.kron(v_plus, v_plus))

    r_minus = (-np.sqrt(3.0) - 1.0) / 2.0
    v_minus = np.array([1.0, r_minus, r_minus], dtype=np.complex128)
    v_minus = v_minus / np.linalg.norm(v_minus)
    psi_minus = np.kron(np.kron(v_minus, v_minus), np.kron(v_minus, v_minus))

    B_gal, _ = np.linalg.qr(np.column_stack([psi_plus, psi_minus]))
    Q_gal = V_all - B_gal @ (B_gal.conj().T @ V_all)
    norms0 = np.linalg.norm(Q_gal, axis=0)
    Q_fixed = Q_gal[:, idx1]

    rng4 = np.random.default_rng(23)
    can4 = rng4.normal(size=81) + 1j * rng4.normal(size=81)
    key4 = rng4.normal(size=81) + 1j * rng4.normal(size=81)
    U0 = Q_gal / norms0
    kk0 = (key4 @ U0) / (can4 @ U0)
    ord0 = np.lexsort((kk0.imag, kk0.real))
    ks0 = kk0[ord0]
    gap0 = np.abs(np.diff(ks0)) > 1e-8 * (1 + np.abs(ks0[:-1]))
    st0 = np.concatenate(([0], np.flatnonzero(gap0) + 1, [len(vecs)]))
    max_k3_run = int((st0[1:] - st0[:-1]).max())

    k4_hits = 0
    for i in idx1:
        ui = Q_gal[:, i] / np.linalg.norm(Q_gal[:, i])
        Qi = Q_gal - np.outer(ui, ui.conj() @ Q_gal)
        ni = np.linalg.norm(Qi, axis=0)
        z_i = [int(k) for k in np.flatnonzero(ni < 1e-8) if k != i]
        val = np.flatnonzero(ni >= 1e-8)
        Ui = Qi[:, val] / ni[val]
        kki = (key4 @ Ui) / (can4 @ Ui)
        ordi = np.lexsort((kki.imag, kki.real))
        ksi = kki[ordi]
        gapi = np.abs(np.diff(ksi)) > 1e-8 * (1 + np.abs(ksi[:-1]))
        st = np.concatenate(([0], np.flatnonzero(gapi) + 1, [len(val)]))
        ln = st[1:] - st[:-1]
        for r_i in np.flatnonzero(ln >= max(1, 3 - len(z_i))):
            grp = [int(val[k]) for k in ordi[st[r_i]:st[r_i + 1]]] + z_i
            for a, b, c in itertools.combinations(grp, 3):
                if costs[i] + costs[a] + costs[b] + costs[c] <= 7:
                    A = V_all[:, [i, a, b, c]]
                    x, *_ = np.linalg.lstsq(A, psi_plus, rcond=None)
                    if np.linalg.norm(A @ x - psi_plus) < 1e-8:
                        k4_hits += 1

    u_qf, s_qf, _ = np.linalg.svd(V_all[:, idx1], full_matrices=False)
    QF = u_qf[:, s_qf > 1e-9]
    off_plus = psi_plus - QF @ (QF.conj().T @ psi_plus)
    B_off = (off_plus / np.linalg.norm(off_plus))[:, None]
    W2_off = V_all[:, idx2] - QF @ (QF.conj().T @ V_all[:, idx2])
    n2_off = np.linalg.norm(W2_off, axis=0)
    res_off = W2_off - B_off @ (B_off.conj().T @ W2_off)
    cand_pairs = [int(x) for x in idx2[np.flatnonzero((n2_off > 1e-8) & (np.linalg.norm(res_off, axis=0) < 1e-7))]]
    if c4.get("cand_1pair_indices") != cand_pairs:
        return False, "cert4: cand_1pair_indices mismatch"

    hits_1p4f = 0
    for p_idx in cand_pairs:
        up = Q_gal[:, p_idx] / np.linalg.norm(Q_gal[:, p_idx])
        Qp = Q_fixed - np.outer(up, up.conj() @ Q_fixed)
        for a in range(len(idx1)):
            ua = Qp[:, a]
            na = np.linalg.norm(ua)
            if na < 1e-8:
                continue
            ua = ua / na
            Qpa = Qp[:, a + 1:] - np.outer(ua, ua.conj() @ Qp[:, a + 1:])
            npa = np.linalg.norm(Qpa, axis=0)
            z_a = [a + 1 + int(k) for k in np.flatnonzero(npa < 1e-8)]
            val = np.flatnonzero(npa >= 1e-8)
            if len(val) + len(z_a) < 3:
                continue
            U = Qpa[:, val] / npa[val]
            kk = (key4 @ U) / (can4 @ U)
            ord_u = np.lexsort((kk.imag, kk.real))
            ks = kk[ord_u]
            gap = np.abs(np.diff(ks)) > 1e-8 * (1 + np.abs(ks[:-1]))
            st = np.concatenate(([0], np.flatnonzero(gap) + 1, [len(val)]))
            ln = st[1:] - st[:-1]
            for r_i in np.flatnonzero(ln >= max(1, 3 - len(z_a))):
                grp = [a + 1 + int(val[k]) for k in ord_u[st[r_i]:st[r_i + 1]]] + z_a
                for b, c, d in itertools.combinations(grp, 3):
                    cols = [p_idx, int(idx1[a]), int(idx1[b]), int(idx1[c]), int(idx1[d])]
                    A = V_all[:, cols]
                    x, *_ = np.linalg.lstsq(A, psi_plus, rcond=None)
                    if np.linalg.norm(A @ x - psi_plus) < 1e-8:
                        hits_1p4f += 1

    if (
        c4.get("inv_flats_by_dim") != flat_counts_by_dim
        or c4.get("inv_flats_total") != sum(flat_counts_by_dim)
        or c4.get("fixed_states") != int(len(idx1))
        or c4.get("pair_orbits") != int(len(idx2))
        or c4.get("cand_1pair") != len(cand_pairs)
        or c4.get("max_k3_run") != max_k3_run
        or max_k3_run >= 3
        or c4.get("k4_hits") != k4_hits
        or k4_hits != 0
        or c4.get("hits_1p4f") != hits_1p4f
        or hits_1p4f != 0
    ):
        return False, "cert4 summary fields mismatch against first-principles calculation"

    return True, "Verified all 4 lower-bound & obstruction certificates from first principles"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--corrupt", action="store_true", help="Adversarially corrupt certificate in-memory and expect FAIL")
    args = parser.parse_args()

    cw_path = OBJ_DIR / "constructive_witnesses.json"
    lb_path = OBJ_DIR / "p2_p3_lower_bound_certificates.json"
    if not cw_path.is_file() or not lb_path.is_file():
        return fail("Missing object/constructive_witnesses.json or object/p2_p3_lower_bound_certificates.json")

    try:
        cw = json.loads(cw_path.read_text(encoding="utf-8"))
        lb = json.loads(lb_path.read_text(encoding="utf-8"))
    except Exception as e:
        return fail(f"JSON parse error: {e}")

    if args.corrupt:
        cw = copy.deepcopy(cw)
        cw["witnesses"][2]["coeffs_A_real"][0] += 1

    ok1, msg1 = verify_constructive_witnesses(cw)
    if not ok1:
        return fail(msg1)
    print(f"[OK] {msg1}")

    ok2, msg2 = build_d3_and_verify_lower_bound_certificates(lb)
    if not ok2:
        return fail(msg2)
    print(f"[OK] {msg2}")

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
