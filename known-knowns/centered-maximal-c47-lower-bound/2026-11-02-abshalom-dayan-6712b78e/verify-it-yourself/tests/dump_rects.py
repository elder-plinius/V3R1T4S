#!/usr/bin/env python3
# Checker A. All integers. Atoms x,y,m are numerators over 2^b, with 0 <= x < Lx, 0 <= y < Ly, m > 0, extended by the periods.
# For a box [x1,x2]x[y1,y2] with S its atoms and rho rational with 4 rho^2 <= mu(S), every z in
# [x2-rho,x1+rho]x[y2-rho,y1+rho] has S inside Q(z,rho), so M mu(z) >= 1 (Q(z,rho) closed, average >= mu(S)/(4 rho^2)).
# Enumerate boxes, take the exact area of the union mod the periods. Prints value = area/(cell mass).
# Usage: check_a.py CERT.json [REACH] [BAR as a fraction]
import sys, json, math
from fractions import Fraction as F
c = json.load(open(sys.argv[1])); b = c['bits']; Lx, Ly = c['Lx'], c['Ly']; A = c['atoms']
reach = int(F(sys.argv[2] if len(sys.argv) > 2 else '6')*(1 << b))
assert Lx > 0 and Ly > 0 and all(0 <= x < Lx and 0 <= y < Ly and m > 0 for x, y, m in A)
total = sum(m for *_, m in A)
R = 40; sc = 1 << (R-b); assert R >= b
ax, ay = reach//Lx+2, reach//Ly+2
P = [(x+u*Lx, y+v*Ly, m) for x, y, m in A for u in range(ax+1) for v in range(ay+1)]
xs = sorted({p[0] for p in P}); ys = sorted({p[1] for p in P}); ix = {v: i for i, v in enumerate(xs)}; iy = {v: i for i, v in enumerate(ys)}
G = [[0]*(len(ys)+1) for _ in range(len(xs)+1)]
for x, y, m in P: G[ix[x]+1][iy[y]+1] += m
for i in range(1, len(xs)+1):
    r = G[i]; q = G[i-1]; s = 0
    for j in range(1, len(ys)+1):
        s += r[j]; r[j] = q[j]+s
rects = set()
lefts = sorted({a[0] for a in A}); bots = sorted({a[1] for a in A})
for x1 in lefts:
    i1 = ix[x1]; Gi1 = G[i1]
    for y1 in bots:
        j1 = iy[y1]
        for i2 in range(i1, len(xs)):
            dx = xs[i2]-x1
            if dx > reach: break
            Gi2 = G[i2+1]; base = Gi2[j1]-Gi1[j1]
            for j2 in range(j1, len(ys)):
                dy = ys[j2]-y1
                if dy > reach: break
                M = Gi2[j2+1]-Gi1[j2+1]-base      # numerator over 2^b
                if M <= 0: continue
                e = max(dx, dy)
                if e*e > M << b: continue         # needs side <= 2 rho = sqrt(mu)
                # rho = floor(2^R sqrt(M/2^b)/2)/2^R, so 4 rho^2 <= M/2^b exactly
                rho = math.isqrt((M << (2*R-b)) >> 2)
                assert 4*rho*rho <= M << (2*R-b)
                a, bb, cc, d = (xs[i2]*sc-rho, x1*sc+rho, ys[j2]*sc-rho, y1*sc+rho)
                if bb > a and d > cc: rects.add((a, bb, cc, d))

with open(sys.argv[3] if len(sys.argv)>3 else 'rects.txt','w') as f:
    f.write(f"{len(rects)}\n")
    for r in sorted(rects,key=lambda t:-(t[1]-t[0])*(t[3]-t[2])): f.write("%d %d %d %d\n"%r)
print(len(rects),'rects dumped, sc',sc,'Lx',Lx*sc,'Ly',Ly*sc)
