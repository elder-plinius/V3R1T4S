# independent combiner for msieve2 output (block size B given), reports M at 10^9..10^11 and first block per 2^k
import sys
B=int(sys.argv[2]); d={}
for l in open(sys.argv[1]):
    b,s,mx,mn=map(int,l.split()); d[b]=(s,mx,mn)
n=0
while n in d: n+=1
print(f"contiguous blocks 0..{n-1}, covered 1..{n*B} (lines {len(d)})")
M=0; first={}
for b in range(n):
    s,mx,mn=d[b]
    for k in range(14,20):
        if k not in first and max(M+mx,-(M+mn))>=2**k: first[k]=(b,M)
    M+=s
    if (b+1)*B in (10**9,10**10,10**11): print(f"M({(b+1)*B}) = {M}")
print(f"M({n*B}) = {M}")
for k in range(14,20):
    if k in first: b,M0=first[k]; print(f"2^{k}: block {b} scan args: {b*B+1} {(b+1)*B} {M0} {2**k}")
    else: print(f"2^{k}: not reached by {n*B}")
