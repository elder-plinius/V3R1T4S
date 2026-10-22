import sys,struct
from mpmath import mp,mpf
import numpy as np
mp.dps=80
def rq(prefix,m):
    raw=open(prefix+'.bin','rb').read(); NW=1<<m
    arr=np.frombuffer(raw,dtype=np.uint64).reshape(2,NW,2)  # little endian lo,hi
    def toint(k): return [int(l)|(int(h)<<64) for l,h in arr[k]]
    v=toint(0); w=toint(1)
    num=sum(a*b for a,b in zip(v,w)); den=sum(a*a for a in v)
    return mpf(num)/mpf(den)
if __name__=="__main__":
    print(rq(sys.argv[1],int(sys.argv[2])))
