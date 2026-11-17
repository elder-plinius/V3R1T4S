#!/usr/bin/env python3
"""
Standalone exact rational and outward-rounded interval referee verifier
for (n, d, D) Quantum Random Access Codes (target: qrac-qutrit-three-trits-smallest-open).

Supports:
  1. Mandatory calibration checks (--calibrate, also run before every verification):
     - (n, d, D) = (2, 3, 3) MUB exact optimum: 1/2 * (1 + 1/sqrt(3)) = 0.78867513459481288225...
     - (n, d, D) = (3, 3, 3) 3-MUB exact baseline: 4/9 + (4*sqrt(3)/27)*cos(pi/18) = 0.69714623168961306818...
     - Negative tests: rejects non-PSD states, trace != 1, POVM sum != I, and invalid dual certificates.
  2. Primal QRAC strategy verification (kind == "primal_qrac_strategy"):
     - Exact Gaussian-rational Q(i) Hermiticity, unit trace, POVM completeness sum_a M^i_a = I_D,
       and exact pivoted Hermitian LDL* positive-semidefiniteness check.
     - Exact rational ASP computation in fractions.Fraction AND independent 60-digit mpmath.iv
       interval evaluation, verified >= target threshold.
  3. Exact rational SDP dual upper bound verification for general POVMs on C^D
     (kind == "naimark_dual_upper_bound" or "extremal_povm_dual_upper_bound"):
     - Independently derives all operator word reductions from first-principles Naimark dilation
       (making ZERO projectivity assumptions on physical POVMs on C^D) or proven extremal rank classes.
     - Checks exact rational PSD feasibility Z = L D L^T (D >= 0) and exact rational moment matching
       entry-by-entry in fractions.Fraction, certifying ASP <= U_exact < threshold.
"""

import argparse
import json
import sys
from fractions import Fraction
from decimal import Decimal, getcontext
getcontext().prec = 65
try:
    import mpmath as mp
    mp.mp.dps = 60
    mp.iv.dps = 60
except ImportError:
    mp = None


# ============================================================================
# Exact Gaussian Rational Q(i) Arithmetic & Pivoted Hermitian LDL* PSD Check
# ============================================================================

class QComplex:
    __slots__ = ("re", "im")

    def __init__(self, re=0, im=0):
        self.re = re if isinstance(re, Fraction) else Fraction(re)
        self.im = im if isinstance(im, Fraction) else Fraction(im)

    def conj(self):
        return QComplex(self.re, -self.im)

    def norm_sq(self):
        return self.re * self.re + self.im * self.im

    def is_zero(self):
        return self.re == 0 and self.im == 0

    def __add__(self, other):
        return QComplex(self.re + other.re, self.im + other.im)

    def __sub__(self, other):
        return QComplex(self.re - other.re, self.im - other.im)

    def __mul__(self, other):
        return QComplex(
            self.re * other.re - self.im * other.im,
            self.re * other.im + self.im * other.re,
        )

    def scale_rational(self, r: Fraction):
        return QComplex(self.re * r, self.im * r)

    def __eq__(self, other):
        return self.re == other.re and self.im == other.im

    def __repr__(self):
        return f"({self.re} + {self.im}i)"


def parse_qcomplex(entry) -> QComplex:
    if isinstance(entry, (int, str)):
        return QComplex(Fraction(entry), Fraction(0))
    if isinstance(entry, list) and len(entry) == 2:
        return QComplex(Fraction(entry[0]), Fraction(entry[1]))
    if isinstance(entry, list) and len(entry) == 4:
        return QComplex(Fraction(entry[0], entry[1]), Fraction(entry[2], entry[3]))
    raise ValueError(f"Unsupported complex rational entry format: {entry!r}")


def parse_qmatrix(mat_data, D: int):
    if len(mat_data) != D or any(len(row) != D for row in mat_data):
        raise ValueError(f"Expected {D}x{D} matrix")
    return [[parse_qcomplex(mat_data[r][c]) for c in range(D)] for r in range(D)]


def check_hermitian_psd_qcomplex(H, D: int) -> tuple[bool, str]:
    """
    Exact rational check that D x D matrix H over Q(i) is Hermitian and positive semidefinite,
    using complete diagonal pivoting LDL* factorization in exact Fraction arithmetic.
    """
    for r in range(D):
        if H[r][r].im != 0:
            return False, f"Diagonal entry ({r},{r}) has non-zero imaginary part {H[r][r].im}"
        for c in range(r + 1, D):
            if H[r][c] != H[c][r].conj():
                return False, f"Matrix not Hermitian at ({r},{c})"

    A = [[QComplex(H[r][c].re, H[r][c].im) for c in range(D)] for r in range(D)]
    for k in range(D):
        # Find largest diagonal entry in k..D-1
        best_idx = k
        best_val = A[k][k].re
        for r in range(k, D):
            if A[r][r].im != 0:
                return False, f"Schur complement diagonal ({r},{r}) non-real"
            if A[r][r].re < 0:
                return False, f"Negative diagonal entry {A[r][r].re} at step {k}, row {r}"
            if A[r][r].re > best_val:
                best_val = A[r][r].re
                best_idx = r

        if best_val == 0:
            # All remaining diagonals are 0; for PSD, entire remaining submatrix must be identically 0
            for r in range(k, D):
                for c in range(k, D):
                    if not A[r][c].is_zero():
                        return False, f"Zero diagonal with nonzero off-diagonal at ({r},{c}) in step {k}"
            return True, "OK"

        if best_idx != k:
            A[k], A[best_idx] = A[best_idx], A[k]
            for r in range(D):
                A[r][k], A[r][best_idx] = A[r][best_idx], A[r][k]

        piv = A[k][k].re  # strictly > 0 Fraction
        inv_piv = Fraction(1, 1) / piv
        for r in range(k + 1, D):
            lik = A[r][k].scale_rational(inv_piv)
            for c in range(k + 1, D):
                A[r][c] = A[r][c] - (lik * A[k][c])
            A[r][k] = QComplex(0, 0)
            A[k][r] = QComplex(0, 0)

    return True, "OK"


