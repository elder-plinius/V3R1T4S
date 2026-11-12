#!/usr/bin/env python3
"""Ball-arithmetic checker for three-body exponential-basis certificates (python-flint / arb).

usage: check_cert.py BASIS VEC1 [VEC2] --bar BAR --margin MARGIN [--prec 320] [--procs 6]

Definition checked (arXiv:2503.17389 eq. 2, muon-atomic units, centre of mass removed):
  H = -(1/2M1) Lap_1 - (1/2M2) Lap_2 - (1/2M3) Lap_3 + q1 q3/r13 + q2 q3/r23 + q1 q2/r12.
With x = r1 - r3, y = r2 - r3:  T = -(1/2) [ w1 Lap_x + w2 Lap_y + 2 w3 grad_x.grad_y ],
  w1 = 1/M1 + 1/M3, w2 = 1/M2 + 1/M3, w3 = 1/M3.
Basis function i: Re[ P_t(x,y) exp(-a X - b Y - c R) ] (X=|x|, Y=|y|, R=|x-y|), P_t a Cartesian tensor:
  L=1: 0: x_k, 1: y_k, 2: (x-y)_k;  L=2 (symmetric traceless): 0: xx, 1: xy, 2: yy, 3: (x-y)(x-y).
If sym = kappa != 0 the function is phi + kappa * P12 phi (P12 swaps particles 1 and 2).
This file derives the matrix elements in OPERATOR form (H applied to the ket) and integrates with the closed-form
relative-coordinate integrals; it shares no code with gen.py / engine.cpp (gradient form, perimetric expansion).
One vector: prints an enclosure of the Rayleigh quotient (an upper bound on the lowest root of the block).
Two vectors: prints an enclosure of the larger root of the 2x2 projected problem (upper bound on the second root).
"""
import sys, argparse, math, itertools
import sympy as sp
from flint import arb, acb, ctx

