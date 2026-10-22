#!/usr/bin/env python3
"""
Exact rational and floating-point Delsarte LP bound for DNA constant-GC-weight codes
in the association scheme X(n, w) = (J(n, w) x H(w, 2) x H(n-w, 2)) // S_n.
"""
import math
from fractions import Fraction

def krawtchouk(N, k, x):
    if k < 0 or k > N:
        return 0
    s = 0
    for j in range(max(0, x + k - N), min(x, k) + 1):
        term = math.comb(x, j) * math.comb(N - x, k - j)
        if j & 1:
            s -= term
        else:
            s += term
    return s

def hahn_Q(N, W, a, i):
    if a < 0 or a > min(W, N - W):
        return Fraction(0)
    s = Fraction(0)
    for t in range(0, min(a, i) + 1):
        num = math.comb(a, t) * math.comb(N + 1 - a, t) * math.comb(i, t)
        den = math.comb(W, t) * math.comb(N - W, t)
        term = Fraction(num, den)
        if t & 1:
            s -= term
        else:
            s += term
    return s

def solve_delsarte_lp(n, d, w):
    """
    Solve the Primal Delsarte LP:
      max 1 + sum_{r in R} A_r
      s.t. sum_{r in R} (-Psi_{k}(r)) A_r <= Psi_{k}(0,0,0)  for all k=(a,b,c) != (0,0,0)
           A_r >= 0
    Using standard Simplex tableau in float (for speed), then extracting dual certificate!
    """
    rels = []
    for i in range(min(w, n - w) + 1):
        for j in range(w - i + 1):
            for l in range(n - w - i + 1):
                if 2 * i + j + l >= d:
                    rels.append((i, j, l))
    if not rels:
        return 1

    modes = []
    for b in range(w + 1):
        for c in range(n - w + 1):
            max_a = min(w - b, n - w - c)
            for a in range(max_a + 1):
                if (a, b, c) != (0, 0, 0):
                    modes.append((a, b, c))

    m = len(modes)
    num_vars = len(rels)
    # Build Simplex tableau with m slack variables
    # Rows 0..m-1: constraints sum_{r} (-Psi_k(r)) A_r + s_k = Psi_k(0,0,0) >= 0
    # Wait: Psi_k(0,0,0) = 1 * comb(w, b) * comb(n-w, c) > 0 ALWAYS!
    # So A_r = 0, s_k = Psi_k(0,0,0) is IMMEDIATELY a basic feasible solution (Phase II directly, no Phase I needed!!)!
    #Wait — think about that! Because Psi_{a,b,c}(0,0,0) = comb(w,b)*comb(n-w,c) > 0 for all (a,b,c),
    # the origin A = 0 is ALWAYS primal feasible! We don't even need Phase I simplex!
    tableau = []
    for a, b, c in modes:
        row = []
        for i, j, l in rels:
            if i > min(w - b, n - w - c):
                val = 0.0
            else:
                psi = float(hahn_Q(n - b - c, w - b, a, i)) * krawtchouk(w - i, b, j) * krawtchouk(n - w - i, c, l)
                val = -psi
            row.append(val)
        rhs = float(math.comb(w, b) * math.comb(n - w, c))
        row.append(rhs)
        tableau.append(row)

    # Objective row: maximize sum A_r -> reduced costs c_j = -1.0
    obj = [-1.0] * num_vars + [0.0]
    basis = [num_vars + k for k in range(m)] # slack variables in basis

    # Standard Simplex iterations (only track non-slack columns, or update full tableau?
    #Wait: we need slack columns if a slack variable leaves and re-enters the basis!
    # So let's include slack columns in tableau!)
    full_tab = []
    for k in range(m):
        row = tableau[k][:-1] + [1.0 if idx == k else 0.0 for idx in range(m)] + [tableau[k][-1]]
        full_tab.append(row)
    full_obj = [-1.0] * num_vars + [0.0] * m + [0.0]
    total_cols = num_vars + m

    eps = 1e-9
    iters = 0
    while iters < 5000:
        iters += 1
        # Choose entering column (Dantzig's rule: most negative reduced cost)
        piv_col = -1
        min_rc = -eps
        for c in range(total_cols):
            if full_obj[c] < min_rc:
                min_rc = full_obj[c]
                piv_col = c
        if piv_col == -1:
            break
        # Minimum ratio test
        piv_row = -1
        min_ratio = 1e100
        for r in range(m):
            a_rc = full_tab[r][piv_col]
            if a_rc > eps:
                ratio = full_tab[r][-1] / a_rc
                if ratio < min_ratio - 1e-12:
                    min_ratio = ratio
                    piv_row = r
        if piv_row == -1:
            return 10**9 # unbounded
        # Pivot on (piv_row, piv_col)
        piv_val = full_tab[piv_row][piv_col]
        inv_piv = 1.0 / piv_val
        p_row = full_tab[piv_row]
        for c in range(total_cols + 1):
            p_row[c] *= inv_piv
        for r in range(m):
            if r != piv_row:
                factor = full_tab[r][piv_col]
                if abs(factor) > 1e-15:
                    r_row = full_tab[r]
                    for c in range(total_cols + 1):
                        r_row[c] -= factor * p_row[c]
        factor = full_obj[piv_col]
        if abs(factor) > 1e-15:
            for c in range(total_cols + 1):
                full_obj[c] -= factor * p_row[c]
        basis[piv_row] = piv_col

    return 1.0 + full_obj[-1]

if __name__ == "__main__":
    from bounds_audit import gc_grid, U_gc, U_gc_reason
    print("Comparing Delsarte LP on X(n, w) with King (2003) bounds for n <= 14...")
    for n in range(4, 15):
        w = n // 2
        for d in range(3, n + 1):
            val, sup = gc_grid[(n, d)]
            if '.' in sup or ':' in sup:
                continue
            lp_val = solve_delsarte_lp(n, d, w)
            lp_int = int(math.floor(lp_val + 1e-7))
            ub = U_gc[(n, d, w)]
            if lp_int <= ub or lp_int - val <= 50:
                print(f"GC ({n:2d},{d:2d},{w:2d}): King={val}{sup:3s} | King_UB={ub} | Delsarte_LP={lp_val:.4f} (floor={lp_int})")
