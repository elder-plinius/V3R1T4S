// SPDX-License-Identifier: AGPL-3.0-or-later
/* Brute-force counter for OEIS A396618(n), n>=2:
   number of n-digit squares N such that for every d=1..n-1, N mod 10^d is NOT a perfect square
   (0 counts as a square, matching Mathematica IntegerQ[Sqrt[0]]).
   Usage: verify n [part nparts]  -> prints count for k in its share of [ceil(sqrt(10^(n-1))), floor(sqrt(10^n-1))]. */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
typedef unsigned __int128 u128; typedef unsigned long long u64;
static u128 P10[40];
static u64 isqrt128(u128 r){ u64 s=(u64)sqrtl((long double)r); while((u128)s*s>r) s--; while((u128)(s+1)*(s+1)<=r) s++; return s; }
static int issq(u128 r){ u64 s=isqrt128(r); return (u128)s*s==r; }
int main(int c,char**v){
  int n=atoi(v[1]); int part=c>3?atoi(v[2]):0, np=c>3?atoi(v[3]):1;
  P10[0]=1; for(int i=1;i<40;i++) P10[i]=P10[i-1]*10;
  u64 lo=isqrt128(P10[n-1]); if((u128)lo*lo<P10[n-1]) lo++;
  u64 hi=isqrt128(P10[n]-1);
  u64 span=hi-lo+1, a=lo+span/np*part, b=(part==np-1)?hi:lo+span/np*(part+1)-1;
  /* N kept as NH*10^12 + NL, updated incrementally N(k+1)=N(k)+2k+1 */
  const u64 T12=1000000000000ULL; u128 N=(u128)a*a; u64 NL=(u64)(N%T12); u128 NH=N/T12;
  u64 cnt=0;
  for(u64 k=a;;k++){
    int ok=1;
    for(int d=1; d<n && ok; d++){
      u128 r = d<=12 ? (u128)(NL%(u64)P10[d]) : (NH%P10[d-12])*T12+NL;
      if(issq(r)) ok=0;
    }
    cnt+=ok;
    if(k==b) break;
    NL+=2*k+1; while(NL>=T12){NL-=T12;NH++;}
  }
  printf("%llu\n",cnt); return 0;
}
