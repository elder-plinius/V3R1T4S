# A000081 via Euler transform recurrence, then Otter's dissimilarity formula; own code.
N=25
r=[0]*(N+1); r[1]=1
for n in range(1,N):
    r[n+1]=sum(sum(d*r[d] for d in range(1,k+1) if k%d==0)*r[n-k+1] for k in range(1,n+1))//n
for n in range(18,N+1):
    s=sum(r[i]*r[n-i] for i in range(1,n))
    if n%2==0: s-=r[n//2]
    print(n, r[n]-s//2)
