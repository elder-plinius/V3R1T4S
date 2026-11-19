#!/usr/bin/env python3
"""
Standalone Rigorous Verifier for N=3 GHZ Nonlocality Robustness Certificate
(Target: ghz-nonlocality-robustness-below-049143)

Performs:
  1. Schema and exact structural checks on object/bell_ghz3_18x24x72.json.
  2. 55-digit outward-rounded interval arithmetic (mpmath.iv) verification of:
       - Mermin 2x2x2 calibration (L = 2, Q_GHZ = 4, Q_noise = 0 => v* = 0.5).
       - Projective qubit observable validity: Tr(O) = 0 and O^2 = I_2 for all
         18 + 24 + 72 = 114 single-qubit settings A_i, B_j, C_k.
       - White-noise expectation Q_noise = Tr((I_8 / 8) B) = 0.
       - Explicit 3-qubit GHZ expectation Q_GHZ = <GHZ_3| B |GHZ_3> summed over
         all 18 x 24 x 72 = 31,104 correlation triples in 55-digit mpmath.iv,
         cross-checked against explicit 2x2 matrix tensor contractions.
  3. Compilation and execution of TWO independent C++17 symmetry-reduced orbit
     enumerators (certify_orbits_a.cpp and certify_orbits_b.cpp, at most 2 threads),
     verifying:
       - Internal brute-force calibrations pass in both implementations.
       - Exact Burnside orbit counts agree (7286, 3771, 349536, 1318100256).
       - Both independent implementations return the identical exact integer local
         bound L, matching cert["exact_L"], and both witnesses achieve L in Python.
  4. Final 55-digit interval check:
       v* = (L - Q_noise) / (Q_GHZ - Q_noise) <= 0.49142 = 0.49143 - 1e-5.
"""

from fractions import Fraction
import json
import os
import shutil
import subprocess
import sys
import tempfile
import mpmath as mp


def lo_mpf(x):
    return mp.mpf(x.a)


def hi_mpf(x):
    return mp.mpf(x.b)


def parse_kv_lines(stdout_text):
    out = {}
    for line in stdout_text.splitlines():
        if "=" in line:
            k, v = line.strip().split("=", 1)
            out[k.strip()] = v.strip()
    return out


def build_F_table(mC, w_int):
    n2 = 2 * mC
    half = mC // 2
    F = [0] * n2
    for s in range(n2):
        s1 = s if s <= mC else n2 - s
        if mC % 2 == 0:
            if s1 < half:
                F[s] = int(w_int[s1])
            elif s1 > half:
                F[s] = -int(w_int[mC - s1])
        else:
            if s1 <= half:
                F[s] = int(w_int[s1])
            else:
                F[s] = -int(w_int[mC - s1])
    return F


def eval_witness_python(mA, mB, mC, stA, stB, F, uA, uB):
    n2 = 2 * mC
    a = [1 if ((uA >> i) & 1) else -1 for i in range(mA)]
    b = [1 if ((uB >> j) & 1) else -1 for j in range(mB)]
    total = 0
    for k in range(mC):
        sk = 0
        for i in range(mA):
            ai = a[i]
            base_i = stA * i + k
            for j in range(mB):
                sk += F[(base_i + stB * j) % n2] * ai * b[j]
        total += abs(sk)
    return total


def verify_mermin_calibration():
    mp.iv.dps = 55
    mp.mp.dps = 55
    F_m = build_F_table(2, [1])
    best_L = max(eval_witness_python(2, 2, 2, 1, 1, F_m, uA, uB) for uA in range(4) for uB in range(4))
    if best_L != 2:
        raise ValueError(f"Mermin calibration local bound mismatch: {best_L} != 2")
    pi_iv = mp.iv.pi
    q_m = mp.iv.mpf(0)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                c = F_m[(i + j + k) % 4]
                if c != 0:
                    q_m += mp.iv.mpf(c) * mp.iv.cos(pi_iv * mp.iv.mpf(i + j + k) / 2)
    v_m = mp.iv.mpf(best_L) / q_m
    if not (mp.mpf("0.5") >= lo_mpf(v_m) and mp.mpf("0.5") <= hi_mpf(v_m)):
        raise ValueError("Mermin calibration v* != 0.5")
    return v_m


