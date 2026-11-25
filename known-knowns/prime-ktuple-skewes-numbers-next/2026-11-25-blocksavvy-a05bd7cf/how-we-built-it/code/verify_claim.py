"""Fast standalone check of claim/result (does NOT replace the full recount in REPRODUCE.md step 2).
Checks: (1) p and p+6 prime (flint BPSW, deterministic below 2^64, and sympy); (2) the block-count table sums to the
stated number of pairs before the crossing block; (3) an own numpy sieve of the crossing block, compared pair by pair
with C*Li2 in Arb (C from constant.py, certified ball): every pair before p in that block satisfies pi6 <= C*Li2,
p violates it, and pi6(p) equals the claim; (4) power-of-ten counts at 1e11 and 1e12 equal OEIS A080841 (saved copy).
usage: python3 verify_claim.py [result_dir]   -> last line PASS or FAIL"""
import sys, os, json, numpy as np, re
from flint import arb, fmpz, ctx
import sympy
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constant import c2ball
B=6*(1<<21)
_cache={}
def block_pairs(j, upto):
    key=(j,upto)
    if key in _cache: return _cache[key]
    a=j*B; hi=upto+7; r=int(hi**0.5)+2
    s=np.ones(r+1,bool); s[:2]=False
    for i in range(2,int(r**0.5)+1):
        if s[i]: s[i*i::i]=False
    seg=np.ones(hi-a,bool)
    for p in np.nonzero(s)[0].tolist():
        st=max(p*p,((a+p-1)//p)*p); seg[st-a::p]=False
    pr=np.nonzero(seg)[0]+a; st=pr[pr<=upto]; st=st[seg[st+6-a]]
    _cache[key]=st.tolist(); return _cache[key]
def verify(res, counts, a080841, quiet=False):
    def fail(m):
        if not quiet: print('FAIL:',m)
        return False
    ctx.prec=200
    p=int(res['skewes_number_inclusive']); N=int(res['pi6_at_p_inclusive']); N0=int(res['pairs_below_crossing_block_start_349012230144'])
    j=p//B
    if j!=int(res['crossing_block']): return fail('crossing block index')
    if not (fmpz(p).is_prime() and fmpz(p+6).is_prime() and sympy.isprime(p) and sympy.isprime(p+6)): return fail('p or p+6 not prime')
    if len(counts)<j or sum(counts[:j])!=N0: return fail('block-count table does not sum to the stated prefix')
    if j*B!=349012230144: return fail('prefix field refers to another block')
    C2,_=c2ball(); C=4*C2; two=arb(2); c2=two.li()-two/two.log()
    rank=N0; prs=block_pairs(j,p)
    if not prs or prs[-1]!=p: return fail('p is not a pair start')
    for q in prs:
        rank+=1; x=arb(q); v=C*((x.li()-x/x.log())-c2)-rank
        if q<p and not v>0: return fail(f'earlier violation (or undecided) at {q}')
        if q==p and not v<0: return fail('no violation at p')
    if rank!=N: return fail(f'pi6(p) is {rank}, claim says {N}')
    for e in (11,12):
        if int(res['power_of_ten_counts'][f'1e{e}'])!=a080841[e]: return fail(f'count at 1e{e} differs from OEIS A080841')
    if not quiet: print(f'p={p} p+6={p+6} prime; pi6(p)={N}; table prefix {N0}; {len(prs)} pairs of block {j} up to p compared; A080841 match')
    return True
def load(rd):
    res=json.load(open(os.path.join(rd,'skewes.json')))
    counts=[int(l.split()[1]) for l in open(os.path.join(rd,'block_counts_0_to_27737.txt')) if not l.startswith('#')]
    t=open(os.path.join(rd,'..','data','oeis_A080841.txt')).read()
    terms=[int(x) for x in ''.join(re.findall(r'%[STU] A080841 (\S+)',t)).split(',') if x]
    a=dict(enumerate(terms,1))
    return res,counts,a
if __name__=='__main__':
    rd=sys.argv[1] if len(sys.argv)>1 else os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','result')
    ok=verify(*load(rd)); print('PASS' if ok else 'FAIL')
