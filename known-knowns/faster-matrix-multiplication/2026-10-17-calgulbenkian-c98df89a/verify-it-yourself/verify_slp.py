#!/usr/bin/env python3
"""
Standalone symbolic verifier and reduced-addition counter for Fast Matrix Multiplication
straight-line programs (SLPs) in Perminov's addition_reduced_ZT JSON format.

Verifies over Z (exact integer polynomial ring Z[a_{i,j}, b_{j,l}]):
1. Every intermediate fresh variable and output linear form uses only ternary coefficients
   in {-1, 1}, references only strictly prior computed variables (acyclic DAG), and has
   no duplicate variable indices within a single linear form.
2. No sharing occurs across U (A-forms), V (B-forms), and W (product-forms).
3. Symbolically expands all intermediate variables, computes the m bilinear products
   M_r = L_r(A) * R_r(B) as exact bilinear forms over Z, and verifies that the output
   forms in W equal the exact matrix product entries (A * B)_{i,l} over Z (with zero
   error on all n1*n2*n3*n1*n2*n3 bilinear monomials).
4. Counts reduced additions cr under Perminov's exact convention:
   each binary +/- in u_fresh, u, v_fresh, v, w_fresh, w counts 1 addition
   (i.e. len(form) - 1 additions for each non-empty linear form; negation is free).
"""

import json
import sys


def expand_dag(base_dim, fresh_list, out_list, section_name):
    """
    Symbolically expand a linear straight-line program section (U, V, or W) over Z.
    Returns (out_vectors, reduced_additions, fresh_count).
    """
    if not isinstance(fresh_list, list) or not isinstance(out_list, list):
        raise ValueError(f"{section_name}: fresh_list and out_list must be lists")

    vars_vec = []
    for i in range(base_dim):
        v = [0] * base_dim
        v[i] = 1
        vars_vec.append(v)

    reduced_adds = 0
    for f_idx, form in enumerate(fresh_list):
        if not isinstance(form, list) or len(form) < 1:
            raise ValueError(f"{section_name}_fresh[{f_idx}]: empty or invalid form")
        reduced_adds += len(form) - 1
        v = [0] * base_dim
        seen = set()
        for term in form:
            idx = term.get("index")
            val = term.get("value")
            if not isinstance(idx, int) or not isinstance(val, int):
                raise ValueError(f"{section_name}_fresh[{f_idx}]: non-integer index/value")
            if val not in (-1, 1):
                raise ValueError(f"{section_name}_fresh[{f_idx}]: non-ternary coefficient {val}")
            if not (0 <= idx < len(vars_vec)):
                raise ValueError(
                    f"{section_name}_fresh[{f_idx}]: index {idx} out of bounds (max {len(vars_vec)-1})"
                )
            if idx in seen:
                raise ValueError(f"{section_name}_fresh[{f_idx}]: duplicate index {idx}")
            seen.add(idx)
            src = vars_vec[idx]
            for j in range(base_dim):
                v[j] += val * src[j]
        vars_vec.append(v)

    out_vecs = []
    for o_idx, form in enumerate(out_list):
        if not isinstance(form, list) or len(form) < 1:
            raise ValueError(f"{section_name}[{o_idx}]: empty or invalid form")
        reduced_adds += len(form) - 1
        v = [0] * base_dim
        seen = set()
        for term in form:
            idx = term.get("index")
            val = term.get("value")
            if not isinstance(idx, int) or not isinstance(val, int):
                raise ValueError(f"{section_name}[{o_idx}]: non-integer index/value")
            if val not in (-1, 1):
                raise ValueError(f"{section_name}[{o_idx}]: non-ternary coefficient {val}")
            if not (0 <= idx < len(vars_vec)):
                raise ValueError(
                    f"{section_name}[{o_idx}]: index {idx} out of bounds (max {len(vars_vec)-1})"
                )
            if idx in seen:
                raise ValueError(f"{section_name}[{o_idx}]: duplicate index {idx}")
            seen.add(idx)
            src = vars_vec[idx]
            for j in range(base_dim):
                v[j] += val * src[j]
        out_vecs.append(v)

    return out_vecs, reduced_adds, len(fresh_list)


