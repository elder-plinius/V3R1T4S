#!/usr/bin/env python3
"""
frozen_gram_builder.py
Constructs and verifies exact Partial Win p2 (Frozen Gram Target) certificates
for unclosed orders n == 1 (mod 4), including the odd-square orders n = 49 = 7^2
and n = 81 = 9^2 where G is constructively rationally congruent to BOTH I_n and n I_n:
    Q I_n Q^T = G   and   P (n I_n) P^T = G   with P = Q / sqrt(n).
"""

import json
import math
import os
import subprocess
import sys


def is_prime(p):
    if p < 2:
        return False
    if p % 2 == 0:
        return p == 2
    d = 3
    while d * d <= p:
        if p % d == 0:
            return False
        d += 2
    return True


def build_paley1_hadamard(m):
    """Build Paley Class I Hadamard matrix of order m = p + 1 where p == 3 (mod 4) is prime."""
    p = m - 1
    assert p % 4 == 3 and is_prime(p), f"p={p} is not a prime == 3 (mod 4)"
    qr = set((x * x) % p for x in range(1, p))
    H = [[1] * m for _ in range(m)]
    for i in range(1, m):
        for j in range(1, m):
            if i == j:
                H[i][j] = -1
            else:
                H[i][j] = 1 if ((j - i) % p) in qr else -1
    return H


def find_best_square_discriminant_border(n, D_rec):
    """
    Search over 3-level border vectors g in {5, 1, -3}^(n-1) with multiplicities (a, b, c)
    satisfying a + b + c = n - 1 such that
        val(g) = 2*n*(n-1)^2 - 2*(n-1)*sum(g_i^2) + (sum(g_i))^2 = r^2
    is an exact integer square with sqrt(det G) / 2^(n-1) > D_rec.
    """
    m = n - 1
    k = m // 4
    scale_pow = k ** (2 * k - 1)
    best = None
    for a in range(m + 1):
        for c in range(m - a + 1):
            b = m - a - c
            sum_g = 5 * a + b - 3 * c
            sum_g2 = 25 * a + b + 9 * c
            val = 2 * n * m * m - 2 * m * sum_g2 + sum_g * sum_g
            if val <= 0:
                continue
            r = math.isqrt(val)
            if r * r == val and r % 4 == 0:
                D_norm = (r // 4) * scale_pow
                if D_norm > D_rec:
                    if best is None or r > best["r"]:
                        best = {
                            "a": a,
                            "b": b,
                            "c": c,
                            "r": r,
                            "D_norm": D_norm,
                            "eff_factor": r / 4.0,
                        }
    return best


def build_frozen_gram_certificate(n, border_info):
    """
    Construct the explicit n x n Frozen Gram Target G, the (n-1) x n {-1, +1} realized
    prefix M0 = [1_{n-1}, H_{n-1}], and the exact n x n rational congruence matrix
    Q = (1 / Q_den) * Q_num satisfying Q Q^T = G.
    """
    m = n - 1
    H = build_paley1_hadamard(m)
    M0 = [[1] + H[i][:] for i in range(m)]

    a, b, c, r = border_info["a"], border_info["b"], border_info["c"], border_info["r"]
    g = [5] * a + [1] * b + [-3] * c
    assert len(g) == m

    G = [[0] * n for _ in range(n)]
    for i in range(m):
        for j in range(m):
            G[i][j] = n if i == j else 1
        G[i][m] = g[i]
        G[m][i] = g[i]
    G[m][m] = n

    # Right kernel vector u in Z^n satisfying M0 * u = 0 and u^T u = 2 m^2:
    # u = [ -m, (H^T 1_m)^T ]^T
    u = [-m] + [sum(H[i][j] for i in range(m)) for j in range(m)]
    assert sum(u[col] * u[col] for col in range(n)) == 2 * m * m
    for i in range(m):
        assert sum(M0[i][col] * u[col] for col in range(n)) == 0

    # G0^{-1} = (1/m) * (I_m - (1/(2m)) J_m)
    # So 2 m^2 (G0^{-1} g)_i = 2 m g_i - sum(g)
    sum_g = sum(g)
    alpha_num = [2 * m * g[i] - sum_g for i in range(m)]

    # Common denominator Q_den = 2 m^2:
    # For rows 0..m-1 of Q_num: Q_den * M0[i]
    # For row m of Q_num: alpha_num^T M0 + r * u^T
    Q_den = 2 * m * m
    Q_num = [[Q_den * x for x in row] for row in M0]
    last_row_num = []
    for col in range(n):
        proj = sum(alpha_num[i] * M0[i][col] for i in range(m))
        last_row_num.append(proj + r * u[col])
    Q_num.append(last_row_num)

    # Simplify Q_den and Q_num by their global GCD
    g_all = Q_den
    for row in Q_num:
        for val in row:
            g_all = math.gcd(g_all, abs(val))
    Q_den //= g_all
    Q_num = [[val // g_all for val in row] for row in Q_num]

    return {
        "n": n,
        "border_multiplicities_5_1_neg3": [a, b, c],
        "r": r,
        "norm_det_sqrt_G": str(border_info["D_norm"]),
        "Q_den": Q_den,
        "G": G,
        "M0": M0,
        "Q_num": Q_num,
    }


def main():
    attempt_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    run_dir = os.path.dirname(os.path.dirname(attempt_dir))
    results_dir = os.path.join(run_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    with open(os.path.join(run_dir, "data", "maxdet_table.json"), "r", encoding="utf-8") as f:
        table = json.load(f)

    open_orders = [29, 33, 37, 45, 49, 53, 57, 65, 69, 73, 77, 81, 85, 89, 93, 97]
    print("=== [1] Scanning All 16 Unclosed n == 1 (mod 4) Orders in 29 <= n <= 97 ===")
    for n in open_orders:
        k = (n - 1) // 4
        D_rec = int(table[str(n)]["exact_norm_det"])
        rec_fac = D_rec / (k ** (2 * k - 1))
        barba_fac = math.sqrt(2 * n - 1) * k
        best = find_best_square_discriminant_border(n, D_rec)
        if best:
            R_ratio = best["eff_factor"] / barba_fac
            print(f"  n={n:2d} (k={k:2d}): (a,b,c)=({best['a']:2d},{best['b']:2d},{best['c']:2d}) "
                  f"r={best['r']:4d} -> eff_factor={best['eff_factor']:7.3f} > rec={rec_fac:7.3f} (R={R_ratio:.4f})")

    print("\n=== [2] Building and Verifying Explicit p2 Certificates for Odd Squares n=49 and n=81 ===")
    for n in [49, 81]:
        D_rec = int(table[str(n)]["exact_norm_det"])
        best = find_best_square_discriminant_border(n, D_rec)
        cert = build_frozen_gram_certificate(n, best)
        out_name = f"G{n}_p2.json"
        out_path = os.path.join(results_dir, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(cert, f, indent=2)
        print(f"\nSaved results/{out_name} (Q_den={cert['Q_den']}, r={cert['r']})")
        subprocess.run(
            ["python3", "verify_maxdet.py", "--gram", os.path.join("results", out_name)],
            cwd=run_dir, check=True
        )


if __name__ == "__main__":
    main()
