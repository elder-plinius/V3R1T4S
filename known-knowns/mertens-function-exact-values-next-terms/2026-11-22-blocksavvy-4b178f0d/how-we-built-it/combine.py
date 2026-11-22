import sys
B=10**8; rows={}
for l in open(sys.argv[1]):
    b,s,mx,mn=map(int,l.split()); rows[b]=(s,mx,mn)
n=max(rows)+1; assert all(b in rows for b in range(n)), "missing blocks"
M=0; known={1:1928,9:-222,10:-33722,11:-87856}  # M(10^8.. ) checks by block index end
targets={k:None for k in range(14,20)}; out=[]
for b in range(n):
    s,mx,mn=rows[b]
    for k in targets:
        if targets[k] is None and (M+mx>=2**k or M+mn<=-2**k): targets[k]=(b,M)
    M+=s; x=(b+1)*B
    for e,v in [(8,1928),(9,-222),(10,-33722),(11,-87856)]:
        if x==10**e: out.append(f"M(10^{e}) = {M} expected {v} {'OK' if M==v else 'MISMATCH'}")
out.append(f"blocks {n}, covered 1..{n*B}, M({n*B}) = {M}")
for k,v in targets.items(): out.append(f"2^{k}: first block {v[0] if v else None} (M before block = {v[1] if v else None}) scan: msieve scan {v[0]*B+1 if v else ''} {(v[0]+1)*B if v else ''} {v[1] if v else ''} {2**k}")
print("\n".join(out))
