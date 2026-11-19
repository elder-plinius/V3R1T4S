#!/usr/bin/env python3
"""Program C: brute force from the definition.
is_asm(M): every row and column has prefix sums in {0,1} and total 1 (entries in {-1,0,1}).
is_tsasm(M): is_asm and M equals its image under all 8 elements of D4.
count_brute(N): enumerate N x N matrices row by row from all ASM-valid rows (pruned only by the
diagonal-symmetry requirement a[i][j]==a[j][i] for j<i and by column prefix sums in {0,1}), then test every complete
matrix with is_tsasm. Rows are restricted to palindromes (vertical-axis invariance), which every D4-invariant
matrix satisfies; the final test re-checks all 8 symmetries anyway."""
import sys, itertools
def is_asm(M):
    N=len(M)
    for L in list(M)+[ [M[i][j] for i in range(N)] for j in range(N)]:
        if len(L)!=N: return False
        s=0
        for x in L:
            if x not in (-1,0,1): return False
            s+=x
            if s not in (0,1): return False
        if s!=1: return False
    return True
def d4(M):
    N=len(M); T=lambda A:[list(r) for r in zip(*A)]
    R=lambda A:[list(r) for r in zip(*A[::-1])]  # rotate 90
    out=[]; A=[list(r) for r in M]
    for k in range(4):
        out.append(A); out.append(T(A)); A=R(A)
    return out
def is_tsasm(M):
    return is_asm(M) and all(X==[list(r) for r in M] for X in d4(M))
def asm_rows(N):
    rows=[]
    def rec(pre,s):
        if len(pre)==N:
            if s==1: rows.append(tuple(pre))
            return
        for x in (-1,0,1):
            if s+x in (0,1): rec(pre+[x],s+x)
    rec([],0); return rows
def count_brute(N):
    rows=[r for r in asm_rows(N) if r==r[::-1]]
    cnt=0; M=[]
    def rec(i,col):
        nonlocal cnt
        if i==N:
            if is_tsasm(M): cnt+=1
            return
        for r in rows:
            if any(r[j]!=M[j][i] for j in range(i)): continue
            nc=[col[j]+r[j] for j in range(N)]
            if any(c not in (0,1) for c in nc): continue
            M.append(r); rec(i+1,nc); M.pop()
    rec(0,[0]*N); return cnt
if __name__=="__main__":
    # fixtures
    pos=[[0,0,1,0,0],[0,1,-1,1,0],[1,-1,1,-1,1],[0,1,-1,1,0],[0,0,1,0,0]]
    neg1=[[1,0,0],[0,1,0],[0,0,1]]           # ASM, not D4-invariant
    neg2=[[0,1,0],[1,1,1],[0,1,0]]           # D4-invariant, not ASM
    print("fixture pos (order-5 TSASM):", is_tsasm(pos))
    print("fixture neg1 (identity 3, ASM not TSASM):", is_asm(neg1), is_tsasm(neg1))
    print("fixture neg2 (symmetric non-ASM):", is_tsasm(neg2))
    nmax=int(sys.argv[1]) if len(sys.argv)>1 else 7
    for n in range(nmax+1):
        print(f"a({n}) order {2*n+1}: {count_brute(2*n+1)}", flush=True)
