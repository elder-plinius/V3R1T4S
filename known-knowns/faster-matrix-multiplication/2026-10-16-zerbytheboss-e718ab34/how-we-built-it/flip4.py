import json,lib,random,subprocess,sys,os,glob,re,time,hashlib
import numpy as np, mk
seed=int(sys.argv[1]);dur=float(sys.argv[2]);F=sys.argv[3];tag=sys.argv[4]
pplus=float(sys.argv[5]) if len(sys.argv)>5 else 0.15
gp=sys.argv[6] if len(sys.argv)>6 else '0.0'
rnd=random.Random(seed);PISO=float(sys.argv[7]) if len(sys.argv)>7 else 0.5
d=json.load(open(F));n=d['n'];U,V,W=lib.tensors(d);R=d['m']
S=[[np.array(M[r]) for M in (U,V,W)] for r in range(R)]  # S[r][mode]
def nnz(S): return sum(int((x!=0).sum()) for t in S for x in t)
def key(x):
    nz=np.flatnonzero(x)
    if len(nz)==0: return None
    return (x*x[nz[0]]).tobytes()
def tern(x): return np.abs(x).max()<=1
def reduce(S):
    ch=True
    while ch:
        ch=False
        S[:]=[t for t in S if all(x.any() for x in t)]
        for mode in range(3):
            o=[k for k in range(3) if k!=mode]
            seen={}
            for i,t in enumerate(S):
                kk=(key(t[o[0]]),key(t[o[1]]))
                if kk in seen:
                    j=seen[kk]; a=S[j];b=S[i]
                    s=(1 if (a[o[0]]==b[o[0]]).all() else -1)*(1 if (a[o[1]]==b[o[1]]).all() else -1)
                    nv=a[mode]+s*b[mode]
                    if tern(nv):
                        a[mode]=nv; S.pop(i); ch=True; break
                else: seen[kk]=i
            if ch: break
    return S
def flip(S):
    m=len(S);mode=rnd.randrange(3);g={}
    for i,t in enumerate(S): g.setdefault(key(t[mode]),[]).append(i)
    c=[v for v in g.values() if len(v)>1]
    if not c: return False
    for _ in range(10):
        a,b=rnd.sample(rnd.choice(c),2) if True else None
        A=S[a];B=S[b]
        s=1 if (A[mode]==B[mode]).all() else -1
        o=[x for x in range(3) if x!=mode];p,q=o if rnd.random()<.5 else o[::-1]
        nPa=A[p]+s*B[p];nQb=B[q]-s*A[q]*0+(-A[q] if False else 0)
        # A: x⊗Pa⊗Qa ; B: x⊗(sPb)⊗Qb  -> x⊗(Pa+sPb)⊗Qa + x⊗sPb⊗(Qb-Qa)
        nQb=B[q]-s*0
        nQb=B[q]-A[q]
        if not(tern(nPa) and tern(nQb)) or not nPa.any() or not nQb.any(): continue
        A[p]=nPa;B[q]=nQb
        return True
    return False
def plus(S):
    m=len(S)
    for _ in range(30):
        a,b=rnd.sample(range(m),2);A=S[a];B=S[b]
        p,q,r=rnd.sample(range(3),3)
        # x⊗y⊗z + x'⊗y'⊗z' = (x-x')⊗y⊗z + x'⊗y⊗(z-z') + x'⊗(y+y')⊗z'  (modes p,q,r)
        x,y,z=A[p],A[q],A[r];x2,y2,z2=B[p],B[q],B[r]
        t1=[None]*3;t2=[None]*3;t3=[None]*3
        t1[p]=x-x2;t1[q]=y;t1[r]=z
        t2[p]=x2;t2[q]=y;t2[r]=z-z2
        t3[p]=x2;t3[q]=y+y2;t3[r]=z2
        if all(tern(v) for t in(t1,t2,t3) for v in t):
            S[:]=[t for i,t in enumerate(S) if i not in(a,b)]+[t1,t2,t3]
            return True
    return False