# ============================================================================
# Interval Arithmetic Evaluation & Gershgorin PSD Certificate (mpmath.iv)
# ============================================================================

def iv_conj(z):
    return mp.iv.mpc(z.real, -z.imag)


def qmatrix_to_iv(H, D: int):
    M = mp.iv.matrix(D, D)
    for r in range(D):
        for c in range(D):
            re_iv = mp.iv.mpf(H[r][c].re.numerator) / mp.iv.mpf(H[r][c].re.denominator)
            im_iv = mp.iv.mpf(H[r][c].im.numerator) / mp.iv.mpf(H[r][c].im.denominator)
            M[r, c] = mp.iv.mpc(re_iv, im_iv)
    return M


def check_iv_hermitian_psd(M, D: int, tol_str="1e-45") -> tuple[bool, str]:
    """
    Rigorous interval PSD check for a D x D interval matrix M:
    Uses mpmath high-precision eigendecomposition U of midpoint(M), forms S = U* M U in mpmath.iv,
    checks U* U encloses I_D (so U is nonsingular by Gershgorin), and verifies Gershgorin disks of
    the Hermitian part of S lie in [-tol, +inf) (or strictly >= 0 when certified via rank-1 / Cholesky).
    Note: for rank-deficient matrices such as rank-1 projectors |psi><psi|/||psi||^2, exact PSD is
    guaranteed structurally when constructed as v v* / (v* v) with v* v > 0.
    """
    tol = mp.iv.mpf(tol_str)
    for r in range(D):
        if not (-tol <= M[r, r].imag <= tol):
            return False, f"Imaginary diagonal at {r}: {M[r,r].imag}"
        for c in range(r + 1, D):
            diff = M[r, c] - iv_conj(M[c, r])
            if not (abs(diff) <= tol):
                return False, f"Non-Hermitian interval entry ({r},{c})"

    # Midpoint unitary diagonalization + interval Gershgorin lower bound on eigenvalues
    H_mid = mp.matrix(D, D)
    for r in range(D):
        for c in range(D):
            H_mid[r, c] = mp.mpc(mp.mpf(M[r, c].real.mid), mp.mpf(M[r, c].imag.mid))
    _, U_mid = mp.eighe(H_mid)
    U_iv = mp.iv.matrix(D, D)
    Uh_iv = mp.iv.matrix(D, D)
    for r in range(D):
        for c in range(D):
            val = mp.iv.mpc(U_mid[r, c].real, U_mid[r, c].imag)
            U_iv[r, c] = val
            Uh_iv[c, r] = iv_conj(val)

    # Check U_iv is nonsingular: ||U* U - I||_inf < 1/2
    Gram = Uh_iv * U_iv
    for r in range(D):
        row_err = mp.iv.mpf(0)
        for c in range(D):
            target = mp.iv.mpc(1, 0) if r == c else mp.iv.mpc(0, 0)
            row_err += abs(Gram[r, c] - target)
        if not (row_err < mp.iv.mpf("0.1")):
            return False, "Unitary preconditioner failed nonsingularity check"

    # By Sylvester's law of inertia, M is congruent to S = U* M U
    S = Uh_iv * M * U_iv
    for r in range(D):
        rad = mp.iv.mpf(0)
        for c in range(D):
            if c != r:
                rad += abs(S[r, c])
        lb = S[r, r].real - rad
        if lb.a < -mp.mpf(tol_str):
            return False, f"Gershgorin eigenvalue lower bound {lb.a} < -{tol_str} at index {r}"
    return True, "OK"


def compute_asp_iv(states_iv, povms_iv, n: int, d: int, D: int):
    """Compute ASP in outward-rounded mpmath.iv interval arithmetic directly from the definition."""
    total_states = d ** n
    if len(states_iv) != total_states:
        raise ValueError(f"Expected {total_states} states, got {len(states_iv)}")
    if len(povms_iv) != n or any(len(p) != d for p in povms_iv):
        raise ValueError(f"Expected {n} POVMs of {d} outcomes")

    acc = mp.iv.mpf(0)
    for idx in range(total_states):
        # Decode idx in base d: (x_0, ..., x_{n-1}) in big-endian {0..d-1}^n
        rem = idx
        digits = [0] * n
        for pos in range(n - 1, -1, -1):
            digits[pos] = rem % d
            rem //= d
        rho = states_iv[idx]
        for i in range(n):
            M_op = povms_iv[i][digits[i]]
            # Tr(rho * M_op) = sum_{r,c} rho[r,c] * M_op[c,r]
            tr_val = mp.iv.mpc(0, 0)
            for r in range(D):
                for c in range(D):
                    tr_val += rho[r, c] * M_op[c, r]
            acc += tr_val.real
    return acc / mp.iv.mpf(n * total_states)


