// Independent second code: log-sum Mobius sieve (no products), segment 2^15, blocks of B (default 125e6).
// Output per block: "b sum maxpref minpref". scan mode: "scan lo hi M0 T".
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <omp.h>
#define SEG (1u<<15)
static uint32_t *pr; static uint16_t *lg; static int np;
static void primes(uint64_t lim){ char *c=calloc(lim+1,1); pr=malloc(4*(lim/2+10)); lg=malloc(2*(lim/2+10)); np=0;
 for(uint64_t i=2;i<=lim;i++) if(!c[i]){ pr[np]=i; lg[np]=(uint16_t)lround(16.0*log2((double)i)); np++; for(uint64_t j=i*i;j<=lim;j+=i)c[j]=1; } free(c);}
static void seg(uint64_t lo,uint32_t len,int8_t*mu,uint16_t*ls){
 uint64_t hi=lo+len-1; memset(ls,0,2*len); for(uint32_t i=0;i<len;i++)mu[i]=1;
 for(int k=0;k<np;k++){ uint64_t p=pr[k]; if(p*p>hi)break; uint16_t l=lg[k];
  for(uint64_t j=(lo+p-1)/p*p;j<=hi;j+=p){ mu[j-lo]=-mu[j-lo]; ls[j-lo]+=l; }
  uint64_t q=p*p; for(uint64_t j=(lo+q-1)/q*q;j<=hi;j+=q) mu[j-lo]=0; }
 if(lo<(1u<<20)){ for(uint32_t i=0;i<len;i++) if(mu[i] && (double)ls[i] < 12.0*log2((double)(lo+i))) mu[i]=-mu[i]; }
 else { double t=12.0*log2((double)lo); for(uint32_t i=0;i<len;i++) if(mu[i] && (double)ls[i] < t) mu[i]=-mu[i]; }
}
int main(int c,char**v){
 if(!strcmp(v[1],"blocks")){ uint64_t B=strtoull(v[2],0,10),b0=strtoull(v[3],0,10),b1=strtoull(v[4],0,10); primes((uint64_t)sqrt((double)(b1*B))+10);
  #pragma omp parallel
  { int8_t*mu=malloc(SEG); uint16_t*ls=malloc(2*SEG);
   #pragma omp for schedule(dynamic,1)
   for(uint64_t b=b0;b<b1;b++){ int64_t s=0,mx=0,mn=0; uint64_t lo=b*B+1,end=(b+1)*B;
    for(uint64_t x=lo;x<=end;x+=SEG){ uint32_t len=(end-x+1<SEG)?end-x+1:SEG; seg(x,len,mu,ls); for(uint32_t i=0;i<len;i++){s+=mu[i]; if(s>mx)mx=s; if(s<mn)mn=s;} }
    #pragma omp critical
    { printf("%llu %lld %lld %lld\n",(unsigned long long)b,(long long)s,(long long)mx,(long long)mn); fflush(stdout);} } }
 } else { uint64_t lo=strtoull(v[2],0,10),hi=strtoull(v[3],0,10); int64_t M=strtoll(v[4],0,10),T=strtoll(v[5],0,10); primes((uint64_t)sqrt((double)hi)+10);
  int8_t*mu=malloc(SEG); uint16_t*ls=malloc(2*SEG);
  for(uint64_t x=lo;x<=hi;x+=SEG){ uint32_t len=(hi-x+1<SEG)?hi-x+1:SEG; seg(x,len,mu,ls); for(uint32_t i=0;i<len;i++){ M+=mu[i]; if(M==T||M==-T){printf("first k=%llu M=%lld\n",(unsigned long long)(x+i),(long long)M);return 0;} } }
  printf("none M_end=%lld\n",(long long)M);} return 0;}
