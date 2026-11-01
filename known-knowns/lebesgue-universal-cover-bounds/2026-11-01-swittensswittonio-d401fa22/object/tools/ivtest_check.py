# Verifies outward containment of the C# Iv type: records from `LebVerify ivtest N file`. Exact Fractions for + - * / sqr sqrt; mpmath.iv (rigorous, 60 digits) for sin/cos and constants.
import sys, struct, math
from fractions import Fraction as F
from mpmath import iv, mp
iv.dps = 60
def d(h): return struct.unpack('<d', struct.pack('<Q', int(h,16)))[0]
def fr(x): return F(x)
bad = 0; cnt = {}; tight = {}
def contains_pt(lo,hi,v): return fr(lo) <= v <= fr(hi)
def chk(name, cond, rec):
    global bad
    cnt[name] = cnt.get(name,0)+1
    if not cond:
        bad += 1
        if bad < 20: print("VIOLATION", name, rec)
def mpf_fr(t):
    s=-1 if t[0] else 1
    return s*F(int(t[1]))*(F(2)**int(t[2]))
def iv_bounds(v): return mpf_fr(v._mpi_[0]), mpf_fr(v._mpi_[1])
for line in open(sys.argv[1]):
    p = line.split(); op = p[0]; v = [d(x) for x in p[1:]]
    xl,xh,yl,yh,rl,rh = v
    if rl != rl or rh != rh: # NaN result: only allowed for div by interval containing 0 -> infinite or sqrt negative
        chk(op, op in ('sqrt','div'), line); continue
    if op in ('add','sub','mul','div','sqr'):
        if op == 'div' and (yl <= 0 <= yh): chk('div0', rl == -math.inf and rh == math.inf, line); continue
        vals = []
        X = [fr(xl), fr(xh)]; Y = [fr(yl), fr(yh)]
        for a in X:
            for b in Y:
                vals.append({'add':lambda:a+b,'sub':lambda:a-b,'mul':lambda:a*b,'div':lambda:a/b if b!=0 else None,'sqr':lambda:a*a}[op]())
        lo, hi = min(vals), max(vals)
        if op == 'sqr' and xl < 0 < xh: lo = F(0)
        chk(op, fr(rl) <= lo and hi <= fr(rh), line)
        w = (fr(rh)-fr(rl)); tight[op] = max(tight.get(op,0), float(w - (hi-lo)) if hi!=lo or w!=0 else 0)
    elif op == 'sqrt':
        # result [rl,rh] must satisfy rl^2 <= xl (or xl<=0) and rh^2 >= xh
        chk(op, (xl <= 0 or fr(rl)**2 <= fr(xl)) and fr(rh)**2 >= fr(xh), line)
    elif op in ('sin10','cos10','sin7'):
        fn = iv.sin if op.startswith('sin') else iv.cos
        xs = [iv.mpf(float(xl)) , iv.mpf(float(xh))]
        # exact enclosure of the function over [xl,xh] (monotone on [0,1.3] for sin; cos decreasing)
        a = fn(iv.mpf(xl)); b = fn(iv.mpf(xh))
        lo = min(iv_bounds(a)[0], iv_bounds(b)[0]); hi = max(iv_bounds(a)[1], iv_bounds(b)[1])
        chk(op, fr(rl) <= lo and hi <= fr(rh), line)
        tight[op] = max(tight.get(op,0), float(fr(rh)-fr(rl)))
    elif op.startswith('const:'):
        nm = op[6:]; x = iv
        s3 = iv.sqrt(3); pi = iv.pi; R5 = 1/(2*iv.sin(2*pi/5))
        ref = {'pi':pi,'R5':R5,'V3x0_0':1/s3,'V3x0_1':-1/(2*s3),'V5x0_1':R5*iv.cos(2*pi/5),'V5x0_2':R5*iv.cos(4*pi/5),'V5x0_3':R5*iv.cos(6*pi/5),'V5x0_4':R5*iv.cos(8*pi/5),
               'V5y0_2':R5*iv.sin(4*pi/5),'V5y0_3':R5*iv.sin(6*pi/5),'twopi5':2*pi/5,'e11':iv.mpf(1)/10**11,'e12':iv.mpf(1)/10**12}[nm]
        lo,hi = iv_bounds(ref)
        chk(op, fr(xl) <= lo and hi <= fr(xh), line)
        tight[op] = float(fr(xh)-fr(xl))
print("records checked:", cnt); print("violations:", bad); print("max extra width over exact image (per op):", tight)
sys.exit(1 if bad else 0)
