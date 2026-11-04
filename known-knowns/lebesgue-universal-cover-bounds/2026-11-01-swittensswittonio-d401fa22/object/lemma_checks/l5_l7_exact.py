# L5/L7/L4 constants and identities: sympy exact + mp.iv enclosures.
import sympy as sp
from mpmath import iv
iv.dps = 60
print("=== R_n, thresholds (mp.iv, 60 digits) ===")
def Rn_iv(n): return 1/(2*iv.cos(iv.pi/(2*n)))
R3, R5 = Rn_iv(3), Rn_iv(5)
print("R3 =", R3); print("R5 =", R5)
print("delta3_thr = 1-R3 =", 1-R3); print("delta5_thr = 1-R5 =", 1-R5)
# paper's printed values (Def 2.6, Rem 4.10): must lie within 5e-13 of the enclosures
for name, val, pr in (("R3", R3, "0.577350269190"), ("R5", R5, "0.525731112119"), ("1-R3", 1-R3, "0.422649730810"), ("1-R5", 1-R5, "0.474268887881")):
    diff = abs(val - iv.mpf(pr)); assert diff.b < iv.mpf('5e-13'), name
    print(f"  paper's printed {name}={pr}: |enclosure - printed| <= {diff.b}  (< 5e-13 OK)")
print("=== exact (sympy): R3^2 = 1/3, R5^2 = (5-sqrt5)/10, chord_m = 1 ===")
x = sp.symbols('x')
R5s = 1/(2*sp.cos(sp.pi/10)); R3s = 1/(2*sp.cos(sp.pi/6))
print("R3 simplifies to", sp.simplify(R3s), "; R3^2 =", sp.simplify(R3s**2))
print("R5^2 - (5-sqrt5)/10 =", sp.simplify(sp.nsimplify(sp.N(R5s**2-(5-sp.sqrt(5))/10, 60), rational=False)), "(numeric residual at 60 digits:", sp.N(R5s**2-(5-sp.sqrt(5))/10, 60), ")")
assert sp.simplify(sp.cos(sp.pi/10)**2 - (5+sp.sqrt(5))/8) == 0
print("cos(pi/10)^2 = (5+sqrt5)/8 -> R5^2 = 1/(4cos^2) = 2/(5+sqrt5) = (5-sqrt5)/10 : exact")
# R_n via diameter: 2 R sin(pi m / n) = 1, m=(n-1)/2, equals 2 R cos(pi/(2n))
for n in (3, 5, 7, 9):
    m = (n-1)//2
    assert sp.simplify(sp.sin(sp.pi*m/n) - sp.cos(sp.pi/(2*n))) == 0
print("sin(pi m/n) = cos(pi/(2n)) for n=2m+1 (n=3,5,7,9 checked exactly)")
print("=== L7 identities used in the arc/vertex support-function proof (sympy, exact) ===")
a, de = sp.symbols('a delta', real=True)
e1 = sp.simplify(sp.expand_trig(2*sp.sin(a-de)*sp.cos(de) - sp.sin(a) - sp.sin(a-2*de)))
e2 = sp.simplify(sp.expand_trig(2*sp.sin(a+de)*sp.cos(de) - sp.sin(a) - sp.sin(a+2*de)))
print("2 sin(a-delta) cos(delta) - sin a - sin(a-2 delta) =", e1); print("2 sin(a+delta) cos(delta) - sin a - sin(a+2 delta) =", e2)
assert e1 == 0 and e2 == 0
print("=== L4: sum_j |p-V_j|^2 = n|p|^2 + n R^2 for regular n-gon (n=3,5) ===")
px, py, R = sp.symbols('p_x p_y R', real=True)
for n in (3, 5):
    V = [(R*sp.cos(2*sp.pi*k/n), R*sp.sin(2*sp.pi*k/n)) for k in range(n)]
    S = sum((px-v[0])**2+(py-v[1])**2 for v in V)
    print(f"n={n}: sum - (n|p|^2+nR^2) =", sp.simplify(sp.expand(S) - n*(px**2+py**2) - n*R**2))
print("=== L5: |R_rho V - R_rho' V| = 2R |sin((rho-rho')/2)| ===")
r1, r2 = sp.symbols('rho1 rho2', real=True)
chord2 = (R*sp.cos(r1)-R*sp.cos(r2))**2 + (R*sp.sin(r1)-R*sp.sin(r2))**2   # V at angle 0 rotated is R(cos rho, sin rho); general V adds a common angle
print("chord^2 - 4R^2 sin^2((rho1-rho2)/2) =", sp.simplify(sp.expand_trig(chord2 - 4*R**2*sp.sin((r1-r2)/2)**2).rewrite(sp.cos)))
