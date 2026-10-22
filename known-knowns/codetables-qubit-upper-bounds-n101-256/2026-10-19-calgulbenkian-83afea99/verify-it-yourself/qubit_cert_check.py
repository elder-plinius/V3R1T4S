"""Exact-integer check of a Farkas certificate that no qubit stabilizer code [[n,k,d']] with d' >= d exists
(quantum weight-enumerator LP with shadow constraints). Standard library only.
Usage: python3 qubit_cert_check.py object.json D
Variables A_0..A_n (stabilizer weight enumerator), S = 2^(n-k), K_j(i) the ternary-alphabet (q=4) Krawtchouk
polynomial K_j(i) = sum_s (-1)^s 3^(j-s) C(i,s) C(n-i,j-s).  Constraints (B_j = (1/S) sum_i K_j(i) A_i):
  E0: A_0 = 1;  E1: sum_i A_i = S;
  Q_j (1 <= j <= d-1): B_j - A_j = 0      (written sum_i K_j(i) A_i - S*A_j = 0)
  G_j (d <= j <= n):   B_j - A_j >= 0     (A_i <= B_i)
  H_j (0 <= j <= n):   shadow, sum_i (-1)^i K_j(i) A_i >= 0
  A_i >= 0.
Certificate: integer multipliers u_E0, u_E1 (free), u_Q (free), v_G >= 0, v_H >= 0 such that the combination
has coefficient <= 0 on every variable A_i (all columns <= 0) while the combination of right-hand sides,
u_E0 + u_E1*S, is > 0.  Then the system is infeasible (Farkas).  D is passed on the command line.
The last line printed is a JSON object with the result."""
import sys, json
from math import comb


def K(n, j, i):
    return sum((-1) ** s * 3 ** (j - s) * comb(i, s) * comb(n - i, j - s) for s in range(j + 1))


def check(c, D):
    n, k, d = int(c['n']), int(c['k']), int(c['d'])
    if d != D:
        return False, 'certificate d=%d differs from the required d=%d' % (d, D)
    S = 2 ** (n - k)
    e0, e1 = int(c['u_E0']), int(c['u_E1'])
    uQ = {int(a): int(b) for a, b in c.get('u_Q', {}).items()}
    vG = {int(a): int(b) for a, b in c.get('v_G', {}).items()}
    vH = {int(a): int(b) for a, b in c.get('v_H', {}).items()}
    if not all(1 <= j <= d - 1 for j in uQ):
        return False, 'Q index out of range'
    if not (all(d <= j <= n for j in vG) and all(v >= 0 for v in vG.values())):
        return False, 'G multipliers out of range or negative'
    if not (all(0 <= j <= n for j in vH) and all(v >= 0 for v in vH.values())):
        return False, 'H multipliers out of range or negative'
    val = e0 + e1 * S
    if val <= 0:
        return False, 'right-hand side value <= 0'
    for i in range(n + 1):
        col = e1 + (e0 if i == 0 else 0)
        for j, v in uQ.items():
            col += v * (K(n, j, i) - (S if i == j else 0))
        for j, v in vG.items():
            col += v * (K(n, j, i) - (S if i == j else 0))
        for j, v in vH.items():
            col += (-1) ** i * v * K(n, j, i)
        if col > 0:
            return False, 'column %d positive' % i
    return True, 'value has %d digits; %d Q, %d G, %d H multipliers; all %d columns <= 0' % (
        len(str(val)), len(uQ), len(vG), len(vH), n + 1)


if __name__ == '__main__':
    c = json.load(open(sys.argv[1]))
    ok, why = check(c, int(sys.argv[2]))
    print('PASS' if ok else 'FAIL', '[[%s,%s]] no code with d >= %s (shadow=%s):' % (c['n'], c['k'], c['d'], c.get('shadow')), why)
    print(json.dumps({"n": c['n'], "k": c['k'], "d": c['d'], "VALID": bool(ok)}))
