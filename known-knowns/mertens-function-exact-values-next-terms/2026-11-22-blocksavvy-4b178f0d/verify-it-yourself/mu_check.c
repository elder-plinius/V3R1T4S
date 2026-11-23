/* Standalone Mertens/Mobius checker, written from the definition for this package.
 * mu(n) = 0 if p^2 | n for some prime p, otherwise (-1)^(number of prime factors of n).
 * M(x) = sum_{n<=x} mu(n).
 * Method (residual division): rem[n] starts at n; for every prime p <= sqrt(hi) dividing n, divide rem by p
 * (mu = 0 if p divides it twice) and flip the sign; a leftover rem > 1 is one prime > sqrt(hi): flip once more.
 *
 * Modes:
 *   mu_check blocks B b0 b1      for b in [b0,b1): block [b*B+1,(b+1)*B]; prints "b sum maxpref minpref"
 *                                (prefixes over k in the block, relative to the block start, non-empty)
 *   mu_check scan lo hi M0 T     M0 = M(lo-1); prints "first k=<k> M=<M>" for the first k in [lo,hi] with
 *                                |M(k)| >= T, else "none M_end=<M(hi)>"
 *   mu_check range lo hi         prints mu(n) for n in [lo,hi], one per line (for brute-force validation)
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#ifdef _OPENMP
#include <omp.h>
#endif
#define SEG 1048576u
static uint32_t *P; static long NP;
static uint64_t isqrt64(uint64_t n){ uint64_t r=0; while((r+1)*(r+1)<=n) r++; return r; }
static uint64_t isqrt_fast(uint64_t n){ uint64_t r=1; while(r*r<=n) r<<=1; uint64_t lo=r>>1, hi=r;
  while(lo+1<hi){ uint64_t m=(lo+hi)/2; if(m*m<=n) lo=m; else hi=m; } return lo; }
static void primes_upto(uint64_t L){ char *c=calloc(L+2,1); P=malloc(sizeof(uint32_t)*(L/2+16)); NP=0;
  for(uint64_t i=2;i<=L;i++) if(!c[i]){ P[NP++]=(uint32_t)i; for(uint64_t j=i*i;j<=L;j+=i) c[j]=1; } free(c); }
static void mu_seg(uint64_t lo, uint32_t len, int8_t *mu, uint64_t *rem){
  uint64_t hi=lo+len-1;
  for(uint32_t i=0;i<len;i++){ mu[i]=1; rem[i]=lo+i; }
  for(long k=0;k<NP;k++){ uint64_t p=P[k]; if(p*p>hi) break;
    uint64_t s=((lo+p-1)/p)*p;
    for(uint64_t j=s;j<=hi;j+=p){ uint32_t i=(uint32_t)(j-lo); if(!mu[i]) continue;
      rem[i]/=p; if(rem[i]%p==0){ mu[i]=0; continue; } mu[i]=-mu[i]; } }
  for(uint32_t i=0;i<len;i++) if(mu[i] && rem[i]>1) mu[i]=-mu[i];
  if(lo==0) mu[0]=0; /* n = 0 is never used */
}
int main(int argc,char**argv){
  if(argc<2){ fprintf(stderr,"usage: see source\n"); return 2; }
  if(!strcmp(argv[1],"blocks") && argc==5){
    uint64_t B=strtoull(argv[2],0,10), b0=strtoull(argv[3],0,10), b1=strtoull(argv[4],0,10);
    primes_upto(isqrt_fast(b1*B)+2);
    #pragma omp parallel
    { int8_t *mu=malloc(SEG); uint64_t *rem=malloc(8*(size_t)SEG);
      #pragma omp for schedule(dynamic,1)
      for(long long bb=(long long)b0; bb<(long long)b1; bb++){ uint64_t b=(uint64_t)bb;
        uint64_t lo=b*B+1, end=(b+1)*B; long long s=0, mx=-(1LL<<62), mn=(1LL<<62);
        for(uint64_t x=lo;x<=end;x+=SEG){ uint32_t len=(end-x+1<SEG)?(uint32_t)(end-x+1):SEG; mu_seg(x,len,mu,rem);
          for(uint32_t i=0;i<len;i++){ s+=mu[i]; if(s>mx) mx=s; if(s<mn) mn=s; } }
        #pragma omp critical
        { printf("%llu %lld %lld %lld\n",(unsigned long long)b,s,mx,mn); fflush(stdout); } }
      free(mu); free(rem); }
    return 0;
  }
  if(!strcmp(argv[1],"scan") && argc==6){
    uint64_t lo=strtoull(argv[2],0,10), hi=strtoull(argv[3],0,10); long long M=strtoll(argv[4],0,10), T=strtoll(argv[5],0,10);
    primes_upto(isqrt_fast(hi)+2); int8_t *mu=malloc(SEG); uint64_t *rem=malloc(8*(size_t)SEG);
    for(uint64_t x=lo;x<=hi;x+=SEG){ uint32_t len=(hi-x+1<SEG)?(uint32_t)(hi-x+1):SEG; mu_seg(x,len,mu,rem);
      for(uint32_t i=0;i<len;i++){ M+=mu[i]; if(M>=T||M<=-T){ printf("first k=%llu M=%lld\n",(unsigned long long)(x+i),M); return 0; } } }
    printf("none M_end=%lld\n",M); return 0;
  }
  if(!strcmp(argv[1],"range") && argc==4){
    uint64_t lo=strtoull(argv[2],0,10), hi=strtoull(argv[3],0,10);
    primes_upto(isqrt_fast(hi)+2); int8_t *mu=malloc(SEG); uint64_t *rem=malloc(8*(size_t)SEG);
    for(uint64_t x=lo;x<=hi;x+=SEG){ uint32_t len=(hi-x+1<SEG)?(uint32_t)(hi-x+1):SEG; mu_seg(x,len,mu,rem);
      for(uint32_t i=0;i<len;i++) printf("%d\n",mu[i]); }
    return 0;
  }
  (void)isqrt64; fprintf(stderr,"bad arguments\n"); return 2;
}
