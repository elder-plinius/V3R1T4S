"""Certifier lens: independent exact certificate for three-player von Neumann poker (arXiv:2407.16155 Sec. 4).

Game: antes 1 each, hands x (I), y (II), z (III) iid uniform(0,1). I checks (3-way showdown, pot 3) or bets b.
After a bet, II and III each call or fold, each seeing only own hand. Highest hand among non-folders takes the pot.
Profile: I bets iff x<A or x>B; II, III call iff hand > C; 0<A<C<B<1 solving Eq. A-C.

Part 1 derives closed-form action payoffs by hand and checks them against an exact cell integrator built from
terminal pot utilities (Fractions) at random rational points. Part 2 proves the sign conditions symbolically for all
b>0 given an ordered solution. Part 3 proves existence/uniqueness of the ordered solution for every b>0.
Part 4 computes the b=2 thresholds and value exactly (algebraic, isolating intervals) and compares printed digits.
"""
import random
from fractions import Fraction as F
import sympy as sp

b, A, B, C, x, y = sp.symbols('b A B C x y', real=True)

# ---------------- closed forms (hand-derived) ----------------
def EI_check(x):
    return 3 * x**2 - 1

def EI_bet(x, A_, B_, C_, b_):
    u = sp.Max(0, x - C_)
    return (2 * C_**2 + 2 * C_ * (u * (3 + 2 * b_) - (1 - C_) * (1 + b_))
            + 3 * (1 + b_) * u**2 - (1 - C_)**2 * (1 + b_))

def DII(y, A_, B_, C_, b_):
    """II's E[call] - E[fold] (only differs when I bets), III fixed at threshold C."""
    m = sp.Min(y, A_) + sp.Max(0, y - B_)
    return m * ((3 + 2 * b_) * C_ + (3 + 3 * b_) * sp.Max(0, y - C_)) - b_ * (A_ + 1 - B_)

# ---------------- exact cell integrator from terminal utilities ----------------
def terminal(xh, yh, zh, Ibet, IIcall, IIIcall, b_):
    """Net payoffs (I, II, III) at a terminal node. Ties are measure zero; break arbitrarily (not used on boundaries)."""
    if not Ibet:
        w = max((xh, 0), (yh, 1), (zh, 2))[1]
        return tuple(2 if i == w else -1 for i in range(3))
    stake = [1 + b_, 1 + (b_ if IIcall else 0), 1 + (b_ if IIIcall else 0)]
    live = [(xh, 0)] + ([(yh, 1)] if IIcall else []) + ([(zh, 2)] if IIIcall else [])
    w = max(live)[1]
    pot = sum(stake)
    return tuple((pot - stake[i]) if i == w else -stake[i] for i in range(3))

