#!/usr/bin/env python3
"""sim_check.py: run the certificate's policy on random real strings; assert after every step that every
frontier value F_p is <= true LCS(A_x, B_{l+p}) computed by a plain DP, and report reward rate.
usage: sim_check.py N states steps seed"""
import sys, array, random
def main():
    N=int(sys.argv[1]); st=array.array('I')
    with open(sys.argv[2],'rb') as f: st.frombytes(f.read())
    P=1<<31; pol={x&~P:x>>31 for x in st}; T=int(sys.argv[3]); rnd=random.Random(int(sys.argv[4]))
    A=[]; B=[rnd.randint(0,1) for _ in range(N)]; l=0; F=[0]*(N+1)
    # plain DP table rows kept: lcs[j] for current x over all columns revealed so far, recomputed when needed
    lcs=[0]*(len(B)+1); worst=10**9; col=[0]
    def code():
        win=B[l:l+N]; 
        if win[N-1]==1: win=[1-c for c in win]
        s=0
        for p in range(N):
            s|=(F[p+1]-F[p])<<p; s|=win[p]<<(N+p)
        return s
    for t in range(T):
        s=code()
        if s not in pol: print('REJECT state not in S',s); return 1
        if pol[s]:
            a=rnd.randint(0,1); A.append(a); G=[F[0]]*(N+1)
            for p in range(N):
                G[p+1]=max(F[p+1],G[p],F[p]+(1 if B[l+p]==a else 0))
            F=G
            nl=[0]*(len(B)+1)
            for j in range(1,len(B)+1):
                nl[j]=max(lcs[j],nl[j-1],lcs[j-1]+(1 if B[j-1]==a else 0))
            lcs=nl
            col=col+[nl[len(B)]]
        else:
            c=rnd.randint(0,1); B.append(c); l+=1; F=F[1:]+[F[N]]
            # extend the plain LCS table by one column, using the kept last column
            newcol=[0]*(len(A)+1)
            for i in range(1,len(A)+1):
                newcol[i]=max(col[i],newcol[i-1],col[i-1]+(1 if c==A[i-1] else 0))
            col=newcol
            lcs=lcs+[col[len(A)]]
        for p in range(N+1):
            if F[p]>lcs[l+p]: print('VIOLATION',t,p,F[p],lcs[l+p]); return 1
        worst=min(worst,min(lcs[l+p]-F[p] for p in range(N+1)))
    print(f'N={N} steps={T} x={len(A)} y={len(B)} reward=F0={F[0]} rate2={2*F[0]/T:.5f} trueLCS={lcs[len(B)]} true_rate={2*lcs[len(B)]/(len(A)+len(B)):.5f} no violation')
    return 0
sys.exit(main())