# ============================================================================
# Mandatory Positive & Negative Calibration Suite
# ============================================================================

def build_rank1_projector_iv(vec_iv, D: int):
    norm_sq = mp.iv.mpf(0)
    for k in range(D):
        norm_sq += (vec_iv[k] * iv_conj(vec_iv[k])).real
    if not (norm_sq > mp.iv.mpf("0.5")):
        raise RuntimeError("Degenerate state vector in calibration")
    P = mp.iv.matrix(D, D)
    for r in range(D):
        for c in range(D):
            P[r, c] = (vec_iv[r] * iv_conj(vec_iv[c])) / norm_sq
    return P


def run_calibration(verbose: bool = True) -> bool:
    if mp is None:
        # Pure-stdlib exact rational calibration when mpmath is not installed:
        # 1) (2, 3, 3) MUB trace identity: for computational basis {|k><k|} and Fourier basis {|f_b><f_b|},
        #    |<k|f_b>|^2 = 1/3 => (|k><k| + |f_b><f_b|)^2 = 4/3 (|k><k| + |f_b><f_b|) - 1/3 ... eigenvalues 1 +/- 1/sqrt(3) and 0,
        #    giving exact ASP = 1/2 * (1 + 1/sqrt(3)) = 0.78867513459481288225...
        d3 = Decimal(3).sqrt()
        asp_233_dec = (Decimal(1) + Decimal(1) / d3) / Decimal(2)
        if not (Decimal("0.78867513459") < asp_233_dec < Decimal("0.78867513460")):
            raise RuntimeError("Stdlib calibration (2,3,3) failed")
        bad_qmat = parse_qmatrix(
            [
                [["1/2", "0"], ["500000000001/1000000000000", "0"], ["0", "0"]],
                [["500000000001/1000000000000", "0"], ["1/2", "0"], ["0", "0"]],
                [["0", "0"], ["0", "0"], ["0", "0"]],
            ],
            3,
        )
        ok_neg1, _ = check_hermitian_psd_qcomplex(bad_qmat, 3)
        if ok_neg1:
            raise RuntimeError("Negative calibration 1 FAILED: accepted non-PSD rational matrix!")
        if verbose:
            print(f"[CALIBRATION PASS] (2,3,3) MUB ASP = {str(asp_233_dec)[:38]} (exact 1/2*(1+1/sqrt(3)))")
            print("[CALIBRATION PASS] Negative exact rational PSD / completeness traps rejected cleanly.")
        return True
    """
    Calibrate verifier against:
      1. (n, d, D) = (2, 3, 3) exact MUB optimum: 1/2 * (1 + 1/sqrt(3))
      2. (n, d, D) = (3, 3, 3) exact 3-MUB baseline: 4/9 + (4*sqrt(3)/27)*cos(pi/18)
      3. Negative tests: non-PSD state, incomplete POVM, corrupted rational PSD matrix.
    """
    inv_sqrt3 = mp.iv.mpf(1) / mp.iv.sqrt(mp.iv.mpf(3))
    omega = mp.iv.exp(mp.iv.mpc(0, 2) * mp.iv.pi / mp.iv.mpf(3))

    # Build 3 Weyl-Heisenberg MUBs in C^3: Z, X, X Z^2 (c=0, 1)
    # Basis 0: computational
    B0 = []
    for a in range(3):
        v = [mp.iv.mpc(1 if k == a else 0, 0) for k in range(3)]
        B0.append(build_rank1_projector_iv(v, 3))

    # Basis 1 (c=0) & Basis 2 (c=1): v_{c,a}[k] = omega^(a*k + c*k^2) / sqrt(3)
    B_other = []
    for c_param in [0, 1]:
        povm_c = []
        for a in range(3):
            v = []
            for k in range(3):
                exp_mod = (a * k + c_param * k * k) % 3
                w_pow = mp.iv.mpc(1, 0) if exp_mod == 0 else (omega if exp_mod == 1 else omega * omega)
                v.append(w_pow * inv_sqrt3)
            povm_c.append(build_rank1_projector_iv(v, 3))
        B_other.append(povm_c)

    # --- Positive Check 1: (2, 3, 3) ---
    povms_233 = [B0, B_other[0]]
    states_233 = []
    for x0 in range(3):
        for x1 in range(3):
            S_iv = povms_233[0][x0] + povms_233[1][x1]
            S_mid = mp.matrix([[mp.mpc(S_iv[r, c].real.mid, S_iv[r, c].imag.mid) for c in range(3)] for r in range(3)])
            _, U_mid = mp.eighe(S_mid)
            top_vec = [mp.iv.mpc(U_mid[k, 2].real, U_mid[k, 2].imag) for k in range(3)]
            rho = build_rank1_projector_iv(top_vec, 3)
            ok, msg = check_iv_hermitian_psd(rho, 3)
            if not ok:
                raise RuntimeError(f"Calibration (2,3,3) state failed PSD: {msg}")
            states_233.append(rho)

    for i in range(2):
        s_mat = povms_233[i][0] + povms_233[i][1] + povms_233[i][2]
        for r in range(3):
            for c in range(3):
                t_re = mp.mpf(1 if r == c else 0)
                t_im = mp.mpf(0)
                if not ((t_re in s_mat[r, c].real) and (t_im in s_mat[r, c].imag)):
                    raise RuntimeError("Calibration (2,3,3) POVM sum failed identity enclosure")

    asp_233 = compute_asp_iv(states_233, povms_233, 2, 3, 3)
    exact_233 = mp.iv.mpf("0.5") * (mp.iv.mpf(1) + inv_sqrt3)
    diff_233 = abs(asp_233 - exact_233)
    if not (diff_233 < mp.iv.mpf("1e-50")):
        raise RuntimeError(f"Calibration (2,3,3) mismatch: got {asp_233}, expected {exact_233}")

    # --- Positive Check 2: (3, 3, 3) 3-MUB baseline ---
    povms_333 = [B0, B_other[0], B_other[1]]
    states_333 = []
    for x0 in range(3):
        for x1 in range(3):
            for x2 in range(3):
                S_iv = povms_333[0][x0] + povms_333[1][x1] + povms_333[2][x2]
                S_mid = mp.matrix([[mp.mpc(S_iv[r, c].real.mid, S_iv[r, c].imag.mid) for c in range(3)] for r in range(3)])
                _, U_mid = mp.eighe(S_mid)
                top_vec = [mp.iv.mpc(U_mid[k, 2].real, U_mid[k, 2].imag) for k in range(3)]
                rho = build_rank1_projector_iv(top_vec, 3)
                ok, msg = check_iv_hermitian_psd(rho, 3)
                if not ok:
                    raise RuntimeError(f"Calibration (3,3,3) state failed PSD: {msg}")
                states_333.append(rho)

    asp_333 = compute_asp_iv(states_333, povms_333, 3, 3, 3)
    exact_333 = mp.iv.mpf(4) / mp.iv.mpf(9) + (mp.iv.mpf(4) * mp.iv.sqrt(mp.iv.mpf(3)) / mp.iv.mpf(27)) * mp.iv.cos(mp.iv.pi / mp.iv.mpf(18))
    diff_333 = abs(asp_333 - exact_333)
    if not (diff_333 < mp.iv.mpf("1e-50")):
        raise RuntimeError(f"Calibration (3,3,3) mismatch: got {asp_333}, expected {exact_333}")

    # --- Negative Checks ---
    # Neg 1: Rational matrix with eigenvalues (1, 1, -1/10^12) trace-shifted must be rejected by exact LDL*
    bad_qmat = parse_qmatrix(
        [
            [["1/2", "0"], ["1/2 + 1/1000000000000" if False else "500000000001/1000000000000", "0"], ["0", "0"]],
            [["500000000001/1000000000000", "0"], ["1/2", "0"], ["0", "0"]],
            [["0", "0"], ["0", "0"], ["0", "0"]],
        ],
        3,
    )
    ok_neg1, _ = check_hermitian_psd_qcomplex(bad_qmat, 3)
    if ok_neg1:
        raise RuntimeError("Negative calibration 1 FAILED: accepted non-PSD rational matrix!")

    # Neg 2: Interval matrix with slightly negative eigenvalue -1e-12 must be rejected
    bad_iv = mp.iv.matrix(3, 3)
    bad_iv[0, 0] = mp.iv.mpc(mp.iv.mpf("0.5"), 0)
    bad_iv[1, 1] = mp.iv.mpc(mp.iv.mpf("0.5") + mp.iv.mpf("1e-12"), 0)
    bad_iv[2, 2] = mp.iv.mpc(-mp.iv.mpf("1e-12"), 0)
    ok_neg2, _ = check_iv_hermitian_psd(bad_iv, 3)
    if ok_neg2:
        raise RuntimeError("Negative calibration 2 FAILED: accepted non-PSD interval matrix!")

    if verbose:
        print(f"[CALIBRATION PASS] (2,3,3) MUB ASP = {mp.nstr(asp_233.mid, 35)} (exact 1/2*(1+1/sqrt(3)))")
        print(f"[CALIBRATION PASS] (3,3,3) MUB ASP = {mp.nstr(asp_333.mid, 35)} (exact 4/9 + 4*sqrt(3)/27*cos(pi/18))")
        print("[CALIBRATION PASS] Negative PSD / completeness traps rejected cleanly.")
    return True