dims=n
def iso(S):
    n1,n2,n3=dims
    kind=rnd.randrange(3);sg=rnd.choice([1,-1])
    sz=[n1,n2,n3][kind]
    i,j=rnd.sample(range(sz),2)
    T=copyS(S)
    for t in T:
        U=t[0].reshape(n1,n2);V=t[1].reshape(n2,n3);Wm=t[2].reshape(n3,n1)
        if kind==0:   # P on n1: U->PU, W->W P^-1
            U[i,:]+=sg*U[j,:]; Wm[:,j]-=sg*Wm[:,i]
        elif kind==1: # Q on n2: U->U Q^-1, V->Q V
            V[i,:]+=sg*V[j,:]; U[:,j]-=sg*U[:,i]
        else:         # R on n3: V->V R^-1, W->R W
            Wm[i,:]+=sg*Wm[j,:]; V[:,j]-=sg*V[:,i]
        t[0]=U.reshape(-1);t[1]=V.reshape(-1);t[2]=Wm.reshape(-1)
        if not all(tern(x) for x in t): return False
    S[:]=T;return True
def copyS(S): return [[x.copy() for x in t] for t in S]
def chash(S):
    return hashlib.md5(b''.join(sorted(b''.join(x.tobytes() for x in t) for t in S))).hexdigest()
def red(S,tagf):
    f=f'{tagf}/s.txt'
    mk.write([t[0].tolist() for t in S],[t[1].tolist() for t in S],[t[2].tolist() for t in S],n,f)
    od=f'{tagf}/o';subprocess.run(['rm','-rf',od])
    subprocess.run(['./reducer','-i',f,'-o',od,'--count','16','--seed',str(rnd.randrange(10**6)),'-ga',str(rnd.choice([0.1,0.25,0.5])),'-gi',str(rnd.choice([0.2,0.5,1.0])),'-gr',str(rnd.choice([0.05,0.1,0.3])),'-gp',str(rnd.choice([0.0,0.0,0.2])),'--max-no-improvements','15'],capture_output=True)
    fs=glob.glob(od+'/*.json')
    if not fs: return None
    c=min(int(re.search(r'cr(\d+)',x).group(1)) for x in fs)
    return c,[x for x in fs if f'cr{c}_' in x][0]
tg=f'fl{tag}{seed}';os.makedirs(tg,exist_ok=True)
base=int(re.search(r'cr(\d+)',F).group(1))
visited=set();best=10**9;t0=time.time();cur=copyS(S);cn=nnz(cur);k=0;nred=0;minnz=cn
Ssaved=copyS(cur)
while time.time()-t0<dur:
    T=copyS(cur)
    if rnd.random()<PISO:
        ok=False
        for _ in range(rnd.randint(1,3)): ok=iso(T) or ok
        if not ok: continue
    elif rnd.random()<pplus and plus(T):
        # walk down
        for _ in range(rnd.randint(5,60)):
            reduce(T)
            if len(T)<=R: break
            flip(T)
        reduce(T)
        if len(T)!=R: continue
    else:
        for _ in range(rnd.randint(1,8)): flip(T)
        reduce(T)
        if len(T)!=R: continue
    new=nnz(T)
    # tabu / annealed acceptance
    if new>cn+rnd.choice([0,0,2,4,8,16]): continue
    h=chash(T)
    if h in visited: continue
    visited.add(h);cur=T;cn=new;k+=1
    if len(visited)>20000: visited.clear()
    if cn<=minnz+6 and rnd.random()<0.5 or k%7==0:
        minnz=min(minnz,cn)
        r=red(T,tg);nred+=1
        if r and r[0]<best:
            best=r[0];subprocess.run(['cp',r[1],f'{tg}/best_cr{best}.json'])
            print(round(time.time()-t0),'k',k,'nnz',cn,'best',best,'base',base,flush=True)
    if k%400==0: # basin hop: restart from original with random-walk
        cur=copyS(Ssaved);cn=nnz(cur)
        for _ in range(rnd.randint(20,200)): flip(cur)
        reduce(cur)
        if len(cur)!=R: cur=copyS(Ssaved)
        cn=nnz(cur)
print('done',k,nred,best,'base',base)
