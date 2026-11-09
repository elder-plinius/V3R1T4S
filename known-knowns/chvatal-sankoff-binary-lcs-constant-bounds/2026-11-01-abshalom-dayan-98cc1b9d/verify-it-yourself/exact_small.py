#!/usr/bin/env python3
"""exact_small.py N states V K m: small-case tests of PROOF.md, exact arithmetic, stdlib only.
 (a) exact gain of the policy chain on S by Gaussian elimination over Fractions, compare with m/K.
 (b) exhaustive: every reveal sequence of length T (all 2^T outcomes, T=14), and for every
     initial window, R_T <= LCS(A_x,B_y) by a plain DP, and every F_p <= LCS(A_x,B_{l+p}).
 (c) exact mean of R_T over those outcomes vs T*g + bounded term: |E R_T - T*g/2... | printed."""
import sys, array
from fractions import Fraction as Fr
N=int(sys.argv[1]); P=1<<31
st=array.array('I'); st.frombytes(open(sys.argv[2],'rb').read())
val=array.array('i'); val.frombytes(open(sys.argv[3],'rb').read())
K=int(sys.argv[4]); m=int(sys.argv[5])
keys=[x&~P for x in st]; pol={x&~P:x>>31 for x in st}; ix={k:i for i,k in enumerate(keys)}; mask=(1<<N)-1
def rowf(h,b,a):
    o=0;v=0
    for p in range(N):
        hp=(h>>p)&1; mm=1 if ((b>>p)&1)==a else 0; x=hp|v|mm; o|=(x-v)<<p; v=x-hp
    return o
def succ(s):
    h=s&mask;b=s>>N;out=[]
    if pol[s]:
        for a in (0,1): out.append((0,rowf(h,b,a)|(b<<N)))
    else:
        for c in (0,1):
            nb=(b>>1)|(c<<(N-1))
            if nb>>(N-1): nb=~nb&mask
            out.append((h&1,(h>>1)|(nb<<N)))
    return out
# (a) gain: restrict to the terminal class reachable from the first state by forward closure of recurrent set via iteration
n=len(keys)
# exact solve of g + u(s) = mean(r + u(next)), u(keys[0]) = 0
A=[[Fr(0)]*(n+1) for _ in range(n)]
for i,s in enumerate(keys):
    # unknowns: g at col 0, u(j) for j>=1 at col j
    A[i][0]+=1
    if i>0: A[i][i]+=1
    rhs=Fr(0)
    for r,t in succ(s):
        rhs+=Fr(r,2); j=ix[t]
        if j>0: A[i][j]-=Fr(1,2)
    A[i][n]=rhs
# Gaussian elimination
for c in range(n):
    p=next(r for r in range(c,n) if A[r][c]!=0)
    A[c],A[p]=A[p],A[c]
    pv=A[c][c]; A[c]=[x/pv for x in A[c]]
    for r in range(n):
        if r!=c and A[r][c]!=0:
            f=A[r][c]; A[r]=[x-f*y for x,y in zip(A[r],A[c])]
g=A[0][n]
print(f'N={N} states={n} exact gain rho per char={g} = {float(g):.10f}; 2rho={float(2*g):.10f}; certified m/K={m/K:.10f}; ok={Fr(m,K)<=2*g}')
# (b) exhaustive
T=14 if len(sys.argv)<7 else int(sys.argv[6])
def lcs(A_,B_):
    prev=[0]*(len(B_)+1)
    for a in A_:
        cur=[0]*(len(B_)+1)
        for j,bc in enumerate(B_,1):
            cur[j]=max(prev[j],cur[j-1],prev[j-1]+(1 if bc==a else 0))
        prev=cur
    return prev
cnt=0;tot=Fr(0);bad=0
def rec(t,h,b,bl,A_,B_,R):
    global cnt,tot,bad
    # bl: window chars as int with bit p = char at position p (raw, not canonical); B_ all columns
    can=bl if not (bl>>(N-1)) else (~bl&mask)
    s=h|(can<<N)
    if s not in pol: raise SystemExit(f'state {s} not in S')
    tab=lcs(A_,B_); l=len(B_)-N
    F=R
    for p in range(N+1):
        if p>0: F+=(h>>(p-1))&1
        if F>tab[l+p]: bad+=1
    if t==T:
        cnt+=1; tot+=R
        global totV; totV+=val[ix[s]]-val[ix[s0_box[0]]]
        return
    if pol[s]:
        for a in (0,1): rec(t+1,rowf(h,bl,a),can,bl,A_+[a],B_,R)
    else:
        for c in (0,1): rec(t+1,h>>1,can,(bl>>1)|(c<<(N-1)),A_,B_+[c],R+(h&1))
totV=0; s0_box=[None]
tele_ok=True
for b0 in range(1<<N):
    B0=[(b0>>p)&1 for p in range(N)]
    can0=b0 if not (b0>>(N-1)) else (~b0&mask)
    s0_box[0]=can0<<N
    c0,t0,v0=cnt,tot,totV
    rec(0,0,0,b0,[],B0,0)
    # step 6, exact, per start state: mean over equally weighted leaves is not uniform across the tree only if depth differs; all leaves have depth T
    leaves=cnt-c0
    lhs=K*Fr(tot-t0,leaves)+Fr(v0 if False else totV-v0,leaves)
    if lhs<Fr(T*m,2): tele_ok=False; print('TELESCOPE FAIL',b0,float(lhs),T*m/2)
print('step 6 telescoping inequality K E R_T + E V(s_T) - V(s_0) >= T m/2, exact, all starts:',tele_ok)
print(f'exhaustive T={T}: paths={cnt}, violations of F_p<=LCS: {bad}; mean R_T={float(tot/cnt):.6f}, T*rho={float(T*g):.6f}')
sys.exit(1 if bad else 0)