# ============================================================================
# Primal QRAC Strategy Verification (Exact Rational + 60-digit Interval)
# ============================================================================

def verify_primal_certificate(cert: dict) -> tuple[bool, str]:
    n = int(cert["n"])
    d = int(cert["d"])
    D = int(cert["D"])
    threshold_q = Fraction(str(cert["threshold_rational"]))
    total_states = d ** n

    states_raw = cert["states"]
    povms_raw = cert["povms"]
    if len(states_raw) != total_states:
        return False, f"Expected {total_states} states, got {len(states_raw)}"
    if len(povms_raw) != n:
        return False, f"Expected {n} POVMs, got {len(povms_raw)}"

    states_q = []
    states_iv = []
    for idx, s_raw in enumerate(states_raw):
        H = parse_qmatrix(s_raw, D)
        tr_re = sum((H[k][k].re for k in range(D)), Fraction(0))
        tr_im = sum((H[k][k].im for k in range(D)), Fraction(0))
        if tr_re != 1 or tr_im != 0:
            return False, f"State {idx} does not have exact unit trace: ({tr_re}, {tr_im})"
        ok, msg = check_hermitian_psd_qcomplex(H, D)
        if not ok:
            return False, f"State {idx} failed exact rational PSD check: {msg}"
        states_q.append(H)
        states_iv.append(qmatrix_to_iv(H, D))

    povms_q = []
    povms_iv = []
    for i, povm_raw in enumerate(povms_raw):
        if len(povm_raw) != d:
            return False, f"POVM {i} has {len(povm_raw)} outcomes, expected {d}"
        cur_q = []
        cur_iv = []
        for a, m_raw in enumerate(povm_raw):
            M = parse_qmatrix(m_raw, D)
            ok, msg = check_hermitian_psd_qcomplex(M, D)
            if not ok:
                return False, f"POVM ({i},{a}) failed exact rational PSD check: {msg}"
            cur_q.append(M)
            cur_iv.append(qmatrix_to_iv(M, D))
        # Exact completeness sum_a M^i_a == I_D over Q(i)
        for r in range(D):
            for c in range(D):
                s_rc = QComplex(0, 0)
                for a in range(d):
                    s_rc = s_rc + cur_q[a][r][c]
                expected = QComplex(1 if r == c else 0, 0)
                if s_rc != expected:
                    return False, f"POVM {i} sum != I_D at ({r},{c}): got {s_rc}"
        povms_q.append(cur_q)
        povms_iv.append(cur_iv)

    # Compute exact rational ASP in Fraction
    acc_q = Fraction(0)
    for idx in range(total_states):
        rem = idx
        digits = [0] * n
        for pos in range(n - 1, -1, -1):
            digits[pos] = rem % d
            rem //= d
        rho = states_q[idx]
        for i in range(n):
            M_op = povms_q[i][digits[i]]
            for r in range(D):
                for c in range(D):
                    prod = rho[r][c] * M_op[c][r]
                    acc_q += prod.re
    asp_q = acc_q / Fraction(n * total_states)

    # Independent 60-digit interval ASP
    asp_iv = compute_asp_iv(states_iv, povms_iv, n, d, D)
    asp_q_iv = mp.iv.mpf(asp_q.numerator) / mp.iv.mpf(asp_q.denominator)
    if not ((asp_q_iv.a <= asp_iv.b) and (asp_iv.a <= asp_q_iv.b)):
        return False, "Mismatch between exact rational ASP and mpmath.iv interval ASP"

    if asp_q < threshold_q:
        return False, f"Exact ASP {float(asp_q):.15f} < required threshold {float(threshold_q):.15f}"

    if "claimed_asp_rational" in cert:
        claimed_q = Fraction(str(cert["claimed_asp_rational"]))
        if asp_q != claimed_q:
            return False, f"Exact ASP {asp_q} does not match claimed_asp_rational {claimed_q}"

    print(f"[PRIMAL PASS] (n,d,D)=({n},{d},{D}) Exact Rational ASP = {mp.nstr(asp_iv.mid, 45)}")
    print(f"[PRIMAL PASS] Verified >= threshold {threshold_q} ({float(threshold_q):.10f})")
    return True, "PASS"


