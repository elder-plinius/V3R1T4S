/* Program B (A155520): forward chain DP.  Ordered tree with m edges = Dyck word of length 2m, stored as
   bits (U=1).  Every way to add a leaf = insert "UD" at one of the 2m+1 positions.  cnt[m+1][w'] +=
   cnt[m][w] once for each DISTINCT w' reachable from w (per-w dedup), so cnt[n][T] = number of
   distinct tree chains * -> ... -> T = drawings.  Row n = histogram over all words of length 2n
   (zeros inside the row printed).  usage: ./progB NMAX  (NMAX <= 12) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
int main(int argc,char**argv){ int N=atoi(argv[1]);
  u64 *cur=calloc(1,sizeof(u64)); cur[0]=1; /* m = 0: empty word */
  for(int m=0;m<N;m++){ int len=2*m, nl=len+2; u64 *nx=calloc((size_t)1<<nl,sizeof(u64));
    for(u64 w=0; w<((u64)1<<len); w++){ if(!cur[w]) continue;
      u64 seen[64]; int ns=0;
      for(int i=0;i<=len;i++){ /* insert bits "10" (U then D) at position i counted from the most significant end */
        int lowbits=len-i; u64 hi=w>>lowbits, lo=w&(((u64)1<<lowbits)-1);
        u64 v=(((hi<<2)|2ULL)<<lowbits)|lo;
        int dup=0; for(int j=0;j<ns;j++) if(seen[j]==v){dup=1;break;}
        if(!dup){ seen[ns++]=v; nx[v]+=cur[w]; } } }
    free(cur); cur=nx; int n=m+1;
    u64 mx=0,trees=0,ws=0; for(u64 w=0;w<((u64)1<<nl);w++) if(cur[w]){trees++; ws+=cur[w]; if(cur[w]>mx)mx=cur[w];}
    u64 *h=calloc(mx+1,sizeof(u64)); for(u64 w=0;w<((u64)1<<nl);w++) if(cur[w]) h[cur[w]]++;
    printf("%d sum=%llu wsum=%llu row: ",n,trees,ws); for(u64 k=1;k<=mx;k++) printf(k<mx?"%llu,":"%llu",h[k]); printf("\n"); fflush(stdout); free(h); }
  return 0; }
