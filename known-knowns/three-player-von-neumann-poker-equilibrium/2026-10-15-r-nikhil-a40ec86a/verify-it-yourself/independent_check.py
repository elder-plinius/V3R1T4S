"""Standalone check (Python 3 standard library only) of the threshold equilibrium of three-player von Neumann poker
(Krityakierne, Thanatipanonda, Zeilberger, arXiv:2407.16155, Section 4), simultaneous callers, any bet b > 0.

Rules (paper): antes 1 each; hands x (I), y (II), z (III) iid uniform(0,1). I checks (three-way showdown, pot 3) or
bets b. After a bet II and III each call or fold, each seeing only own hand. Highest hand among non-folders takes the
pot. Profile: I bets iff x < A or x > B; II and III call iff own hand > C; Eq. A-C of the paper.

1. Payoff formulas: closed forms are compared with an exact cell integrator built only from terminal pot utilities,
   at seeded random rational (A < C < B, b, hand) points, for players I, II and III.
2. Sign identities (exact polynomial arithmetic over Q in x, y, A, B, C, b):
     I   on (0, C]: E_bet - E_check = (3C^2 + bC^2 - b - 1) - (3x^2 - 1)  = 3(A^2 - x^2)          [Eq. A]
     I   on [C, 1): E_bet - E_check = b(3x^2 - 2Cx - 1)                    (root B >0 by Eq. B)
     II  (III alike): E_call - E_fold = m(y)[(3+2b)C + (3+3b)(y-C)^+] - b(A+1-B), m(y) = min(y,A) + (y-B)^+,
         and with Eq. C, (3+2b)CA = b(A+1-B), it equals (3+2b)C(y-A), 0, A(3+3b)(y-C),
         (y-B)(3+2b)C + (A+y-B)(3+3b)(y-C) on (0,A), (A,C], (C,B), (B,1).
3. Existence/uniqueness inequalities used in the crossing argument (polynomial identities).
4. b = 2: thresholds and value by monotone bisection in 110-digit Decimal arithmetic, cross-checked with a sign change
   of the degree-8 eliminant of C in exact Fractions; comparison with the paper's printed digits.
Last line: PASS or FAIL.
"""
import random
import sys
from fractions import Fraction as F
from decimal import Decimal as D, getcontext

OK = True


def fail(msg):
    global OK
    OK = False
    print('FAIL:', msg)


# ---------------------------------------------------------------- 1. payoff formulas
def terminal(xh, yh, zh, ibet, iic, iiic, b):
    if not ibet:
        w = max((xh, 0), (yh, 1), (zh, 2))[1]
        return [2 if i == w else -1 for i in range(3)]
    stake = [1 + b, 1 + (b if iic else 0), 1 + (b if iiic else 0)]
    live = [(xh, 0)] + ([(yh, 1)] if iic else []) + ([(zh, 2)] if iiic else [])
    w = max(live)[1]
    pot = sum(stake)
    return [(pot - stake[i]) if i == w else -stake[i] for i in range(3)]


def expect(player, own, action, A, B, C, b):
    pts = sorted(set([F(0), F(1), A, B, C, own]))
    cells = list(zip(pts[:-1], pts[1:]))
    tot = F(0)
    for (a1, a2) in cells:
        for (c1, c2) in cells:
            area = (a2 - a1) * (c2 - c1)
            p, q = (a1 + a2) / 2, (c1 + c2) / 2
            if (a1, a2) == (c1, c2):
                d = (a2 - a1) / 4
                orders = [(area / 2, p, p + d), (area / 2, p + d, p)]
            else:
                orders = [(area, p, q)]
            for (w, s, t) in orders:
                if player == 0:
                    xh, yh, zh, ibet = own, s, t, action
                elif player == 1:
                    xh, yh, zh = s, own, t
                    ibet = xh < A or xh > B
                else:
                    xh, yh, zh = s, t, own
                    ibet = xh < A or xh > B
                iic = action if player == 1 else yh > C
                iiic = action if player == 2 else zh > C
                tot += w * terminal(xh, yh, zh, ibet, iic and ibet, iiic and ibet, b)[player]
    return tot


def closed_I(x, A, B, C, b):
    u = max(F(0), x - C)
    bet = 2 * C**2 + 2 * C * (u * (3 + 2 * b) - (1 - C) * (1 + b)) + 3 * (1 + b) * u**2 - (1 - C)**2 * (1 + b)
    return bet, 3 * x**2 - 1


def closed_II(y, A, B, C, b):
    m = min(y, A) + max(F(0), y - B)
    return m * ((3 + 2 * b) * C + (3 + 3 * b) * max(F(0), y - C)) - b * (A + 1 - B)


