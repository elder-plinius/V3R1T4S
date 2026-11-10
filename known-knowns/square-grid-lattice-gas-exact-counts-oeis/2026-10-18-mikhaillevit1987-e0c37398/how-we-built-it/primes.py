# deterministic Miller-Rabin for n < 3.3e24; picks primes just below given bounds
import sys
def mr(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        if n%p==0: return n==p
    d=n-1;s=0
    while d%2==0: d//=2;s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
def below(b,k):
    out=[];n=b-1
    while len(out)<k:
        if mr(n): out.append(n)
        n-=1
    return out
if __name__=='__main__':
    print('A',*below(2**62,4)); print('B',*below(2**61,4))
