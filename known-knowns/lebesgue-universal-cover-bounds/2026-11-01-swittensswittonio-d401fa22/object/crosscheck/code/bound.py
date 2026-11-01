"""Independent certified LOWER bound on beta(Box)=area conv(D u C3 u C5) (Mishra Prop 4.9), written
from the paper's definitions (Def 2.6, Lemma 4.7, Lemma 4.8, Prop 4.9, Lemma 4.4).
Arithmetic: mpmath interval (iv) for constants/corners/radii; every witness point is certified by EXACT
integer arithmetic against outward-rounded corner boxes; hull + area exact (integers). Candidate points are
generated with plain floats (unproved), only the exact certification matters for soundness."""
import math
from fractions import Fraction
import numpy as np
from mpmath import iv
iv.prec = 160
S_BITS = 80
S = 1 << S_BITS
TAU = Fraction(8344, 10000)

def ivf(x): return iv.mpf(float(x))          # exact conversion of a double

from mpmath.libmp import to_man_exp
def _scaled(t, up):
    sgn,man0,exp,bc = t
    man = -man0 if sgn else man0
    k = exp + S_BITS
    if k>=0: return man<<k
    return (-((-man)>>(-k))) if up else (man>>(-k))
def mp_floor_scaled(x):   # x: iv number or mpf-tuple endpoint ; floor(lower end*S)
    return _scaled(x._mpi_[0],False)
def mp_ceil_scaled(x):
    return _scaled(x._mpi_[1],True)

PI = iv.pi
R3 = 1/(2*iv.sin(PI/3))
R5 = 1/(2*iv.sin(2*PI/5))

def corners_iv(n, circ, rot, cx, cy):
    """interval boxes (xlo,xhi,ylo,yhi) as scaled ints for corners of regular n-gon, circumradius circ,
    rotated by rot (exact double), centre (cx,cy) exact doubles. Corner j at angle 2 pi j/n + rot."""
    out = []
    for j in range(n):
        a = 2*PI*j/n + ivf(rot)
        x = ivf(cx) + circ*iv.cos(a); y = ivf(cy) + circ*iv.sin(a)
        out.append((mp_floor_scaled(x), mp_ceil_scaled(x), mp_floor_scaled(y), mp_ceil_scaled(y)))
    return out

def f_lower(d):
    """lower end of f over interval d (f increasing on d>=1/2, f=pi/4 flat below): conservative."""
    if d.a <= 0.5: return float(PI.a/4)
    x = iv.mpf(1)/2/d
    acos = iv.atan2(iv.sqrt(1-x*x), x)
    v = (PI-acos)/4 + iv.sqrt(d*d-iv.mpf(1)/4)/2
    return float(v.a)

def apriori_lb(b):
    c3x,h3x,c3y,h3y,cr,hr,c5x,h5x,c5y,h5y = b
    best = iv.mpf(0)
    res = []
    for cx,hx,cy,hy in ((c3x,h3x,c3y,h3y),(c5x,h5x,c5y,h5y)):
        dx = max(abs(Fraction(cx))-Fraction(hx),Fraction(0)); dy = max(abs(Fraction(cy))-Fraction(hy),Fraction(0))
        d2 = iv.mpf(dx.numerator)/iv.mpf(dx.denominator); d2 = d2*d2
        e2 = iv.mpf(dy.numerator)/iv.mpf(dy.denominator); e2 = e2*e2
        d = iv.sqrt(d2+e2)
        res.append(f_lower(d))
    return max(res)

def radius_int(b):
    """(rho3, rho5) as scaled ints, rounded DOWN (outward erosion): rho = 1 - delta, delta rounded up."""
    c3x,h3x,c3y,h3y,cr,hr,c5x,h5x,c5y,h5y = b
    d3 = iv.sqrt(ivf(h3x)**2+ivf(h3y)**2)
    d5 = iv.sqrt(ivf(h5x)**2+ivf(h5y)**2) + 2*R5*iv.sin(ivf(hr)/2)
    return mp_floor_scaled(1-d3), mp_floor_scaled(1-d5), float(d3.b), float(d5.b)

