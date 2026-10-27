// SPDX-License-Identifier: AGPL-3.0-or-later
/* Fast counter for A396618(n) (n>=10): k = q*10^8 + t. Suffix tests d<=8 depend only on t (precomputed table);
   d=9..n-1 tested per candidate with a mod-9009 quadratic-residue prefilter and exact integer sqrt.
   Usage: search n part nparts */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdint.h>
typedef unsigned __int128 u128; typedef uint64_t u64;
#define T8 100000000ULL
#define T16 10000000000000000ULL
#define MQ 9009
static unsigned char qr[MQ]; static u64 P[20];
static inline int sq64(u64 r){ if(!qr[r%MQ]) return 0; u64 s=(u64)sqrt((double)r); while(s*s>r) s--; while((s+1)*(s+1)<=r) s++; return s*s==r; }
static inline int sq128(u128 r,unsigned m){ if(!qr[m]) return 0; u64 s=(u64)sqrtl((long double)r); while((u128)s*s>r) s--; while((u128)(s+1)*(s+1)<=r) s++; return (u128)s*s==r; }
static u64 isq(u128 r){ u64 s=(u64)sqrtl((long double)r); while((u128)s*s>r) s--; while((u128)(s+1)*(s+1)<=r) s++; return s; }
int main(int c,char**v){
  int n=atoi(v[1]), part=atoi(v[2]), np=atoi(v[3]);
  for(int i=0;i<MQ;i++) qr[(u64)i*i%MQ]=1;
  P[0]=1; for(int i=1;i<20;i++) P[i]=P[i-1]*10;
  u128 lo10=1; for(int i=0;i<n-1;i++) lo10*=10; u128 hi10=lo10*10-1;
  u64 lo=isq(lo10); if((u128)lo*lo<lo10) lo++; u64 hi=isq(hi10);
  /* table of t mod 10^8 surviving d=1..8 */
  uint32_t *S=malloc(sizeof(uint32_t)*20000000); u64 ns=0;
  for(u64 t=0;t<T8;t++){ u64 r=t*t; int ok=1; for(int d=1;d<=8&&ok;d++) if(sq64(r%P[d])) ok=0; if(ok) S[ns++]=(uint32_t)t; }
  fprintf(stderr,"table survivors %llu\n",(unsigned long long)ns);
  u64 q0=lo/T8, q1=hi/T8; u64 nq=q1-q0+1;
  u64 qa=q0+nq*part/np, qb=q0+nq*(part+1)/np; /* [qa,qb) */
  u64 m16 = T16%MQ; u64 cnt=0;
  for(u64 q=qa;q<qb;q++){
    for(u64 i=0;i<ns;i++){
      u64 t=S[i]; u64 k=q*T8+t; if(k<lo||k>hi) continue;
      u64 m=2*q*t; u64 L=t*t+(m%T8)*T8; u64 H=q*q+m/T8; if(L>=T16){L-=T16;H++;}
      int ok=1;
      for(int d=9; d<n && d<=16 && ok; d++) if(sq64(L%P[d])) ok=0;
      for(int d=17; d<n && ok; d++){ u64 h=H%P[d-16]; unsigned mm=(unsigned)(((h%MQ)*m16+L%MQ)%MQ);
        if(sq128((u128)h*T16+L,mm)) ok=0; }
      cnt+=ok;
    }
  }
  printf("%llu\n",(unsigned long long)cnt); return 0;
}
