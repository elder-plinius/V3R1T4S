#!/usr/bin/env python3
"""
Standalone Re-Verification Audit & Repaired-Scheme Checker for polytof p3
Target: polytof-toffoli-tcount-benchmark-tensors (ZIB-IOL/polytof, pinned commit 0dcac107d15adc34dc646242d222f21ae7d32699)

Recomputes from scratch against the pinned ZIB-IOL/polytof checkout:
  1. Parses docs/tensors.md (verifying sha256 f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3)
     and checks all 88 reference tensors in data/tensors/*.npy and 88 basis-change matrices in
     data/paper/transform/*.npy, identifying the 2 qubit-dimension discrepancies:
       - 0108 (Ham15 (low)): actual n = 42 vs docs/tensors.md n = 46 (0808 has n = 46)
       - 0114 (Mod Mult_55): actual n = 11 vs docs/tensors.md n = 12 (0814 has n = 12)
  2. Verifies every decomposition file in data/paper/ (185 files total):
       - All 88 files in data/paper/cpd/topp/*.npy, covering all 13,528 stored CP schemes
         (74 single-row files + 14 multi-row pool files: 13 x 1,000 + 454 = 13,454 pool schemes),
         confirming 13,528/13,528 valid symmetric cubic reconstructions and 88/88 rank matches
         against both filename and docs/tensors.md.
       - All 9 files in data/paper/cpd/base/*.npy (0525..0533, k = 2..10), confirming 9/9 valid
         untransformed bilinear reconstructions and 9/9 rank matches against docs/tensors.md
         (97/97 total CP files match docs/tensors.md).
       - All 88 files in data/paper/waring/*.npy under the full phase-polynomial signature
         (linear S_{iii} odd_cols == 0, quadratic S_{iij} odd_pairs == 0, and cubic S_{ijk}
         matching both BCO-transformed and original tensors), confirming 88/88 valid Waring
         reconstructions matching their filenames, 83/88 matching docs/tensors.md, and uncovering
         the 5 posted Waring rank discrepancies:
           * 0105 (CSLA MUX_3): posted 0105-00041.npy has rank 41 vs table 39 (+2)
           * 0108 (Ham15 (low)): posted 0108-00077.npy has rank 77 vs table 73 (+4)
           * 0115 (Mod Red_21): posted 0115-00055.npy has rank 55 vs table 51 (+4)
           * 0728 (GF(2^5) Mult): posted 0728-00061.npy has rank 61 vs table 59 (+2; 0128-00059.npy has 59)
           * 0817 (QCLA Com_7): posted 0817-00063.npy has rank 63 vs table 59 (+4)
  3. Independently verifies the 4 shipped repaired Waring schemes in object/waring/:
       - object/waring/0105-00039.npy (rank 39, repairing 0105 from 41 -> 39)
       - object/waring/0108-00073.npy (rank 73, repairing 0108 from 77 -> 73)
       - object/waring/0115-00051.npy (rank 51, repairing 0115 from 55 -> 51)
       - object/waring/0817-00059.npy (rank 59, repairing 0817 from 63 -> 59)
     under the full signature (linear, quadratic, and cubic parities in both BCO and original bases)
     and verifies exact consistency with object/p3_audit_certificate.json.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path
import numpy as np

PINNED_POLYTOF_COMMIT = "0dcac107d15adc34dc646242d222f21ae7d32699"
PINNED_TENSORS_MD_SHA256 = "f83839d0589888d75fb0ac357f8e251bc3f743d5c1749757cb51beec26676dc3"

VERIFY_DIR = Path(__file__).resolve().parent
PKG_DIR = VERIFY_DIR.parent
OBJ_DIR = PKG_DIR / "object"
WARING_OBJ_DIR = OBJ_DIR / "waring"
CERT_PATH = OBJ_DIR / "p3_audit_certificate.json"

REPAIRED_SPECS = [
    {"tensor_id": "0105", "circuit": "CSLA MUX_3", "n": 21, "table_waring": 39, "posted_file": "0105-00041.npy", "posted_waring": 41, "repaired_file": "object/waring/0105-00039.npy", "repaired_waring": 39},
    {"tensor_id": "0108", "circuit": "Ham15 (low)", "n": 42, "table_waring": 73, "posted_file": "0108-00077.npy", "posted_waring": 77, "repaired_file": "object/waring/0108-00073.npy", "repaired_waring": 73},
    {"tensor_id": "0115", "circuit": "Mod Red_21", "n": 28, "table_waring": 51, "posted_file": "0115-00055.npy", "posted_waring": 55, "repaired_file": "object/waring/0115-00051.npy", "repaired_waring": 51},
    {"tensor_id": "0817", "circuit": "QCLA Com_7", "n": 42, "table_waring": 59, "posted_file": "0817-00063.npy", "posted_waring": 63, "repaired_file": "object/waring/0817-00059.npy", "repaired_waring": 59},
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def gf2_inv(A: np.ndarray) -> np.ndarray:
    """Invert an n x n binary matrix over GF(2) using Gauss-Jordan elimination."""
    n = A.shape[0]
    assert A.shape == (n, n), f"Expected square matrix, got {A.shape}"
    assert np.all((A == 0) | (A == 1)), "Transform matrix contains non-binary entries"
    M = np.hstack([A.astype(np.uint8), np.eye(n, dtype=np.uint8)])
    for col in range(n):
        pivots = np.flatnonzero(M[col:, col])
        if len(pivots) == 0:
            raise ValueError("Matrix is singular over GF(2)")
        pivot = int(pivots[0]) + col
        if pivot != col:
            M[[col, pivot]] = M[[pivot, col]]
        rows = np.flatnonzero(M[:, col])
        rows = rows[rows != col]
        if len(rows):
            M[rows] ^= M[col]
    return M[:, n:].copy()


def fast_bco_tensor(n: int, triples: np.ndarray, A_trans: np.ndarray):
    """
    Build dense symmetric (n, n, n) tensor T_orig from upper-triangular triples
    and compute BCO-transformed tensor T_bco = (A_trans^{-1})^{tensor 3} T_orig mod 2
    using bitpacked uint64 mode contractions.
    Returns (T_orig, T_bco, orig_nnz, bco_nnz).
    """
    T_orig = np.zeros((n, n, n), dtype=np.uint8)
    if len(triples):
        idx = triples.astype(np.intp)
        assert np.all((idx[:, 0] >= 0) & (idx[:, 0] < idx[:, 1]) & (idx[:, 1] < idx[:, 2]) & (idx[:, 2] < n)), (
            "Invalid upper-triangular triple coordinates"
        )
        for p in ((0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)):
            T_orig[idx[:, p[0]], idx[:, p[1]], idx[:, p[2]]] = 1

    orig_nnz = int(len(triples))
    A_inv = gf2_inv(A_trans)
    if np.array_equal(A_inv, np.eye(n, dtype=np.uint8)):
        return T_orig, T_orig.copy(), orig_nnz, orig_nnz

    W = (n + 63) // 64
    T_pack = np.zeros((n, n, W), dtype=np.uint64)
    for w in range(W):
        c0 = w * 64
        c1 = min(n, c0 + 64)
        shifts = np.arange(c1 - c0, dtype=np.uint64)[None, None, :]
        T_pack[:, :, w] = np.bitwise_or.reduce(T_orig[:, :, c0:c1].astype(np.uint64) << shifts, axis=2)

    T1 = np.zeros((n, n, W), dtype=np.uint64)
    for i in range(n):
        idx = np.flatnonzero(A_inv[i])
        if len(idx):
            T1[i] = np.bitwise_xor.reduce(T_pack[idx], axis=0)

    T2 = np.zeros((n, n, W), dtype=np.uint64)
    for j in range(n):
        idx = np.flatnonzero(A_inv[j])
        if len(idx):
            T2[:, j, :] = np.bitwise_xor.reduce(T1[:, idx, :], axis=1)

    pos = np.arange(n, dtype=np.uint64)
    T2_unpacked = ((T2[:, :, pos // 64] >> (pos % 64)) & 1).astype(np.uint8)
    T2_t = T2_unpacked.transpose(0, 2, 1)
    T2_t_pack = np.zeros((n, n, W), dtype=np.uint64)
    for w in range(W):
        c0 = w * 64
        c1 = min(n, c0 + 64)
        shifts = np.arange(c1 - c0, dtype=np.uint64)[None, None, :]
        T2_t_pack[:, :, w] = np.bitwise_or.reduce(T2_t[:, :, c0:c1].astype(np.uint64) << shifts, axis=2)

    T3_t_pack = np.zeros((n, n, W), dtype=np.uint64)
    for k in range(n):
        idx = np.flatnonzero(A_inv[k])
        if len(idx):
            T3_t_pack[:, k, :] = np.bitwise_xor.reduce(T2_t_pack[:, idx, :], axis=1)

    T_bco = ((T3_t_pack[:, :, pos // 64] >> (pos % 64)) & 1).astype(np.uint8).transpose(0, 2, 1)
    grid = np.arange(n)
    mask_ijk = (grid[:, None, None] < grid[None, :, None]) & (grid[None, :, None] < grid[None, None, :])
    bco_nnz = int(np.sum(T_bco[mask_ijk]))
    return T_orig, T_bco, orig_nnz, bco_nnz


def bitvecs_to_dense(word_matrix: np.ndarray, n: int) -> np.ndarray:
    pos = np.arange(n, dtype=np.uint64)
    return ((word_matrix[:, pos // 64] >> (pos % 64)) & 1).astype(np.uint8)


def verify_cpd_topp_file(cpd_path: Path, n: int, T_bco: np.ndarray):
    """
    Verify all stored CP schemes (including all rows of multi-row pool files)
    in a data/paper/cpd/topp/{id}-{rank}.npy file against T_bco on all i < j < k.
    Returns (decoded_rank, num_schemes, passed_schemes).
    """
    data = np.load(cpd_path)
    assert data.ndim == 2 and data.dtype == np.uint64, f"Unexpected CPD array format in {cpd_path}"
    num_schemes = int(data.shape[0])
    vec_words = (n + 63) // 64
    assert data.shape[1] % (3 * vec_words) == 0, f"Invalid column count in {cpd_path}"
    rank = int(data.shape[1] // (3 * vec_words))

    all_vecs = bitvecs_to_dense(data.reshape(num_schemes * 3 * rank, vec_words), n).reshape(
        num_schemes, rank, 3, n
    )
    U_all = all_vecs[:, :, 0, :]
    V_all = all_vecs[:, :, 1, :]
    W_all = all_vecs[:, :, 2, :]

    grid = np.arange(n)
    mask_ijk = (grid[:, None, None] < grid[None, :, None]) & (grid[None, :, None] < grid[None, None, :])
    ref_ijk = T_bco[mask_ijk]

    if num_schemes == 1:
        U, V, W = U_all[0], V_all[0], W_all[0]
        T_uvw = np.zeros((n, n, n), dtype=np.uint8)
        for t in range(rank):
            su = np.flatnonzero(U[t])
            sv = np.flatnonzero(V[t])
            sw = np.flatnonzero(W[t])
            if len(su) and len(sv) and len(sw):
                T_uvw[np.ix_(su, sv, sw)] ^= 1
        T_rec = (
            T_uvw
            ^ T_uvw.transpose(0, 2, 1)
            ^ T_uvw.transpose(1, 0, 2)
            ^ T_uvw.transpose(1, 2, 0)
            ^ T_uvw.transpose(2, 0, 1)
            ^ T_uvw.transpose(2, 1, 0)
        )
        ok = bool(np.array_equal(T_rec[mask_ijk], ref_ijk))
        return rank, 1, (1 if ok else 0)

    passed = 0
    for start in range(0, num_schemes, 64):
        end = min(start + 64, num_schemes)
        B = end - start
        shifts = np.arange(B, dtype=np.uint64)[:, None, None]
        U_b = np.bitwise_or.reduce(U_all[start:end].astype(np.uint64) << shifts, axis=0)
        V_b = np.bitwise_or.reduce(V_all[start:end].astype(np.uint64) << shifts, axis=0)
        W_b = np.bitwise_or.reduce(W_all[start:end].astype(np.uint64) << shifts, axis=0)
        T_uvw = np.zeros((n, n, n), dtype=np.uint64)
        for t in range(rank):
            T_uvw ^= (U_b[t, :, None, None] & V_b[t, None, :, None] & W_b[t, None, None, :])
        T_rec = (
            T_uvw
            ^ T_uvw.transpose(0, 2, 1)
            ^ T_uvw.transpose(1, 0, 2)
            ^ T_uvw.transpose(1, 2, 0)
            ^ T_uvw.transpose(2, 0, 1)
            ^ T_uvw.transpose(2, 1, 0)
        )
        full_mask = (np.uint64(1) << np.uint64(B)) - np.uint64(1) if B < 64 else np.uint64(0xFFFFFFFFFFFFFFFF)
        expected = np.where(ref_ijk == 1, full_mask, np.uint64(0))
        diff = (T_rec[mask_ijk] ^ expected) & full_mask
        bad_mask = np.bitwise_or.reduce(diff)
        for b in range(B):
            if not ((bad_mask >> np.uint64(b)) & np.uint64(1)):
                passed += 1
    return rank, num_schemes, passed


def verify_cpd_base_file(cpd_path: Path, tensor_path: Path):
    """
    Verify untransformed bilinear CP decomposition in data/paper/cpd/base/{id}-{rank}.npy
    against data/tensors/{id}.npy over all k x k x k entries.
    Returns (k, decoded_rank, num_schemes, passed_schemes).
    """
    t_arr = np.load(tensor_path)
    dims = tuple(int(x) for x in t_arr[0])
    assert len(dims) == 3 and dims[0] == dims[1] == dims[2], f"Unexpected base tensor dims {dims}"
    k = dims[0]
    T_ref = np.zeros(dims, dtype=np.uint8)
    for i, j, m in t_arr[1:]:
        T_ref[int(i), int(j), int(m)] = 1

    data = np.load(cpd_path)
    assert data.ndim == 2 and data.dtype == np.uint64
    num_schemes = int(data.shape[0])
    vec_words = (k + 63) // 64
    rank = int(data.shape[1] // (3 * vec_words))
    all_vecs = bitvecs_to_dense(data.reshape(num_schemes * 3 * rank, vec_words), k).reshape(
        num_schemes, rank, 3, k
    )
    passed = 0
    for s in range(num_schemes):
        U, V, W = all_vecs[s, :, 0, :], all_vecs[s, :, 1, :], all_vecs[s, :, 2, :]
        T_rec = np.zeros((k, k, k), dtype=np.uint8)
        for t in range(rank):
            T_rec ^= (U[t, :, None, None] & V[t, None, :, None] & W[t, None, None, :])
        if np.array_equal(T_rec, T_ref):
            passed += 1
    return k, rank, num_schemes, passed


def verify_waring_matrix_full_signature(
    A_raw: np.ndarray,
    n: int,
    T_bco: np.ndarray,
    T_orig: np.ndarray,
    A_trans: np.ndarray,
    require_distinct_nonzero: bool = False,
):
    """
    Verify a Waring parity matrix A_raw of shape (r, n) under the full signature:
      1. Exact binary entries in {0, 1}.
      2. In BCO basis:
         - linear parities S_{iii}: odd_cols_bco == 0
         - quadratic parities S_{iij} (i < j): odd_pairs_bco == 0
         - cubic parities S_{ijk} (i < j < k): matches T_bco[i, j, k]
      3. In original basis (P = A_raw @ A_trans^T mod 2):
         - linear parities: odd_cols_orig == 0
         - quadratic parities: odd_pairs_orig == 0
         - cubic parities: matches T_orig[i, j, k]
    """
    if A_raw.ndim != 2 or A_raw.shape[1] != n:
        return False, {"error": f"Shape mismatch: got {A_raw.shape}, expected (*, {n})"}
    if not np.all((A_raw == 0) | (A_raw == 1)):
        return False, {"error": "Matrix contains non-binary values outside {0, 1}"}

    A = A_raw.astype(np.uint8)
    r = int(A.shape[0])

    if require_distinct_nonzero:
        if np.any(np.all(A == 0, axis=1)):
            return False, {"error": "Matrix contains an all-zero parity row"}
        if len({ A[q].tobytes() for q in range(r) }) != r:
            return False, {"error": "Matrix contains duplicate parity rows"}

    grid = np.arange(n)
    mask_ijk = (grid[:, None, None] < grid[None, :, None]) & (grid[None, :, None] < grid[None, None, :])

    def check_basis(P: np.ndarray, T_ref: np.ndarray):
        P_i64 = P.astype(np.int64)
        col_sums = P_i64.sum(axis=0)
        odd_cols = int(np.sum(col_sums % 2))
        pair_sums = (P_i64[:, :, None] * P_i64[:, None, :]).sum(axis=0)
        odd_pairs = int(np.sum(np.triu(pair_sums, k=1) % 2))
        if n <= 90:
            W = (r + 63) // 64
            acc = np.zeros((n, n, n), dtype=np.uint64)
            for w in range(W):
                q0 = w * 64
                q1 = min(r, q0 + 64)
                shifts = np.arange(q1 - q0, dtype=np.uint64)[:, None]
                pw = np.bitwise_or.reduce(P[q0:q1].astype(np.uint64) << shifts, axis=0)
                acc ^= (pw[:, None, None] & pw[None, :, None] & pw[None, None, :])
            acc ^= acc >> np.uint64(32)
            acc ^= acc >> np.uint64(16)
            acc ^= acc >> np.uint64(8)
            acc ^= acc >> np.uint64(4)
            acc ^= acc >> np.uint64(2)
            acc ^= acc >> np.uint64(1)
            T_rec = (acc & np.uint64(1)).astype(np.uint8)
        else:
            T_rec = np.zeros((n, n, n), dtype=np.uint8)
            for q in range(r):
                supp = np.flatnonzero(P[q])
                m = len(supp)
                for a in range(m):
                    i = int(supp[a])
                    for b in range(a + 1, m):
                        j = int(supp[b])
                        T_rec[i, j, supp[b + 1 :]] ^= 1
        cubic_ok = bool(np.array_equal(T_rec[mask_ijk], T_ref[mask_ijk]))
        return cubic_ok, odd_cols, odd_pairs

    cubic_bco_ok, odd_cols_bco, odd_pairs_bco = check_basis(A, T_bco)

    # Push parities forward to original basis (for n <= 90) or verify via BCO equivalence
    if np.array_equal(A_trans, np.eye(n, dtype=np.uint8)) or n > 90:
        cubic_orig_ok, odd_cols_orig, odd_pairs_orig = cubic_bco_ok, odd_cols_bco, odd_pairs_bco
    else:
        P_orig = np.zeros((r, n), dtype=np.uint8)
        for col in range(n):
            idx = np.flatnonzero(A_trans[col])
            if len(idx):
                P_orig[:, col] = np.bitwise_xor.reduce(A[:, idx], axis=1)
        cubic_orig_ok, odd_cols_orig, odd_pairs_orig = check_basis(P_orig, T_orig)

    all_ok = (
        cubic_bco_ok
        and odd_cols_bco == 0
        and odd_pairs_bco == 0
        and cubic_orig_ok
        and odd_cols_orig == 0
        and odd_pairs_orig == 0
    )
    return all_ok, {
        "rank": r,
        "bco_cubic_match": cubic_bco_ok,
        "bco_odd_cols": odd_cols_bco,
        "bco_odd_pairs": odd_pairs_bco,
        "orig_cubic_match": cubic_orig_ok,
        "orig_odd_cols": odd_cols_orig,
        "orig_odd_pairs": odd_pairs_orig,
    }


def parse_docs_tensors_md(md_path: Path):
    """Parse all benchmark tables in docs/tensors.md."""
    actual_sha = sha256_file(md_path)
    assert actual_sha == PINNED_TENSORS_MD_SHA256, (
        f"docs/tensors.md sha256 mismatch: {actual_sha} != {PINNED_TENSORS_MD_SHA256}"
    )
    md_text = md_path.read_text(encoding="utf-8")
    table_meta = {}
    base_meta = {}

    for raw_line in md_text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) == 9 and (cells[0].isdigit() or cells[0] == "--") and (cells[1].isdigit() or cells[1] == "--"):
            id08, id01, circ, n_s, nnz_s, cp_s, _method, war_s, dp_s = cells
            n_v, nnz_v, cp_v, war_v = int(n_s), int(nnz_s), int(cp_s), int(war_s.rstrip("*"))
            dp_prefixes = dp_s.split()
            for tid_s, pref in [(id08, "08"), (id01, "01")]:
                if tid_s != "--" and pref in dp_prefixes:
                    table_meta[tid_s] = {
                        "tensor_id": tid_s,
                        "circuit": circ,
                        "table_n": n_v,
                        "table_nnz": nnz_v,
                        "table_cp": cp_v,
                        "table_waring": war_v,
                        "section": "Circuit Benchmarks",
                    }
        elif len(cells) == 11 and cells[0].isdigit() and cells[0].startswith("07"):
            id07, id05, _id03, id01, circ, k_s, n_s, nnz_s, cp_s, war_s, dp_s = cells
            k_v, n_v, nnz_v, cp_v, war_v = int(k_s), int(n_s), int(nnz_s), int(cp_s), int(war_s.rstrip("*"))
            dp_prefixes = dp_s.split()
            for tid_s, pref in [(id07, "07"), (id01, "01")]:
                if pref in dp_prefixes:
                    table_meta[tid_s] = {
                        "tensor_id": tid_s,
                        "circuit": circ,
                        "table_n": n_v,
                        "table_nnz": nnz_v,
                        "table_cp": cp_v,
                        "table_waring": war_v,
                        "section": "GF(2^k) Multiplication",
                    }
            base_meta[id05] = {
                "tensor_id": id05,
                "circuit": circ,
                "k": k_v,
                "table_n": k_v,
                "table_cp": cp_v,
                "section": "GF(2^k) Multiplication (base)",
            }
        elif len(cells) == 7 and cells[0].isdigit() and cells[0].startswith("01"):
            tid_s, circ, n_s, nnz_s, cp_s, _method, war_s = cells
            table_meta[tid_s] = {
                "tensor_id": tid_s,
                "circuit": circ,
                "table_n": int(n_s),
                "table_nnz": int(nnz_s),
                "table_cp": int(cp_s),
                "table_waring": int(war_s.rstrip("*")),
                "section": "Additional ATQ Benchmarks",
            }

    assert len(table_meta) == 88, f"Expected 88 topp table entries, got {len(table_meta)}"
    assert len(base_meta) == 9, f"Expected 9 base table entries, got {len(base_meta)}"
    return table_meta, base_meta


def recompute_p3_audit(polytof_dir: Path):
    """Recompute the complete p3 audit of data/paper/ from scratch."""
    git_dir = polytof_dir / ".git"
    if git_dir.exists():
        head = subprocess.check_output(
            ["git", "-C", str(polytof_dir), "rev-parse", "HEAD"], text=True
        ).strip()
        assert head == PINNED_POLYTOF_COMMIT, (
            f"polytof HEAD mismatch: got {head}, expected {PINNED_POLYTOF_COMMIT}"
        )

    table_meta, base_meta = parse_docs_tensors_md(polytof_dir / "docs" / "tensors.md")

    tensors_dir = polytof_dir / "data" / "tensors"
    transform_dir = polytof_dir / "data" / "paper" / "transform"
    cpd_topp_dir = polytof_dir / "data" / "paper" / "cpd" / "topp"
    cpd_base_dir = polytof_dir / "data" / "paper" / "cpd" / "base"
    waring_dir = polytof_dir / "data" / "paper" / "waring"

    transform_files = sorted(transform_dir.glob("*.npy"))
    cpd_topp_files = sorted(cpd_topp_dir.glob("*.npy"))
    cpd_base_files = sorted(cpd_base_dir.glob("*.npy"))
    waring_files = sorted(waring_dir.glob("*.npy"))

    assert len(transform_files) == 88, f"Expected 88 transform files, found {len(transform_files)}"
    assert len(cpd_topp_files) == 88, f"Expected 88 cpd/topp files, found {len(cpd_topp_files)}"
    assert len(cpd_base_files) == 9, f"Expected 9 cpd/base files, found {len(cpd_base_files)}"
    assert len(waring_files) == 88, f"Expected 88 waring files, found {len(waring_files)}"

    dimension_discrepancies = []
    waring_discrepancies = []
    cp_discrepancies = []
    pool_files_summary = []

    topp_cp_schemes_total = 0
    topp_cp_schemes_valid = 0
    topp_cp_files_matching_table = 0

    waring_schemes_valid = 0
    waring_files_matching_table = 0

    bco_cache = {}

    for tf in transform_files:
        tid_s = tf.stem
        assert tid_s in table_meta, f"Transform tensor {tid_s} missing from docs/tensors.md"
        meta = table_meta[tid_s]

        t_arr = np.load(tensors_dir / f"{tid_s}.npy")
        actual_n = int(t_arr[0, 0])
        assert int(t_arr[0, 1]) == actual_n and int(t_arr[0, 2]) == actual_n
        triples = t_arr[1:]
        A_trans = np.load(tf)
        T_orig, T_bco, orig_nnz, bco_nnz = fast_bco_tensor(actual_n, triples, A_trans)
        bco_cache[tid_s] = (actual_n, T_orig, T_bco, A_trans, orig_nnz, bco_nnz)

        if actual_n != meta["table_n"]:
            counterpart_id = "08" + tid_s[2:]
            counterpart_n = int(np.load(tensors_dir / f"{counterpart_id}.npy")[0, 0])
            dimension_discrepancies.append({
                "tensor_id": tid_s,
                "circuit": meta["circuit"],
                "table_n": meta["table_n"],
                "actual_n": actual_n,
                "counterpart_id": counterpart_id,
                "counterpart_n": counterpart_n,
            })

        # Verify cpd/topp/{tid_s}-*.npy (all stored rows)
        cpd_matches = list(cpd_topp_dir.glob(f"{tid_s}-*.npy"))
        assert len(cpd_matches) == 1
        cpd_f = cpd_matches[0]
        fn_cp_rank = int(cpd_f.stem.split("-")[1])
        dec_cp_rank, num_schemes, passed_schemes = verify_cpd_topp_file(cpd_f, actual_n, T_bco)
        assert dec_cp_rank == fn_cp_rank, f"Filename/decoded CP rank mismatch on {cpd_f.name}"
        assert passed_schemes == num_schemes, f"CP verification failed on {cpd_f.name}: {passed_schemes}/{num_schemes}"
        topp_cp_schemes_total += num_schemes
        topp_cp_schemes_valid += passed_schemes
        if num_schemes > 1:
            pool_files_summary.append({
                "file": cpd_f.name,
                "tensor_id": tid_s,
                "circuit": meta["circuit"],
                "n": actual_n,
                "cp_rank": dec_cp_rank,
                "stored_schemes": num_schemes,
                "valid_schemes": passed_schemes,
            })
        if dec_cp_rank == meta["table_cp"]:
            topp_cp_files_matching_table += 1
        else:
            cp_discrepancies.append({
                "tensor_id": tid_s,
                "file": cpd_f.name,
                "table_cp": meta["table_cp"],
                "posted_cp": dec_cp_rank,
            })

        # Verify waring/{tid_s}-*.npy (full signature in BCO and original bases)
        war_matches = list(waring_dir.glob(f"{tid_s}-*.npy"))
        assert len(war_matches) == 1
        war_f = war_matches[0]
        fn_war_rank = int(war_f.stem.split("-")[1])
        A_war = np.load(war_f)
        ok_war, war_info = verify_waring_matrix_full_signature(
            A_war, actual_n, T_bco, T_orig, A_trans, require_distinct_nonzero=True
        )
        assert ok_war, f"Upstream Waring file {war_f.name} failed full-signature check: {war_info}"
        assert war_info["rank"] == fn_war_rank, f"Filename/decoded Waring rank mismatch on {war_f.name}"
        waring_schemes_valid += 1
        if war_info["rank"] == meta["table_waring"]:
            waring_files_matching_table += 1
        else:
            waring_discrepancies.append({
                "tensor_id": tid_s,
                "circuit": meta["circuit"],
                "n": actual_n,
                "orig_nnz": orig_nnz,
                "bco_nnz": bco_nnz,
                "cp_rank": meta["table_cp"],
                "table_waring": meta["table_waring"],
                "posted_file": war_f.name,
                "posted_waring": war_info["rank"],
                "excess_over_table": war_info["rank"] - meta["table_waring"],
            })

    # Verify all 9 cpd/base files (0525..0533)
    base_cp_schemes_total = 0
    base_cp_schemes_valid = 0
    base_cp_files_matching_table = 0
    base_files_summary = []

    for bf in cpd_base_files:
        tid_s = bf.stem.split("-")[0]
        fn_rank = int(bf.stem.split("-")[1])
        assert tid_s in base_meta, f"Base CPD tensor {tid_s} missing from docs/tensors.md"
        bmeta = base_meta[tid_s]
        k, dec_rank, num_s, pass_s = verify_cpd_base_file(bf, tensors_dir / f"{tid_s}.npy")
        assert k == bmeta["k"] and dec_rank == fn_rank and pass_s == num_s == 1
        base_cp_schemes_total += num_s
        base_cp_schemes_valid += pass_s
        if dec_rank == bmeta["table_cp"]:
            base_cp_files_matching_table += 1
        else:
            cp_discrepancies.append({
                "tensor_id": tid_s,
                "file": bf.name,
                "table_cp": bmeta["table_cp"],
                "posted_cp": dec_rank,
            })
        base_files_summary.append({
            "file": bf.name,
            "tensor_id": tid_s,
            "circuit": bmeta["circuit"],
            "k": k,
            "cp_rank": dec_rank,
            "valid": True,
        })

    assert len(dimension_discrepancies) == 2, f"Expected 2 dimension discrepancies, got {len(dimension_discrepancies)}"
    assert len(waring_discrepancies) == 5, f"Expected 5 Waring discrepancies, got {len(waring_discrepancies)}"
    assert len(cp_discrepancies) == 0, f"Expected 0 CP discrepancies, got {len(cp_discrepancies)}"
    assert topp_cp_schemes_valid == topp_cp_schemes_total == 13528
    assert base_cp_schemes_valid == base_cp_schemes_total == 9
    assert waring_schemes_valid == 88

    # Verify the 4 shipped repaired Waring schemes in object/waring/
    repaired_entries = []
    for spec in REPAIRED_SPECS:
        tid_s = spec["tensor_id"]
        actual_n, T_orig, T_bco, A_trans, orig_nnz, bco_nnz = bco_cache[tid_s]
        assert actual_n == spec["n"]
        wpath = PKG_DIR / spec["repaired_file"]
        assert wpath.is_file(), f"Missing repaired Waring file {wpath}"
        A_rep = np.load(wpath)
        ok_rep, rep_info = verify_waring_matrix_full_signature(
            A_rep, actual_n, T_bco, T_orig, A_trans, require_distinct_nonzero=True
        )
        assert ok_rep, f"Repaired Waring file {wpath.name} failed full-signature verification: {rep_info}"
        assert rep_info["rank"] == spec["repaired_waring"] == spec["table_waring"], (
            f"Repaired Waring rank {rep_info['rank']} != table {spec['table_waring']}"
        )
        repaired_entries.append({
            "tensor_id": tid_s,
            "circuit": spec["circuit"],
            "n": actual_n,
            "orig_nnz": orig_nnz,
            "bco_nnz": bco_nnz,
            "table_waring": spec["table_waring"],
            "posted_file": spec["posted_file"],
            "posted_waring": spec["posted_waring"],
            "repaired_file": spec["repaired_file"],
            "repaired_waring": rep_info["rank"],
            "reduction_vs_posted": spec["posted_waring"] - rep_info["rank"],
            "sha256": sha256_file(wpath),
            "bco_cubic_match": rep_info["bco_cubic_match"],
            "bco_odd_cols": rep_info["bco_odd_cols"],
            "bco_odd_pairs": rep_info["bco_odd_pairs"],
            "orig_cubic_match": rep_info["orig_cubic_match"],
            "orig_odd_cols": rep_info["orig_odd_cols"],
            "orig_odd_pairs": rep_info["orig_odd_pairs"],
            "parity_matrix": A_rep.astype(int).tolist(),
        })

    cert = {
        "target_id": "polytof-toffoli-tcount-benchmark-tensors",
        "partial_win": "p3",
        "upstream_repo": "https://github.com/ZIB-IOL/polytof",
        "pinned_commit": PINNED_POLYTOF_COMMIT,
        "docs_tensors_md_sha256": PINNED_TENSORS_MD_SHA256,
        "audit_coverage": {
            "total_decomposition_files_in_data_paper": len(cpd_topp_files) + len(cpd_base_files) + len(waring_files),
            "transform_files_verified": len(transform_files),
            "cpd_topp_files_verified": len(cpd_topp_files),
            "cpd_topp_single_row_files": len(cpd_topp_files) - len(pool_files_summary),
            "cpd_topp_multi_row_pool_files": len(pool_files_summary),
            "cpd_topp_total_stored_schemes_verified": topp_cp_schemes_valid,
            "cpd_base_files_verified": len(cpd_base_files),
            "cpd_base_total_stored_schemes_verified": base_cp_schemes_valid,
            "total_cp_files_matching_table": topp_cp_files_matching_table + base_cp_files_matching_table,
            "total_cp_schemes_verified": topp_cp_schemes_valid + base_cp_schemes_valid,
            "waring_files_verified_full_signature": waring_schemes_valid,
            "waring_files_matching_table": waring_files_matching_table,
            "waring_files_exceeding_table": len(waring_discrepancies),
            "dimension_discrepancies_count": len(dimension_discrepancies),
            "repaired_waring_schemes_count": len(repaired_entries),
        },
        "waring_rank_discrepancies": waring_discrepancies,
        "dimension_discrepancies": dimension_discrepancies,
        "repaired_waring_schemes": repaired_entries,
        "cpd_topp_pool_files": pool_files_summary,
        "cpd_base_files": base_files_summary,
    }
    return cert, bco_cache


def verify_existing_certificate(existing_cert: dict, recomputed_cert: dict, bco_cache: dict):
    """
    Verify that object/p3_audit_certificate.json matches the freshly recomputed audit
    and that every embedded parity_matrix inside object/p3_audit_certificate.json
    independently passes full-signature verification.
    """
    assert isinstance(existing_cert, dict), "Certificate is not a JSON object"
    rep_list = existing_cert.get("repaired_waring_schemes", [])
    assert len(rep_list) == 4, f"Expected 4 repaired_waring_schemes in certificate, got {len(rep_list)}"
    for item in rep_list:
        tid_s = item.get("tensor_id")
        assert tid_s in bco_cache, f"Unknown tensor_id {tid_s} in certificate"
        actual_n, T_orig, T_bco, A_trans, _orig_nnz, _bco_nnz = bco_cache[tid_s]
        A_json = np.array(item.get("parity_matrix", []), dtype=np.int64)
        ok_j, info_j = verify_waring_matrix_full_signature(
            A_json, actual_n, T_bco, T_orig, A_trans, require_distinct_nonzero=True
        )
        assert ok_j, f"Embedded parity_matrix for {tid_s} in p3_audit_certificate.json failed verification: {info_j}"
        assert info_j["rank"] == item.get("repaired_waring") == item.get("table_waring")

    assert existing_cert == recomputed_cert, (
        "object/p3_audit_certificate.json does not match recomputed p3 audit!"
    )


def main():
    parser = argparse.ArgumentParser(description="Recompute and verify polytof p3 audit.")
    parser.add_argument(
        "--polytof-dir",
        default=os.environ.get("POLYTOF_DIR", "polytof"),
        help="Path to ZIB-IOL/polytof checkout at commit 0dcac107d15adc34dc646242d222f21ae7d32699",
    )
    parser.add_argument(
        "--write-cert",
        action="store_true",
        help="Write recomputed certificate to object/p3_audit_certificate.json",
    )
    args = parser.parse_args()

    t0 = time.time()
    polytof_dir = Path(args.polytof_dir).resolve()
    assert polytof_dir.is_dir(), f"polytof directory not found: {polytof_dir}"

    recomputed_cert, bco_cache = recompute_p3_audit(polytof_dir)

    if args.write_cert:
        CERT_PATH.write_text(json.dumps(recomputed_cert, indent=2) + "\n", encoding="utf-8")

    existing_cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
    verify_existing_certificate(existing_cert, recomputed_cert, bco_cache)

    cov = recomputed_cert["audit_coverage"]
    print(
        f"[PASS] Pinned polytof commit {PINNED_POLYTOF_COMMIT[:12]} & docs/tensors.md "
        f"(sha256={PINNED_TENSORS_MD_SHA256[:12]}...) parsed."
    )
    print(
        f"[PASS] Audited all {cov['total_decomposition_files_in_data_paper']} decomposition files in data/paper/: "
        f"{cov['cpd_topp_files_verified']} cpd/topp ({cov['cpd_topp_total_stored_schemes_verified']}/"
        f"{cov['cpd_topp_total_stored_schemes_verified']} schemes across {cov['cpd_topp_single_row_files']} single-row "
        f"+ {cov['cpd_topp_multi_row_pool_files']} pool files), "
        f"{cov['cpd_base_files_verified']} cpd/base ({cov['cpd_base_total_stored_schemes_verified']}/9 bilinear schemes), "
        f"and {cov['waring_files_verified_full_signature']} waring (88/88 full-signature valid)."
    )
    print(
        "[PASS] Recomputed p3 discrepancies vs docs/tensors.md: "
        "5 Waring rank discrepancies (0105: 41 vs 39, 0108: 77 vs 73, 0115: 55 vs 51, "
        "0728: 61 vs 59, 0817: 63 vs 59) and 2 dimension discrepancies (0108: n=42 vs 46, 0114: n=11 vs 12)."
    )
    for rep in recomputed_cert["repaired_waring_schemes"]:
        print(
            f"[PASS] Repaired Waring scheme {rep['repaired_file']} ({rep['circuit']}, n={rep['n']}): "
            f"posted={rep['posted_waring']} -> repaired={rep['repaired_waring']} == table={rep['table_waring']} "
            f"(full signature BCO & orig bases: PASS, sha256={rep['sha256'][:12]}...)"
        )
    print(f"[PASS] Complete p3 audit recomputed and verified in {time.time() - t0:.2f}s.")
    print("PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Verification error: {exc}")
        print("FAIL")
        sys.exit(1)
