// Segmented Mobius sieve. Mode "blocks": for blocks [b*B+1, (b+1)*B], b in [b0,b1), output
// "b sum maxpref minpref" (prefix relative to block start). Mode "scan lo hi M0 target": print first k
// in [lo,hi] with |M(k)|==target given M(lo-1)=M0.
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <omp.h>
#define SEG (1u<<17)
static uint32_t *pr; static int np;
static void small_primes(uint64_t lim){ char *c=calloc(lim+1,1); pr=malloc(sizeof(uint32_t)*(lim/2+10)); np=0;
 for(uint64_t i=2;i<=lim;i++){ if(!c[i]){pr[np++]=i; for(uint64_t j=i*i;j<=lim;j+=i)c[j]=1;} } free(c);}
// sieve mu for [lo, lo+len)
static void seg_mu(uint64_t lo, uint32_t len, int8_t *mu, uint64_t *pd){
 uint64_t hi=lo+len-1; for(uint32_t i=0;i<len;i++){mu[i]=1;pd[i]=1;}
 for(int k=0;k<np;k++){ uint64_t p=pr[k]; if(p*p>hi) break;
  uint64_t s=((lo+p-1)/p)*p; for(uint64_t j=s;j<=hi;j+=p){ mu[j-lo]=-mu[j-lo]; pd[j-lo]*=p; }
  uint64_t q=p*p; s=((lo+q-1)/q)*q; for(uint64_t j=s;j<=hi;j+=q) mu[j-lo]=0; }
 for(uint32_t i=0;i<len;i++) if(mu[i] && pd[i]!=lo+i) mu[i]=-mu[i];
}
int main(int argc,char**argv){
 if(argc<2){fprintf(stderr,"usage\n");return 1;}
 if(!strcmp(argv[1],"blocks")){
  uint64_t B=strtoull(argv[2],0,10), b0=strtoull(argv[3],0,10), b1=strtoull(argv[4],0,10);
  small_primes((uint64_t)sqrt((double)(b1*B))+10);
  #pragma omp parallel
  { int8_t *mu=malloc(SEG); uint64_t *pd=malloc(8*SEG);
   #pragma omp for schedule(dynamic,1)
   for(uint64_t b=b0;b<b1;b++){ int64_t s=0,mx=0,mn=0; uint64_t lo=b*B+1, end=(b+1)*B;
    for(uint64_t x=lo;x<=end;x+=SEG){ uint32_t len=(end-x+1<SEG)?(uint32_t)(end-x+1):SEG; seg_mu(x,len,mu,pd);
     for(uint32_t i=0;i<len;i++){ s+=mu[i]; if(s>mx)mx=s; if(s<mn)mn=s; } }
    #pragma omp critical
    { printf("%llu %lld %lld %lld\n",(unsigned long long)b,(long long)s,(long long)mx,(long long)mn); fflush(stdout);} }
  }
 } else { uint64_t lo=strtoull(argv[2],0,10), hi=strtoull(argv[3],0,10); int64_t M=strtoll(argv[4],0,10), T=strtoll(argv[5],0,10);
  small_primes((uint64_t)sqrt((double)hi)+10); int8_t *mu=malloc(SEG); uint64_t *pd=malloc(8*SEG);
  for(uint64_t x=lo;x<=hi;x+=SEG){ uint32_t len=(hi-x+1<SEG)?(uint32_t)(hi-x+1):SEG; seg_mu(x,len,mu,pd);
   for(uint32_t i=0;i<len;i++){ M+=mu[i]; if(M==T||M==-T){ printf("first k=%llu M=%lld\n",(unsigned long long)(x+i),(long long)M); return 0;} } }
  printf("none M_end=%lld\n",(long long)M); }
 return 0;}
