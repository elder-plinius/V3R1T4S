// SPDX-License-Identifier: AGPL-3.0-or-later
// min-diameter g-Golomb ruler search: n marks in [0,D], each positive difference occurs <= G times.
// usage: gg G n D [abound...]  -> prints FOUND ruler or NONE, node count
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int G,N,D; static int A[64]; static int x[64]; static unsigned char cnt[512];
static long long nodes=0; static int found=0; static int SS=0,MM=1; static long long c2=0;
// capacity bound for segment [p,D] containing k=N-m marks after placing p (counts must include p's diffs) -- applied post-placement
static int capbound(int p,int k){
  // pool: avail[d]=G-cnt[d], d=1..D-p-1 ; smallest values sums
  int need=(k*(k-1))/2-1; // diffs inside segment except D-p already counted
  static int pref[2048]; int c=0; long s=0; int L=D-p;
  for(int d=1; d<L && c<need; d++){ int a=G-cnt[d]; while(a-->0 && c<need){ s+=d; pref[++c]=s; } }
  // span-s bound: diffs of span<=s number M=sum_{t=1..s}(k-t); weight sum <= s(s+1)/2 * L ; span k-1 is D-p itself
  int M=0;
  for(int t=1;t<k-1;t++){ M+=k-t; if(M>c) return 0; if(pref[M] > (long)t*(t+1)/2*L) return 0; }
  return 1;
}
static int capok(int p,int m){ return 1; }
static int rec(int m){ // m marks placed: x[0..m-1], plus implicit D at end
  nodes++;
  if(m==N-1){ // check mirror: x1 <= D - x[N-2]
    if(x[1] > D - x[N-2]) return 0;
    found=1; return 1; }
  int lo=x[m-1]+1;
  // need D - p >= A[N-m]  (marks p..D: N-m marks)
  int hi=D-A[N-m];
  if(m>=2){ int h2 = D - x[1]; if(m==N-2 && hi>h2) hi=h2; }
  for(int i=0;i<m;i++){ int t=x[i]+A[m-i+1]; if(t>lo) lo=t; }
  for(int p=lo;p<=hi;p++){
    if(m==2 && (c2++)%MM!=SS) continue;
    if(m<N-2 && !capok(p,m)) { continue; }
    // marks i..m span: p - x[i] >= A[m-i+1] already in lo; also x[i]..D with new count handled by hi
    int ok=1,i;
    if(cnt[D-p]>=G) continue;
    for(i=0;i<m;i++){ if(cnt[p-x[i]]>=G){ok=0;break;} cnt[p-x[i]]++; }
    if(ok){ cnt[D-p]++;
      // careful: if D-p equals some p-x[i], counts accumulated sequentially, recheck
      int bad=0; for(int j=0;j<m;j++) if(cnt[p-x[j]]>G){bad=1;break;}
      if(cnt[D-p]>G) bad=1;
      if(!bad && (m>=N-2 || capbound(p,N-m))){ x[m]=p; if(rec(m+1)) return 1; }
      cnt[D-p]--; }
    for(int j=0;j<i;j++) cnt[p-x[j]]--;
  }
  return 0;
}
int main(int c,char**v){ G=atoi(v[1]); N=atoi(v[2]); D=atoi(v[3]);
  for(int k=1;k<64;k++)A[k]=0; for(int k=4;k<c;k++){ if(!strcmp(v[k],"-s")){SS=atoi(v[k+1]);MM=atoi(v[k+2]);break;} A[k-3]=atoi(v[k]); } // A[1],A[2],... given
  memset(cnt,0,sizeof cnt); x[0]=0; cnt[D]=1; x[N-1]=D;
  if(N==2){ printf("FOUND 0 %d\n",D); return 0;}
  int r=rec(1);
  if(r){ printf("FOUND"); for(int i=0;i<N;i++)printf(" %d",x[i]); printf(" nodes %lld\n",nodes);} else printf("NONE nodes %lld\n",nodes);
  return 0; }
