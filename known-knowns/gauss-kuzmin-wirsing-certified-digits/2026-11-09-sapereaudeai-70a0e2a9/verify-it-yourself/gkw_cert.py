#!/usr/bin/env python3
"""
V3R1T4S runs 2026-11-08-2057 / 2026-11-09-0627: rigorous enclosure of lambda_2 of the Gauss-Kuzmin-Wirsing operator
    (L f)(z) = sum_{n>=1} (z+n)^-2 f(1/(z+n))
on the Hardy space H^2(D), D = {|z - 3/5| < 4/5}, with orthonormal basis e_k = w^k, w = (z - 3/5)/(4/5).

Route (see claim/PROOF.md):
  (1) eigvec : approximate eigenvector v (degree N-1 in w) by a filtered power iteration in
               midpoint arithmetic on the section (non-rigorous; only finds an approximate object).
  (2) certify: everything below is arb ball arithmetic (python-flint) or a proved inequality.
     a. residual   eta >= ||(L - mu) v|| / ||v|| for the TRUE operator: coefficients of L v for
                   j < J computed exactly in balls, coefficients j >= J bounded analytically.
     b. truncation eps >= ||L - P_K L P_K|| (analytic sup bound for L(I-P_K) + matrix/tail bound
                   for (I-P_K) L P_K).
     c. resolvent  sup ||(P_K L P_K - z)^-1|| on the circles |z - mu| = r0 and |z| = rho, from
                   rigorous inverses at Q sample points plus the resolvent identity between them.
     d. counting   rigorous isolating enclosures of all eigenvalues of A_K = P_K L P_K (acb_mat.eig).
     e. enclosure  |lambda - mu| <= r0 M eta / (1 - M (1 + r0 M) eta),  M = M_K / (1 - eps M_K).
Usage:
  python gkw_cert.py eigvec  N PREC CYCLES OUT.txt [INIT.txt|- [THREADS [MUOUT.txt]]]
         (2026-11-09: memory-lean section build, optional warm start from a shorter vector INIT.txt;
          2026-11-09-0757: P applied by exact polynomial composition; MUOUT receives the Rayleigh quotient of v)
  python gkw_cert.py certify VFILE MUFILE K PREC J R0 RHO Q2 QRHO OUT.json
"""
import sys, json, time
from flint import arb, acb, arb_mat, acb_mat, fmpz, fmpq, fmpz_poly, ctx

C = fmpq(3, 5)      # centre
R = fmpq(4, 5)      # radius
A1 = fmpq(8, 5)     # 1 + c : Hurwitz parameter


def A(q):
    """exact rational -> arb ball (rigorous)"""
    return arb(q)


def zeta_list(smax):
    """Z[s] = zeta(s, 8/5) for 2 <= s <= smax (arb Hurwitz zeta, rigorous)"""
    a = arb(8) / 5
    Z = [None, None]
    for s in range(2, smax + 1):
        Z.append(arb(s).zeta(a))
    return Z


def fact_list(nmax):
    F = [arb(1)]
    for i in range(1, nmax + 1):
        F.append(F[-1] * i)
    return F


def hankel_h(smax_index, Z, F):
    """h[s] = (s+1)! * zeta(s+2, 8/5), s = 0..smax_index"""
    return [F[s + 1] * Z[s + 2] for s in range(smax_index + 1)]


def w_to_monomial(v):
    """p_m with sum_k v_k ((u-c)/R)^k = sum_m p_m u^m.  Rigorous (balls).
    Taylor shift of v(t) by beta = -c/R = -3/4, then scale t = u/R."""
    n = len(v)
    beta = arb(-3) / 4
    p = list(v)
    # synthetic division: coefficients of v(t + beta)
    for i in range(n):
        for k in range(n - 2, i - 1, -1):
            p[k] = p[k] + beta * p[k + 1]
    alpha = arb(5) / 4
    s = arb(1)
    for m in range(n):
        p[m] = p[m] * s
        s = s * alpha
    return p


