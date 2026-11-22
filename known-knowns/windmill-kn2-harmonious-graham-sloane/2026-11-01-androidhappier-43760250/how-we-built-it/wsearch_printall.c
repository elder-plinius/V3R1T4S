/* wsearch.c - exhaustive search for harmonious labelings of the windmill K_n^(2).
   Definition (Graham-Sloane 1980): a graph with q edges is harmonious if its vertices get DISTINCT labels in Z_q
   such that the q edge sums f(u)+f(v) mod q are pairwise distinct.  K_n^(2): two copies of K_n sharing one vertex c;
   2n-1 vertices, q = n(n-1).
   Reduction (translation, PROVED in NOTES): f -> f - f(c) keeps labels distinct and shifts every edge sum by -2f(c),
   a bijection of Z_q, so WLOG f(c) = 0.  No other symmetry is used: A' = labels of clique-1 non-shared vertices,
   B' = clique-2, enumerated as increasing tuples (that only removes the 7!·7! orderings inside each clique, which do
   not change the multiset of labels or sums).  Both orders (A,B) and (B,A) are enumerated, so every solution is
   counted exactly twice.
   Output: number of sum-distinct n-sets {0} u A' (all C(n,2) pair sums distinct mod q), number of solutions. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128;
static int n, q;
static int A[32], B[32];
static long long nA = 0, nSol = 0, nodesB = 0;
static u128 one = 1;
static u128 SA;          /* sums used by clique A */
static void printsol(void){
  printf("SOLUTION A={0"); for(int i=0;i<n-1;i++) printf(",%d",A[i]);
  printf("} B={0"); for(int i=0;i<n-1;i++) printf(",%d",B[i]); printf("}\n"); fflush(stdout);
}
/* clique B: k elements placed, used = SA | sums of B so far, usedV = labels used */
static void recB(int k, int lo, u128 used, u128 usedV){
  nodesB++;
  if(k==n-1){ nSol++; printsol(); return; }
  for(int x=lo;x<q;x++){
    if(usedV>>x & 1) continue;
    u128 add = 0; int ok=1;
    /* sums x+0 and x+B[i] */
    int s = x % q; if((used>>s)&1) continue; add |= one<<s;
    for(int i=0;i<k;i++){ s=(x+B[i])%q; if(((used|add)>>s)&1){ok=0;break;} add|=one<<s; }
    if(!ok) continue;
    B[k]=x; recB(k+1,x+1,used|add,usedV|(one<<x));
  }
}
static void recA(int k, int lo, u128 used){
  if(k==n-1){
    nA++; SA=used;
    u128 usedV = one<<0; for(int i=0;i<n-1;i++) usedV|=one<<A[i];
    recB(0,1,used,usedV);
    return;
  }
  for(int x=lo;x<q;x++){
    u128 add=0; int ok=1;
    int s=x%q; if((used>>s)&1) continue; add|=one<<s;
    for(int i=0;i<k;i++){ s=(x+A[i])%q; if(((used|add)>>s)&1){ok=0;break;} add|=one<<s; }
    if(!ok) continue;
    A[k]=x; recA(k+1,x+1,used|add);
  }
}
int main(int argc,char**argv){
  n=atoi(argv[1]); q=n*(n-1);
  if(q>128){fprintf(stderr,"q too big\n");return 1;}
  recA(0,1,0);
  printf("n=%d q=%d sum_distinct_sets_containing_0=%lld solutions_ordered_pairs=%lld nodesB=%lld\n",n,q,nA,nSol,nodesB);
  printf("VERDICT n=%d: %s\n",n,nSol? "HARMONIOUS":"NOT HARMONIOUS");
  return 0;
}
