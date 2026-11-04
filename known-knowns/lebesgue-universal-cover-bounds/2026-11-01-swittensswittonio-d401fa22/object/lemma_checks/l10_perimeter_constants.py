# Constants for L11/L12: hull radius, perimeter bound, Steiner excess for eps-inflated membership; B_n inside D(0,R_n).
from mpmath import iv
iv.dps = 50
R3 = 1/(2*iv.cos(iv.pi/6)); R5 = 1/(2*iv.cos(iv.pi/10))
rout = iv.mpf('0.7') + R3                       # every point of every placed body with |t|<=0.7 is within 0.7+R3 of the origin
P = 2*iv.pi*rout                                 # perimeter of a convex set inside a disc of radius rout is <= 2 pi rout
print("r_out = 0.7+R3 =", rout); print("perimeter bound 2*pi*r_out =", P, "(paper: 8.026)")
assert P.b < iv.mpf('8.0259') and P.a > iv.mpf('8.0258')
# B_n subset D(0,R_n): arc intervals h = 1 - R cos(psi) <= 1 - R cos(pi/(2n)) = 1/2 <= R ; vertex intervals h <= R.
for n, R in ((3, R3), (5, R5)):
    print(f"n={n}: R cos(pi/(2n)) =", R*iv.cos(iv.pi/(2*n)), "(must contain 1/2);  1/2 <= R_n:", iv.mpf('0.5') < R)
# Steiner excess for inflation eps: eps*P + pi*eps^2
for eps in ('1e-12', '2e-12', '1e-9'):
    e = iv.mpf(eps); print(f"eps={eps}: eps*P+pi*eps^2 <=", (e*P + iv.pi*e*e).b)
