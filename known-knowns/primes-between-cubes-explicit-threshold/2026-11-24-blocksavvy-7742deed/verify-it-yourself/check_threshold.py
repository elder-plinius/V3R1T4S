#!/usr/bin/env python3
"""Standalone checker for object/certificate.json, written from object/proof.md (mpmath interval arithmetic, outward rounding).
1. The certificate's constants must equal the values in the cited statements (listed in EXPECTED below).
2. Recomputes Phi(X0) = 2(A0 + A1 + A2) + R_E + R_T at X0 = 3 e^Y (proof Lemmas 4-5) and the monotonicity / validity
   conditions (M1)-(M4), (V1)-(V4) (proof Lemma 6), at 200 and 300 bits.
3. Phi_upper_stated must be >= the recomputed upper end, within 1e-9 of it, and < 1.
4. Tightness: at Y - 0.001 the recomputed Phi must be > 1 (so the certificate is not vacuous).
usage: check_threshold.py object/certificate.json   -> last line PASS or FAIL, exit 0 iff PASS"""
import sys, json
from decimal import Decimal
from mpmath import iv, mp

EXPECTED = {"Y": "29.735", "alpha": "1/3 + 1e-9", "delta": "1e-9", "u2": "1e-6", "I1_K": "2.4798", "I1_h_lower_factor": "2.99",
            "I3_zero_free_c": "51.34", "I5_KLN_C1": "17.418", "I5_KLN_C2": "5.272", "I5_exponent_bound_on_logT": "3.8",
            "I4_min_logT": "481958",
            "I4_Bellotti_Thm1_1_rows": [{"C": "9.77e21", "B": "57.8875", "e": "19703/1800"},
                                        {"C": "7.65e10", "B": "33.08", "e": "503/45"},
                                        {"C": "0.27", "B": "0", "e": "14/10"}]}

def I(s):
    s = s.replace(' ', '')
    if '+' in s:
        return sum((I(t) for t in s.split('+')), iv.mpf(0))
    if '/' in s:
        a, b = s.split('/'); return iv.mpf(a) / iv.mpf(b)
    return iv.mpf(s)
def pw(b, e): return iv.exp(e * iv.log(b))
def lt(a, b): return a.b < b.a
def ge(a, b): return a.a >= b.b

def phi(cert, Ys):
    Y = I(Ys); al = I(cert["alpha"]); de = I(cert["delta"]); u2 = I(cert["u2"]); c = I(cert["I3_zero_free_c"])
    K = I(cert["I1_K"]); h = I(cert["I1_h_lower_factor"])
    X = 3 * iv.exp(Y); L = al * X; lL = iv.log(L)
    nu = 1 / (c * pw(L, I('2/3')) * pw(lL, I('1/3')))
    a8 = 1 - I('8/3') * al
    A0 = al * X * iv.exp(-(I('2/5') - al) * X)
    A1 = I('2/5') * X * (I(cert["I5_KLN_C1"]) * pw(L, I(cert["I5_exponent_bound_on_logT"])) * iv.exp(-u2 * a8 * X)
                         + I(cert["I5_KLN_C2"]) * L * L * iv.exp(-u2 * X))
    A2 = iv.mpf(0); mono = True
    for r in cert["I4_Bellotti_Thm1_1_rows"]:
        C, B, e = I(r["C"]), I(r["B"]), I(r["e"])
        m = 1 - I('3/2') * B * al * iv.sqrt(u2)
        g = nu - B * al * nu * iv.sqrt(nu)
        A2 += C * pw(L, e) * iv.exp(-X * g) / m
        Q = (1 - B * al * iv.sqrt(nu)) * X * nu * (1 - 1 / lL) / 3
        mono = mono and ge(Q, e + 1 / lL) and lt(iv.mpf(0), m) and lt(B * al * iv.sqrt(nu), iv.mpf(1))
    A2 = lL * A2
    RE = 3 * K / h * (X + 1) * iv.log(X + 1) * iv.exp(-de * X)
    RT = iv.log(4) / h * (iv.sqrt(2) * iv.exp(-X / 6) + pw(iv.mpf(2), I('1/3')) * (X + 1) / iv.log(2) * iv.exp(-X / 3))
    Phi = 2 * (A0 + A1 + A2) + RE + RT
    conds = {'M1': ge((I('2/5') - al) * X, iv.mpf(1)), 'M2': ge(u2 * a8 * X, I('4.8')) and ge(u2 * X, iv.mpf(3)),
             'M3': mono, 'M4': ge(de * X, iv.mpf(2)), 'V1': lt(I(cert["I4_min_logT"]), L), 'V2': ge(X, I('1e6')),
             'V3': lt(nu, u2) and ge(1 - u2, I('0.98')), 'V4': lt(iv.mpf(1), lL) and lt(iv.mpf(0), a8)}
    return Phi, conds

def main(path):
    cert = json.load(open(path))
    ok = True
    for k, v in EXPECTED.items():
        if cert.get(k) != v:
            print(f"constant {k} = {cert.get(k)!r} differs from the cited value {v!r}"); ok = False
    stated = I(cert["Phi_upper_stated"]); tight = I(cert["Y_minus_0.001_Phi_lower_stated"])
    Ym = str(Decimal(cert["Y"]) - Decimal('0.001'))
    for prec in (200, 300):
        iv.prec = prec; mp.prec = prec
        P, conds = phi(cert, cert["Y"])
        Pm, _ = phi(cert, Ym)
        print(f"prec {prec}: Phi(3e^{cert['Y']}) in [{mp.nstr(mp.mpf(P.a.a), 16)}, {mp.nstr(mp.mpf(P.b.b), 16)}];  Phi at Y = {Ym} in [{mp.nstr(mp.mpf(Pm.a.a), 10)}, {mp.nstr(mp.mpf(Pm.b.b), 10)}]")
        print('  ' + ' '.join(f"{k}:{'ok' if v else 'NO'}" for k, v in conds.items()))
        checks = {'Phi<1': lt(P, iv.mpf(1)), 'stated>=sup': ge(stated, P), 'stated-sup<1e-9': lt(stated - P, I('1e-9')),
                  'stated<1': lt(stated, iv.mpf(1)), 'Y-0.001 fails': lt(iv.mpf(1), Pm) and ge(Pm, tight)}
        print('  ' + ' '.join(f"{k}:{'ok' if v else 'NO'}" for k, v in checks.items()))
        ok = ok and all(conds.values()) and all(checks.values())
    print('PASS' if ok else 'FAIL'); return ok

if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1] if len(sys.argv) > 1 else 'object/certificate.json') else 1)
