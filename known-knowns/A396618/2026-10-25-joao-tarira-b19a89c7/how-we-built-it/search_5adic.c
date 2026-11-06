// SPDX-License-Identifier: AGPL-3.0-or-later
/* A396618(n) counter by a 5-adic/2-adic argument (no square roots, no QR filters).
   Fact: N = k^2 mod 10^d is a perfect square s^2 (0 <= s^2 < 10^d)  iff  some s <= B_d = isqrt(10^d-1) has
   s^2 == k^2 (mod 5^d) and (mod 2^d).  If 5 does not divide k, then 5 does not divide s, and since (Z/5^d)^* is cyclic,
   s == +-k (mod 5^d); because B_d < 5^d, s is r or 5^d-r where r = k mod 5^d.  So each d costs O(1).
   If 5 | k: k == 0 mod 10 -> k^2 mod 10 = 0 (square); k == 5 mod 10 -> k^2 mod 100 = 25 (square). Excluded for n >= 3.
   Structure: k = q*W + t, W = 10^6; table of t (mod 10^6) passing d = 1..6; d = 7..n-1 per candidate.
   Usage: padic n part nparts   (n >= 8) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
typedef uint64_t u64; typedef unsigned __int128 u128;
#define W 1000000ULL
static u64 M5[30], B[30], MASK[30];
static u64 isq(u128 x){ u64 s=0; for(int b=62;b>=0;b--){ u64 c=s|(1ULL<<b); if((u128)c*c<=x) s=c; } return s; }
/* does d fail for k (5 not dividing k), given r = k mod 5^d and kk = k*k mod 2^64 */
static inline int fails(u64 r,u64 kk,int d){
  if(r<=B[d]){ u64 s=r; if(((s*s-kk)&MASK[d])==0) return 1; }
  if(M5[d]-r<=B[d]){ u64 s=M5[d]-r; if(((s*s-kk)&MASK[d])==0) return 1; }
  return 0; }
int main(int c,char**v){
  int n=atoi(v[1]), part=atoi(v[2]), np=atoi(v[3]);
  M5[0]=1; u128 p10=1;
  for(int d=1;d<30;d++){ M5[d]=M5[d-1]*5; p10*=10; if(d<=24) B[d]=isq(p10-1); MASK[d]=(d>=64)?~0ULL:((1ULL<<d)-1); }
  u128 lo10=1; for(int i=0;i<n-1;i++) lo10*=10;
  u64 lo=isq(lo10-1)+1, hi=isq(lo10*10-1);      /* lo^2 >= 10^(n-1), hi^2 < 10^n */
  /* table: t in [0,W) with 5 !| t passing d=1..6 (k mod 10^6 = t determines these) */
  uint32_t *T=malloc(4*W), *T7=malloc(4*W), *T8=malloc(4*W); u64 ns=0;
  for(u64 t=0;t<W;t++){ if(t%5==0) continue; u64 kk=t*t; int ok=1;
    for(int d=1;d<=6&&ok;d++) if(fails(t%M5[d],kk,d)) ok=0;
    if(ok){ T[ns]=t; T7[ns]=t%M5[7]; T8[ns]=t%M5[8]; ns++; } }
  fprintf(stderr,"table %llu\n",(unsigned long long)ns);
  u64 q0=lo/W, q1=hi/W, nq=q1-q0+1, qa=q0+nq*part/np, qb=q0+nq*(part+1)/np; u64 cnt=0;
  for(u64 q=qa;q<qb;q++){
    u64 a[30]; for(int d=7;d<n;d++) a[d]=(q*W)%M5[d];
    for(u64 i=0;i<ns;i++){
      u64 t=T[i], k=q*W+t; if(k<lo||k>hi) continue;
      u64 kk=k*k; int bad=0;
      { u64 r=a[7]+T7[i]; if(r>=M5[7]) r-=M5[7]; bad|=fails(r,kk,7); }
      if(n>8){ u64 r=a[8]+T8[i]; if(r>=M5[8]) r-=M5[8]; bad|=fails(r,kk,8); }
      for(int d=9; d<n; d++){ u64 r=a[d]+t; if(r>=M5[d]) r-=M5[d];
        if(r<=B[d] || M5[d]-r<=B[d]) bad|=fails(r,kk,d); }
      cnt+=!bad;
    }
  }
  printf("%llu\n",(unsigned long long)cnt); return 0; }
