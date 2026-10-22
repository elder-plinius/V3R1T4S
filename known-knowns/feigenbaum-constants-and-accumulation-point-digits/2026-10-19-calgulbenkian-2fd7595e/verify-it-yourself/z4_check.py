#!/usr/bin/env python3
"""Standard-library (decimal) check of a quartic (z = 4) Feigenbaum-Cvitanovic fixed point and its
unstable eigenfunction, from Chebyshev coefficients, at about 1300 digits.

Definitions (written from the standard setting; g is the fixed point with g(0) = 1 and a quartic maximum):
  g(x) = phi(x^4),  phi(u) = 1 + u * S(u),  S(u) = sum_k c_k T_k(2u - 1)      [c = c_coeffs]
  fixed-point equation   g(x) = alpha * g( g(x / alpha) ),  alpha = 1 / g(1) = 1 / phi(1)
  in the variable u = x^4, with p1 = phi(1), w = p1^4 * u, y = phi(w), v = y^4:
        phi(u) * p1 = phi(v)
  linearised operator   delta * h(x) = alpha * [ g'(g(x/alpha)) h(x/alpha) + h(g(x/alpha)) ],  h(x) = psi(x^4),
  psi(u) = sum_k b_k T_k(2u - 1)                                              [b = b_coeffs]
  in u:   delta * psi(u) = (1 / p1) * [ psi(v) + 4 * phi'(v) * y^3 * psi(w) ]
All arithmetic is decimal.Decimal with 1300 significant digits (the printed residuals are far above
the rounding level 1e-1290, so they are the equation residuals, not arithmetic noise).

usage: z4_check.py OBJECT_JSON [THURLBY_EXCERPT OEIS_DATA_FILE]
"""
import sys, json, time, re
from decimal import Decimal, getcontext

getcontext().prec = 1300
D = Decimal


def cheb_eval(coef, s):
    """sum_k coef[k] T_k(s) by Clenshaw's recurrence"""
    b1 = D(0)
    b2 = D(0)
    two_s = 2 * s
    for k in range(len(coef) - 1, 0, -1):
        b1, b2 = coef[k] + two_s * b1 - b2, b1
    return coef[0] + s * b1 - b2


def cheb_deriv_coeffs(coef):
    """coefficients of d/ds sum coef[k] T_k(s) in the basis T_j (j = 0 .. n-2)"""
    n = len(coef)
    d = [D(0)] * (n + 1)
    for k in range(n - 1, 0, -1):
        d[k - 1] = d[k + 1] + 2 * k * coef[k]
    d[0] = d[0] / 2
    return d[:n - 1]


def make(c):
    dc = cheb_deriv_coeffs(c)

    def S(u):
        return cheb_eval(c, 2 * u - 1)

    def dS(u):
        return 2 * cheb_eval(dc, 2 * u - 1)

    def phi(u):
        return 1 + u * S(u)

    def dphi(u):
        return S(u) + u * dS(u)

    return S, phi, dphi


def digits_agree(a, b):
    d = abs(a - b)
    if d == 0:
        return 99999
    return int((-d.log10()).to_integral_value(rounding='ROUND_FLOOR'))


def exp10(x):
    """floor of log10 |x| as an integer (x != 0)"""
    return int(abs(x).log10().to_integral_value(rounding='ROUND_FLOOR'))


