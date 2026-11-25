#!/usr/bin/env python3
"""Standalone check (Python standard library only) of the sexy-prime Skewes number object.
Definition (Toth 2019; OEIS A210439 wording): the first prime p with pi_6(p) > C*Li_2(p), where
pi_6(x) = #{prime q <= x : q+6 prime} (pairs need not be consecutive primes), C = 4*C_2 (C_2 = twin prime constant,
OEIS A005597), Li_2(x) = int_2^x dt/log(t)^2.
What this checker does (about 10-30 s):
 1. p and p+6 are prime (deterministic Miller-Rabin, bases valid below 3.3e24).
 2. object/block_counts_0_to_27737.txt sums, over blocks before p's block, to the stated prefix, and its first 8 blocks
    (n < 100663296) equal a recount by a small sieve here (885041 pairs).
 3. Own segmented sieve of p's block [a, p+6]: pair starts in [a, p] counted and ranked from the prefix.
 4. Li_2 in decimal arithmetic (45 digits, Ramanujan series for li) at a; then for every pair q in the block, enclosures
    Li_2(q) in [Li_2(a) + sum (v-u)/log(v)^2, Li_2(a) + sum (v-u)/log(u)^2] over consecutive pairs (the integrand decreases).
    Every q < p must satisfy pi_6(q) < C*lower, and p must satisfy pi_6(p) > C*upper.
 It does NOT redo the exhaustive count below a (that is RUN_IT_YOURSELF.md step 2, C code, ~5-10 min).
Last line: PASS or FAIL."""
import json, math, os, sys
from decimal import Decimal as D, getcontext
getcontext().prec=45
HERE=os.path.dirname(os.path.abspath(__file__)); PKG=os.path.dirname(HERE)
B=6*(1<<21)
C2=D('0.66016181584686957392781211001455577843262336028')   # OEIS A005597; certified ball in how-we-built-it/code/constant.py
C=4*C2
GAMMA=D('0.577215664901532860606512090082402431042159336')
def is_prime(n):
    if n<2: return False
    for p in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        if n%p==0: return n==p
    d=n-1; s=0
    while d%2==0: d//=2; s+=1
    for a in (2,3,5,7,11,13,17,19,23,29,31,37,41):
        x=pow(a,d,n)
        if x in (1,n-1): continue
        for _ in range(s-1):
            x=x*x%n
            if x==n-1: break
        else: return False
    return True