def P_matrix(n):
    """P[m][k] = coefficient of u^m in ((u-c)/R)^k = binom(k,m) (-c)^(k-m) R^(-k) (exact rationals)"""
    rows = [[fmpq(0)] * n for _ in range(n)]
    for k in range(n):
        Rk = (fmpq(5, 4)) ** k
        b = fmpz(1)
        for m in range(k, -1, -1):
            # binom(k, m) with m from k down: binom(k,m-1) = binom(k,m)*m/(k-m+1)
            rows[m][k] = fmpq(b) * (fmpq(-3, 5) ** (k - m)) * Rk
            if m > 0:
                b = b * m // (k - m + 1)
    return arb_mat([[arb(x) for x in r] for r in rows])


def Lcoeffs_from_monomial(p, J, h, F):
    """(L v)_j in the w-basis for j < J, where v(u) = sum_m p_m u^m. Rigorous.
    (Lv)(z) = sum_m p_m zeta(m+2, z+1);  coefficient of (z-c)^j of zeta(m+2,z+1) is
    (-1)^j binom(m+1+j, j) zeta(m+2+j, 1+c) = (-1)^j/j! * h[m+j] / (m+1)!.  Times R^j for w."""
    n = len(p)
    q = arb_mat(n, 1, [p[m] / F[m + 1] for m in range(n)])
    out = []
    Rr = arb(4) / 5
    chunk = 256
    j0 = 0
    Rj = arb(1)
    while j0 < J:
        j1 = min(J, j0 + chunk)
        Hm = arb_mat([[h[j + m] for m in range(n)] for j in range(j0, j1)])
        S = Hm * q
        for t, j in enumerate(range(j0, j1)):
            val = S[t, 0] * Rj / F[j]
            if j % 2:
                val = -val
            out.append(val)
            Rj = Rj * Rr
        j0 = j1
    return out


def zeta_tail_kappa(sigma0):
    """kappa >= zeta(sigma, a) * a^sigma for all sigma >= sigma0, a = 8/5 (proved bound, Lemma 6):
    zeta(s,a) <= a^-s [1 + (a/(1+a))^s (1 + (1+a)/(s-1))], decreasing in s."""
    a = arb(8) / 5
    s = arb(sigma0)
    return 1 + (a / (1 + a)) ** s * (1 + (1 + a) / (s - 1))


def tail_l1_factor(m, J, kappa):
    """Upper bound for T_m(J) = sum_{j>=J} binom(m+1+j, j) R^j zeta(m+j+2, 1+c)  (needs m < J).
    T <= kappa (1+c)^-(m+2) binom(m+1+J, J) (R/(1+c))^J / (1 - q),  q = (m+2+J)/(2(J+1))."""
    assert m < J
    b = arb.bin_uiui(m + 1 + J, J)
    q = arb(m + 2 + J) / (2 * (J + 1))
    return kappa * (arb(5) / 8) ** (m + 2) * b * (arb(1) / 2) ** J / (1 - q)


def load_vec(path):
    v = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            man, ex = line.split()
            v.append(arb(fmpz(int(man))) * arb(2) ** int(ex))   # exact dyadic
    return v


def save_vec(path, v, header):
    with open(path, 'w') as f:
        f.write('# ' + header + '\n')
        for x in v:
            man, ex = x.mid().man_exp()
            f.write('%s %s\n' % (man, ex))