def candidates(Vc, c0, rho, N):
    """float candidate boundary points of intersection_j D(Vc_j, rho), star-shaped about c0 (the body centre)."""
    W = c0[None,:]-Vc                        # n x 2
    if np.max(np.hypot(W[:,0],W[:,1])) >= rho: return np.zeros((0,2))
    ph = 2*np.pi*np.arange(N)/N
    u = np.stack([np.cos(ph),np.sin(ph)],1)  # N x 2
    bb = u@W.T                               # N x n
    disc = bb*bb - (W*W).sum(1)[None,:] + rho*rho
    r = -bb + np.sqrt(np.maximum(disc,0))
    j = np.argmin(r,1); rr = r[np.arange(N),j]
    P = c0[None,:] + rr[:,None]*u
    extra = []
    sw = np.nonzero(j != np.roll(j,-1))[0]
    for k in sw:
        a,bq = Vc[j[k]],Vc[j[(k+1)%N]]
        dv = bq-a; dd = math.hypot(*dv)
        if dd==0 or dd>2*rho: continue
        mid = (a+bq)/2; h = math.sqrt(max(rho*rho-dd*dd/4,0.0)); nrm = np.array([-dv[1],dv[0]])/dd
        extra += [mid+h*nrm, mid-h*nrm]
    if extra: P = np.vstack([P,np.array(extra)])
    return c0[None,:] + (1-1e-11)*(P-c0[None,:])

def certify(P, boxes, rho):
    """exact: keep points whose farthest-possible distance to every corner box is <= rho. P float array."""
    out = []
    sc = float(S)
    for x,y in P:
        X = int(x*sc); Y = int(y*sc); ok = True
        for (xl,xh,yl,yh) in boxes:
            dx = max(abs(X-xl),abs(X-xh)); dy = max(abs(Y-yl),abs(Y-yh))
            if dx*dx+dy*dy > rho*rho: ok = False; break
        if ok: out.append((X,Y))
    return out

def disc_points(N):
    R = S//2 - S//(10**12)   # radius ~ 0.5(1-2e-12) : exact check below
    pts = []
    for k in range(N):
        a = 2*math.pi*k/N
        X = int(math.cos(a)*float(R)); Y = int(math.sin(a)*float(R))
        if X*X+Y*Y <= (S//2)**2: pts.append((X,Y))
    return pts

def hull_area2(pts):
    """exact twice-area numerator (scaled by S^2) of the convex hull (monotone chain)."""
    pts = sorted(set(pts))
    if len(pts)<3: return 0,0
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[]
    for p in pts:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    up=[]
    for p in reversed(pts):
        while len(up)>=2 and cross(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    h = lo[:-1]+up[:-1]
    a2 = 0
    for i in range(len(h)):
        x1,y1 = h[i]; x2,y2 = h[(i+1)%len(h)]
        a2 += x1*y2-x2*y1
    return a2, len(h)

_V3 = None
def hull_bound(b, N, Nd=None, want_pts=False):
    """certified lower bound on beta(box) at candidate resolution N per body. returns (area Fraction, npts)."""
    c3x,h3x,c3y,h3y,cr,hr,c5x,h5x,c5y,h5y = b
    rho3,rho5,d3,d5 = radius_int(b)
    pts = disc_points(Nd or N)
    for n,circ,rot,cx,cy,rho in ((3,R3,0.0,c3x,c3y,rho3),(5,R5,cr,c5x,c5y,rho5)):
        boxes = corners_iv(n,circ,rot,cx,cy)
        Vc = np.array([[(xl+xh)/2/float(S),(yl+yh)/2/float(S)] for xl,xh,yl,yh in boxes])
        c0 = np.array([cx,cy],dtype=float)
        P = candidates(Vc,c0,rho/float(S),N)
        pts += certify(P,boxes,rho)
    a2,nh = hull_area2(pts)
    return Fraction(a2,2*S*S), nh, d3, d5

def leaf_bound(b, tiers=(1024,4096,16384), accept=TAU+Fraction(1,10**12)):
    """returns dict: apriori lb, hull lb per tier, final lower bound, accepted flag."""
    ap = apriori_lb(b)
    res = {'ap':ap,'tiers':{}}
    best = Fraction(0)
    for N in tiers:
        a,nh,d3,d5 = hull_bound(b,N)
        res['tiers'][N]=float(a); res['d3']=d3; res['d5']=d5; best=max(best,a)
    res['hull']=float(best); res['hullF']=best
    res['lb']=max(ap,float(best))
    return res
