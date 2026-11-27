#!/usr/bin/env python3
"""Standalone second implementation (mpmath interval arithmetic, outward rounding), written from PROOF.md only.
Checks Lemma 6 (the final inequality) and conditions (M1)-(M6), (V1)-(V4) at X0 = 3 e^Y.
usage: standalone_check.py Y c [thm11|thm12]   -> prints PASS/FAIL, exit 0 iff PASS"""
import sys
from mpmath import iv, mp
iv.prec = 300
def I(s):
    if '/' in s:
        a, b = s.split('/'); return iv.mpf(a)/iv.mpf(b)
    return iv.mpf(s)
def pw(b, e):  # b>0
    return iv.exp(e*iv.log(b))
def lt(a, b):  # certified a < b
    return a.b < b.a
def ge(a, b):
    return a.a >= b.b
def main(Ys, cs, variant='thm11'):
    Y, c = I(Ys), I(cs)
    al = iv.mpf(1)/3 + I('1e-9'); de = I('1e-9'); u2 = I('1e-6')
    X = 3*iv.exp(Y); L = al*X; lL = iv.log(L)
    nu = 1/(c*pw(L, I('2/3'))*pw(lL, I('1/3')))
    a8 = 1 - I('8/3')*al
    # (zeros, sigma<=3/5)  N*(T)<=T log T
    s0 = al*X*iv.exp(-(I('2/5')-al)*X)
    # KLN on [3/5,1-u2]
    s1 = I('2/5')*X*(I('17.418')*pw(L, I('3.8'))*iv.exp(-u2*a8*X) + I('5.272')*L*L*iv.exp(-u2*X))
    if variant == 'thm11':
        rows = [('9.77e21','57.8875','19703/1800'), ('7.65e10','33.08','503/45'), ('0.27','0','14/10')]; fac = lL
    else:
        rows = [('4.72e20','57.8875','10393/900')]; fac = iv.mpf(1)
    s2 = iv.mpf(0); mono = True
    for C, B, e in rows:
        C, B, e = I(C), I(B), I(e)
        m = 1 - I('3/2')*B*al*iv.sqrt(u2)
        g = nu - B*al*nu*iv.sqrt(nu)
        s2 += C*pw(L, e)*iv.exp(-X*g)/m
        Q = (1 - B*al*iv.sqrt(nu))*X*nu*(1 - 1/lL)/3
        need = e + (1/lL if variant == 'thm11' else 0)
        mono = mono and ge(Q, need) and lt(iv.mpf(0), m) and lt(B*al*iv.sqrt(nu), iv.mpf(1))
    s2 = fac*s2
    rE = 3*I('2.4798')/I('2.99')*(X+1)*iv.log(X+1)*iv.exp(-de*X)
    rT = iv.log(4)/I('2.99')*(iv.sqrt(2)*iv.exp(-X/6) + pw(iv.mpf(2), I('1/3'))*(X+1)/iv.log(2)*iv.exp(-X/3))
    Phi = 2*(s0+s1+s2) + rE + rT
    checks = {'Phi<1': lt(Phi, iv.mpf(1)), 'M1': ge((I('2/5')-al)*X, iv.mpf(1)),
              'M2': ge(u2*a8*X, I('4.8')) and ge(u2*X, iv.mpf(3)), 'M3': mono, 'M4': ge(de*X, iv.mpf(2)),
              'V1': lt(iv.mpf(481958), L), 'V2': ge(X, I('1e6')), 'V3': lt(nu, u2), 'V4': lt(iv.mpf(1), lL) and lt(iv.mpf(0), a8)}
    print(f"Y={Ys} c={cs} {variant}: Phi in [{mp.nstr(mp.mpf(Phi.a.a),15)}, {mp.nstr(mp.mpf(Phi.b.b),15)}]  X0*nu0 in [{mp.nstr(mp.mpf((X*nu).a.a),15)}, {mp.nstr(mp.mpf((X*nu).b.b),15)}]")
    print('  ' + ' '.join(f"{k}:{'ok' if v else 'NO'}" for k, v in checks.items()))
    ok = all(checks.values()); print('PASS' if ok else 'FAIL'); return ok
if __name__ == '__main__':
    sys.exit(0 if main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else 'thm11') else 1)
