# Zeng far-field constants with EXACT vertex radii (mp.iv, 200 bits) + symbolic checks of d_k, G, shoelace identity.
from mpmath import iv
import sympy as sp
iv.prec = 200
def G(rho):  # pi/4 + (1/2) sqrt(rho^2-1/4) - (1/4) arccos(1/(2 rho)),  arccos x = atan2(sqrt(1-x^2), x)
    x = 1/(2*rho); return iv.pi/4 + iv.sqrt(rho*rho - iv.mpf(1)/4)/2 - iv.atan2(iv.sqrt(1-x*x), x)/4
R3 = 1/iv.sqrt(3); R5 = 1/(2*iv.cos(iv.pi/10))
b3 = iv.mpf('0.190700'); b5 = iv.mpf('0.194601')
d3 = iv.sqrt(b3*b3 + R3*R3 + 2*b3*R3*iv.cos(iv.pi/3))
d5 = iv.sqrt(b5*b5 + R5*R5 + 2*b5*R5*iv.cos(iv.pi/5))
print("d3(b3) =", d3); print("d5(b5) =", d5)
print("d3(b3), d5(b5) > 1/2 :", d3.a > iv.mpf(1)/2, d5.a > iv.mpf(1)/2)
g3 = G(d3) - iv.mpf('0.834'); g5 = G(d5) - iv.mpf('0.834')
print("G(d3(b3)) - 0.834 in", g3); print("G(d5(b5)) - 0.834 in", g5)
assert g3.a > 0 and g5.a > 0
print("paper prints 2.13944145452936e-7 (non-enclosing radii) ; enclosure above gives 2.139441454410e-7 at 12 digits")
# monotonicity: d'(r) = (r + R cos delta)/d(r) > 0 for r>=0 ; G'(rho) = sqrt(4 rho^2-1)/(4 rho)
r, R, dl = sp.symbols('r R delta', positive=True)
d = sp.sqrt(r**2 + R**2 + 2*r*R*sp.cos(dl))
print("d' - (r+R cos delta)/d =", sp.simplify(sp.diff(d, r) - (r + R*sp.cos(dl))/d))
rho = sp.symbols('rho', positive=True)
Gs = sp.pi/4 + sp.sqrt(rho**2 - sp.Rational(1, 4))/2 - sp.acos(1/(2*rho))/4
print("G' - sqrt(4rho^2-1)/(4rho) =", sp.simplify(sp.diff(Gs, rho) - sp.sqrt(4*rho**2-1)/(4*rho)))
print("G(1/2) =", sp.simplify(Gs.subs(rho, sp.Rational(1, 2))))
# cos(pi/5) exact = (1+sqrt5)/4
print("cos(pi/5) - (1+sqrt5)/4 =", sp.simplify(sp.cos(sp.pi/5) - (1+sp.sqrt(5))/4))
# shoelace expansion identity (symbolic, m=5 generic polygon)
m = 5
cx = sp.symbols('cx0:%d' % m); cy = sp.symbols('cy0:%d' % m); dx = sp.symbols('dx0:%d' % m); dy = sp.symbols('dy0:%d' % m)
def S(X, Y): return sp.Rational(1, 2)*sum(X[i]*Y[(i+1) % m] - Y[i]*X[(i+1) % m] for i in range(m))
lhs = S([cx[i]+dx[i] for i in range(m)], [cy[i]+dy[i] for i in range(m)]) - S(cx, cy)
det = lambda ax, ay, bx, by: ax*by - ay*bx
rhs = sp.Rational(1, 2)*sum(det(dx[i], dy[i], cx[(i+1) % m]-cx[(i-1) % m], cy[(i+1) % m]-cy[(i-1) % m]) for i in range(m)) + sp.Rational(1, 2)*sum(det(dx[i], dy[i], dx[(i+1) % m], dy[(i+1) % m]) for i in range(m))
print("S(c+d) - S(c) - [1/2 sum det(d_i, c_{i+1}-c_{i-1}) + 1/2 sum det(d_i,d_{i+1})] =", sp.expand(lhs - rhs))
# gradient of S wrt vertex i
print("dS/dx_i - (y_{i+1}-y_{i-1})/2 =", sp.simplify(sp.diff(S(cx, cy), cx[2]) - (cy[3]-cy[1])/2), "; dS/dy_i + (x_{i+1}-x_{i-1})/2 =", sp.simplify(sp.diff(S(cx, cy), cy[2]) + (cx[3]-cx[1])/2))
# rotation derivative: d/dpsi Q_psi q = Q_psi J q ; chord |Q_a q - Q_b q| = 2|q||sin((a-b)/2)| <= |q||a-b|
a, b, qx, qy = sp.symbols('a b q_x q_y', real=True)
Qa = sp.Matrix([[sp.cos(a), -sp.sin(a)], [sp.sin(a), sp.cos(a)]]); J = sp.Matrix([[0, -1], [1, 0]]); q = sp.Matrix([qx, qy])
print("d/dpsi(Q q) - Q J q =", sp.simplify(sp.diff(Qa*q, a) - Qa*J*q).T)
Qb = Qa.subs(a, b); diff = (Qa-Qb)*q
print("|Qa q - Qb q|^2 - 4 |q|^2 sin^2((a-b)/2) =", sp.simplify(sp.expand_trig((diff.T*diff)[0] - 4*(qx**2+qy**2)*sp.sin((a-b)/2)**2).rewrite(sp.cos)))
