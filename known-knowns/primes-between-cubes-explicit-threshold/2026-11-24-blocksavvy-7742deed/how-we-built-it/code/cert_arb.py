#!/usr/bin/env python3
"""Interval (arb, outward-rounded) certificate for: a prime in (n^3,(n+1)^3) for every n >= exp(exp(Y)).
Implements Phi(X) and the monotonicity conditions M1-M6 of PROOF.md at X0 = 3 exp(Y).
Usage: cert_arb.py --Y 29.735 [--c 51.34] [--dens thm11|thm12|kln] [--prec 128] [--Cscale 1]
Prints PASS/FAIL and every term as an arb ball. Exit code 0 iff PASS."""
import argparse, sys
from flint import arb, ctx

def A(s):  # exact decimal / rational given as string -> arb enclosure
    if '/' in s:
        p, q = s.split('/'); return arb(p) / arb(q)
    return arb(s)

def certify(Y, c, dens='thm11', prec=128, Cscale='1', verbose=True):
    ctx.prec = prec
    out = {}
    Y = A(Y); c = A(c)
    alpha = arb(1)/3 + A('1e-9'); delta = A('1e-9')
    u2 = A('1e-6'); s1 = A('3/5')
    K = A('2.4798'); C1k = A('17.418'); C2k = A('5.272')
    X = 3*Y.exp()                           # X0 = log x0
    L = alpha*X                             # log T
    lL = L.log()
    nu = 1/(c * L**(arb(2)/3) * lL**(arb(1)/3))   # zero-free width at height T
    out['X0'] = X; out['L0'] = L; out['nu0'] = nu; out['X0*nu0'] = X*nu
    # A0: zeros counted trivially for sigma <= 3/5, N*(T) <= T log T
    A0 = alpha*X*(-(A('2/5')-alpha)*X).exp()
    # A1: KLN-type bound on [3/5, 1-u2]
    a8 = 1 - 8*alpha/3
    if dens == 'kln':   # ablation: KLN all the way to 1-nu, (log T)^(5-2 sigma) kept exactly
        # int_nu^{0.4} X L^{3+2u} e^{-u a8 X} du <= L^3 X e^{-nu(a8 X - 2 lL)}/(a8 X - 2 lL); second term <= L^2 e^{-nu X}
        A1 = C1k*L**3*X*(-(nu*(a8*X-2*lL))).exp()/(a8*X-2*lL) + C2k*L**2*(-(nu*X)).exp()
        A2 = arb(0)
    else:
        A1 = A('2/5')*X*(C1k*L**A('3.8')*(-(u2*a8*X)).exp() + C2k*L**2*(-(u2*X)).exp())
        if dens == 'thm12':
            terms = [(A('4.72e20')*A(Cscale), A('57.8875'), A('10393/900'))]
            loglogT = arb(1)
        elif dens == 'thm13':   # Bellotti Thm 1.3, T >= exp(6.7e12) (proof only sketched in the source)
            terms = [(A('4.45e12')*A(Cscale), A('57.8875'), A('10393/900'))]
            loglogT = arb(1)
        else:
            terms = [(A('9.77e21')*A(Cscale), A('57.8875'), A('19703/1800')),
                     (A('7.65e10'), A('33.08'), A('503/45')),
                     (A('0.27'), arb(0), A('14/10'))]
            loglogT = lL
        A2 = arb(0); out['M3'] = []
        for (Ci, Bi, ei) in terms:
            gi = nu - Bi*alpha*nu**A('3/2')
            mi = 1 - A('3/2')*Bi*alpha*u2.sqrt()
            A2 += Ci * L**ei * (-(X*gi)).exp() / mi
            Qi = (1 - Bi*alpha*nu.sqrt()) * X*nu * (1 - 1/lL)/3
            need = ei + (1/lL if dens == 'thm11' else 0)
            out['M3'].append((Qi, need, mi))
        A2 = loglogT*A2
    RE = 3*K/A('2.99') * (X+1)*(X+1).log()*(-(delta*X)).exp()
    RT = arb(4).log()/A('2.99')*(arb(2).sqrt()*(-X/6).exp() + arb(2)**(arb(1)/3)*(X+1)/arb(2).log()*(-X/3).exp())
    Phi = 2*(A0+A1+A2) + RE + RT
    out.update(A0=A0, A1=A1, A2=A2, RE=RE, RT=RT, Phi=Phi)
    conds = {
      'Phi<1': Phi < 1,
      'M1 (2/5-alpha)X0>=1': (A('2/5')-alpha)*X >= 1,
      'M2 u2*a8*X0>=4.8 and u2*X0>=3': (u2*a8*X >= A('4.8')) and (u2*X >= 3),
      'M4 delta*X0>=2': delta*X >= 2,
      'V1 log T0 > 481958 (Bellotti constants)': L > 481958,
      'V2 log x0 >= 1e6 (K=2.4798)': X >= A('1e6'),
      'V3 1-u2 >= 0.98 and nu0 < u2': (1-u2 >= A('0.98')) and (nu < u2),
      'V4 log L0 > 1, a8 > 0': (lL > 1) and (a8 > 0),
    }
    if dens == 'thm13':
        conds['V1b log T0 >= 6.7e12 (Bellotti Thm 1.3)'] = L >= A('6.7e12')
    if dens != 'kln':
        conds['M3 Q_i(X0) >= e_i (+1/logL), m_i>0, B_i alpha sqrt(nu0)<1'] = all(
            (Q >= need) and (m > 0) for (Q, need, m) in out['M3'])
    else:
        conds['M3k a8*X0 - 2 log L0 > 0 and ablation monotone (checked: Xnu*a8/3*(1-1/logL) >= 3+2/logL... )'] = \
            (a8*X - 2*lL > 0) and (X*nu*a8*(1-1/lL)/3 >= 3 + 1)
    ok = all(conds.values())
    if verbose:
        print(f"prec={prec} Y={Y.mid()} c={c.mid()} dens={dens} Cscale={Cscale}")
        for k in ['X0','L0','nu0','X0*nu0','A0','A1','A2','RE','RT','Phi']:
            print(f"  {k:7s} = {out[k].str(12, radius=True)}")
        if 'M3' in out:
            for i,(Q,need,m) in enumerate(out['M3']):
                print(f"  M3[{i}] Q={Q.str(8)} need>={need.str(8)} m={m.str(8)}")
        for k,v in conds.items(): print(f"  {'ok ' if v else 'NO '} {k}")
        print("PASS" if ok else "FAIL")
    return ok, out

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--Y', required=True); ap.add_argument('--c', default='51.34')
    ap.add_argument('--dens', default='thm11', choices=['thm11','thm12','thm13','kln'])
    ap.add_argument('--prec', type=int, default=128); ap.add_argument('--Cscale', default='1')
    a = ap.parse_args()
    ok, _ = certify(a.Y, a.c, a.dens, a.prec, a.Cscale)
    sys.exit(0 if ok else 1)
