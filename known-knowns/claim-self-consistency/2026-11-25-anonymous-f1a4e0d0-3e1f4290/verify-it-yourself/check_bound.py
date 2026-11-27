#!/usr/bin/env python3
"""Standalone checker (Python standard library only), written from the source's definitions:
f(r) = [tanh(s(r+R)) - tanh(s(r-R))]/(2 tanh(sR)); Eq. (3) T00 = -(1/8pi) v^2 rho^2/(4 r^2) f'(r)^2 (G=c=1);
gamma = cosh(0.5 ln|1 - v^2 f^2|).  Total energy E = -(c^4/(12 G)) beta^2 I, I = int_0^inf f'^2 r^2 dr.
Checks: u*, the closed-form bound, the numbers in object/bound.json, the identity f(R) = 1/(1+tanh^2 sR) and the
inequality I/R >= 1/4 by Simpson quadrature over sigma R in [1e-3, 1e3]; prints PASS or FAIL last."""
import hashlib, json, math, os, sys

obj = json.load(open(sys.argv[1]))
c = 299792458.0; G = 6.6743e-11
R = obj['operating_point']['R_m']; gm1 = obj['operating_point']['gamma_minus_1']
ok = True

def chk(name, cond):
    global ok
    print(('ok   ' if cond else 'FAIL ') + name)
    ok = ok and cond

def gam(u):
    return math.cosh(0.5 * math.log(abs(1 - u * u)))

# u*: gamma(u) = 1 + gm1 on [0, 1); use closed form (2-u^2)/(2 sqrt(1-u^2)) - 1 = (1 - sqrt(1-u^2))^2/(2 sqrt(1-u^2))
# to avoid cancellation; bisection.
def gm1_of(u):
    w = math.sqrt(1 - u * u)
    return (1 - w) ** 2 / (2 * w)
lo, hi = 0.0, 0.5
for _ in range(200):
    m = 0.5 * (lo + hi)
    if gm1_of(m) < gm1: lo = m
    else: hi = m
us = 0.5 * (lo + hi)
print('u* = %.15f' % us)
chk('u* matches object (rel 1e-13)', abs(us - obj['u_star']) <= 1e-13 * us)
chk('closed form equals cosh formula at u=0.3', abs(gam(0.3) - 1 - gm1_of(0.3)) < 1e-14)
bound = -(c ** 4 / (48 * G)) * us ** 2 * R
print('bound = %.10e J  (%.6e kg)' % (bound, bound / c ** 2))
chk('bound_J matches object (rel 1e-9)', abs(bound - obj['bound_J']) <= 1e-9 * abs(bound))
chk('bound_kg matches object (rel 1e-6)', abs(bound / c ** 2 - obj['bound_kg_equivalent']) <= 1e-6 * abs(bound / c ** 2))

def fp(r, s):
    a = s * (r + R); b = s * (r - R)
    sech2 = lambda x: 0.0 if abs(x) > 350 else 1.0 / math.cosh(x) ** 2
    return s * (sech2(a) - sech2(b)) / (2 * math.tanh(s * R))

def f(r, s):
    return (math.tanh(s * (r + R)) - math.tanh(s * (r - R))) / (2 * math.tanh(s * R))

def simpson(g, a, b, n):
    h = (b - a) / n
    t = g(a) + g(b)
    for k in range(1, n):
        t += (4 if k % 2 else 2) * g(a + k * h)
    return t * h / 3

def I(s):
    w = 1.0 / s
    pts = sorted(set([0.0, max(R - 40 * w, 0.0), R, R + 40 * w, R + 80 * w + 40 * R]))
    g = lambda r: fp(r, s) ** 2 * r * r
    return sum(simpson(g, a, b, 4000) for a, b in zip(pts[:-1], pts[1:]))

for sR in (0.1, 0.7, 3.0):
    s = sR / R
    chk('f(R) = 1/(1+tanh^2 sR) at sR=%g' % sR, abs(f(R, s) - 1 / (1 + math.tanh(sR) ** 2)) < 1e-12)
mins = []
for k in range(0, 121):
    sR = 10 ** (-3 + 6 * k / 120)
    mins.append((I(sR / R) / R, sR))
m, sRm = min(mins)
print('min over 121-point grid of I/R = %.6f at sR = %.4f (proof needs >= 0.25)' % (m, sRm))
chk('I/R >= 1/4 on the grid', m >= 0.25)
# golden-section refinement in log(sigma R) around the grid minimum
a, b = math.log10(sRm) - 0.1, math.log10(sRm) + 0.1
gr = (math.sqrt(5) - 1) / 2
F = lambda k: I(10 ** k / R) / R
x1, x2 = b - gr * (b - a), a + gr * (b - a); f1, f2 = F(x1), F(x2)
for _ in range(60):
    if f1 < f2: b, x2, f2 = x2, x1, f1; x1 = b - gr * (b - a); f1 = F(x1)
    else: a, x1, f1 = x1, x2, f2; x2 = a + gr * (b - a); f2 = F(x2)
m = min(f1, f2); sRm = 10 ** (0.5 * (a + b))
print('refined min I/R = %.7f at sR = %.5f' % (m, sRm))
chk('I/R minimum matches object (rel 1e-5)', abs(m - obj['I_over_R_minimum']) <= 1e-5 * m)
chk('sigma R at minimum matches object (rel 2e-5)', abs(sRm - obj['sigma_R_at_least_abs_E']) <= 2e-5 * sRm)
Eleast = -(c ** 4 / (12 * G)) * us ** 2 * m * R
print('least |E| = %.8e J' % Eleast)
chk('least |E| matches object (rel 1e-5)', abs(Eleast - obj['least_abs_E_over_sigma_J']) <= 1e-5 * abs(Eleast))
chk('least |E| <= bound', Eleast <= bound)
exp = {'source_sha256': 'dd152cede691d4357e8f12acce620763855e57a7beabda182151349262d34a4d',
       'source_url': 'https://ntrs.nasa.gov/api/citations/20110015936/downloads/20110015936.pdf',
       'bound_formula': 'E <= -(c^4/(48 G)) u_star^2 R, for every sigma > 0', 'proof': 'object/PROOF.md',
       'source': 'H. White, Warp Field Mechanics 101, NASA NTRS 20110015936 (2011)'}
chk('text fields exact', all(obj.get(k) == v for k, v in exp.items()))
chk('operating point exact', obj['operating_point'] == {'R_m': 0.005, 'gamma_minus_1': 1e-7})
chk('constants exact', obj['constants'] == {'c_m_per_s': 299792458, 'G_SI': 6.6743e-11})
pp = os.path.join(os.path.dirname(os.path.abspath(sys.argv[1])), 'PROOF.md')
chk('object/PROOF.md sha256 matches object', os.path.isfile(pp) and hashlib.sha256(open(pp, 'rb').read()).hexdigest() == obj.get('proof_sha256'))
chk('no extra fields', set(obj) == set(exp) | {'proof_sha256', 'operating_point', 'constants', 'u_star', 'bound_J', 'bound_kg_equivalent',
    'least_abs_E_over_sigma_J', 'sigma_R_at_least_abs_E', 'I_over_R_minimum'})
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
