/* Exhaustive verifier for Erdos #699 over n in [A,B] (see BRIEF.md R1-R3).
   For each n: gap = n - prevprime(n); only i <= gap can fail (R1). For each such i, P(n,i) = primes p >= i with
   p | C(n,i): p > i iff n mod p < i (R2); p = i iff floor(n/i) mod i == 0. Large members p > sqrt(n) are p = (n-b)/a.
   Candidate set J of j in (i, n/2] dominated digitwise by n in every base p in P(n,i); a survivor is a counterexample.
   Usage: fast699 A B STRICT(0/1)   prints summary and any counterexample candidates.  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
typedef uint64_t u64;
static uint8_t *sv; static u64 SB;
static int isprime(u64 x){ if(x<2) return 0; if(x==2) return 1; if(!(x&1)) return 0; return !((sv[x>>4]>>((x>>1)&7))&1); }
static void sieve(u64 N){ SB=N; sv=calloc((N>>4)+2,1); for(u64 p=3;p*p<=N;p+=2) if(isprime(p)) for(u64 q=p*p;q<=N;q+=2*p) sv[q>>4]|=1<<((q>>1)&7); }
static int dom(u64 j,u64 n,u64 p){ while(j){ if(j%p>n%p) return 0; j/=p; n/=p; } return 1; }
static u64 *J; static size_t nJ, capJ; static int init;
static u64 *pend; static size_t npend;
static u64 *smallp; static size_t nsmall;
static long long fallbacks=0, nontrivial=0, maxJ=0;
static void filt(u64 n,u64 p){ size_t k=0; for(size_t t=0;t<nJ;t++) if(dom(J[t],n,p)) J[k++]=J[t]; nJ=k; }
static void addJ(u64 v){ if(nJ==capJ){capJ=capJ?2*capJ:1024; J=realloc(J,capJ*8);} J[nJ++]=v; }
static long long dseeds=0;
/* all j in (lo, hi] whose base-p digits are <= those of n (Lucas-dominated), built digit by digit */
static void seedrec(u64 n,u64 p,u64 lo,u64 hi,u64 acc,u64 pw,u64 m){
  if(m==0){ if(acc>lo && acc<=hi) addJ(acc); return; }
  u64 dmax=m%p; for(u64 d=0; d<=dmax; d++){ u64 v=acc+d*pw; if(v>hi) break; seedrec(n,p,lo,hi,v,pw*p,m/p); } }
static void seedfrom(u64 n,u64 p,u64 lo,u64 hi){ seedrec(n,p,lo,hi,0,1,n); }
int main(int argc,char**argv){
  u64 A=strtoull(argv[1],0,10), B=strtoull(argv[2],0,10); int strict=atoi(argv[3]);
  sieve(B+2);
  u64 T0=(u64)sqrtl((long double)B)+2;
  for(u64 p=2;p<=T0;p++) if(isprime(p)){ smallp=realloc(smallp,(nsmall+1)*8); smallp[nsmall++]=p; }
  pend=malloc(8*(nsmall+64));
  u64 pp=0; for(u64 x=A; x>=2; x--) if(isprime(x)){pp=x;break;}
  long long cex=0;
  for(u64 n=A;n<=B;n++){
    if(isprime(n)) { pp=n; continue; }
    if(n<4) continue;
    u64 gap=n-pp, half=n/2; u64 imax = gap < half-1 ? gap : half-1;
    u64 T=(u64)sqrtl((long double)n); while(T*T<=n) T++;   /* T > sqrt(n) */
    for(u64 i=1;i<=imax;i++){
      nontrivial++; nJ=0; init=0; npend=0;
      /* phase 1: p = (n-b)/a >= T, a >= 2 */
      for(u64 a=2; n/a>=T && !(init&&nJ==0); a++){
        for(u64 b=0;b<i && b<=n;b++){
          u64 m=n-b; if(m%a) continue; u64 p=m/a; if(p<T || p<=i) continue;
          if(!isprime(p)) continue;
          if(!init){ for(u64 c=0;c<=a;c++) for(u64 d=0;d<=b;d++){ u64 j=c*p+d; if(j>i && j<=half) addJ(j);} init=1;
                     for(size_t t=0;t<npend;t++) filt(n,pend[t]); }
          else filt(n,p);
          if(init && nJ==0) break;
        }
      }
      if(!(init&&nJ==0)){
        /* phase 2: primes i < p < T with n mod p < i */
        for(size_t t=0;t<nsmall && smallp[t]<T; t++){ u64 p=smallp[t]; if(p<=i) continue; if(n%p<i){ if(init){ filt(n,p); if(!nJ) break;} else pend[npend++]=p; } }
        /* p = i */
        if(!(init&&nJ==0) && !strict && isprime(i) && (n/i)%i==0){ if(init) filt(n,i); else pend[npend++]=i; }
        if(!init){ /* no prime > sqrt(n) in P(n,i): seed J from the pending prime with the fewest dominated numbers */
          size_t best=0; long double bc=1e30L;
          for(size_t t=0;t<npend;t++){ long double c=1; u64 m=n; while(m){ c*=(long double)(m%pend[t]+1); m/=pend[t]; } if(c<bc){bc=c;best=t;} }
          if(npend && bc<=2e7L){ seedfrom(n,pend[best],i,half); dseeds++;
            for(size_t t=0;t<npend && nJ;t++) if(t!=best) filt(n,pend[t]); }
          else { fallbacks++;
            for(u64 j=i+1;j<=half;j++){ int ok=1; for(size_t t=0;t<npend&&ok;t++) ok=dom(j,n,pend[t]); if(ok) addJ(j);} }
          init=1;
        }
      }
      if((long long)nJ>maxJ) maxJ=nJ;
      if(nJ){ for(size_t t=0;t<nJ && t<5;t++) printf("CANDIDATE n=%llu i=%llu j=%llu\n",(unsigned long long)n,(unsigned long long)i,(unsigned long long)J[t]); cex+=nJ; }
    }
  }
  printf("DONE A=%llu B=%llu strict=%d nontrivial_i=%lld digit_seeds=%lld fallbacks=%lld candidates=%lld\n",(unsigned long long)A,(unsigned long long)B,strict,nontrivial,dseeds,fallbacks,cex);
  return 0;
}