# ---------------------------------------------------------------- (1) approximate eigenvector
def compose_P(x, N, S):
    """y = P x, P[m][k] = binom(k, m) (-3/5)^(k-m) (5/4)^k, i.e. y(u) = sum_k x_k ((5u - 3)/4)^k, computed exactly in
    integers (fmpz_poly composition) after rounding each x_k to the fixed-point grid 2^-S 4^-(N-1-k); midpoint result.
    Non-rigorous helper of eigvec only (2026-11-09-0757: replaces the stored N x N matrix P, saving memory)."""
    xi = []
    for k in range(N):
        man, ex = x[k, 0].mid().man_exp()
        sh = int(ex) + S + 2 * (N - 1 - k)
        m = int(man)
        xi.append(m << sh if sh >= 0 else (m >> (-sh) if m >= 0 else -((-m) >> (-sh))))
    Y = fmpz_poly(xi)(fmpz_poly([-3, 5]))
    co = Y.coeffs()
    scale = arb(2) ** (-(S + 2 * (N - 1)))
    y = arb_mat(N, 1)
    for m in range(min(N, len(co))):
        y[m, 0] = (arb(co[m]) * scale).mid()
    return y


def cmd_eigvec(N, prec, cycles, out, init=None, threads=1, muout=None):
    """Non-rigorous: finds an approximate eigenvector only (midpoint arithmetic). Memory-lean: B is built in place as
    a midpoint matrix; since 2026-11-09-0757 the factor P is applied by exact integer polynomial composition
    (compose_P) instead of a stored matrix. If muout is given, the Rayleigh quotient mu = <v, Mv>/<v, v> of the final
    v for the section M = B P is written there in decimal at the working precision (it is only a proposed centre;
    the certificate checks whatever centre it is given)."""
    ctx.prec = prec
    ctx.threads = threads
    t0 = time.time()
    Z = zeta_list(2 * N + 2)
    F = fact_list(2 * N + 2)
    h = hankel_h(2 * N, Z, F)
    Finv = [1 / F[m + 1] for m in range(N)]
    # B[j][m] = (-1)^j R^j / j! * h[j+m] / (m+1)!   (w-row j, monomial column m)
    B = arb_mat(N, N)
    Rr = arb(4) / 5
    Rj = arb(1)
    for j in range(N):
        fac = Rj / F[j]
        if j % 2:
            fac = -fac
        for m in range(N):
            B[j, m] = (h[j + m] * (Finv[m] * fac)).mid()
        Rj = Rj * Rr
    del Z, h
    S = prec + 64
    print('setup %.1fs' % (time.time() - t0), flush=True)
    # filter roots (approximate eigenvalues 1, l3, l4, l5, l6; values only steer the iteration)
    roots = [arb(1), arb('0.100884509293104'), arb('-0.0354961590216598'),
             arb('0.0128437903624403'), arb('-0.00471777751157104')]
    v = arb_mat(N, 1)
    if init:
        v0 = load_vec(init)
        assert len(v0) <= N
        for i, x in enumerate(v0):
            v[i, 0] = x
        print('warm start from %s (%d coefficients)' % (init, len(v0)), flush=True)
    else:
        v[0, 0] = arb(1)
    def mv(x):
        y = B * compose_P(x, N, S)
        return y.mid()
    for cyc in range(cycles):
        for r in roots:
            v = (mv(v) - v * r).mid()
        nrm = abs(v[0, 0])
        v = (v * (1 / nrm)).mid()
        if cyc % 5 == 0 or cyc == cycles - 1:
            Lv = mv(v)
            mu = (Lv[0, 0] / v[0, 0])
            res = Lv - v * mu
            s = sum((res[i, 0] ** 2 for i in range(N)), arb(0)).sqrt()
            print('cycle %d  mu %s  section-residual %s  t=%.0fs' % (cyc, mu.mid().str(30, radius=False),
                  s.mid().str(5, radius=False), time.time() - t0), flush=True)
    vv = [v[i, 0].mid() for i in range(N)]
    save_vec(out, vv, 'approximate lambda_2 eigenvector, w-basis, N=%d prec=%d cycles=%d init=%s' % (
        N, prec, cycles, init if init is None else init.replace(chr(92), '/').split('/')[-1]))
    print('saved', out, 'time %.1fs' % (time.time() - t0))
    if muout:
        Lv = mv(v)
        num = sum((v[i, 0] * Lv[i, 0] for i in range(N)), arb(0))
        den = sum((v[i, 0] ** 2 for i in range(N)), arb(0))
        muR = (num / den).mid()
        nd = int(prec * 0.30103) - 20
        with open(muout, 'w') as f:
            f.write(muR.str(nd, radius=False) + '\n')
            f.write('# Rayleigh quotient <v, Mv>/<v, v> of %s for the N=%d section M = B P, midpoint arithmetic at %d bits, '
                    '%d significant digits; a proposed centre only (proves nothing)\n' % (
                        out.replace(chr(92), '/').split('/')[-1], N, prec, nd))
        print('mu (Rayleigh quotient, %d digits) saved to %s; first 40: %s' % (nd, muout, muR.str(40, radius=False)),
              flush=True)


