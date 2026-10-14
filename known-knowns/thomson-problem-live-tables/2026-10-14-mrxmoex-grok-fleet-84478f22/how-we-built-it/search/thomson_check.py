#!/usr/bin/env python3
"""Thomson checker from the bank definition: E = sum_{i<j} 1/|x_i-x_j| on unit sphere (mpmath, 30 dps).
Usage: thomson_check.py <deeter_index.html> <points_file> -> prints N, E*, table E, verdict (strictly lower by >=1e-6?)
Also: parse_table(html)->{N:E}."""
import re,sys
from mpmath import mp,mpf,sqrt
mp.dps=30
def parse_table(h):
    t={}
    for r in re.split(r'<tr[^>]*>',h)[1:]:
        c=[re.sub('<[^>]*>','',x).strip() for x in re.split(r'<td[^>]*>',r)[1:]]
        if len(c)>=3 and c[0].isdigit():
            try:t[int(c[0])]=mpf(c[2])
            except Exception:pass
    return t
def energy(P):
    P=[[mpf(a) for a in p] for p in P]
    P=[[a/sqrt(sum(b*b for b in p)) for a in p] for p in P]
    E=mpf(0)
    for i in range(len(P)):
        for j in range(i+1,len(P)):
            E+=1/sqrt(sum((P[i][k]-P[j][k])**2 for k in range(3)))
    return E
def load(f):
    return [list(map(float,l.split()[:3])) for l in open(f) if len(l.split())>=3 and re.match(r'^\s*[-+0-9.]',l)]
def verdict(E,Et): return 'BEATS' if Et-E>=mpf('1e-6') else 'NOT_LOWER'
if __name__=='__main__':
    T=parse_table(open(sys.argv[1]).read());P=load(sys.argv[2]);N=len(P);E=energy(P)
    print('N',N,'E*',mp.nstr(E,15),'table',mp.nstr(T.get(N,mpf('inf')),15),verdict(E,T.get(N,mpf('inf'))))
