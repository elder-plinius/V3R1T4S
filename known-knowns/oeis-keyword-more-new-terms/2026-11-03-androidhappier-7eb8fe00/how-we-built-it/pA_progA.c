/* Program A: count locally disjoint rooted identity trees (A316471) by canonical-id backtracking.
   Tree = strictly increasing set of branch ids (ids assigned in size order); branches' child-sets pairwise disjoint.
   Usage: progA N [nodisj]   prints "n a(n)" for n=1..N. Trees of size <= N-1 are stored. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct { int size; int nch; int off; } T;
static T *tr; static int ntr=0, cap=0; static int *ch; static long chn=0, chcap=0;
static int *mark; static int nodisj=0;
static int cur[64]; static int ncur;
static int sizestart[64];
static long cnt; static int store;
static void addtree(int size){
  if(ntr==cap){cap=cap?cap*2:1024; tr=realloc(tr,sizeof(T)*cap);}
  if(chn+ncur>chcap){chcap=chcap?chcap*2:4096; while(chn+ncur>chcap) chcap*=2; ch=realloc(ch,sizeof(int)*chcap);}
  tr[ntr].size=size; tr[ntr].nch=ncur; tr[ntr].off=chn;
  memcpy(ch+chn,cur,sizeof(int)*ncur); chn+=ncur; ntr++;
}
static int limit; /* number of trees usable as branches (ids < limit) */
static void rec(int minid,int rem,int size){
  if(rem==0){ cnt++; if(store) addtree(size); return; }
  for(int id=minid; id<limit; id++){
    T t=tr[id]; if(t.size>rem) break;
    int ok=1;
    if(!nodisj) for(int k=0;k<t.nch;k++) if(mark[ch[t.off+k]]){ok=0;break;}
    if(!ok) continue;
    if(!nodisj) for(int k=0;k<t.nch;k++) mark[ch[t.off+k]]=1;
    cur[ncur++]=id;
    rec(id+1,rem-t.size,size);
    ncur--;
    if(!nodisj) for(int k=0;k<t.nch;k++) mark[ch[t.off+k]]=0;
  }
}
int main(int argc,char**argv){
  int N=atoi(argv[1]); if(argc>2) nodisj=1;
  ncur=0; addtree(1); printf("1 1\n"); fflush(stdout);
  for(int n=2;n<=N;n++){
    limit=ntr; mark=realloc(mark,sizeof(int)*(ntr+1)); memset(mark,0,sizeof(int)*(ntr+1));
    store=(n<N); cnt=0; ncur=0;
    rec(0,n-1,n);
    printf("%d %ld\n",n,cnt); fflush(stdout);
  }
  return 0;
}
