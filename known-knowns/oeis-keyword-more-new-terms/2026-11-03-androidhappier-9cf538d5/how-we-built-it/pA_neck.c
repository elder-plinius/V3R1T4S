/* A325786 Program A: enumerate compositions of n recursively as part lists; keep those that are
   lexicographically minimal among all cyclic rotations (neckQ, non-strict: ties allowed); complete iff
   every 1..n is the sum of some circular contiguous block (lengths 1..k starting at each position). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n, q[64]; static long long cnt;
static int neck(int k){ for(int r=1;r<k;r++){ for(int i=0;i<k;i++){ int a=q[i], b=q[(i+r)%k]; if(a<b) break; if(a>b) return 0; } } return 1; }
static int complete(int k){ static char seen[128]; memset(seen,0,n+1); int got=0;
  for(int s=0;s<k;s++){ int t=0; for(int L=1;L<=k;L++){ t+=q[(s+L-1)%k]; if(!seen[t]){seen[t]=1;got++;} } }
  return got==n; }
static void rec(int k,int rem){ if(rem==0){ if(neck(k)&&complete(k)) cnt++; return; }
  for(int p=1;p<=rem;p++){ q[k]=p; if(k>0 && p<q[0]) continue; /* rotation starting at this part would be smaller */ rec(k+1,rem-p);} }
int main(int c,char**v){ int lo=atoi(v[1]),hi=atoi(v[2]); for(n=lo;n<=hi;n++){ cnt=0; if(n>0){ for(int p=1;p<=n;p++){q[0]=p;rec(1,n-p);} } printf("%d %lld\n",n,cnt); fflush(stdout);} }
