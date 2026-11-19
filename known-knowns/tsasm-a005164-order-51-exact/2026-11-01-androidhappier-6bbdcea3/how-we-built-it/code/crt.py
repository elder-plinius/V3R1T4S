#!/usr/bin/env python3
"""CRT-combine residue files 'n=.. p=.. a_mod_p=..' : reconstruct with the first k primes (k = all but the last),
check with the last prime. Prints n, value, check result, and published OEIS value comparison."""
import sys,re,glob
from functools import reduce
pub=[1,1,1,2,4,13,46,248,1516,13654,142873,2156888,38456356,974936056,29540545024,1259111024288,64726478396896,4641989615977216,404396533544588344,48825344233129714772,7202552030561982627472,1464587581921220811285325,365627222082497915618219716,125253905685915522767942493032,52893528399758443649956432899616]
res={}  # n -> {p:r}
for f in sys.argv[1:]:
    for line in open(f):
        m=re.match(r"n=(\d+) p=(\d+) a_mod_p=(\d+)",line)
        if m: res.setdefault(int(m[1]),{})[int(m[2])]=int(m[3])
def crt(pairs):
    x,M=0,1
    for p,r in pairs:
        t=((r-x)*pow(M,-1,p))%p; x+=M*t; M*=p
    return x,M
for n in sorted(res):
    ps=sorted(res[n].items())
    if len(ps)<2: print(n,"need >=2 primes"); continue
    x,M=crt(ps[:-1]); pc,rc=ps[-1]
    ok = x%pc==rc
    cmp = "" if n>=len(pub) else ("matches OEIS" if x==pub[n] else f"DIFFERS from OEIS {pub[n]}")
    print(f"n={n} value={x} modulus_bits={M.bit_length()} value_bits={x.bit_length()} check_prime={pc} check={'OK' if ok else 'FAIL'} {cmp}")
