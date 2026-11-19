#!/usr/bin/env python3
"""
Standalone zero-dependency exact rational verifier for the closed MinT cell
(t=3, m=11, s=19) in base 3 via the Martin-Stinson / Bierbrauer linear-programming
bound on the embedded ordered orthogonal array OOA(3^11, 19, S_3, T=4, k=8).

Uses ONLY the Python standard library (fractions, json, math, sys).
"""
import json
import math
import sys
from fractions import Fraction


def enum_compositions_fixed_len(total, length):
    """Yield all tuples of `length` non-negative integers summing to `total`."""
    if length == 1:
        yield (total,)
        return
    for first in range(total + 1):
        for tail in enum_compositions_fixed_len(total - first, length - 1):
            yield (first,) + tail


def univariate_krawtchouk(deg, a_val, b_val, base):
    """
    Exact integer univariate Krawtchouk value:
      K_deg(a_val, b_val) = sum_{j=0}^{deg} (-1)^j (base - 1)^{deg - j} C(a_val, j) C(b_val, deg - j)
    for non-negative integers a_val, b_val.
    """
    if b_val < 0 or a_val + b_val < deg:
        return 0
    bm1 = base - 1
    acc = 0
    lo = max(0, deg - b_val)
    hi = min(deg, a_val)
    for j in range(lo, hi + 1):
        term = math.comb(a_val, j) * math.comb(b_val, deg - j) * (bm1 ** (deg - j))
        if j % 2 == 1:
            acc -= term
        else:
            acc += term
    return acc


def multivariate_krawtchouk(f_tup, x_tup, base, depth):
    """
    Exact integer multivariate Krawtchouk kernel K_f(X) on the ordered Hamming / NRT scheme
    (Martin & Stinson 1999; Bierbrauer 2007; MinT desc_OBoundLP.html):
      K_f(X) = base^{|f| - ||f||} * prod_{i=1}^{T} K_{f_i}(X_{i-1}, X_i + sum_{j=i+1}^{T} (X_j - f_j))
    where |f| = sum_{i=1}^T i*f_i, ||f|| = sum_{i=1}^T f_i, and
    X = (X_0, ..., X_{T-1}, X_T) counts coordinates first differing at digit 1..T, with X_T = equal coords.
    """
    size_f = sum(i * f_tup[i] for i in range(1, depth + 1))
    breadth_f = sum(f_tup[1:])
    if breadth_f == 0:
        return 1
    prod = 1
    suffix_diff = 0
    for i in range(depth, 0, -1):
        fi = f_tup[i]
        a_arg = x_tup[i - 1]
        b_arg = x_tup[i] + suffix_diff
        if b_arg < 0 or a_arg + b_arg < fi:
            return 0
        if fi > 0:
            kv = univariate_krawtchouk(fi, a_arg, b_arg, base)
            if kv == 0:
                return 0
            prod *= kv
        suffix_diff += x_tup[i] - fi
    return (base ** (size_f - breadth_f)) * prod


