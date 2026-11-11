#!/usr/bin/env python3
"""
Standalone First-Principles Exact Verifier for hadamard-maxdet-records
(Orders n = 81, 89, 93, 97, 101, 105, 109, 117).

Requirements: Python 3.8+ standard library only (zero external packages required).
If `sympy` is installed, automatically adds a third independent determinant check via
`sympy.Matrix(mat).det(method="bareiss")`.

Checks performed for every order n in {81, 89, 93, 97, 101, 105, 109, 117}:
  1. Exact schema, key-set, and SHA-256 integrity of `object/hadamard_maxdet_8_records.json`,
     `object/M081.txt` .. `object/M117.txt`, and `INDEX.csv`.
  2. Exact entry check (`X[i][j] in {-1, +1}` and shape `n x n`) and byte-for-byte agreement
     between `object/M<nnn>.txt`, `record["matrix_rows"]`, and algebraic reconstruction from
     `record["generator_params"]` (including exact Hadamard orthogonality `H * H^T = m * I_m`
     of every underlying order-(n-1) Hadamard core).
  3. Exact determinant computation by TWO independent standard-library integer algorithms:
       (a) Fraction-free Bareiss elimination over arbitrary-precision Python `int`,
       (b) 14-prime 61-bit modular Gaussian elimination + Chinese Remainder Theorem (CRT),
     plus optional `sympy.Matrix.det(method="bareiss")` cross-check when SymPy is available.
  4. Exact divisibility by `2^(n-1)`, exact equality with `D_norm` and `factored_D_norm`,
     strict improvement over BOTH academic literature records (Farmakis-Kounias 1987,
     Orrick-Solomon 2003/2007, Rokicki 2005) AND prior merged/open V3R1T4S claims
     (merged PR #155 on n = 109; open PRs #539, #540, #541 on n = 105, 109, 117),
     and strict satisfaction of Barba's (1933) upper bound `|det(X)|^2 < (2n - 1)*(n - 1)^(n - 1)`.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import sys
from decimal import Decimal, getcontext
from pathlib import Path
from typing import Dict, List, Tuple

sys.dont_write_bytecode = True
getcontext().prec = 140

try:
    import sympy as _sp  # type: ignore
    HAS_SYMPY = True
except Exception:
    HAS_SYMPY = False

EXPECTED_ORDERS = [81, 89, 93, 97, 101, 105, 109, 117]

# Exact academic literature baselines D_norm = |det(X)| / 2^(n-1)
# Sources: Farmakis & Kounias 1987 (81, 89); Orrick & Solomon 2003/2007 (93, 97, 101); Rokicki 2005 (105, 109, 117).
LITERATURE_BASELINE_D_NORM: Dict[int, int] = {
    81: 196 * (20 ** 39),
    89: 220 * (22 ** 43),
    93: 239 * (23 ** 45),
    97: 256 * (24 ** 47),
    101: 7110 * (25 ** 48),
    105: 384743747284587846942188483608583600735563257274079045682562818122226665625,
    109: 1877483841834222713683125485573890072927341503771574105042244268774869908324352,
    117: 72314994254613394470813334860641212637154205430658679584420251275641935854599391452615,
}

# Prior merged V3R1T4S main-branch record (PR #155, merged 2026-10-15: 291 * 27^53 on n = 109)
V3R1T4S_MERGED_D_NORM: Dict[int, int] = {
    109: 291 * (27 ** 53),
}

# Unmerged open V3R1T4S PR claims checked as extra margin (PR #539 on 105, PR #540 on 109, PR #541 on 117)
V3R1T4S_OPEN_PR_D_NORM: Dict[int, int] = {
    105: 277 * (26 ** 51),
    109: 297 * (27 ** 53),
    117: 325 * (29 ** 57),
}

# 14 distinct 61-bit primes for independent modular Gaussian elimination + CRT.
# Their product exceeds 2^840 > 10^252, vastly larger than 2 * 117^(117/2) ~ 10^121.
CRT_PRIMES: Tuple[int, ...] = (
    2305843009213693951,  # 2^61 - 1 (Mersenne prime)
    2305843009213693921,
    2305843009213693907,
    2305843009213693723,
    2305843009213693693,
    2305843009213693669,
    2305843009213693613,
    2305843009213693561,
    2305843009213693549,
    2305843009213693487,
    2305843009213693421,
    2305843009213693373,
    2305843009213693277,
    2305843009213693193,
)

TOP_KEYS = {"schema_version", "record_count", "orders_improved", "records"}
RECORD_KEYS = {
    "n",
    "residue_mod_4",
    "D_norm",
    "det_exact",
    "factored_D_norm",
    "previous_literature_D_norm",
    "previous_v3r1t4s_merged_D_norm",
    "matrix_file",
    "matrix_file_sha256",
    "matrix_rows",
    "generator_params",
}


class VerificationError(Exception):
    pass


def require(cond: bool, msg: str) -> None:
    if not cond:
        raise VerificationError(msg)


def parse_sign_rows(rows: List[str], expected_n: int) -> List[List[int]]:
    require(isinstance(rows, list) and len(rows) == expected_n, f"Expected {expected_n} rows, got {len(rows) if isinstance(rows, list) else type(rows)}")
    mat: List[List[int]] = []
    for r_idx, row in enumerate(rows):
        require(isinstance(row, str) and len(row) == expected_n, f"Row {r_idx} does not have exact length {expected_n}")
        prow: List[int] = []
        for c_idx, ch in enumerate(row):
            if ch == "+":
                prow.append(1)
            elif ch == "-":
                prow.append(-1)
            else:
                raise VerificationError(f"Invalid sign character {ch!r} at ({r_idx}, {c_idx})")
        mat.append(prow)
    return mat


def mat_to_rows(mat: List[List[int]]) -> List[str]:
    out: List[str] = []
    for r in mat:
        out.append("".join("+" if v == 1 else "-" for v in r))
    return out


def verify_hadamard_core(H: List[List[int]], m: int) -> None:
    require(len(H) == m and all(len(r) == m for r in H), f"Hadamard core shape != {m}x{m}")
    for i in range(m):
        for v in H[i]:
            require(v in (-1, 1), "Hadamard core entry outside {-1, +1}")
        for j in range(i, m):
            dot = sum(H[i][c] * H[j][c] for c in range(m))
            expected = m if i == j else 0
            require(dot == expected, f"Hadamard orthogonality failed at ({i}, {j}): dot={dot}, expected={expected}")


def unpack_hex_matrix(hex_rows: List[str], expected_m: int) -> List[List[int]]:
    require(isinstance(hex_rows, list) and len(hex_rows) == expected_m, f"core_hex length != {expected_m}")
    expected_hex_len = (expected_m + 3) // 4
    out: List[List[int]] = []
    for idx, s in enumerate(hex_rows):
        require(isinstance(s, str) and ":" in s, f"Malformed core_hex row {idx}")
        ln_s, hx = s.split(":", 1)
        require(ln_s.isdigit() and int(ln_s) == expected_m, f"core_hex row {idx} prefix {ln_s} != {expected_m}")
        require(len(hx) == expected_hex_len and all(c in "0123456789abcdef" for c in hx), f"Invalid hex payload at row {idx}")
        bits_full = "".join(f"{int(ch, 16):04b}" for ch in hx)
        # Ensure any trailing padding bits beyond expected_m are strictly '0'
        require(all(b == "0" for b in bits_full[expected_m:]), f"Non-zero trailing pad bits in core_hex row {idx}")
        bits = bits_full[:expected_m]
        out.append([1 if b == "1" else -1 for b in bits])
    return out


def build_gs_from_4vecs(vA_s: str, vB_s: str, vC_s: str, vD_s: str, negacyclic: bool) -> List[List[int]]:
    require(not negacyclic, "Expected circulant Goethals-Seidel blocks (negacyclic=False)")
    k = len(vA_s)
    require(k > 0 and all(len(s) == k for s in (vA_s, vB_s, vC_s, vD_s)), "Mismatched GS generator lengths")
    vecs: List[List[int]] = []
    for s in (vA_s, vB_s, vC_s, vD_s):
        require(all(ch in "+-" for ch in s), "Invalid sign character in GS generator")
        vecs.append([1 if ch == "+" else -1 for ch in s])

    def circ(v: List[int]) -> List[List[int]]:
        # numpy.roll(v, r): row r has entry j equal to v[(j - r) % k]
        return [[v[(j - r) % k] for j in range(k)] for r in range(k)]

    def mat_T(M: List[List[int]]) -> List[List[int]]:
        return [[M[r][c] for r in range(k)] for c in range(k)]

    def mul_R(M: List[List[int]]) -> List[List[int]]:
        # Right-multiply by back-identity R_rev: reverses each row
        return [list(reversed(row)) for row in M]

    def neg(M: List[List[int]]) -> List[List[int]]:
        return [[-x for x in row] for row in M]

    A0, B, C, D = [circ(v) for v in vecs]
    BR, CR, DR = mul_R(B), mul_R(C), mul_R(D)
    BtR, CtR, DtR = mul_R(mat_T(B)), mul_R(mat_T(C)), mul_R(mat_T(D))

    blocks = [
        [A0, BR, CR, DR],
        [neg(BR), A0, neg(DtR), CtR],
        [neg(CR), DtR, A0, neg(BtR)],
        [neg(DR), neg(CtR), BtR, A0],
    ]
    H: List[List[int]] = []
    for brow in blocks:
        for r in range(k):
            H.append(brow[0][r] + brow[1][r] + brow[2][r] + brow[3][r])
    return H


def build_os1_std(H: List[List[int]], r1: int, r2: int, r3: int) -> List[List[int]]:
    m = len(H)
    require(0 <= r1 < r2 < r3 < m, f"Invalid OS-1 triplet ({r1}, {r2}, {r3})")
    w = [H[r1][j] * H[r2][j] * H[r3][j] for j in range(m)]
    Hw = [[H[i][j] * w[j] for j in range(m)] for i in range(m)]
    patterns = [(1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)]
    B = [[-1] * m for _ in range(4)]
    for a, pat in enumerate(patterns):
        for j in range(m):
            if (Hw[r1][j], Hw[r2][j], Hw[r3][j]) == pat:
                B[a][j] = 1
    rem_idx = [i for i in range(m) if i not in (r1, r2, r3)]
    H_rem: List[List[int]] = []
    for idx in rem_idx:
        row = Hw[idx][:]
        dot = sum(B[0][j] * row[j] for j in range(m))
        if dot > 0:
            row = [-x for x in row]
        H_rem.append(row)
    M: List[List[int]] = []
    for a in range(4):
        M.append([-1] + B[a])
    for row in H_rem:
        M.append([-1] + row)
    return M


def build_os2_std(H: List[List[int]], r_trip: List[int], c_trip: List[int], eps_sign: str) -> List[List[int]]:
    m = len(H)
    require(len(r_trip) == 3 and len(c_trip) == 3, "Invalid OS-2 triplets")
    r0, r1, r2 = int(r_trip[0]), int(r_trip[1]), int(r_trip[2])
    c0, c1, c2 = int(c_trip[0]), int(c_trip[1]), int(c_trip[2])
    require(0 <= r0 < r1 < r2 < m and 0 <= c0 < c1 < c2 < m, "Out-of-range OS-2 triplet")
    require(eps_sign in ("+1", "-1"), f"Invalid eps_sign {eps_sign!r}")
    eps = 1 if eps_sign == "+1" else -1

    row_order = [r0, r1, r2] + [r for r in range(m) if r not in (r0, r1, r2)]
    col_order = [c0, c1, c2] + [c for c in range(m) if c not in (c0, c1, c2)]
    Hp = [[H[r][c] for c in col_order] for r in row_order]

    m3 = m - 3
    s_col = [Hp[0][3 + j] * Hp[1][3 + j] * Hp[2][3 + j] for j in range(m3)]
    tau_row = [Hp[3 + i][0] * Hp[3 + i][1] * Hp[3 + i][2] for i in range(m3)]

    R_top = [[Hp[a][3 + j] * s_col[j] for j in range(m3)] for a in range(3)]
    C_left = [[Hp[3 + i][b] * tau_row[i] for b in range(3)] for i in range(m3)]
    H_rem = [[tau_row[i] * Hp[3 + i][3 + j] * s_col[j] * eps for j in range(m3)] for i in range(m3)]

    a, b, c = R_top[0], R_top[1], R_top[2]
    B_top = [
        [(-a[j] - b[j] - c[j] + 1) // 2 for j in range(m3)],
        [(-a[j] + b[j] + c[j] + 1) // 2 for j in range(m3)],
        [(a[j] - b[j] + c[j] + 1) // 2 for j in range(m3)],
        [(a[j] + b[j] - c[j] + 1) // 2 for j in range(m3)],
    ]
    B_left = []
    for i in range(m3):
        al, bl, cl = C_left[i][0], C_left[i][1], C_left[i][2]
        B_left.append([
            (-al - bl - cl + 1) // 2,
            (-al + bl + cl + 1) // 2,
            (al - bl + cl + 1) // 2,
            (al + bl - cl + 1) // 2,
        ])
    C4 = [
        [1, -1, -1, -1],
        [-1, -1, -1, -1],
        [-1, -1, -1, -1],
        [-1, -1, -1, -1],
    ]
    M: List[List[int]] = []
    for r in range(4):
        M.append(C4[r] + B_top[r])
    for i in range(m3):
        M.append(B_left[i] + H_rem[i])
    return M


def apply_flips(M: List[List[int]], n: int, flipped_rows: List[int], flipped_cols: List[int], sparse_flips: List[List[int]]) -> None:
    require(isinstance(flipped_rows, list) and flipped_rows == sorted(set(flipped_rows)), "Invalid flipped_rows list")
    require(isinstance(flipped_cols, list) and flipped_cols == sorted(set(flipped_cols)), "Invalid flipped_cols list")
    for r in flipped_rows:
        require(isinstance(r, int) and 0 <= r < n, f"Invalid flipped row index {r}")
        for c in range(n):
            M[r][c] = -M[r][c]
    for c in flipped_cols:
        require(isinstance(c, int) and 0 <= c < n, f"Invalid flipped col index {c}")
        for r in range(n):
            M[r][c] = -M[r][c]
    seen_pairs = set()
    for pair in sparse_flips:
        require(isinstance(pair, list) and len(pair) == 2, f"Invalid sparse_flip entry {pair!r}")
        r, c = pair[0], pair[1]
        require(isinstance(r, int) and isinstance(c, int) and 0 <= r < n and 0 <= c < n, f"Out-of-range sparse flip ({r}, {c})")
        require((r, c) not in seen_pairs, f"Duplicate sparse flip ({r}, {c})")
        seen_pairs.add((r, c))
        M[r][c] = -M[r][c]


def reconstruct_and_check_params(n: int, gp: dict) -> List[str]:
    require(isinstance(gp, dict) and "kind" in gp, f"n={n}: missing generator_params.kind")
    kind = gp["kind"]
    m = n - 1
    if kind == "gs_os1":
        expected_keys = {"kind", "k", "negacyclic", "vA", "vB", "vC", "vD", "row_sums", "triplet", "flipped_rows", "flipped_cols", "sparse_flips"}
        require(set(gp.keys()) == expected_keys, f"n={n}: unexpected keys in gs_os1 generator_params: {set(gp.keys()) ^ expected_keys}")
        require(gp["k"] * 4 == m, f"n={n}: 4*k != n-1")
        H = build_gs_from_4vecs(gp["vA"], gp["vB"], gp["vC"], gp["vD"], bool(gp["negacyclic"]))
        actual_sums = [sum(1 if ch == "+" else -1 for ch in gp[key]) for key in ("vA", "vB", "vC", "vD")]
        require(gp["row_sums"] == actual_sums, f"n={n}: row_sums mismatch ({gp['row_sums']} != {actual_sums})")
        verify_hadamard_core(H, m)
        trip = gp["triplet"]
        require(isinstance(trip, list) and len(trip) == 3, f"n={n}: invalid triplet")
        M = build_os1_std(H, int(trip[0]), int(trip[1]), int(trip[2]))
        apply_flips(M, n, gp["flipped_rows"], gp["flipped_cols"], gp["sparse_flips"])
        return mat_to_rows(M)
    if kind == "hadamard_core_os1":
        expected_keys = {"kind", "core_order", "core_hex", "triplet", "flipped_rows", "flipped_cols", "sparse_flips"}
        require(set(gp.keys()) == expected_keys, f"n={n}: unexpected keys in hadamard_core_os1: {set(gp.keys()) ^ expected_keys}")
        require(gp["core_order"] == m, f"n={n}: core_order != {m}")
        H = unpack_hex_matrix(gp["core_hex"], m)
        verify_hadamard_core(H, m)
        trip = gp["triplet"]
        require(isinstance(trip, list) and len(trip) == 3, f"n={n}: invalid triplet")
        M = build_os1_std(H, int(trip[0]), int(trip[1]), int(trip[2]))
        apply_flips(M, n, gp["flipped_rows"], gp["flipped_cols"], gp["sparse_flips"])
        return mat_to_rows(M)
    if kind == "hadamard_core_os2":
        expected_keys = {"kind", "core_order", "core_hex", "row_triplet", "col_triplet", "eps_sign", "flipped_rows", "flipped_cols", "sparse_flips"}
        require(set(gp.keys()) == expected_keys, f"n={n}: unexpected keys in hadamard_core_os2: {set(gp.keys()) ^ expected_keys}")
        require(gp["core_order"] == m, f"n={n}: core_order != {m}")
        H = unpack_hex_matrix(gp["core_hex"], m)
        verify_hadamard_core(H, m)
        M = build_os2_std(H, gp["row_triplet"], gp["col_triplet"], gp["eps_sign"])
        apply_flips(M, n, gp["flipped_rows"], gp["flipped_cols"], gp["sparse_flips"])
        return mat_to_rows(M)
    raise VerificationError(f"n={n}: unsupported generator_params.kind {kind!r}")


def det_bareiss_int(mat: List[List[int]]) -> int:
    n = len(mat)
    a = [row[:] for row in mat]
    sign = 1
    prev_pivot = 1
    for k in range(n - 1):
        if a[k][k] == 0:
            swap_row = -1
            for i in range(k + 1, n):
                if a[i][k] != 0:
                    swap_row = i
                    break
            if swap_row == -1:
                return 0
            a[k], a[swap_row] = a[swap_row], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            row_i = a[i]
            row_k = a[k]
            rik = row_i[k]
            if rik == 0:
                for j in range(k + 1, n):
                    row_i[j] = (pivot * row_i[j]) // prev_pivot
            else:
                for j in range(k + 1, n):
                    row_i[j] = (pivot * row_i[j] - rik * row_k[j]) // prev_pivot
            row_i[k] = 0
        prev_pivot = pivot
    return sign * a[n - 1][n - 1]


def det_mod_prime(mat: List[List[int]], p: int) -> int:
    n = len(mat)
    a = [[x % p for x in row] for row in mat]
    det = 1
    for k in range(n):
        piv = k
        while piv < n and a[piv][k] == 0:
            piv += 1
        if piv == n:
            return 0
        if piv != k:
            a[k], a[piv] = a[piv], a[k]
            det = (p - det) % p
        akk = a[k][k]
        det = (det * akk) % p
        inv = pow(akk, p - 2, p)
        row_k = a[k]
        for i in range(k + 1, n):
            rik = a[i][k]
            if rik:
                fac = (rik * inv) % p
                row_i = a[i]
                for j in range(k + 1, n):
                    row_i[j] = (row_i[j] - fac * row_k[j]) % p
    return det


def det_crt_int(mat: List[List[int]]) -> int:
    mod_prod = 1
    residue = 0
    for p in CRT_PRIMES:
        r_p = det_mod_prime(mat, p)
        if mod_prod == 1:
            residue = r_p
            mod_prod = p
        else:
            inv = pow(mod_prod % p, p - 2, p)
            k = ((r_p - residue) % p) * inv % p
            residue += mod_prod * k
            mod_prod *= p
    if residue > mod_prod // 2:
        residue -= mod_prod
    return residue


def parse_factored_d_norm(expr: str) -> int:
    m = re.fullmatch(r"([1-9][0-9]*)\s*\*\s*([1-9][0-9]*)\^([1-9][0-9]*)", expr)
    require(m is not None, f"Invalid factored_D_norm format: {expr!r}")
    assert m is not None
    return int(m.group(1)) * (int(m.group(2)) ** int(m.group(3)))


def verify_package(pkg_root: Path, run_corrupt_self_test: bool = False) -> None:
    obj_json_path = pkg_root / "object" / "hadamard_maxdet_8_records.json"
    idx_csv_path = pkg_root / "INDEX.csv"
    require(obj_json_path.is_file(), "Missing object/hadamard_maxdet_8_records.json")
    require(idx_csv_path.is_file(), "Missing INDEX.csv")

    try:
        data = json.loads(obj_json_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise VerificationError(f"Invalid JSON in hadamard_maxdet_8_records.json: {exc}") from exc

    require(isinstance(data, dict) and set(data.keys()) == TOP_KEYS, f"Unexpected top-level JSON keys: {set(data.keys()) if isinstance(data, dict) else type(data)}")
    require(data["schema_version"] == "1.0", f"Unexpected schema_version {data['schema_version']!r}")
    require(data["record_count"] == 8, f"Expected record_count == 8, got {data['record_count']!r}")
    require(data["orders_improved"] == EXPECTED_ORDERS, f"orders_improved mismatch: {data['orders_improved']!r}")
    records = data["records"]
    require(isinstance(records, list) and len(records) == 8, "Expected 8 records in JSON")

    with idx_csv_path.open(encoding="utf-8", newline="") as f:
        idx_rows = list(csv.DictReader(f))
    require(len(idx_rows) == 8, f"Expected 8 rows in INDEX.csv, got {len(idx_rows)}")

    if run_corrupt_self_test:
        first_m = pkg_root / "object" / "M081.txt"
        raw_lines = [ln.strip() for ln in first_m.read_text(encoding="utf-8").splitlines() if ln.strip()]
        raw_lines[0] = ("+" if raw_lines[0][0] == "-" else "-") + raw_lines[0][1:]
        mat_bad = parse_sign_rows(raw_lines, 81)
        det_bad = abs(det_bareiss_int(mat_bad))
        d_claimed = int(records[0]["D_norm"])
        if det_bad != d_claimed * (1 << 80):
            raise VerificationError("Adversarial --corrupt mutation properly rejected (determinant mismatch)")
        raise RuntimeError("Adversarial --corrupt mutation was NOT rejected!")

    print(f"=== Verifying 8 Hadamard Maximal Determinant Records (Bareiss + 14-Prime CRT + SymPy={HAS_SYMPY}) ===")

    sympy_queue: List[Tuple[int, List[List[int]], int]] = []

    for idx, (rec, irow) in enumerate(zip(records, idx_rows)):
        require(isinstance(rec, dict) and set(rec.keys()) == RECORD_KEYS, f"Record #{idx} key-set mismatch")
        n = rec["n"]
        require(isinstance(n, int) and n == EXPECTED_ORDERS[idx], f"Record #{idx} order {n!r} != {EXPECTED_ORDERS[idx]}")
        require(rec["residue_mod_4"] == n % 4 and n % 4 == 1, f"n={n}: invalid residue_mod_4")

        rel_mfile = f"object/M{n:03d}.txt"
        require(rec["matrix_file"] == rel_mfile, f"n={n}: matrix_file {rec['matrix_file']!r} != {rel_mfile!r}")
        mpath = pkg_root / rel_mfile
        require(mpath.is_file(), f"n={n}: missing matrix file {rel_mfile}")

        mbytes = mpath.read_bytes()
        actual_sha = hashlib.sha256(mbytes).hexdigest()
        require(rec["matrix_file_sha256"] == actual_sha, f"n={n}: matrix_file_sha256 mismatch in JSON")

        mtext = mbytes.decode("utf-8")
        disk_rows = [ln for ln in mtext.splitlines() if ln]
        require(mtext == "\n".join(disk_rows) + "\n", f"n={n}: matrix file {rel_mfile} has unexpected whitespace/formatting")
        require(disk_rows == rec["matrix_rows"], f"n={n}: {rel_mfile} differs from JSON matrix_rows")

        reconstructed_rows = reconstruct_and_check_params(n, rec["generator_params"])
        require(reconstructed_rows == disk_rows, f"n={n}: generator_params reconstruction differs from {rel_mfile}")

        mat = parse_sign_rows(disk_rows, n)
        det_b = det_bareiss_int(mat)
        det_c = det_crt_int(mat)
        require(det_b == det_c, f"n={n}: Bareiss det ({det_b}) != 14-prime CRT det ({det_c})")
        sympy_queue.append((n, mat, det_b))

        det_abs = abs(det_b)
        require(isinstance(rec["det_exact"], str) and rec["det_exact"].isdigit(), f"n={n}: invalid det_exact string")
        require(isinstance(rec["D_norm"], str) and rec["D_norm"].isdigit(), f"n={n}: invalid D_norm string")
        require(det_abs == int(rec["det_exact"]), f"n={n}: |det| != det_exact")

        scale = 1 << (n - 1)
        require(det_abs % scale == 0, f"n={n}: |det| is not divisible by 2^(n-1)")
        d_norm = det_abs // scale
        require(d_norm == int(rec["D_norm"]), f"n={n}: D_norm mismatch")
        require(parse_factored_d_norm(rec["factored_D_norm"]) == d_norm, f"n={n}: factored_D_norm != D_norm")

        lit_prev = LITERATURE_BASELINE_D_NORM[n]
        require(rec["previous_literature_D_norm"] == str(lit_prev), f"n={n}: previous_literature_D_norm mismatch")
        require(d_norm > lit_prev, f"n={n}: D_norm ({d_norm}) does not beat literature record ({lit_prev})")

        if n in V3R1T4S_MERGED_D_NORM:
            v3_prev = V3R1T4S_MERGED_D_NORM[n]
            require(rec["previous_v3r1t4s_merged_D_norm"] == str(v3_prev), f"n={n}: previous_v3r1t4s_merged_D_norm mismatch")
            require(d_norm > v3_prev, f"n={n}: D_norm ({d_norm}) does not beat merged V3R1T4S record ({v3_prev})")
            expected_idx_table_val = str(v3_prev)
        else:
            require(rec["previous_v3r1t4s_merged_D_norm"] is None, f"n={n}: expected null previous_v3r1t4s_merged_D_norm")
            expected_idx_table_val = str(lit_prev)

        if n in V3R1T4S_OPEN_PR_D_NORM:
            require(d_norm > V3R1T4S_OPEN_PR_D_NORM[n], f"n={n}: D_norm does not beat open PR value")

        # Exact Barba (1933) bound for n == 1 (mod 4): |det(X)|^2 <= (2n - 1) * (n - 1)^(n - 1)
        barba_sq = (2 * n - 1) * ((n - 1) ** (n - 1))
        require(det_abs * det_abs < barba_sq, f"n={n}: |det|^2 violates Barba upper bound")

        # Verify INDEX.csv row parity
        require(irow["target_id"] == "hadamard-maxdet-records", f"INDEX.csv row {idx}: bad target_id")
        require(irow["cell"] == f"n={n}", f"INDEX.csv row {idx}: bad cell {irow['cell']!r}")
        require(irow["value"] == str(d_norm), f"INDEX.csv row {idx}: value != D_norm")
        require(irow["table_value"] == expected_idx_table_val, f"INDEX.csv row {idx}: table_value mismatch")
        require(irow["file"] == rel_mfile, f"INDEX.csv row {idx}: file mismatch")
        require(irow["sha256"] == actual_sha, f"INDEX.csv row {idx}: sha256 mismatch")

        ratio = Decimal(det_abs) / Decimal(barba_sq).sqrt()
        gain_lit = (Decimal(d_norm - lit_prev) / Decimal(lit_prev)) * Decimal(100)
        extra_v3 = ""
        if n in V3R1T4S_MERGED_D_NORM:
            gain_v3 = (Decimal(d_norm - V3R1T4S_MERGED_D_NORM[n]) / Decimal(V3R1T4S_MERGED_D_NORM[n])) * Decimal(100)
            extra_v3 = f" (+{gain_v3:.4f}% vs V3R1T4S PR #155)"
        print(
            f"  [OK] n={n:>3d} | D_norm = {rec['factored_D_norm']:<14s} | "
            f"+{gain_lit:.4f}% vs lit{extra_v3} | Barba ratio = {ratio:.6f}"
        )

    # Confirm no unexpected extra files sit inside object/
    expected_obj_files = {"hadamard_maxdet_8_records.json"} | {f"M{n:03d}.txt" for n in EXPECTED_ORDERS}
    actual_obj_files = {p.name for p in (pkg_root / "object").iterdir() if p.is_file()}
    require(actual_obj_files == expected_obj_files, f"Unexpected files in object/: {actual_obj_files ^ expected_obj_files}")

    if HAS_SYMPY:
        for n, mat, det_b in sympy_queue:
            det_sp = int(_sp.Matrix(mat).det(method="bareiss"))
            require(det_b == det_sp, f"n={n}: Bareiss det ({det_b}) != SymPy det ({det_sp})")

    print("All 8 matrices, core orthogonality relations, Bareiss + CRT" + (" + SymPy" if HAS_SYMPY else "") + " determinants, and Barba bounds verified.")
    print("PASS")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify 8 Hadamard maximal determinant record matrices.")
    parser.add_argument("--corrupt", action="store_true", help="Run adversarial mutation self-test and exit 1 with FAIL.")
    args = parser.parse_args()
    pkg_root = Path(__file__).resolve().parent.parent
    try:
        verify_package(pkg_root, run_corrupt_self_test=args.corrupt)
    except VerificationError as exc:
        print(f"VERIFICATION ERROR: {exc}")
        print("FAIL")
        sys.exit(1)
    except Exception as exc:
        print(f"UNEXPECTED ERROR: {exc}")
        print("FAIL")
        sys.exit(1)


if __name__ == "__main__":
    main()