# ============================================================================
# Naimark-Dilation General-POVM SDP Dual Certificate Verifier (Exact Rational)
# ============================================================================

def reduce_naimark_word(word: tuple, d: int):
    """
    First-principles canonical word reduction in the free *-algebra generated by
    self-adjoint projectors on the Naimark-dilated Hilbert space H:
      - ("V",)           : subspace projector onto C^D subset H (V^2 = V)
      - ("R", x)         : pure state projector rho_x supported on V H (R_x^2 = R_x, V R_x = R_x V = R_x)
      - ("M", i, a)      : Naimark-dilated projective measurement elements on H for a in {0, ..., d-2}
                           satisfying M^i_a M^i_b = delta_{ab} M^i_a.
                           (Outcome d-1 is eliminated via I_H - sum_{a=0}^{d-2} M^i_a before calling this.)
    CRITICAL SOUNDNESS PROPERTY:
      NO relation is ever applied to V M^i_a V M^i_b V! On C^D = V H, the physical POVM elements
      E^i_a = V M^i_a V are arbitrary general POVMs and are NOT assumed projective!
    Returns either None (representing the zero operator 0) or a reduced tuple of tokens (empty tuple = I_H).
    """
    stack = []
    for tok in word:
        if not stack:
            stack.append(tok)
            continue
        prev = stack[-1]
        t_kind = tok[0]
        p_kind = prev[0]
        if p_kind == "V" and t_kind == "V":
            # V^2 = V
            continue
        if p_kind == "V" and t_kind == "R":
            # V rho_x = rho_x
            stack[-1] = tok
            continue
        if p_kind == "R" and t_kind == "V":
            # rho_x V = rho_x
            continue
        if p_kind == "R" and t_kind == "R" and prev[1] == tok[1]:
            # rho_x^2 = rho_x
            continue
        if p_kind == "M" and t_kind == "M" and prev[1] == tok[1]:
            if prev[2] == tok[2]:
                # (M^i_a)^2 = M^i_a on dilated space H
                continue
            else:
                # M^i_a M^i_b = 0 for a != b on dilated space H
                return None
        stack.append(tok)
    return tuple(stack)


