#!/usr/bin/env python3
"""Exact algebraic probe on de Grey-Gibbs-Helm (arXiv:2401.06784, Sec. 7.4 & 10.2)
open internal-ratio edge-cuboid families II and III."""
import math
import sympy as sp

p, q, u, t, X = sp.symbols("p q u t X")

# Family II from DGH Sec 7.4:
E2 = -4 * p**2 * q**2 * (p**4 - 4*p**2*q**2 - q**4) * (p**4 + 4*p**2*q**2 - q**4) * (3*p**4 + q**4) * (p**4 + 3*q**4)
t_expr = (p**4 - q**4) / (4 * p**2 * q**2)
E2_check = sp.simplify(E2 - (32 * p**5 * q**5)**2 * (1 - t_expr**2) * (1 + 3*t_expr**2))
print("Family II identity check (should be 0):", E2_check)

# Family III from DGH Sec 7.4:
G1 = p**4 - 2*p**3*q - 2*p**2*q**2 - 2*p*q**3 + q**4
G2 = p**4 - 2*p**3*q + 6*p**2*q**2 - 2*p*q**3 + q**4
G3 = p**4 + 2*p**3*q - 2*p**2*q**2 + 2*p*q**3 + q**4
G4 = p**4 + 2*p**3*q + 6*p**2*q**2 + 2*p*q**3 + q**4
E3 = (p**2 - q**2)**2 * G1 * G2 * G3 * G4
u_expr = (p**2 + q**2) / (p * q)
X_expr = u_expr**2
E3_check = sp.simplify(E3 - (p**2 - q**2)**2 * (p*q)**8 * (X_expr**2 - 12*X_expr + 16) * (X_expr**2 + 4*X_expr + 16))
print("Family III identity check (should be 0):", E3_check)

# Check DGH full cuboid edges & diagonals for Family II and Family III!
a2 = (p**2 - q**2) * (p**4 + 2*p**3*q + 2*p**2*q**2 - 2*p*q**3 + q**4) * (p**4 - 2*p**3*q + 2*p**2*q**2 + 2*p*q**3 + q**4)
b2 = 4 * p * q * (p**4 - q**4)**2
c2_sq = E2
f12_2 = sp.factor(a2**2 + b2**2)
f13_2 = sp.factor(a2**2 + c2_sq)
f23_2 = sp.factor(b2**2 + c2_sq)
sp_2  = sp.factor(a2**2 + b2**2 + c2_sq)
print("Family II face/space diag squares factored:")
print("  a^2+b^2   =", f12_2)
print("  a^2+c^2   =", f13_2)
print("  b^2+c^2   =", f23_2)
print("  a^2+b^2+c^2 =", sp_2)

a3 = 2 * p * q * (p**4 + 2*p**3*q + 2*p**2*q**2 - 2*p*q**3 + q**4) * (p**4 - 2*p**3*q + 2*p**2*q**2 + 2*p*q**3 + q**4)
b3 = 8 * p**2 * q**2 * (p**2 - q**2) * (p**2 + q**2)**2
c3_sq = E3
print("Family III face/space diag squares factored:")
print("  a^2+b^2   =", sp.factor(a3**2 + b3**2))
print("  a^2+c^2   =", sp.factor(a3**2 + c3_sq))
print("  b^2+c^2   =", sp.factor(b3**2 + c3_sq))
print("  a^2+b^2+c^2 =", sp.factor(a3**2 + b3**2 + c3_sq))

# Exhaustive search for rational points on Family II quartic Y^2 = (1 - t^2)(1 + 3 t^2)
print("\nRational points on Y^2 = (1 - t^2)(1 + 3 t^2) for t = num/den, |num|, den <= 500:")
pts_II = []
for den in range(1, 501):
    for num in range(0, 501):
        if math.gcd(num, den) == 1:
            val = (den**2 - num**2) * (den**2 + 3 * num**2)
            if val >= 0 and math.isqrt(val)**2 == val:
                pts_II.append((num, den))
print("  pts_II:", pts_II)

# Exhaustive search for rational points on Family III quartic Y^2 = (X^2 - 12 X + 16)(X^2 + 4 X + 16)
print("\nRational points on Y^2 = (X^2 - 12 X + 16)(X^2 + 4 X + 16) for X = num/den, |num|, den <= 500:")
pts_III = []
for den in range(1, 501):
    for num in range(-500, 501):
        if math.gcd(abs(num), den) == 1:
            val = (num**2 - 12*num*den + 16*den**2) * (num**2 + 4*num*den + 16*den**2)
            if val >= 0 and math.isqrt(val)**2 == val:
                pts_III.append((num, den))
print("  pts_III:", pts_III)

# Also check pairwise resultants of G1, G2, G3, G4 and F1, F2, F3, F4!
F1 = q**4 + 4*p**2*q**2 - p**4
F2 = p**4 + 4*p**2*q**2 - q**4
F3 = 3*p**4 + q**4
F4 = p**4 + 3*q**4
print("\nFamily II pairwise resultants wrt p (at q=1):")
for i, A in enumerate([F1, F2, F3, F4], 1):
    for j, B in enumerate([F1, F2, F3, F4], 1):
        if i < j:
            res = sp.resultant(A.subs(q, 1), B.subs(q, 1), p)
            print(f"  Res(F{i}, F{j}) = {res} = {sp.factorint(abs(int(res)))}")

print("\nFamily III pairwise resultants wrt p (at q=1):")
for i, A in enumerate([G1, G2, G3, G4], 1):
    for j, B in enumerate([G1, G2, G3, G4], 1):
        if i < j:
            res = sp.resultant(A.subs(q, 1), B.subs(q, 1), p)
            print(f"  Res(G{i}, G{j}) = {res} = {sp.factorint(abs(int(res)))}")
