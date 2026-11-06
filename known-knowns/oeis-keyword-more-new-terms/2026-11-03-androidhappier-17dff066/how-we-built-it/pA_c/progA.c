/* Program A (A331783): locally disjoint rooted semi-identity trees.
   A tree of size n = a set S of distinct NON-LEAF trees (ids, strictly increasing) with pairwise disjoint child-id sets,
   plus k = n-1-size(S) >= 0 leaf children. Each S with size(S) <= n-1 gives exactly one tree.
   Stored per tree: size and its DISTINCT child ids (leaf id 0 included if k > 0).  Usage: progA N [nodisj] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef struct { int size; int nch; long off; } T;
static T *tr; static long ntr=0, cap=0; static int *ch; static long chn=0, chcap=0;
static int *mark; static int nodisj=0;
static int cur[64]; static int ncur; static long cnt; static int store; static long limit;
static void addtree(int size,int haveleaf){
  int m=ncur+haveleaf;
  if(ntr==cap){cap=cap?cap*2:1024; tr=realloc(tr,sizeof(T)*cap);}
  if(chn+m>chcap){chcap=chcap?chcap*2:4096; while(chn+m>chcap) chcap*=2; ch=realloc(ch,sizeof(int)*chcap);}
  tr[ntr].size=size; tr[ntr].nch=m; tr[ntr].off=chn;
  if(haveleaf) ch[chn++]=0;
  memcpy(ch+chn,cur,sizeof(int)*ncur); chn+=ncur; ntr++;
}
static void rec(long minid,int rem,int size){
  /* current S is valid: fill remaining rem with leaves */
  cnt++; if(store) addtree(size, rem>0);
  for(long id=minid; id<limit; id++){
    T t=tr[id]; if(t.size>rem) break;
    int ok=1;
    if(!nodisj) for(int k=0;k<t.nch;k++) if(mark[ch[t.off+k]]){ok=0;break;}
    if(!ok) continue;
    if(!nodisj) for(int k=0;k<t.nch;k++) mark[ch[t.off+k]]=1;
    cur[ncur++]=(int)id;
    rec(id+1,rem-t.size,size);
    ncur--;
    if(!nodisj) for(int k=0;k<t.nch;k++) mark[ch[t.off+k]]=0;
  }
}
int main(int argc,char**argv){
  int N=atoi(argv[1]); if(argc>2) nodisj=1;
  ncur=0; addtree(1,0); printf("1 1\n"); fflush(stdout);
  for(int n=2;n<=N;n++){
    limit=ntr; mark=realloc(mark,sizeof(int)*(ntr+1)); memset(mark,0,sizeof(int)*(ntr+1));
    store=(n<N); cnt=0; ncur=0;
    rec(1,n-1,n);   /* ids >= 1 are non-leaf trees */
    printf("%d %ld\n",n,cnt); fflush(stdout);
  }
  return 0;
}
