// SPDX-License-Identifier: AGPL-3.0-or-later
// Search irreducible zero-sum sets of 2k distinct odd integers with max |x| = 2n-1 exactly.
// Irreducible: no nonempty proper zero-sum subset  <=>  SS(A) ∩ SS(B) = {0, S}  (A = positives, B = |negatives|).
// DFS over magnitudes 2n-1, 2n-3, ..., 1: each goes to A, B, or is skipped. Largest (2n-1) forced into A (negation symmetry).
// Usage: irr n k   -> prints first set found (or NONE) and node count.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define W 24
typedef struct { uint64_t w[W]; } bs;
static int N2,K2; static long long nodes; static int sel[200], side[200], ns;
static inline void shor(bs*r,const bs*a,int s){ // r = a | (a<<s)
  int q=s>>6,b=s&63; for(int i=W-1;i>=0;i--){uint64_t v=0; if(i-q>=0){v=a->w[i-q]<<b; if(b&&i-q-1>=0) v|=a->w[i-q-1]>>(64-b);} r->w[i]=a->w[i]|v;}}
static inline int inter_only0(const bs*a,const bs*b){ uint64_t x=(a->w[0]&b->w[0])&~1ULL; if(x) return 0; for(int i=1;i<W;i++) if(a->w[i]&b->w[i]) return 0; return 1;}
static int dfs(int m, bs*SA, bs*SB, int sa, int sb, int placed){
  nodes++;
  int r=K2-placed;
  int D=sa-sb; if(D<0)D=-D;
  if(r==1){ // last element: magnitude D, odd, < m+2 (i.e. <= m), placed on smaller side
    if(D<1||D>m||!(D&1)) return 0;
    bs t; if(sa<sb){shor(&t,SA,D); // check intersection = {0,S}
      int S=sb; bs x; for(int i=0;i<W;i++) x.w[i]=t.w[i]&SB->w[i]; x.w[0]&=~1ULL; x.w[S>>6]&=~(1ULL<<(S&63)); for(int i=0;i<W;i++) if(x.w[i]) return 0;
      sel[ns]=D; side[ns]=0; ns++; return 1;}
    else {shor(&t,SB,D); int S=sa; bs x; for(int i=0;i<W;i++) x.w[i]=t.w[i]&SA->w[i]; x.w[0]&=~1ULL; x.w[S>>6]&=~(1ULL<<(S&63)); for(int i=0;i<W;i++) if(x.w[i]) return 0;
      sel[ns]=D; side[ns]=1; ns++; return 1;}
  }
  if(m<1) return 0;
  // remaining magnitudes available: m, m-2, ..., 1 : count (m+1)/2
  if((m+1)/2 < r) return 0;
  // max reduction of |D| using r elements: sum of r largest available
  int mx=0; for(int i=0;i<r;i++) mx+=m-2*i;
  if(D>mx) return 0;
  bs t;
  // put m in A
  shor(&t,SA,m); if(inter_only0(&t,SB)){ sel[ns]=m; side[ns]=0; ns++; if(dfs(m-2,&t,SB,sa+m,sb,placed+1)) return 1; ns--; }
  shor(&t,SB,m); if(inter_only0(SA,&t)){ sel[ns]=m; side[ns]=1; ns++; if(dfs(m-2,SA,&t,sa,sb+m,placed+1)) return 1; ns--; }
  return dfs(m-2,SA,SB,sa,sb,placed);
}
int main(int argc,char**argv){
  int n=atoi(argv[1]), k=atoi(argv[2]); N2=2*n-1; K2=2*k;
  bs SA,SB; memset(&SA,0,sizeof SA); memset(&SB,0,sizeof SB); SA.w[0]=1; SB.w[0]=1;
  bs t; shor(&t,&SA,N2); sel[0]=N2; side[0]=0; ns=1;
  int r=dfs(N2-2,&t,&SB,N2,0,1);
  printf("n=%d k=%d %s nodes=%lld",n,k,r?"FOUND":"NONE",nodes);
  if(r){printf(" set:"); for(int i=0;i<ns;i++) printf(" %d",side[i]?-sel[i]:sel[i]);}
  printf("\n"); return 0;
}