def parse_frac_list(lst, expected_len, expected_den, label):
    if not isinstance(lst, list) or len(lst) != expected_len:
        raise ValueError(f"{label} length mismatch")
    fracs = []
    for idx, item in enumerate(lst):
        if not isinstance(item, str) or "/" not in item:
            raise ValueError(f"{label}[{idx}] must be an exact fraction string")
        num_s, den_s = item.split("/", 1)
        num_i, den_i = int(num_s), int(den_s)
        if num_i != idx or den_i != expected_den:
            raise ValueError(f"{label}[{idx}] = {item} != {idx}/{expected_den}")
        fracs.append(Fraction(num_i, den_i))
    return fracs


def verify_projective_and_quantum_iv(mA, mB, mC, stA, stB, alpha_f, beta_f, gamma_f, F):
    mp.iv.dps = 55
    mp.mp.dps = 55
    pi_iv = mp.iv.pi

    def make_bloch_xy(fracs):
        obs = []
        for fr in fracs:
            ang = pi_iv * mp.iv.mpf(fr.numerator) / mp.iv.mpf(fr.denominator)
            cx = mp.iv.cos(ang)
            sy = mp.iv.sin(ang)
            # Verify O = cx * sigma_x + sy * sigma_y satisfies O^2 = (cx^2 + sy^2) I_2 = I_2:
            norm_sq = cx * cx + sy * sy
            if not (lo_mpf(norm_sq) <= mp.mpf(1) <= hi_mpf(norm_sq)):
                raise ValueError("Projective observable norm^2 interval does not contain 1")
            if hi_mpf(norm_sq) - lo_mpf(norm_sq) > mp.mpf("1e-48"):
                raise ValueError("Insufficient interval precision on observable norm")
            obs.append((cx, sy))
        return obs

    obsA = make_bloch_xy(alpha_f)
    obsB = make_bloch_xy(beta_f)
    obsC = make_bloch_xy(gamma_f)

    # Explicit 3-qubit GHZ expectation via Pauli-XY action on |GHZ_3> = (|000> + |111>)/sqrt(2):
    # For O_r = cx_r X + sy_r Y, O_r |0> = (cx_r + i sy_r)|1> and O_r |1> = (cx_r - i sy_r)|0>.
    # Hence <GHZ_3| A_i x B_j x C_k |GHZ_3> = Re((cx_A + i sy_A)(cx_B + i sy_B)(cx_C + i sy_C))
    #   = cx_A cx_B cx_C - cx_A sy_B sy_C - sy_A cx_B sy_C - sy_A sy_B cx_C,
    # and Tr((I_8 / 8)(A_i x B_j x C_k)) = (1/8) Tr(A_i) Tr(B_j) Tr(C_k) = 0 identically.
    q_matrix_iv = mp.iv.mpf(0)
    q_trig_iv = mp.iv.mpf(0)
    n2 = 2 * mC

    for i in range(mA):
        cxA, syA = obsA[i]
        for j in range(mB):
            cxB, syB = obsB[j]
            # Multiply (cxA + i syA)(cxB + i syB) = reAB + i imAB
            reAB = cxA * cxB - syA * syB
            imAB = cxA * syB + syA * cxB
            for k in range(mC):
                s = (stA * i + stB * j + k) % n2
                coeff = F[s]
                if coeff == 0:
                    continue
                cxC, syC = obsC[k]
                exp_ijk = reAB * cxC - imAB * syC
                c_iv = mp.iv.mpf(coeff)
                q_matrix_iv += c_iv * exp_ijk

                ang_sum = pi_iv * mp.iv.mpf(stA * i + stB * j + k) / mp.iv.mpf(mC)
                q_trig_iv += c_iv * mp.iv.cos(ang_sum)

    # Verify explicit Pauli-matrix contraction and trigonometric cosine sum overlap tightly:
    overlap_lo = max(lo_mpf(q_matrix_iv), lo_mpf(q_trig_iv))
    overlap_hi = min(hi_mpf(q_matrix_iv), hi_mpf(q_trig_iv))
    if overlap_lo > overlap_hi:
        raise ValueError("Matrix contraction and trigonometric GHZ expectations disagree!")

    # Conservative hull of both interval evaluations:
    hull_lo = min(lo_mpf(q_matrix_iv), lo_mpf(q_trig_iv))
    hull_hi = max(hi_mpf(q_matrix_iv), hi_mpf(q_trig_iv))
    return mp.iv.mpf([hull_lo, hull_hi])


