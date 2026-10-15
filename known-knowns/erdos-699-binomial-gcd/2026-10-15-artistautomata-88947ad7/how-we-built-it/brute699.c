/* Independent brute force for Erdos #699, n in [4,N]: for every k compute the set of primes p with v_p(C(n,k)) > 0
   by Legendre's formula (no Kummer/Lucas shortcut), then test every pair i<j<=n/2 for a common prime p >= i
   (or p > i with STRICT). Prints every failing triple. Usage: brute699 N STRICT */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
static int vf(int m,int p){int v=0; while(m){m/=p; v+=m;} return v;}
int main(int c,char**v){ int N=atoi(v[1]), strict=atoi(v[2]); int *pr=malloc(4*N), np=0; char*s=calloc(N+1,1);
  for(int i=2;i<=N;i++) if(!s[i]){ pr[np++]=i; for(long q=(long)i*i;q<=N;q+=i) s[q]=1; }
  int W=(np+63)/64; uint64_t *bs=malloc(8*(size_t)W*(N/2+1)); long fails=0;
  for(int n=4;n<=N;n++){ int h=n/2; memset(bs,0,8*(size_t)W*(h+1));
    for(int k=1;k<=h;k++) for(int t=0;t<np && pr[t]<=n;t++){ int p=pr[t]; if(vf(n,p)-vf(k,p)-vf(n-k,p)>0) bs[(size_t)k*W+t/64]|=1ULL<<(t%64); }
    for(int i=1;i<h;i++){ int t0=0; while(t0<np && (strict? pr[t0]<=i : pr[t0]<i)) t0++;
      for(int j=i+1;j<=h;j++){ int ok=0; for(int w=t0/64; w<W && !ok; w++){ uint64_t m=bs[(size_t)i*W+w]&bs[(size_t)j*W+w]; if(w==t0/64) m&= ~0ULL<<(t0%64); if(m) ok=1; }
        if(!ok){ printf("FAIL n=%d i=%d j=%d\n",n,i,j); fails++; } } } }
  printf("BRUTE DONE N=%d strict=%d fails=%ld\n",N,strict,fails); return 0; }