def run_soundness_calibrations():
    """
    Positive controls verifying the kernel identities directly on explicit nets in base 2 and base 3:
      sum_{x, y in A} K_f(type(x, y)) == 0   for 1 <= |f| <= k
      sum_{x, y in A} K_f(type(x, y)) >= 0   for |f| >= k + 1
    """
    # 1. Base-3 digital (0, 2, 4)-net (Latin hypercube / OA(9, 4, 3, 2) lifted to T=2, k=2):
    # M = 9 points in (Z_3^2)^4:
    pts3 = []
    for u0 in range(3):
        for u1 in range(3):
            c0 = (u0, u1)
            c1 = (u1, u0)
            c2 = ((u0 + u1) % 3, (u0 + 2 * u1) % 3)
            c3 = ((u0 + 2 * u1) % 3, (u0 + u1) % 3)
            pts3.append((c0, c1, c2, c3))
    types3 = list(enum_compositions_fixed_len(4, 3))
    dist3 = {t: 0 for t in types3}
    for x in pts3:
        for y in pts3:
            cnt = [0, 0, 0]
            for c in range(4):
                if x[c][0] != y[c][0]:
                    cnt[0] += 1
                elif x[c][1] != y[c][1]:
                    cnt[1] += 1
                else:
                    cnt[2] += 1
            dist3[tuple(cnt)] += 1
    for f in types3:
        sz = f[1] + 2 * f[2]
        tot = sum(dist3[X] * multivariate_krawtchouk(f, X, 3, 2) for X in types3)
        if 1 <= sz <= 2:
            if tot != 0:
                raise AssertionError(f"Base-3 calibration failed zero check at {f}: {tot}")
        elif tot < 0:
            raise AssertionError(f"Base-3 calibration failed PSD check at {f}: {tot}")

    # 2. Base-2 digital (1, 3, 4)-net (M = 8, s = 4, T = 2, k = 2):
    pts2 = []
    for u0 in (0, 1):
        for u1 in (0, 1):
            for u2 in (0, 1):
                pts2.append(((u0, u1), (u1, u2), (u2, u0), (u0 ^ u1 ^ u2, u0 ^ u1)))
    types2 = list(enum_compositions_fixed_len(4, 3))
    dist2 = {t: 0 for t in types2}
    for x in pts2:
        for y in pts2:
            cnt = [0, 0, 0]
            for c in range(4):
                if x[c][0] != y[c][0]:
                    cnt[0] += 1
                elif x[c][1] != y[c][1]:
                    cnt[1] += 1
                else:
                    cnt[2] += 1
            dist2[tuple(cnt)] += 1
    for f in types2:
        sz = f[1] + 2 * f[2]
        tot = sum(dist2[X] * multivariate_krawtchouk(f, X, 2, 2) for X in types2)
        if 1 <= sz <= 2:
            if tot != 0:
                raise AssertionError(f"Base-2 calibration failed zero check at {f}: {tot}")
        elif tot < 0:
            raise AssertionError(f"Base-2 calibration failed PSD check at {f}: {tot}")


