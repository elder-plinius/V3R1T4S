import sys
from fractions import Fraction
from math import isqrt
fn, m, pub = sys.argv[1], int(sys.argv[2]), sys.argv[3]
rows=[]
for l in open(fn):
    i,v,s=l.split(); rows.append((int(i),int(v,16),int(s,16)))
print("orbits:",len(rows), "ids contiguous:", [r[0] for r in rows]==list(range(len(rows))))
print("all v > 0:", all(r[1]>0 for r in rows), " min v bits:", min(r[1] for r in rows).bit_length(), " max v bits:", max(r[1] for r in rows).bit_length())
rat=[Fraction(r[2],r[1]) for r in rows]
hi=max(rat); lo=min(rat)
ih=rat.index(hi); il=rat.index(lo)
print("argmax orbit",ih,"argmin orbit",il)
print("C_hi = max (Cv)_i/v_i exactly = %d / %d"%(hi.numerator,hi.denominator))
print("C_hi (decimal 40 digits):", "%d.%s"%(hi.numerator//hi.denominator, str((hi.numerator%hi.denominator)*10**40//hi.denominator).zfill(40)))
print("C_lo = min ratio (decimal 40):", "%d.%s"%(lo.numerator//lo.denominator, str((lo.numerator%lo.denominator)*10**40//lo.denominator).zfill(40)))
print("C_hi - C_lo (float):", float(hi-lo), " relative:", float((hi-lo)/hi))
# outward rounded upper bound for C_hi^(1/m): smallest U/10^D with (U/10^D)^m >= hi
D=40
n,d=hi.numerator,hi.denominator
def upper(D):
    lo_,hi_=0,10**(D+2)
    # find least U with U^m * d >= n*10^(D m)
    while lo_<hi_:
        mid=(lo_+hi_)//2
        if mid**m*d>=n*10**(D*m): hi_=mid
        else: lo_=mid+1
    return lo_
def lower(D):
    U=upper(D)
    return U-1 if U**m*d>n*10**(D*m) else U
U=upper(D); L=lower(D)
fmt=lambda U,D: "%d.%s"%(U//10**D,str(U%10**D).zfill(D))
print("W <= C_hi^(1/m) <= (outward rounded UP, 40 decimals):", fmt(U,D))
print("   (rounded down, 40 decimals):", fmt(L,D))
U20=upper(20); print("outward rounded UP at 20 decimals:", fmt(U20,20))
P=Fraction(pub)
margin=Fraction(U,10**D)
print("published bound:",pub," improvement (published - rounded-up claim) =", float(P-margin), " >= 1e-9 :", (P-margin)>=Fraction(1,10**9))
print("exact check, margin as Fraction >= 1e-9:", P-margin >= Fraction(1,10**9))