def main():
    t0 = time.time()
    obj = json.load(open(sys.argv[1]))
    U = [D(k) / 31 for k in range(1, 31)] + [D(1) / 1000003]   # 31 test points in (0, 1)
    res = {}
    for tag in ('N1', 'N2'):
        c = [D(s) for s in obj['c_coeffs_' + tag]]
        b = [D(s) for s in obj['b_coeffs_' + tag]]
        _, phi, dphi = make(c)
        psi = lambda u, b=b: cheb_eval(b, 2 * u - 1)
        p1 = phi(D(1))
        alpha = 1 / p1
        r_fp = []
        for u in U:
            w = p1 ** 4 * u
            y = phi(w)
            v = y ** 4
            r_fp.append(phi(u) * p1 - phi(v))
        nums = []
        for u in U:
            w = p1 ** 4 * u
            y = phi(w)
            v = y ** 4
            nums.append(((psi(v) + 4 * dphi(v) * y ** 3 * psi(w)) / p1, psi(u)))
        i0 = 9    # u = 10/31, where psi is far from zero
        d0 = nums[i0][0] / nums[i0][1]
        deltas = [d0]
        r_eig = [nm - d0 * pu for nm, pu in nums]
        res[tag] = dict(n=len(c), alpha=alpha, r_fp=r_fp, deltas=deltas, r_eig=r_eig, psi0=psi(D(0)))
        print("== resolution %s: %d Chebyshev coefficients for phi, %d for psi" % (tag, len(c), len(b)))
        print("alpha = 1/phi(1) = %s" % format(alpha, '.70f'))
        print("fixed-point residuals phi(u)*phi(1) - phi(v) at %d points: largest in absolute value %s" % (len(U), format(max(r_fp, key=abs), '.3e')))
        print("delta from the eigen-equation at u = 10/31: %s" % format(d0, '.60f'))
        print("eigen-equation residuals (L psi)(u) - delta psi(u) at the same %d points: largest in absolute value %s" % (len(U), format(max(r_eig, key=abs), '.3e')))
        print("  psi(0) = %s ; largest |psi(u)| at the test points %s" % (format(res[tag]['psi0'], '.20f'), format(max(abs(pu) for _, pu in nums), '.3f')))
        res[tag]['spread'] = max(abs(r) for r in r_eig)
    a1, a2 = res['N1']['alpha'], res['N2']['alpha']
    d1, d2 = res['N1']['deltas'][0], res['N2']['deltas'][0]
    dec_a = digits_agree(a1, a2)
    dec_d = digits_agree(d1, d2)
    print("== the two resolutions (%d and %d coefficients; the larger is %.2f %% bigger)" % (res['N1']['n'], res['N2']['n'], 100.0 * (res['N2']['n'] - res['N1']['n']) / res['N1']['n']))
    print("|alpha_N1 - alpha_N2| ~ 1e%d   decimals agreeing: %d" % (exp10(a1 - a2), dec_a))
    print("|delta_N1 - delta_N2| ~ 1e%d   decimals agreeing: %d" % (exp10(d1 - d2), dec_d))
    claimed_a, claimed_d = obj['agreeing_decimals_alpha_4'], obj['agreeing_decimals_delta_4']
    for tag in ('N1', 'N2'):
        pa = D(obj['alpha_4_' + tag]); pd = D(obj['delta_4_' + tag])
        print("printed alpha_4_%s (%d decimals) vs computed |alpha|: agree to 1e%d; printed delta_4_%s vs computed delta: agree to 1e%d" % (tag, len(obj['alpha_4_' + tag].split('.')[1]), exp10(pa - abs(res[tag]['alpha'])), tag, exp10(pd - res[tag]['deltas'][0])))
    ok = True
    # conditions of the checker (thresholds are the contributor's stated decimal counts)
    worst_fp = max(exp10(r) for t in res for r in res[t]['r_fp'])
    worst_sp = max(exp10(res[t]['spread']) for t in res)
    print("worst fixed-point residual over both resolutions ~ 1e%d; worst eigen-equation residual ~ 1e%d" % (worst_fp, worst_sp))
    ok &= worst_fp < -(claimed_a + 5) and worst_sp < -(claimed_d + 5)
    ok &= (dec_a >= claimed_a) and (dec_d >= claimed_d)
    ok &= abs(res['N1']['psi0'] - 1) < D(10) ** -50
    ok &= res['N2']['n'] >= 1.02 * res['N1']['n']
    print("claimed agreeing decimals: alpha %d, delta %d; measured: alpha %d, delta %d" % (claimed_a, claimed_d, dec_a, dec_d))
    # comparison with published values (data files in table-record)
    if len(sys.argv) > 3:
        th = open(sys.argv[2]).read()
        for name, key, val in (('alpha_4', 'α4', abs(a1)), ('delta_4', 'δ4', d1)):
            m = re.search(key + r' = [+-]?(\d)\.(.*?)(?:\n\s*\n|\.\s*\.\s*\.)', th, re.S)
            digs = m.group(1) + '.' + re.sub(r'[^0-9]', '', m.group(2))
            pub = D(digs)
            n = len(digs) - 2
            ours = format(val, '.%df' % (n + 20))[:len(digs)]   # truncated, not rounded
            same = 0
            while same < len(digs) and digs[same] == ours[same]:
                same += 1
            print("Thurlby thesis table 4.6, %s: %d decimals transcribed; leading characters equal to this computation: %d of %d" % (name, n, same, len(digs)))
            ok &= (same == len(digs))
        oe = open(sys.argv[3]).read()
        m = re.search(r'data: ([0-9,]+)', oe)
        od = m.group(1).replace(',', '')
        ours = format(abs(a1), '.80f').replace('.', '')
        same = 0
        while same < len(od) and od[same] == ours[same]:
            same += 1
        print("OEIS A195102 data: %d digits, leading digits equal to |alpha_4| of this computation: %d" % (len(od), same))
        ok &= (same == len(od))
    print("alpha_4 = -%s..." % format(abs(a1), '.60f'))
    print("delta_4 = +%s..." % format(d1, '.60f'))
    print("elapsed %.1f s" % (time.time() - t0))
    print("RESULT %s" % ("PASS" if ok else "FAIL"))
    sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
