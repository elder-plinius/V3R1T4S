#!/usr/bin/env python3
"""Checker for C1, written from the source's definitions (White 2011, NTRS 20110015936).

f(r) = [tanh(s(r+R)) - tanh(s(r-R))] / (2 tanh(sR));  T00 = -(1/8pi) v^2 rho^2/(4 r^2) f'(r)^2  (G=c=1)
gamma(u) = cosh(0.5 ln|1-u^2|);  E = int T00 dV  ->  E = -(c^4/(12G)) beta^2 I,  I = int_0^inf f'^2 r^2 dr
Closed-form bound: I >= R f(R)^2 >= R/4  ->  E <= -(c^4/(48 G)) beta^2 R.
"""
import mpmath as mp

mp.mp.dps = 30
c = mp.mpf(299792458)
G = mp.mpf('6.67430e-11')
R = mp.mpf('5e-3')
gt = 1 + mp.mpf('1e-7')


def gamma(u):
    return mp.cosh(mp.log(abs(1 - u * u)) / 2)


def fp(r, s, R=R):
    return s * (mp.sech(s * (r + R)) ** 2 - mp.sech(s * (r - R)) ** 2) / (2 * mp.tanh(s * R))


def f(r, s, R=R):
    return (mp.tanh(s * (r + R)) - mp.tanh(s * (r - R))) / (2 * mp.tanh(s * R))


def I(s, R=R):
    w = 1 / s
    pts = [0, max(R - 40 * w, 0), R, R + 40 * w, mp.inf]
    pts = sorted(set(pts))
    return mp.quad(lambda r: fp(r, s, R) ** 2 * r * r, pts)


def E(s, beta, R=R):
    return -(c ** 4 / (12 * G)) * beta ** 2 * I(s, R)


# u*: gamma(u) = gt on u<1; closed form gamma = (2-u^2)/(2 sqrt(1-u^2))
ustar = mp.findroot(lambda u: (2 - u * u) / (2 * mp.sqrt(1 - u * u)) - gt, mp.mpf('0.03'))
print('u* =', mp.nstr(ustar, 15), ' gamma(u*)-1 =', mp.nstr(gamma(ustar) - 1, 10))
print('check gamma formula equals closed form at u=0.5:', mp.nstr(gamma(mp.mpf('0.5')) - (2 - 0.25) / (2 * mp.sqrt(0.75)), 5))
# iff part: gamma increasing on [0,1)
us = [mp.mpf(k) / 1000 for k in range(0, 1000)]
print('gamma monotone increasing on [0,0.999]:', all(gamma(us[i + 1]) > gamma(us[i]) for i in range(len(us) - 1)))
# u>1 branch: gamma >= 1 always (AM-GM), so any v_s > 1 already exceeds u*
print('f(R) identity 1/(1+tanh^2 sR) at sR=0.7:', mp.nstr(f(R, 0.7 / R) - 1 / (1 + mp.tanh(0.7) ** 2), 5))
print('f(0) = 1 at sR=0.3:', mp.nstr(f(0, 0.3 / R), 20))

# known negative: beta = 0
print('known negative: E(beta=0) =', E(1 / R, 0))
# known positive: thin-wall asymptote at sR = 50
s = 50 / R
thin = -(c ** 4 / G) * ustar ** 2 * R ** 2 * s / 36
print('thin-wall test sR=50: E/asymptote =', mp.nstr(E(s, ustar) / thin, 10))

for name, beta in [('u* (source gamma formula)', ustar), ('0.0004c (slide SR reading)', mp.mpf('4e-4'))]:
    bound = -(c ** 4 / (48 * G)) * beta ** 2 * R
    print('\n' + name, ' beta =', mp.nstr(beta, 10))
    print('  closed-form bound E <=', mp.nstr(bound, 10), 'J  =', mp.nstr(bound / c ** 2, 6), 'kg')
    for sR in ['0.01', '0.1', '0.5', '1', '2', '5', '20', '100']:
        e = E(mp.mpf(sR) / R, beta)
        print('  sR=%-5s E = %s J  E/bound = %s' % (sR, mp.nstr(e, 10), mp.nstr(e / bound, 8)))