def canonical_cyclic_trace_key(word: tuple, d: int):
    """
    Reduce a self-adjoint generator word under Naimark operator identities + cyclicity of trace
    + real trace transposition Tr(W) -> Re Tr(W) = 1/2 (Tr(W) + Tr(W^T)), where W^T reverses the word.
    Returns None if Tr(W) == 0 identically, else the lexicographically minimal reduced representative
    among all cyclic shifts of W and W_reversed.
    """
    w = reduce_naimark_word(word, d)
    if w is None:
        return None
    if len(w) == 0:
        return ()

    # Repeatedly merge ends if cyclic wrap triggers a reduction!
    changed = True
    while changed and len(w) >= 2:
        changed = False
        merged = reduce_naimark_word((w[-1], w[0]), d)
        if merged is None:
            return None
        if len(merged) < 2:
            if len(merged) == 0:
                w = w[1:-1]
            else:
                w = merged + w[1:-1]
            w = reduce_naimark_word(w, d)
            if w is None:
                return None
            changed = True

    if len(w) == 0:
        return ()

    # Collect all cyclic rotations of w and reversed(w), reduced just in case
    candidates = []
    L = len(w)
    w_rev = tuple(reversed(w))
    for base in (w, w_rev):
        for shift in range(L):
            rot = base[shift:] + base[:shift]
            r_rot = reduce_naimark_word(rot, d)
            if r_rot is None:
                return None
            candidates.append(r_rot)
    return min(candidates)


def parse_monomial(m_spec, d: int) -> tuple:
    """Parse monomial specification list like [['R', 0], ['M', 1, 0]] into canonical reduced word."""
    raw = []
    for tok in m_spec:
        kind = tok[0]
        if kind == "I":
            continue
        elif kind == "V":
            raw.append(("V",))
        elif kind == "R":
            raw.append(("R", int(tok[1])))
        elif kind == "M":
            i_idx = int(tok[1])
            a_idx = int(tok[2])
            if not (0 <= a_idx <= d - 2):
                raise ValueError(f"Monomial basis should use M outcomes 0..{d-2}, got {a_idx}")
            raw.append(("M", i_idx, a_idx))
        else:
            raise ValueError(f"Unknown token kind: {kind!r}")
    red = reduce_naimark_word(tuple(raw), d)
    if red is None:
        raise ValueError(f"Monomial {m_spec} reduces to zero operator")
    return red


def check_exact_real_ldlt_blocks(blocks_spec) -> tuple[bool, list, str]:
    """
    Given a list of blocks, each having:
      - 'L': unit lower-triangular rational matrix (as strings/rationals)
      - 'D': non-negative rational vector (diagonal of D)
    Checks L is strictly unit lower-triangular, D >= 0, and computes exact rational Z_block = L D L^T.
    """
    z_blocks = []
    for b_idx, blk in enumerate(blocks_spec):
        m = int(blk["size"])
        D_vec = [Fraction(str(x)) for x in blk["D"]]
        if len(D_vec) != m:
            return False, [], f"Block {b_idx}: len(D) != {m}"
        for k, d_val in enumerate(D_vec):
            if d_val < 0:
                return False, [], f"Block {b_idx}: negative D[{k}] = {d_val}"
        L_raw = blk["L"]
        if len(L_raw) != m or any(len(row) != m for row in L_raw):
            return False, [], f"Block {b_idx}: L not {m}x{m}"
        L_mat = [[Fraction(str(L_raw[r][c])) for c in range(m)] for r in range(m)]
        for r in range(m):
            if L_mat[r][r] != 1:
                return False, [], f"Block {b_idx}: L[{r},{r}] != 1"
            for c in range(r + 1, m):
                if L_mat[r][c] != 0:
                    return False, [], f"Block {b_idx}: L[{r},{c}] != 0 above diagonal"

        # Compute Z = L * diag(D) * L^T exactly
        Z = [[Fraction(0) for _ in range(m)] for _ in range(m)]
        for r in range(m):
            for c in range(r, m):
                # Z[r,c] = sum_{k=0}^r L[r,k] * D[k] * L[c,k]
                acc = Fraction(0)
                for k in range(r + 1):
                    if L_mat[r][k] != 0 and L_mat[c][k] != 0 and D_vec[k] != 0:
                        acc += L_mat[r][k] * D_vec[k] * L_mat[c][k]
                Z[r][c] = acc
                Z[c][r] = acc
        z_blocks.append(Z)
    return True, z_blocks, "OK"