def verify_slp_file(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("z2", False) is True:
        raise ValueError("Scheme has z2=true (mod 2 only); exact integer Z scheme required")

    dims = data.get("n")
    if not isinstance(dims, list) or len(dims) != 3 or not all(isinstance(x, int) and x > 0 for x in dims):
        raise ValueError(f"Invalid dimensions n={dims}")
    n1, n2, n3 = dims
    m = data.get("m")
    if not isinstance(m, int) or m <= 0:
        raise ValueError(f"Invalid rank m={m}")

    U, u_adds, u_fv = expand_dag(n1 * n2, data.get("u_fresh", []), data.get("u", []), "u")
    V, v_adds, v_fv = expand_dag(n2 * n3, data.get("v_fresh", []), data.get("v", []), "v")
    W, w_adds, w_fv = expand_dag(m, data.get("w_fresh", []), data.get("w", []), "w")

    if len(U) != m or len(V) != m:
        raise ValueError(f"U and V must have m={m} rows, got {len(U)} and {len(V)}")
    if len(W) != n1 * n3:
        raise ValueError(f"W must have n1*n3={n1*n3} rows, got {len(W)}")

    # Compute naive additions of the expanded bilinear tensor (U, V, W) over Z
    u_naive = sum(max(0, sum(1 for x in row if x != 0) - 1) for row in U)
    v_naive = sum(max(0, sum(1 for x in row if x != 0) - 1) for row in V)
    w_naive = sum(max(0, sum(1 for x in row if x != 0) - 1) for row in W)
    total_naive = u_naive + v_naive + w_naive

    # Verify exact symbolic identity over Z:
    # In Perminov's convention, W encodes C^T of shape n3 x n1 in row-major order:
    # row c_idx = l * n1 + i computes C_{i, l} = sum_{j=0}^{n2-1} A_{i, j} * B_{j, l}.
    # Check both C^T order (l * n1 + i) and C order (i * n3 + l), requiring exact match on C^T order.
    errors_ct = 0
    for l in range(n3):
        for i in range(n1):
            c_idx = l * n1 + i
            w_row = W[c_idx]
            for a_idx in range(n1 * n2):
                ai, aj = a_idx // n2, a_idx % n2
                for b_idx in range(n2 * n3):
                    bj, bl = b_idx // n3, b_idx % n3
                    coeff = 0
                    for r in range(m):
                        wr = w_row[r]
                        if wr != 0:
                            ur = U[r][a_idx]
                            if ur != 0:
                                vr = V[r][b_idx]
                                if vr != 0:
                                    coeff += ur * vr * wr
                    target = 1 if (ai == i and bl == l and aj == bj) else 0
                    if coeff != target:
                        errors_ct += 1

    if errors_ct != 0:
        raise ValueError(f"Symbolic bilinear identity failed over Z ({errors_ct} mismatched monomials)")

    total_reduced = u_adds + v_adds + w_adds
    total_fv = u_fv + v_fv + w_fv

    declared_red = data.get("complexity", {}).get("reduced")
    if declared_red is not None and declared_red != total_reduced:
        raise ValueError(
            f"Declared complexity.reduced={declared_red} != recounted {total_reduced}"
        )

    return {
        "n": [n1, n2, n3],
        "m": m,
        "cr": total_reduced,
        "u_adds": u_adds,
        "v_adds": v_adds,
        "w_adds": w_adds,
        "fv": total_fv,
        "cn": total_naive,
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: verify_slp.py reduced_json_file [...]", file=sys.stderr)
        sys.exit(2)

    import os
    all_ok = True
    for path in sys.argv[1:]:
        try:
            res = verify_slp_file(path)
            n1, n2, n3 = res["n"]
            print(
                f"PASS: {os.path.basename(path)} | format={n1}x{n2}x{n3} m={res['m']} "
                f"cr={res['cr']} (U={res['u_adds']}, V={res['v_adds']}, W={res['w_adds']}) "
                f"fv={res['fv']} cn={res['cn']}"
            )
        except Exception as e:
            print(f"FAIL: {os.path.basename(path)} | {e}")
            all_ok = False

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
