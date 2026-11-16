#!/usr/bin/env python3
"""Standalone exact GF(2) verifier for Bivariate Bicycle quantum LDPC logical operators.

Follows target.md verification protocol:
1. Builds 0/1 block-circulant check matrices H_X = [A | B] and H_Z = [B^T | A^T] on Z_l x Z_m.
2. Verifies H_X * H_Z^T == 0 (mod 2) and k = n - rank(H_X) - rank(H_Z) == expected_k.
3. Parses strictly increasing qubit support indices from the witness file (0 <= q_0 < ... < q_{w-1} < n).
4. Verifies H_X * u == 0 (mod 2), rank([H_Z; u]) == rank(H_Z) + 1 (nontrivial logical outside stabilizer
   row space), wt(u) <= max_weight, and invariance under row-convention coordinate inversion.
Python 3.9+ standard library only.
"""

import argparse
import json
import re
import sys


def parse_poly_terms(poly_str: str, l: int, m: int):
    terms = []
    for raw_t in poly_str.replace(" ", "").split("+"):
        if not raw_t:
            continue
        if raw_t == "1":
            dx, dy = 0, 0
        else:
            mx = re.search(r"x(?:\^(\d+))?", raw_t)
            my = re.search(r"y(?:\^(\d+))?", raw_t)
            if not mx and not my:
                raise ValueError(f"Cannot parse monomial: {raw_t}")
            dx = (int(mx.group(1)) if (mx and mx.group(1)) else (1 if mx else 0)) % l
            dy = (int(my.group(1)) if (my and my.group(1)) else (1 if my else 0)) % m
        key = (dx, dy)
        if key in terms:
            terms.remove(key)
        else:
            terms.append(key)
    return terms


def build_bb_matrices(l: int, m: int, terms_a, terms_b, row_convention: bool = False):
    N = l * m
    n = 2 * N

    def idx(x: int, y: int) -> int:
        return ((x % l) * m) + (y % m)

    hx_rows = []
    hz_rows = []
    sgn = 1 if row_convention else -1
    for rx in range(l):
        for ry in range(m):
            hx = 0
            hz = 0
            for dx, dy in terms_a:
                hx ^= 1 << idx(rx + sgn * dx, ry + sgn * dy)
                hz ^= 1 << (N + idx(rx - sgn * dx, ry - sgn * dy))
            for dx, dy in terms_b:
                hx ^= 1 << (N + idx(rx + sgn * dx, ry + sgn * dy))
                hz ^= 1 << idx(rx - sgn * dx, ry - sgn * dy)
            hx_rows.append(hx)
            hz_rows.append(hz)
    return n, N, hx_rows, hz_rows


def gf2_echelon(rows):
    """Return sorted list of (pivot_bit_lsb, row_mask) in row-echelon form over GF(2)."""
    basis = []  # list of (piv, mask)
    for r in rows:
        v = r
        for piv, bmask in basis:
            if (v >> piv) & 1:
                v ^= bmask
        if v != 0:
            lsb = (v & -v).bit_length() - 1
            basis.append((lsb, v))
    return basis


def gf2_in_span(basis, vec: int) -> bool:
    v = vec
    for piv, bmask in basis:
        if (v >> piv) & 1:
            v ^= bmask
    return v == 0


def parse_support_file(path: str, n: int):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read().strip()
    if not raw:
        raise ValueError("Empty witness file")
    toks = raw.split()
    qs = []
    for t in toks:
        if not t.isdigit():
            raise ValueError(f"Non-integer token in witness file: {t}")
        q = int(t)
        if q < 0 or q >= n:
            raise ValueError(f"Qubit index {q} out of range [0, {n - 1}]")
        qs.append(q)
    for i in range(len(qs) - 1):
        if qs[i] >= qs[i + 1]:
            raise ValueError(f"Support indices not strictly increasing at {qs[i]} >= {qs[i + 1]}")
    mask = 0
    for q in qs:
        mask |= 1 << q
    return qs, mask


