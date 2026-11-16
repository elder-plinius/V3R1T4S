#!/usr/bin/env python3
"""Formalist lens audit for IEANTN node ZetaHadamard.v1.

Pure Python standard-library numerical & structural verification of:
1. Statement audit of `ZetaHadamard.v1.logDeriv_partial_fractions`:
   - Residue signs of g(z) = -logDeriv(zeta_1)(z) * (1/(s-z) - 1/(w-z)) on a finite
     rectangle R = [-5, 4] x [-20, 20] via high-order Gauss-Legendre contour integration.
2. Trivial-zero Gauss digamma identity:
   sum_{k>=0} (1/(s + 2(k+1)) - 1/(w + 2(k+1))) = -(digamma(s/2 + 1) - digamma(w/2 + 1)) / 2.
3. Critical-strip zero sum verification across the 3 `Conclusions.lean` benchmark points
   (imaginary-part sharp test where w - s is real) plus a general complex pair (s, w).
4. Verification of the 4-step periodic Bernoulli Euler-Maclaurin analytic continuation
   formula for riemannZeta_0(s) on Re(s) > -3 against standard high-order Euler-Maclaurin.
"""
import cmath
import math
import sys

EULER_GAMMA = 0.5772156649015328606065120900824024310421


def digamma_complex(z: complex) -> complex:
    """High-accuracy complex digamma via recurrence + asymptotic Bernoulli expansion."""
    acc = 0j
    cur = complex(z)
    while cur.real < 14.0 or abs(cur) < 14.0:
        acc -= 1.0 / cur
        cur += 1.0
    inv2 = 1.0 / (cur * cur)
    # psi(z) ~ log(z) - 1/(2z) - sum B_{2k}/(2k z^{2k})
    b_coeffs = [
        -1.0 / 12.0,
        1.0 / 120.0,
        -1.0 / 252.0,
        1.0 / 240.0,
        -1.0 / 132.0,
        691.0 / 32760.0,
        -1.0 / 12.0,
        3617.0 / 8160.0,
    ]
    poly = 0j
    p = inv2
    for c in b_coeffs:
        poly += c * p
        p *= inv2
    return acc + cmath.log(cur) - 0.5 / cur + poly


def zeta_and_deriv(s: complex, N: int = 120) -> tuple:
    """High-accuracy zeta(s) and zeta'(s) via 8-term Euler-Maclaurin on Re(s) > -5, s != 1."""
    s = complex(s)
    # f(x) = x^{-s}
    total = 0j
    for n in range(1, N):
        total += cmath.exp(-s * math.log(n))
    nN = float(N)
    N_ms = cmath.exp(-s * math.log(nN))
    total += 0.5 * N_ms + (nN * N_ms) / (s - 1.0)
    # Bernoulli B_2, B_4, ..., B_14
    bernoulli = [
        (2, 1.0 / 6.0),
        (4, -1.0 / 30.0),
        (6, 1.0 / 42.0),
        (8, -1.0 / 30.0),
        (10, 5.0 / 66.0),
        (12, -691.0 / 2730.0),
        (14, 7.0 / 6.0),
    ]
    poch = s
    fact = 2.0
    for idx, (k, bk) in enumerate(bernoulli):
        if idx > 0:
            poch = poch * (s + (k - 3)) * (s + (k - 2))
            fact *= (k - 1) * k
        total += (bk / fact) * poch * N_ms * (nN ** (1 - k))

    # Analytic termwise derivative of Euler-Maclaurin:
    dtotal = 0j
    for n in range(1, N):
        ln_n = math.log(n)
        dtotal -= ln_n * cmath.exp(-s * ln_n)
    lnN = math.log(nN)
    dN_ms = -lnN * N_ms
    dtotal += 0.5 * dN_ms + (nN * dN_ms * (s - 1.0) - nN * N_ms) / ((s - 1.0) ** 2)
    poch = s
    dpoch = 1.0 + 0j
    fact = 2.0
    for idx, (k, bk) in enumerate(bernoulli):
        if idx > 0:
            a = s + (k - 3)
            b = s + (k - 2)
            dpoch = dpoch * (a * b) + poch * (a + b)
            poch = poch * a * b
            fact *= (k - 1) * k
        scale = (bk / fact) * (nN ** (1 - k))
        dtotal += scale * (dpoch * N_ms + poch * dN_ms)
    return total, dtotal


