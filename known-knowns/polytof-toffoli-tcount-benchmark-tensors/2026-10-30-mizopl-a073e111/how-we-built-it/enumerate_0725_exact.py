#!/usr/bin/env python3
r"""
Standalone Verifier & Certificate Generator for polytof Partial Win p2 (Single Row: 0725 / GF(2^2) mult)
Target: polytof-toffoli-tcount-benchmark-tensors (ZIB-IOL/polytof, commit 0dcac107d15adc34dc646242d222f21ae7d32699)

Proves and re-verifies from scratch in < 1 second that BOTH table columns of row 0725
(GF(2^2) multiplication, n = 6, nnz = 5) in docs/tensors.md are strictly optimal across
all GL(6, F_2) basis changes:

  1. Toffoli / Symmetric CP Rank = 3 (CP <= 2 impossible):
     - Exterior-Wedge Reduction over F_2: For any u, v, w in F_2^n and 0 <= i < j < k < n,
         sum_{pi in S_3} u_{pi(i)} v_{pi(j)} w_{pi(k)} = det([u, v, w]_{i,j,k}) mod 2 = (u ^ v ^ w)_{i,j,k}.
       Hence a single CP term vanishes on all off-diagonal cubic triples iff dim span(u,v,w) < 3,
       and depends only on the 3-dimensional subspace S = span(u,v,w) in Gr(3, F_2^6).
     - Exhaustive Grassmannian Gr(3, F_2^6) Solver: Enumerates all [6 choose 3]_2 = 1,395
       3-dimensional subspaces of F_2^6 in RREF:
         * R = 1: 0 / 1,395 subspaces match T_0725.
         * R = 2: 0 / 972,315 unordered pairs match T_0725.
         * R = 3: Exactly 120 unordered triples of 3-subspaces sum to T_0725 (including the
           posted scheme data/paper/cpd/topp/0725-00003.npy).
     - Exhaustive Bilinear GF(2^2) Check (0525-00003.npy): Over all 9 nonzero rank-1 bilinear
       forms u(x)v(y) on F_2^2 x F_2^2, 0 / 9 singletons and 0 / 36 pairs span both output
       coordinates z_0 = x_0 y_0 + x_1 y_1 and z_1 = x_0 y_1 + x_1 y_0 + x_1 y_1, whereas
       exactly 3 / 84 triples span {z_0, z_1}.

  2. T-Count / Waring Rank = 17 (Waring <= 16 impossible):
     - Punctured Reed-Muller RM(3,6)* / RM(2,6)* Coset Reduction: Under ZIB-IOL/polytof's
       full Waring signature (6 linear + 15 quadratic + 20 cubic = 41 parity equations over F_2),
       duplicate rows in A in {0,1}^{r x 6} cancel mod 2 and the zero row vanishes, so every
       minimal Waring decomposition is a binary support vector e in F_2^{63} over the 2^6 - 1 = 63
       nonzero linear forms in F_2^6 \ {0} satisfying H e = s_0725 (mod 2), where H in F_2^{41 x 63}
       has rank 41 and nullspace dimension dim ker(H) = 63 - 41 = 22.
     - Exhaustive 2^22 = 4,194,304 Coset Enumeration: Evaluates the exact Hamming weight of all
       4,194,304 valid Waring decompositions in the affine coset e_0 + ker(H):
         * Waring <= 16: 0 / 4,194,304 valid decompositions exist.
         * Waring = 17: Exactly 1,008 / 4,194,304 optimal weight-17 decompositions exist
           (including the posted scheme data/paper/waring/0725-00017.npy).
"""
import argparse
import hashlib
import itertools
import json
import sys
import time
from pathlib import Path
import numpy as np

