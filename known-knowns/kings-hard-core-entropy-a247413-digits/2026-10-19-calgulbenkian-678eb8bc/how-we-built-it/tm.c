// King-graph transfer matrix, site-by-site frontier DP, exact 128-bit fixed-point power iteration.
// usage: tm m cyc iters nthreads outprefix   (cyc=1 periodic rows, cyc=0 open strip)
#include "stdio.h"
#include "stdlib.h"
#include "stdint.h"
#include "string.h"
#include "pthread.h"
typedef unsigned __int128 u128;
static int m, cyc, NT;
static u128 *cur, *nxt, *vec, *vec2;   // cur/nxt: frontier arrays; vec: compact column vector
static size_t NW, NF;                  // 2^m, frontier size
static int curstep; static int mode;   // mode 0: site step, 1: contract
typedef struct {int t;} targ;
static inline int bit(size_t x,int k){return (x>>k)&1;}
static void *work(void *p){
  int t=((targ*)p)->t; int i=curstep;
  if(mode==1){ // contract frontier -> vec2 over word
    size_t lo=NW*t/NT, hi=NW*(t+1)/NT;
    for(size_t w=lo;w<hi;w++){
      u128 s=cur[w]+cur[w|(1ULL<<m)];
      if(cyc){ s+=cur[w|(2ULL<<m)]+cur[w|(3ULL<<m)]; }
      vec2[w]=s;
    }
    return 0;
  }
  size_t lo=NF*t/NT, hi=NF*(t+1)/NT;
  size_t Abit=1ULL<<m, Bbit=2ULL<<m;
  for(size_t y=lo;y<hi;y++){
    int b=bit(y,i), a=bit(y,m);
    int By=cyc?bit(y,m+1):0;
    // y fields are reachable only if consistent; compute sources
    u128 s=0;
    size_t rest=y & ~((size_t)1<<i) & ~Abit;     // word bits except i, keeps B
    if(i==0){ // cyclic only: A=B=old[0]=a
      size_t w=(y&(NW-1)&~(size_t)1)|(size_t)a;
      if(By!=a || bit(y,m)!=a){nxt[y]=0;continue;}
      if(b==0) s=vec[w];
      else if(a==0 && bit(w,m-1)==0 && bit(w,1)==0) s=vec[w];
      nxt[y]=s; continue;
    }
    // i>=1 : sources x: word bit i = a, A_x in {0,1}
    size_t xbase=rest | ((size_t)a<<i);
    for(int ax=0;ax<2;ax++){
      size_t x=xbase | (ax? Abit:0);
      if(b==0) s+=cur[x];
      else {
        if(ax==0 && a==0 && bit(y,i-1)==0){
          int nxtold;
          if(i<m-1) nxtold=bit(x,i+1);
          else nxtold=cyc?By:0;       // old[m] = old[0] (B) cyclic
          int ok = (nxtold==0);
          if(ok && cyc && i==m-1 && bit(y,0)!=0) ok=0; // new[0]
          if(ok) s+=cur[x];
        }
      }
    }
    nxt[y]=s;
  }
  return 0;
}
static void run(int md,int st){
  mode=md; curstep=st; pthread_t th[64]; targ ta[64];
  for(int t=0;t<NT;t++){ta[t].t=t;pthread_create(&th[t],0,work,&ta[t]);}
  for(int t=0;t<NT;t++)pthread_join(th[t],0);
}
int main(int argc,char**argv){
  int cnt=(argc>6);
  m=atoi(argv[1]);cyc=atoi(argv[2]);int iters=atoi(argv[3]);NT=atoi(argv[4]);char*pre=argv[5];
  NW=(size_t)1<<m; NF=NW<<(cyc?2:1);
  cur=malloc(NF*16); nxt=malloc(NF*16); vec=malloc(NW*16); vec2=malloc(NW*16);
  // initial vec: independent column states = 1
  for(size_t w=0;w<NW;w++){ int ok=!(w&(w>>1)); if(cyc&&m>2&&(w&1)&&((w>>(m-1))&1))ok=0; vec[w]=ok?(cnt?(u128)1:((u128)1<<60)):0; }
  // NOTE open-strip i==0 handled by a generic rewrite below
  for(int it=0;it<=iters;it++){
    int last=(it==iters);
    // step 0 : special
    // build frontier after site 0 directly into cur
    {
      mode=0; curstep=0;
    }
    // generic i=0 for both modes done here serially-parallel:
    {
      size_t Abit=1ULL<<m;
      // inline simple parallel via run with custom code: reuse work() for cyc; open handled here
      if(cyc){ run(0,0); u128*tmp=cur;cur=nxt;nxt=tmp; }
      else {
        // frontier = word | A(old[0]) <<m ; place new[0]
        for(size_t y=0;y<NF;y++){ int b=bit(y,0), a=bit(y,m); size_t w=(y&(NW-1)&~(size_t)1)|(size_t)a; u128 s=0;
          if(b==0) s=vec[w]; else if(a==0 && bit(w,1)==0) s=vec[w];
          cur[y]=s; }
      }
    }
    for(int i=1;i<m;i++){ run(0,i); u128*tmp=cur;cur=nxt;nxt=tmp; }
    run(1,0);
    if(cnt){ if(it==iters-1){ u128 tot=0; for(size_t w=0;w<NW;w++) tot+=vec2[w];
        char buf[64]; int n=0; if(tot==0)buf[n++]='0'; while(tot){buf[n++]='0'+(int)(tot%10);tot/=10;} while(n--)putchar(buf[n]); putchar('\n'); return 0; }
      for(size_t w=0;w<NW;w++) vec[w]=vec2[w]; continue; }
    u128 mx=0; for(size_t w=0;w<NW;w++) if(vec2[w]>mx) mx=vec2[w];
    if(last){
      FILE*f=fopen(strcat(strcpy(malloc(512),pre),".bin"),"wb");
      fwrite(vec,16,NW,f); fwrite(vec2,16,NW,f); fclose(f);
      break;
    }
    int bl=0; u128 t=mx; while(t){bl++;t>>=1;}
    int sh=bl-101;
    for(size_t w=0;w<NW;w++){ vec[w]= sh>=0? (vec2[w]>>sh):(vec2[w]<<(-sh)); }
    if(it%20==0){fprintf(stderr,"it %d sh %d\n",it,sh);}
  }
  return 0;
}
