# REPRODUCE skeptic: K_8^(2) not harmonious

context: subagent (reproduce)

Worked on a private copy of claim/; nothing was written into claim/. `sha256sum -c SHA256SUMS.txt` passes for all 16 listed files (copy and original).

## Definition used (quoted from CLAIM / Graham-Sloane)
"a harmonious labeling of a graph with q edges assigns distinct residues mod q to the vertices so that the q edge sums (u+v mod q) are pairwise distinct. K_n^(2) is two copies of K_n sharing one vertex (2n-1 vertices, n(n-1) edges)." For n = 8: 15 vertices, q = 56.

## Independent search, written BEFORE reading the author's code (I read only CLAIM.md and result/ first)
Symmetry used: translation only. If f is harmonious, g = f + t is injective (translation is a bijection of Z_q) and every edge sum moves by 2t, so distinct sums stay distinct; g -> g - t undoes it. So WLOG f(center) = 0. I used no unit multiplier and no A/B swap. Labels inside a clique are enumerated as increasing sets; this is not a symmetry reduction, because the edge sums depend only on the label set of each clique.
After the reduction: S_A = {0} ∪ f(A) and S_B = {0} ∪ f(B) are 8-subsets of Z_56 that contain 0. Each has 28 distinct pair sums, S_A ∩ S_B = {0}, and the two sum sets are disjoint. Since 28 + 28 = 56, the two sum sets partition Z_56.

Method R1 (C, `rsearch.c`, inlined below): backtracking enumerates every such set with 64-bit sum and element masks (q ≤ 64). It sorts by sum mask, binary-searches for the exact complement mask, then requires the element masks to share only bit 0.
Method R2 (Python, `rsearch2.py`, inlined below): recursive enumeration, a dict keyed by frozenset of sums, a complement lookup and the same intersection test.
Brute force B4 (`brute4.py`, inlined below): every injective labeling of K_4^(2) (12P7 = 3,991,680), no reduction at all.

| n | q | sets (R1 = R2) | distinct sum sets | ordered pairs R1 / R2 | expected |
|---|---|---|---|---|---|
| 4 | 12 | 120 | 91 | 48 / 48 | harmonious |
| 5 | 20 | 1460 | 1252 | 0 / 0 | not (n odd, Graham-Sloane) |
| 6 | 30 | 13608 | 12344 | 0 / 0 | not (Graham-Sloane) |
| 7 | 42 | 90888 | 81948 | 0 / 0 | not (n odd) |
| 8 | 56 | 449472 | 407352 | 0 / 0 | the claim |

- B4 finds 20736 harmonious labelings of K_4^(2) = 12 translations × 48 ordered pairs × 3!·3! orderings. This matches R1/R2 exactly and confirms that the translation reduction loses nothing. Example labeling: center 0, A = {1, 2, 8}, B = {5, 7, 11}.
- The 48 n = 4 ordered pairs from R1 match result/n4_solutions_P1.txt and result/n4_solutions_P2.txt exactly after sorting (diff is empty).
- Determinism: R1 n = 8 was run twice with identical output (~0.47 s each). R2 n = 8 took ~27 s. R1 and R2 agree.
- Exhaustiveness: the pruning rejects a partial set only when a pair sum repeats. That is a monotone condition, so no full candidate is lost. The join tests every set against every set whose sum mask is the exact complement. Nothing is sampled.

## Comparison with the claim's programs and outputs (after my search)
- Read checkers/wsearch.c, checkers/mitm.py, checkers/check_label.py and REPRODUCE.md. They use the same definition and the same translation-only reduction, justified correctly in REPRODUCE.md. wsearch.c (nested A-then-B backtracking, 128-bit masks) and mitm.py (breadth-first + mask dict join) are genuinely different algorithms.
- Recompiled and re-ran: `gcc -O2 checkers/wsearch.c`; `./wsearch 8` gives sets=449472, solutions_ordered_pairs=0, nodesB=270416160, in 40.1 s. `python3 checkers/mitm.py 8` gives 449472 sets, distinct_masks=407352, 0 pairs, in 11.2 s. Both are byte-identical in content to result/P1_wsearch_n8.txt and result/P2_mitm_n8.txt (timings aside).
- n = 3..7 for wsearch and mitm: only n = 4 is HARMONIOUS (48 pairs); 3, 5, 6 and 7 have 0. Set counts match mine.
- `python3 checkers/brute_n4.py` gives 20736 expected 20736. `check_label.py 4 "0 2 6 11" "3 7 9"` gives VALID.
- Extras (P3 wjoin, mod14, mod_multiset) were not re-run. They are not needed for the criterion's "two independent programs", and the claimed decision does not depend on them.

## Mismatches / missing objects / non-determinism
None found. Every count (449472 sets, 407352 distinct masks, 0 ordered pairs at n = 8; 48 pairs and 20736 labelings at n = 4; 0 at n = 6) matches across four implementations: my R1 and R2, and the author's P1 and P2.
Scope: this checks the computation only. The literature/status check (DS6 and whether a published decision exists) is not part of the reproduce role and I did not verify it.

