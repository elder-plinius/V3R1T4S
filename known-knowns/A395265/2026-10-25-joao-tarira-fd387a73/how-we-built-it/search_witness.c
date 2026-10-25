// SPDX-License-Identifier: AGPL-3.0-or-later
// bidirectional min-diameter g-Golomb search: N marks in [0,D], each positive difference occurs <= G times.
// Marks placed alternately from the left (0,...) and from the right (D,...); mirror broken by x1 <= D-x[N-2].
// usage: gb G N D a(1) .. a(N-1) [-s S M]   (-s: only branches with (first-level index % M)==S)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int G,N,D,A[64],X[64]; static unsigned char cnt[1024];
static int placed[64],np=0; // positions placed (for diff counting)
static long long nodes=0; static int SS=0,MM=1; static long long lvl1=0;
static int capbound(int a,int b,int k){ // k unplaced marks strictly inside (a,b)
  int K=k+2, L=b-a; int need=K*(K-1)/2-1; static long pref[4096]; int c=0; long s=0;
  for(int d=1; d<L && c<need; d++){ int av=G-cnt[d]; while(av-->0 && c<need){ s+=d; pref[++c]=s; } }
  int M=0;
  for(int t=1;t<K-1;t++){ M+=K-t; if(M>c) return 0; if(pref[M] > (long)t*(t+1)/2*L) return 0; }
  return 1;
}
static int add(int p){ int i; for(i=0;i<np;i++){ int d=p>placed[i]?p-placed[i]:placed[i]-p; if(cnt[d]>=G){ for(int j=0;j<i;j++){int e=p>placed[j]?p-placed[j]:placed[j]-p; cnt[e]--;} return 0;} cnt[d]++; } placed[np++]=p; return 1; }
static void rem(void){ int p=placed[--np]; for(int i=0;i<np;i++){ int d=p>placed[i]?p-placed[i]:placed[i]-p; cnt[d]--; } }
// X[i] final positions; left filled 0..nl-1, right filled N-1 .. N-nr
static int rec(int nl,int nr){
  nodes++;
  int k=N-nl-nr;
  if(k==0) return 1;
  int left = (nl<=nr);
  int idx = left? nl : N-1-nr;
  int lo,hi;
  if(left){ lo=X[nl-1]+1; hi=X[N-nr]-1; } else { lo=X[nl-1]+1; hi=X[N-nr]-1; }
  // subruler bounds vs all placed marks
  for(int i=0;i<nl;i++){ int t=X[i]+A[idx-i+1]; if(t>lo) lo=t; }
  for(int j=N-nr;j<N;j++){ int t=X[j]-A[j-idx+1]; if(t<hi) hi=t; }
  if(!left && nr==1){ int t=D-X[1]; if(t>lo) lo=t; } // mirror: D - x[N-2] <= x[1]  ->  x[N-2] >= D-x[1]
  int first = (nl+nr==2 && left); // first branching level: x[1]
  for(int p=(left?lo:hi); left? p<=hi : p>=lo; p+= left?1:-1){
    if(first){ if((lvl1++)%MM!=SS) continue; }
    if(!add(p)) continue;
    X[idx]=p;
    int a,b; if(left){a=p;b=X[N-nr];} else {a=X[nl-1];b=p;}
    int nk=k-1;
    int ok=1;
    if(nk>=1){ if(b-a < A[nk+2]) ok=0; else if(nk>=2 && !capbound(a,b,nk)) ok=0; }
    if(ok){ if(rec(left?nl+1:nl, left?nr:nr+1)) return 1; }
    rem();
  }
  return 0;
}
int main(int c,char**v){ G=atoi(v[1]); N=atoi(v[2]); D=atoi(v[3]);
  int k=4; for(int i=1;i<N;i++) A[i]=atoi(v[k++]); A[N]=D; for(int i=N+1;i<64;i++)A[i]=1<<20;
  for(;k<c;k++) if(!strcmp(v[k],"-s")){ SS=atoi(v[k+1]); MM=atoi(v[k+2]); k+=2; }
  X[0]=0; X[N-1]=D; add(0); add(D);
  int r = N==2 ? 1 : rec(1,1);
  if(r){ printf("FOUND"); for(int i=0;i<N;i++)printf(" %d",X[i]); printf(" nodes %lld\n",nodes);} else printf("NONE nodes %lld\n",nodes);
  return 0; }
