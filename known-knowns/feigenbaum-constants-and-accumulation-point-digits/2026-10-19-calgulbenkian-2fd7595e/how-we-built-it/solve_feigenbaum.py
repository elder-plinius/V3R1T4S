#!/usr/bin/env python3
"""
Ultra-Fast C-MPFR + SciPy Mixed-Precision Solver for Target 29:
  feigenbaum-constants-and-accumulation-point-digits

1. Partial Win p2:
   Quartic (z = 4) Feigenbaum constants alpha_4 and delta_4 to >= 1,050 agreeing
   decimal digits across two Chebyshev collocation resolutions N1 = 1070 and N2 = 1100
   (differing by 2.80% > 2%), exceeding OEIS A195102 (49 digits) and Thurlby 2021 (~330 digits).

2. Partial Win p1:
   Logistic map accumulation point r_inf (OEIS A098587, 95 digits) and Myrberg point
   c_inf (OEIS A218453, 65 digits) to >= 340 agreeing decimal digits via two independent methods:
   - Method 1: Renormalization fixed-point projection psi_m(1; tilde_mu_m) = phi*(1) = -1/alpha_2
     with Richardson + Wynn epsilon acceleration.
   - Method 2: Exact superstable period-2^m cycle parameters c_m (f_{c_m}^{(2^m)}(0) = 0 via
     the exact renormalization identity s_{m-1}(c_m) = 0) with Richardson + Wynn acceleration.
"""

import ctypes
import json
import os
import time
from concurrent.futures import ProcessPoolExecutor
import numpy as np
from scipy.linalg import lu_factor, lu_solve
import gmpy2
from gmpy2 import mpfr

LIB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libfeig_c.dylib")
_lib = ctypes.CDLL(LIB_PATH)

_lib.feig_ctx_create.restype = ctypes.c_void_p
_lib.feig_ctx_create.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_long]
_lib.feig_ctx_set_initial.argtypes = [
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double),
    ctypes.c_double,
]
_lib.feig_ctx_eval_r.restype = ctypes.c_double
_lib.feig_ctx_eval_r.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)]
_lib.feig_ctx_update_c.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)]
_lib.feig_ctx_eval_e.restype = ctypes.c_double
_lib.feig_ctx_eval_e.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)]
_lib.feig_ctx_update_b_delta.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_double)]
_lib.feig_ctx_get_strings.argtypes = [
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_size_t,
]
_lib.feig_ctx_get_coeff.argtypes = [
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_size_t,
]
_lib.renorm_ctx_create.restype = ctypes.c_void_p
_lib.renorm_ctx_create.argtypes = [ctypes.c_int, ctypes.c_long]
_lib.renorm_eval_sm.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_size_t,
]


def cheb_T_U_np(t, N):
    m = len(t)
    T = np.ones((m, N))
    U = np.ones((m, N))
    if N > 1:
        T[:, 1] = t
        U[:, 1] = 2.0 * t
    for k in range(2, N):
        T[:, k] = 2.0 * t * T[:, k - 1] - T[:, k - 2]
        U[:, k] = 2.0 * t * U[:, k - 1] - U[:, k - 2]
    dT = np.zeros((m, N))
    for k in range(1, N):
        dT[:, k] = k * U[:, k - 1]
    return T, dT


def eval_phi_dphi_np(c_short, u, N):
    K = len(c_short)
    T, dT = cheb_T_U_np(2.0 * u - 1.0, N)
    S = np.zeros(len(u))
    dS = np.zeros(len(u))
    for k in range(K):
        S += c_short[k] * T[:, k]
        dS += 2.0 * c_short[k] * dT[:, k]
    return 1.0 + u * S, S + u * dS, T


