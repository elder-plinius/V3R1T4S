// SPDX-License-Identifier: AGPL-3.0-or-later
/* Independent exhaustive checker for g-Golomb rulers (written separately from gg2.c).
   Marks are placed from the RIGHT: 0 and D fixed, then interior marks in decreasing order.
   usage: vf g n D B1 B2 ... Bn-1   (Bk = known minimal diameter of a k-mark g-ruler, k=1..n-1)
   prints "EXISTS <ruler>" or "NONE <nodes>". */
#include <stdio.h>
#include <stdlib.h>
int g,n,D,B[64],m[64],c[256]; long long nodes;
/* smallest-possible sums bound for the left segment [0,q] that must hold k marks */
int segok(int q,int k){
  int need=k*(k-1)/2-1, got=0; long s=0, ps[1200];
  for(int d=1; d<q && got<need; d++) for(int a=g-c[d]; a>0 && got<need; a--){ s+=d; ps[++got]=s; }
  int M=0;
  for(int t=1;t<=k-2;t++){ M+=k-t; if(M>got) return 0; if(ps[M] > (long)t*(t+1)/2*q) return 0; }
  return 1;
}
int go(int j){ /* m[0]=D, m[1..j-1] placed decreasing; need marks m[j..n-2], then 0 */
  nodes++;
  if(j==n-1){ return (D-m[1] <= m[n-2]); } /* canonical: first gap <= last gap (mirror) */
  int left=n-j;                              /* marks in [0,q] incl. q and 0 */
  int top=m[j-1]-1, bot=B[left];             /* q >= B(left) */
  for(int i=0;i<j;i++){ int t=m[i]-B[j-i+1]; if(t<top) top=t; } /* m[i]-q >= B(j-i+1) */
  for(int q=top;q>=bot;q--){
    int ok=1,i; c[q]++;
    if(c[q]>g) ok=0;
    for(i=0;i<j && ok;i++){ if(++c[m[i]-q]>g) ok=0; }
    if(ok && (left<=2 || segok(q,left))){ m[j]=q; if(go(j+1)) return 1; }
    c[q]--; for(int r=0;r<i;r++) c[m[r]-q]--;
  }
  return 0;
}
int main(int argc,char**argv){
  g=atoi(argv[1]); n=atoi(argv[2]); D=atoi(argv[3]);
  for(int k=1;k<n;k++) B[k]=atoi(argv[3+k]);
  if(n<=2){ printf(n==1?"EXISTS 0\n":"EXISTS 0 %d\n",D); return 0; }
  m[0]=D; c[D]=1; m[n-1]=0;
  if(go(1)){ printf("EXISTS"); for(int i=n-1;i>=0;i--) printf(" %d",m[i]); printf("\n"); }
  else printf("NONE %lld\n",nodes);
  return 0;
}
