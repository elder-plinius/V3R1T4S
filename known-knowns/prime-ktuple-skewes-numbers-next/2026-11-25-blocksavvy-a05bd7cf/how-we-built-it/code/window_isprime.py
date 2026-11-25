# Independent local check by primality testing (no sieve): every n in [lo, p] with n and n+6 tested by flint's
# fmpz.is_prime (deterministic BPSW range < 2^64) and sympy.isprime; prints pair starts in the window.
import sys, sympy
from flint import fmpz
lo,hi=int(sys.argv[1]),int(sys.argv[2])
pairs=[]
for n in range(lo|1,hi+1,2):
    if fmpz(n).is_prime() and fmpz(n+6).is_prime():
        assert sympy.isprime(n) and sympy.isprime(n+6); pairs.append(n)
print('window',lo,hi,'pairs',len(pairs)); print('last5',pairs[-5:])