def build_J_JE_double(z, N):
    c = np.zeros(4)
    c[0] = -1.47 if z == 2 else -1.74
    c[1] = 0.06 if z == 2 else 0.12
    for curN in [4, 8, 16, 32]:
        if len(c) < curN:
            c = np.pad(c, (0, curN - len(c)))
        j = np.arange(curN)
        u = 0.5 * (1.0 + np.cos((2 * j + 1) * np.pi / (2 * curN)))
        Tu, _ = cheb_T_U_np(2.0 * u - 1.0, curN)
        Vu = u[:, None] * Tu
        for _ in range(12):
            p1 = 1.0 + np.sum(c)
            w = (p1**z) * u
            pu = 1.0 + Vu @ c
            y, dy, Tw = eval_phi_dphi_np(c, w, curN)
            v = y**z
            pv, dpv, Tv = eval_phi_dphi_np(c, v, curN)
            r = pu * p1 - pv
            if np.max(np.abs(r)) < 1e-14:
                break
            Vw = w[:, None] * Tw
            Vv = v[:, None] * Tv
            dy_dc = Vw + (dy * z * (p1 ** (z - 1)) * u)[:, None]
            dv_dc = (z * (y ** (z - 1)))[:, None] * dy_dc
            J = p1 * Vu + pu[:, None] - Vv - dpv[:, None] * dv_dc
            c -= np.linalg.solve(J, r)
    c32 = np.ascontiguousarray(c, dtype=np.float64)
    j32 = np.arange(32)
    u32 = 0.5 * (1.0 + np.cos((2 * j32 + 1) * np.pi / 64.0))
    Tu32, _ = cheb_T_U_np(2.0 * u32 - 1.0, 32)
    p1 = 1.0 + np.sum(c32)
    w32 = (p1**z) * u32
    y32, _, Tw32 = eval_phi_dphi_np(c32, w32, 32)
    v32 = y32**z
    _, dpv32, Tv32 = eval_phi_dphi_np(c32, v32, 32)
    rhs32 = (1.0 / p1) * (Tv32 + (z * dpv32 * (y32 ** (z - 1)))[:, None] * Tw32)
    L32 = np.linalg.solve(Tu32, rhs32)
    evals, evecs = np.linalg.eig(L32)
    idx = np.argmax(evals.real)
    delta0 = float(evals[idx].real)
    b32 = evecs[:, idx].real
    b32 /= np.sum(b32 * ((-1.0) ** np.arange(32)))
    b32 = np.ascontiguousarray(b32, dtype=np.float64)

    j = np.arange(N)
    u = 0.5 * (1.0 + np.cos((2 * j + 1) * np.pi / (2 * N)))
    Tu, _ = cheb_T_U_np(2.0 * u - 1.0, N)
    Vu = u[:, None] * Tu
    p1 = 1.0 + np.sum(c32)
    w = (p1**z) * u
    pu = np.ones(N)
    for k in range(32):
        pu += c32[k] * Vu[:, k]
    y, dy, Tw = eval_phi_dphi_np(c32, w, N)
    v = y**z
    pv, dpv, Tv = eval_phi_dphi_np(c32, v, N)
    Vw = w[:, None] * Tw
    Vv = v[:, None] * Tv
    dy_dc = Vw + (dy * z * (p1 ** (z - 1)) * u)[:, None]
    dv_dc = (z * (y ** (z - 1)))[:, None] * dy_dc
    J = p1 * Vu + pu[:, None] - Vv - dpv[:, None] * dv_dc
    rhsN = (1.0 / p1) * (Tv + (z * dpv * (y ** (z - 1)))[:, None] * Tw)
    JE = np.zeros((N + 1, N + 1))
    JE[:N, :N] = rhsN - delta0 * Tu
    psi0_u = np.zeros(N)
    for k in range(32):
        psi0_u += b32[k] * Tu[:, k]
    JE[:N, N] = -psi0_u
    JE[N, :N] = (-1.0) ** np.arange(N)
    return c32, b32, delta0, lu_factor(J), lu_factor(JE)