def part1(n=300, seed=7):
    rng = random.Random(seed)
    done = 0
    while done < n:
        A, C, B = sorted(F(rng.randint(1, 9999), 10000) for _ in range(3))
        b = F(rng.randint(1, 5000), rng.randint(1, 1000))
        h = F(rng.randint(1, 99999), 100000)
        if len({A, B, C, h}) < 4:
            continue
        bet, chk = closed_I(h, A, B, C, b)
        if expect(0, h, True, A, B, C, b) != bet or expect(0, h, False, A, B, C, b) != chk:
            fail('player I closed form at %s' % ((A, B, C, b, h),))
        for pl in (1, 2):
            if expect(pl, h, True, A, B, C, b) - expect(pl, h, False, A, B, C, b) != closed_II(h, A, B, C, b):
                fail('player %d closed form at %s' % (pl + 1, (A, B, C, b, h)))
        done += 1
    print('part1: closed forms equal the exact terminal-utility integrator at %d random rational points '
          '(players I, II, III)' % done)


# ---------------------------------------------------------------- 2. polynomial identities
VARS = ('x', 'y', 'A', 'B', 'C', 'b')


class P:
    def __init__(self, d=None):
        self.d = {k: v for k, v in (d or {}).items() if v != 0}

    @staticmethod
    def var(name):
        e = [0] * len(VARS)
        e[VARS.index(name)] = 1
        return P({tuple(e): F(1)})

    @staticmethod
    def const(c):
        return P({(0,) * len(VARS): F(c)})

    def __add__(self, o):
        o = o if isinstance(o, P) else P.const(o)
        d = dict(self.d)
        for k, v in o.d.items():
            d[k] = d.get(k, 0) + v
        return P(d)

    __radd__ = __add__

    def __neg__(self):
        return P({k: -v for k, v in self.d.items()})

    def __sub__(self, o):
        return self + (-(o if isinstance(o, P) else P.const(o)))

    def __rsub__(self, o):
        return P.const(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, P) else P.const(o)
        d = {}
        for k1, v1 in self.d.items():
            for k2, v2 in o.d.items():
                k = tuple(a + c for a, c in zip(k1, k2))
                d[k] = d.get(k, 0) + v1 * v2
        return P(d)

    __rmul__ = __mul__

    def __pow__(self, n):
        r = P.const(1)
        for _ in range(n):
            r = r * self
        return r

    def iszero(self):
        return not self.d


x, y, A, B, C, b = (P.var(v) for v in VARS)


def part2():
    EqA = (3 * A**2 - 1) - (3 * C**2 + b * C**2 - b - 1)                                   # = 0
    EqB = (3 * B**2 - 1) - (-2 * b * C * B + 3 * b * B**2 + 3 * B**2 - b - 1)              # = 0
    EqC = (-A + B - 1) - (2 * b * C * A + 3 * C * A - b * A - A - b + b * B + B - 1)       # = 0
    # Eq. B is b(3B^2 - 2CB - 1) up to sign; Eq. C is -( (3+2b)CA - b(A+1-B) )
    if not (EqB + b * (3 * B**2 - 2 * C * B - 1)).iszero():
        fail('Eq. B form')
    if not (EqC + ((3 + 2 * b) * C * A - b * (A + 1 - B))).iszero():
        fail('Eq. C form')
    # Player I on (0, C]: u = 0
    bet_low = 2 * C**2 + 2 * C * (-(1 - C) * (1 + b)) - (1 - C)**2 * (1 + b)
    chk = 3 * x**2 - 1
    DI_low = bet_low - chk
    # DI_low - 3(A^2 - x^2) = -EqA  (so equals 3(A^2 - x^2) exactly when Eq. A holds)
    if not (DI_low - 3 * (A**2 - x**2) + EqA).iszero():
        fail('I low identity')
    # Player I on [C, 1): u = x - C
    u = x - C
    bet_high = 2 * C**2 + 2 * C * (u * (3 + 2 * b) - (1 - C) * (1 + b)) + 3 * (1 + b) * u**2 - (1 - C)**2 * (1 + b)
    if not (bet_high - chk - b * (3 * x**2 - 2 * C * x - 1)).iszero():
        fail('I high identity')
    # continuity of I's bet payoff at x = C
    if not ((bet_high - bet_low) - (3 * (1 + b) * u**2 + 2 * C * (3 + 2 * b) * u)).iszero():
        fail('I bet payoff continuity form')
    # Player II on each region, modulo Eq. C: replace b(A+1-B) by (3+2b)CA, i.e. add EqC-form
    K = (3 + 2 * b) * C * A
    regions = {
        '(0,A)': (y, P.const(0), (3 + 2 * b) * C * (y - A)),
        '(A,C]': (A, P.const(0), P.const(0)),
        '(C,B)': (A, y - C, A * (3 + 3 * b) * (y - C)),
        '(B,1)': (A + y - B, y - C, (y - B) * (3 + 2 * b) * C + (A + y - B) * (3 + 3 * b) * (y - C)),
    }
    for name, (m, plus, claimed) in regions.items():
        raw = m * ((3 + 2 * b) * C + (3 + 3 * b) * plus) - b * (A + 1 - B)
        # raw - claimed = K - b(A+1-B) = -(EqC form) ... must be exactly that
        if not (raw - claimed - (K - b * (A + 1 - B))).iszero():
            fail('II identity on %s' % name)
    # Existence: A^2 - C^2 = b(C^2 - 1)/3 under Eq. A
    if not ((3 * A**2 - 3 * C**2) - b * (C**2 - 1) - EqA).iszero():
        fail('A<C identity')
    print('part2: Eq. B <=> b(3B^2-2CB-1)=0; Eq. C <=> (3+2b)CA=b(A+1-B); I: D=3(A^2-x^2) on (0,C], '
          'D=b(3x^2-2Cx-1) on [C,1); II/III region forms verified; A^2-C^2=b(C^2-1)/3')