def expect(player, own, action, A_, B_, C_, b_):
    """Exact E[payoff of `player` with hand `own` taking `action`], others follow the profile.
    Opponent hands split at every breakpoint; within a pair of cells the outcome depends only on the order of the
    two opponent hands, which is split by area (cells identical -> half each)."""
    pts = sorted(set([F(0), F(1), A_, B_, C_, own]))
    cells = [(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot = F(0)
    for (a1, a2) in cells:
        for (c1, c2) in cells:
            area = (a2 - a1) * (c2 - c1)
            p = (a1 + a2) / 2  # representative of opponent 1
            q = (c1 + c2) / 2  # representative of opponent 2
            if (a1, a2) == (c1, c2):
                orders = [(area / 2, p, p + (a2 - a1) / 4), (area / 2, p + (a2 - a1) / 4, p)]
            else:
                orders = [(area, p, q)]
            for (w, s, t) in orders:
                if player == 0:
                    xh, yh, zh = own, s, t
                    Ibet = action
                elif player == 1:
                    xh, yh, zh = s, own, t
                    Ibet = (xh < A_) or (xh > B_)
                else:
                    xh, yh, zh = s, t, own
                    Ibet = (xh < A_) or (xh > B_)
                if player != 0 and not Ibet:
                    pay = terminal(xh, yh, zh, False, False, False, b_)
                else:
                    IIc = action if player == 1 else (yh > C_)
                    IIIc = action if player == 2 else (zh > C_)
                    pay = terminal(xh, yh, zh, Ibet, IIc, IIIc, b_)
                tot += w * pay[player]
    return tot

def part1(trials=400, seed=20261015):
    rng = random.Random(seed)
    worst = 0
    for t in range(trials):
        cuts = sorted(F(rng.randint(1, 997), 1000) for _ in range(3))
        A_, C_, B_ = cuts  # any ordered thresholds (equations not needed for the payoff formulas)
        if len(set(cuts)) < 3:
            continue
        b_ = F(rng.randint(1, 4000), rng.randint(1, 1000))
        h = F(rng.randint(1, 9999), 10000)
        if h in (A_, B_, C_):
            continue
        # Player I
        bet = expect(0, h, True, A_, B_, C_, b_)
        chk = expect(0, h, False, A_, B_, C_, b_)
        assert bet == sp.Rational(EI_bet(sp.Rational(h), sp.Rational(A_), sp.Rational(B_), sp.Rational(C_), sp.Rational(b_))), (t, 'Ibet')
        assert chk == EI_check(h), (t, 'Icheck')
        # Players II and III
        for pl in (1, 2):
            d = expect(pl, h, True, A_, B_, C_, b_) - expect(pl, h, False, A_, B_, C_, b_)
            assert sp.Rational(d) == DII(sp.Rational(h), sp.Rational(A_), sp.Rational(B_), sp.Rational(C_), sp.Rational(b_)), (t, pl)
        worst += 1
    print('PART1 closed forms == exact cell integrator at', worst, 'random rational (A<C<B, b, hand) points, players I, II, III')

# ---------------- Part 2: sign conditions for all b>0 given ordered solution ----------------
EqA = sp.Eq(3 * A**2 - 1, 3 * C**2 + b * C**2 - b - 1)
EqB = sp.Eq(3 * B**2 - 1, -2 * b * C * B + 3 * b * B**2 + 3 * B**2 - b - 1)
EqC = sp.Eq(-A + B - 1, 2 * b * C * A + 3 * C * A - b * A - A - b + b * B + B - 1)

def part2():
    # Player I on (0, C]: u = 0
    K = sp.expand(EI_bet(x, A, B, C, b).subs(sp.Max(0, x - C), 0))
    assert sp.expand(K - (3 * C**2 + b * C**2 - b - 1)) == 0
    DI_low = sp.expand(K - EI_check(x))
    # with Eq. A: K = 3A^2 - 1, so DI_low = 3(A^2 - x^2)
    DI_low_A = sp.expand(DI_low.subs(b * C**2, 3 * A**2 - 3 * C**2 + b))
    assert sp.expand(DI_low_A - 3 * (A**2 - x**2)) == 0
    print('PART2 I on (0,C]: D_I(x) = 3(A^2 - x^2) under Eq. A  [>0 on (0,A), <0 on (A,C)]')
    # Player I on [C, 1): u = x - C
    Q = sp.expand(EI_bet(x, A, B, C, b).subs(sp.Max(0, x - C), x - C) - EI_check(x))
    assert sp.Poly(Q, x).LC() == 3 * b
    # Eq. B simplifies to b*(3B^2 - 2CB - 1) = 0
    assert sp.factor(sp.expand(EqB.lhs - EqB.rhs)) in (-b * (3 * B**2 - 2 * B * C - 1), b * (-3 * B**2 + 2 * B * C + 1))
    QB = sp.expand(Q.subs(x, B))
    rem = sp.rem(sp.Poly(QB, B), sp.Poly(3 * B**2 - 2 * C * B - 1, B))
    assert sp.expand(rem.as_expr()) == 0, rem
    # So Q(B)=0; Q(x) = (x - B)(3b x + k) with k determined; Q(C) = D_I(C) = 3(A^2 - C^2) < 0 (continuity of D_I at C)
    k = sp.symbols('k')
    sol = sp.solve(sp.Poly(sp.expand(Q - (x - B) * (3 * b * x + k)), x).all_coeffs()[-2], k)
    kk = sol[0]
    resid = sp.expand(Q - (x - B) * (3 * b * x + kk))
    resid = sp.rem(sp.Poly(resid, B), sp.Poly(3 * B**2 - 2 * C * B - 1, B)).as_expr()
    assert sp.simplify(resid) == 0, resid
    QC = sp.expand(Q.subs(x, C))
    assert sp.expand(QC - DI_low.subs(x, C)) == 0
    print('PART2 I on [C,1): D_I(x) = (x-B)(3b x + k), k =', sp.factor(kk))
    print('       D_I(C) = (C-B)(3bC+k) = 3(A^2-C^2) < 0 and C<B  => 3bC+k > 0 => 3bx+k > 0 on (C,1)')
    print('       => D_I < 0 on (C,B), > 0 on (B,1)')
    # Player II (III symmetric)
    pieces = {
        '(0,A)': (y, 0),
        '(A,C)': (A, 0),
        '(C,B)': (A, y - C),
        '(B,1)': (A + y - B, y - C),
    }
    for name, (m, mx) in pieces.items():
        expr = sp.expand(m * ((3 + 2 * b) * C + (3 + 3 * b) * mx) - b * (A + 1 - B))
        print('PART2 II on', name, ': D_II =', sp.factor(expr))
    # Eq. C <=> (3+2b) C A = b (A + 1 - B)
    assert sp.expand((EqC.lhs - EqC.rhs) + ((3 + 2 * b) * C * A - b * (A + 1 - B))) == 0
    print('       Eq. C <=> (3+2b)CA = b(A+1-B). Hence D_II = (3+2b)C(y-A) <0 on (0,A); = 0 on (A,C];')
    print('       on (C,B): A(3+3b)(y-C) > 0; on (B,1): (y-B)(3+2b)C + (A+y-B)(3+3b)(y-C) > 0.')

# ---------------- Part 3: existence and uniqueness of the ordered solution, all b>0 ----------------
def part3():
    c = sp.symbols('c', positive=True)
    bp = sp.symbols('beta', positive=True)
    Bc = (c + sp.sqrt(c**2 + 3)) / 3          # positive root of 3B^2 - 2cB - 1 = 0
    L2 = ((3 + bp) * c**2 - bp) / 3           # A^2 from Eq. A
    c0sq = bp / (3 + bp)
    # denominator (3+2b)c - b > 0 on [c0, 1]: c0 > b/(3+2b)  <=>  c0^2 > b^2/(3+2b)^2
    diff = sp.factor(sp.together(c0sq - bp**2 / (3 + 2 * bp)**2))
    print('PART3 c0^2 - (b/(3+2b))^2 =', diff)
    num, den = sp.fraction(diff)
    assert all(t.is_positive for t in sp.Poly(sp.expand(num), bp).coeffs()) or sp.expand(num).is_positive
    # B(c) increasing: derivative
    dB = sp.diff(Bc, c)
    print('PART3 dB/dc =', sp.simplify(dB), '(>0 since c/sqrt(c^2+3) > -1)')
    # R(c) = b(1-B(c))/((3+2b)c - b): numerator decreasing, positive for c<1 (B(1) = 1), denominator increasing positive
    assert sp.simplify(Bc.subs(c, 1) - 1) == 0
    # L(c) increasing from 0 (c=c0) to 1 (c=1)
    assert sp.simplify(L2.subs(c, 1) - 1) == 0 and sp.simplify(L2.subs(c, sp.sqrt(c0sq))) == 0
    # Ordering: A<C <=> L2 < c^2 <=> b(c^2-1) < 0 ; C<B <=> sqrt(c^2+3) > 2c <=> c<1
    assert sp.expand(L2 - c**2 - bp * (c**2 - 1) / 3) == 0
    print('PART3 A^2 - C^2 = b(C^2-1)/3 < 0 for C<1;  B - C = (sqrt(C^2+3) - 2C)/3 > 0 for C<1;  B(C) < 1 for C<1.')
    print('PART3 => unique crossing C* in (c0,1) of increasing L and decreasing R gives the unique ordered solution.')

# ---------------- Part 4: b = 2 exact ----------------
def part4(digits=60):
    bb = sp.Integer(2)
    c = sp.symbols('c')
    Bv = sp.symbols('Bv')
    # eliminate: Eq.B: 3Bv^2 - 2c Bv - 1 = 0 ; Eq.A: 3A^2 = (3+b)c^2 - b ; Eq.C: A((3+2b)c - b) = b(1-Bv)
    a = sp.symbols('a')
    e1 = 3 * Bv**2 - 2 * c * Bv - 1
    e2 = 3 * a**2 - (3 + bb) * c**2 + bb
    e3 = a * ((3 + 2 * bb) * c - bb) - bb * (1 - Bv)
    r1 = sp.resultant(e2, e3, a)       # in c, Bv
    r2 = sp.resultant(r1, e1, Bv)       # in c
    pc = sp.factor_list(sp.Poly(r2, c))
    print('PART4 b=2 resultant factors in C:', [(sp.Poly(f, c).degree(), m) for f, m in pc[1]])
    cands = []
    for f, m in pc[1]:
        P = sp.Poly(f, c)
        for ((lo, hi), _mult) in P.intervals(eps=sp.Rational(1, 10**40)):
            lo, hi = sp.Rational(lo), sp.Rational(hi)
            if hi < 0 or lo > 1:
                continue
            cr = sp.CRootOf(P, [r for r in range(P.degree()) if sp.CRootOf(P, r).is_real and lo <= sp.CRootOf(P, r).evalf(50) <= hi][0])
            cands.append((P, cr, lo, hi))
    sols = []
    for P, cr, lo, hi in cands:
        cv = cr.evalf(digits + 20)
        Bvv = (cv + sp.sqrt(cv**2 + 3)) / 3
        if (3 + bb) * cv**2 - bb <= 0:
            continue
        av = sp.sqrt(((3 + bb) * cv**2 - bb) / 3)
        if abs(av * ((3 + 2 * bb) * cv - bb) - bb * (1 - Bvv)) < sp.Float(10)**(-digits):
            if 0 < av < cv < Bvv < 1:
                sols.append((P, lo, hi, av, Bvv, cv))
    assert len(sols) == 1, len(sols)
    P, lo, hi, av, Bvv, cv = sols[0]
    print('PART4 minimal polynomial of C (b=2):', P.as_expr())
    print('PART4 isolating interval for C: [', lo, ',', hi, ']  width', sp.N(hi - lo, 3))
    # value to I
    Kc = 3 * av**2 - 1
    Ebet_hi = lambda t: (2 * cv**2 + 2 * cv * ((t - cv) * (3 + 2 * bb) - (1 - cv) * (1 + bb))
                         + 3 * (1 + bb) * (t - cv)**2 - (1 - cv)**2 * (1 + bb))
    tt = sp.symbols('tt')
    V = Kc * av + sp.integrate(3 * tt**2 - 1, (tt, av, Bvv)) + sp.integrate(sp.expand(Ebet_hi(tt)), (tt, Bvv, 1))
    V = sp.N(V, digits)
    print('PART4 A =', sp.N(av, 45))
    print('PART4 B =', sp.N(Bvv, 45))
    print('PART4 C =', sp.N(cv, 45))
    print('PART4 V =', sp.N(V, 45))
    for name, val, printed in (('A', av, '0.137058194328370'), ('B', Bvv, '0.829422249795391'),
                               ('C', cv, '0.641304115985175'), ('V', V, '0.122557074714865')):
        r15 = sp.Float(val, 40).round(15)
        print('PART4 %s rounded to 15 dp: %s ; printed %s ; match: %s ; |diff| = %s' % (
            name, sp.N(r15, 16), printed, abs(sp.Float(val, 40) - sp.Float(printed, 40)) < sp.Float('5e-16'),
            sp.N(abs(sp.Float(val, 40) - sp.Float(printed, 40)), 3)))
    # two-player sanity is not applicable here; instead check Eq. A-C residuals
    print('PART4 residuals:', [sp.N(e, 5) for e in (
        3 * av**2 - 1 - (3 * cv**2 + bb * cv**2 - bb - 1),
        3 * Bvv**2 - 1 - (-2 * bb * cv * Bvv + 3 * bb * Bvv**2 + 3 * Bvv**2 - bb - 1),
        -av + Bvv - 1 - (2 * bb * cv * av + 3 * cv * av - bb * av - av - bb + bb * Bvv + Bvv - 1))])

if __name__ == '__main__':
    part1()
    part2()
    part3()
    part4()
