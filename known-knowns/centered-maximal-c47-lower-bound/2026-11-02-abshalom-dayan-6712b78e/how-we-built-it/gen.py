#!/usr/bin/env python3
# gen.py Lx Ly m1 L [dnA dnB] : writes a fam5 parameter file from the strip equations and the brick tile table. No atom of Tomar's enters; the frame arguments 3.3 2.75 4.0 are his frame values rounded.
# Strip equations (mu terms are first estimates of the row mass inside the box):
#  A: y in [ sqrt(1+.05)/2 , Ly - sqrt(4 m1+2+.6)/2 ], |x| <= Lx/2 - sqrt(1+m1+.2)/2
#  B: y in [ sqrt(m1+.1)/2 , Ly - sqrt(2 m1+2+.25)/2 ], x in [ sqrt(1+m1+.2)/2 , Lx - sqrt(2 m1+4+.35)/2 ]
# Tile for unit strip height: L levels, equal atoms m, period p, level spacing (1-sqrt m)/(L-1), alternate levels shifted by p/2.
import sys,math
Lx,Ly,m1=map(float,sys.argv[1:4]);L=int(sys.argv[4]);dA=int(sys.argv[5]) if len(sys.argv)>5 else 0;dB=int(sys.argv[6]) if len(sys.argv)>6 else 0
T={1:(1.0,1.2071),2:(.1786,.5101),3:(.0718,.32345),4:(.03765,.23422),5:(.023932,.18674),6:(.016293,.15408),7:(.011352,.12861),8:(.008702,.11261)}
m,p=T[L]
s=math.sqrt
yal=s(1.05)/2;yah=Ly-s(4*m1+2.6)/2;xa=Lx/2-s(1+m1+.2)/2
ybl=s(m1+.1)/2;ybh=Ly-s(2*m1+2.25)/2;xbl=s(1+m1+.2)/2;xbr=Lx-s(2*m1+4.35)/2
def row(anch,c,lo,hi,hl,dn):
    H=hi-lo;mid=(lo+hi)/2;n=max(1,round(2*hl/(p*H))+dn);d=(1-s(m))/(L-1)*H if L>1 else 0
    M=n*L*m*H*H
    o=[f"{anch} {c:.9g} {mid:.9g} {hl:.9g} {M:.9g} {n} {L}"]
    for j in range(L):
        phi=(.25 if j%2 else -.25) if L>1 else 0
        o.append(f"{(j-(L-1)/2)*d:.9g} 1 {phi}")
    return o
print(f"{Lx} {Ly} {m1} 2");print('\n'.join(row(0,(xbl+xbr)/2,ybl,ybh,(xbr-xbl)/2,dB)));print('\n'.join(row(1,0,yal,yah,xa,dA)))
