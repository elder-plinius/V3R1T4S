#!/usr/bin/env python3
"""Second, independent re-check of a certificate (contrarian lens).  Krawtchouk numbers by the three-term
recurrence (j+1) K_{j+1}(x) = (3(n-j) + j - 4x) K_j(x) - 3(n-j+1) K_{j-1}(x), K_0 = 1, K_1 = 3n - 4x, and the LP
in its ORIGINAL unscaled form with exact Fractions: B_j = 2^-(n-k) sum_i K_j(i) A_i, Sh_j = 2^-(n-k) sum_i (-1)^i K_j(i) A_i.
Constraints: A_0 - 1 = 0; sum A_i - 2^(n-k) = 0; B_j - A_j = 0 (1<=j<d); B_j - A_j >= 0 (j>=d); Sh_j >= 0.
The certificate's multipliers are re-scaled (rows of check_cert.py are 2^(n-k) x these rows)."""
import json, sys
from fractions import Fraction as F
c = json.load(open(sys.argv[1])); n, k, d = c["n"], c["k"], c["d"]
K = [[1] * (n + 1), [3 * n - 4 * x for x in range(n + 1)]]
for j in range(1, n):
    K.append([((3 * (n - j) + j - 4 * x) * K[j][x] - 3 * (n - j + 1) * K[j - 1][x]) // (j + 1) for x in range(n + 1)])
    assert all(((3 * (n - j) + j - 4 * x) * K[j][x] - 3 * (n - j + 1) * K[j - 1][x]) % (j + 1) == 0 for x in range(n + 1))
S = 2 ** (n - k)
col = [F(0)] * (n + 1)
val = F(0)
u0, u1 = int(c["u_E0"]), int(c["u_E1"])
col[0] += u0; val += u0                                   # A_0 = 1
for i in range(n + 1): col[i] += u1                       # sum A_i = 2^(n-k)
val += u1 * S
for fam in ("u_Q", "v_G"):
    for js, v in c[fam].items():
        j, v = int(js), int(v) * S                        # unscaled row = scaled row / 2^(n-k)
        assert (fam == "u_Q" and 1 <= j < d) or (fam == "v_G" and d <= j <= n and v >= 0)
        for i in range(n + 1):
            col[i] += F(v * K[j][i], S)
        col[j] -= v
for js, v in c["v_H"].items():
    j, v = int(js), int(v) * S
    assert v >= 0 and c["shadow"]
    for i in range(n + 1):
        col[i] += F(v * (-1) ** i * K[j][i], S)
ok = val > 0 and max(col) <= 0
print("check2", "PASS" if ok else "FAIL", "[[%d,%d,%d]]" % (n, k, d), "value>0:", val > 0, "max column:", "<=0" if max(col) <= 0 else max(col))
sys.exit(0 if ok else 1)
