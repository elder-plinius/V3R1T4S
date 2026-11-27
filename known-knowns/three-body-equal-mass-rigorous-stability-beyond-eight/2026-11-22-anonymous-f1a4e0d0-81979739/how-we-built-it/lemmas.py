"""Symbolic checks (sympy) of the algebraic lemmas behind the certificate.
L1  S is a reversor: f(S x) = -S f(x) for the equal-mass planar 3-body vector field.
L2  x0(vx, vy) lies in Fix(S); P = 0, COM = 0, L = 0 exactly at x0.
L3  On {x2 = y2 = 0, P = 0, COM = 0, L = 0, (v1 - v3).q1 = 0, q1 != 0} the state is in Fix(S).
L4  Exact equivariances used for the trivial block: f commutes with translations (e), Galilei boosts (b), rotations (R);
    omega(f, u) = dH(u), omega(Rx, u) = dL(u); dH(e)=dH(b)=dH(Rx)=0, dL(e)=dL(b)=0 at x0 (P = 0, COM = 0).
L5  A^{-1} = -J A^T J for symplectic A; M = S A^{-1} S A follows from phi_t(Sy) = S phi_{-t}(y).
"""
import sympy as sp, functools
print = functools.partial(print, flush=True)
q = sp.symbols('x1 y1 x2 y2 x3 y3', real=True)
v = sp.symbols('u1 w1 u2 w2 u3 w3', real=True)
X = sp.Matrix(list(q) + list(v))
def f(X):
    Q = [sp.Matrix([X[2*i], X[2*i+1]]) for i in range(3)]
    acc = []
    for i in range(3):
        a = sp.zeros(2, 1)
        for j in range(3):
            if j != i:
                d = Q[j] - Q[i]
                a += d / (d.dot(d))**sp.Rational(3, 2)
        acc += [a[0], a[1]]
    return sp.Matrix(list(X[6:12]) + acc)
perm = {0: 4, 1: 5, 2: 2, 3: 3, 4: 0, 5: 1, 6: 10, 7: 11, 8: 8, 9: 9, 10: 6, 11: 7}
S = sp.zeros(12, 12)
for i in range(12):
    S[i, perm[i]] = -1 if i < 6 else 1
fx = f(X)
def canon(e):
    # expand the base of every power so equal distances become identical expressions
    e = e.replace(lambda u: u.is_Pow and not u.exp.is_Integer, lambda u: sp.Pow(sp.expand(u.base), u.exp))
    return sp.expand(e)
L1 = (f(S * X) + S * fx).applyfunc(canon)
print('L1 reversor f(Sx) + S f(x) == 0:', L1 == sp.zeros(12, 1))
print('S^2 == I:', S * S == sp.eye(12))
vx, vy = sp.symbols('vx vy', real=True)
x0 = sp.Matrix([-1, 0, 0, 0, 1, 0, vx, vy, -2*vx, -2*vy, vx, vy])
print('L2 S x0 == x0:', sp.simplify(S * x0 - x0) == sp.zeros(12, 1))
P = [sum(X[6+2*i] for i in range(3)), sum(X[7+2*i] for i in range(3))]
COM = [sum(X[2*i] for i in range(3)), sum(X[2*i+1] for i in range(3))]
L = sum(X[2*i]*X[7+2*i] - X[2*i+1]*X[6+2*i] for i in range(3))
sub0 = dict(zip(X, x0))
print('L2 P, COM, L at x0:', [sp.simplify(e.subs(sub0)) for e in P + COM + [L]])
# L3: parametrise x2=y2=0, x3=-x1, y3=-y1 (COM), v2 = -(v1+v3) (P); then L = q1 x (v1 - v3)
a, b, p1, p2, r1, r2 = sp.symbols('a b p1 p2 r1 r2', real=True)
Xs = sp.Matrix([a, b, 0, 0, -a, -b, p1, p2, -(p1+r1), -(p2+r2), r1, r2])
Ls = sp.expand(L.subs(dict(zip(X, Xs))))
print('L3 L on {q2=0,COM=0,P=0} =', sp.factor(Ls), ' ; (v1-v3).q1 =', sp.expand((p1-r1)*a + (p2-r2)*b))
# L=0 and dot=0 with (a,b)!=0 => v1-v3 is orthogonal to both q1 and J q1 => v1=v3:
M2 = sp.Matrix([[a, b], [-b, a]])
print('L3 det[[a,b],[-b,a]] =', sp.factor(M2.det()), '(non-zero iff q1 != 0)')
SXs = S * Xs
print('L3 state with v1=v3 is S-fixed:', sp.simplify((S*Xs - Xs).subs({r1: p1, r2: p2})) == sp.zeros(12, 1))
# L4
H = sum((X[6+k]**2) for k in range(6))/2 - sum(1/sp.sqrt((X[2*j]-X[2*i])**2 + (X[2*j+1]-X[2*i+1])**2) for i in range(3) for j in range(i+1, 3))
J = sp.zeros(12, 12)
for i in range(6):
    J[i, i+6] = 1; J[i+6, i] = -1
gradH = sp.Matrix([sp.diff(H, x) for x in X]); gradL = sp.Matrix([sp.diff(L, x) for x in X])
print('L4 f == J gradH:', (fx - J * gradH).applyfunc(canon) == sp.zeros(12, 1))
Rx = sp.Matrix(sum(([-X[c+1], X[c]] for c in range(0, 12, 2)), []))
print('L4 Rx == J gradL:', sp.simplify(Rx - J * gradL) == sp.zeros(12, 1))
ex = sp.Matrix([1, 0, 1, 0, 1, 0] + [0]*6); ey = sp.Matrix([0, 1, 0, 1, 0, 1] + [0]*6)
bx = sp.Matrix([0]*6 + [1, 0, 1, 0, 1, 0]); by = sp.Matrix([0]*6 + [0, 1, 0, 1, 0, 1])
om = lambda u, w: (u.T * J * w)[0]
for nm, u in (('ex', ex), ('ey', ey), ('bx', bx), ('by', by), ('Rx', Rx)):
    print('L4 dH(%s) at x0 =' % nm, sp.simplify((gradH.T * u)[0].subs(sub0)), '; dL(%s) at x0 =' % nm, sp.simplify((gradL.T * u)[0].subs(sub0)))
print('L4 omega(ex,bx), omega(ey,by), omega(ex,by), omega(ex,ey), omega(bx,by) =', om(ex, bx), om(ey, by), om(ex, by), om(ex, ey), om(bx, by))
# Jacobian equivariances: Df(x) e = 0 (translation), Df(x) b = e, Df R x = R f  (linearised group actions)
Df = fx.jacobian(X)
print('L4 Df e_x == 0:', (Df * ex).applyfunc(canon) == sp.zeros(12, 1), '; Df b_x == e_x:', (Df * bx - ex).applyfunc(canon) == sp.zeros(12, 1))
Rm = sp.zeros(12, 12)
for c in range(0, 12, 2):
    Rm[c, c+1] = -1; Rm[c+1, c] = 1
print('L4 Df R x == R f (rotation equivariance):', (Df * (Rm * X) - Rm * fx).applyfunc(canon) == sp.zeros(12, 1))
print('L4 R symplectic-commuting (R^T J R == J):', sp.simplify(Rm.T * J * Rm - J) == sp.zeros(12, 12))
print('L5 S^T J S == -J (S anti-symplectic):', sp.simplify(S.T * J * S + J) == sp.zeros(12, 12))