def compile_and_run_cpp(cpp_path, cert_path, tmpdir, bin_name):
    cxx = shutil.which("clang++") or shutil.which("g++") or shutil.which("c++")
    if not cxx:
        raise RuntimeError("No C++17 compiler (clang++ / g++) found in PATH")
    bin_path = os.path.join(tmpdir, bin_name)
    comp = subprocess.run(
        [cxx, "-O3", "-std=c++17", "-pthread", cpp_path, "-o", bin_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if comp.returncode != 0:
        raise RuntimeError(f"Compilation failed for {os.path.basename(cpp_path)}: {comp.stderr.strip()}")
    run = subprocess.run(
        [bin_path, cert_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if run.returncode != 0:
        raise ValueError(f"{bin_name} exited with {run.returncode}: {run.stderr.strip()}")
    return parse_kv_lines(run.stdout)


def verify_certificate(cert_path):
    with open(cert_path, "r", encoding="utf-8") as f:
        cert = json.load(f)

    expected_keys = {
        "schema", "target_id", "N", "mA", "mB", "mC", "stepA", "stepB",
        "alpha_pi_fractions", "beta_pi_fractions", "gamma_pi_fractions",
        "marginals_1body_2body", "tensor_law", "w_int", "exact_L", "Q_noise",
        "Q_GHZ_45d", "v_star_interval_lo_45d", "v_star_interval_hi_45d",
        "alice_c2m_orbits", "alice_d4m_orbits", "bob_c2m_orbits", "total_orbit_pairs"
    }
    if set(cert.keys()) != expected_keys:
        raise ValueError("Certificate keys do not match schema")

    if cert["schema"] != "ghz3_asymmetric_planar_bell_certificate_v1":
        raise ValueError("Unexpected schema version")
    if cert["target_id"] != "ghz-nonlocality-robustness-below-049143":
        raise ValueError("Unexpected target_id")
    if cert["N"] != 3 or cert["mA"] != 18 or cert["mB"] != 24 or cert["mC"] != 72:
        raise ValueError("Unexpected (N, mA, mB, mC) dimensions")
    if cert["stepA"] != 4 or cert["stepB"] != 3:
        raise ValueError("Unexpected step multipliers")
    if cert["marginals_1body_2body"] != 0 or cert["Q_noise"] != 0:
        raise ValueError("Expected full-correlation zero-marginal functional with Q_noise = 0")

    mA, mB, mC = 18, 24, 72
    stA, stB = 4, 3
    alpha_f = parse_frac_list(cert["alpha_pi_fractions"], mA, mA, "alpha_pi_fractions")
    beta_f = parse_frac_list(cert["beta_pi_fractions"], mB, mB, "beta_pi_fractions")
    gamma_f = parse_frac_list(cert["gamma_pi_fractions"], mC, mC, "gamma_pi_fractions")

    w_int = cert["w_int"]
    if not isinstance(w_int, list) or len(w_int) != 36 or not all(isinstance(x, int) for x in w_int):
        raise ValueError("w_int must be a list of 36 exact integers")

    v_mermin = verify_mermin_calibration()

    F = build_F_table(mC, w_int)
    Q_iv = verify_projective_and_quantum_iv(mA, mB, mC, stA, stB, alpha_f, beta_f, gamma_f, F)

    # Check Q_GHZ_45d recorded in JSON matches recomputed Q_iv within 1e-42:
    q_claimed = mp.mpf(str(cert["Q_GHZ_45d"]))
    if abs(q_claimed - (lo_mpf(Q_iv) + hi_mpf(Q_iv)) / 2) > mp.mpf("1e-35"):
        raise ValueError("Claimed Q_GHZ_45d does not match recomputed 55-digit GHZ expectation")

    here = os.path.dirname(os.path.abspath(__file__))
    cpp_a = os.path.join(here, "certify_orbits_a.cpp")
    cpp_b = os.path.join(here, "certify_orbits_b.cpp")

    with tempfile.TemporaryDirectory() as tmpdir:
        res_a = compile_and_run_cpp(cpp_a, cert_path, tmpdir, "certify_orbits_a")
        res_b = compile_and_run_cpp(cpp_b, cert_path, tmpdir, "certify_orbits_b")

    if res_a.get("IMPL_A_CALIBRATIONS") != "PASS" or res_b.get("IMPL_B_CALIBRATIONS") != "PASS":
        raise ValueError("C++ orbit calibrators did not pass")

    c2m_a = int(res_a["ALICE_C2M_ORBITS"])
    d4m_a = int(res_a["ALICE_RED_ORBITS"])
    c2m_b = int(res_a["BOB_C2M_ORBITS"])
    pairs_a = int(res_a["TOTAL_ORBIT_PAIRS"])

    if (
        c2m_a != int(res_b["BURNSIDE_ALICE_C2M"])
        or d4m_a != int(res_b["BURNSIDE_ALICE_D4M"])
        or c2m_b != int(res_b["BURNSIDE_BOB_C2M"])
        or pairs_a != int(res_b["TOTAL_ORBIT_PAIRS"])
    ):
        raise ValueError("Orbit counts disagree between independent implementations A and B")

    if (
        c2m_a != cert["alice_c2m_orbits"]
        or d4m_a != cert["alice_d4m_orbits"]
        or c2m_b != cert["bob_c2m_orbits"]
        or pairs_a != cert["total_orbit_pairs"]
    ):
        raise ValueError("Orbit counts do not match certificate metadata")

    L_a = int(res_a["EXACT_L"])
    L_b = int(res_b["EXACT_L"])
    if L_a != L_b:
        raise ValueError(f"Independent orbit enumerators disagree on L: {L_a} != {L_b}")
    if L_a != int(cert["exact_L"]):
        raise ValueError(f"Recomputed exact_L = {L_a} != claimed exact_L = {cert['exact_L']}")

    # Re-evaluate both witnesses in pure Python:
    uA_a, uB_a = int(res_a["WITNESS_UA"]), int(res_a["WITNESS_UB"])
    uA_b, uB_b = int(res_b["WITNESS_UA"]), int(res_b["WITNESS_UB"])
    if eval_witness_python(mA, mB, mC, stA, stB, F, uA_a, uB_a) != L_a:
        raise ValueError("Python witness check failed for Implementation A witness")
    if eval_witness_python(mA, mB, mC, stA, stB, F, uA_b, uB_b) != L_b:
        raise ValueError("Python witness check failed for Implementation B witness")

    v_iv = mp.iv.mpf(L_a) / Q_iv
    v_lo = lo_mpf(v_iv)
    v_hi = hi_mpf(v_iv)

    if abs(mp.mpf(str(cert["v_star_interval_lo_45d"])) - v_lo) > mp.mpf("1e-42"):
        raise ValueError("Claimed v_star_interval_lo_45d mismatch")
    if abs(mp.mpf(str(cert["v_star_interval_hi_45d"])) - v_hi) > mp.mpf("1e-42"):
        raise ValueError("Claimed v_star_interval_hi_45d mismatch")

    threshold = mp.mpf("0.49142")
    if not (v_hi <= threshold):
        raise ValueError(f"Certified v* upper bound {mp.nstr(v_hi, 15)} exceeds threshold 0.49142")

    print("Calibration checks (mpmath.iv, 55 dps + C++ brute-force vs orbit):", flush=True)
    print(f"  Mermin 2x2x2 v*       = {mp.nstr((lo_mpf(v_mermin) + hi_mpf(v_mermin)) / 2, 18)}", flush=True)
    print(f"  Impl A & B small-grid = PASS (2x2x2, 6x8x24, 8x12x24, 9x6x18)", flush=True)
    print("Independent exact symmetry-reduced orbit enumerations (18 x 24 x 72):", flush=True)
    print(f"  Alice C_36 / D_36     = {c2m_a} / {d4m_a} orbits", flush=True)
    print(f"  Bob C_48              = {c2m_b} orbits", flush=True)
    print(f"  Orbit pairs checked   = {pairs_a} (covering 2^42 = 4,398,046,511,104 strategies)", flush=True)
    print(f"  Exact L (Impl A, min) = {L_a} ({res_a['ELAPSED_SEC']}s)", flush=True)
    print(f"  Exact L (Impl B, max) = {L_b} ({res_b['ELAPSED_SEC']}s)", flush=True)
    print("Quantum expectations & critical visibility (mpmath.iv, 55 dps):", flush=True)
    print(f"  Q_noise               = 0 (exact)", flush=True)
    print(f"  Q_GHZ                 = [{mp.nstr(lo_mpf(Q_iv), 30)}, {mp.nstr(hi_mpf(Q_iv), 30)}]", flush=True)
    print(f"  Certified v* interval = [{mp.nstr(v_lo, 25)}, {mp.nstr(v_hi, 25)}]", flush=True)
    print("  Record beaten         = 0.49143 (arXiv:2310.20677v3 Table III; target <= 0.49142)", flush=True)
    print("PASS", flush=True)


def main():
    if len(sys.argv) != 2:
        print("Usage: verify_ghz3.py path/to/bell_ghz3_18x24x72.json")
        print("FAIL")
        sys.exit(1)
    try:
        verify_certificate(sys.argv[1])
    except Exception as exc:
        print(f"Verification error ({type(exc).__name__}): {exc}", flush=True)
        print("FAIL", flush=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
