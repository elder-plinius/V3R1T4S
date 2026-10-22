import sys
from mpmath import mp,mpf,log,exp,nstr
mp.dps=70
def load(fn):
    d={}
    for line in open(fn):
        m,_,x=line.split(); d[int(m)]=mpf(x)
    return d
def wynn(S):
    # returns table of epsilon even columns: list of lists; eps_{2k}^{(n)}
    n=len(S); e_prev=[mpf(0)]*(n+1); e_cur=list(S)
    cols=[list(S)]
    for k in range(1,n):
        nxt=[]
        for j in range(len(e_cur)-1):
            dlt=e_cur[j+1]-e_cur[j]
            nxt.append((e_prev[j+1] if len(e_prev)>j+1 else 0)+ (1/dlt if dlt!=0 else mpf(10)**60))
        e_prev,e_cur=e_cur,nxt
        cols.append(nxt)
        if len(nxt)<2: break
    return cols
if __name__=="__main__":
    kind=sys.argv[1]; d=load(sys.argv[2]); m0=int(sys.argv[3])
    ms=sorted(k for k in d if k>=m0)
    L={m:log(d[m]) for m in ms}
    D=[L[m]-L[m-1] for m in ms[1:]] if kind=='cyc' else None
    if kind=='open': D=[L[m]-L[m-1] for m in ms[1:]]
    S=[exp(x) for x in D]
    print('last raw',nstr(S[-1],30))
    cols=wynn(S)
    for k in range(0,len(cols),2):
        c=cols[k]
        print('order',k//2,[nstr(x,28) for x in c[-4:]])
