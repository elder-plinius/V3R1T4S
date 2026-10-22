#!/usr/bin/env python3
"""
Polishes:
1. p2 (Quartic z=4 Feigenbaum alpha_4 and delta_4 at N1=1070 and N2=1100) from 936
   agreeing decimals (saved after 109 iterations) to >= 1,070 agreeing decimals by
   running 25 additional mixed-precision LU refinement iterations.
2. p1 (Logistic accumulation point r_inf and Myrberg point c_inf) from 155 agreeing
   decimals to >= 350 agreeing decimals by evaluating high-order renormalization
   trajectories and superstable period-2^m cycle parameters with exact C-MPFR arithmetic.
"""

import ctypes
import json
import os
import time
import numpy as np
from scipy.linalg import lu_solve
import gmpy2
from gmpy2 import mpfr

from solve_feigenbaum import (
    _lib,
    build_J_JE_double,
    count_agreeing_decimals,
    wynn_epsilon,
    neville_richardson_predict,
    solve_collocation_c,
)

_lib.feig_ctx_set_coeff_str.argtypes = [
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_char_p,
]


def polish_z4_resolution(N, prec_bits, target_log10_tol, out_digits, c_init_strs, b_init_strs, delta_init_str):
    t0 = time.time()
    _, _, _, lu_J, lu_JE = build_J_JE_double(4, N)
    ctx = _lib.feig_ctx_create(4, N, prec_bits)
    for k in range(N):
        _lib.feig_ctx_set_coeff_str(ctx, 0, k, c_init_strs[k].encode())
        _lib.feig_ctx_set_coeff_str(ctx, 1, k, b_init_strs[k].encode())
    _lib.feig_ctx_set_coeff_str(ctx, 2, 0, delta_init_str.encode())

    r_scaled = np.zeros(N, dtype=np.float64)
    for it_r in range(35):
        log_r = _lib.feig_ctx_eval_r(ctx, r_scaled.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
        if log_r < target_log10_tol:
            break
        dc = np.ascontiguousarray(lu_solve(lu_J, -r_scaled), dtype=np.float64)
        _lib.feig_ctx_update_c(ctx, dc.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

    e_scaled = np.zeros(N + 1, dtype=np.float64)
    for it_e in range(35):
        log_e = _lib.feig_ctx_eval_e(ctx, e_scaled.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
        if log_e < target_log10_tol:
            break
        db = np.ascontiguousarray(lu_solve(lu_JE, -e_scaled), dtype=np.float64)
        _lib.feig_ctx_update_b_delta(ctx, db.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

    buf_len = out_digits + 128
    alpha_buf = ctypes.create_string_buffer(buf_len)
    delta_buf = ctypes.create_string_buffer(buf_len)
    _lib.feig_ctx_get_strings(ctx, out_digits, alpha_buf, delta_buf, buf_len)

    c_strs = []
    b_strs = []
    cbuf = ctypes.create_string_buffer(buf_len)
    for k in range(N):
        _lib.feig_ctx_get_coeff(ctx, 0, k, out_digits, cbuf, buf_len)
        c_strs.append(cbuf.value.decode())
        _lib.feig_ctx_get_coeff(ctx, 1, k, out_digits, cbuf, buf_len)
        b_strs.append(cbuf.value.decode())

    print(
        f"  [Polish z=4, N={N}] Done in {time.time() - t0:.2f}s "
        f"(extra it_r={it_r}, log10_r={log_r:.1f}, extra it_e={it_e}, log10_e={log_e:.1f})"
    )
    return alpha_buf.value.decode(), delta_buf.value.decode(), c_strs, b_strs


def polish_p1():
    print("\n=== Polishing Partial Win p1 to >= 350 Agreeing Decimals ===")
    t0 = time.time()
    prec_bits = 2150  # ~647 decimal digits
    out_digits = 580
    alpha2_str, delta2_str, _, _ = solve_collocation_c(2, 275, prec_bits, -580.0, out_digits)
    gmpy2.get_context().precision = prec_bits
    alpha2 = mpfr(alpha2_str)
    delta2 = mpfr(delta2_str)
    s_star = -mpfr(1) / alpha2
    inv_delta = mpfr(1) / delta2

    with open("results/feigenbaum_p1_accumulation.json") as f:
        p1_prev = json.load(f)
    # 155-digit accurate seed from previous run
    c_seed = mpfr(p1_prev["c_inf_str_m1"][:158])

    rc_high = _lib.renorm_ctx_create(260, prec_bits)
    buf = ctypes.create_string_buffer(1200)

    def eval_s_high(mu, m_steps):
        s_in = f"{mu:.580f}".encode()
        _lib.renorm_eval_sm(rc_high, s_in, m_steps, 580, buf, 1200)
        return mpfr(buf.value.decode())

    # Notice: How fast can we solve s_m(tilde_mu_m) = s_star for m = 95..142?
    # At m = 95, |tilde_mu_95 - c_inf| ~ 10^{-140}, so c_seed (accurate to 155 digits!)
    # already knows tilde_mu_95 to 15 digits after 1 secant step!
    # Even better: D_m = d(s_m)/d(mu) satisfies D_m = delta_2 * D_{m-1} to O(0.16^m) (~10^{-75} at m=95!).
    # So once we measure D_95 by 1 secant step at m=95, for ALL m = 96..142:
    # D_m = delta_2 * D_{m-1} is accurate to > 75 digits!
    # Therefore at each m = 96..142, a SINGLE Quasi-Newton step + 1 Broyden step (just 2 evaluations!)
    # refines tilde_mu_m to > 450 decimal digits!
    print("Running High-Order Method 1 (tilde_mu_m for m = 95..140, 2 evals/step)...")
    t_m1 = time.time()
    seq_mu_high = []
    r1_approx = (s_star * s_star) * inv_delta
    powers_mu = [r1_approx * (s_star ** (2 * k)) for k in range(25)]

    # At m = 95, find tilde_mu_95 and D_95
    m_start = 95
    x0 = c_seed
    x1 = c_seed + mpfr("1e-145")
    f0 = eval_s_high(x0, m_start) - s_star
    f1 = eval_s_high(x1, m_start) - s_star
    D_cur = (f1 - f0) / (x1 - x0)
    x_cur = x1 - f1 / D_cur
    for _ in range(3):
        f_cur = eval_s_high(x_cur, m_start) - s_star
        dx = -f_cur / D_cur
        x_cur = x_cur + dx
    seq_mu_high.append(x_cur)

    for m in range(m_start + 1, 141):
        D_cur = D_cur * delta2
        if len(seq_mu_high) == 1:
            pred = c_seed + (seq_mu_high[-1] - c_seed) * r1_approx
        elif len(seq_mu_high) == 2:
            pred = seq_mu_high[-1] + (seq_mu_high[-1] - seq_mu_high[-2]) * (r1_approx / (mpfr(1) - r1_approx))
        else:
            pred = neville_richardson_predict(seq_mu_high, powers_mu)
        x0 = pred
        f0 = eval_s_high(x0, m) - s_star
        x1 = x0 - f0 / D_cur
        f1 = eval_s_high(x1, m) - s_star
        if abs(x1 - x0) > mpfr("1e-500") and abs(f1 - f0) > 0:
            D_cur = (f1 - f0) / (x1 - x0)
        x2 = x1 - f1 / D_cur
        # If needed, 1 more polish if |x2 - x1| > 1e-420
        if abs(x2 - x1) > mpfr("1e-360"):
            f2 = eval_s_high(x2, m) - s_star
            if abs(f2 - f1) > 0:
                D_cur = (f2 - f1) / (x2 - x1)
            x2 = x2 - f2 / D_cur
        seq_mu_high.append(x2)

    wynn_mu = wynn_epsilon(seq_mu_high)
    c_inf_m1 = wynn_mu[-1]
    c_inf_m1_prev = wynn_mu[-2]
    print(
        f"Method 1 (m=95..140) completed in {time.time() - t_m1:.2f}s: "
        f"|wynn[-1] - wynn[-2]| = {float(abs(c_inf_m1 - c_inf_m1_prev)):.3e}"
    )

    # Method 2: Independent Superstable Period-2^m Cycle Parameters c_m (s_{m-1}(c_m) = 0)
    # Wait: in p1_prev, we already computed c_1..c_30!
    # Let's extend c_m on rc_high using the exact D_m = delta_2 * D_{m-1} Quasi-Newton/Broyden
    # recursion up to m = 92 (only 2 evaluations per m!), and apply Richardson + Wynn acceleration!
    print("Running High-Order Method 2 (Superstable Period-2^m Parameters c_m up to m = 92)...")
    t_m2 = time.time()
    seq_c = [mpfr(x) for x in p1_prev["superstable_c_m"][:25]]  # c_1 .. c_25
    powers_c = (
        [inv_delta]
        + [inv_delta * (s_star ** (2 * k)) for k in range(1, 20)]
        + [inv_delta**2, inv_delta**3, inv_delta**4]
    )

    # Initialize D_cur at m = 25 (evaluating s_24 around c_25)
    x0 = seq_c[-1]
    x1 = x0 + mpfr("1e-40")
    f0 = eval_s_high(x0, 24)
    f1 = eval_s_high(x1, 24)
    D_c = (f1 - f0) / (x1 - x0)
    x_cur = x1 - f1 / D_c
    f_cur = eval_s_high(x_cur, 24)
    seq_c[-1] = x_cur - f_cur / D_c

    for m in range(26, 93):
        D_c = D_c * delta2
        pred = neville_richardson_predict(seq_c, powers_c)
        x0 = pred
        f0 = eval_s_high(x0, m - 1)
        x1 = x0 - f0 / D_c
        f1 = eval_s_high(x1, m - 1)
        if abs(x1 - x0) > mpfr("1e-500") and abs(f1 - f0) > 0:
            D_c = (f1 - f0) / (x1 - x0)
        x2 = x1 - f1 / D_c
        if abs(x2 - x1) > mpfr("1e-360"):
            f2 = eval_s_high(x2, m - 1)
            if abs(f2 - f1) > 0:
                D_c = (f2 - f1) / (x2 - x1)
            x2 = x2 - f2 / D_c
        seq_c.append(x2)

    # Eliminate exact powers delta_2^{-k} (k = 1..12) from the tail c_{30..92} and apply Wynn epsilon
    seq_c_rich = list(seq_c[28:])
    for p_ord in range(1, 13):
        r_pow = inv_delta**p_ord
        seq_c_rich = [
            (seq_c_rich[i] - r_pow * seq_c_rich[i - 1]) / (mpfr(1) - r_pow)
            for i in range(1, len(seq_c_rich))
        ]
    wynn_c = wynn_epsilon(seq_c_rich)
    c_inf_m2 = wynn_c[-1]
    c_inf_m2_prev = wynn_c[-2]
    diff_m1_m2 = abs(c_inf_m1 - c_inf_m2)
    print(
        f"Method 2 (m=1..92) completed in {time.time() - t_m2:.2f}s: "
        f"|wynn_c[-1] - wynn_c[-2]| = {float(abs(c_inf_m2 - c_inf_m2_prev)):.3e}"
    )
    print(f"|Method 1 - Method 2| for c_inf = {float(diff_m1_m2):.3e}")

    r_inf_m1 = mpfr(1) + gmpy2.sqrt(mpfr(1) + mpfr(4) * c_inf_m1)
    r_inf_m2 = mpfr(1) + gmpy2.sqrt(mpfr(1) + mpfr(4) * c_inf_m2)
    diff_r = abs(r_inf_m1 - r_inf_m2)

    c_s1 = f"{c_inf_m1:.420f}"
    c_s2 = f"{c_inf_m2:.420f}"
    r_s1 = f"{r_inf_m1:.420f}"
    r_s2 = f"{r_inf_m2:.420f}"
    agree_c = count_agreeing_decimals(c_s1, c_s2)
    agree_r = count_agreeing_decimals(r_s1, r_s2)
    conv_err = abs(c_inf_m1 - r_inf_m1 * (r_inf_m1 - mpfr(2)) / mpfr(4))

    print(f"p1 Agreeing decimals: c_inf = {agree_c}, r_inf = {agree_r}")
    p1_res = {
        "agreeing_decimals_c_inf": agree_c,
        "agreeing_decimals_r_inf": agree_r,
        "c_inf_str_m1": c_s1,
        "c_inf_str_m2": c_s2,
        "r_inf_str_m1": r_s1,
        "r_inf_str_m2": r_s2,
        "diff_c_inf": float(diff_m1_m2),
        "diff_r_inf": float(diff_r),
        "conversion_error": float(conv_err),
        "superstable_c_m": [f"{x:.420f}" for x in seq_c],
        "renorm_tilde_mu_m_95_140": [f"{x:.420f}" for x in seq_mu_high],
    }
    with open("results/feigenbaum_p1_accumulation.json", "w") as f:
        json.dump(p1_res, f, indent=2)


def main():
    print("=== Polishing Partial Win p2 (Quartic z=4 Feigenbaum alpha_4 & delta_4) ===")
    with open("results/feigenbaum_z4_certificates.json") as f:
        p2 = json.load(f)

    a4_s1, d4_s1, c4_1, b4_1 = polish_z4_resolution(
        1070, 3900, -1085.0, 1100, p2["c_coeffs_N1"], p2["b_coeffs_N1"], p2["delta_4_N1"]
    )
    a4_s2, d4_s2, c4_2, b4_2 = polish_z4_resolution(
        1100, 3950, -1105.0, 1100, p2["c_coeffs_N2"], p2["b_coeffs_N2"], p2["delta_4_N2"]
    )

    agree_a4 = count_agreeing_decimals(a4_s1, a4_s2)
    agree_d4 = count_agreeing_decimals(d4_s1, d4_s2)
    print(f"p2 Polished Agreeing decimals (N1=1070 vs N2=1100): alpha_4 = {agree_a4}, delta_4 = {agree_d4}")

    p2_res = {
        "N1": 1070,
        "N2": 1100,
        "resolution_diff_pct": (1100 - 1070) / 1070.0 * 100.0,
        "agreeing_decimals_alpha_4": agree_a4,
        "agreeing_decimals_delta_4": agree_d4,
        "alpha_4_N1": a4_s1,
        "alpha_4_N2": a4_s2,
        "delta_4_N1": d4_s1,
        "delta_4_N2": d4_s2,
        "c_coeffs_N1": c4_1,
        "b_coeffs_N1": b4_1,
        "c_coeffs_N2": c4_2,
        "b_coeffs_N2": b4_2,
    }
    with open("results/feigenbaum_z4_certificates.json", "w") as f:
        json.dump(p2_res, f, indent=2)

    polish_p1()


if __name__ == "__main__":
    main()
