#!/usr/bin/env python3
"""lemma1_small.py: exact enumeration test of Lemma 1 of PROOF.md: 2 E L(x,y) <= E L(x+y,x+y), for x+y <= 7,
exact Fractions, stdlib only. Also prints E L(n,n)/n, a brute-force value of the superadditive sequence."""
from fractions import Fraction as Fr
from functools import lru_cache
def lcs(a,la,b,lb):
    prev=[0]*(lb+1)
    for i in range(la):
        ai=(a>>i)&1; cur=[0]*(lb+1)
        for j in range(lb):
            cur[j+1]=max(prev[j+1],cur[j],prev[j]+(1 if ai==((b>>j)&1) else 0))
        prev=cur
    return prev[lb]
@lru_cache(None)
def EL(x,y):
    s=0
    for a in range(1<<x):
        for b in range(1<<y):
            s+=lcs(a,x,b,y)
    return Fr(s,1<<(x+y))
ok=True
for n in range(1,8):
    print(f'n={n} E L(n,n)={EL(n,n)} ={float(EL(n,n)):.6f} per char {float(EL(n,n))/n:.6f}')
    for x in range(0,n+1):
        y=n-x
        if not 2*EL(x,y)<=EL(n,n): ok=False; print('FAIL',x,y)
print('Lemma 1 small cases hold:',ok)
