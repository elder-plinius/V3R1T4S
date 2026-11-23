# independent checker: mu via sympy.factorint (Pollard rho / trial), compare block sums/extrema from msieve (B=1000)
import subprocess,random,sys,os
MSIEVE=os.environ.get("MSIEVE","./msieve")
from sympy import factorint
random.seed(20261122); B=1000; ok=True
bs=[1,2,3]+[random.randrange(290000000,340000000) for _ in range(6)]   # blocks near 3e11
for b in bs:
    r=subprocess.run([MSIEVE,"blocks",str(B),str(b),str(b+1)],capture_output=True,text=True).stdout.split()
    s=mx=mn=0
    for n in range(b*B+1,(b+1)*B+1):
        f=factorint(n); mu=0 if any(e>1 for e in f.values()) else (-1)**len(f)
        s+=mu; mx=max(mx,s); mn=min(mn,s)
    good=[int(r[1]),int(r[2]),int(r[3])]==[s,mx,mn]; ok&=good
    print(f"block {b} [{b*B+1},{(b+1)*B}] sieve {r[1:]} independent {[s,mx,mn]} {'AGREE' if good else 'DISAGREE'}")
# known mu(1..30)
mus=[1,-1,-1,0,-1,1,-1,0,0,1,-1,0,-1,1,1,0,-1,0,-1,0,1,1,-1,0,0,1,0,0,-1,-1]
r=subprocess.run([MSIEVE,"blocks","30","0","1"],capture_output=True,text=True).stdout.split()
print("M(30) sieve",r[1],"known",sum(mus), "AGREE" if int(r[1])==sum(mus) else "DISAGREE"); ok&=int(r[1])==sum(mus)
print("ALL_AGREE" if ok else "SOME_DISAGREE")
