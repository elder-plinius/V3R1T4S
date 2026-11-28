/* Program B (A131449): per ordered tree (Dyck word, bit-encoded), count increasing labelings by a DP
   over removal orders: f(S) = number of ways to remove the vertex set S leaf-by-leaf (a vertex may be
   removed only when all its children are removed); labelings = orders = f(all).  No hook formula.
   Row = values sorted non-increasing.  Prints "index value" (offset 0); stderr: row length and sum.
   usage: ./progB NMAX (NMAX <= 8) */
#include <stdio.h>
#include <stdlib.h>
typedef unsigned long long u64;
static int cmpd(const void*a,const void*b){u64 x=*(const u64*)a,y=*(const u64*)b;return (x<y)-(x>y);}
int main(int argc,char**argv){ int N=atoi(argv[1]); long idx=0;
  for(int n=0;n<=N;n++){ u64 *vals=malloc(sizeof(u64)*5000); int nv=0;
    for(u64 w=0; w<((u64)1<<(2*n)); w++){ /* bit 2n-1-i = char i, 1 = U */
      int bal=0,ok=1; for(int i=0;i<2*n;i++){ bal+= ((w>>(2*n-1-i))&1)?1:-1; if(bal<0){ok=0;break;} } if(!ok||bal) continue;
      int par[16],st[16],sp=0,cnt=0; unsigned childmask[16]={0};
      for(int i=0;i<2*n;i++){ if((w>>(2*n-1-i))&1){ int v=cnt++; par[v]= sp? st[sp-1] : -1; if(sp) childmask[st[sp-1]]|=1u<<v; st[sp++]=v; } else sp--; }
      u64 *f=calloc((size_t)1<<n,sizeof(u64)); f[0]=1;
      for(unsigned S=0;S<(1u<<n);S++){ if(!f[S]) continue;
        for(int v=0;v<n;v++) if(!(S>>v&1) && (childmask[v]&~S)==0) f[S|1u<<v]+=f[S]; }
      vals[nv++]= n? f[(1u<<n)-1] : 1; free(f); }
    qsort(vals,nv,sizeof(u64),cmpd); u64 s=0;
    for(int i=0;i<nv;i++){ printf("%ld %llu\n",idx++,vals[i]); s+=vals[i]; }
    fprintf(stderr,"row %d len %d sum %llu\n",n,nv,s); free(vals); }
  return 0; }