# ---------------------------------------------------------------- (2) certification
def frob_upper(M, r0=0, r1=None, c0=0, c1=None):
    r1 = M.nrows() if r1 is None else r1
    c1 = M.ncols() if c1 is None else c1
    s = arb(0)
    for i in range(r0, r1):
        for j in range(c0, c1):
            u = abs(M[i, j]).upper() if isinstance(M, arb_mat) else M[i, j].abs_upper()
            s += arb(u) ** 2
    return arb(s.upper()).sqrt().upper()


def resolvent_circle(AK, center, radius, Q, prec_inv):
    """Upper bound for sup_{|z-center|=radius} ||(L_K - z)^-1|| where L_K = A_K (+) 0 on H^2.
    At Q equally spaced points z_i: m_i >= max(||(A_K - z_i)^-1||_F, 1/|z_i|) (rigorous inverse);
    between points ||R(z)|| <= m_i / (1 - delta m_i), delta = 2 radius sin(pi/(2Q)) (resolvent identity)."""
    old = ctx.prec
    ctx.prec = prec_inv
    K = AK.nrows()
    Ac = acb_mat(AK)
    pi = arb.pi()
    delta = (2 * arb(radius) * (pi / (2 * Q)).sin())
    worst = arb(0)
    worst_pt = None
    for i in range(Q):
        th = 2 * pi * i / Q
        z = acb(center) + acb(radius) * acb(th.cos(), th.sin())
        Mz = Ac - acb_mat(K, K, [z if a == b else 0 for a in range(K) for b in range(K)])
        X = Mz.inv()
        s = arb(0)
        for a in range(K):
            for b in range(K):
                s += arb(X[a, b].abs_upper()) ** 2
        m = arb(s.upper()).sqrt()
        m = arb(m.upper())
        invz = arb((1 / abs(z)).upper())
        if invz > m:
            m = invz
        dm = delta * m
        if not (dm < 1):
            ctx.prec = old
            return None, float(m.upper()), i
        b = arb((m / (1 - dm)).upper())
        if b > worst:
            worst = b
            worst_pt = i
    ctx.prec = old
    return arb(worst.upper()), None, worst_pt


