#!/usr/bin/env python3
"""Compare Program A (row-major, CRT over P_A), Program B (column-major, CRT over P_B, and wraparound mod 2^128)
and the OEIS DATA for every n.  usage: compare.py A_crt.txt B_crt.txt B_wrap128.txt"""
import re,sys
pub=[1,1,1,2,4,13,46,248,1516,13654,142873,2156888,38456356,974936056,29540545024,1259111024288,64726478396896,4641989615977216,404396533544588344,48825344233129714772,7202552030561982627472,1464587581921220811285325,365627222082497915618219716,125253905685915522767942493032,52893528399758443649956432899616]
def load(f,pat):
    d={}
    for l in open(f):
        m=re.search(pat,l)
        if m: d[int(m[1])]=(int(m[2]), 'check=OK' in l if 'check=' in l else True)
    return d
A=load(sys.argv[1],r"n=(\d+) value=(\d+)"); B=load(sys.argv[2],r"n=(\d+) value=(\d+)"); W=load(sys.argv[3],r"n=(\d+) mode=wrap2\^128 value_mod_2\^128=(\d+)")
allok=True
for n in sorted(set(A)&set(B)):
    a=A.get(n,(None,False)); b=B.get(n,(None,False)); w=W.get(n,(None,True))
    agree = a[0] is not None and a[0]==b[0] and a[1] and b[1] and (w[0] is None or w[0]==a[0]%2**128)
    o = "" if n>=len(pub) else ("OEIS=yes" if a[0]==pub[n] else "OEIS=NO")
    if not agree or o=="OEIS=NO": allok=False
    print(f"n={n} A={a[0]} B={b[0]} wrap128={'-' if w[0] is None else ('same' if w[0]==a[0]%2**128 else 'DIFF')} A==B:{agree} {o}")
print(("ALL_AGREE" if allok else "MISMATCH")+f" over n={min(set(A)&set(B))}..{max(set(A)&set(B))}; only in A: {sorted(set(A)-set(B))}")
