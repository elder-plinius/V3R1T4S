"""Literal Table 2 / Table 3 transcription. Parameters use paper indices."""
from fractions import Fraction as F

def family(b11=F(1,8),b21=F(1,8),c11=F(1,4),b23=F(0),b32=F(1,2),c33=F(1,10),c34=F(0)):
    b11,b21,c11,b23,b32,c33,c34=map(F,(b11,b21,c11,b23,b32,c33,c34))
    beta=max(b11,b21)
    assert all(0<=x<=1 for x in [b11,b21,c11,b23,b32,c33,c34])
    if c11==0:assert b11<=b21<=F(1,4)
    elif c11==F(1,2):assert b11<=F(1,4) and b21<=min(b11,F(1,2)-2*b11)
    else:assert 0<c11<F(1,2) and b11==b21 and b11<=F(1,4)
    assert c11<=min(F(1,2),(2-b11)/(3+2*b11+2*b21))
    assert b23<=max(F(0),(b11-b21)/(2*(1-b21)))
    hi=F(3,4)*(b11+b21)+beta/4
    assert b32<=F(1,2)+hi and F(1,2)-b32<=c33<=F(1,2)-b32+hi
    a=[[[F(0)]*4 for _ in range(4)] for _ in range(3)]
    for p in range(3):a[p][3][1:]=[F(1)]*3
    a[0][2][2]=F(1,2)
    a[1][0][0]=b11;a[1][1][0]=b21;a[1][1][2]=b23;a[1][2][1]=b32
    a[1][2][2]=F(1,2)+(b11+b21)/2+beta/2-b23*(1-b21)
    a[1][3][0]=2*(b11+b21)
    a[2][0][0]=c11;a[2][1][0]=F(1,2)-c11;a[2][2][2]=c33;a[2][2][3]=c34;a[2][3][0]=F(1)
    return a
