# Program C: Python brute force with Fractions and statistics-free median, n<=10 (definition check)
import sys
from fractions import Fraction
def parts(s):
    if not s: yield []; return
    f=s[0]
    for p in parts(s[1:]):
        for i in range(len(p)):
            yield p[:i]+[[f]+p[i]]+p[i+1:]
        yield [[f]]+p
def med(xs):
    xs=sorted(xs); m=len(xs)
    return Fraction(xs[m//2]) if m%2 else Fraction(xs[m//2-1]+xs[m//2],2)
for n in range(1,int(sys.argv[1])+1):
    c=sum(1 for p in parts(list(range(1,n+1))) if med([med(b) for b in p]).denominator==1)
    print(n,c,flush=True)
