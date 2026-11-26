#!/usr/bin/env python3
"""Driver for the C engine: run cubic per prime, CRT -> exact U(N), inverse Euler ->
connected, validate against b-files. Glue only (analysis), not the heavy compute."""
import sys, os, subprocess, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import engine as E
from math import factorial

def is_prime(n):
    if n < 2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n % p == 0: return n == p
    d=n-1; r=0
    while d%2==0: d//=2; r+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(r-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True

def primes_near(base, k):
    out=[]; n=base|1
    while len(out)<k:
        if is_prime(n): out.append(n)
        n-=2
    return out

def crt(residues, mods):
    from functools import reduce
    M=reduce(lambda a,b:a*b, mods)
    x=0
    for r,m in zip(residues,mods):
        Mi=M//m; x += r*Mi*pow(Mi,-1,m)
    return x % M

def run_c(binpath, deg, nmax, prime, pivot):
    out=subprocess.run([binpath,'--deg',str(deg),'--nmax',str(nmax),'--prime',str(prime),'--pivot',pivot],
                       capture_output=True,text=True)
    S={}
    for line in out.stdout.strip().splitlines():
        parts=line.split()
        if len(parts)!=2: continue
        try: n,s=int(parts[0]),int(parts[1])
        except ValueError: continue
        S[n]=s
    if out.returncode!=0:
        # OOM / crash under the memory cap: each N is printed (with fflush) only after it
        # fully completes, so every flushed line is a complete, correct value. Keep them and
        # stop at the last complete N instead of discarding the whole run.
        sys.stderr.write("C partial rc=%d prime=%d reached N=%d: %s\n"%(
            out.returncode, prime, (max(S) if S else -1), out.stderr[-200:]))
    return S

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--bin',default='./cubic')
    ap.add_argument('--deg',type=int,default=3)
    ap.add_argument('--nmax',type=int,default=40)
    ap.add_argument('--pivot',default='max')
    ap.add_argument('--nprimes',type=int,default=4)
    ap.add_argument('--checkbfile',default='')
    ap.add_argument('--checkall',default='')
    ap.add_argument('--dumpU',action='store_true')
    args=ap.parse_args()
    primes=primes_near(4611686018427387849, args.nprimes)
    Smaps=[run_c(args.bin,args.deg,args.nmax,p,args.pivot) for p in primes]
    common=set(Smaps[0].keys())
    for sm in Smaps[1:]: common &= set(sm.keys())
    Ns=sorted(common)
    reached=max(Ns) if Ns else 0
    U={}
    for N in Ns:
        Nf=factorial(N)
        resid=[(Smaps[i][N]*pow(Nf,-1,primes[i]))%primes[i] for i in range(len(primes))]
        U[N]=crt(resid,primes)
    C=E.connected_from_U(U, reached)
    sys.stderr.write("reached N=%d (requested nmax=%d)\n"%(reached, args.nmax))
    if args.dumpU:
        for N in Ns:
            if U[N]: print("%d %d %d"%(N,U[N],C.get(N,0)))
    def loadb(p):
        d={}
        for l in open(p):
            l=l.strip()
            if not l or l.startswith('#'): continue
            a,b=l.split(); d[int(a)]=int(b)
        return d
    idx2N = (lambda idx: 2*idx) if args.deg==3 else (lambda idx: idx)
    mm=0; checked=0
    if args.checkbfile:
        for idx,v in loadb(args.checkbfile).items():
            N=idx2N(idx)
            if N in C and v!=0:
                checked+=1
                if C[N]!=v: print("MISMATCH connected idx=%d N=%d bfile=%d ours=%d"%(idx,N,v,C[N])); mm+=1
    if args.checkall:
        for idx,v in loadb(args.checkall).items():
            N=idx2N(idx)
            if N in U and v!=0:
                checked+=1
                if U[N]!=v: print("MISMATCH all idx=%d N=%d bfile=%d ours=%d"%(idx,N,v,U[N])); mm+=1
    print("primes:%d nmax:%d pivot:%s checked:%d mismatches:%d"%(len(primes),args.nmax,args.pivot,checked,mm))
    print("PASS" if (mm==0 and checked>0) else "FAIL")

if __name__=='__main__':
    main()
