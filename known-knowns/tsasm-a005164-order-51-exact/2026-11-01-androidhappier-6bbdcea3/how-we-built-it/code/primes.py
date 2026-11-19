# deterministic Miller-Rabin for n < 3.3e24 (bases first 13 primes)
def isprime(n):
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
def below(start,k):
    out=[];n=start
    while len(out)<k:
        n-=1
        if isprime(n): out.append(n)
    return out
if __name__=="__main__":
    print("P_A", below(2**62,4))
    print("P_B", below(2**61,4))