def solve_collocation_c(z, N, prec_bits, target_log10_tol, out_digits):
    t0 = time.time()
    c32, b32, delta0, lu_J, lu_JE = build_J_JE_double(z, N)
    ctx = _lib.feig_ctx_create(z, N, prec_bits)
    _lib.feig_ctx_set_initial(
        ctx,
        32,
        c32.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        b32.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
        delta0,
    )
    r_scaled = np.zeros(N, dtype=np.float64)
    for it_r in range(110):
        log_r = _lib.feig_ctx_eval_r(ctx, r_scaled.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
        if log_r < target_log10_tol:
            break
        dc = np.ascontiguousarray(lu_solve(lu_J, -r_scaled), dtype=np.float64)
        _lib.feig_ctx_update_c(ctx, dc.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

    e_scaled = np.zeros(N + 1, dtype=np.float64)
    for it_e in range(110):
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
        f"  [C-MPFR z={z}, N={N}] Solved in {time.time() - t0:.2f}s "
        f"(it_r={it_r}, log10_r={log_r:.1f}, it_e={it_e}, log10_e={log_e:.1f}, "
        f"|c[-1]|={float(c_strs[-1]):.2e}, |b[-1]|={float(b_strs[-1]):.2e})"
    )
    return alpha_buf.value.decode(), delta_buf.value.decode(), c_strs, b_strs


def count_agreeing_decimals(s1, s2):
    p1 = s1.split(".")[1]
    p2 = s2.split(".")[1]
    for i in range(min(len(p1), len(p2))):
        if p1[i] != p2[i]:
            return i
    return min(len(p1), len(p2))


def wynn_epsilon(seq):
    n = len(seq)
    e_prev = [mpfr(0)] * (n + 1)
    e_curr = list(seq)
    even_cols = [seq[-1]]
    for k in range(1, n):
        e_next = []
        for i in range(n - k):
            diff = e_curr[i + 1] - e_curr[i]
            if diff == 0:
                val = e_prev[i + 1]
            else:
                val = e_prev[i + 1] + mpfr(1) / diff
            e_next.append(val)
        e_prev = e_curr
        e_curr = e_next
        if k % 2 == 0 and len(e_curr) > 0:
            even_cols.append(e_curr[-1])
    return even_cols


def neville_richardson_predict(seq, powers):
    if len(seq) < 3:
        return seq[-1]
    diffs = [seq[i] - seq[i - 1] for i in range(1, len(seq))]
    K = min(len(diffs) - 1, len(powers))
    poly = [mpfr(1)]
    for j in range(K):
        rj = powers[j]
        new_poly = [mpfr(0)] * (len(poly) + 1)
        for idx, coeff in enumerate(poly):
            new_poly[idx] += coeff
            new_poly[idx + 1] -= rj * coeff
        poly = new_poly
    d_next = mpfr(0)
    for i in range(1, K + 1):
        d_next -= poly[i] * diffs[-i]
    return seq[-1] + d_next


def solve_p1_accumulation_point():
    print("\n=== Solving Partial Win p1: Logistic Accumulation Point r_inf & Myrberg Point c_inf ===")
    t0 = time.time()
    prec_bits = 1850
    out_digits = 500
    alpha2_str, delta2_str, _, _ = solve_collocation_c(2, 260, prec_bits, -520.0, out_digits)
    gmpy2.get_context().precision = prec_bits
    alpha2 = mpfr(alpha2_str)
    delta2 = mpfr(delta2_str)
    s_star = -mpfr(1) / alpha2
    inv_delta = mpfr(1) / delta2

    # Two-level C renormalization contexts:
    # Level 1 (fast predictor/secant): N_low = 120, prec = 950 bits (~285 digits)
    # Level 2 (high-precision polish): N_high = 245, prec = 1850 bits (~556 digits)
    rc_low = _lib.renorm_ctx_create(120, 950)
    rc_high = _lib.renorm_ctx_create(245, 1850)
    buf = ctypes.create_string_buffer(1024)

    def eval_s(rc, mu, m_steps, digits):
        mu_s = gmpy2.digits(mu, 10, digits + 20)
        # format string from mpfr
        s_in = f"{mu:.{digits}f}".encode()
        _lib.renorm_eval_sm(rc, s_in, m_steps, digits, buf, 1024)
        return mpfr(buf.value.decode())

    # Method 1: tilde_mu_m where s_m(tilde_mu_m) = s_star for m = 1..52
    print("Running Method 1 (Renormalization Fixed-Point Projection tilde_mu_m)...")
    t_m1 = time.time()
    seq_mu = []
    r1_approx = (s_star * s_star) * inv_delta
    powers_mu = [r1_approx * (s_star ** (2 * k)) for k in range(30)]
    for m in range(1, 51):
        if m == 1:
            x0, x1 = mpfr("1.401"), mpfr("1.4012")
        elif m == 2:
            x0, x1 = mpfr("1.401155"), mpfr("1.4011552")
        else:
            pred = neville_richardson_predict(seq_mu, powers_mu)
            last_diff = abs(seq_mu[-1] - seq_mu[-2])
            eps = last_diff * mpfr("1e-5") if last_diff > mpfr("1e-240") else mpfr("1e-240")
            x0 = pred
            x1 = pred + eps

        # First converge to ~190 digits on rc_low (N=120)
        f0 = eval_s(rc_low, x0, m, 270) - s_star
        deriv = mpfr(1)
        for _ in range(6):
            f1 = eval_s(rc_low, x1, m, 270) - s_star
            if abs(f1 - f0) == 0:
                break
            deriv = (f1 - f0) / (x1 - x0)
            dx = -f1 / deriv
            x0, f0 = x1, f1
            x1 = x1 + dx
            if abs(dx) < mpfr("1e-188"):
                break

        # Polish on rc_high (N=245) using the known derivative `deriv` (only 1 or 2 evals!)
        for _ in range(2):
            fh = eval_s(rc_high, x1, m, 500) - s_star
            dx = -fh / deriv
            x1 = x1 + dx
            if abs(dx) < mpfr("1e-480"):
                break
        seq_mu.append(x1)

    wynn_mu = wynn_epsilon(seq_mu)
    c_inf_m1 = wynn_mu[-1]
    c_inf_m1_prev = wynn_mu[-2]
    print(
        f"Method 1 completed in {time.time() - t_m1:.2f}s: "
        f"|wynn[-1] - wynn[-2]| = {float(abs(c_inf_m1 - c_inf_m1_prev)):.3e}"
    )

    # Method 2: Superstable period-2^m cycle parameters c_m (s_{m-1}(c_m) = 0)
    print("Running Method 2 (Superstable Period-2^m Cycle Parameters c_m + Richardson/Wynn)...")
    t_m2 = time.time()
    seq_c = [mpfr("1.0")]
    powers_c = (
        [inv_delta]
        + [inv_delta * (s_star ** (2 * k)) for k in range(1, 20)]
        + [inv_delta**2, inv_delta**3]
    )
    for m in range(2, 53):
        if m == 2:
            x0, x1 = mpfr("1.3107"), mpfr("1.310703")
        elif m == 3:
            x0, x1 = mpfr("1.381547"), mpfr("1.3815475")
        else:
            pred = neville_richardson_predict(seq_c, powers_c)
            last_diff = abs(seq_c[-1] - seq_c[-2])
            eps = last_diff * mpfr("1e-5") if last_diff > mpfr("1e-240") else mpfr("1e-240")
            x0 = pred
            x1 = pred + eps

        f0 = eval_s(rc_low, x0, m - 1, 270)
        deriv = mpfr(1)
        for _ in range(6):
            f1 = eval_s(rc_low, x1, m - 1, 270)
            if abs(f1 - f0) == 0:
                break
            deriv = (f1 - f0) / (x1 - x0)
            dx = -f1 / deriv
            x0, f0 = x1, f1
            x1 = x1 + dx
            if abs(dx) < mpfr("1e-188"):
                break

        for _ in range(2):
            fh = eval_s(rc_high, x1, m - 1, 500)
            dx = -fh / deriv
            x1 = x1 + dx
            if abs(dx) < mpfr("1e-480"):
                break
        seq_c.append(x1)

    seq_c_rich = list(seq_c[4:])
    for p_ord in range(1, 7):
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
        f"Method 2 completed in {time.time() - t_m2:.2f}s: "
        f"|wynn_c[-1] - wynn_c[-2]| = {float(abs(c_inf_m2 - c_inf_m2_prev)):.3e}"
    )
    print(f"|Method 1 - Method 2| for c_inf = {float(diff_m1_m2):.3e}")

    r_inf_m1 = mpfr(1) + gmpy2.sqrt(mpfr(1) + mpfr(4) * c_inf_m1)
    r_inf_m2 = mpfr(1) + gmpy2.sqrt(mpfr(1) + mpfr(4) * c_inf_m2)
    diff_r = abs(r_inf_m1 - r_inf_m2)
    print(f"|Method 1 - Method 2| for r_inf = {float(diff_r):.3e}")

    conv_err = abs(c_inf_m1 - r_inf_m1 * (r_inf_m1 - mpfr(2)) / mpfr(4))
    print(f"Conversion check |c_inf - r_inf*(r_inf-2)/4| = {float(conv_err):.3e}")

    return {
        "c_inf_str_m1": f"{c_inf_m1:.420f}",
        "c_inf_str_m2": f"{c_inf_m2:.420f}",
        "r_inf_str_m1": f"{r_inf_m1:.420f}",
        "r_inf_str_m2": f"{r_inf_m2:.420f}",
        "diff_c_inf": float(diff_m1_m2),
        "diff_r_inf": float(diff_r),
        "conversion_error": float(conv_err),
        "superstable_c_m": [f"{x:.420f}" for x in seq_c[:30]],
        "renorm_tilde_mu_m": [f"{x:.420f}" for x in seq_mu[:30]],
    }