def logderiv_zeta(z: complex) -> complex:
    """Exact logDeriv(zeta)(z) = zeta'(z)/zeta(z) across all C \\ ({1} U zeros),
    using Euler-Maclaurin on Re(z) >= 0 and logDeriv_riemannZeta_one_sub on Re(z) < 0
    to avoid IEEE-754 float64 cancellation at negative real parts.
    """
    z = complex(z)
    if z.real >= 0.0:
        zv, dzv = zeta_and_deriv(z, N=120)
        return dzv / zv
    w = 1.0 - z
    zw, dzw = zeta_and_deriv(w, N=120)
    # logDeriv zeta (1 - w) = -logDeriv zeta w + log(2*pi) - digamma(w) + (pi/2)*tan(pi*w/2)
    return (
        -(dzw / zw)
        + math.log(2.0 * math.pi)
        - digamma_complex(w)
        + 0.5 * math.pi * cmath.tan(0.5 * math.pi * w)
    )


def zeta1_and_logderiv(z: complex) -> tuple:
    """F(z) = -zeta_1'(z)/zeta_1(z) = -(zeta'(z)/zeta(z) + 1/(z - 1))."""
    if abs(z - 1.0) < 1e-6:
        return 1.0 + 0j, -EULER_GAMMA + 0j
    F = -(logderiv_zeta(z) + 1.0 / (z - 1.0))
    return 0j, F


def log_gamma_stirling(z: complex) -> complex:
    acc = 0j
    cur = complex(z)
    while cur.real < 12.0 or abs(cur) < 12.0:
        acc -= cmath.log(cur)
        cur += 1.0
    inv2 = 1.0 / (cur * cur)
    b = [1.0 / 12.0, -1.0 / 360.0, 1.0 / 1260.0, -1.0 / 1680.0, 1.0 / 1188.0]
    poly = 0j
    p = 1.0 / cur
    for c in b:
        poly += c * p
        p *= inv2
    return acc + (cur - 0.5) * cmath.log(cur) - cur + 0.5 * math.log(2.0 * math.pi) + poly


def hardy_Z(t: float) -> float:
    s = 0.5 + 1j * t
    zv, _ = zeta_and_deriv(s, N=90)
    lg = log_gamma_stirling(0.25 + 0.5j * t)
    theta = lg.imag - 0.5 * t * math.log(math.pi)
    return (cmath.exp(1j * theta) * zv).real


def find_critical_zeros(count: int = 80) -> list:
    """Locate the first `count` positive ordinates gamma_n of zeta(1/2 + i*gamma_n) = 0."""
    zeros = []
    t = 10.0
    dt = 0.15
    prev_t = t
    prev_z = hardy_Z(t)
    while len(zeros) < count:
        t += dt
        cur_z = hardy_Z(t)
        if prev_z * cur_z <= 0.0:
            a, b = prev_t, t
            fa, fb = prev_z, cur_z
            for _ in range(60):
                m = 0.5 * (a + b)
                fm = hardy_Z(m)
                if abs(fm) < 1e-14 or abs(b - a) < 1e-13:
                    a = b = m
                    break
                if fa * fm <= 0.0:
                    b, fb = m, fm
                else:
                    a, fa = m, fm
            root = 0.5 * (a + b)
            z_root = 0.5 + 1j * root
            for _ in range(4):
                zv, dzv = zeta_and_deriv(z_root, N=120)
                z_root -= zv / dzv
            zeros.append(z_root.imag)
        prev_t, prev_z = t, cur_z
    return zeros


def gauss_legendre_16():
    # 8-point Gauss-Legendre on [-1, 1] replicated on subintervals for simple exactness
    nodes = [
        -0.96028985649753623,
        -0.79666647741362674,
        -0.52553240991632899,
        -0.18343464249564980,
        0.18343464249564980,
        0.52553240991632899,
        0.79666647741362674,
        0.96028985649753623,
    ]
    weights = [
        0.10122853629037626,
        0.22238103445337447,
        0.31370664587788729,
        0.36268378337836198,
        0.36268378337836198,
        0.31370664587788729,
        0.22238103445337447,
        0.10122853629037626,
    ]
    return nodes, weights


def integrate_segment(func, z0: complex, z1: complex, panels: int = 80) -> complex:
    nodes, weights = gauss_legendre_16()
    total = 0j
    dz = (z1 - z0) / panels
    for k in range(panels):
        a = z0 + k * dz
        b = a + dz
        mid = 0.5 * (a + b)
        half = 0.5 * (b - a)
        seg = 0j
        for x, w in zip(nodes, weights):
            seg += w * func(mid + half * x)
        total += half * seg
    return total


def p4_periodic(t: float) -> float:
    u = t - math.floor(t)
    return (u ** 4) / 24.0 - (u ** 3) / 12.0 + (u ** 2) / 24.0 - 1.0 / 720.0


