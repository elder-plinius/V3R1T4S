#!/usr/bin/env python3
# Writes calibration certificates at 40 bits: Lin's measure from the page's formula, Tomar's from his exact rational file.
import json,sys
from fractions import Fraction as F
from decimal import Decimal as D,getcontext
getcontext().prec=60
s=D(22).sqrt(); h=(5+s)/6; V=h+1; w=(17+4*s)/9; u=(2+s)/3
a=2*h-(2*(2+w)).sqrt()/2-u/2; b=V-D(2).sqrt()*u/2-w.sqrt()/2
Phi=(2*h*V-4*a*b)/(1+w); print('Phi formula',Phi,'h',h,'V',V,'w',w,'a',a,'b',b)
B=40; S=1<<B
r=lambda d:int((d*S).to_integral_value())
json.dump(dict(bits=B,Lx=r(2*h),Ly=r(V),atoms=[[0,0,S],[r(h),0,r(w)]]),open('out/lin40.json','w'))
t=json.load(open(sys.argv[1])); print('tomar pts sample',t['pts'][:2],'lam',t['lam'])
Px,Py=F(t['Px']),F(t['Py']); lam=F(t['lam'])
at={}
for p in t['pts']:
    x,y,m=[F(str(v)) for v in (p[:3] if isinstance(p,list) else (p['x'],p['y'],p['m']))]
    k=(round(x%Px*S),round(y%Py*S)); at[k]=at.get(k,0)+round(m*S)
json.dump(dict(bits=B,Lx=round(Px*S),Ly=round(Py*S),atoms=[[a,b,m] for (a,b),m in sorted(at.items())]),open('out/tomar40.json','w'))
print('tomar atoms',len(at),'exact cell area/mass ceiling',float(Px*Py/sum(F(str(p[2] if isinstance(p,list) else p['m'])) for p in t['pts'])))