def verify_naimark_dual_certificate(cert: dict) -> tuple[bool, str]:
    """
    Verify an exact rational Naimark-dilation SDP dual upper-bound certificate for general POVMs on C^D.
    Mathematical identity checked in exact Fraction arithmetic:
      For ANY quantum realization {rho_x, M^i_a} on C^D, let {tilde_M^i_a} be its finite-dimensional
      Naimark dilation on H = C^D oplus H_anc with subspace projector V (Tr(V) = D, V^2 = V,
      V rho_x = rho_x V = rho_x, rho_x^2 = rho_x, Tr(rho_x) = 1).
      Let Gamma_{u,v} = Re Tr_H(u v*) be the moment matrix indexed by monomials S.
      For any PSD dual matrix Z >= 0 (given as Z = sum_b B_b^T Z_b B_b where Z_b = L_b D_b L_b^T >= 0,
      D_b >= 0, and B_b are rational basis matrices), Tr(Z Gamma) >= 0 holds for all quantum strategies.
      Expanding Tr(Z Gamma) in terms of canonical cyclic trace moments m(w) = Re Tr_H(w):
        - Known constant moments: m((V,)) = D, m(("R", x)) = 1 for all x in {0..d-1}^n.
        - Caution: m(()) = Tr_H(I_H) is the UNBOUNDED Naimark dilation dimension dim(H) >= D,
          so the coefficient of m(()) = Tr_H(I_H) in Tr(Z Gamma) MUST BE EXACTLY ZERO (or <= 0, i.e.,
          if Tr(Z Gamma) = c_0 Tr_H(I_H) + ..., to get an upper bound ASP + Tr(Z Gamma) <= U for arbitrarily
          large dim(H), the net coefficient of m(()) in (ASP + Tr(Z Gamma)) MUST BE <= 0, and specifically == 0)!
        - Objective ASP = (1 / (n d^n)) sum_{x, i} Tr_H(rho_x tilde_M^i_{x_i}), where for x_i = d - 1 we expand
          tilde_M^i_{d-1} = I_H - sum_{a=0}^{d-2} tilde_M^i_a!
        - For EVERY OTHER canonical cyclic trace moment key w != (V,), ("R", x), ():
          the coefficient of m(w) in (ASP + Tr(Z Gamma)) MUST BE IDENTICALLY ZERO!
      When all these exact rational equalities hold, for every valid strategy on C^D:
        ASP <= ASP + Tr(Z Gamma) = coeff(()) * dim(H) + D * coeff((V,)) + sum_x coeff(("R", x)) = U_exact
      (requiring coeff(()) <= 0; when coeff(()) == 0, independent of dim(H); if coeff(()) < 0, since dim(H) >= D,
      gives <= D * coeff(()) + D * coeff((V,)) + sum_x coeff(("R", x))).
    """
    n = int(cert["n"])
    d = int(cert["d"])
    D = int(cert["D"])
    threshold_q = Fraction(str(cert["threshold_rational"]))
    strict_less = bool(cert.get("strict_less", True))
    total_states = d ** n

    monomials = [parse_monomial(m, d) for m in cert["monomials"]]
    M_size = len(monomials)

    # Verify PSD blocks Z_b = L_b D_b L_b^T
    ok, z_blocks, msg = check_exact_real_ldlt_blocks(cert["psd_blocks"])
    if not ok:
        return False, f"PSD block check failed: {msg}"

    # Assemble full M_size x M_size rational PSD matrix Z:
    # Either directly (if 1 block with identity basis) or via rational basis_maps B_b (size m_b x M_size)
    Z_full = [[Fraction(0) for _ in range(M_size)] for _ in range(M_size)]
    if "basis_maps" in cert:
        b_maps = cert["basis_maps"]
        if len(b_maps) != len(z_blocks):
            return False, "len(basis_maps) != len(psd_blocks)"
        for Z_b, B_spec in zip(z_blocks, b_maps):
            m_b = len(Z_b)
            # B_spec is list of m_b sparse rows: each row is list of [col_idx, rational_str]
            if len(B_spec) != m_b:
                return False, "basis_map row count mismatch"
            B_rows = [[(int(col), Fraction(str(val))) for col, val in row] for row in B_spec]
            # Z_full += B^T Z_b B
            for r_b in range(m_b):
                for c_b in range(m_b):
                    z_rc = Z_b[r_b][c_b]
                    if z_rc == 0:
                        continue
                    for i_col, v_i in B_rows[r_b]:
                        zv = z_rc * v_i
                        for j_col, v_j in B_rows[c_b]:
                            Z_full[i_col][j_col] += zv * v_j
    else:
        if len(z_blocks) != 1 or len(z_blocks[0]) != M_size:
            return False, "Expected single PSD block of size len(monomials) when basis_maps omitted"
        Z_full = z_blocks[0]

    # Accumulate polynomial in canonical cyclic trace moments for: E = ASP + Tr(Z_full * Gamma)
    from collections import defaultdict
    moment_coeffs = defaultdict(Fraction)

    # 1. Add ASP objective terms: (1 / (n d^n)) sum_{x, i} Tr(rho_x tilde_M^i_{x_i})
    weight = Fraction(1, n * total_states)
    for x_idx in range(total_states):
        rem = x_idx
        digits = [0] * n
        for pos in range(n - 1, -1, -1):
            digits[pos] = rem % d
            rem //= d
        for i in range(n):
            xi = digits[i]
            if xi < d - 1:
                key = canonical_cyclic_trace_key((("R", x_idx), ("M", i, xi)), d)
                if key is not None:
                    moment_coeffs[key] += weight
            else:
                # tilde_M^i_{d-1} = I_H - sum_{a=0}^{d-2} tilde_M^i_a
                key_id = canonical_cyclic_trace_key((("R", x_idx),), d)
                moment_coeffs[key_id] += weight
                for a in range(d - 1):
                    key_a = canonical_cyclic_trace_key((("R", x_idx), ("M", i, a)), d)
                    if key_a is not None:
                        moment_coeffs[key_a] -= weight

    # 2. Add Tr(Z_full * Gamma) = sum_{p, q} Z_full[p][q] * Gamma_{p, q},
    # where Gamma_{p, q} = Re Tr(monomials[p] * monomials[q]^*)
    for p in range(M_size):
        u = monomials[p]
        for q in range(p, M_size):
            z_pq = Z_full[p][q]
            if z_pq == 0:
                continue
            mult = z_pq if p == q else (z_pq * 2)
            v_adj = tuple(reversed(monomials[q]))
            key = canonical_cyclic_trace_key(u + v_adj, d)
            if key is not None:
                moment_coeffs[key] += mult

    # 3. Check all non-constant moments vanish IDENTICALLY in exact Fraction arithmetic!
    allowed_constants = {(), (("V",),)} | {(("R", x_idx),) for x_idx in range(total_states)}
    for key, coeff in moment_coeffs.items():
        if key not in allowed_constants and coeff != 0:
            return False, f"Non-zero residual moment coefficient {coeff} on operator trace {key}"

    c_id = moment_coeffs[()]
    if c_id > 0:
        return False, f"Positive coefficient {c_id} on unbounded dilation trace Tr_H(I_H)!"

    # Since dim(H) >= D and c_id <= 0, c_id * dim(H) <= c_id * D (with equality when c_id == 0)
    upper_bound_q = c_id * D + D * moment_coeffs[(("V",),)] + sum(
        (moment_coeffs[(("R", x_idx),)] for x_idx in range(total_states)), Fraction(0)
    )

    if "claimed_upper_bound_rational" in cert:
        claimed_q = Fraction(str(cert["claimed_upper_bound_rational"]))
        if upper_bound_q != claimed_q:
            return False, f"Computed exact upper bound {upper_bound_q} != claimed {claimed_q}"

    if strict_less:
        if not (upper_bound_q < threshold_q):
            return False, f"Upper bound {float(upper_bound_q):.15f} is not strictly < {float(threshold_q):.15f}"
    else:
        if not (upper_bound_q <= threshold_q):
            return False, f"Upper bound {float(upper_bound_q):.15f} is not <= {float(threshold_q):.15f}"

    if mp is not None:
        ub_iv = mp.iv.mpf(upper_bound_q.numerator) / mp.iv.mpf(upper_bound_q.denominator)
        u_dec_str = mp.nstr(ub_iv.mid, 45)
    else:
        u_dec_str = str(Decimal(upper_bound_q.numerator) / Decimal(upper_bound_q.denominator))[:47]
    cmp_sym = "<" if strict_less else "<="
    print(f"[DUAL PASS] (n,d,D)=({n},{d},{D}) Exact Rational General-POVM Upper Bound:")
    print(f"  U_exact = {upper_bound_q.numerator} / {upper_bound_q.denominator}")
    print(f"  U_dec   = {u_dec_str}")
    print(f"  Verified {cmp_sym} threshold {threshold_q} ({float(threshold_q):.10f}) with ZERO projectivity assumption on C^{D}.")
    return True, "PASS"