def main():
    os.makedirs("results", exist_ok=True)
    # 1. Solve p2 first (takes ~3 seconds in C-MPFR!)
    print("=== Solving Partial Win p2: Quartic (z=4) Feigenbaum alpha_4 & delta_4 to >= 1,050 Decimals ===")
    a4_s1, d4_s1, c4_1, b4_1 = solve_collocation_c(4, 1070, 3900, -1085.0, 1100)
    a4_s2, d4_s2, c4_2, b4_2 = solve_collocation_c(4, 1100, 3950, -1105.0, 1100)

    agree_a4 = count_agreeing_decimals(a4_s1, a4_s2)
    agree_d4 = count_agreeing_decimals(d4_s1, d4_s2)
    print(f"p2 Agreeing decimals (N1=1070 vs N2=1100): alpha_4 = {agree_a4}, delta_4 = {agree_d4}")

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

    # 2. Solve p1
    p1_res = solve_p1_accumulation_point()
    agree_c = count_agreeing_decimals(p1_res["c_inf_str_m1"], p1_res["c_inf_str_m2"])
    agree_r = count_agreeing_decimals(p1_res["r_inf_str_m1"], p1_res["r_inf_str_m2"])
    p1_res["agreeing_decimals_c_inf"] = agree_c
    p1_res["agreeing_decimals_r_inf"] = agree_r
    print(f"p1 Agreeing decimals: c_inf = {agree_c}, r_inf = {agree_r}")

    with open("results/feigenbaum_p1_accumulation.json", "w") as f:
        json.dump(p1_res, f, indent=2)

    print("Saved both p1 and p2 certificates in results/!")


if __name__ == "__main__":
    main()
