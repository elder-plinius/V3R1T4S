/* seg699: indep699.c (run 2026-10-14-1615, replicator) with the smallest-prime-factor table replaced by a segmented
   factor sieve over [A - 1000, B], so memory stays about 60 MB at n ~ 10^9. Same method otherwise:
   For each n and each i with no prime in [n-i+1, n] (otherwise that prime divides both binomials, BRIEF R1):
   P(n,i) = primes p >= i dividing C(n,i), found completely as
     p > i : the prime factors > i of n, n-1, ..., n-i+1 (smallest-prime-factor table; p | C(n,i) iff n mod p < i),
     p = i : i prime and v_i(C(n,i)) > 0, tested by Legendre's formula.
   A counterexample j in (i, n/2] has every base-p digit <= that of n for every p in P(n,i) (Lucas). Candidates are
   enumerated by CRT on the lowest digit (j mod p <= n mod p) over primes of P(n,i) whose product just exceeds n/2,
   then each candidate gets the full Lucas test in every base of P(n,i). Survivors are printed.
   Usage: indep699 A B STRICT(0/1)   (STRICT: only p > i)  */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
#define W 12
static u64 LO, HI; static uint32_t *fac; static uint8_t *nf;   /* distinct prime factors of x in [LO, HI] */
static void segsieve(u64 lo,u64 hi){ LO=lo; HI=hi; u64 L=hi-lo+1; fac=malloc(L*W*4); nf=calloc(L,1); u64 *rem=malloc(L*8);
  for(u64 t=0;t<L;t++) rem[t]=lo+t;
  u64 r=1; while((r+1)*(r+1)<=hi) r++;
  uint8_t *c=calloc(r+1,1);
  for(u64 p=2;p<=r;p++) if(!c[p]){ for(u64 q=p*p;q<=r;q+=p) c[q]=1;
      for(u64 m=((lo+p-1)/p)*p; m<=hi; m+=p){ u64 t=m-lo; if(rem[t]==0) continue; fac[t*W+nf[t]++]=(uint32_t)p; while(rem[t]%p==0) rem[t]/=p; } }
  for(u64 t=0;t<L;t++) if(rem[t]>1) fac[t*W+nf[t]++]=(uint32_t)rem[t];
  free(rem); free(c); }
static int isprime(u64 x){ if(x<LO||x>HI){ fprintf(stderr,"ERROR out of segment %llu\n",(unsigned long long)x); exit(2);} u64 t=x-LO; return x>=2 && nf[t]==1 && fac[t*W]==x; }
static int smallprime(u64 x){ if(x<2) return 0; for(u64 d=2;d*d<=x;d++) if(x%d==0) return 0; return 1; }
static u64 legendre(u64 m,u64 p){ u64 v=0; while(m){ m/=p; v+=m; } return v; }
static int lucas_ok(u64 j,u64 n,u64 p){ while(j){ if(j%p>n%p) return 0; j/=p; n/=p; } return 1; }
static u64 modinv(u64 a,u64 m){ /* a, m coprime */ long long t=0,nt=1; long long r=(long long)m, nr=(long long)(a%m);
  while(nr){ long long q=r/nr, x; x=t-q*nt; t=nt; nt=x; x=r-q*nr; r=nr; nr=x; } if(t<0) t+=(long long)m; return (u64)t; }
static u64 P[4096], K[4096]; static int nP;
static u64 *res, *res2; static size_t cap;
static long long cands=0, enumerated=0, cases=0, overflow=0;
int main(int argc,char**argv){
  u64 A=strtoull(argv[1],0,10), B=strtoull(argv[2],0,10); int strict=atoi(argv[3]);
  segsieve(A>1004?A-1000:0,B); cap=1<<20; res=malloc(cap*8); res2=malloc(cap*8);
  for(u64 n=(A<4?4:A); n<=B; n++){
    u64 half=n/2;
    for(u64 i=1;i<half;i++){
      if(isprime(n-(i-1))) break;            /* a prime in [n-i+1, n]: this i and all larger i are settled */
      cases++; nP=0;
      for(u64 k=0;k<i;k++){ u64 m=n-k; if(m<LO){ fprintf(stderr,"ERROR below segment\n"); exit(2);} u64 tt0=m-LO; for(int f=0;f<nf[tt0];f++){ u64 p=fac[tt0*W+f];
          if(p>i){ int seen=0; for(int t=0;t<nP;t++) if(P[t]==p){seen=1;break;} if(!seen){ P[nP]=p; K[nP]=n%p; nP++; } } } }
      if(!strict && smallprime(i) && legendre(n,i)-legendre(i,i)-legendre(n-i,i)>0){ P[nP]=i; K[nP]=n%i; nP++; }
      if(nP==0){ printf("ERROR empty P n=%llu i=%llu\n",(unsigned long long)n,(unsigned long long)i); continue; }
      /* order by density (K+1)/P ascending, take primes until the modulus exceeds n/2 */
      for(int a=1;a<nP;a++){ u64 p=P[a],k=K[a]; int b=a-1; while(b>=0 && (u128)(K[b]+1)*p > (u128)(k+1)*P[b]){ P[b+1]=P[b]; K[b+1]=K[b]; b--; } P[b+1]=p; K[b+1]=k; }
      size_t nr=1; res[0]=0; u64 M=1; int used=0;
      for(int t=0;t<nP && M<=half;t++){
        u64 p=P[t], k=K[t]; size_t need=nr*(k+1);
        if(need>cap){ overflow++; break; }
        u64 inv=modinv(M%p,p); size_t m2=0;
        for(size_t s=0;s<nr;s++) for(u64 r=0;r<=k;r++){
          /* x' = x + M * ((r - x) * inv mod p) */
          u64 x=res[s]; u64 d=((r+p-(x%p))%p); u64 tt=(u64)(((u128)d*inv)%p); res2[m2++]=x+M*tt; }
        u64 *sw=res; res=res2; res2=sw; nr=m2; M*=p; used++;
      }
      for(size_t s=0;s<nr;s++) for(u64 j=res[s]; j<=half; j+=M){
        if(j<=i) continue;
        enumerated++;
        int ok=1; for(int t=0;t<nP && ok;t++) ok=lucas_ok(j,n,P[t]);
        if(ok){ cands++; printf("CANDIDATE n=%llu i=%llu j=%llu\n",(unsigned long long)n,(unsigned long long)i,(unsigned long long)j); }
        if(M>half) break;
      }
    }
  }
  printf("DONE A=%llu B=%llu strict=%d cases=%lld enumerated=%lld overflow=%lld candidates=%lld\n",(unsigned long long)A,(unsigned long long)B,strict,cases,enumerated,overflow,cands);
  return 0;
}