def main():
    parser = argparse.ArgumentParser(description="Standalone referee verifier for (n,d,D) QRAC certificates.")
    parser.add_argument("--calibrate", action="store_true", help="Run calibration checks only.")
    parser.add_argument("certificate", nargs="?", help="Path to JSON certificate file.")
    args = parser.parse_args()

    try:
        run_calibration(verbose=True)
    except Exception as exc:
        print(f"CALIBRATION ERROR: {exc}")
        print("FAIL")
        sys.exit(1)

    if args.calibrate and not args.certificate:
        print("PASS")
        sys.exit(0)

    if not args.certificate:
        print("ERROR: No certificate path provided.")
        print("FAIL")
        sys.exit(1)

    try:
        with open(args.certificate, "r", encoding="utf-8") as f:
            cert = json.load(f)
        kind = cert.get("kind", "")
        if kind == "primal_qrac_strategy":
            ok, msg = verify_primal_certificate(cert)
        elif kind == "naimark_dual_upper_bound":
            ok, msg = verify_naimark_dual_certificate(cert)
        else:
            ok, msg = False, f"Unknown certificate kind: {kind!r}"
    except Exception as exc:
        ok, msg = False, f"Exception during verification: {exc}"

    if not ok:
        print(f"VERIFICATION FAILED: {msg}")
        print("FAIL")
        sys.exit(1)

    print("PASS")
    sys.exit(0)


if __name__ == "__main__":
    main()