def cmd_certify(vfile, mufile, K, prec, J, r0s, rhos, Q2, Qr, out):
    ctx.prec = prec
    t0 = time.time()
    log = {}
    v = load_vec(vfile)
    N = len(v)
    mu_str = open(mufile).read().split()[0]
    mu = arb(mu_str).mid()          # exact dyadic centre mu
    r0 = arb(r0s).mid()
    rho = arb(rhos).mid()
    assert J > N + 1 and K < N
    Smax = N + J + 2
    Z = zeta_list(Smax)
    F = fact_list(Smax + 1)
    h = hankel_h(N + J, Z, F)
    print('tables %.1fs' % (time.time() - t0), flush=True)

    # ---- (a) residual of the true operator
    p = w_to_monomial(v)
    Lv = Lcoeffs_from_monomial(p, J, h, F)
    s_in = arb(0)
    for j in range(J):
        rj = Lv[j] - mu * v[j] if j < N else Lv[j]
        s_in += rj ** 2
    res_head = s_in.sqrt()
    kappa = zeta_tail_kappa(J + 2)
    tail = arb(0)
    for m in range(N):
        tail += arb(abs(p[m]).upper()) * tail_l1_factor(m, J, kappa)
    res_norm = arb((res_head + tail).upper())
    vnorm2 = sum((x ** 2 for x in v), arb(0))
    vnorm_lo = arb(vnorm2.lower()).sqrt()
    vnorm_lo = arb(vnorm_lo.lower())
    eta = arb((res_norm / vnorm_lo).upper())
    log.update(N=N, J=J, prec=prec, mu=mu_str[:80] + '...', res_head=res_head.str(5), res_tail=tail.str(5),
               eta=eta.str(5), vnorm_lower=vnorm_lo.str(10), kappa=kappa.str(10))
    print('residual: head %s tail %s eta %s  (%.1fs)' % (res_head.str(5), tail.str(5), eta.str(5),
                                                          time.time() - t0), flush=True)

    # ---- (b) section A_K and truncation bound eps
    J0 = max(6 * K, 200)
    PK = P_matrix(K)
    Rr = arb(4) / 5
    Brows = []
    Rj = arb(1)
    for j in range(J0):
        sgn = -1 if j % 2 else 1
        fac = Rj / F[j] * sgn
        Brows.append([h[j + m] / F[m + 1] * fac for m in range(K)])
        Rj = Rj * Rr
    BK = arb_mat(Brows)
    AJ0 = BK * PK                    # (L e_k)_j, j < J0, k < K   (rigorous)
    AK = arb_mat([[AJ0[i, k] for k in range(K)] for i in range(K)])
    epsb_mid = frob_upper(AJ0, K, J0, 0, K)
    kappa0 = zeta_tail_kappa(J0 + 2)
    tails = [arb(0)] * K
    tf = [tail_l1_factor(m, J0, kappa0) for m in range(K)]
    sq = arb(0)
    for k in range(K):
        t = arb(0)
        for m in range(k + 1):
            t += arb(abs(PK[m, k]).upper()) * tf[m]
        sq += t ** 2
    epsb_tail = arb(sq.upper()).sqrt()
    # analytic bound for ||L (I - P_K)||  (Lemma 4)
    rho1 = arb(13) / 16
    rhoinf = arb(3) / 4
    epsa = (arb(25) / 16) * rho1 ** K / (1 - rho1 ** 2).sqrt() + (arb(10) / 13) * rhoinf ** K / (1 - rhoinf ** 2).sqrt()
    eps = arb((epsa + arb(epsb_mid) + epsb_tail).upper())
    normAK = frob_upper(AK)
    log.update(K=K, J0=J0, eps_a=epsa.str(5), eps_b_rows=arb(epsb_mid).str(5), eps_b_tail=epsb_tail.str(5),
               eps=eps.str(5), AK_frobenius=arb(normAK).str(8))
    print('eps: a %s  b_rows %s  b_tail %s  total %s  (%.1fs)' % (epsa.str(3), arb(epsb_mid).str(3),
          epsb_tail.str(3), eps.str(3), time.time() - t0), flush=True)

    # ---- (d) eigenvalues of A_K, rigorous isolation
    ctx.prec = 2 * prec // 3
    E = acb_mat(AK).eig()
    ctx.prec = prec
    # acb_mat.eig raises if it cannot isolate K simple eigenvalues; check the count explicitly as well
    if len(E) != K:
        raise SystemExit('eig returned %d eigenvalues, expected K = %d' % (len(E), K))
    inside2 = []   # eigenvalues certainly inside |z - mu| < r0
    outside_rho = []
    for e in E:
        d2 = abs(e - acb(mu))
        if d2 < r0:
            inside2.append(e)
        elif not (d2 > r0):
            raise SystemExit('eigenvalue ball straddles Gamma_2: %s' % e)
        de = abs(e)
        if de > rho:
            outside_rho.append(e)
        elif not (de < rho):
            raise SystemExit('eigenvalue ball straddles |z|=rho: %s' % e)
    log.update(n_eig_total=len(E), n_eig_inside_Gamma2=len(inside2), n_eig_outside_rho=len(outside_rho),
               eig_inside_Gamma2=[e.str(40) for e in inside2], eig_outside_rho=[e.str(20) for e in outside_rho])
    print('A_K: %d eigenvalues in Gamma_2, %d with |z|>rho: %s' % (len(inside2), len(outside_rho),
          [e.str(12) for e in outside_rho]), flush=True)

    # ---- (c) resolvent bounds
    M2K, fail, wpt = resolvent_circle(AK, mu, r0, Q2, 320)
    if M2K is None:
        raise SystemExit('Gamma_2 sampling too coarse: m=%g at %d' % (fail, wpt))
    MrK, fail, wpt2 = resolvent_circle(AK, arb(0), rho, Qr, 320)
    if MrK is None:
        raise SystemExit('Gamma_rho sampling too coarse: m=%g at %d' % (fail, wpt2))
    g2 = eps * M2K
    gr = eps * MrK
    if not (g2 < 1 and gr < 1):
        raise SystemExit('small-gain fails: M_K(G2)=%s M_K(rho)=%s eps=%s' % (M2K.str(4), MrK.str(4), eps.str(4)))
    M2 = arb((M2K / (1 - g2)).upper())
    Mr = arb((MrK / (1 - gr)).upper())
    Rbig = normAK + eps + 1
    log.update(M_K_Gamma2=M2K.str(6), M_K_rho=MrK.str(6), smallgain_Gamma2=g2.str(4), smallgain_rho=gr.str(4),
               M_L_Gamma2=M2.str(6), M_L_rho=Mr.str(6), r0=r0s, rho=rhos, Q2=Q2, Qrho=Qr)
    print('resolvent: M_K(G2) %s  M_K(rho) %s  gains %s %s (%.1fs)' % (M2K.str(4), MrK.str(4), g2.str(3),
          gr.str(3), time.time() - t0), flush=True)

    # ---- (e) enclosure
    denom = 1 - M2 * (1 + r0 * M2) * eta
    assert denom > 0
    rad = arb((r0 * M2 * eta / denom).upper())
    import math
    l10 = rad.log() / arb(10).log()
    D = int(math.floor(-float(l10.upper())))  # radius < 10^-D  (checked exactly below)
    while not (rad < arb(10) ** (-D)):
        D -= 1
    ok_count = (len(inside2) == 1 and len(outside_rho) == 2 and (abs(mu) - r0) > rho)
    log.update(radius=rad.str(6), certified_D=D, isolation_ok=ok_count, time_s=round(time.time() - t0, 1))
    log['C83_enclosure_mid'] = (-mu).str(D + 15, radius=False)
    print('RESULT: |lambda - mu| <= %s  ->  D = %d certified decimals; isolation/counting ok = %s' % (
        rad.str(5), D, ok_count), flush=True)
    with open(out, 'w') as f:
        json.dump(log, f, indent=1)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'eigvec':
        init = sys.argv[6] if len(sys.argv) > 6 and sys.argv[6] != '-' else None
        thr = int(sys.argv[7]) if len(sys.argv) > 7 else 1
        muo = sys.argv[8] if len(sys.argv) > 8 else None
        cmd_eigvec(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], init, thr, muo)
    elif cmd == 'certify':
        a = sys.argv[2:]
        cmd_certify(a[0], a[1], int(a[2]), int(a[3]), int(a[4]), a[5], a[6], int(a[7]), int(a[8]), a[9])
