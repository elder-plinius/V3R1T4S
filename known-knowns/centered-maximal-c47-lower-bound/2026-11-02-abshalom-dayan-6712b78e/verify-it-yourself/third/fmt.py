#!/usr/bin/env python3
"""Turn exact integer output of vsweep/vtree into rigorous decimals, exact integer arithmetic only.
usage: fmt.py sweep|tree outputfile"""
import sys,re
from fractions import Fraction as F
def dec(fr,digs=14,up=False):
    v=fr*10**digs; q=v.numerator//v.denominator
    if up and q*v.denominator!=v.numerator: q+=1
    s=str(q).rjust(digs+1,'0'); return s[:-digs]+'.'+s[-digs:]
mode,fn=sys.argv[1:3]
txt=open(fn).read()
h=re.search(r'bits (\d+) kbits (\d+) Lx (\d+) Ly (\d+) M (\d+) n (\d+)',txt)
b,k,Lx,Ly,M,n=map(int,h.groups())
den=2**(b+2*k)*M   # V=A_U2/(2^(2b+2k)) / (M/2^b)
if mode=='sweep':
    a=int(re.search(r'area_inner_U2 (\d+)',txt)[1]);o=int(re.search(r'area_outer_U2 (\d+)',txt)[1])
    print('SWEEP V_lower',dec(F(a,den)),'V_upper',dec(F(o,den),up=True),'width',dec(F(o-a,den),up=True),' area_lower',dec(F(a,2**(2*b+2*k))),'V*mass_lower',dec(F(a,2**(2*b+2*k))))
    print('      trivial cap area/mass',dec(F(Lx*Ly,2**b*M),up=True))
else:
    tot=int(re.search(r'total_U2 (\d+)',txt)[1])
    for m in re.finditer(r'depth (\d+) side_log2_U (\d+) cumcov_U2 (\d+) cumunc_U2 (\d+)',txt):
        d,sl,c,u=map(int,m.groups())
        if c==0 and u==0: continue
        print(f'TREE depth {d} side 2^{sl-(b+k)} V_lower {dec(F(c,den),10)} V_upper {dec(F(tot-u,den),10,True)} width {dec(F(tot-u-c,den),10,True)}')