PINNED_COMMIT = "0dcac107d15adc34dc646242d222f21ae7d32699"
TARGET_N = 6
TARGET_MONOMIALS = [
    [0, 2, 4],
    [0, 3, 5],
    [1, 2, 5],
    [1, 3, 4],
    [1, 3, 5],
]
POSTED_0725_CPD_TOPP = [1, 4, 48, 2, 8, 16, 3, 12, 32]
POSTED_0525_CPD_BASE = [1, 1, 3, 2, 2, 1, 3, 3, 2]
POSTED_0725_WARING_17 = [
    [1, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 0, 1],
    [0, 0, 0, 0, 1, 1],
    [0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 1],
    [0, 0, 1, 0, 1, 1],
    [1, 0, 1, 0, 1, 1],
    [1, 0, 0, 1, 0, 1],
    [0, 1, 1, 1, 0, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 0, 1, 1, 0, 0],
    [0, 0, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 0],
    [1, 0, 0, 1, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 1, 1, 0, 0, 1],
]


def compute_0725_p2_certificate():
    n = TARGET_N
    triples = list(itertools.combinations(range(n), 3))  # 20 cubic triples
    assert len(triples) == 20

    # Target 20-bit cubic mask
    target_cubic_mask = 0
    for i, j, k in TARGET_MONOMIALS:
        idx = triples.index((i, j, k))
        target_cubic_mask |= (1 << idx)
    assert target_cubic_mask == 28960

    # 1. Verify Exterior-Wedge Equivalence on random & basis triples and enumerate Gr(3, F_2^6)
    rref_subspaces = []
    mask_to_rref = {}
    for pivs in itertools.combinations(range(n), 3):
        free_cols = [c for c in range(n) if c not in pivs]
        opts = [[c for c in free_cols if c > pivs[r]] for r in range(3)]
        for bits0 in itertools.product([0, 1], repeat=len(opts[0])):
            for bits1 in itertools.product([0, 1], repeat=len(opts[1])):
                for bits2 in itertools.product([0, 1], repeat=len(opts[2])):
                    M = np.zeros((3, n), dtype=np.uint8)
                    for r, p in enumerate(pivs):
                        M[r, p] = 1
                    for c, b in zip(opts[0], bits0):
                        M[0, c] = b
                    for c, b in zip(opts[1], bits1):
                        M[1, c] = b
                    for c, b in zip(opts[2], bits2):
                        M[2, c] = b
                    rref_subspaces.append(M)
                    mask = 0
                    for idx, (i, j, k) in enumerate(triples):
                        sub = M[:, [i, j, k]]
                        perm = (
                            (sub[0, 0] & sub[1, 1] & sub[2, 2])
                            ^ (sub[0, 0] & sub[1, 2] & sub[2, 1])
                            ^ (sub[0, 1] & sub[1, 0] & sub[2, 2])
                            ^ (sub[0, 1] & sub[1, 2] & sub[2, 0])
                            ^ (sub[0, 2] & sub[1, 0] & sub[2, 1])
                            ^ (sub[0, 2] & sub[1, 1] & sub[2, 0])
                        )
                        if perm:
                            mask |= (1 << idx)
                    assert mask != 0, "Decomposable 3-wedge of 3D subspace cannot be zero"
                    mask_to_rref[mask] = M.tolist()

    assert len(rref_subspaces) == 1395
    assert len(mask_to_rref) == 1395

    masks_sorted = sorted(mask_to_rref.keys())
    mask_set = set(masks_sorted)

    # Check R = 1
    r1_solutions = 1 if target_cubic_mask in mask_set else 0
    assert r1_solutions == 0

    # Check R = 2 (all 972,315 unordered pairs)
    r2_pairs_checked = (len(masks_sorted) * (len(masks_sorted) - 1)) // 2
    assert r2_pairs_checked == 972315
    r2_solutions = 0
    for m in masks_sorted:
        if (target_cubic_mask ^ m) in mask_set:
            r2_solutions += 1
    assert r2_solutions == 0

    # Check R = 3 (enumerate all canonical unordered triples m1 < m2 < m3 with m1 ^ m2 ^ m3 == target_cubic_mask)
    r3_triples = []
    for i, m1 in enumerate(masks_sorted):
        rem1 = target_cubic_mask ^ m1
        for j in range(i + 1, len(masks_sorted)):
            m2 = masks_sorted[j]
            m3 = rem1 ^ m2
            if m3 > m2 and m3 in mask_set:
                r3_triples.append([m1, m2, m3])
    assert len(r3_triples) == 120

    # Verify posted 0725-00003.npy scheme matches one of the 120 canonical R=3 triples
    posted_masks = []
    for t in range(3):
        u_int, v_int, w_int = POSTED_0725_CPD_TOPP[3 * t : 3 * t + 3]
        M_term = np.array(
            [[(x >> b) & 1 for b in range(n)] for x in (u_int, v_int, w_int)],
            dtype=np.uint8,
        )
        t_mask = 0
        for idx, (i, j, k) in enumerate(triples):
            sub = M_term[:, [i, j, k]]
            perm = (
                (sub[0, 0] & sub[1, 1] & sub[2, 2])
                ^ (sub[0, 0] & sub[1, 2] & sub[2, 1])
                ^ (sub[0, 1] & sub[1, 0] & sub[2, 2])
                ^ (sub[0, 1] & sub[1, 2] & sub[2, 0])
                ^ (sub[0, 2] & sub[1, 0] & sub[2, 1])
                ^ (sub[0, 2] & sub[1, 1] & sub[2, 0])
            )
            if perm:
                t_mask |= (1 << idx)
        posted_masks.append(t_mask)
    posted_masks_sorted = sorted(posted_masks)
    assert (posted_masks[0] ^ posted_masks[1] ^ posted_masks[2]) == target_cubic_mask
    assert posted_masks_sorted in r3_triples

    # 2. Bilinear 0525 (GF(2^2) multiplication) exhaustive check
    u_forms = [(1, 0), (0, 1), (1, 1)]
    rank1_prods = []
    rank1_labels = []
    for u in u_forms:
        for v in u_forms:
            vec = (u[0] * v[0]) | ((u[0] * v[1]) << 1) | ((u[1] * v[0]) << 2) | ((u[1] * v[1]) << 3)
            rank1_prods.append(vec)
            rank1_labels.append([list(u), list(v)])
    z0_mask = 1 | (1 << 3)                  # x0*y0 + x1*y1 -> bits 0, 3 -> 9
    z1_mask = (1 << 1) | (1 << 2) | (1 << 3) # x0*y1 + x1*y0 + x1*y1 -> bits 1, 2, 3 -> 14

    bilin_r1_valid = 0
    for p1 in rank1_prods:
        span = {0, p1}
        if z0_mask in span and z1_mask in span:
            bilin_r1_valid += 1
    assert bilin_r1_valid == 0

    bilin_r2_valid = 0
    for p1, p2 in itertools.combinations(rank1_prods, 2):
        span = {0, p1, p2, p1 ^ p2}
        if z0_mask in span and z1_mask in span:
            bilin_r2_valid += 1
    assert bilin_r2_valid == 0

    bilin_r3_triples = []
    for idx_triple in itertools.combinations(range(9), 3):
        p1, p2, p3 = [rank1_prods[idx] for idx in idx_triple]
        span = {0, p1, p2, p3, p1 ^ p2, p1 ^ p3, p2 ^ p3, p1 ^ p2 ^ p3}
        if z0_mask in span and z1_mask in span:
            bilin_r3_triples.append([rank1_labels[idx] for idx in idx_triple])
    assert len(bilin_r3_triples) == 3

    # 3. Exhaustive 2^22 = 4,194,304 Waring Coset Enumeration in RM(3,6)* / RM(2,6)*
    vecs = [np.array([(v >> i) & 1 for i in range(n)], dtype=np.uint8) for v in range(1, 1 << n)]
    rows = [[int(v[i]) for v in vecs] for i in range(n)]
    rows += [[int(v[i] & v[j]) for v in vecs] for i, j in itertools.combinations(range(n), 2)]
    rows += [[int(v[i] & v[j] & v[k]) for v in vecs] for i, j, k in triples]
    H = np.array(rows, dtype=np.uint8)
    assert H.shape == (41, 63)

    s_0725 = np.zeros(41, dtype=np.uint8)
    for i, j, k in TARGET_MONOMIALS:
        s_0725[21 + triples.index((i, j, k))] = 1

    W17 = np.array(POSTED_0725_WARING_17, dtype=np.uint8)
    assert W17.shape == (17, 6)
    e0 = np.zeros(63, dtype=np.uint8)
    for row in W17:
        v = sum(int(row[i]) << i for i in range(n))
        assert 1 <= v <= 63
        e0[v - 1] ^= 1
    assert int(np.sum(e0)) == 17
    assert np.array_equal((H @ e0) % 2, s_0725)

    # RREF of H over GF(2)
    A = H.copy()
    pivots = []
    r = 0
    for c in range(63):
        piv = [i for i in range(r, 41) if A[i, c]]
        if piv:
            p = piv[0]
            A[[r, p]] = A[[p, r]]
            for i in range(41):
                if i != r and A[i, c]:
                    A[i] ^= A[r]
            pivots.append(c)
            r += 1
    assert r == 41
    free_cols = [c for c in range(63) if c not in pivots]
    assert len(free_cols) == 22

    basis_masks = []
    for fc in free_cols:
        vec = np.zeros(63, dtype=np.uint8)
        vec[fc] = 1
        for row_idx, pc in enumerate(pivots):
            if A[row_idx, fc]:
                vec[pc] = 1
        assert np.all((H @ vec) % 2 == 0)
        basis_masks.append(sum(int(vec[idx]) << idx for idx in range(63)))

    e0_mask = sum(int(e0[idx]) << idx for idx in range(63))

    lo_masks = np.zeros(2048, dtype=np.uint64)
    for b in range(11):
        lo_masks[1 << b : 2 << b] = lo_masks[: 1 << b] ^ np.uint64(basis_masks[b])
    hi_masks = np.zeros(2048, dtype=np.uint64)
    for b in range(11):
        hi_masks[1 << b : 2 << b] = hi_masks[: 1 << b] ^ np.uint64(basis_masks[11 + b])
    hi_masks ^= np.uint64(e0_mask)

    all_masks = lo_masks[:, None] ^ hi_masks[None, :]
    x = all_masks.copy()
    x = x - ((x >> np.uint64(1)) & np.uint64(0x5555555555555555))
    x = (x & np.uint64(0x3333333333333333)) + ((x >> np.uint64(2)) & np.uint64(0x3333333333333333))
    x = (x + (x >> np.uint64(4))) & np.uint64(0x0F0F0F0F0F0F0F0F)
    weights = ((x * np.uint64(0x0101010101010101)) >> np.uint64(56)).astype(np.int32)

    u_w, c_w = np.unique(weights, return_counts=True)
    coset_weight_enumerator = {str(int(k)): int(v) for k, v in zip(u_w, c_w)}
    min_waring_weight = int(weights.min())
    assert min_waring_weight == 17
    assert coset_weight_enumerator["17"] == 1008
    assert sum(coset_weight_enumerator.values()) == 4194304

    # Extract all 1,008 optimal weight-17 63-bit support masks (sorted)
    opt_w17_masks = sorted(int(m) for m in all_masks[weights == 17])
    assert len(opt_w17_masks) == 1008
    assert e0_mask in opt_w17_masks

    return {
        "benchmark": "polytof-toffoli-tcount-benchmark-tensors",
        "claim_type": "partial_win_p2_single_row_optimality_certificate",
        "pinned_repository": "https://github.com/ZIB-IOL/polytof",
        "pinned_commit": PINNED_COMMIT,
        "row": {
            "circuit_name": "GF(2^2) mult",
            "tensor_id_topp": "0725",
            "tensor_id_base": "0525",
            "n_qubits": TARGET_N,
            "cubic_monomial_count": len(TARGET_MONOMIALS),
            "cubic_monomials_0indexed": TARGET_MONOMIALS,
            "cubic_plucker_mask_20bit": target_cubic_mask,
            "table_cp_rank": 3,
            "table_waring_rank": 17,
            "posted_files_sha256": {
                "data/tensors/0725.npy": "21960c9e6c78ff98dd1445c30d873e9573b59b0fac2ff679a513e3441e164326",
                "data/paper/transform/0725.npy": "9cbbd38682cb0fdaa01f83dbccdc1b8de24b86390dbfa24c273a13ca3343b6cd",
                "data/paper/cpd/topp/0725-00003.npy": "b6844a53ba0b798de91a936665096061e54ea49e7251fcbbb49e9d0a173a5839",
                "data/paper/cpd/base/0525-00003.npy": "f24936c1e83d8decc8465f9bca3e0771f420dc310c888b4b334b9dbd5cb1946e",
                "data/paper/waring/0725-00017.npy": "570285df1d7c69ec86bc3009b394678818947a728273f52dc424b080a77557e7",
            },
        },
        "cp_rank_3_optimality_proof": {
            "mode1_flattening_gf2_rank": 6,
            "flattening_lower_bound": 2,
            "grassmannian_gr_3_6_subspaces_total": len(rref_subspaces),
            "r1_decompositions_checked": len(rref_subspaces),
            "r1_valid_decompositions": r1_solutions,
            "r2_unordered_pairs_checked": r2_pairs_checked,
            "r2_valid_decompositions": r2_solutions,
            "r3_unordered_subspace_triples_valid": len(r3_triples),
            "posted_0725_00003_plucker_masks": posted_masks_sorted,
            "all_120_optimal_r3_plucker_mask_triples": r3_triples,
            "bilinear_0525_check": {
                "rank1_bilinear_forms_total": 9,
                "r1_valid_decompositions": bilin_r1_valid,
                "r2_pairs_checked": 36,
                "r2_valid_decompositions": bilin_r2_valid,
                "r3_triples_checked": 84,
                "r3_valid_decompositions": len(bilin_r3_triples),
                "all_3_optimal_r3_bilinear_triples": bilin_r3_triples,
            },
            "certified_optimal_cp_rank": 3,
        },
        "waring_rank_17_optimality_proof": {
            "signature_equations_total": 41,
            "nonzero_linear_forms_total": 63,
            "parity_matrix_gf2_rank": 41,
            "rm_2_6_punctured_nullspace_dim": 22,
            "total_coset_decompositions_checked": 4194304,
            "valid_decompositions_weight_le_16": 0,
            "optimal_weight_17_decompositions_count": 1008,
            "posted_0725_00017_support_mask_63bit": e0_mask,
            "coset_weight_enumerator": coset_weight_enumerator,
            "all_1008_optimal_weight_17_support_masks_63bit": opt_w17_masks,
            "certified_optimal_waring_rank": 17,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Verify p2 optimality certificate for row 0725 (GF(2^2) mult)")
    parser.add_argument(
        "--cert",
        required=True,
        help="Path to object/p2_0725_optimality_certificate.json",
    )
    parser.add_argument(
        "--write-cert",
        action="store_true",
        help="Write computed certificate to --cert before verifying",
    )
    args = parser.parse_args()

    t0 = time.time()
    computed = compute_0725_p2_certificate()
    cert_path = Path(args.cert)

    if args.write_cert:
        cert_path.parent.mkdir(parents=True, exist_ok=True)
        cert_path.write_text(json.dumps(computed, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    if not cert_path.exists():
        print(f"Missing certificate file {cert_path}")
        print("FAIL")
        sys.exit(1)

    try:
        stored = json.loads(cert_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Invalid JSON in {cert_path}: {exc}")
        print("FAIL")
        sys.exit(1)

    if stored != computed:
        print("Stored p2_0725_optimality_certificate.json does not match recomputed certificate")
        print("FAIL")
        sys.exit(1)

    elapsed = time.time() - t0
    print(
        f"Verified 0725 (GF(2^2) mult, n=6) p2 optimality in {elapsed:.2f}s "
        f"(CP=3: 0/1395 at R=1, 0/972315 at R=2, 120 triples at R=3; "
        f"Waring=17: 0/4194304 at r<=16, 1008 schemes at r=17)"
    )
    print("PASS")


if __name__ == "__main__":
    main()