def verify_certificate_dict(cert):
    """Return (ok: bool, msg: str) checking all LP dual certificate conditions in exact Fraction arithmetic."""
    cell = cert["cell"]
    ooa = cert["embedded_ooa"]
    b = int(cell["b"])
    t = int(cell["t"])
    m = int(cell["m"])
    s = int(cell["s"])
    k = m - t
    T = int(ooa["T"])
    M_target = b ** m

    if b != 3 or t != 3 or m != 11 or s != 19:
        return False, f"Unexpected target cell {(t, m, s)} base {b}"
    if int(ooa["k"]) != k or int(ooa["M_target"]) != M_target or int(ooa["s"]) != s or int(ooa["b"]) != b:
        return False, "Mismatch in embedded OOA parameters"
    if T < 1 or T > k:
        return False, f"Invalid truncation depth T={T} for strength k={k}"

    L = int(cert["common_denominator_L"])
    if L <= 0:
        return False, "Invalid common_denominator_L"

    zero_f = tuple([s] + [0] * T)
    seen_f = set()
    weights = []
    for entry in cert["dual_weights_u"]:
        f = tuple(int(v) for v in entry["f"])
        if len(f) != T + 1 or any(v < 0 for v in f) or sum(f) != s:
            return False, f"Invalid type tuple {f}"
        if f == zero_f or f in seen_f:
            return False, f"Duplicate or zero dual type {f}"
        seen_f.add(f)
        sz = sum(i * f[i] for i in range(1, T + 1))
        if sz != int(entry["size"]):
            return False, f"Size mismatch on {f}"
        num = int(entry["u_num"])
        den = int(entry["u_den"])
        if den <= 0:
            return False, f"Non-positive denominator on {f}"
        u_frac = Fraction(num, den)
        if L % den != 0 or int(entry["u_scaled_by_L"]) != num * (L // den):
            return False, f"Scaled integer mismatch on {f}"
        if u_frac * L != int(entry["u_scaled_by_L"]):
            return False, f"Fraction vs scaled mismatch on {f}"
        if sz > k and u_frac > 0:
            return False, f"Sign violation at |f|={sz} > k={k}: u_f = {u_frac} > 0"
        weights.append((f, u_frac))

    all_types = list(enum_compositions_fixed_len(s, T + 1))
    expected_num_types = math.comb(s + T, T)
    if len(all_types) != expected_num_types:
        return False, "Type count mismatch"

    x_diag = tuple([0] * T + [s])
    min_non_diag = None
    for X in all_types:
        if X == x_diag:
            continue
        val = Fraction(1, 1)
        for f, u_frac in weights:
            kv = multivariate_krawtchouk(f, X, b, T)
            if kv != 0:
                val += u_frac * kv
        if val < 0:
            return False, f"Dual infeasibility at X={X}: 1 + sum u_f K_f(X) = {val} < 0"
        if min_non_diag is None or val < min_non_diag:
            min_non_diag = val

    diag_bound = Fraction(1, 1)
    for f, u_frac in weights:
        diag_bound += u_frac * multivariate_krawtchouk(f, x_diag, b, T)

    claimed_num = int(cert["exact_lower_bound"]["numerator"])
    claimed_den = int(cert["exact_lower_bound"]["denominator"])
    if diag_bound != Fraction(claimed_num, claimed_den):
        return False, f"Bound mismatch: computed {diag_bound} vs claimed {claimed_num}/{claimed_den}"

    if diag_bound <= M_target:
        return False, f"Insufficient lower bound: {diag_bound} <= {M_target}"

    return True, (
        f"VERIFIED (Python Fraction): M >= {diag_bound.numerator}/{diag_bound.denominator} "
        f"(~{float(diag_bound):.6f}) > 3^11 = {M_target} across all {expected_num_types - 1} "
        f"non-diagonal shapes (min_LHS = {min_non_diag})"
    )


def main():
    if len(sys.argv) < 2:
        print("Usage: verify_python_exact.py <certificate.json> [--corrupt-test]", file=sys.stderr)
        sys.exit(2)

    run_soundness_calibrations()
    print("[Python] Positive soundness calibrations on explicit base-3 and base-2 nets: OK")

    with open(sys.argv[1], "r", encoding="utf-8") as fp:
        cert = json.load(fp)

    ok, msg = verify_certificate_dict(cert)
    print("[Python]", msg)
    if not ok:
        print("FAIL")
        sys.exit(1)

    if "--corrupt-test" in sys.argv[2:]:
        # Corrupt 1: flip sign of a |f| > k dual variable
        bad1 = json.loads(json.dumps(cert))
        for e in bad1["dual_weights_u"]:
            if int(e["size"]) > 8 and int(e["u_num"]) < 0:
                e["u_num"] = str(-int(e["u_num"]))
                e["u_scaled_by_L"] = str(-int(e["u_scaled_by_L"]))
                break
        ok1, _ = verify_certificate_dict(bad1)
        if ok1:
            print("FAIL: corrupted sign was accepted!")
            sys.exit(1)

        # Corrupt 2: scale all weights by 1.01 so tight X constraint goes negative
        bad2 = json.loads(json.dumps(cert))
        bad2["common_denominator_L"] = str(int(bad2["common_denominator_L"]) * 100)
        for e in bad2["dual_weights_u"]:
            e["u_num"] = str(int(e["u_num"]) * 101)
            e["u_den"] = str(int(e["u_den"]) * 100)
            e["u_scaled_by_L"] = str(int(e["u_scaled_by_L"]) * 101)
        ok2, _ = verify_certificate_dict(bad2)
        if ok2:
            print("FAIL: infeasible scaled certificate was accepted!")
            sys.exit(1)

        print("[Python] Negative corruption checks (sign violation & dual slack violation rejected): OK")


if __name__ == "__main__":
    main()