## My code (inlined, sha256 of each file before inlining)

### rsearch.c (5f9473408e8761eaa7ff09403057f1ce6cfa46d630ff0124ef6ead29057da76d)
```
/* Independent exhaustive search (reproduce skeptic).
 Definition: harmonious labeling of graph with q edges = injective f:V->Z_q with the q edge sums f(u)+f(v) mod q pairwise distinct.
 K_n^(2): center c, cliques {c}uA, {c}uB, |A|=|B|=n-1, q=n(n-1).
 Symmetry used: translation f->f+t (sums shift by 2t, injectivity kept) => WLOG f(c)=0. Nothing else.
 Then S_A={0}uf(A), S_B={0}uf(B) are n-subsets of Z_q containing 0, each with C(n,2)=q/2 distinct pair sums,
 S_A n S_B={0}, and sumset(S_A) disjoint from sumset(S_B). Count ordered pairs (S_A,S_B). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef struct { uint64_t sm, em; } rec;
static int n,q; static rec *R; static long nr=0,cap=0; static int el[16];
static void rec_(int k,int start,uint64_t sm,uint64_t em){
  if(k==n){ if(nr==cap){cap=cap?cap*2:1024;R=realloc(R,cap*sizeof(rec));} R[nr].sm=sm;R[nr].em=em;nr++; return; }
  for(int x=start;x<q;x++){
    uint64_t add=0; int ok=1;
    for(int i=0;i<k;i++){ int s=(el[i]+x)%q; uint64_t b=1ULL<<s; if((sm|add)&b){ok=0;break;} add|=b; }
    if(!ok) continue; el[k]=x; rec_(k+1,x+1,sm|add,em|(1ULL<<x));
  }
}
static int cmp(const void*a,const void*b){uint64_t x=((rec*)a)->sm,y=((rec*)b)->sm;return x<y?-1:x>y;}
int main(int argc,char**argv){
  n=atoi(argv[1]); q=n*(n-1); el[0]=0; rec_(1,1,0,1ULL);
  qsort(R,nr,sizeof(rec),cmp);
  uint64_t full=(q==64)?~0ULL:((1ULL<<q)-1);
  long pairs=0, distinct=0;
  for(long i=0;i<nr;i++) if(i==0||R[i].sm!=R[i-1].sm) distinct++;
  for(long i=0;i<nr;i++){
    uint64_t want=full&~R[i].sm;
    long lo=0,hi=nr; while(lo<hi){long m=(lo+hi)/2; if(R[m].sm<want) lo=m+1; else hi=m;}
    for(long j=lo;j<nr&&R[j].sm==want;j++) if((R[i].em&R[j].em)==1ULL){ pairs++;
      if(argc>2){ for(int x=0;x<q;x++) if(R[i].em>>x&1) printf("%d ",x); printf("| "); for(int x=0;x<q;x++) if(R[j].em>>x&1) printf("%d ",x); printf("\n"); } }
  }
  printf("n=%d q=%d sets=%ld distinct_masks=%ld ordered_pairs=%ld\n",n,q,nr,distinct,pairs);
  return 0;
}
```

### rsearch2.py (94eb1481868890b6f1ffaa2e8e652a1a1658dd0f1c408a6f2e7762883e703adf)
```
# Second independent method (python): enumerate sum-distinct n-sets containing 0, index by frozenset of sums,
# for each set look up the complementary sum-set exactly; require label sets meet only in 0.
import sys
n=int(sys.argv[1]);q=n*(n-1)
sets=[]
def go(el,sums,start):
    if len(el)==n: sets.append((tuple(el),frozenset(sums))); return
    for x in range(start,q):
        new=[(e+x)%q for e in el]
        if len(set(new))<len(new) or any(s in sums for s in new): continue
        go(el+[x],sums|set(new),x+1)
go([0],set(),1)
idx={}
for el,s in sets: idx.setdefault(s,[]).append(el)
full=frozenset(range(q));pairs=0
for el,s in sets:
    for el2 in idx.get(full-s,[]):
        if set(el)&set(el2)=={0}: pairs+=1
print(f"n={n} q={q} sets={len(sets)} distinct_sumsets={len(idx)} ordered_pairs={pairs}")
```

### brute4.py (95becbbcafbcff777bd3a11ebbe1dce5a574008f0fbe223f8e32c954739ed408)
```
# Unreduced brute force over all injective labelings of K_4^(2) (7 vertices, q=12), definition only.
import itertools
n=4;q=12;V=list(range(2*n-1))  # 0 = center, 1..3 = A, 4..6 = B
E=[(u,v) for C in ([0,1,2,3],[0,4,5,6]) for u,v in itertools.combinations(C,2)]
assert len(E)==q
cnt=0;ex=None
for f in itertools.permutations(range(q),len(V)):
    s={(f[u]+f[v])%q for u,v in E}
    if len(s)==q:
        cnt+=1; ex=ex or f
print("n=4 harmonious labelings (no reduction):",cnt,"example",ex,"expected 12*48*3!*3! =",12*48*36)
```

pass: true
