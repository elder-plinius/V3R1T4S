import json
def count_part(f,o): return len(f)+sum(max(0,len(e)-1) for e in o)
def cr(d): return count_part(d['u_fresh'],d['u'])+count_part(d['v_fresh'],d['v'])+count_part(d['w_fresh'],d['w'])
def expand(n_in,fresh,out):
    vs=[[1 if j==i else 0 for j in range(n_in)] for i in range(n_in)]
    for e in fresh:
        assert len(e)==2 and e[0]['index']!=e[1]['index']
        v=[0]*n_in
        for t in e:
            assert t['value'] in(-1,1) and 0<=t['index']<len(vs)
            for k in range(n_in): v[k]+=t['value']*vs[t['index']][k]
        vs.append(v)
    mat=[]
    for e in out:
        seen=set();v=[0]*n_in
        for t in e:
            assert t['value'] in(-1,1) and t['index'] not in seen and 0<=t['index']<len(vs)
            seen.add(t['index'])
            for k in range(n_in): v[k]+=t['value']*vs[t['index']][k]
        mat.append(v)
    return mat
def tensors(d):
    n1,n2,n3=d['n'];m=d['m']
    U=expand(n1*n2,d['u_fresh'],d['u']);V=expand(n2*n3,d['v_fresh'],d['v'])
    WT=expand(m,d['w_fresh'],d['w'])
    assert len(U)==m and len(V)==m and len(WT)==n1*n3
    W=[[WT[c][r] for c in range(n1*n3)] for r in range(m)]
    return U,V,W
def brent(n,U,V,W):
    n1,n2,n3=n;m=len(U);bad=0
    for a in range(n1*n2):
        i1,j1=divmod(a,n2)
        for b in range(n2*n3):
            j2,k1=divmod(b,n3)
            for c in range(n3*n1):
                k2,i2=divmod(c,n1)
                t=1 if (i1==i2 and j1==j2 and k1==k2) else 0
                s=sum(U[r][a]*V[r][b]*W[r][c] for r in range(m) if U[r][a] and V[r][b])
                if s!=t: bad+=1
    return bad
def verify(path):
    d=json.load(open(path)); 
    if isinstance(d['n'],int): pass
    U,V,W=tensors(d)
    ent=all(x in(-1,0,1) for M in(U,V,W) for r in M for x in r)
    return dict(n=d['n'],m=d['m'],cr=cr(d),brent_bad=brent(d['n'],U,V,W),ternary=ent)