def verify_witness(path: str, l: int, m: int, poly_a: str, poly_b: str, expected_k: int, max_weight: int):
    terms_a = parse_poly_terms(poly_a, l, m)
    terms_b = parse_poly_terms(poly_b, l, m)
    n, N, hx_rows, hz_rows = build_bb_matrices(l, m, terms_a, terms_b, row_convention=False)

    # 1. Check CSS commutation H_X * H_Z^T == 0 mod 2
    for rx in hx_rows:
        for rz in hz_rows:
            if (bin(rx & rz).count("1") & 1) != 0:
                return False, "CSS commutation H_X * H_Z^T != 0", {}

    # 2. Check ranks and k
    ech_hx = gf2_echelon(hx_rows)
    ech_hz = gf2_echelon(hz_rows)
    rank_hx = len(ech_hx)
    rank_hz = len(ech_hz)
    k = n - rank_hx - rank_hz
    if k != expected_k:
        return False, f"Dimension mismatch: got k={k}, expected {expected_k}", {}

    # 3. Parse support and check syndrome + rank([H_Z; u]) == rank(H_Z) + 1
    qs, u_mask = parse_support_file(path, n)
    wt = len(qs)
    if bin(u_mask).count("1") != wt:
        return False, "Bitmask weight mismatch", {}

    for i, rx in enumerate(hx_rows):
        if (bin(rx & u_mask).count("1") & 1) != 0:
            return False, f"Nonzero X-syndrome at check {i}", {}

    if gf2_in_span(ech_hz, u_mask):
        return False, "Witness lies in rowspace(H_Z) (trivial stabilizer, not a logical operator)", {}

    # Explicit rank check: rank([H_Z; u]) == rank(H_Z) + 1
    rank_aug = len(gf2_echelon(hz_rows + [u_mask]))
    if rank_aug != rank_hz + 1:
        return False, f"Augmented rank check failed: {rank_aug} != {rank_hz + 1}", {}

    # 4. Also check coordinate-inverted row-convention isomorphism (i, j) -> (-i mod l, -j mod m)
    _, _, hx_r, hz_r = build_bb_matrices(l, m, terms_a, terms_b, row_convention=True)
    u_rev = 0
    for q in qs:
        blk = 0 if q < N else N
        rem = q - blk
        ix, iy = rem // m, rem % m
        rix, riy = (-ix) % l, (-iy) % m
        u_rev |= 1 << (blk + rix * m + riy)
    for rx in hx_r:
        if (bin(rx & u_rev).count("1") & 1) != 0:
            return False, "Row-convention isomorphism syndrome check failed", {}
    if gf2_in_span(gf2_echelon(hz_r), u_rev):
        return False, "Row-convention isomorphism stabilizer check failed", {}

    if max_weight is not None and wt > max_weight:
        return False, f"Weight {wt} exceeds max_weight {max_weight}", {}

    left_wt = sum(1 for q in qs if q < N)
    right_wt = wt - left_wt
    stats = {
        "k": k,
        "l": l,
        "left_weight": left_wt,
        "m": m,
        "n": n,
        "rank_HX": rank_hx,
        "rank_HZ": rank_hz,
        "rank_HZ_aug": rank_aug,
        "right_weight": right_wt,
        "weight": wt,
    }
    return True, "OK", stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("-l", type=int, required=True)
    ap.add_argument("-m", type=int, required=True)
    ap.add_argument("-a", required=True)
    ap.add_argument("-b", required=True)
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--max-weight", type=int, default=None)
    args = ap.parse_args()

    try:
        ok, msg, stats = verify_witness(
            args.path, args.l, args.m, args.a, args.b, args.k, args.max_weight
        )
    except Exception as exc:
        print(f"PARSE_ERROR: {exc}")
        print("FAIL")
        sys.exit(1)

    if not ok:
        print(f"VERIFY_ERROR: {msg}")
        print("FAIL")
        sys.exit(1)

    print(json.dumps(stats, sort_keys=True))
    print("PASS")


if __name__ == "__main__":
    main()