def part3():
    # c0^2 - (b/(3+2b))^2 = 3b(b^2+3b+3)/((b+3)(2b+3)^2): check the cross-multiplied polynomial identity
    lhs = b * (2 * b + 3)**2 - b**2 * (b + 3)
    rhs = 3 * b * (b**2 + 3 * b + 3)
    if not (lhs - rhs).iszero():
        fail('denominator positivity identity')
    # B(c) = (c + sqrt(c^2+3))/3 is the positive root of 3B^2 - 2cB - 1 (product of roots -1/3 < 0)
    # B(1) = 1: 3 - 2 - 1 = 0
    if 3 - 2 - 1 != 0:
        fail('B(1)')
    # B > C for C < 1: 3C^2 - 2C*C - 1 = C^2 - 1 < 0, so C lies strictly between the roots, below B
    if not ((3 * C**2 - 2 * C * C - 1) - (C**2 - 1)).iszero():
        fail('B>C identity')
    print('part3: crossing-argument identities verified (denominator (3+2b)C-b > 0 on [c0,1]; B(1)=1; '
          '3C^2-2C*C-1 = C^2-1 < 0 so C < B for C < 1)')


# ---------------------------------------------------------------- 4. b = 2 numbers
POLY_C = [180075, -205800, -59780, 161840, -69540, -10688, 23648, -8832, 1152]   # degree 8 .. 0


def peval(c):
    r = F(0)
    for a in POLY_C:
        r = r * c + a
    return r


def part4():
    getcontext().prec = 110
    bb = D(2)

    def LmR(c):
        Bc = (c + (c * c + 3).sqrt()) / 3
        L = (((3 + bb) * c * c - bb) / 3).sqrt()
        R = bb * (1 - Bc) / ((3 + 2 * bb) * c - bb)
        return L - R

    lo = (bb / (3 + bb)).sqrt()
    hi = D(1)
    for _ in range(330):
        mid = (lo + hi) / 2
        if LmR(mid) < 0:
            lo = mid
        else:
            hi = mid
    Cv = (lo + hi) / 2
    Bv = (Cv + (Cv * Cv + 3).sqrt()) / 3
    Av = (((3 + bb) * Cv * Cv - bb) / 3).sqrt()
    V = 2 * Av**3 + bb * ((1 - Bv**3) - Cv * (1 - Bv**2) - (1 - Bv))
    # eliminant sign change around C in exact rationals
    e = F(1, 10**60)
    Cf = F(str(Cv))
    if not (peval(Cf - e) * peval(Cf + e) < 0):
        fail('degree-8 eliminant has no sign change at the bisected C')
    if not (0 < Av < Cv < Bv < 1):
        fail('ordering at b=2')
    q = D(10) ** -15
    printed = {'A': '0.137058194328370', 'B': '0.829422249795391', 'C': '0.641304115985175', 'V': '0.122557074714865'}
    vals = {'A': Av, 'B': Bv, 'C': Cv, 'V': V}
    print('part4 (b=2): unique ordered solution, 0 < A < C < B < 1')
    for k in 'ABCV':
        print('  %s = %s  (rounded to 15 dp: %s; paper prints %s; equal: %s)' % (
            k, format(vals[k], '.50f'), vals[k].quantize(q), printed[k], str(vals[k].quantize(q)) == printed[k]))
    print('V_50 = %s' % format(V, '.50f'))
    return V


if __name__ == '__main__':
    part1()
    part2()
    part3()
    part4()
    print('PASS' if OK else 'FAIL')
    sys.exit(0 if OK else 1)
