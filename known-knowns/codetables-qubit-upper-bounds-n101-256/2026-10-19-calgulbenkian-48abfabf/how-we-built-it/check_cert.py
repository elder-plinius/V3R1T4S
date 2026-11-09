#!/usr/bin/env python3
"""Independent exact checker for a Farkas infeasibility certificate of the qubit stabilizer LP.

Standard library only; integer arithmetic only (no floats anywhere in the decision).

LP for an [[n,k,d]] qubit stabilizer code (stabilizer S, |S| = 2^(n-k), normalizer N = S^perp):
  variables A_0..A_n >= 0 (weight distribution of S);
  B_j := 2^-(n-k) * sum_i K_j(i) A_i   (quaternary MacWilliams identity),
  S_j := 2^-(n-k) * sum_i (-1)^i K_j(i) A_i   (Rains shadow enumerator),
  with K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s)  (Krawtchouk polynomial, q = 4).
Constraints, multiplied through by 2^(n-k) so every coefficient is an integer:
  E0:  A_0 = 1
  E1:  sum_i A_i = 2^(n-k)                          (equivalently B_0 = 1)
  Q_j: sum_i K_j(i) A_i - 2^(n-k) A_j  = 0   for 1 <= j <= d-1   (A_j = B_j below the distance)
  G_j: sum_i K_j(i) A_i - 2^(n-k) A_j >= 0   for d <= j <= n     (A_j <= B_j)
  H_j: sum_i (-1)^i K_j(i) A_i        >= 0   for 0 <= j <= n     (shadow; only if "shadow": true)
Farkas: if integers u_E0, u_E1, u_Qj (any sign) and v_Gj, v_Hj >= 0 satisfy, for every column i,
  c_i := u_E0[i==0] + u_E1 + sum_j u_Qj (K_j(i) - 2^(n-k)[i==j]) + sum_j v_Gj (K_j(i) - 2^(n-k)[i==j])
         + sum_j v_Hj (-1)^i K_j(i)  <= 0,
and the value  u_E0 * 1 + u_E1 * 2^(n-k) > 0, then no nonnegative A satisfies the constraints, so no
[[n,k,d]] stabilizer code exists. (Proof: for feasible A >= 0, value = sum_i c_i A_i - sum v_G G(A) - sum v_H H(A) <= 0.)

Usage: check_cert.py CERT.json   -> prints VERIFIED or FAILED with the reason; exit code 0 only if VERIFIED.
CERT.json: {"n":..,"k":..,"d":..,"shadow":true|false,"u_E0":"int","u_E1":"int",
            "u_Q":{"j":"int",...},"v_G":{"j":"int",...},"v_H":{"j":"int",...}}  (integers as decimal strings;
            omitted indices are 0).
"""
import json, sys
from math import comb


def kraw(n, j, i):
    """Quaternary Krawtchouk K_j(i) by the explicit binomial sum (exact integer)."""
    return sum((-1) ** s * 3 ** (j - s) * comb(i, s) * comb(n - i, j - s) for s in range(0, j + 1))


def check(cert):
    n, k, d, shadow = int(cert["n"]), int(cert["k"]), int(cert["d"]), bool(cert["shadow"])
    if not (0 <= k <= n and 1 <= d <= n + 1):
        return False, "bad parameters"
    S = 2 ** (n - k)
    uE0, uE1 = int(cert["u_E0"]), int(cert["u_E1"])
    uQ = {int(j): int(v) for j, v in cert.get("u_Q", {}).items()}
    vG = {int(j): int(v) for j, v in cert.get("v_G", {}).items()}
    vH = {int(j): int(v) for j, v in cert.get("v_H", {}).items()}
    if any(not (1 <= j <= d - 1) for j in uQ):
        return False, "u_Q index outside 1..d-1"
    if any(not (d <= j <= n) for j in vG):
        return False, "v_G index outside d..n"
    if any(not (0 <= j <= n) for j in vH):
        return False, "v_H index outside 0..n"
    if vH and not shadow:
        return False, "shadow multipliers given but shadow is false"
    if any(v < 0 for v in vG.values()) or any(v < 0 for v in vH.values()):
        return False, "negative inequality multiplier"
    value = uE0 + uE1 * S
    if value <= 0:
        return False, "certificate value is not positive"
    # w_j = total multiplier on the MacWilliams row j (equality or inequality form share the same row)
    w = {}
    for j, v in list(uQ.items()) + list(vG.items()):
        w[j] = w.get(j, 0) + v
    worst = None
    for i in range(n + 1):
        c = uE1 + (uE0 if i == 0 else 0)
        for j, v in w.items():
            c += v * kraw(n, j, i)
            if i == j:
                c -= v * S
        sgn = -1 if i % 2 else 1
        for j, v in vH.items():
            c += sgn * v * kraw(n, j, i)
        if c > 0:
            return False, "column %d has positive combined coefficient" % i
        worst = c if worst is None else max(worst, c)
    return True, "value=%d digits, max column coefficient <= 0, %d+%d+%d multipliers" % (
        len(str(value)), len(uQ), len(vG), len(vH))


if __name__ == "__main__":
    cert = json.load(open(sys.argv[1]))
    ok, why = check(cert)
    tag = "[[%s,%s,%s]] shadow=%s" % (cert["n"], cert["k"], cert["d"], cert["shadow"])
    print(("VERIFIED " if ok else "FAILED ") + tag + ": " + why)
    sys.exit(0 if ok else 1)
