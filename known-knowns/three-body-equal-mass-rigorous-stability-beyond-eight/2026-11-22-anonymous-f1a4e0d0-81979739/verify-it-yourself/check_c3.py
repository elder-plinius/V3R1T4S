"""Standalone check, written from the definitions, of the stability half of the claim from the saved enclosure
object/A_row2_r55.json of A = D phi_t(x0) (t = half period) over the certified box.
Definitions: state (q1,q2,q3,v1,v2,v3) in R^12, unit masses (canonical, J = [[0,I],[-I,0]]); reversor
S(q1,q2,q3,v1,v2,v3) = (-q3,-q2,-q1,v3,v2,v1); monodromy M = S A^-1 S A with A^-1 = -J A^T J.
Checks (outward-rounded ball arithmetic, python-flint):
 1. A^T J A - J contains 0 entrywise (A is consistent with symplecticity).
 2. p(l) = det(l I - M); Taylor coefficients c_0..c_7 of p at l = 1 contain 0 (8 trivial multipliers, which theory
    forces: see how-we-built-it/PROOF.md step 5), q(l) = p(l)/(l-1)^8 from c_8..c_12 (exact algebra).
 3. q palindromic quartic l^4 + a l^3 + b l^2 + a' l + 1: for a = a3 and a = a1, s^2 + a s + (b - 2) has a certified
    positive discriminant and both roots strictly inside (-2, 2)  =>  four distinct multipliers on the unit circle.
 4. omega = arccos(s/2)/(2 pi) encloses the source's 40-digit frequencies (object/res_eig_angles_row2.txt).
Prints PASS or FAIL as the last line."""
import json, sys, os
from math import comb
from flint import arb, arb_mat, ctx
ctx.prec = 384
here = os.path.dirname(os.path.abspath(__file__))
import hashlib, csv
row = list(csv.DictReader(open(os.path.join(here, '..', 'INDEX.csv'))))[0]
h = hashlib.sha256(open(os.path.join(here, '..', row['file']), 'rb').read()).hexdigest()
if h != row['sha256']:
    print('0. object sha256 mismatch with INDEX.csv:', h)
    print('FAIL'); sys.exit(1)
print('0. object sha256 matches INDEX.csv')
def parse(s):
    s = s.strip()
    if s.startswith('['):
        body = s[1:-1]
        if '+/-' in body:
            m, r = body.split('+/-')
            m = m.strip() or '0'
            return arb(m) + arb(0, arb(r.strip()))
        return arb(body)
    return arb(s)
A = arb_mat([[parse(x) for x in row] for row in json.load(open(os.path.join(here, '..', 'object', 'A_row2_r55.json')))['A']])
n = 12
J = arb_mat([[1 if j == i + 6 else (-1 if i == j + 6 else 0) for j in range(n)] for i in range(n)])
ok = True
D = A.transpose() * J * A - J
c1 = all(D[i, j].contains(0) for i in range(n) for j in range(n))
print('1. A^T J A - J contains 0:', c1); ok &= c1
perm = [4, 5, 2, 3, 0, 1, 10, 11, 8, 9, 6, 7]
S = arb_mat([[(-1 if i < 6 else 1) if j == perm[i] else 0 for j in range(n)] for i in range(n)])
M = S * (-(J * A.transpose() * J)) * S * A
p = M.charpoly()
pc = [p[k] for k in range(13)]
c = [sum((pc[k] * comb(k, j) for k in range(j, 13)), arb(0)) for j in range(13)]
c2 = all(c[j].contains(0) for j in range(8))
print('2. c_0..c_7 contain 0:', c2); ok &= c2
q = [arb(0)] * 5
for i in range(5):
    for k in range(i + 1):
        q[k] += c[8 + i] * comb(i, k) * (-1) ** (i - k)
print('   q coefficients l^0..l^4:', [x.str(10, radius=True) for x in q])
src = sorted(arb(x) for x in open(os.path.join(here, '..', 'object', 'res_eig_angles_row2.txt')).read().split('stability angles:')[1].split()[:2])
for name, a in (('a3', q[3]), ('a1', q[1])):
    disc = a * a - 4 * (q[2] - 2)
    good = bool(disc > 0)
    if good:
        s1, s2 = (-a - disc.sqrt()) / 2, (-a + disc.sqrt()) / 2
        good = bool(s1 > -2) and bool(s2 < 2)
        om = sorted([(s / 2).acos() / (2 * arb.pi()) for s in (s1, s2)], key=lambda z: float(z.mid()))
        cons = all(o.overlaps(t) for o, t in zip(om, src))
        print('3. via %s: disc %s, s %s %s, in (-2,2): %s; omega %s; encloses source: %s' % (name, disc.str(8, radius=True),
              s1.str(15, radius=True), s2.str(15, radius=True), good, [o.str(18, radius=True) for o in om], cons))
        ok &= good and cons
    else:
        print('3. via %s: discriminant not certified positive' % name); ok = False
print('PASS' if ok else 'FAIL')
sys.exit(0 if ok else 1)
