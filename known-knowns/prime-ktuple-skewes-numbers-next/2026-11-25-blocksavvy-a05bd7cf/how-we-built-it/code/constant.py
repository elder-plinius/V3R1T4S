"""C2 certified by Euler-transform identity (OEIS A005597 formula, tail supplied here).

Let s_n=(1/n)*sum_{d|n} mu(d) 2^(n/d) (number of primitive binary necklaces). For |z|<1/2,
1-2z = product_{n>=1}(1-z^n)^{s_n}. Therefore
(1-2/p)/(1-1/p)^2 = product_{n>=2}(1-p^-n)^{s_n}.
Multiplying over p>=11 (positive convergent products) gives C2=(175/256)*product_{n>=2}[zeta(n)*product_{p=2,3,5,7}(1-p^-n)]^{-s_n}.
For n>N, s_n<=2^n, and sum_{p>=11} -log(1-p^-n) <= [11^-n*(1+11/(n-1))]/(1-11^-n) <= 3*11^-n for n>=12.
Thus missing tail in log(C2) has magnitude <=3*(2/11)^(N+1)/(1-2/11), and is nonpositive.
N=100 gives <1e-73, much smaller than ball precision 256 bits.
"""
from flint import arb, fmpz, ctx

def c2ball(N=100, prec=256):
    ctx.prec=prec
    c=arb(175)/256
    for n in range(2,N+1):
        sn=sum(int(fmpz(d).moebius_mu()) * 2**(n//d) for d in range(1,n+1) if n%d==0)//n
        z=arb(n).zeta()
        for p in (2,3,5,7): z*=1-arb(p)**(-n)
        c*=z**(-sn)
    tail=3*(arb(2)/11)**(N+1)/(1-arb(2)/11)
    # tail log [-tail,0] enclosed symmetrically, harmless over-enclosure
    return c*arb(0,tail).exp(), tail

if __name__=='__main__':
    c,t=c2ball(); print('C2 =',c.str(65)); print('C_sexy =',(4*c).str(65)); print('log_tail <=',t.str(15));
    print('diameter(C2) <=',(2*c.rad()).str(15))