def derive(L):
    X, Y, R = sp.symbols('X Y R', positive=True)
    a, b, c, d, e, g = sp.symbols('a b c d e g')
    w1, w2, w3, q13, q23, q12 = sp.symbols('w1 w2 w3 q13 q23 q12')
    xs = sp.symbols('x1:4'); ys = sp.symbols('y1:4'); ct, st = sp.symbols('ct st')
    rs = [xs[i] - ys[i] for i in range(3)]
    dot = lambda s, t: sum(s[i] * t[i] for i in range(3))
    if L == 1:
        types = [list(xs), list(ys), rs]
    else:
        def stf(s, t):
            return [sp.Rational(1, 2) * (s[i] * t[j] + s[j] * t[i]) - (sp.Rational(1, 3) * dot(s, t) if i == j else 0)
                    for i in range(3) for j in range(3)]
        types = [stf(xs, xs), stf(xs, ys), stf(ys, ys), stf(rs, rs)]
    # ket exponential F = exp(-d X - e Y - g R): first and second derivatives divided by F
    vx = [-d * xs[j] / X - g * rs[j] / R for j in range(3)]
    vy = [-e * ys[j] / Y + g * rs[j] / R for j in range(3)]
    lapx = d**2 + g**2 - 2 * d / X - 2 * g / R + 2 * d * g * dot(xs, rs) / (X * R)
    lapy = e**2 + g**2 - 2 * e / Y - 2 * g / R - 2 * e * g * dot(ys, rs) / (Y * R)
    mixed = dot(vx, vy) + 2 * g / R
    orient = {xs[0]: X, xs[1]: 0, xs[2]: 0, ys[0]: Y * ct, ys[1]: Y * st, ys[2]: 0}
    def reduce_scalar(expr):
        po = sp.Poly(sp.expand(expr.subs(orient)), st); out = 0
        for (n,), cf in po.terms():
            assert n % 2 == 0
            out += cf * (1 - ct**2) ** (n // 2)
        out = sp.expand(sp.expand(out).subs(ct, (X**2 + Y**2 - R**2) / (2 * X * Y)))
        out = sp.expand(out * X * Y * R)
        po = sp.Poly(out, X, Y, R)       # raises if a negative power survived
        return {mon: cf for mon, cf in po.terms()}
    table = {}
    for tb, Pb in enumerate(types):
        for tk, Pk in enumerate(types):
            S_int = 0; H_int = 0
            for n in range(len(Pb)):
                P = Pk[n]
                lap_x = sum(sp.diff(P, xs[j], 2) for j in range(3)) + 2 * sum(sp.diff(P, xs[j]) * vx[j] for j in range(3)) + P * lapx
                lap_y = sum(sp.diff(P, ys[j], 2) for j in range(3)) + 2 * sum(sp.diff(P, ys[j]) * vy[j] for j in range(3)) + P * lapy
                mix = (sum(sp.diff(P, xs[j], ys[j]) for j in range(3)) + sum(sp.diff(P, xs[j]) * vy[j] for j in range(3))
                       + sum(sp.diff(P, ys[j]) * vx[j] for j in range(3)) + P * mixed)
                Hk = -sp.Rational(1, 2) * (w1 * lap_x + w2 * lap_y + 2 * w3 * mix) + P * (q13 / X + q23 / Y + q12 / R)
                S_int += Pb[n] * P; H_int += Pb[n] * Hk
            table[(tb, tk)] = (reduce_scalar(S_int), reduce_scalar(H_int))
    args = (a, b, c, d, e, g, w1, w2, w3, q13, q23, q12)
    funcs = {}
    scale = 1                                   # one common integer scale for every S and H entry
    for Sd, Hd in table.values():
        for cf in list(Sd.values()) + list(Hd.values()):
            for term in sp.Add.make_args(sp.expand(cf)):
                scale = math.lcm(scale, int(sp.Rational(term.as_coeff_Mul()[0]).q))
    for key, (Sd, Hd) in table.items():
        Sd = {m: sp.expand(cf * scale) for m, cf in Sd.items()}; Hd = {m: sp.expand(cf * scale) for m, cf in Hd.items()}
        monS = list(Sd); monH = list(Hd)
        fS = sp.lambdify(args, [Sd[m] for m in monS], modules=[{}], cse=True)
        fH = sp.lambdify(args, [Hd[m] for m in monH], modules=[{}], cse=True)
        funcs[key] = (monS, fS, monH, fH)
    return funcs

FACT = [math.factorial(i) for i in range(40)]
def gammas(mons, A, B, C):
    """G[l,m,n] = int X^l Y^m R^n exp(-A X - B Y - C R) dX dY dR over the triangle region (closed form)."""
    u = 1 / (A + B); wq = 1 / (A + C); v = 1 / (B + C)
    mx = max(l + m + n for l, m, n in mons) + 2
    pu = [u]; pw = [wq]; pv = [v]
    for _ in range(mx):
        pu.append(pu[-1] * u); pw.append(pw[-1] * wq); pv.append(pv[-1] * v)
    out = {}
    for (l, m, n) in mons:
        s = 0
        for i in range(l + 1):
            for j in range(m + 1):
                for k in range(n + 1):
                    cf = math.comb(l, i) * math.comb(m, j) * math.comb(n, k) * FACT[i + j] * FACT[l - i + k] * FACT[m - j + n - k]
                    s = s + cf * pu[i + j] * pw[l - i + k] * pv[m - j + n - k]
        out[(l, m, n)] = 2 * s
    return out

class Basis:
    def __init__(self, path):
        tok = open(path).read().split(); i = 0; self.kappa = 0; self.charges = [1, 1, -1]
        while True:
            k = tok[i]
            if k == 'L': self.L = int(tok[i + 1]); i += 2
            elif k == 'prec': i += 2
            elif k == 'masses': self.masses = tok[i + 1:i + 4]; i += 4
            elif k == 'charges': self.charges = [int(t) for t in tok[i + 1:i + 4]]; i += 4
            elif k == 'sym': self.kappa = int(tok[i + 1]); i += 2
            elif k == 'N': self.N = int(tok[i + 1]); i += 2; break
            else: raise ValueError(k)
        self.rows = []
        for n in range(self.N):
            r = tok[i:i + 7]; i += 7
            self.rows.append((int(r[0]), r[1:]))
        assert i == len(tok)
        self.cplx = any(arb(s) != 0 for _, r in self.rows for s in (r[1], r[3], r[5]))
    def setup(self):
        def inv(m):
            if m == 'inf': return arb(0)
            if '/' in m:
                n, dd = m.split('/'); return arb(dd) / arb(n)
            return 1 / arb(m)
        i1, i2, i3 = [inv(m) for m in self.masses]
        q1, q2, q3 = self.charges
        self.consts = (i1 + i3, i2 + i3, i3, arb(q1 * q3), arb(q2 * q3), arb(q1 * q2))
        self.funcs = derive(self.L)
        self.par = []
        for t, r in self.rows:
            if self.cplx: self.par.append((t, acb(arb(r[0]), arb(r[1])), acb(arb(r[2]), arb(r[3])), acb(arb(r[4]), arb(r[5]))))
            else: self.par.append((t, arb(r[0]), arb(r[2]), arb(r[4])))
    def exch(self, f):
        t, a, b, c = f; s = 1
        if self.L == 1:
            if t == 0: t = 1
            elif t == 1: t = 0
            else: s = -1
        else:
            if t == 0: t = 2
            elif t == 2: t = 0
        return (t, b, a, c), s
    def prim(self, f, h, conj):
        tb, a, b, c = f; tk, d, e, g = h
        if conj: a, b, c = a.conjugate(), b.conjugate(), c.conjugate()
        A, B, C = a + d, b + e, c + g
        for z in (A + B, A + C, B + C):
            assert (z.real if self.cplx else z) > 0, 'non-integrable pair'
        monS, fS, monH, fH = self.funcs[(tb, tk)]
        G = gammas(set(monS) | set(monH), A, B, C)
        cs = fS(a, b, c, d, e, g, *self.consts); ch = fH(a, b, c, d, e, g, *self.consts)
        S = sum((cf * G[m] for cf, m in zip(cs, monS)), 0 * A); H = sum((cf * G[m] for cf, m in zip(ch, monH)), 0 * A)
        return (S.real, H.real) if self.cplx else (S, H)
    def realel(self, f, h):
        if not self.cplx: return self.prim(f, h, False)
        s1, h1 = self.prim(f, h, False); s2, h2 = self.prim(f, h, True)
        return (s1 + s2) / 2, (h1 + h2) / 2
    def element(self, i, j):
        S, H = self.realel(self.par[i], self.par[j])
        if self.kappa:
            o, sg = self.exch(self.par[j]); s2, h2 = self.realel(self.par[i], o)
            S = S + self.kappa * sg * s2; H = H + self.kappa * sg * h2
        return S, H

def worker(job):
    path, prec, vecs, rows = job
    ctx.prec = prec
    B = Basis(path); B.setup()
    V = [[arb(s) for s in v] for v in vecs]; nv = len(V)
    acc = {(p, q): [arb(0), arb(0)] for p in range(nv) for q in range(p, nv)}
    for i in rows:
        for j in range(i + 1):
            S, H = B.element(i, j)
            for (p, q), ac in acc.items():
                if i == j: wgt = V[p][i] * V[q][i]
                elif p == q: wgt = 2 * V[p][i] * V[p][j]
                else: wgt = V[p][i] * V[q][j] + V[p][j] * V[q][i]
                ac[0] += wgt * S; ac[1] += wgt * H
    return {k: (str(v[0].mid()), str(v[0].rad()), str(v[1].mid()), str(v[1].rad())) for k, v in acc.items()}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('basis'); ap.add_argument('vecs', nargs='+')
    ap.add_argument('--bar'); ap.add_argument('--margin', default='0'); ap.add_argument('--prec', type=int, default=320)
    ap.add_argument('--procs', type=int, default=6)
    o = ap.parse_args(); ctx.prec = o.prec
    B = Basis(o.basis)
    vecs = [open(v).read().split() for v in o.vecs]
    for v in vecs: assert len(v) == B.N
    from multiprocessing import Pool
    order = list(range(B.N)); chunks = [order[k::o.procs * 4] for k in range(o.procs * 4)]
    with Pool(o.procs) as pool:
        parts = pool.map(worker, [(o.basis, o.prec, vecs, ch) for ch in chunks if ch])
    nv = len(vecs); Sm = {}; Hm = {}
    for part in parts:
        for k, (sm, sr, hm, hr) in part.items():
            Sm[k] = Sm.get(k, arb(0)) + arb(sm, sr); Hm[k] = Hm.get(k, arb(0)) + arb(hm, hr)
    print('basis', o.basis, 'L', B.L, 'N', B.N, 'sym', B.kappa, 'masses', *B.masses, 'complex', B.cplx, 'prec', o.prec)
    if nv == 1:
        assert Sm[(0, 0)] > 0
        E = Hm[(0, 0)] / Sm[(0, 0)]; what = 'Rayleigh quotient (upper bound on the lowest root of the block)'
    else:
        s11, s12, s22 = Sm[(0, 0)], Sm[(0, 1)], Sm[(1, 1)]; h11, h12, h22 = Hm[(0, 0)], Hm[(0, 1)], Hm[(1, 1)]
        assert s11 > 0 and s11 * s22 - s12 * s12 > 0, 'projected overlap not positive definite'
        qa = s11 * s22 - s12 * s12; qb = -(h11 * s22 + h22 * s11 - 2 * h12 * s12); qc = h11 * h22 - h12 * h12
        disc = qb * qb - 4 * qa * qc; assert disc > 0
        E = (-qb + disc.sqrt()) / (2 * qa); what = 'larger root of the 2x2 projected problem (upper bound on the second root of the block)'
        print('smaller root', ((-qb - disc.sqrt()) / (2 * qa)).str(40))
    print(what); print('enclosure:', E.str(50)); print('upper end (rounded to 45 digits):', E.upper().str(45, radius=False))
    if o.bar:
        thr = arb(o.bar) - arb(o.margin)
        ok = E < thr
        print('bar', o.bar, 'margin', o.margin, 'bar - upper end =', (arb(o.bar) - E.upper()).str(20))
        print('CERTIFIED: upper end < bar - margin' if ok else 'NOT CERTIFIED')
        sys.exit(0 if ok else 1)
if __name__ == '__main__':
    main()