def zeta_via_p4_continuation(s: complex, M: int = 80) -> complex:
    """Verify the 4-step periodic P_4 analytic continuation formula on Re(s) > -3, s != 1:
    zeta(s) = 1/(s-1) + 1/2 + s/12 - s(s+1)(s+2)/720
              - s(s+1)(s+2)(s+3) * int_1^infty P_4(t) t^{-s-4} dt.
    """
    nodes, weights = gauss_legendre_16()
    integral = 0j
    for n in range(1, M):
        # integrate on [n, n+1] where P_4 is a smooth quartic polynomial!
        sub = 8 if n < 16 else 1
        step = 1.0 / sub
        for j in range(sub):
            a = n + j * step
            mid = a + 0.5 * step
            half = 0.5 * step
            seg = 0j
            for x, w in zip(nodes, weights):
                t = mid + half * x
                seg += w * p4_periodic(t) * cmath.exp(-(s + 4.0) * math.log(t))
            integral += half * seg
    poch4 = s * (s + 1.0) * (s + 2.0) * (s + 3.0)
    poch3 = s * (s + 1.0) * (s + 2.0)
    return 1.0 / (s - 1.0) + 0.5 + s / 12.0 - poch3 / 720.0 - poch4 * integral


def main() -> None:
    print("=== Formalist Lens Audit: IEANTN ZetaHadamard.v1 ===")

    # 1. Verify P_4 periodic Euler-Maclaurin analytic continuation on Re(s) > -3
    print("\n[Test 1] Periodic P_4 Euler-Maclaurin continuation on Re(s) > -3:")
    for s_test in [2.3 + 1.5j, 0.4 + 3.0j, -1.2 + 2.5j, -2.4 + 1.0j]:
        z_ref, _ = zeta_and_deriv(s_test)
        z_p4 = zeta_via_p4_continuation(s_test, M=120)
        err = abs(z_ref - z_p4)
        poch4 = s_test * (s_test + 1.0) * (s_test + 2.0) * (s_test + 3.0)
        tail_bound = abs(poch4) / (720.0 * (s_test.real + 3.0) * (120.0 ** (s_test.real + 3.0)))
        print("  s = %14s | |zeta_ref - zeta_P4| = %.3e (tail bound %.3e)" % (str(s_test), err, tail_bound))
        assert err <= 1.05 * tail_bound + 1e-12, "P_4 continuation mismatch at %s: %e" % (s_test, err)

    # 2. Verify Gauss digamma trivial-zero sum identity
    print("\n[Test 2] Trivial-zero Gauss digamma series identity:")
    for s_val, w_val in [(0.3 + 5j, 1.5 + 5j), (-3.0 + 2j, 1.5 + 2j), (0.25 + 7j, 2.1 - 3j)]:
        K = 20000
        part = 0j
        for k in range(K):
            tau = -2.0 * (k + 1)
            part += 1.0 / (s_val - tau) - 1.0 / (w_val - tau)
        # Euler-Maclaurin tail from k=K to infty of (s - w) / ((2k+2+s)(2k+2+w)) ~ (s-w)/(4*K)
        tail = (w_val - s_val) / (4.0 * K)  # wait: 1/(s+2k+2) - 1/(w+2k+2) = (w - s)/((s+2k+2)(w+2k+2))
        lhs = part + tail
        rhs = -0.5 * (digamma_complex(0.5 * s_val + 1.0) - digamma_complex(0.5 * w_val + 1.0))
        err = abs(lhs - rhs)
        print("  s=%s, w=%s | |sum_trivial - (-1/2 delta_digamma)| = %.3e" % (s_val, w_val, err))
        assert err < 1e-7, "Trivial-zero digamma sign/factor mismatch!"

    # 3. Finite-rectangle Cauchy residue audit on R = [-5, 4] x [-20, 20]
    print("\n[Test 3] Finite-contour Cauchy residue theorem sign audit on [-5, 4] x [-20, 20]:")
    gammas = find_critical_zeros(80)
    print("  Located %d conjugate pairs of critical-line zeros: gamma_1=%.9f ... gamma_80=%.9f" % (
        len(gammas), gammas[0], gammas[-1]
    ))
    assert abs(gammas[0] - 14.1347251417) < 1e-8
    assert abs(gammas[1] - 21.0220396388) < 1e-8

    s0 = 0.3 + 5.0j
    w0 = 1.5 + 5.0j

    def integrand(z: complex) -> complex:
        _, Fz = zeta1_and_logderiv(z)
        return Fz * (1.0 / (s0 - z) - 1.0 / (w0 - z))

    c_bl, c_br, c_tr, c_tl = -5.0 - 20.0j, 4.0 - 20.0j, 4.0 + 20.0j, -5.0 + 20.0j
    contour = (
        integrate_segment(integrand, c_bl, c_br, panels=120)
        + integrate_segment(integrand, c_br, c_tr, panels=160)
        + integrate_segment(integrand, c_tr, c_tl, panels=120)
        + integrate_segment(integrand, c_tl, c_bl, panels=160)
    ) / (2.0j * math.pi)

    # Exact sum of residues inside [-5, 4] x [-20, 20]:
    # Poles of g(z) = F(z)*(1/(s0-z) - 1/(w0-z)) inside R:
    # - z = s0: Res(1/(s0-z)) = -1 => -F(s0) = zeta'/zeta(s0) + 1/(s0 - 1)
    # - z = w0: Res(-1/(w0-z)) = +1 => +F(w0) = -(zeta'/zeta(w0) + 1/(w0 - 1))
    # - trivial zeros inside (-5, 4): tau_0 = -2, tau_1 = -4, where Res(F, tau) = -1:
    #   sum_{tau in {-2, -4}} (-1)*(1/(s0 - tau) - 1/(w0 - tau))
    # - non-trivial zeros inside (-20, 20): 0.5 +- i*gamma_1 (since gamma_1=14.1347 < 20 < gamma_2=21.022):
    #   sum_{rho} (-m(rho))*(1/(s0 - rho) - 1/(w0 - rho))
    _, Fs0 = zeta1_and_logderiv(s0)
    _, Fw0 = zeta1_and_logderiv(w0)
    res_expected = (-Fs0) + Fw0
    for tau in (-2.0, -4.0):
        res_expected -= 1.0 / (s0 - tau) - 1.0 / (w0 - tau)
    for g in gammas:
        if g < 20.0:
            for rho in (0.5 + 1j * g, 0.5 - 1j * g):
                res_expected -= 1.0 / (s0 - rho) - 1.0 / (w0 - rho)

    contour_err = abs(contour - res_expected)
    print("  (1/2pi i) oint_R g(z) dz = %.12f %+.12fj" % (contour.real, contour.imag))
    print("  Exact residue sum in R   = %.12f %+.12fj" % (res_expected.real, res_expected.imag))
    print("  |contour - residues|     = %.3e" % contour_err)
    assert contour_err < 1e-9, "Contour residue sign mismatch!"

    # 4. Full partial-fraction statement audit across benchmark points
    print("\n[Test 4] Statement sign audit of ZetaHadamard.v1.logDeriv_partial_fractions (80 zero pairs):")
    benchmarks = [
        ("Conclusions.lean #1", 0.3 + 5.0j, 1.5 + 5.0j, True),
        ("Conclusions.lean #2", -3.0 + 2.0j, 1.5 + 2.0j, True),
        ("Conclusions.lean #3", 0.5 + 30.0j, 1.5 + 30.0j, True),
        ("General off-line pair", 0.25 + 7.0j, 2.1 - 3.0j, False),
    ]
    for label, s_pt, w_pt, real_diff in benchmarks:
        rhs = (
            (logderiv_zeta(s_pt) - logderiv_zeta(w_pt))
            + 0.5 * (digamma_complex(0.5 * s_pt + 1.0) - digamma_complex(0.5 * w_pt + 1.0))
            + 1.0 / (s_pt - 1.0)
            - 1.0 / (w_pt - 1.0)
        )
        partial = 0j
        for g in gammas:
            for rho in (0.5 + 1j * g, 0.5 - 1j * g):
                partial += 1.0 / (s_pt - rho) - 1.0 / (w_pt - rho)
        diff = rhs - partial
        T_cut = 0.5 * (gammas[-1] + 203.0)
        rvm_tail = -((w_pt - s_pt) / math.pi) * (math.log(T_cut / (2.0 * math.pi)) + 1.0) / T_cut
        print("  %-22s | |RHS - S_80| = %.4e | |RHS - S_80 - RvM_tail| = %.4e | |Im(RHS - S_80)| = %.4e" % (
            label, abs(diff), abs(diff - rvm_tail), abs(diff.imag)
        ))
        assert abs(diff - rvm_tail) < 1e-3, "RvM tail-corrected partial sum mismatch!"
        if real_diff:
            assert abs(diff.imag) < 2e-5, "Imaginary-part cancellation failed — sign bug!"

    print("\nALL FORMALIST SIGN, RESIDUE, AND CONTINUATION AUDITS PASSED.")


if __name__ == "__main__":
    main()