def li(x):
    x=D(x); u=x.ln(); tot=D(0); term=D(1); inner=D(0); n=1; fact=D(1)
    while True:
        fact*=n
        if (n-1)%2==0: inner+=D(1)/(2*((n-1)//2)+1)
        t=(-1)**(n-1)*u**n/(fact*D(2)**(n-1))*inner
        tot+=t
        if n>10 and abs(t)<D(10)**-40: break
        n+=1
    return GAMMA+u.ln()+x.sqrt()*tot
def Li2(x):
    x=D(x); return li(x)-x/x.ln()-(li(2)-D(2)/D(2).ln())
def sieve_small(n):
    s=bytearray([1])*(n+1); s[0]=s[1]=0
    for i in range(2,int(n**0.5)+1):
        if s[i]: s[i*i::i]=bytearray(len(range(i*i,n+1,i)))
    return s
def main():
    obj=json.load(open(os.path.join(PKG,'object','sexy_skewes.json')))
    counts=[int(l.split()[1]) for l in open(os.path.join(PKG,'object','block_counts_0_to_27737.txt')) if l.strip() and not l.startswith('#')]
    p=int(obj['skewes_number_inclusive']); N=int(obj['pi6_at_p_inclusive']); N0=int(obj['pairs_below_crossing_block_start_349012230144'])
    j=p//B; a=j*B
    assert j==int(obj['crossing_block']) and a==349012230144, 'block index'
    assert is_prime(p) and is_prime(p+6), 'p or p+6 not prime'
    rows=[l.split() for l in open(os.path.join(PKG,'object','block_counts_0_to_27737.txt')) if l.strip() and not l.startswith('#')]
    assert [int(r[0]) for r in rows]==list(range(27738)) and all(len(r)==2 for r in rows), 'block table index column'
    assert len(counts)==27738 and sum(counts[:j])==N0, 'block table prefix'
    assert sum(counts)==1416032531 and int(obj['block_length'])==B and int(obj['p_plus_6'])==p+6, 'table total / fields'
    # published A080841 values (q+6 < 10^n; equal to our p <= 10^n counts at these n)
    assert obj['power_of_ten_counts']=={'1e8':879908,'1e9':6849047,'1e10':54818296,'1e11':448725003,'1e12':3741217498}, 'power-of-ten counts vs OEIS A080841'
    # small exact range: blocks 0..7
    s=sieve_small(8*B+6); big=int.from_bytes(bytes(s[:8*B]),'little'); big6=int.from_bytes(bytes(s[6:8*B+6]),'little')
    small=bin(big&big6).count('1')
    s8=bytes(s[:10**8+1]); i8=int.from_bytes(s8,'little')&int.from_bytes(bytes(s[6:10**8+7]),'little')
    assert bin(i8).count('1')==879908, 'pi6(1e8)'
    assert small==sum(counts[:8]), 'blocks 0..7 recount'
    # crossing block sieve
    hi=a+B+7; r=int(math.isqrt(hi))+1; base=sieve_small(r)
    seg=bytearray([1])*(hi-a)
    for q in range(2,r+1):
        if base[q]:
            st=max(q*q,((a+q-1)//q)*q)
            if st<hi: seg[st-a::q]=bytearray(len(range(st-a,hi-a,q)))
    allp=[a+i for i in range(0,B) if seg[i] and seg[i+6]]
    assert len(allp)==counts[j], 'crossing block count'
    pairs=[q for q in allp if q<=p]
    assert pairs and pairs[-1]==p, 'p is not a pair start'
    L0=Li2(a); lo=D(0); up=D(0); prev=a; rank=N0; minmargin=None; minq=None
    for q in pairs:
        w=q-prev
        if w:
            lo+=D(w)/D(q).ln()**2; up+=D(w)/D(prev).ln()**2
        prev=q; rank+=1
        if q<p:
            m=C*(L0+lo)-rank
            if not m>0: raise AssertionError(f'earlier violation or undecided at {q}')
            if minmargin is None or m<minmargin: minmargin,minq,minr=m,q,rank
        else:
            v=rank-C*(L0+up)
            if not v>0: raise AssertionError('no violation at p')
    assert rank==N, f'pi6(p)={rank}, object says {N}'
    Lp=C*Li2(p)
    assert abs(Lp-D(obj['C_times_Li2_at_p'].split()[0]))<D('1e-9') and abs((Lp-N)-D(obj['difference']))<D('1e-9'), 'stated C*Li2(p)'
    assert str(C).startswith(obj['C'].split('=')[1].strip()[:30]), 'stated C'
    mm=obj['min_margin_before_p']
    assert int(mm['at_q'])==minq and int(mm['pi6'])==minr and abs(minmargin-D(mm['value']))<D('1e-5'), 'stated min margin'
    # exclusive convention: first q with (#pairs < q) > C*Li2(q)
    rk=N0; exc=None
    for q in allp:
        if exc is None and rk>C*Li2(q): exc=q
        rk+=1
        if exc: break
    assert exc==int(obj['exclusive_convention_first_violation']), f'exclusive value {exc}'
    print(f'p={p} and p+6 prime; blocks 0..7 recount {small}; prefix {N0}; {len(pairs)} pairs in block {j} up to p;')
    print(f'min margin before p (lower bound) {float(minmargin):.6f}; pi6(p)={rank} exceeds C*Li2(p) upper enclosure by {float(v):.6f}')
    print('note: exhaustive count below the crossing block is RUN_IT_YOURSELF.md step 2 (not done here)')
if __name__=='__main__':
    try: main(); print('PASS')
    except Exception as e: print('error:',e); print('FAIL'); sys.exit(1)
